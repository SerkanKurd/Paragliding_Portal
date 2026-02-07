from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vario_simulator/", views.vario_simulator_view, name="vario_simulator"),
    path("igc_converter/", views.igc_converter_view, name="igc_converter"),
    path("flight_visualizer/", views.flight_visualizer_view, name="flight_visualizer"),
]