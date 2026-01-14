import os
import base64
import io
from flask import Flask, render_template, request, send_file
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# قراءة مفتاح OpenAI من متغيرات البيئة
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text", "").strip()
    if not text:
        return "No text provided", 400

    prompt = f"""
Create a clean minimal image.
The image must contain ONLY this exact text:
"{text}"

Rules:
- Perfect readability
- No spelling changes
- No extra symbols or words
- Centered text
- High contrast
- Minimal background
- Use Arabic typography if text is Arabic
- Use English typography if text is English
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return send_file(
        io.BytesIO(image_bytes),
        mimetype="image/png"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway PORT
    app.run(host="0.0.0.0", port=port)
