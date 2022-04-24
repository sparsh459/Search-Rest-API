from django.urls import path
from search import views

urlpatterns = [
    path('allpara/',views.ParagraphList.as_view(), name='ListAll'),
    path('addpara/', views.paralist, name='AddPara'),
    path('searchinpara/', views.getparalist, name='SearchInPara'),
]
