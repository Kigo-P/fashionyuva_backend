import requests
import base64
from datetime import datetime
from app.models.transaction import Transaction
from app import db

class MpesaService:
    def __init__(self, config):
        self.config = config
        
    def get_access_token(self):
        try:
            credentials = f"{self.config.MPESA_CONSUMER_KEY}:{self.config.MPESA_CONSUMER_SECRET}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            response = requests.get(
                'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
                headers={'Authorization': f'Basic {encoded_credentials}'}
            )
            
            return response.json()['access_token']
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def initiate_payment(self, phone_number, amount):
        try:
            access_token = self.get_access_token()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password_string = f"{self.config.MPESA_BUSINESS_SHORTCODE}{self.config.MPESA_PASSKEY}{timestamp}"
            password = base64.b64encode(password_string.encode()).decode()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.config.MPESA_BUSINESS_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.config.MPESA_BUSINESS_SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": self.config.MPESA_CALLBACK_URL,
                "AccountReference": "Online Store",
                "TransactionDesc": "Payment for products"
            }
            
            response = requests.post(
                'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                json=payload,
                headers=headers
            )
            
            data = response.json()
            
            # Create transaction record
            transaction = Transaction(
                merchant_request_id=data.get('MerchantRequestID'),
                checkout_request_id=data.get('CheckoutRequestID'),
                phone_number=phone_number,
                amount=amount
            )
            db.session.add(transaction)
            db.session.commit()
            
            return data
            
        except Exception as e:
            raise Exception(f"Failed to initiate payment: {str(e)}")