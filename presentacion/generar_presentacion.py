from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

NAVY=RGBColor(0x1B,0x3A,0x5C); BLUE=RGBColor(0x1F,0x4E,0x79); TEAL=RGBColor(0x14,0x9C,0x9A)
ORG=RGBColor(0xF2,0x8C,0x28); INK=RGBColor(0x22,0x2B,0x36); MUT=RGBColor(0x6B,0x77,0x85)
BG=RGBColor(0xF5,0xF7,0xFA); WHITE=RGBColor(255,255,255); LINE=RGBColor(0xD9,0xDF,0xE7)
FONT="Calibri"
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
blank=prs.slide_layouts[6]
TOTAL=16

def rect(s,x,y,w,h,fill,shape=MSO_SHAPE.RECTANGLE,line=None):
    r=s.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb=fill
    if line: r.line.color.rgb=line; r.line.width=Pt(0.75)
    else: r.line.fill.background()
    r.shadow.inherit=False
    return r
def text(s,x,y,w,h,t,size=16,bold=False,color=INK,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,italic=False):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(0.05); tf.margin_top=tf.margin_bottom=Inches(0.03); tf.vertical_anchor=anchor
    lines=t if isinstance(t,list) else [t]
    for i,l in enumerate(lines):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; r=p.add_run(); r.text=l
        r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic; r.font.color.rgb=color; r.font.name=FONT
        if i: p.space_before=Pt(6)
    return tb
def bullets(s,x,y,w,h,items,size=16,color=INK):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(8)
        head,_,rest=it.partition("|")
        r=p.add_run(); r.text="▪  "; r.font.color.rgb=TEAL; r.font.size=Pt(size); r.font.name=FONT
        if rest:
            r=p.add_run(); r.text=head; r.font.bold=True; r.font.size=Pt(size); r.font.color.rgb=NAVY; r.font.name=FONT
            r=p.add_run(); r.text=rest; r.font.size=Pt(size); r.font.color.rgb=color; r.font.name=FONT
        else:
            r=p.add_run(); r.text=head; r.font.size=Pt(size); r.font.color.rgb=color; r.font.name=FONT
def slide(title,n,kicker=None):
    s=prs.slides.add_slide(blank)
    s.background.fill.solid(); s.background.fill.fore_color.rgb=BG
    rect(s,0,0,13.333,0.12,NAVY); rect(s,0,0.12,13.333,0.04,TEAL)
    if kicker: text(s,0.6,0.38,9,0.3,kicker.upper(),11,True,TEAL)
    text(s,0.6,0.62,12.1,0.8,title,29,True,NAVY)
    text(s,0.6,7.05,9,0.3,"DAB/DAB+ e IBOC · Grupo 6 · UTP",10,False,MUT)
    text(s,11.7,7.05,1.05,0.3,f"{n} / {TOTAL}",10,False,MUT,PP_ALIGN.RIGHT)
    return s
def card(s,x,y,w,h,title,body,accent=TEAL,tsize=16,bsize=13.5):
    rect(s,x,y,w,h,WHITE,line=LINE); rect(s,x,y,0.08,h,accent)
    text(s,x+0.25,y+0.15,w-0.4,0.4,title,tsize,True,NAVY)
    text(s,x+0.25,y+0.62,w-0.4,h-0.7,body,bsize,False,INK)
def stat(s,x,y,w,big,small,color=NAVY):
    rect(s,x,y,w,1.35,WHITE,line=LINE)
    text(s,x,y+0.12,w,0.7,big,34,True,color,PP_ALIGN.CENTER)
    text(s,x+0.1,y+0.85,w-0.2,0.5,small,12,False,MUT,PP_ALIGN.CENTER)
