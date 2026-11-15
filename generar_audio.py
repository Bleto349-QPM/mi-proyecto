# -*- coding: utf-8 -*-
"""Genera audio/<clave>.mp3 con voz en español (gTTS). Uso: python generar_audio.py"""
import os
from gtts import gTTS
from narracion import NARRACION

os.makedirs("audio", exist_ok=True)
for clave, texto in NARRACION.items():
    ruta = os.path.join("audio", f"{clave}.mp3")
    if not os.path.exists(ruta):
        gTTS(texto, lang="es", tld="com.mx").save(ruta)
        print("ok", ruta)
