from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mN0zh5CWKmQVI9OP8fZE6/BYlYbgGnP9lDjG7LlgUeTv5WAJi4BaYiX5xwk1d2xPy91G4d1a5QZyfCEC3j3yd+R4Up1ph26M3zqOcFOIQRCyjR5siLW+Dbv4o5kFA7zgZYas4mzQwL4j6oQ5zfxBAQdB04t89/1O/w1cDnyilFU= ')
handler = WebhookHandler('437895d36a783c6b1fac639715902243')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()