# -*- coding: utf-8 -*-
"""
Video educativo: Problemas 4, 5, 6 y 7 de Ingeniería Óptica (Manim Community Edition).

Cada problema sigue 5 bloques:
  1) Título y datos
  2) Fórmulas y desarrollo paso a paso (resultado en recuadro verde)
  3) Interpretación técnica correcta (panel azul/verde)
  4) Consecuencia de una interpretación errada (panel rojo/ámbar)
  5) Transición limpia (FadeOut de toda la pantalla)

Render completo en 1080p:
    manim -pqh optica_manim.py VideoCompleto

Un problema por separado:
    manim -pqh optica_manim.py Problema4     (también Problema5, Problema6, Problema7)

Solo usa Text (no requiere LaTeX instalado).
"""
import os
import textwrap

from manim import *

# ----------------------------- Paleta y estilo -----------------------------
BG = "#0F172A"
TXT = "#F1F5F9"
MUTED = "#94A3B8"
SKY = "#38BDF8"
GREEN_OK = "#22C55E"
TEAL = "#2DD4BF"
RED_BAD = "#EF4444"
AMBER = "#F59E0B"
YELLOW = "#FDE68A"
CARD = "#1E293B"

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


# ------------------------------- Contenido ---------------------------------
PROBLEMAS = [
    dict(
        n=4,
        titulo="Cálculo de VOA en enlace DWDM",
        datos=[
            ("Ptx", "+3 dBm"),
            ("Distancia (d)", "40 km"),
            ("Atenuación (α)", "0.25 dB/km"),
            ("Aislador", "0.6 dB"),
            ("2 conectores", "0.4 dB c/u"),
            ("Rango RX", "-18 a -6 dBm"),
            ("Prx deseado", "-10 dBm"),
        ],
        pasos=[
            dict(l="1) Pérdida de la fibra",
                 s="L_fibra = α × d",
                 n="L_fibra = 0.25 dB/km × 40 km = 10 dB", r="10 dB"),
            dict(l="2) Pérdidas pasivas sin VOA",
                 s="L_pasivas = L_fibra + L_aislador + (n × L_conector)",
                 n="L_pasivas = 10 + 0.6 + (2 × 0.4) = 11.4 dB", r="11.4 dB"),
            dict(l="3) Potencia recibida actual",
                 s="Prx_actual = Ptx - L_pasivas",
                 n="Prx_actual = +3 dBm - 11.4 dB = -8.4 dBm", r="-8.4 dBm"),
            dict(l="4) VOA requerido",
                 s="VOA = Prx_actual - Prx_deseado",
                 n="VOA = -8.4 - (-10) = 1.6 dB", r="1.6 dB"),
        ],
        cajas=[3],
        correcta=("Aunque -8.4 dBm está dentro del rango del receptor, queda muy cerca del "
                  "límite superior (-6 dBm). Instalar el VOA de 1.6 dB lleva la potencia a "
                  "-10 dBm, asegurando margen operativo y evitando saturación."),
        errada=("No instalar atenuador por creer que -8.4 dBm ya es válido deja al receptor con "
                "margen reducido; cualquier aumento de potencia del transmisor o menor pérdida "
                "real puede saturar el receptor, generar errores de bit (BER) e inestabilidad "
                "DWDM."),
    ),
    dict(
        n=5,
        titulo="Presupuesto óptico y amplificación EDFA (Lima - Huaral)",
        datos=[
            ("Ptx (1550 nm)", "0 dBm"),
            ("Distancia (d)", "80 km"),
            ("Atenuación (α)", "0.22 dB/km"),
            ("L adicional", "2 dB"),
            ("Margen", "3 dB"),
            ("Sensibilidad RX", "-18 dBm"),
            ("EDFA", "G = 20 dB, Pout máx = +17 dBm"),
        ],
        pasos=[
            dict(l="1) Pérdida de la fibra",
                 s="L_fibra = α × d",
                 n="L_fibra = 0.22 × 80 = 17.6 dB", r="17.6 dB"),
            dict(l="2) Pérdida total del enlace",
                 s="L_total = L_fibra + L_adicional + Margen",
                 n="L_total = 17.6 + 2 + 3 = 22.6 dB", r="22.6 dB"),
            dict(l="3) Potencia recibida sin EDFA",
                 s="Prx = Ptx - L_total",
                 n="Prx = 0 - 22.6 = -22.6 dBm  (menor que -18 dBm: no opera)",
                 r="-22.6 dBm", c=AMBER),
            dict(l="4) Salida del EDFA",
                 s="Pout = Ptx + G  →  limitada a Pout_máx",
                 n="Pout teórica = +20 dBm  →  limitada por equipo a +17 dBm",
                 r="+17 dBm"),
            dict(l="5) Potencia recibida con EDFA",
                 s="Prx = Pout_real - L_total",
                 n="Prx = 17 - 22.6 = -5.6 dBm", r="-5.6 dBm"),
        ],
        cajas=[4],
        correcta=("Sin EDFA se reciben -22.6 dBm, valor inferior a la sensibilidad mínima "
                  "(-18 dBm), por lo que el enlace no opera. Con el EDFA (limitado a +17 dBm) "
                  "se reciben -5.6 dBm, logrando operación estable y buen margen."),
        errada=("Ignorar el margen de ingeniería de 3 dB (diseñar al límite) o asumir que el "
                "EDFA entrega +20 dBm sin revisar su límite máximo (+17 dBm) provoca cálculos "
                "irreales y caídas del enlace ante degradaciones futuras."),
    ),
    dict(
        n=6,
        titulo="Enlace larga distancia, número de EDFAs y OSNR (Lima - Trujillo)",
        datos=[
            ("Distancia (d)", "600 km"),
            ("Atenuación (α)", "0.22 dB/km"),
            ("L adicional", "20 dB"),
            ("Margen", "3 dB"),
            ("EDFA", "G = 20 dB (NF = 5 dB)"),
            ("Raman", "G = 10 dB (NF = 2 dB)"),
            ("OSNR mínimo", "18 dB"),
        ],
        pasos=[
            dict(l="1) Pérdida de la fibra",
                 s="L_fibra = α × d",
                 n="L_fibra = 0.22 × 600 = 132 dB", r="132 dB"),
            dict(l="2) Pérdida total del enlace",
                 s="L_total = L_fibra + L_adicional + Margen",
                 n="L_total = 132 + 20 + 3 = 155 dB", r="155 dB"),
            dict(l="3) Número de EDFAs",
                 s="N_EDFA = L_total / G_EDFA",
                 n="N_EDFA = 155 / 20 = 7.75 ≈ 8 EDFAs", r="8 EDFAs"),
            dict(l="4) OSNR de diseño",
                 s="OSNR_diseño = OSNR_mínimo + Margen",
                 n="OSNR_diseño = 18 + 3 = 21 dB", r="21 dB"),
        ],
        cajas=[2, 3],
        correcta=("Se requieren ~8 EDFAs para compensar los 155 dB y un OSNR de diseño mínimo de "
                  "21 dB. Sin embargo, el cálculo por potencia no es una solución única: se debe "
                  "evaluar una arquitectura híbrida EDFA + Raman para controlar el ruido "
                  "acumulado."),
        errada=("Asumir que solo basta con sumar ganancia de 8 EDFAs en cascada sin analizar el "
                "ruido ASE acumulado degrada severamente el OSNR por debajo de 21 dB, haciendo "
                "inviable la transmisión aunque exista buena potencia."),
    ),
    dict(
        n=7,
        titulo="Atenuador fijo en red FTTH (OLT - ONT)",
        datos=[
            ("Prx inicial", "-4 dBm"),
            ("Rango recomendado ONT", "-28 a -9 dBm"),
            ("Prx deseado", "-13 dBm"),
            ("Atenuadores disponibles", "3, 6, 9 y 12 dB"),
        ],
        pasos=[
            dict(l="1) Comparación con el rango de la ONT",
                 s="Prx_inicial  vs  límite superior de la ONT",
                 n="-4 dBm supera el límite de -9 dBm  (exceso de potencia)",
                 r="exceso de potencia", c=AMBER),
            dict(l="2) Atenuación requerida",
                 s="A = Prx_inicial - Prx_deseado",
                 n="A = -4 - (-13) = 9 dB", r="9 dB"),
            dict(l="3) Potencia final y elección del atenuador",
                 s="Prx_final = Prx_inicial - A",
                 n="Prx_final = -4 dBm - 9 dB = -13 dBm  →  atenuador fijo de 9 dB",
                 r="-13 dBm"),
        ],
        cajas=[2],
        correcta=("La potencia inicial de -4 dBm supera el límite superior (-9 dBm) y satura la "
                  "ONT. Instalar el atenuador fijo de 9 dB ubica la recepción en -13 dBm, un "
                  "punto estable y seguro."),
        errada=("Creer que «más potencia siempre es mejor» y dejar la ONT en -4 dBm satura el "
                "fotodetector, eleva la tasa de errores, causa cortes intermitentes y genera "
                "diagnósticos falsos (potencia alta pero servicio degradado)."),
    ),
]


