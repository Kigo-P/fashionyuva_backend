import os
import requests
import base64
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

# Initialize Blueprint
payment = Blueprint("payment", __name__)
api = Api(payment)

class MpesaAPI:
    def __init__(self):
        # Initialize with environment variables
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.business_shortcode = os.getenv('MPESA_BUSINESS_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.callback_url = os.getenv('MPESA_CALLBACK_URL')
        
        # API endpoints
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def get_access_token(self):
        """Generate OAuth access token"""
        try:
            auth_string = base64.b64encode(
                f"{self.consumer_key}:{self.consumer_secret}".encode()
            ).decode()

            headers = {"Authorization": f"Basic {auth_string}"}
            response = requests.get(self.auth_url, headers=headers)
            
            if response.status_code == 200:
                return response.json()["access_token"]
            return None
            
        except Exception as e:
            print(f"Error generating access token: {str(e)}")
            return None

    def generate_password(self):
        """Generate password for STK push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()
        return password, timestamp

    def initiate_stk_push(self, phone_number, amount):
        """Initiate STK push payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"error": "Failed to generate access token"}, 400

            password, timestamp = self.generate_password()

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": self.callback_url,
                "AccountReference": "Online Store",
                "TransactionDesc": "Payment for products"
            }

            response = requests.post(
                self.stk_push_url,
                json=payload,
                headers=headers
            )

            return response.json(), response.status_code

        except Exception as e:
            return {"error": str(e)}, 500

# Initialize MpesaAPI instance
mpesa_api = MpesaAPI()

def require_token(f):
    """Decorator to check for valid API token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "No token provided"}), 401
        # Add your token validation logic here if needed
        return f(*args, **kwargs)
    return decorated

# Define routes using Blueprint
@payment.route('/initiate', methods=['POST'])
@require_token
def initiate_payment():
    """Endpoint to initiate M-Pesa payment"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        amount = data.get('amount')

        if not phone_number or not amount:
            return jsonify({
                "error": "Phone number and amount are required"
            }), 400

        # Format phone number
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            phone_number = '254' + phone_number

        response, status_code = mpesa_api.initiate_stk_push(phone_number, amount)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment.route('/callback', methods=['POST'])
def callback():
    """Callback endpoint for M-Pesa"""
    try:
        callback_data = request.get_json()

        # Extract important fields
        result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        result_desc = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
        merchant_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('MerchantRequestID')
        checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')

        if result_code == 0:
            payment_details = callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
            
            # Extract payment details
            amount = next((item.get('Value') for item in payment_details if item.get('Name') == 'Amount'), None)
            mpesa_receipt = next((item.get('Value') for item in payment_details if item.get('Name') == 'MpesaReceiptNumber'), None)
            
            # TODO: Add your payment processing logic here
            # For example, update database, send notifications, etc.
            
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Success",
            "MerchantRequestID": merchant_request_id,
            "CheckoutRequestID": checkout_request_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500