def table(s,x,y,w,rows,colw,rowh=0.42,size=12,center=True):
    gt=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(rowh*len(rows)))
    t=gt.table
    tblPr=gt._element.graphic.graphicData.tbl.tblPr
    tblPr.set('bandRow','0'); tblPr.set('firstRow','0')
    for j,cw in enumerate(colw): t.columns[j].width=Inches(cw)
    for i,row in enumerate(rows):
        t.rows[i].height=Inches(rowh)
        for j,v in enumerate(row):
            c=t.cell(i,j); c.text=""; c.vertical_anchor=MSO_ANCHOR.MIDDLE
            c.margin_left=c.margin_right=Inches(0.1)
            p=c.text_frame.paragraphs[0]; r=p.add_run(); r.text=str(v); r.font.size=Pt(size); r.font.name=FONT
            c.fill.solid()
            if i==0: c.fill.fore_color.rgb=NAVY; r.font.color.rgb=WHITE; r.font.bold=True
            else:
                c.fill.fore_color.rgb=WHITE if i%2 else RGBColor(0xEE,0xF2,0xF7); r.font.color.rgb=INK
                if j==0: r.font.bold=True; r.font.color.rgb=NAVY
            if center and j>0 and i>0 and len(str(v))<14: p.alignment=PP_ALIGN.CENTER
            if center and j>0 and i==0 and len(rows[0])>3: p.alignment=PP_ALIGN.CENTER
    return t
def style_chart(ch,legend=True,size=12):
    ch.font.size=Pt(size); ch.font.name=FONT; ch.font.color.rgb=INK
    ch.has_legend=legend
    if legend: ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout=False
def bar(s,x,y,w,h,cats,series,colors,horizontal=False,fmt='0.0',legend=True,maxv=None,gap=60):
    cd=CategoryChartData(); cd.categories=cats
    for n,v in series: cd.add_series(n,v)
    gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(x),Inches(y),Inches(w),Inches(h),cd)
    ch=gf.chart; style_chart(ch,legend)
    pl=ch.plots[0]; pl.gap_width=gap; pl.has_data_labels=True
    dl=pl.data_labels; dl.number_format=fmt; dl.number_format_is_linked=False; dl.font.size=Pt(12); dl.position=XL_LABEL_POSITION.OUTSIDE_END
    for i,sr in enumerate(pl.series):
        sr.format.fill.solid(); sr.format.fill.fore_color.rgb=colors[i]
    va=ch.value_axis; va.visible=False; va.has_major_gridlines=False
    if maxv: va.maximum_scale=maxv
    va.minimum_scale=0
    ca=ch.category_axis; ca.format.line.color.rgb=LINE; ca.tick_labels.font.size=Pt(12)
    if horizontal: ca.reverse_order=True
    return ch

# 1 Portada
s=prs.slides.add_slide(blank); s.background.fill.solid(); s.background.fill.fore_color.rgb=NAVY
rect(s,0,0,0.35,7.5,TEAL)
text(s,1.0,0.7,11,0.4,"UNIVERSIDAD TECNOLÓGICA DEL PERÚ  ·  FACULTAD DE INGENIERÍA",13,True,RGBColor(0x9F,0xD6,0xD5))
text(s,1.0,1.1,11,0.4,"Sistemas de Radiodifusión y Televisión Digital",13,False,RGBColor(0xC9,0xD6,0xE3))
text(s,1.0,2.0,11.3,2.2,["Radiodifusión sonora digital:","DAB/DAB+ frente a IBOC (HD Radio)"],42,True,WHITE)
text(s,1.0,4.05,11,0.6,"Análisis comparativo y estudio de caso para Lima Metropolitana",22,False,RGBColor(0xF6,0xC2,0x8B))
rect(s,1.0,4.9,1.6,0.05,ORG)
text(s,1.0,5.15,11,1.3,["Grupo 6","Fabrizzio Reyes · Eslin Lopez · Benjamin Zanabria · Miguel San Miguel · Pablo Sánchez","Docente: Jaime Andres Rupaylla Arestegui  ·  Lima, noviembre de 2026"],14,False,RGBColor(0xC9,0xD6,0xE3))

