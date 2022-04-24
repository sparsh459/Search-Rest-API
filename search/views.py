from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from search.serializer import paralistSerializer, searchlistSerializer
from search.models import para
from django.core import serializers
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, filters
from drf_yasg.utils import swagger_auto_schema
from url_filter.integrations.drf import DjangoFilterBackend
from drf_yasg import openapi
# from django.core.cache import cache

addpara_respone_scheme_dict ={
    "200": openapi.Response(
        description="Adding paragrapgh to database",
        examples={
            "application/json": [
                {
                    "id": 43,
                    "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
                },
                {
                    "id": 44,
                    "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
                },
                {
                    "id": 45,
                    "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
                }
            ]
        }
    ),
    "400": openapi.Response("Bad Request")
}

allpara_respone_scheme_dict ={
    "200": openapi.Response(
        description="List out the paragraphs in the database",
        examples={
            "application/json": [{
                "id": 1,
                "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
            },
            {
                "id": 2,
                "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
            },
            {
                "id": 3,
                "sentence": "Praesent consequat tortor turpis, ut ullamcorper dolor lobortis a. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam placerat sit amet risus quis hendrerit.Cras blandit purus metus, vel molestie lacus sagittis tincidunt. Nam sed nibh efficitur diam placerat iaculis. Mauris placerat ut odio ut eleifend."
            }
            ]
        }
    ),
    "400": openapi.Response("Bad Request")
}

query_to_search = openapi.Parameter('q', in_=openapi.IN_QUERY, description='Input the word to search the paragraph', type=openapi.TYPE_STRING, operation_description='This endpoint does some magic')

class ParagraphList(generics.ListAPIView):
    """
    List all the paragraphs from the postgresql database
    """
    permission_classes = [IsAuthenticated]

    queryset = para.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['sentence']
    @swagger_auto_schema(responses=allpara_respone_scheme_dict)
    def get(self, request):
        query = self.get_queryset()
        serializer = paralistSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(method='post', responses=addpara_respone_scheme_dict, request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "sentence":openapi.Schema(type=openapi.TYPE_STRING, description="Enter the Paragraph")
    }
))
@api_view(['POST'])
def paralist(request):
    """
    Create new paragraph after every two newline to postgresql db
    """

    if request.method == 'POST':
        todata = request.data['sentence'].split("\n\n\n")
        
        for data in todata:
            request.data['sentence'] = data
            searchdata = request.data['sentence'].split(" ")

            serializeraddpara = paralistSerializer(data=request.data, )
            if serializeraddpara.is_valid():
                serializeraddpara.save()
            serilizerdata = request.data
            
            for word in searchdata:
                serilizerdata['word'] = serilizerdata['sentence']
                serilizerdata['word'] = word
                serilizerdata['index'] = serializeraddpara.data['id']

                serializer = searchlistSerializer(data=serilizerdata)
                if serializer.is_valid():
                    serializer.save()


        if len(serializeraddpara.data) != 0:
            return Response(serializeraddpara.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializeraddpara.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(method='get', manual_parameters=[query_to_search])
@api_view(['GET'])
def getparalist(request):
    """
    search a particular word in the db and returns top 10 paragraphs that contains the word
    """
    query = str(request.GET['q'])
    query = query.lower()
    paragraphs = para.objects.filter(searchinpara__word__contains=query)[:10]
    json_data = serializers.serialize('json',paragraphs)
    if paragraphs:
        return HttpResponse(json_data, content_type='application/json')
    else: 
        return Response("Not Found")