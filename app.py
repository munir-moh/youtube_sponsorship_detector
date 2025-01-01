from flask import Flask, request
from markupsafe import Markup
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/channels', methods=['GET'])
def confirm_channel_subscription():
    # Store channel from args, subscription time, expiry date into dynamodb table
    channel_id = request.args.get('hub.topic').split("channel_id=")[1]
    lease_seconds = request.args.get('hub.lease_seconds')
    challenge = request.args.get('hub.challenge')
    challenge_escaped = str(Markup.escape(challenge))
    return challenge_escaped

@app.route('/channels', methods=['POST'])
def detect_publication():
    doc = request.data
    doc = doc.decode('utf-8')
    try:
        print('doc', doc)
    except AttributeError:
        print('Failed to unpack attributes')
        print(traceback.format_exc())
        print('request', doc)
    except Exception:
        print("* captured exception *")
        print(traceback.format_exc())
        return "exception", 500

    return "", 200

if __name__ == "__main__":
    app.run(debug=True)