# ------------------------------- Utilidades --------------------------------
def parrafo(texto, ancho_car=56, font_size=30, color=TXT):
    """Párrafo con saltos de línea automáticos."""
    lineas = textwrap.wrap(texto, ancho_car)
    return VGroup(*[Text(l, font_size=font_size, color=color) for l in lineas]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.2
    )


def ajustar(mob, ancho_max, alto_max):
    """Reduce el objeto (nunca lo agranda) para que quepa en pantalla."""
    if mob.width > ancho_max:
        mob.scale_to_fit_width(ancho_max)
    if mob.height > alto_max:
        mob.scale_to_fit_height(alto_max)
    return mob


def panel(titulo, texto, color, color_titulo, ancho_max=12.4, alto_max=5.2):
    t = Text(titulo, font_size=36, weight=BOLD, color=color_titulo)
    p = parrafo(texto)
    cuerpo = VGroup(t, p).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
    ajustar(cuerpo, ancho_max - 1.2, alto_max - 0.9)  # scale_to_fit_width / height
    marco = RoundedRectangle(
        corner_radius=0.2,
        width=cuerpo.width + 1.0,
        height=cuerpo.height + 0.9,
        stroke_color=color,
        stroke_width=4,
        fill_color=color,
        fill_opacity=0.12,
    )
    cuerpo.move_to(marco).shift(RIGHT * 0.1)
    barra = RoundedRectangle(
        corner_radius=0.06, width=0.14, height=marco.height - 0.5,
        stroke_width=0, fill_color=color, fill_opacity=1,
    ).move_to(marco.get_left() + RIGHT * 0.3)
    return VGroup(marco, barra, cuerpo)


