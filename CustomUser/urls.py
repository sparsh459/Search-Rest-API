from django.urls import path
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='RegisterUser'),
    path('logout/', LogoutView.as_view(), name='LogoutAPI'),
]