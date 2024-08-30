from django.shortcuts import render, redirect, HttpResponse
from demo.middleware import MyMiddleware

import phonenumbers
from django.shortcuts import render, redirect
import re
from phonenumbers import carrier

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .utils import (
    get_coordinates,
    send_email_to_client,
    send_mail_with_attachment,
)  # Assume you saved the function in utils.py


def get_carrier_info(phone_number):
    try:
        number = phonenumbers.parse(phone_number, "IN")
        if phonenumbers.is_valid_number(number):
            carrier_name = carrier.name_for_number(number, "en")
            return {
                "phone_number": phone_number,
                "country_code": number.country_code,
                "carrier": carrier_name,
            }
    except phonenumbers.NumberParseException:
        return None
    return None


def phone_number_verification_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        if phone_number is None:
            return render(
                request,
                "phone_verification.html",
                {"error": "Phone number is required"},
            )

        # Validate phone number format (simple validation)
        # pattern = re.compile(r"^\+?91\d{10}$")
        # if not pattern.match(phone_number):
        #     return render(
        #         request,
        #         "phone_verification.html",
        #         {"error": "Invalid phone number format for India"},
        #     )

        carrier_info = get_carrier_info(phone_number)
        if carrier_info:
            return render(
                request, "verification_success.html", {"carrier_info": carrier_info}
            )
        else:
            return redirect("verification_error")
    else:
        return render(request, "phone_verification.html")


def verification_error_view(request):
    return render(request, "verification_error.html")


# @MyMiddleware
def index(request):
    api_key = " AIzaSyBz8AsGvst0BoXP-SYVMiQZ8XobsLXMecI"
    return render(request, "phone_verification.html")


# @MyMiddleware
def index2(request):
    return render(request, "send_mail.html")


def location_to_map(request):
    address = request.GET.get("address", "gota")
    api_key = "d3cf13cd181b4e82b349bde8092f2f98"  # Replace with your OpenCage API key

    lat, lng = get_coordinates(address, api_key)
    if lat and lng:
        return render(
            request, "map_template.html", {"lat": lat, "lng": lng, "address": address}
        )
    else:
        return JsonResponse({"error": "Unable to find location"}, status=400)


def send_mail(request):
    subject = "This email is from the Django server"
    message = "This is a test message from the Django server"
    recipient_list = ["mihirdiku1@gmail.com"]
    file_path = "demo/images/demo.xlsx"
    try:
        from django.core.mail import send_mail

        print("Import successful!")
    except ModuleNotFoundError as e:
        print("Import failed:", e)

    send_mail_with_attachment(subject, message, recipient_list, file_path)()
    return HttpResponse("email send successfullly")
