"""
Added from https://github.com/rasooll
"""

import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"


def send_request(request, amount, description, phone, email):
    callback_url = request.build_absolute_uri(reverse_lazy("accounts:verify-deposit"))

    data = {
        "MerchantID": settings.ZARINPAL["MERCHANT"],
        "Amount": float(amount),
        "Description": description,
        "Phone": phone,
        "Email": email,
        "CallbackURL": callback_url,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        # TODO (bug) response will return 502
        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                return JsonResponse(
                    {
                        "status": True,
                        "url": ZP_API_STARTPAY + str(response["Authority"]),
                        "authority": response["Authority"],
                    }
                )
            else:
                return JsonResponse({"status": False, "code": str(response["Status"])})
        return response

    except requests.exceptions.Timeout:
        return JsonResponse({"status": False, "code": "timeout"})
    except requests.exceptions.ConnectionError:
        return JsonResponse({"status": False, "code": "connection error"})


def verify(amount, authority):
    data = {
        "MerchantID": settings.ZARINPAL["MERCHANT"],
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response["Status"] == 100:
            return JsonResponse({"status": True, "RefID": response["RefID"]})
        else:
            return JsonResponse({"status": False, "code": str(response["Status"])})
    return response
