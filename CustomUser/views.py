from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
register_response_scheme_dict = {
    "200": openapi.Response(
        description="User Added to the Database",
        examples={
            "application/json":{
                "name": "Surinder Sing",
                "email": "surinder.singh2311@hotmail.com",
                "dob": "2000-1-12"
            }
        }
    ),
    "400": openapi.Response(
        description="Bad Request",
        examples={
            "dob": "Field Required",
            "password": "Field Required"
        }
    )
}

class RegisterView(APIView):
    @swagger_auto_schema(operation_description="Adds a new user to database", responses=register_response_scheme_dict, request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="Enter Your Name"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Enter Your Email"),
            "dob": openapi.Schema(type=openapi.TYPE_STRING, description="Enter your Date of Birth"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Enter Your Password")
        }
    ))
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    @swagger_auto_schema(operation_description="Removes the jwt token of a user thus rendering the session useless and the user has to login again")
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response