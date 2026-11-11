from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor as C
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from PIL import Image
M="orig/x/ppt/media/image%d.png"
DK=C(0x1E,0x3A,0x2F); SG=C(0x7D,0x9B,0x7E); LSG=C(0xE4,0xEC,0xE4); CR=C(0xF6,0xF4,0xEE)
RED=C(0xC8,0x10,0x2E); INK=C(0x25,0x2D,0x29); MUT=C(0x6A,0x74,0x6E); WH=C(255,255,255); LN=C(0xD8,0xDF,0xD8); GOLD=C(0xD9,0x9A,0x2B)
F="Calibri"; prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5); BL=prs.slide_layouts[6]
N=[0]; TOTAL=25
def rect(s,x,y,w,h,fill,shape=MSO_SHAPE.RECTANGLE,line=None):
    r=s.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h)); r.fill.solid(); r.fill.fore_color.rgb=fill
    if line: r.line.color.rgb=line; r.line.width=Pt(.75)
    else: r.line.fill.background()
    r.shadow.inherit=False; return r
def text(s,x,y,w,h,t,size=16,bold=False,color=INK,al=PP_ALIGN.LEFT,anc=MSO_ANCHOR.TOP,it=False):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anc
    tf.margin_left=tf.margin_right=Inches(.05); tf.margin_top=tf.margin_bottom=Inches(.03)
    for i,l in enumerate(t if isinstance(t,list) else [t]):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.alignment=al
        if i: p.space_before=Pt(6)
        r=p.add_run(); r.text=l; r.font.size=Pt(size); r.font.bold=bold; r.font.italic=it; r.font.color.rgb=color; r.font.name=F
    return tb
def bullets(s,x,y,w,h,items,size=16,mark=SG):
    tf=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)).text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(9)
        h_,_,r_=it.partition("|")
        r=p.add_run(); r.text="●  "; r.font.size=Pt(size*.6); r.font.color.rgb=mark; r.font.name=F
        if r_:
            r=p.add_run(); r.text=h_; r.font.bold=True; r.font.size=Pt(size); r.font.color.rgb=DK; r.font.name=F
            r=p.add_run(); r.text=r_; r.font.size=Pt(size); r.font.color.rgb=INK; r.font.name=F
        else:
            r=p.add_run(); r.text=h_; r.font.size=Pt(size); r.font.color.rgb=INK; r.font.name=F
def pic(s,path,x,y,w,h,cover=True):
    im=Image.open(path); iw,ih=im.size; p=s.shapes.add_picture(path,Inches(x),Inches(y),Inches(w),Inches(h))
    if cover:
        ar=w/h; iar=iw/ih
        if iar>ar: c=(1-ar/iar)/2; p.crop_left=c; p.crop_right=c
        else: c=(1-iar/ar)/2; p.crop_top=c; p.crop_bottom=c
    return p
def fit(s,path,x,y,w,h):
    iw,ih=Image.open(path).size; sc=min(w/iw,h/ih); ww,hh=iw*sc,ih*sc
    return s.shapes.add_picture(path,Inches(x+(w-ww)/2),Inches(y+(h-hh)/2),Inches(ww),Inches(hh))
def slide(title,kick):
    N[0]+=1; s=prs.slides.add_slide(BL); s.background.fill.solid(); s.background.fill.fore_color.rgb=CR
    rect(s,0,0,.28,7.5,DK); rect(s,0,0,.28,1.6,RED)
    text(s,.7,.38,9,.3,kick.upper(),11,True,RED); text(s,.7,.66,12,.8,title,28,True,DK)
    text(s,.7,7.08,9,.3,"DAB/DAB+ e IBOC · Grupo 6 · UTP",10,False,MUT); text(s,11.6,7.08,1.1,.3,f"{N[0]} / {TOTAL}",10,False,MUT,PP_ALIGN.RIGHT)
    return s
def card(s,x,y,w,h,title,body,acc=SG,ts=16,bs=13.5,fill=WH):
    bs=bs*1.15
    rect(s,x,y,w,h,fill,line=LN); rect(s,x,y,w,.07,acc)
    text(s,x+.2,y+.2,w-.4,.45,title,ts,True,DK)
    if isinstance(body,list): bullets(s,x+.2,y+.7,w-.4,h-.8,body,bs,acc)
    else: text(s,x+.2,y+.7,w-.4,h-.8,body,bs,False,INK)