# 2 Contexto
s=slide("La radio sigue siendo analógica en un dial saturado",2,"Contexto")
card(s,0.6,1.7,3.9,2.6,"Tecnología heredada","AM (1920) y FM (1940): sensibles al ruido y al multitrayecto, un programa por portadora y casi sin datos.",ORG)
card(s,4.7,1.7,3.9,2.6,"Perú sin estándar","La TV adoptó ISDB-T en 2009; la radio digital aún no tiene estándar adoptado formalmente.",TEAL)
card(s,8.8,1.7,3.9,2.6,"Lima saturada","La banda FM de 88–108 MHz está prácticamente llena: no entran nuevos operadores.",BLUE)
text(s,0.6,4.65,12,0.4,"Por qué estudiarlo",16,True,NAVY)
bullets(s,0.6,5.1,12,1.9,["Técnica|  más programas con calidad cercana al CD en el ancho de banda de una emisora.",
 "Social|  alertas tempranas (EWF) en un país expuesto a sismos y tsunamis.",
 "Económica|  una docena de programas con una fracción de la energía de la FM."],15)

# 3 Objetivos
s=slide("Objetivo y alcance del estudio",3,"Introducción")
rect(s,0.6,1.7,12.1,1.3,NAVY)
text(s,0.9,1.8,11.5,1.1,"Analizar y comparar DAB/DAB+ e IBOC en operación, especificaciones, cobertura y nivel de servicio, y aplicarlo al diseño de una solución de radio digital para Lima Metropolitana.",18,False,WHITE,anchor=MSO_ANCHOR.MIDDLE)
steps=[("1","Principios","OFDM, codificación de canal y de audio"),("2","Comparación","Frente a analógica, DRM+, satélite e Internet"),("3","Especificaciones","Bandas, modos, propagación y redes"),("4","Dimensionamiento","Múltiplex DAB+ y conversión IBOC"),("5","Servicio","Indicadores QoS, QoE y SLA")]
for i,(n,t,d) in enumerate(steps):
    x=0.6+i*2.45
    rect(s,x,3.4,2.3,3.2,WHITE,line=LINE)
    c=rect(s,x+0.75,3.6,0.8,0.8,TEAL,MSO_SHAPE.OVAL); 
    text(s,x+0.75,3.7,0.8,0.6,n,24,True,WHITE,PP_ALIGN.CENTER)
    text(s,x+0.1,4.6,2.1,0.4,t,16,True,NAVY,PP_ALIGN.CENTER)
    text(s,x+0.15,5.1,2.0,1.4,d,13,False,INK,PP_ALIGN.CENTER)

# 4 Dos filosofías
s=slide("Misma base técnica, filosofías opuestas",4,"Marco teórico")
for x,col,name,sub,items in [(0.6,TEAL,"DAB / DAB+","Eureka-147 · ETSI (Europa)",["Banda nueva (Banda III VHF)","Múltiplex compartido: 12–20 programas","Redes de frecuencia única (SFN)","Códec abierto HE-AAC v2"]),
                            (6.85,ORG,"IBOC / HD Radio","NRSC-5 · iBiquity/Xperi (EE. UU.)",["Mismo canal de la emisora AM/FM","Portadoras digitales en los bordes","Transición gradual, receptor analógico sigue sirviendo","Códec propietario HDC con regalías"])]:
    rect(s,x,1.7,5.85,4.6,WHITE,line=LINE); rect(s,x,1.7,5.85,1.2,col)
    text(s,x+0.3,1.78,5.3,0.6,name,28,True,WHITE); text(s,x+0.3,2.4,5.3,0.4,sub,14,False,WHITE)
    bullets(s,x+0.3,3.15,5.3,3,items,16)
