from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("<str:generator>", views.FileSelect.as_view(), name="file_select"),
    path("<str:generator>/<str:b64_file_path>", views.CardDisplay.as_view(), name="card_display"),
]
