from dataclasses import fields
from rest_framework import serializers
from search.models import para, searchinpara

class paralistSerializer(serializers.ModelSerializer):
    class Meta:
        model = para
        fields = '__all__'

class searchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = searchinpara
        fields = ['word', 'index']