rect(s,5.85,3.6,1.15,0.9,NAVY,MSO_SHAPE.OVAL); text(s,5.85,3.78,1.15,0.5,"vs",20,True,WHITE,PP_ALIGN.CENTER)
text(s,0.6,6.45,12.1,0.45,"Comparten COFDM, codificación convolucional, entrelazado y códecs de la familia AAC.",14,False,MUT,PP_ALIGN.CENTER,italic=True)

# 5 Tabla comparativa
s=slide("Comparación técnica DAB+ frente a IBOC",5,"Análisis comparativo")
rows=[["Parámetro","DAB+","IBOC FM"],["Espectro","Nuevo: bloques de 1,712 MHz","El canal de la emisora existente"],
["Ancho de banda","1,536 MHz por múltiplex","≈ 2 × 69 kHz (bandas laterales)"],["Modulación","COFDM π/4-DQPSK, 1536 portadoras","COFDM QPSK, hasta 1093 subportadoras"],
["Separación de portadoras","1 kHz (modo I)","363,373 Hz"],["Intervalo de guarda","246 µs","≈ 150 µs"],
["Códec de audio","HE-AAC v2 (abierto)","HDC (propietario)"],["Capacidad","≈ 1152 kbit/s netos por múltiplex","≈ 100–150 kbit/s por emisora"]]
table(s,0.6,1.7,12.1,rows,[2.9,4.6,4.6],0.58,14,center=False)
text(s,0.6,6.45,12.1,0.4,"Fuente: informe técnico, Tabla 2 y capítulo 5.",11,False,MUT)

# 6 Matriz
s=slide("DAB+ lidera la matriz de decisión para el Perú",6,"Análisis comparativo")
bar(s,0.6,1.6,6.6,5.2,["DAB+","IBOC","DRM+"],[("Puntaje ponderado",(7.6,6.9,6.55))],[TEAL],fmt='0.00',legend=False,maxv=9)
ch=s.shapes[-1].chart; pts=ch.plots[0].series[0].points
for i,c in enumerate([TEAL,ORG,MUT]): pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=c
text(s,7.6,1.7,5.1,0.4,"Siete criterios ponderados",16,True,NAVY)
bullets(s,7.6,2.2,5.1,3.2,["DAB+ 7,60|  eficiencia espectral, receptores y datos.","IBOC 6,90|  bajo costo de transición y sin espectro nuevo.","DRM+ 6,55|  sólido, pero con pocos receptores."],15)
rect(s,7.6,5.1,5.1,1.5,WHITE,line=LINE); rect(s,7.6,5.1,0.08,1.5,ORG)
text(s,7.85,5.2,4.7,1.3,"Si se prioriza costo y espectro (0,25 cada uno), IBOC se acerca a DAB+: refuerza una estrategia combinada.",14,False,INK,anchor=MSO_ANCHOR.MIDDLE)

# 7 Escenario A
s=slide("Escenario A: múltiplex DAB+ en bloque 12C",7,"Estudio de caso · Lima")
stat(s,0.6,1.7,2.9,"14 + 2","servicios de audio y de datos",TEAL)
stat(s,3.7,1.7,2.9,"75,7 %","de capacidad usada (654 de 864 CU)",NAVY)
stat(s,0.6,3.25,2.9,"227,36 MHz","bloque 12C, modo I",BLUE)
stat(s,3.7,3.25,2.9,"1152 kbit/s","capacidad neta, EEP-3A",ORG)
bullets(s,0.6,4.85,6.1,2,["Reserva|  210 CU (280 kbit/s): 3–4 programas más.","Equivalente en FM|  2,8 MHz frente a 1,712 MHz."],14)
cd=CategoryChartData(); cd.categories=["Asignadas","Reserva"]; cd.add_series("CU",(654,210))
gf=s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT,Inches(7.2),Inches(1.6),Inches(5.5),Inches(5.2),cd); ch=gf.chart; style_chart(ch,True,13)
pl=ch.plots[0]; pl.has_data_labels=True; pl.data_labels.number_format='0'; pl.data_labels.number_format_is_linked=False; pl.data_labels.font.size=Pt(14); pl.data_labels.font.bold=True; pl.data_labels.font.color.rgb=WHITE
for i,c in enumerate([TEAL,LINE]): pt=pl.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=c
ch.has_title=True; ch.chart_title.text_frame.text="Ocupación del múltiplex (CU)"; ch.chart_title.text_frame.paragraphs[0].runs[0].font.size=Pt(14); ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold=True

