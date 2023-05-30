import decimal

import google.auth
import requests
from googleapiclient.discovery import build

from core import settings


def receive_payment(data):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/debit_mobile_account/'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    response = requests.post(ENDPOINT, data=data, headers=headers)
    response_data = response.json()
    print('From receive_payment', response_data)
    return response_data


def make_payment(data):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/credit_mobile_account/'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    response = requests.post(ENDPOINT, data=data, headers=headers)
    response_data = response.json()
    print("From make_payment", response_data)
    return response_data


def get_transaction_status(transaction_id):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/transaction_status'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    params = {
        "transaction_id": transaction_id,
    }
    response = requests.get(ENDPOINT, params=params, headers=headers)
    print('Raw response from get_transaction_status: ', response)
    response_data = response.json()
    print('From get_transaction_status: ', response_data)
    return response_data


def get_api_wallet_balance():
    ENDPOINT = 'https://payhubghana.io/api/v1.0/wallet_balance'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    payload = {
        "wallet_id": settings.PAYHUB_WALLET_ID,
    }
    response = requests.get(ENDPOINT, headers=headers, params=payload)
    try:
        main_balance = response.json()['main_balance']
        main_balance = decimal.Decimal(main_balance)
    except KeyError:
        main_balance = decimal.Decimal(0)
    return main_balance


def fetch_youtube_data(channel_id):
    # Set up the YouTube API client
    API_KEY = settings.YOUTUBE_API_KEY
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # parameters for the API request
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,  # max num of videos to fetch
        order="date",
        type="video"
    )

    # Send the API request and fetch the videos from the channel
    response = request.execute()
    videos = response.get("items", [])
    return videos
