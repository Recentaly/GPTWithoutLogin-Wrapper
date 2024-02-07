from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_cloudflared import run_with_cloudflared
import waitress
import logging

from res.src.Api import API

app = Flask(__name__)
CORS(app)

run_with_cloudflared(app)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api = API()

@app.route("/chat/completions", methods=["POST"])
def chat():
    
    messages = request.json.get("messages", [])
    model = request.json.get("model", "gpt-3.5-turbo")
    
    config = {
        "frequency_penalty": request.json.get("frequency_penalty", 0.0),
        "max_tokens": request.json.get("max_tokens", 150),
        "presence_penalty": request.json.get("presence_penalty", 0.0),
        "stream": request.json.get("stream", False),
        "temperature": request.json.get("temperature", 0.7),
        "top_p": request.json.get("top_p", 0.7)
    }
    
    def stream():
        
        for chunk in api.chat(messages, model, config):
            yield chunk + b"\n\n"
        
    if config.get("stream", False):
        return Response(stream(), content_type="text/event-stream")
    
    else:   return jsonify(next(api.chat(messages, model, config)))

@app.route("/models", methods=["GET"])
def models():
    return jsonify(
        {"data": [
            {"id": "gpt-3.5-turbo"},
            {"id": "gpt-3.5-turbo-0125"},
            {"id": "gpt-3.5-turbo-16k"},
            ]
        }
    ), 200
    



if __name__ == "__main__":
    
    run_with_cloudflared(app)
    app.run(port=5000, host="0.0.0.0", debug=False)
