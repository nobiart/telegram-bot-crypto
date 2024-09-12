import websocket
import json
import requests

alerts = []

TELEGRAM_TOKEN = ""
TELEGRAM_CHANNEL = ""

def send_message(text):
    res = requests.get("https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN), params=dict(
        chat_id=TELEGRAM_CHANNEL, text=text))
    
def on_open(ws):
    sub_msg = {"'method'": "SUBSCRIBE", "params":["!miniTicker@arr"], "id": 1}
    ws.send(json.dumps(sub_msg))
    print("Opened connection")

def on_message(ws, message):
    data = json.loads(message)
    # call functions
    alert_down("TONUSDT", 5.400, data)
    alert_up("ATOMUSDT", 5.415, data)

def alert_down(symbol, price, data):
    for x in data:
        if x["s"] == symbol and float(x["c"]) <= price and x["s"] not in alerts:
            print(x["s"] + " " + x["c"])
            send_message(x["s"] + " " + x["c"])
            alerts.append(x["s"])

def alert_up(symbol, price, data):
    for x in data:
        if x["s"] == symbol and float(x["c"]) >= price and x["s"] not in alerts:
            print(x["s"] + " " + x["c"])
            send_message(x["s"] + " " + x["c"])
            alerts.append(x["s"])

url = "wss://stream.binance.com:9443"

ws = websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_message)

ws.run_forever()
