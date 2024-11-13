import os
import requests
import base64
from datetime import datetime
from models import Transaction
from app import db
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource

payment = Blueprint("payment", __name__)
api = Api(payment)


class MpesaService:
    def __init__(self, config):
        self.config = config

    def get_access_token(self):
        try:
            credentials = f"{self.config['MPESA_CONSUMER_KEY']}:{self.config['MPESA_CONSUMER_SECRET']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")

            response = requests.get(
                "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
                headers={"Authorization": f"Basic {encoded_credentials}"},
            )

            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                raise Exception(f"Access token request failed: {response.json()}")

        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def initiate_payment(self, phone_number, amount):
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password_string = f"{self.config['MPESA_BUSINESS_SHORTCODE']}{self.config['MPESA_PASSKEY']}{timestamp}"
            password = base64.b64encode(password_string.encode()).decode()
            payload = {
                "BusinessShortCode": self.config["MPESA_BUSINESS_SHORTCODE"],
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": int(phone_number),
                "PartyB": self.config["MPESA_BUSINESS_SHORTCODE"],
                "PhoneNumber": int(phone_number),
                "CallBackURL": self.config["MPESA_CALLBACK_URL"],
                "AccountReference": "Online Store",
                "TransactionDesc": "Payment for products",
            }

            print(payload)

            response = requests.request(
                "POST",
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.get_access_token()}",
                },
                json=payload,
                timeout=10,
            )

            data = response.json()

            # Create transaction record
            # transaction = Transaction(
            #     merchant_request_id=data.get("MerchantRequestID"),
            #     checkout_request_id=data.get("CheckoutRequestID"),
            #     phone_number=phone_number,
            #     amount=amount,
            # )
            # db.session.add(transaction)
            # db.session.commit()

            return data

        except Exception as e:
            raise Exception(f"Failed to initiate payment: {str(e)}")


config = {
    "MPESA_CONSUMER_KEY": os.getenv("MPESA_CONSUMER_KEY"),
    "MPESA_CONSUMER_SECRET": os.getenv("MPESA_CONSUMER_SECRET"),
    "MPESA_BUSINESS_SHORTCODE": os.getenv("MPESA_BUSINESS_SHORTCODE"),
    "MPESA_PASSKEY": os.getenv("MPESA_PASSKEY"),
    "MPESA_CALLBACK_URL": os.getenv("MPESA_CALLBACK_URL"),
}

mpesa_service = MpesaService(config)


class InitiatePayment(Resource):
    def post(self):
        """Endpoint to initiate an M-Pesa payment."""
        try:
            data = request.get_json()
            phone_number = data.get("phone_number")
            amount = data.get("amount")

            if not phone_number or not amount:
                return {"error": "Phone number and amount are required."}, 400

            # Format phone number if necessary
            if phone_number.startswith("0"):
                phone_number = "254" + phone_number[1:]
            elif not phone_number.startswith("254"):
                phone_number = "254" + phone_number

            response_data = mpesa_service.initiate_payment(phone_number, amount)
            return response_data, 200

        except Exception as e:
            return {"error": str(e)}, 500


class Callback(Resource):
    def post(self):
        """Callback endpoint for M-Pesa to receive payment status."""
        try:
            callback_data = request.get_json()

            # Extract necessary fields from the callback
            result_code = (
                callback_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
            )
            result_desc = (
                callback_data.get("Body", {}).get("stkCallback", {}).get("ResultDesc")
            )
            merchant_request_id = (
                callback_data.get("Body", {})
                .get("stkCallback", {})
                .get("MerchantRequestID")
            )
            checkout_request_id = (
                callback_data.get("Body", {})
                .get("stkCallback", {})
                .get("CheckoutRequestID")
            )

            # If payment is successful
            if result_code == 0:
                payment_details = (
                    callback_data.get("Body", {})
                    .get("stkCallback", {})
                    .get("CallbackMetadata", {})
                    .get("Item", [])
                )

                # Extract payment details
                amount = next(
                    (
                        item.get("Value")
                        for item in payment_details
                        if item.get("Name") == "Amount"
                    ),
                    None,
                )
                mpesa_receipt = next(
                    (
                        item.get("Value")
                        for item in payment_details
                        if item.get("Name") == "MpesaReceiptNumber"
                    ),
                    None,
                )

                # Update transaction status in the database
                transaction = Transaction.query.filter_by(
                    checkout_request_id=checkout_request_id
                ).first()
                if transaction:
                    transaction.result_code = result_code
                    transaction.result_desc = result_desc
                    transaction.amount = amount
                    transaction.mpesa_receipt = mpesa_receipt
                    db.session.commit()

            return {
                "ResultCode": 0,
                "ResultDesc": "Success",
                "MerchantRequestID": merchant_request_id,
                "CheckoutRequestID": checkout_request_id,
            }

        except Exception as e:
            return {"error": str(e)}, 500


class CheckStatus(Resource):
    def get(self, checkout_id):
        return make_response(
            jsonify({"message": "success", "status": "completed"}), 200
        )


api.add_resource(InitiatePayment, "/initiate")
api.add_resource(Callback, "/callback")
api.add_resource(CheckStatus, "/status/<string:checkout_id>")
