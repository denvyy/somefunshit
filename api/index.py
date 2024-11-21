from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
import io

app = Flask(__name__)

# Получение города по IP
def get_city_by_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json",verify=False)
        data = response.json()
        print(data["city"])
        return data["city"]
    except Exception:
        return "Unknown City"

# Генерация изображения
def create_image_with_text(text):
    # Создаем белое изображение размером 500x500
    img = Image.new("RGB", (500, 500), color="white")
    draw = ImageDraw.Draw(img)
    
    # Настройка шрифта
    try:
        font = ImageFont.truetype("arial.ttf", 36)  # Убедитесь, что шрифт установлен
    except IOError:
        font = ImageFont.load_default()

    # Вычисление размеров текста с использованием textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Центрирование текста
    position = ((500 - text_width) // 2, (500 - text_height) // 2)
    draw.text(position, text, fill="black", font=font)
    return img


@app.route("/", methods=["GET"])
def index():
    # Получаем IP клиента
    client_ip = request.remote_addr
    
    city = get_city_by_ip(client_ip)
    img = create_image_with_text(city)
    
    # Сохраняем изображение в буфер для отправки
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")