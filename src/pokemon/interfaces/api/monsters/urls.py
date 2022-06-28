from django.urls import path

from . import views

app_name = "monsters"

urlpatterns = [
    path(
        "", views.MonsterCatalogue.as_view(), name="monster-catalogue",
    ),
]
