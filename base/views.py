
import shortner.models as shortner_models
import shortner.serializers as shortner_serializers
from django.shortcuts import redirect
from django.shortcuts import render


def login_page(request):
    print("Request: ", request.user)
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')


def redirect_to_original(request, short_key):
    print("SHORT KEY: ", short_key, "User: ", request.user)

    orginal_url = shortner_models.ShortUrl.objects.get(short_key=short_key).original_url_id.url

    return redirect(orginal_url)


def view_details(request, short_key):
    short = shortner_models.ShortUrl.objects.get(short_key=short_key)
    details = shortner_serializers.ShortUrlSerializer(short, context={"request": request}).data

    return render(request, 'view.html', context={"details": details})
