import os
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    image_data = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            img = Image.new("RGB", (1024, 1024), "#0f0f0f")
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 90)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            x = (1024 - (bbox[2] - bbox[0])) // 2
            y = (1024 - (bbox[3] - bbox[1])) // 2

            draw.text((x, y), text, fill="white", font=font)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            image_data = base64.b64encode(buf.getvalue()).decode()

    return render_template("index.html", image=image_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
