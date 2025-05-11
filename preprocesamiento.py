import pandas as pd
import spacy
import nltk
import re
from nltk.corpus import stopwords

# Descargar stopwords de NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

# Cargar comentarios
df = pd.read_csv("comentarios_youtube1.csv")

# Función de limpieza
def limpiar_texto(texto):
    # Convertir a minúsculas
    texto = texto.lower()
    # Eliminar URLs
    texto = re.sub(r"http\S+|www\S+|https\S+", '', texto, flags=re.MULTILINE)
    # Eliminar puntuación, emojis y otros caracteres especiales
    texto = re.sub(r"[^\w\s]", '', texto)
    # Eliminar números
    texto = re.sub(r"\d+", '', texto)
    # Tokenización, stopwords y lematización
    doc = nlp(texto)
    tokens_limpios = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_space]
    return " ".join(tokens_limpios)

# Aplicar limpieza
df["comentario_limpio"] = df["comentario"].astype(str).apply(limpiar_texto)

# Guardar resultado
df.to_csv("comentarios_limpios.csv", index=False, encoding="utf-8-sig")
print("✅ Comentarios preprocesados guardados.")
