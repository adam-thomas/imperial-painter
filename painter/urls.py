from django.urls import path

from . import views


urlpatterns = [
    path("noreload", views.CardDisplay.as_view(), name="card_display_noreload"),
    path("", views.CardDisplayReload.as_view(), name="card_display"),
]
