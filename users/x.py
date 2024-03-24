import sys
import requests
import json


import requests

get_url = "https://challenge-server.tracks.run/hotel-reservation-en/hotels"



getapi = 'https://track-challenge-api-labrat.herokuapp.com/hotel-reservation-en/hotels'
postapi = 'https://track-challenge-api-labrat.herokuapp.com/hotel-reservation-en/reservations'
def search_hotels(access_token, search_params):
    payload = {}
    headers = {
      'X-ACCESS-TOKEN': 'af1d18dc-1aa9-40cf-bde0-35e1f1b1e0f1'
    }

    response = requests.request("GET", get_url, headers=headers, data=payload,params=search_params)

    resp = response.json()
    return resp


    # headers = {'X-ACCESS-TOKEN': str(access_token)}
    # response = requests.get(getapi, params=search_params, headers=headers)
    # return response.json()

def reserve_room(access_token, room_id, guest_name, checkin_date, checkout_date):
    headers = {'X-ACCESS-TOKEN': str(access_token)}
    reservation_data = {
        "room_id": room_id,
        "guest_name": guest_name,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date
    }
    response = requests.post(reserve_api_url, json=reservation_data, headers=headers)
    return response.json()

def sort_condition(dat,par):
    ans = []
    for val in dat:
        for dec in val['plans']:
            if dec['condition'] == par['condition']:
                ans.append(val)

    return ans

def main(argv):
    # このコードは引数と標準出力を用いたサンプルコードです。
    # このコードは好きなように編集・削除してもらって構いません。
    # ---
    # This is a sample code to use arguments and outputs.
    # Edit and remove this code as you like.

    for i, v in enumerate(argv):
        print("argv[{0}]: {1}".format(i, v))
    print(type(argv[1]))
    par = json.loads(argv[1])
    print(par)
    dat = search_hotels(argv[0],par)
    if len(dat) == 0:
        return "Plan not found."

    print(sort_condition(dat,par))
    # print(dat)
3.6666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666629
3333333











































































































