def tarjeta_dato(etiqueta, valor):
    lab = Text(etiqueta, font_size=22, color=MUTED)
    val = Text(valor, font_size=30, weight=BOLD, color=YELLOW)
    val.scale_to_fit_width(min(val.width, 3.5))
    lab.scale_to_fit_width(min(lab.width, 3.5))
    cont = VGroup(lab, val).arrange(DOWN, buff=0.15)
    rect = RoundedRectangle(
        corner_radius=0.15, width=4.0, height=1.5,
        stroke_color=SKY, stroke_width=2, fill_color=CARD, fill_opacity=1,
    )
    cont.move_to(rect)
    return VGroup(rect, cont)


# ------------------------------ Escena base --------------------------------
class BaseProblemas(Scene):
    def setup(self):
        self.camera.background_color = BG
        self.fin_voz = 0.0

    # --- narración (audio/<clave>.mp3, generado con generar_audio.py) --------
    def hablar(self, clave):
        ruta = os.path.join(AUDIO_DIR, f"{clave}.mp3")
        if not os.path.exists(ruta):
            return False
        from pydub import AudioSegment
        dur = AudioSegment.from_file(ruta).duration_seconds
        self.add_sound(ruta)
        self.fin_voz = self.renderer.time + dur + 0.5
        return True

    def esperar_voz(self):
        """Espera hasta que termine la locución en curso (si la hay)."""
        resto = self.fin_voz - self.renderer.time
        if resto > 0:
            self.wait(resto)

    # --- bloque 1 -----------------------------------------------------------
    def bloque_titulo_datos(self, p):
        num = Text(f"PROBLEMA {p['n']}", font_size=68, weight=BOLD, color=SKY)
        sub = Text(p["titulo"], font_size=38, color=TXT)
        ajustar(sub, 12.4, 2)
        tg = VGroup(num, sub).arrange(DOWN, buff=0.4)
        self.hablar(f"p{p['n']}_titulo")
        self.play(FadeIn(num, shift=UP * 0.3), run_time=1)
        self.play(Write(sub), run_time=1.5)
        self.wait(2)

        enc = Text(f"Problema {p['n']} · {p['titulo']}", font_size=30, color=SKY)
        ajustar(enc, 12.4, 1)
        linea = Line(LEFT * 6.4, RIGHT * 6.4, color=SKY, stroke_width=2)
        self.encabezado = VGroup(enc, linea).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        self.play(FadeOut(tg, shift=UP * 0.5), FadeIn(self.encabezado, shift=DOWN * 0.3))

        self.subtitulo_actual = None
        self.poner_subtitulo("1 · Datos del problema", SKY)
        tarjetas = VGroup(*[tarjeta_dato(k, v) for k, v in p["datos"]])
        tarjetas.arrange_in_grid(cols=2 if len(tarjetas) == 4 else 3, buff=(0.35, 0.35))
        ajustar(tarjetas, 12.4, 4.6)
        tarjetas.move_to(DOWN * 0.7)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tarjetas], lag_ratio=0.25))
        self.wait(4)
        self.esperar_voz()
        self.play(FadeOut(tarjetas))

    def poner_subtitulo(self, texto, color):
        nuevo = Text(texto, font_size=28, color=color).next_to(self.encabezado, DOWN, buff=0.3)
        if self.subtitulo_actual is None:
            self.play(FadeIn(nuevo, shift=DOWN * 0.2), run_time=0.6)
        else:
            self.play(FadeOut(self.subtitulo_actual), FadeIn(nuevo, shift=DOWN * 0.2),
                      run_time=0.6)
        self.subtitulo_actual = nuevo

    # --- bloque 2 -----------------------------------------------------------
    def bloque_desarrollo(self, p):
        self.poner_subtitulo("2 · Fórmulas y desarrollo paso a paso", SKY)

        filas, simbolicas = [], []
        for paso in p["pasos"]:
            color_res = paso.get("c", GREEN_OK)
            etiqueta = Text(paso["l"], font_size=24, color=MUTED)
            numerica = Text(paso["n"], font_size=32, color=TXT, t2c={paso["r"]: color_res})
            filas.append(VGroup(etiqueta, numerica).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        todo = VGroup(*filas).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # factor de ajuste automático (ancho y alto) y posición final
        factor = min(1.0, 12.2 / todo.width, 4.9 / todo.height)
        todo.scale(factor).move_to(DOWN * 0.85)

        for paso, fila in zip(p["pasos"], filas):
            sim = Text(paso["s"], font_size=32, color=YELLOW).scale(factor)
            sim.move_to(fila[1].get_left(), aligned_edge=LEFT)
            simbolicas.append(sim)

        for i, (fila, sim) in enumerate(zip(filas, simbolicas)):
            self.hablar(f"p{p['n']}_paso{i}")
            self.play(FadeIn(fila[0], shift=RIGHT * 0.2), Write(sim), run_time=1.2)
            self.wait(1.5)  # leer la ecuación base
            self.play(ReplacementTransform(sim, fila[1]), run_time=1.6)  # sustitución numérica
            self.wait(1.8)
            self.esperar_voz()

        cajas = [
            SurroundingRectangle(filas[i][1], color=GREEN_OK, buff=0.15, corner_radius=0.1,
                                 stroke_width=5)
            for i in p["cajas"]
        ]
        self.play(*[Create(c) for c in cajas], run_time=1.2)
        self.play(*[Indicate(filas[i][1], color=GREEN_OK, scale_factor=1.05) for i in p["cajas"]])
        self.wait(3.5)
        self.quitar_contenido()

    # --- bloques 3 y 4 ------------------------------------------------------
    def bloque_panel(self, subtitulo, color_sub, titulo, texto, color, color_titulo, clave):
        self.poner_subtitulo(subtitulo, color_sub)
        pnl = panel(titulo, texto, color, color_titulo).move_to(DOWN * 0.8)
        con_voz = self.hablar(clave)
        self.play(FadeIn(pnl, shift=UP * 0.3), run_time=1.2)
        if con_voz:
            self.esperar_voz()
            self.wait(1.5)
        else:
            self.wait(max(7, len(texto) / 12))  # tiempo de lectura proporcional al texto

    def quitar_contenido(self):
        """Desvanece todo salvo el encabezado y el subtítulo vigentes."""
        fijos = (self.encabezado, self.subtitulo_actual)
        resto = [m for m in self.mobjects if not any(m is f for f in fijos)]
        if resto:
            self.play(FadeOut(*resto), run_time=0.8)

    def bloque_correcta(self, p):
        self.bloque_panel("3 · Explicación de la respuesta", GREEN_OK,
                          "Interpretación técnica correcta", p["correcta"], TEAL, GREEN_OK,
                          f"p{p['n']}_correcta")
        self.quitar_contenido()

    def bloque_errada(self, p):
        self.bloque_panel("4 · Si se interpreta mal…", AMBER,
                          "Consecuencia de una interpretación errada", p["errada"],
                          RED_BAD, AMBER, f"p{p['n']}_errada")

    # --- bloque 5 -----------------------------------------------------------
    def bloque_transicion(self):
        self.wait(1)
        self.play(FadeOut(*self.mobjects), run_time=1.2)
        self.subtitulo_actual = None
        self.wait(0.5)

    def animar_problema(self, p):
        self.bloque_titulo_datos(p)
        self.bloque_desarrollo(p)
        self.bloque_correcta(p)
        self.bloque_errada(p)
        self.bloque_transicion()


# ------------------------------- Escenas -----------------------------------
class Problema4(BaseProblemas):
    def construct(self):
        self.animar_problema(PROBLEMAS[0])


class Problema5(BaseProblemas):
    def construct(self):
        self.animar_problema(PROBLEMAS[1])


class Problema6(BaseProblemas):
    def construct(self):
        self.animar_problema(PROBLEMAS[2])


class Problema7(BaseProblemas):
    def construct(self):
        self.animar_problema(PROBLEMAS[3])


class VideoCompleto(BaseProblemas):
    """Los 4 problemas en un solo video."""

    def construct(self):
        intro = Text("Ingeniería Óptica", font_size=64, weight=BOLD, color=SKY)
        sub = Text("Problemas 4, 5, 6 y 7 resueltos paso a paso", font_size=34, color=TXT)
        g = VGroup(intro, sub).arrange(DOWN, buff=0.4)
        ajustar(g, 12.4, 5)
        self.hablar("intro")
        self.play(FadeIn(intro, shift=UP * 0.3))
        self.play(Write(sub))
        self.wait(2.5)
        self.esperar_voz()
        self.play(FadeOut(g))
        self.wait(0.4)

        for p in PROBLEMAS:
            self.animar_problema(p)
