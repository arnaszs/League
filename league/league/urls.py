from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('leagueweb.urls')),  # Include leagueweb app's URLs for the root path
    # Add other app URLs as needed
]
