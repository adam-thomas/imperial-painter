from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("admin", admin.site.urls, name="admin"),
    path("<str:generator>", views.FileSelect.as_view(), name="file_select"),
    path("<str:generator>/<str:b64_file_path>", views.CardDisplay.as_view(), name="card_display"),
]

urlpatterns += staticfiles_urlpatterns()