def stat(s,x,y,w,big,small,col=DK,h=1.35):
    tc=C(0x4A,0x73,0x58) if col==SG else (C(0xA8,0x70,0x10) if col==GOLD else col)
    rect(s,x,y,w,h,WH,line=LN); rect(s,x,y,.07,h,col)
    text(s,x+.1,y+.1,w-.15,.7,big,30,True,tc,PP_ALIGN.CENTER); text(s,x+.15,y+.82,w-.3,.5,small,12,False,MUT,PP_ALIGN.CENTER)
def table(s,x,y,w,rows,cw,rh=.5,size=13,center=False):
    g=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(rh*len(rows))); t=g.table
    pr=g._element.graphic.graphicData.tbl.tblPr; pr.set('bandRow','0'); pr.set('firstRow','0')
    for j,c in enumerate(cw): t.columns[j].width=Inches(c)
    for i,row in enumerate(rows):
        t.rows[i].height=Inches(rh)
        for j,v in enumerate(row):
            c=t.cell(i,j); c.text=""; c.vertical_anchor=MSO_ANCHOR.MIDDLE; c.margin_left=c.margin_right=Inches(.12)
            p=c.text_frame.paragraphs[0]; r=p.add_run(); r.text=str(v); r.font.size=Pt(size); r.font.name=F; c.fill.solid()
            if i==0: c.fill.fore_color.rgb=DK; r.font.color.rgb=WH; r.font.bold=True
            else:
                c.fill.fore_color.rgb=WH if i%2 else LSG; r.font.color.rgb=INK
                if j==0: r.font.bold=True; r.font.color.rgb=DK
            if center and j>0: p.alignment=PP_ALIGN.CENTER
def chart(s,x,y,w,h,cats,series,cols,horiz=False,fmt='0.0',legend=True,maxv=None,title=None,point_cols=None,gap=55,lsize=12):
    cd=CategoryChartData(); cd.categories=cats
    for n,v in series: cd.add_series(n,v)
    ch=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED if horiz else XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(x),Inches(y),Inches(w),Inches(h),cd).chart
    ch.font.size=Pt(lsize); ch.font.name=F; ch.font.color.rgb=INK; ch.has_legend=legend
    if legend: ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout=False
    pl=ch.plots[0]; pl.gap_width=gap; pl.has_data_labels=True; d=pl.data_labels; d.number_format=fmt; d.number_format_is_linked=False; d.font.size=Pt(lsize); d.position=XL_LABEL_POSITION.OUTSIDE_END
    for i,sr in enumerate(pl.series): sr.format.fill.solid(); sr.format.fill.fore_color.rgb=cols[i]
    if point_cols:
        for i,c in enumerate(point_cols): pt=pl.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=c
    va=ch.value_axis; va.visible=False; va.has_major_gridlines=False; va.minimum_scale=0
    if maxv: va.maximum_scale=maxv
    ca=ch.category_axis; ca.format.line.color.rgb=LN
    if horiz: ca.reverse_order=True
    if title:
        ch.has_title=True; ch.chart_title.text_frame.text=title; r=ch.chart_title.text_frame.paragraphs[0].runs[0]; r.font.size=Pt(14); r.font.bold=True; r.font.color.rgb=DK
    return ch
def imgcard(s,path,x,y,w,h,cap=None):
    rect(s,x,y,w,h,WH,line=LN); fit(s,path,x+.15,y+.15,w-.3,h-.3-(.35 if cap else 0))
    if cap: text(s,x,y+h-.45,w,.35,cap,11,False,MUT,PP_ALIGN.CENTER,it=True)

