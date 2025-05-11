import pandas as pd
import spacy
import re

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

# Leer CSV con separador correcto
df = pd.read_csv("comentarios_youtube1.csv", sep=";")
print("Columnas detectadas:", df.columns.tolist())

# Asegurar que la columna 'comentario' no tenga nulos
df["comentario"] = df["comentario"].fillna("")

# Función para limpiar texto (incluye limpieza de emojis)
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)                 # quitar URLs
    texto = re.sub(r"[^\w\s]", "", texto)                        # quitar signos
    texto = re.sub(r"\d+", "", texto)                            # quitar números
    texto = re.sub(r"[^\x00-\x7F\u00A0-\u00FF]+", "", texto)     # quitar emojis y símbolos raros
    doc = nlp(texto)
    tokens_limpios = [token.lemma_ for token in doc if not token.is_space]
    return " ".join(tokens_limpios)

# Aplicar limpieza
print("Procesando comentarios...")
df["comentario_limpio"] = df["comentario"].astype(str).apply(limpiar_texto)

# Mostrar primeros ejemplos para ver el cambio
print("\n🔍 Ejemplos:")
print(df[["comentario", "comentario_limpio"]].head(5))

# Guardar el resultado
df.to_csv("comentarios_limpios2.csv", index=False, encoding="utf-8-sig")
print("\n✅ Archivo 'comentarios_limpios2.csv' guardado correctamente.")
