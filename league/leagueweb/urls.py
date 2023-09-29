from django.urls import path
from .views import CustomLoginView, HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # Add other authentication-related views and URLs as needed
]