# 1 Portada
N[0]+=1; s=prs.slides.add_slide(BL); s.background.fill.solid(); s.background.fill.fore_color.rgb=DK
pic(s,M%1,7.6,0,5.733,7.5); rect(s,7.35,0,.25,7.5,RED)
rect(s,.6,.6,3.4,.95,WH,MSO_SHAPE.ROUNDED_RECTANGLE); fit(s,M%2,.7,.65,3.2,.85)
text(s,.6,2.0,6.5,.4,"SISTEMAS DE RADIODIFUSIÓN Y TELEVISIÓN DIGITAL",12,True,C(0xB9,0xD0,0xB9))
text(s,.6,2.45,6.6,2.6,"Radiodifusión sonora digital: DAB/DAB+ frente a IBOC (HD Radio)",32,True,WH)
text(s,.6,4.55,6.5,.8,"Análisis comparativo y estudio de caso para Lima Metropolitana",16,False,C(0xF0,0xC9,0x7A))
rect(s,.6,5.4,1.2,.05,RED)
text(s,.6,5.6,6.6,1.6,["GRUPO 6","Fabrizzio Reyes · Eslin Lopez · Benjamin Zanabria","Miguel San Miguel · Pablo Sánchez","Docente: Jaime Andres Rupaylla Arestegui · Lima, noviembre de 2026"],12.5,False,C(0xDD,0xE8,0xDD))
# 2 Intro
s=slide("¿Por qué es importante la radiodifusión digital?","Introducción")
text(s,.7,1.8,6.3,1.4,"Las tecnologías analógicas AM y FM presentan limitaciones en calidad, eficiencia espectral y transmisión de datos.",18,False,INK)
rect(s,.7,3.3,6.3,1.7,DK); text(s,.95,3.4,5.8,1.5,"La radio digital mejora esto mediante audio comprimido y servicios adicionales.",18,True,WH,anc=MSO_ANCHOR.MIDDLE)
bullets(s,.7,5.3,6.3,1.6,["AM desde 1920, FM desde 1940: tecnología esencialmente analógica.","Perú: ISDB-T en TV desde 2009; la radio digital aún sin estándar."],14)
imgcard(s,M%4,7.4,1.8,5.3,4.9,"Señal analógica frente a señal digital")
# 3 Problemas
s=slide("Principales problemas de la radio analógica","Introducción")
for i,(t,b,c) in enumerate([("Ruido","Sensibilidad al ruido y a las interferencias.",RED),("Pocas emisoras","Limitada cantidad de emisoras disponibles.",SG),("Espectro","Baja eficiencia en el uso del espectro radioeléctrico.",GOLD),("Sin datos","Capacidad limitada para transmitir información adicional.",DK)]):
    x=.7+i*3.05; card(s,x,1.8,2.85,2.3,t,b,c,17,14)