# 8 Balance de enlace
s=slide("Un solo transmisor no alcanza el interior de toda Lima",8,"Estudio de caso · Balance de enlace")
bar(s,0.6,1.6,7.4,5.2,["Móvil","Portátil exterior","Portátil interior"],[("Radio urbano (km)",(30.2,41.1,14.8)),("Radio suburbano (km)",(52.0,70.8,25.5))],[TEAL,BLUE],fmt='0.0',maxv=85)
text(s,8.4,1.7,4.3,0.4,"Transmisor en Cerro San Cristóbal",16,True,NAVY)
bullets(s,8.4,2.2,4.3,2.6,["10 kW PRA|  2,5 kW + 8 dBd de ganancia.","Ruido artificial|  figura de 9,7 dB en Banda III (17,6 dB en FM).","Modelo|  Okumura-Hata, hb = 200 m."],14)
rect(s,8.4,5.0,4.3,1.6,NAVY); text(s,8.6,5.05,3.9,1.5,"Interior: solo 14,8 km. El cono norte y sur están a 15–30 km: se necesita una SFN.",15,True,WHITE,anchor=MSO_ANCHOR.MIDDLE)

# 9 SFN
s=slide("Red de frecuencia única de cuatro sitios",9,"Estudio de caso · SFN")
rows=[["Par de sitios","Distancia (km)","Δt máx. (µs)","¿< 246 µs?"],["San Cristóbal – Morro Solar","16,5","55,0","Sí"],["San Cristóbal – Carabayllo","18,2","60,7","Sí"],["San Cristóbal – Ate/Huachipa","14,3","47,7","Sí"],["Morro Solar – Carabayllo","34,0","113,4","Sí"],["Carabayllo – Ate/Huachipa","27,0","90,1","Sí"]]
table(s,0.6,1.8,7.6,rows,[3.4,1.5,1.4,1.3],0.6,14)
stat(s,8.6,1.8,4.1,"4 sitios","1 principal de 2,5 kW + 3 de relleno de 1 kW",TEAL)
stat(s,8.6,3.35,4.1,"73,7 km","distancia equivalente al intervalo de guarda",NAVY)
bullets(s,0.6,5.7,12,1.2,["Sincronismo|  GPS y alimentación EDI sobre fibra con respaldo IP.","Sin autointerferencia|  todas las distancias son menores que 73,7 km."],14)

# 10 IBOC
s=slide("Escenario B: IBOC híbrido necesita al menos −14 dBc",10,"Estudio de caso · Conversión de una FM de 30 kW")
bar(s,0.6,1.6,7.6,5.2,["FM analógica","−20 dBc","−14 dBc","−10 dBc"],[("Radio móvil urbano (km)",(28.4,22.5,35.8,48.7))],[BLUE],legend=False,maxv=58)
ch=s.shapes[-1].chart; pts=ch.plots[0].series[0].points
for i,c in enumerate([MUT,ORG,TEAL,TEAL]): pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=c
text(s,8.6,1.7,4.1,0.4,"Qué significa",16,True,NAVY)
bullets(s,8.6,2.2,4.1,3,["−20 dBc|  22,5 km: menor que la analógica; blend constante.","−14 dBc|  35,8 km: supera a la analógica.","Capacidad|  ≈ 98 kbit/s en MP1: 2–3 programas."],14)
rect(s,8.6,5.3,4.1,1.3,WHITE,line=LINE); rect(s,8.6,5.3,0.08,1.3,ORG)
text(s,8.85,5.35,3.8,1.2,"Equiparar 14 programas exigiría convertir 14 emisoras.",14,False,INK,anchor=MSO_ANCHOR.MIDDLE)

