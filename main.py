import os
import requests
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# === Función para extraer el ID desde la URL ===
def get_video_id_from_url(url):
    query = urlparse(url)
    return parse_qs(query.query).get("v", [None])[0]

# === CONFIGURACIÓN ===
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Inserta aquí la URL del video
video_url = "https://www.youtube.com/watch?v=lfG8PiImmsM"
VIDEO_ID = get_video_id_from_url(video_url)

if not VIDEO_ID:
    raise ValueError("No se pudo extraer el ID del video. Verifica la URL.")

print(f"ID del video extraído: {VIDEO_ID}")

# === LLAMADA A LA API ===
BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
params = {
    "part": "snippet",
    "videoId": VIDEO_ID,
    "key": API_KEY,
    "textFormat": "plainText",
    "maxResults": 100
}

comments = []
next_page_token = None

while True:
    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        print("Error al obtener los datos:", response.text)
        break

    data = response.json()

    for item in data.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]
        texto = comment["textDisplay"].replace(",", "")  # ← Quita las comas

        comments.append({
            "comentario": texto,
            "usuario": comment["authorDisplayName"],
            "fecha": comment["publishedAt"],
            "likes": comment["likeCount"],
            "video_id": VIDEO_ID
        })


    next_page_token = data.get("nextPageToken")

    if not next_page_token:
        break

# === GUARDAR ===
df = pd.DataFrame(comments)
df.to_csv("comentarios_youtube.csv", index=False, encoding="utf-8-sig")
print(f"✅ {len(df)} comentarios guardados exitosamente.")
