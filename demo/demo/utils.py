import requests
from django.core.mail import send_mail, EmailMessage  # Correct module import
from django.conf import settings
import urllib.parse


def get_coordinates(address, api_key):
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {"q": address, "key": api_key, "limit": 1}
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"]["code"] == 200:  # Check for successful status code
        if data["results"]:
            result = data["results"][0]
            geometry = result["geometry"]
            return geometry["lat"], geometry["lng"]
        else:
            print("No results found")
            return None, None
    else:
        print("API Error:", data["status"]["message"])
        return None, None


# Example usage
# api_key = "daec8462e042407bbb92f73b577b526c"  # Replace with your OpenCage API key
# address = "1600 Amphitheatre Parkway, Mountain View, CA"
# lat, lng = get_coordinates(address, api_key)
# if lat and lng:
# print(f"Latitude: {lat}, Longitude: {lng}")
# else:
# print("Location not found")


def send_email_to_client():
    subject = "This email is from the Django server"
    message = "This is a test message from the Django server"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["mihirdiku1@gmail.com"]

    print("email is sending")

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)


def send_mail_with_attachment(subject, message, recipient_list, file_path):
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    mail.attach_file(file_path)
    mail.send()
