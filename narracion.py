# -*- coding: utf-8 -*-
"""Textos de la narración (escritos para ser hablados) de cada problema."""

NARRACION = {
    "intro": ("Bienvenido. En este video resolveremos paso a paso los problemas cuatro, cinco, "
              "seis y siete de ingeniería óptica, y veremos qué significa cada resultado y qué "
              "pasa si lo interpretamos mal."),
    # ---------------- Problema 4 ----------------
    "p4_titulo": ("Problema cuatro. Cálculo del atenuador óptico variable, o VOA, en un enlace "
                  "DWDM. El transmisor entrega más 3 dBm. El enlace mide 40 kilómetros, con una "
                  "atenuación de 0 coma 25 decibeles por kilómetro. Hay un aislador de 0 coma 6 "
                  "decibeles y dos conectores de 0 coma 4 decibeles cada uno. El receptor acepta "
                  "potencias entre menos 18 y menos 6 dBm, y queremos recibir menos 10 dBm."),
    "p4_paso0": ("Paso uno. La pérdida de la fibra es la atenuación por la distancia: 0 coma 25 "
                 "por 40 kilómetros, igual a 10 decibeles."),
    "p4_paso1": ("Paso dos. Sumamos todas las pérdidas pasivas, sin el atenuador: los 10 decibeles "
                 "de fibra, más 0 coma 6 del aislador, más dos conectores de 0 coma 4. En total, "
                 "11 coma 4 decibeles."),
    "p4_paso2": ("Paso tres. La potencia que llega hoy al receptor es la del transmisor menos las "
                 "pérdidas: más 3 menos 11 coma 4, igual a menos 8 coma 4 dBm."),
    "p4_paso3": ("Paso cuatro. El atenuador requerido es la potencia actual menos la deseada: "
                 "menos 8 coma 4 menos menos 10, igual a 1 coma 6 decibeles. Ese es el valor del "
                 "VOA que debemos instalar."),
    "p4_correcta": ("Aunque menos 8 coma 4 dBm está dentro del rango del receptor, queda muy cerca "
                    "del límite superior, que es menos 6. Instalar el VOA de 1 coma 6 decibeles "
                    "lleva la potencia a menos 10 dBm. Así aseguramos margen de operación y "
                    "evitamos que el receptor se sature."),
    "p4_errada": ("Ahora, el error. Si no instalamos el atenuador, creyendo que menos 8 coma 4 ya "
                  "es válido, el receptor queda con poco margen. Cualquier aumento de potencia "
                  "del transmisor, o una pérdida real menor, puede saturarlo. Eso genera errores "
                  "de bit, el famoso BER, e inestabilidad en el sistema DWDM."),
    # ---------------- Problema 5 ----------------
    "p5_titulo": ("Problema cinco. Presupuesto óptico y amplificación con EDFA en el enlace Lima "
                  "Huaral. El transmisor entrega 0 dBm en 1550 nanómetros. La distancia es de 80 "
                  "kilómetros, con 0 coma 22 decibeles por kilómetro. Hay 2 decibeles de pérdidas "
                  "adicionales y reservamos un margen de 3 decibeles. La sensibilidad del receptor "
                  "es menos 18 dBm. El EDFA da 20 decibeles de ganancia, pero su salida máxima es "
                  "más 17 dBm."),
    "p5_paso0": ("Paso uno. La pérdida de la fibra es 0 coma 22 por 80 kilómetros, igual a 17 "
                 "coma 6 decibeles."),
    "p5_paso1": ("Paso dos. La pérdida total suma la fibra, las pérdidas adicionales y el margen "
                 "de ingeniería: 17 coma 6, más 2, más 3, igual a 22 coma 6 decibeles."),
    "p5_paso2": ("Paso tres. Sin amplificador, la potencia recibida es 0 menos 22 coma 6, o sea "
                 "menos 22 coma 6 dBm. Esto es menor que la sensibilidad de menos 18, así que el "
                 "enlace no opera."),
    "p5_paso3": ("Paso cuatro. Con el EDFA, la salida teórica sería 0 más 20, igual a más 20 dBm. "
                 "Pero el equipo está limitado a más 17 dBm, y ese es el valor real que debemos "
                 "usar."),
    "p5_paso4": ("Paso cinco. Con el EDFA, la potencia recibida es 17 menos 22 coma 6, igual a "
                 "menos 5 coma 6 dBm, muy por encima de la sensibilidad del receptor."),
    "p5_correcta": ("Sin EDFA se reciben menos 22 coma 6 dBm, un valor inferior a la sensibilidad "
                    "mínima de menos 18, por lo que el enlace no funciona. Con el EDFA, limitado "
                    "a más 17 dBm, se reciben menos 5 coma 6 dBm. Logramos una operación estable "
                    "y con buen margen."),
    "p5_errada": ("El error aquí es doble. Ignorar el margen de ingeniería de 3 decibeles, es "
                  "decir diseñar al límite, o asumir que el EDFA entrega más 20 dBm sin revisar "
                  "su máximo de más 17. Ambos errores producen cálculos irreales, y el enlace se "
                  "cae cuando aparecen degradaciones futuras."),
    # ---------------- Problema 6 ----------------
    "p6_titulo": ("Problema seis. Enlace de larga distancia entre Lima y Trujillo: cuántos EDFAs "
                  "necesitamos y qué OSNR de diseño. La distancia es de 600 kilómetros, con 0 coma "
                  "22 decibeles por kilómetro, 20 decibeles de pérdidas adicionales y 3 de margen. "
                  "Cada EDFA da 20 decibeles de ganancia, con figura de ruido de 5. El amplificador "
                  "Raman da 10 decibeles, con figura de ruido de 2. El OSNR mínimo es 18 "
                  "decibeles."),
    "p6_paso0": ("Paso uno. La fibra pierde 0 coma 22 por 600 kilómetros, es decir, 132 "
                 "decibeles."),
    "p6_paso1": ("Paso dos. La pérdida total es 132, más 20, más 3, igual a 155 decibeles."),
    "p6_paso2": ("Paso tres. El número de EDFAs es la pérdida total dividida entre la ganancia de "
                 "cada uno: 155 entre 20 es 7 coma 75. Redondeando hacia arriba, necesitamos 8 "
                 "EDFAs."),
    "p6_paso3": ("Paso cuatro. El OSNR de diseño es el mínimo más el margen: 18 más 3, igual a 21 "
                 "decibeles."),
    "p6_correcta": ("Se requieren aproximadamente 8 EDFAs para compensar los 155 decibeles, y un "
                    "OSNR de diseño mínimo de 21 decibeles. Pero ojo: el cálculo por potencia no "
                    "es una solución única. Hay que evaluar una arquitectura híbrida, EDFA más "
                    "Raman, para controlar el ruido acumulado."),
    "p6_errada": ("El error sería pensar que basta con sumar la ganancia de 8 EDFAs en cascada, "
                  "sin analizar el ruido ASE acumulado. Ese ruido degrada severamente el OSNR por "
                  "debajo de 21 decibeles, y la transmisión se vuelve inviable, aunque haya buena "
                  "potencia."),
    # ---------------- Problema 7 ----------------
    "p7_titulo": ("Problema siete. Atenuador fijo en una red FTTH, entre la OLT y la ONT. La "
                  "potencia recibida inicial es menos 4 dBm. El rango recomendado de la ONT va de "
                  "menos 28 a menos 9 dBm. Queremos llegar a menos 13 dBm, y disponemos de "
                  "atenuadores de 3, 6, 9 y 12 decibeles."),
    "p7_paso0": ("Paso uno. Comparamos: menos 4 dBm es mayor que el límite superior de menos 9 "
                 "dBm. Es decir, hay exceso de potencia."),
    "p7_paso1": ("Paso dos. La atenuación requerida es la potencia inicial menos la deseada: "
                 "menos 4 menos menos 13, igual a 9 decibeles."),
    "p7_paso2": ("Paso tres. La potencia final es menos 4 menos 9, igual a menos 13 dBm. Entre los "
                 "atenuadores disponibles, elegimos el fijo de 9 decibeles."),
    "p7_correcta": ("La potencia inicial de menos 4 dBm supera el límite superior de menos 9 y "
                    "satura la ONT. Al instalar el atenuador fijo de 9 decibeles, la recepción "
                    "queda en menos 13 dBm, un punto estable y seguro."),
    "p7_errada": ("El error común es creer que más potencia siempre es mejor, y dejar la ONT en "
                  "menos 4 dBm. Eso satura el fotodetector, aumenta la tasa de errores, causa "
                  "cortes intermitentes y genera diagnósticos falsos: la potencia se ve alta, "
                  "pero el servicio está degradado."),
}
