from django.conf import settings


def version_info(request):
    return {"APP_VERSION": getattr(settings, "APP_VERSION", "Bilinmiyor")}

