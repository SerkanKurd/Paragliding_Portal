from django.urls import include, path

from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vario_simulator/", views.vario_simulator_view, name="vario_simulator"),
    path("weight_control/", views.weight_control_view, name="weight_control"),
    path("igc_converter/", views.igc_converter_view, name="igc_converter"),
    path("flight_visualizer/", views.flight_visualizer_view, name="flight_visualizer"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("wings/", views.WingListView.as_view(), name="wing_list"),
]
