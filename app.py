import os
import base64
import io
from flask import Flask, render_template, request, send_file
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text", "").strip()
    if not text:
        return "No text", 400

    prompt = f"""
    Create a clean image with centered readable text.
    The image must contain exactly this text:
    "{text}"

    Rules:
    - Perfect readability
    - No extra symbols
    - High contrast
    - Minimal background
    - Arabic text if input is Arabic
    - English text if input is English
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return send_file(io.BytesIO(image_bytes), mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