# 11 Energía
s=slide("DAB+ consume ≈ 14 veces menos energía por programa",11,"Estudio de caso · Eficiencia energética")
bar(s,0.6,1.6,6.3,5.2,["FM analógica","DAB+ (SFN)"],[("Energía anual (MWh)",(2008,146))],[ORG],fmt='#,##0',legend=False,maxv=2400)
ch=s.shapes[-1].chart; pts=ch.plots[0].series[0].points
for i,c in enumerate([ORG,TEAL]): pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=c
ch.has_title=True; ch.chart_title.text_frame.text="Energía anual para 14 programas (MWh)"; r=ch.chart_title.text_frame.paragraphs[0].runs[0]; r.font.size=Pt(14); r.font.bold=True
stat(s,7.3,1.7,2.65,"13,8×","relación FM / DAB+",ORG)
stat(s,10.05,1.7,2.65,"1 862 MWh","ahorro anual estimado",TEAL)
rows=[["","FM","DAB+"],["Consumo total (kW)","229,3","16,7"],["Por programa (kW)","16,38","1,19"],["Eficiencia global","65 %","33 %"]]
table(s,7.3,3.5,5.4,rows,[2.4,1.5,1.5],0.55,14)
text(s,7.3,5.9,5.4,0.9,"Aun con amplificadores COFDM menos eficientes y tres sitios de relleno.",13,False,MUT,italic=True)

# 12 Equipamiento
s=slide("Equipamiento propuesto",12,"Estudio de caso · Hojas de datos")
card(s,0.6,1.7,5.9,2.4,"Escenario A · DAB+",["GatesAir Maxiva VAXT-HE: transmisor","AVT MAGIC DABMUX plus: codificación y multiplexación","Receptores y analizadores DAB para drive test"],TEAL,bsize=14)
card(s,6.8,1.7,5.9,2.4,"Escenario B · IBOC",["Nautel GV2: transmisor FM híbrido","GatesAir Flexiva FMXi 4g: importador/exportador HD Radio","Receptores HD Radio y equipos de medición"],ORG,bsize=14)
rect(s,0.6,4.5,12.1,2.0,WHITE,line=LINE)
text(s,0.9,4.6,11.5,0.4,"Modelo de inversión",16,True,NAVY)
bullets(s,0.9,5.05,11.5,1.4,["DAB+|  la inversión recae en el operador del múltiplex; cada emisora paga según sus CU.","IBOC|  cada emisora invierte en excitador, importador/exportador, licencia y quizá un transmisor nuevo."],14)

# 13 QoS QoE SLA
s=slide("Nivel de servicio: QoS, QoE y SLA",13,"Evaluación")
stat(s,0.6,1.7,3.0,"99,988 %","disponibilidad calculada (≈ 63 min/año)",TEAL)
stat(s,0.6,3.25,3.0,"99,95 %","SLA mensual propuesto",NAVY)
rows=[["Indicador","Objetivo"],["Campo mediano (portátil interior)","≥ 62 dBµV/m"],["C/N móvil","≥ 15 dB"],["MER en el transmisor","≥ 30 dB"],["Sincronismo SFN","≤ 1 µs"],["Cobertura de ubicaciones","≥ 95 % interior · ≥ 99 % móvil"],["Calidad de audio (MUSHRA)","≥ 70 música · ≥ 60 hablado"],["Activación de alerta EWF","≤ 10 s"]]
table(s,3.9,1.7,8.8,rows,[4.4,4.4],0.55,14)
text(s,0.6,4.8,3.0,1.8,"Punto crítico: el sistema radiante no se duplica; se propone antena en dos mitades con alimentación independiente.",12.5,False,MUT,italic=True)

