import pandas as pd

# BLOQUE 1: CARGA DE DATOS: python abre el excel y lo examina
ruta_excel = 'gsc-lauragilastro.xlsx'
excel_completo = pd.read_excel(ruta_excel, sheet_name=None)

# Extraemos las pestañas que necesitamos usando los nombres exactos que me has dicho
df_consultas = excel_completo['Consultas']
df_paginas = excel_completo['Páginas']

# Limpieza de datos: a veces Google pone "0" o símbolos raros, vamos a asegurarnos de que los números sean números
df_consultas['Clics'] = pd.to_numeric(df_consultas['Clics'], errors='coerce')
df_consultas['Posición'] = pd.to_numeric(df_consultas['Posición'], errors='coerce')
df_consultas['Impresiones'] = pd.to_numeric(df_consultas['Impresiones'], errors='coerce')
df_consultas['CTR'] = pd.to_numeric(df_consultas['CTR'], errors='coerce')

# BLOQUE 2: FILTRAMOS LAS PALABRAS CLAVE
# Explicación: filtramos las palabras clave que:
# Tengan muchas impresiones: Google las posiciona y son exitosas en el mercado, hay que explotarlas, no pierdas tiempo en las que no sirven
# Tienen pocos clicks: se muestran mucho pero algo falla (metatítulos/descrips mal, canibalización... etc)
# Posicionamiento: del 4 al 20 (el cuello de botella)

# Pasito 1: buscamos la palabra con más impresiones y calculamos su 5%
max_impresiones = df_consultas['Impresiones'].max()
umbral = max_impresiones * 0.05

# Pasito 2: usamos ese umbral para filtrar
oportunidades = df_consultas[df_consultas['Impresiones'] > umbral].copy()

# Pasito 3: buscamos palabras con CTR bajo (-3%) y positions del 4 al 20
drama = oportunidades[
    (oportunidades['CTR'] < 0.03) &
    (oportunidades['Posición'] > 3) &
    (oportunidades['Posición'] <= 20)
].copy()

# BLOQUE 3: CLASIFICACIÓN Y CÁLCULO DE PÉRDIDAS DE CLICKS
drama['Pérdida de clics aprox'] = (drama['Impresiones'] * 0.05).astype(int) - drama['Clics']
drama = drama.sort_values(by='Pérdida de clics aprox', ascending=False)
drama = drama.head(5) # Solo muestra 5 palabras, pero podría mostrar 20, 50 o las que queramos, solo tenemos que cambiar ese número.

# Lo que printeamos:
if drama.empty:
    print("No se han encontrado palabras clave a las que atacar")
else:
    print("MISTERIO DE LOS CLICKS PERDIDOS RESUELTO: ESTAS SON LAS PALABRAS CLAVES A LAS QUE ATACAR:")
    print(drama[['Consultas principales', 'Posición', 'Pérdida de clics aprox']].to_string(index=False))
    print("REVISIÓN SUGERIDA: comprobar metadatos para estas palabras y crear contenidos creativos para potenciarlas")
