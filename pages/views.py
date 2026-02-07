from django.shortcuts import render
from django.http import HttpResponse
from .utilities.IGC_file_parse import convert_igc_to_excel, fligth_data_to_json
from . import models
from dotenv import get_key


def home(request):
    context = {
        "utilities": models.Card.objects.all()
        .order_by("order", "id")
        .exclude(is_active=False)
    }
    if request.headers.get("HX-Request"):
        return render(request, "partials/main_partial.html", context)

    return render(request, "includes/main.html", context)


def vario_simulator_view(request):
    context = {
        "title": "Vario Simülatörü",
        "min_sink": -5.0,
        "max_lift": 5.0,
        "step": 0.1,
    }
    if request.headers.get("HX-Request"):
        return render(request, "partials/vario_tool_partial.html", context)
    return render(request, "includes/vario_tool.html", context)


def igc_converter_view(request):
    if request.method == "POST" and request.FILES.get("igc_file"):
        igc_file = request.FILES["igc_file"]
        igc_content = igc_file.read().decode("utf-8")
        excel_data = convert_igc_to_excel(igc_content)

        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{igc_file.name}.xlsx"'
        return response
    if request.headers.get("HX-Request"):
        return render(request, "partials/igc_converter_partial.html")
    return render(request, "includes/igc_converter.html")


def flight_visualizer_view(request):
    if request.method == "POST" and request.FILES.get("igc_file"):
        igc_file = request.FILES["igc_file"]
        igc_content = igc_file.read().decode("utf-8")

        flight_data = fligth_data_to_json(igc_content)
        context = {
            "flight_points": flight_data,
            "cesium_token": get_key(
                ".env", "CESIUM_ION_TOKEN"
            ),  # CesiumIon'dan ücretsiz alabilirsin
        }
        return render(request, "includes/flight_3d.html", context)

    return render(request, "partials/flight_3d_getfile_partial.html")