# 14 Conclusiones
s=slide("Conclusiones",14,"Cierre")
items=[("DAB+","1152 kbit/s netos: 14 programas y 2 servicios de datos con el 76 % de la capacidad.",TEAL),
("SFN","Un transmisor cubre ≈ 30 km móvil pero solo ≈ 15 km en interiores: se requieren 4 sitios.",BLUE),
("IBOC","−20 dBc queda corto frente a la analógica; −14 dBc es el mínimo útil.",ORG),
("Energía","≈ 14 veces menos consumo por programa y 1 862 MWh/año de ahorro.",TEAL),
("Decisión","DAB+ 7,60 frente a IBOC 6,90; depende del espectro en Banda III tras el apagado analógico.",NAVY),
("Servicio","99,988 % de disponibilidad, compatible con un SLA de 99,95 %.",BLUE)]
for i,(t,b,c) in enumerate(items):
    x=0.6+(i%3)*4.1; y=1.7+(i//3)*2.65
    card(s,x,y,3.9,2.45,t,b,c,tsize=18,bsize=14)

# 15 Recomendaciones
s=slide("Recomendaciones",15,"Cierre")
rec=[("MTC","Evaluar reservar un segmento de Banda III (216–230 MHz) y definir un marco de pilotos."),
("Piloto","DAB+ en Lima con transmisor principal y un sitio de relleno, con drive test."),
("Planificación","Usar UIT-R P.1812/P.1546 con DEM y población por manzana."),
("IBOC","Operar como mínimo a −14 dBc y estudiar interferencia en canales adyacentes."),
("Alertas","Incluir EWF e integrar con el Sistema de Alerta Temprana del INDECI."),
("Ecosistema","Receptores digitales en autos y teléfonos; múltiplex con capacidad para medios públicos, educativos y lenguas originarias.")]
for i,(t,b) in enumerate(rec):
    x=0.6+(i%2)*6.15; y=1.65+(i//2)*1.7
    rect(s,x,y,5.95,1.5,WHITE,line=LINE); rect(s,x+0.2,y+0.35,0.75,0.75,TEAL,MSO_SHAPE.OVAL)
    text(s,x+0.2,y+0.47,0.75,0.5,str(i+1),20,True,WHITE,PP_ALIGN.CENTER)
    text(s,x+1.15,y+0.12,4.7,0.4,t,16,True,NAVY); text(s,x+1.15,y+0.55,4.7,0.95,b,13,False,INK)

# 16 Cierre
s=prs.slides.add_slide(blank); s.background.fill.solid(); s.background.fill.fore_color.rgb=NAVY
rect(s,0,0,0.35,7.5,TEAL)
text(s,1.0,1.4,11,0.5,"PERSPECTIVAS",13,True,RGBColor(0x9F,0xD6,0xD5))
text(s,1.0,1.9,11.3,1.4,"Planificar la radio digital junto con el apagado de la TV analógica",36,True,WHITE)
for i,(t,d) in enumerate([("Radio híbrida","RadioDNS: metadatos y streaming"),("5G Broadcast","Radiodifusión al teléfono"),("xHE-AAC","Más programas por múltiplex"),("Alertas","Infraestructura crítica")]):
    x=1.0+i*2.95; rect(s,x,4.2,2.75,1.5,RGBColor(0x24,0x4A,0x73))
    text(s,x+0.15,4.3,2.5,0.4,t,16,True,RGBColor(0xF6,0xC2,0x8B)); text(s,x+0.15,4.85,2.5,0.8,d,13,False,WHITE)
text(s,1.0,6.3,11,0.5,"¡Gracias!  ·  Grupo 6",20,True,WHITE)

prs.save("/home/user/mi-proyecto/presentacion/DAB_IBOC_Grupo6.pptx")
