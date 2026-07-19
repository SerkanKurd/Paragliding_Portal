from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView

from paragliding.models import Wing

from . import models
from .utilities.IGC_file_parse import convert_igc_to_excel, fligth_data_to_json, sample_fligth_data


def home(request):
    context = {
        "utilities": models.Card.objects.all().order_by("order", "id").exclude(is_active=False),
        # "messages": ["deneme1", "deneme2", "deneme3"],
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


MAX_IGC_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_and_read_igc_file(uploaded_file):
    if not uploaded_file:
        return None, "Lütfen bir IGC dosyası seçin."

    if not uploaded_file.name.lower().endswith(".igc"):
        return None, "Yalnızca .igc veya .IGC uzantılı dosyalar kabul edilmektedir."

    if uploaded_file.size > MAX_IGC_FILE_SIZE:
        return None, "Dosya boyutu çok büyük. Maksimum dosya boyutu 10 MB olmalıdır."

    try:
        raw_data = uploaded_file.read()
        try:
            content = raw_data.decode("utf-8")
        except UnicodeDecodeError:
            content = raw_data.decode("latin-1")
        return content, None
    except Exception as e:
        return None, f"Dosya okunurken bir hata oluştu: {str(e)}"


def igc_converter_view(request):
    if request.method == "POST":
        igc_file = request.FILES.get("igc_file")
        igc_content, error = validate_and_read_igc_file(igc_file)
        if error:
            template = (
                "partials/igc_converter_partial.html"
                if request.headers.get("HX-Request")
                else "includes/igc_converter.html"
            )
            return render(request, template, {"error": error}, status=400)

        try:
            excel_data = convert_igc_to_excel(igc_content)
            response = HttpResponse(
                excel_data,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{igc_file.name}.xlsx"'
            return response
        except Exception as e:
            template = (
                "partials/igc_converter_partial.html"
                if request.headers.get("HX-Request")
                else "includes/igc_converter.html"
            )
            return render(
                request,
                template,
                {"error": f"IGC dosyası işlenirken bir hata oluştu: {str(e)}"},
                status=400,
            )

    if request.headers.get("HX-Request"):
        return render(request, "partials/igc_converter_partial.html")
    return render(request, "includes/igc_converter.html")


def weight_control_view(request):
    context = {"wings": Wing.objects.all()}
    if request.headers.get("HX-Request"):
        return render(request, "partials/weight_control_partial.html", context)
    return render(request, "includes/weight_control.html", context)


def flight_visualizer_view(request):
    if request.method == "POST":
        if request.POST.get("show_sample") == "true":
            flight_data = sample_fligth_data()
        else:
            igc_file = request.FILES.get("igc_file")
            igc_content, error = validate_and_read_igc_file(igc_file)
            if error:
                template = (
                    "partials/flight_3d_getfile_partial.html"
                    if request.headers.get("HX-Request")
                    else "includes/flight_3d_getfile.html"
                )
                return render(request, template, {"error": error}, status=400)

            try:
                flight_data = fligth_data_to_json(igc_content)
            except Exception as e:
                template = (
                    "partials/flight_3d_getfile_partial.html"
                    if request.headers.get("HX-Request")
                    else "includes/flight_3d_getfile.html"
                )
                return render(
                    request,
                    template,
                    {"error": f"IGC dosyası çözümlenirken hata oluştu: {str(e)}"},
                    status=400,
                )

        context = {
            "flight_points": flight_data,
            "cesium_token": settings.CESIUM_TOKEN,
        }
        return render(request, "includes/flight_3d.html", context)

    if request.htmx:
        return render(request, "partials/flight_3d_getfile_partial.html")
    return render(request, "includes/flight_3d_getfile.html")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class WingListView(ListView):
    model = Wing
    template_name = "includes/wing_list.html"
    context_object_name = "wings"


@login_required
def profile_view(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/profile_partial.html")
    return render(request, "includes/profile.html")
