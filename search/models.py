from django.db import models

# Create your models here.

class para(models.Model):
    sentence = models.TextField()
    
class searchinpara(models.Model):
    word = models.CharField(max_length=40)
    index = models.ForeignKey(para, on_delete=models.CASCADE)