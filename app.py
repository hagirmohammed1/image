from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text", "").strip()
    if not text:
        return "No text provided", 400

    # إعداد الصورة
    width, height = 1024, 1024
    bg_color = "white"
    text_color = "black"

    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # خط افتراضي (يعمل دائمًا)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 64)
    except:
        font = ImageFont.load_default()

    # لف النص
    wrapped_text = textwrap.fill(text, width=25)

    # حساب التمركز
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2

    draw.multiline_text(
        (x, y),
        wrapped_text,
        fill=text_color,
        font=font,
        align="center"
    )

    # إخراج الصورة
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
