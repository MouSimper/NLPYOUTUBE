import pandas as pd

# Cargar comentarios limpios
df = pd.read_csv("comentarios_limpios2.csv", sep=",")

# Añadir columna vacía para etiquetas
df["etiqueta"] = ""

# Guardar plantilla
df.to_csv("plantilla_etiquetado.csv", index=False, encoding="utf-8-sig")
print("✅ Plantilla para etiquetado creada: 'plantilla_etiquetado.csv'")
