from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Use an unusual name, so it is less easy to guess the admin source name.
    path('hello-pokemon/', admin.site.urls),

    # API interface with V1.
    path(
        'api/v1/',
        include('pokemon.interfaces.api.urls', namespace='api')
    ),
]