rect(s,.7,4.5,12.1,2.2,DK); text(s,1.0,4.6,3,.4,"PROPUESTA DEL ESTUDIO",12,True,C(0xF0,0xC9,0x7A))
text(s,1.0,5.05,11.5,1.5,"Analizar los sistemas DAB/DAB+ e IBOC y evaluar su aplicación mediante dos escenarios de implementación para Lima Metropolitana.",20,False,WH)
# 4 Justificación
s=slide("Justificación: cuatro perspectivas","Justificación y objetivos")
for i,(t,b,c) in enumerate([("Técnica","Mejorar la calidad y robustez de la transmisión de audio.",DK),("Espectral","Aprovechar mejor las frecuencias ante la saturación de FM en Lima.",SG),("Social","Alertas de emergencia, información de tráfico y contenidos educativos.",RED),("Económica y ambiental","Reducir el consumo energético transmitiendo múltiples programas.",GOLD)]):
    x=.7+(i%2)*6.15; y=1.8+(i//2)*2.55; card(s,x,y,5.95,2.35,t,b,c,19,16)
# 5 Objetivos
s=slide("Objetivo general y objetivos específicos","Justificación y objetivos")
rect(s,.7,1.75,12.1,1.35,DK); text(s,1.0,1.8,11.5,1.25,"Analizar y comparar DAB/DAB+ e IBOC considerando su operación, especificaciones técnicas, cobertura y nivel de servicio, aplicándolo al diseño de una solución para Lima Metropolitana.",17,False,WH,anc=MSO_ANCHOR.MIDDLE)
for i,(t,d) in enumerate([("Principios","OFDM, codificación de canal y de audio"),("Comparación","Frente a analógica, DRM+, satélite e Internet"),("Especificaciones","Bandas, modos, propagación y redes"),("Dimensionamiento","Múltiplex DAB+ y conversión IBOC"),("Servicio","Indicadores QoS, QoE y SLA")]):
    x=.7+i*2.45; rect(s,x,3.45,2.3,3.25,WH,line=LN); rect(s,x+.75,3.65,.8,.8,RED,MSO_SHAPE.OVAL)
    text(s,x+.75,3.75,.8,.6,str(i+1),24,True,WH,PP_ALIGN.CENTER); text(s,x+.1,4.65,2.1,.4,t,16,True,DK,PP_ALIGN.CENTER); text(s,x+.15,5.15,2.0,1.4,d,13,False,INK,PP_ALIGN.CENTER)
# 6 DAB vs IBOC
s=slide("¿Qué son DAB+ e IBOC?","Marco teórico")
for x,col,name,sub,its in [(.7,DK,"DAB+","Digital Audio Broadcasting · Europa",["Utiliza principalmente la Banda III de VHF.","Varias emisoras en un solo múltiplex.","Emplea el códec HE-AAC v2."]),(6.85,RED,"IBOC / HD Radio","In-Band On-Channel · Estados Unidos",["Usa las mismas frecuencias de AM y FM.","Transmite señales analógicas y digitales a la vez.","Emplea el códec propietario HDC."])]:
    rect(s,x,1.75,5.95,4.0,WH,line=LN); rect(s,x,1.75,5.95,1.15,col); text(s,x+.3,1.82,5.3,.6,name,26,True,WH); text(s,x+.3,2.4,5.3,.4,sub,13,False,WH)
    bullets(s,x+.3,3.15,5.4,2.5,its,16,col)
rect(s,.7,6.0,12.1,.8,LSG); text(s,.9,6.0,11.7,.8,"Diferencia principal: DAB+ usa un múltiplex compartido; IBOC digitaliza el canal individual de cada emisora.",15,True,DK,anc=MSO_ANCHOR.MIDDLE)
# 7 Fundamentos
s=slide("Fundamentos tecnológicos","Marco teórico")
for i,(t,its,c) in enumerate([("1 · OFDM",["Divide la información en múltiples subportadoras.","Mejora el comportamiento frente al multitrayecto.","Transmisión eficiente del flujo digital."],DK),("2 · COFDM",["Combina OFDM con codificación de canal.","Entrelazado para distribuir los errores.","Mejora la robustez de la señal recibida."],SG),("3 · Codificación de audio",["DAB+: HE-AAC v2.","IBOC: HDC.","Comprime el audio para varios programas digitales."],RED)]):
    card(s,.7+i*4.1,1.8,3.9,4.8,t,its,c,19,15)
# 8 Espectro OFDM
s=slide("Espectro OFDM: subportadoras ortogonales","Marco teórico")
imgcard(s,M%7,.7,1.8,7.6,4.9,"Cinco subportadoras separadas Δf = 1/Tu")
card(s,8.6,1.8,4.2,2.3,"Ortogonalidad","El pico de cada subportadora coincide con los ceros de las demás.",DK,16,14)
card(s,8.6,4.3,4.2,2.4,"Beneficio","Aprovecha mejor el ancho de banda y resiste el multitrayecto.",SG,16,14)
# 9 Sistema DAB+
s=slide("Sistema DAB+","Marco teórico")
card(s,.7,1.8,6.0,3.2,"Características principales",["COFDM en Banda III de VHF (174–240 MHz).","Bloques de ≈ 1,536 MHz ocupados.","HE-AAC v2; admite redes SFN."],DK,17,14.5)
card(s,.7,5.2,6.0,1.6,"Servicios adicionales","Información del programa, carátulas, tráfico, guía electrónica (EPG) y alertas de emergencia (EWF).",SG,15,13)
pic(s,M%8,7.0,1.8,5.8,5.0)
# 10-11 diagramas
s=slide("Diagrama de bloques del transmisor DAB+","Marco teórico"); imgcard(s,M%9,.7,1.8,12.1,4.7,"Del audio PCM a la antena: codificación, protección, entrelazado, IFFT y RF")
text(s,.7,6.6,12.1,.4,"Cadena: HE-AAC v2 → Reed-Solomon → convolucional → entrelazado → MSC+FIC → π/4-DQPSK → IFFT + guarda → RF.",12,False,MUT)
s=slide("Diagrama de bloques del receptor DAB+","Marco teórico"); imgcard(s,M%10,.7,1.8,12.1,4.7,"Sincronización, FFT, desentrelazado, Viterbi y decodificación de audio y datos")
text(s,.7,6.6,12.1,.4,"El receptor realiza el proceso inverso y entrega audio, datos (PAD) y DLS / SlideShow.",12,False,MUT)
# 12 IBOC
s=slide("Sistema IBOC (HD Radio)","Marco teórico")
card(s,.7,1.8,5.7,2.5,"Características",["Señales analógica y digital en el mismo canal.","Bandas AM y FM; OFDM con QPSK en FM.","Programas digitales adicionales con HDC."],RED,17,14)
card(s,.7,4.5,5.7,2.3,"Ventaja principal","Modernizar una emisora existente sin necesitar una nueva frecuencia.",SG,17,14.5)
text(s,6.75,1.8,6,.4,"MODOS DE FUNCIONAMIENTO EN FM",12,True,RED)
for i,(t,d) in enumerate([("Híbrido","Mantiene la FM analógica y agrega portadoras digitales."),("Híbrido extendido","Aumenta la capacidad digital."),("Totalmente digital","Elimina la señal analógica y usa todo el canal.")]):
    y=2.2+i*1.0; rect(s,6.75,y,6.05,.9,WH,line=LN); rect(s,6.75,y,.07,.9,[SG,GOLD,RED][i]); text(s,7.0,y+.04,5.7,.3,t,14,True,DK); text(s,7.0,y+.38,5.7,.5,d,12.5,False,INK)
pic(s,M%11,6.75,5.3,6.05,1.5)
# 13 Espectro IBOC
s=slide("Espectro de la señal IBOC FM híbrida","Marco teórico")
imgcard(s,M%12,.7,1.8,7.6,4.9,"Bandas laterales digitales a ambos lados de la portadora FM")
card(s,8.6,1.8,4.2,2.3,"Híbrido (MP1)","Señal FM analógica en el centro y bandas digitales primarias a ±.",RED,16,14)
card(s,8.6,4.3,4.2,2.4,"Dato clave","Cada banda lateral ocupa ≈ 69 kHz; el canal total es el de la emisora.",SG,16,14)
# 14 Comparación
s=slide("Comparación entre DAB+ e IBOC","Análisis comparativo")
rows=[["Característica","DAB+","IBOC"],["Origen","Europa","Estados Unidos"],["Frecuencia","Banda III","AM y FM"],["Modulación","COFDM","COFDM"],["Códec","HE-AAC v2","HDC"],["Capacidad","12–20 programas aprox.","1–4 programas aprox."],["Espectro","Requiere bloques nuevos","Reutiliza el canal existente"],["Red SFN","Sí","No nativa"],["Implementación","Múltiplex compartido","Por emisora"]]
table(s,.7,1.75,8.2,rows,[2.4,2.9,2.9],.56,13.5)
rect(s,9.2,1.75,3.6,3.0,DK); text(s,9.45,1.85,3.2,.4,"ANÁLISIS",12,True,C(0xF0,0xC9,0x7A)); text(s,9.45,2.3,3.2,2.4,"DAB+ destaca por su eficiencia espectral y capacidad; IBOC facilita la transición de las emisoras analógicas.",15,False,WH)
fit(s,M%13,9.3,4.9,3.4,1.9)
# 15 Caso
s=slide("Estudio de caso: Lima Metropolitana","Estudio de caso")
card(s,.7,1.8,4.1,2.2,"Escenario A","Red DAB+ en Banda III, bloque 12C.",DK,18,15)
card(s,.7,4.2,4.1,2.2,"Escenario B","Conversión de una emisora FM existente a IBOC híbrido.",RED,18,15)
card(s,5.0,1.8,4.0,4.6,"Situación identificada",["Banda FM 88–108 MHz prácticamente saturada.","Alta demanda de información y entretenimiento.","Se requiere mejorar la eficiencia del espectro.","Medio para alertas ante emergencias."],SG,17,14)
imgcard(s,M%15,9.2,1.8,3.6,4.6,"Lima Metropolitana y Callao")
# 16 Escenario A
s=slide("Escenario A: implementación DAB+ en Lima","Estudio de caso")
for i,(b,sm,c) in enumerate([("12C","bloque · 227,360 MHz",DK),("Modo I","ancho ocupado 1,536 MHz",SG),("EEP-3A","perfil de protección",GOLD),("10 kW","PRA desde Cerro San Cristóbal",RED)]):
    stat(s,.7+(i%2)*3.15,1.8+(i//2)*1.6,3.0,b,sm,c)
card(s,.7,5.1,6.15,1.7,"Capacidad del múltiplex","14 programas de audio + 2 servicios de datos: 654 de 864 CU (75,7 %). Quedan 210 CU libres.",DK,16,13.5)
pic(s,M%16,7.1,1.8,5.7,5.0)
# 17 Ocupación
s=slide("Ocupación del múltiplex DAB+","Estudio de caso")
sv=[("Radio Nacional",54),("Noticias 1",48),("Noticias 2",48),("Música pop 1",54),("Música pop 2",48),("Tropical / cumbia",48),("Criolla y folclore",48),("Clásica / cultural",72),("Deportes 1",36),("Deportes 2",36),("Rock / alternativa",48),("Radio educativa",36),("Radio en quechua",30),("Religiosa",30),("Alerta EWS",6),("TPEG + EPG",12)]
chart(s,.7,1.6,8.0,5.4,[a for a,_ in sv],[("CU",[b for _,b in sv])],[SG],horiz=True,fmt='0',legend=False,maxv=85,gap=35,lsize=11)
stat(s,9.1,1.8,3.7,"654 / 864","unidades de capacidad usadas",DK); stat(s,9.1,3.35,3.7,"75,7 %","ocupación del múltiplex",RED); stat(s,9.1,4.9,3.7,"210 CU","reserva: 3–4 programas más",GOLD)
# 18 Cobertura
s=slide("Cobertura desde el Cerro San Cristóbal","Estudio de caso")
chart(s,.7,1.6,7.0,5.3,["Móvil urbano","Portátil exterior","Portátil interior"],[("Radio de cobertura (km)",(30.2,41.1,14.8))],[SG],legend=False,maxv=50,point_cols=[SG,SG,RED],title="Radio de cobertura (km)")
card(s,8.0,1.8,4.8,2.2,"Limitación","En interiores solo llega a 14,8 km; el cono norte y sur están a 15–30 km.",RED,16,14)
card(s,8.0,4.2,4.8,2.5,"Solución: SFN de 4 sitios","Un principal de 2,5 kW y tres de relleno de 1 kW, sincronizados por GPS.",DK,16,14)
# 19 SFN
s=slide("Red de frecuencia única (SFN) propuesta","Estudio de caso")
imgcard(s,M%19,.7,1.8,6.0,4.9,"Sitios y radios de cobertura portátil en interiores")
card(s,7.0,1.8,5.8,3.0,"Sitios propuestos",["Cerro San Cristóbal (principal)","Morro Solar (Chorrillos)","Carabayllo (cono norte)","Ate–Huachipa (cono este)"],DK,17,15)
card(s,7.0,5.0,5.8,1.8,"Ventaja de la SFN","Todos emiten el mismo múltiplex en la misma frecuencia; distancias ≤ 34 km frente a 73,7 km de guarda.",SG,16,13.5)
# 20 Escenario B
s=slide("Escenario B: conversión IBOC híbrida","Estudio de caso")
card(s,.7,1.8,4.0,2.6,"Emisora hipotética",["98,1 MHz · 30 kW PRA","Cerro San Cristóbal","IBOC híbrido MP1"],RED,17,14.5)
card(s,.7,4.6,4.0,2.2,"Programas",["HD1: 64 kbit/s","HD2: 32 kbit/s"],SG,17,14.5)
chart(s,5.0,1.6,7.8,5.3,["FM analógica","−20 dBc","−14 dBc","−10 dBc"],[("Móvil urbano (km)",(28.4,22.5,35.8,48.7)),("Portátil interior (km)",(0,8.7,13.9,18.9))],[DK,RED],fmt='0.0;;',maxv=58,title="Cobertura según la potencia digital")
# 21 Comparación cobertura y consumo
s=slide("Cobertura IBOC y consumo energético","Resultados")
chart(s,.7,1.6,6.0,4.4,["FM estéreo","−20 dBc","−14 dBc","−10 dBc"],[("km",(28.4,22.5,35.8,48.7))],[SG],fmt='0.0',legend=False,maxv=58,point_cols=[MUT,RED,SG,SG],title="Cobertura móvil urbana (km)")
chart(s,6.9,1.6,5.9,4.4,["14 emisoras FM","Red DAB+ SFN"],[("kW",(229.3,16.7))],[RED],fmt='0.0',legend=False,maxv=280,point_cols=[RED,SG],title="Consumo eléctrico total (kW)")
rect(s,.7,6.15,6.0,.75,LSG); text(s,.9,6.15,5.7,.75,"−14 dBc es el mínimo para superar a la analógica.",14,True,DK,anc=MSO_ANCHOR.MIDDLE)
rect(s,6.9,6.15,5.9,.75,DK); text(s,7.1,6.15,5.5,.75,"DAB+ consume ≈ 13,8 veces menos energía.",14,True,WH,anc=MSO_ANCHOR.MIDDLE)
# 22 Consumo detalle
s=slide("DAB+ consume ≈ 14 veces menos por programa","Resultados")
chart(s,.7,1.6,6.0,5.3,["FM analógica","DAB+ (SFN)"],[("Consumo por programa (kW)",(16.38,1.19))],[RED],fmt='0.00',legend=False,maxv=20,point_cols=[RED,SG],title="Consumo por programa (kW)")
stat(s,7.1,1.8,2.75,"13,8×","relación FM / DAB+",RED); stat(s,10.05,1.8,2.75,"1 862 MWh","ahorro anual",DK)
table(s,7.1,3.5,5.7,[["","FM","DAB+"],["Programas","14","14"],["Eficiencia global","65 %","33 %"],["Energía anual","2 008 MWh","146 MWh"]],[2.5,1.6,1.6],.6,14,True)
text(s,7.1,6.1,5.7,.8,"Aun con amplificadores COFDM menos eficientes y tres sitios de relleno.",12.5,False,MUT,it=True)
# 23 Equipamiento
s=slide("Equipamiento y calidad del servicio","Equipamiento")
card(s,.7,1.8,4.1,2.9,"Para DAB+",["GatesAir Maxiva VAXT-HE","AVT MAGIC DABMUX plus","PrecisionWave Signal Analyzer","Televés MOSAIQ6"],DK,16,13)
card(s,.7,4.9,4.1,1.9,"Para IBOC",["Nautel GV2 · GatesAir Flexiva FMXi 4g","Receptor de monitoreo HD Radio"],RED,16,12.5)
pic(s,M%24,5.0,1.8,3.4,5.0)
stat(s,8.6,1.8,4.2,"99,988 %","disponibilidad calculada de la red DAB+",SG)
card(s,8.6,3.35,4.2,1.7,"QoS","Intensidad de campo, C/N, MER, BER y disponibilidad.",DK,15,12.5)
card(s,8.6,5.15,4.2,1.65,"QoE","Calidad de audio, tiempo de sintonía, interrupciones.",RED,15,12.5)
# 24 Conclusiones
s=slide("Conclusiones","Cierre")
cs=[("COFDM","DAB+ e IBOC modernizan la radio con COFDM.",DK),("Eficiencia","DAB+: 14 programas y 2 servicios de datos.",SG),("SFN","Lima requiere 4 sitios para cobertura interior.",GOLD),("IBOC","Digitaliza FM sin frecuencia nueva, con capacidad limitada.",RED),("Energía","DAB+ consume ≈ 13,8 veces menos.",DK),("Decisión","La matriz sitúa a DAB+ como la más conveniente (7,60 frente a 6,90).",SG)]
for i,(t,b,c) in enumerate(cs): card(s,.7+(i%3)*4.1,1.8+(i//3)*2.55,3.9,2.35,t,b,c,18,14)
# 25 Cierre
N[0]+=1; s=prs.slides.add_slide(BL); s.background.fill.solid(); s.background.fill.fore_color.rgb=DK
pic(s,M%25,9.6,0,3.733,7.5); rect(s,9.35,0,.25,7.5,RED)
text(s,.8,1.5,8,.4,"PERSPECTIVAS",12,True,C(0xF0,0xC9,0x7A)); text(s,.8,2.0,8.3,1.9,"Planificar la radio digital junto con el apagado de la TV analógica",32,True,WH)
for i,t in enumerate(["Radio híbrida","5G Broadcast","xHE-AAC","Alertas"]):
    rect(s,.8+(i%2)*4.1,4.2+(i//2)*.95,3.9,.8,C(0x2C,0x52,0x42)); text(s,1.0+(i%2)*4.1,4.2+(i//2)*.95,3.6,.8,t,16,True,WH,anc=MSO_ANCHOR.MIDDLE)
text(s,.8,6.3,8,.6,"¡Gracias! · Grupo 6",22,True,C(0xF0,0xC9,0x7A))
prs.save("/home/user/mi-proyecto/presentacion/Informe_y_estudio_de_caso_mejorado.pptx")
