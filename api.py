import json
import tkinter.messagebox

import requests

model_url = 'https://l7y8f0kzil.execute-api.eu-west-2.amazonaws.com/model_prediction'


def send_data(prediction_data):
    global model_url
    headers = {"Content-Type": 'application/json'}
    prediction = requests.post(model_url, headers=headers, json=prediction_data, timeout=5)

    print(prediction)
    print(prediction.json())
    if prediction.status_code == 400:
        tkinter.messagebox.showerror(title="Klaida",
                                     message="Nepavyko įvertinti failo. Blogai išsiųsti duomenys")
        return
    if prediction.status_code == 404:
        tkinter.messagebox.showerror(title="Klaida",
                                     message="Nepavyko išsiųsti duomenų")
        return
    if prediction.status_code == 200:
        prediction_body = prediction.json()
        return prediction_body


def quality_value(prediction_data):
    responceJSON = send_data(prediction_data)
    predictions = responceJSON['predictions']
    quality_1 = predictions[0][0]
    quality_2 = predictions[0][1]
    quality_3 = predictions[0][2]
    quality_4 = predictions[0][3]
    quality_5 = predictions[0][4]
    quality = -1

    if quality_1 > quality_2 and quality_1 > quality_3 and quality_1 > quality_4 and quality_1 > quality_5:
        quality = 1
    if quality_2 > quality_1 and quality_2 > quality_3 and quality_2 > quality_4 and quality_2 > quality_5:
        quality = 2
    if quality_3 > quality_1 and quality_3 > quality_2 and quality_3 > quality_4 and quality_3 > quality_5:
        quality = 3
    if quality_4 > quality_1 and quality_4 > quality_2 and quality_4 > quality_3 and quality_4 > quality_5:
        quality = 4
    if quality_5 > quality_1 and quality_5 > quality_2 and quality_5 > quality_3 and quality_5 > quality_4:
        quality = 5

    return quality
