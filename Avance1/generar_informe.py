# -*- coding: utf-8 -*-
"""Genera el informe del Avance 1 en formato APA 7 (Word)."""
import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "Avance1_Fogon_Andino.docx")

FUENTE = "Times New Roman"


# ---------------------------------------------------------------
# Utilidades de formato APA 7
# ---------------------------------------------------------------
def nuevo_documento():
    doc = Document()
    sec = doc.sections[0]
    # Tamano carta (21.59 x 27.94 cm) y margenes 2.54 cm
    sec.page_width = Cm(21.59)
    sec.page_height = Cm(27.94)
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)
    # Estilo Normal: Times New Roman 12, interlineado doble, alineado izquierda
    estilo = doc.styles["Normal"]
    estilo.font.name = FUENTE
    estilo.font.size = Pt(12)
    estilo.element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
    pf = estilo.paragraph_format
    pf.line_spacing = 2.0
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    # Numero de pagina en la esquina superior derecha
    agregar_numero_pagina(sec)
    return doc


def agregar_numero_pagina(sec):
    header = sec.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run()
    run.font.name = FUENTE
    run.font.size = Pt(12)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)


def parrafo(doc, texto, sangria=True, alineacion=WD_ALIGN_PARAGRAPH.LEFT,
            interlineado=2.0):
    p = doc.add_paragraph()
    p.alignment = alineacion
    p.paragraph_format.line_spacing = interlineado
    if sangria:
        p.paragraph_format.first_line_indent = Cm(1.27)
    run = p.add_run(texto)
    run.font.name = FUENTE
    run.font.size = Pt(12)
    return p


def titulo1(doc, texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(texto)
    run.bold = True
    run.font.name = FUENTE
    run.font.size = Pt(12)
    return p


def titulo2(doc, texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.keep_with_next = True
    run = p.add_run(texto)
    run.bold = True
    run.font.name = FUENTE
    run.font.size = Pt(12)
    return p


def titulo3(doc, texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.keep_with_next = True
    run = p.add_run(texto)
    run.bold = True
    run.italic = True
    run.font.name = FUENTE
    run.font.size = Pt(12)
    return p


def figura(doc, nro, titulo, archivo, ancho_cm=14.5):
    # Numero de figura en negrita (alineado a la izquierda, sin sangria)
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.line_spacing = 2.0
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.keep_with_next = True
    r = p1.add_run(f"Figura {nro}")
    r.bold = True
    r.font.name = FUENTE
    r.font.size = Pt(12)
    # Titulo en cursiva, una linea debajo
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p2.paragraph_format.line_spacing = 2.0
    p2.paragraph_format.keep_with_next = True
    r2 = p2.add_run(titulo)
    r2.italic = True
    r2.font.name = FUENTE
    r2.font.size = Pt(12)
    # Imagen centrada
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.line_spacing = 1.0
    p3.paragraph_format.space_after = Pt(0)
    run3 = p3.add_run()
    run3.add_picture(os.path.join(BASE, archivo), width=Cm(ancho_cm))


def formato_apa_tabla(tabla):
    """Bordes APA: solo lineas horizontales (arriba, debajo de encabezados,
    abajo del cuerpo). Sin bordes verticales."""
    tbl = tabla._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for nombre in ("top", "bottom", "left", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{nombre}")
        if nombre in ("top", "bottom"):
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "8")
            el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "none")
        borders.append(el)
    tblPr.append(borders)


def tabla_apa(doc, nro, titulo, encabezados, filas, ancho_col=None,
              nota=None):
    # Numero de tabla (negrita)
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.line_spacing = 2.0
    p1.paragraph_format.keep_with_next = True
    r = p1.add_run(f"Tabla {nro}")
    r.bold = True
    r.font.name = FUENTE
    r.font.size = Pt(12)
    # Titulo en cursiva
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p2.paragraph_format.line_spacing = 2.0
    p2.paragraph_format.keep_with_next = True
    r2 = p2.add_run(titulo)
    r2.italic = True
    r2.font.name = FUENTE
    r2.font.size = Pt(12)
    # Tabla
    t = doc.add_table(rows=1 + len(filas), cols=len(encabezados))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    formato_apa_tabla(t)
    # Encabezados
    for j, enc in enumerate(encabezados):
        celda = t.rows[0].cells[j]
        celda.paragraphs[0].text = ""
        p = celda.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(enc)
        run.bold = False
        run.font.name = FUENTE
        run.font.size = Pt(10)
    # Cuerpo
    for i, fila in enumerate(filas):
        for j, valor in enumerate(fila):
            celda = t.rows[i + 1].cells[j]
            p = celda.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(valor))
            run.font.name = FUENTE
            run.font.size = Pt(10)
    if ancho_col:
        for j, w in enumerate(ancho_col):
            for fila in t.rows:
                fila.cells[j].width = Cm(w)
    if nota:
        pn = doc.add_paragraph()
        pn.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pn.paragraph_format.line_spacing = 1.0
        pn.paragraph_format.space_before = Pt(6)
        rn = pn.add_run(nota)
        rn.font.name = FUENTE
        rn.font.size = Pt(10)
        rn.italic = True
    return t


# ===============================================================
# CONSTRUCCION DEL DOCUMENTO
# ===============================================================
doc = nuevo_documento()

# ---------------------------------------------------------------
# PORTADA (estudiante)
# ---------------------------------------------------------------
for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("Modelado de Requerimientos del Negocio de "
              "Fogón Andino S.A.C.: Avance 1")
r.bold = True
r.font.name = FUENTE
r.font.size = Pt(12)

doc.add_paragraph()  # linea en blanco extra

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("[Nombre completo del Estudiante 1], "
              "[Nombre completo del Estudiante 2], "
              "[Nombre completo del Estudiante 3] y "
              "[Nombre completo del Estudiante 4]")
r.font.name = FUENTE
r.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("Universidad Tecnológica del Perú")
r.font.name = FUENTE
r.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("Curso: Diseño e Implementación de Arquitectura Empresarial")
r.font.name = FUENTE
r.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("Docente: Ing. Jair Darnley Vásquez Aguirre")
r.font.name = FUENTE
r.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 2.0
r = p.add_run("Setiembre de 2026")
r.font.name = FUENTE
r.font.size = Pt(12)

doc.add_page_break()

# ---------------------------------------------------------------
# RESUMEN
# ---------------------------------------------------------------
titulo1(doc, "Resumen")
parrafo(doc,
        "El presente informe documenta el primer avance del proyecto final "
        "del curso Diseño e Implementación de Arquitectura Empresarial. "
        "El equipo seleccionó la empresa ficticia Fogón Andino S.A.C., un "
        "restaurante de comida peruana con servicio en local y delivery, "
        "sobre la cual se modelaron los requerimientos del negocio. Se "
        "aplicaron principios de gestión de proyectos de software, "
        "enfoques de modelado del negocio (BPM y RUP) e ingeniería de "
        "requerimientos para producir documentación estructurada que "
        "servirá de insumo a la fase de arquitectura empresarial basada "
        "en TOGAF. Se identificaron los actores y casos de uso del "
        "negocio, se construyó el modelo de dominio y se elaboraron dos "
        "diagramas de actividades correspondientes a los procesos de "
        "atención en el local y de pedidos en línea con delivery. Asimismo, "
        "se elaboró la especificación de requerimientos de software "
        "(SRS), que incluye el diagrama de contexto, la clasificación de "
        "requerimientos funcionales y no funcionales según el nivel de "
        "madurez CMMI y tres especificaciones de casos de uso. El equipo "
        "ubica la gestión de sus requerimientos en el nivel 2 del modelo "
        "CMMI (REQM), con prácticas iniciales del nivel 3 (RD).",
        sangria=False)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 2.0
p.paragraph_format.first_line_indent = Cm(1.27)
r = p.add_run("Palabras clave: ")
r.italic = True
r.font.name = FUENTE
r.font.size = Pt(12)
r2 = p.add_run("modelado del negocio, ingeniería de requerimientos, "
               "casos de uso, CMMI, diagrama de actividades")
r2.font.name = FUENTE
r2.font.size = Pt(12)

doc.add_page_break()

# ---------------------------------------------------------------
# TABLA DE CONTENIDOS
# ---------------------------------------------------------------
titulo1(doc, "Tabla de Contenidos")
contenido = [
    ("1. Introducción", 0),
    ("1.1. Presentación de la Empresa", 1),
    ("1.2. Actividad Principal y Procesos del Negocio", 1),
    ("1.3. Objetivos del Avance", 1),
    ("1.4. Alcance y Limitaciones", 1),
    ("2. Modelado del Negocio", 0),
    ("2.1. Actores y Casos de Uso del Negocio", 1),
    ("2.2. Modelo de Dominio", 1),
    ("2.3. Diagramas de Actividades", 1),
    ("3. Especificación de Requerimientos de Software", 0),
    ("3.1. Introducción y Descripción General", 1),
    ("3.2. Diagrama de Contexto", 1),
    ("3.3. Nivel de Madurez CMMI del Equipo", 1),
    ("3.4. Requerimientos Funcionales y No Funcionales", 1),
    ("3.5. Especificación de Casos de Uso", 1),
    ("4. Conclusiones", 0),
    ("Referencias", 0),
]
for texto, nivel in contenido:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    if nivel == 1:
        p.paragraph_format.left_indent = Cm(1.27)
    run = p.add_run(texto)
    run.font.name = FUENTE
    run.font.size = Pt(12)

doc.add_page_break()

# ===============================================================
# 1. INTRODUCCION
# ===============================================================
titulo1(doc, "1. Introducción")

titulo2(doc, "1.1. Presentación de la Empresa")
parrafo(doc,
        "Fogón Andino S.A.C. es una empresa ficticia del rubro gastronómico "
        "dedicada a la preparación y comercialización de comida peruana "
        "tradicional. Cuenta con un local principal en el distrito de "
        "Miraflores, Lima, con capacidad para 80 comensales distribuidos en "
        "20 mesas, y atiende actualmente una demanda diaria aproximada de "
        "350 clientes entre servicio en el local y pedidos por delivery. La "
        "empresa emplea a 18 personas, entre las que se encuentran mozos, "
        "cocineros, cajeros, un administrador y repartidores externos "
        "contratados bajo la modalidad de reparto.")
parrafo(doc,
        "La empresa se encuentra en un proceso de transformación digital. "
        "En la actualidad, la mayoría de sus operaciones se realizan de "
        "manera manual o con herramientas de ofimática que no están "
        "integradas, lo que genera demoras, errores de registro y pérdida "
        "de información. Por ello, la dirección ha decidido emprender el "
        "desarrollo de un sistema de gestión de pedidos que permita "
        "integrar la atención en el local, los pedidos en línea y el "
        "servicio de delivery, y que posteriormente sirva como base para "
        "la definición de la arquitectura empresarial de la organización.")

titulo2(doc, "1.2. Actividad Principal y Procesos del Negocio")
parrafo(doc,
        "La actividad principal de Fogón Andino S.A.C. consiste en ofrecer "
        "platos de comida peruana preparados al momento, tanto en sus "
        "instalaciones como a domicilio. Para ello, la organización ejecuta "
        "de manera cotidiana un conjunto de procesos de negocio, entre los "
        "que destacan los siguientes: (a) atención de pedidos en el local, "
        "que abarca desde la recepción del comensal hasta el cobro y la "
        "liberación de la mesa; (b) gestión de pedidos en línea con "
        "delivery, que comprende la recepción del pedido a través de una "
        "tienda virtual, la confirmación de stock, el pago electrónico, la "
        "preparación, el empaquetado y la entrega; (c) gestión de la carta "
        "y los insumos, que incluye la actualización de los platos "
        "disponibles y el abastecimiento por parte de los proveedores; y "
        "(d) gestión de reservas y cobros, que agrupa la reserva de mesas "
        "y la emisión de comprobantes de pago.")
parrafo(doc,
        "De acuerdo con Sommerville (2011), los procesos de negocio "
        "describen lo que hace una organización y constituyen el punto de "
        "partida para identificar las necesidades que el software debe "
        "satisfacer. Por esta razón, en el presente avance se han modelado "
        "los dos procesos más relevantes para la estrategia de "
        "transformación digital de la empresa: la atención de pedidos en "
        "el local y la gestión de pedidos en línea con delivery.")

titulo2(doc, "1.3. Objetivos del Avance")
parrafo(doc,
        "El objetivo general del presente avance es modelar los "
        "requerimientos del negocio de Fogón Andino S.A.C., aplicando "
        "principios de gestión de proyectos de software, modelado del "
        "negocio e ingeniería de requerimientos, para producir una "
        "documentación estructurada que sirva de insumo a la fase de "
        "arquitectura empresarial (TOGAF) que se desarrollará en la "
        "siguiente unidad. Para la planificación y el control del "
        "proyecto se han considerado las buenas prácticas de dirección "
        "de proyectos descritas por el Project Management Institute "
        "(2021). Como objetivos específicos se plantean: "
        "identificar los actores y casos de uso del negocio; construir el "
        "modelo de dominio; elaborar dos diagramas de actividades de "
        "procesos relevantes; y elaborar la especificación de "
        "requerimientos de software, incluyendo la clasificación de "
        "requerimientos y tres especificaciones de casos de uso.")

titulo2(doc, "1.4. Alcance y Limitaciones")
parrafo(doc,
        "El alcance del avance se limita al modelado del negocio y a la "
        "especificación de requerimientos funcionales y no funcionales del "
        "sistema de gestión de pedidos. Quedan fuera del alcance el diseño "
        "de la arquitectura técnica, la selección de tecnologías, la "
        "implementación del software y la definición de la arquitectura "
        "empresarial con TOGAF, los cuales se abordarán en entregables "
        "posteriores. Como limitación principal, se considera que la "
        "empresa es de carácter ficticio, por lo que la información sobre "
        "volúmenes de venta, presupuestos y tiempos se ha estimado a "
        "partir de valores razonables para un restaurante de características "
        "similares. La presente documentación se ha estructurado siguiendo "
        "las normas de publicación de la American Psychological Association "
        "(2020).")

doc.add_page_break()

# ===============================================================
# 2. MODELADO DEL NEGOCIO
# ===============================================================
titulo1(doc, "2. Modelado del Negocio")
parrafo(doc,
        "El modelado del negocio es una disciplina que permite representar "
        "de manera estructurada cómo funciona una organización, cómo "
        "genera valor, qué actividades realiza, quiénes participan y qué "
        "información utiliza (Jacobson et al., 2000). En el presente "
        "apartado se modela el negocio de Fogón Andino S.A.C. desde la "
        "perspectiva del proceso unificado de desarrollo (RUP), "
        "considerando los actores y casos de uso del negocio, el modelo de "
        "dominio y los diagramas de actividades de sus procesos más "
        "relevantes.")

titulo2(doc, "2.1. Actores y Casos de Uso del Negocio")
parrafo(doc,
        "Los actores del negocio son las personas, organizaciones o "
        "sistemas externos que interactúan con los procesos de la "
        "organización y obtienen algún valor de ellos. Para Fogón Andino "
        "S.A.C. se han identificado los actores que se muestran en la "
        "Tabla 1.")
tabla_apa(doc, 1, "Actores del negocio de Fogón Andino S.A.C.",
          ["Actor", "Tipo", "Descripción", "Procesos en los que participa"],
          [["Cliente", "Externo",
            "Persona que consume los platos en el local o solicita delivery.",
            "Pedido en local, pedido en línea, pago"],
           ["Mozo", "Interno",
            "Personal de sala que atiende al comensal y toma el pedido.",
            "Atención en el local"],
           ["Chef / Cocinero", "Interno",
            "Responsable de la preparación de los platos.",
            "Preparación de comida, abastecimiento"],
           ["Cajero", "Interno",
            "Encargado del cobro y la emisión de comprobantes.",
            "Cobro y facturación"],
           ["Repartidor", "Externo",
            "Encargado de entregar los pedidos a domicilio.",
            "Delivery"],
           ["Proveedor", "Externo",
            "Empresa que abastece de insumos a la cocina.",
            "Abastecimiento"],
           ["Administrador", "Interno",
            "Encargado de la gestión de la carta, reportes y configuración.",
            "Gestión de la carta, reportes"]],
          ancho_col=[2.6, 1.7, 6.0, 4.0],
          nota="Nota. Elaboración propia.")
parrafo(doc,
        "Un caso de uso del negocio representa un proceso del negocio "
        "observado desde la perspectiva de un actor que recibe un "
        "resultado de valor (Jacobson et al., 2000). En la Tabla 2 se "
        "presentan los casos de uso del negocio identizados, y en la "
        "Figura 1 el diagrama correspondiente.")
tabla_apa(doc, 2, "Casos de uso del negocio",
          ["ID", "Caso de uso del negocio", "Actor(es)", "Resultado de valor"],
          [["CU-N1", "Realizar pedido", "Cliente, Mozo",
            "Pedido registrado y enviado a cocina"],
           ["CU-N2", "Preparar comida", "Chef",
            "Platos listos para servir o entregar"],
           ["CU-N3", "Cobrar pedido", "Cajero, Cliente",
            "Comprobante emitido y mesa liberada"],
           ["CU-N4", "Entregar pedido a domicilio", "Repartidor, Cliente",
            "Pedido entregado en la dirección del cliente"],
           ["CU-N5", "Abastecer insumos", "Proveedor, Chef",
            "Stock de insumos reabastecido"]],
          ancho_col=[1.5, 4.8, 3.6, 4.4],
          nota="Nota. Elaboración propia.")
parrafo(doc,
        "El diagrama de la Figura 1 representa los casos de uso del "
        "negocio y las relaciones con los actores que participan en cada "
        "uno. Se trata de una vista organizacional, no de software, por lo "
        "que describe lo que hace el negocio y no las funcionalidades "
        "concretas del sistema futuro.")
figura(doc, 1, "Diagrama de casos de uso del negocio de Fogón Andino S.A.C.",
       "fig1_casos_uso_negocio.png", ancho_cm=15.5)

doc.add_page_break()

titulo2(doc, "2.2. Modelo de Dominio")
parrafo(doc,
        "El modelo de dominio es una representación conceptual de los "
        "elementos más importantes de un negocio y de las relaciones que "
        "existen entre ellos. Su propósito es identificar los conceptos "
        "fundamentales del problema, comprender cómo se relacionan y "
        "establecer un lenguaje común entre usuarios, analistas y "
        "desarrolladores (Pressman, 2014). Para Fogón Andino S.A.C. se "
        "han identificado los conceptos de Cliente, Pedido, "
        "DetallePedido, Plato, Mesa, Reserva, Empleado, Repartidor y "
        "Boleta, cuyas relaciones se muestran en la Figura 2.")
parrafo(doc,
        "Entre las relaciones más importantes se encuentran las "
        "siguientes: un cliente puede realizar uno o varios pedidos; cada "
        "pedido contiene uno o varios detalles de pedido; cada detalle "
        "hace referencia a un plato de la carta; todo pedido genera como "
        "máximo una boleta; los pedidos en el local se asignan a una "
        "mesa; las reservas se asocian a un cliente y a una mesa; y los "
        "empleados atienden los pedidos, mientras que los repartidores "
        "tienen a su cargo la entrega de los pedidos a domicilio.")
figura(doc, 2, "Modelo de dominio de Fogón Andino S.A.C.",
       "fig2_modelo_dominio.png", ancho_cm=16.5)

doc.add_page_break()

titulo2(doc, "2.3. Diagramas de Actividades")
parrafo(doc,
        "El diagrama de actividades es uno de los diagramas de "
        "comportamiento de UML que permite representar el flujo de "
        "actividades que se ejecutan para completar un proceso, "
        "mostrando el orden en que ocurren las acciones, las decisiones "
        "que pueden presentarse y las actividades que pueden realizarse "
        "de manera paralela (Booch et al., 2006). A continuación se "
        "modelan los dos procesos de negocio más relevantes de Fogón "
        "Andino S.A.C.")
titulo3(doc, "2.3.1. Proceso de atención de pedido en el local")
parrafo(doc,
        "La Figura 3 representa el proceso que se ejecuta cuando un "
        "comensal llega al restaurante. El flujo inicia con la recepción "
        "del cliente y la asignación de una mesa; a continuación, el mozo "
        "entrega la carta y toma el pedido. Existe un nodo de decisión "
        "que verifica si el pedido está completo; en caso de que el "
        "cliente desee agregar algo, el flujo regresa a la actividad de "
        "toma del pedido. Una vez confirmado, el pedido se envía a "
        "cocina, se preparan los platos, se sirven en la mesa y, al "
        "finalizar la comida, se emite la boleta, se realiza el cobro y "
        "se libera la mesa.")
figura(doc, 3, "Diagrama de actividades del proceso de atención de pedido "
               "en el local",
       "fig3_actividades_local.png", ancho_cm=12.0)

doc.add_page_break()

titulo3(doc, "2.3.2. Proceso de pedido en línea con delivery")
parrafo(doc,
        "La Figura 4 modela el proceso de un pedido realizado a través de "
        "la tienda virtual. El flujo se inicia cuando el cliente ingresa "
        "a la aplicación y consulta la carta; selecciona los platos y "
        "confirma el pedido. El sistema verifica la disponibilidad de "
        "stock; si algún plato no está disponible, se notifica al cliente "
        "y el flujo regresa a la consulta de la carta. Cuando hay stock "
        "suficiente, se registra el pedido y se procesa el pago en línea; "
        "si el pago no es aprobado, el pedido no se confirma. Finalmente, "
        "el pedido se envía a cocina, se prepara y empaqueta, y se asigna "
        "un repartidor para su entrega a domicilio.")
figura(doc, 4, "Diagrama de actividades del proceso de pedido en línea "
               "con delivery",
       "fig4_actividades_online.png", ancho_cm=12.0)

doc.add_page_break()

# ===============================================================
# 3. ESPECIFICACION DE REQUERIMIENTOS DE SOFTWARE
# ===============================================================
titulo1(doc, "3. Especificación de Requerimientos de Software")
titulo2(doc, "3.1. Introducción y Descripción General")
parrafo(doc,
        "El presente documento de especificación de requerimientos de "
        "software (SRS, por sus siglas en inglés) describe las "
        "necesidades, capacidades, restricciones y características que "
        "debe cumplir el sistema de gestión de pedidos de Fogón Andino "
        "S.A.C. Siguiendo la definición de la ISO/IEC/IEEE 29148 (2018), "
        "la SRS es una colección estructurada de los requisitos "
        "esenciales del software, incluyendo funciones, rendimiento, "
        "restricciones de diseño, atributos e interfaces externas.")
parrafo(doc,
        "El propósito del sistema es integrar y automatizar los procesos "
        "de atención en el local, pedidos en línea con delivery, cobros, "
        "gestión de la carta y generación de reportes, con el fin de "
        "reducir los tiempos de atención, disminuir los errores de "
        "registro manuales y mejorar la experiencia del cliente. Los "
        "usuarios del sistema serán los mozos, el chef, el cajero, el "
        "administrador del restaurante, los repartidores y los clientes "
        "finales que utilicen la tienda virtual.")

titulo2(doc, "3.2. Diagrama de Contexto")
parrafo(doc,
        "El diagrama de contexto es una vista de alto nivel que permite "
        "delimitar el sistema y sus interacciones con los actores "
        "externos, mostrando el flujo de información entre el sistema y "
        "su entorno. En la Figura 5 se observa que el sistema central se "
        "comunica con seis tipos de usuarios (cliente, mozo, chef, "
        "cajero, repartidor y administrador) y con dos sistemas externos: "
        "la pasarela de pago, encargada de validar y registrar los pagos "
        "electrónicos, y el portal de proveedores, que recibe las órdenes "
        "de compra de insumos.")
figura(doc, 5, "Diagrama de contexto del sistema de gestión de pedidos",
       "fig5_diagrama_contexto.png", ancho_cm=15.5)

doc.add_page_break()

titulo2(doc, "3.3. Nivel de Madurez CMMI del Equipo")
parrafo(doc,
        "CMMI (Capability Maturity Model Integration) es un modelo de "
        "referencia que proporciona buenas prácticas para que las "
        "organizaciones mejoren sus procesos, capacidades y desempeño "
        "(CMMI Institute, 2023). En el área de requerimientos, CMMI "
        "distingue dos niveles de capacidad: la gestión de requerimientos "
        "(REQM), propia del nivel 2, y el desarrollo de requerimientos "
        "(RD), propio del nivel 3.")
parrafo(doc,
        "El equipo ubica la gestión de requerimientos del presente "
        "proyecto en el nivel 2 (REQM), ya que los requerimientos "
        "identificados están documentados, clasificados y controlados "
        "mediante una matriz de trazabilidad, y se ha definido un "
        "procedimiento para gestionar los cambios: cualquier modificación "
        "a un requerimiento debe ser registrada, analizada y aprobada por "
        "el equipo antes de su incorporación. Asimismo, se aplican "
        "algunas prácticas iniciales del nivel 3 (RD), como la obtención "
        "de requerimientos a partir de las necesidades de los "
        "stakeholders y su descomposición en requisitos del sistema y de "
        "componentes, tal como se aprecia en la Tabla 3, donde cada "
        "necesidad del negocio se traza hacia un requerimiento "
        "funcional, un caso de uso y un componente del sistema.")
tabla_apa(doc, 3, "Matriz de trazabilidad de requerimientos",
          ["Necesidad del negocio", "RF", "Caso de uso", "Componente"],
          [["Reducir el tiempo de toma de pedidos en el local",
            "RF-02", "CU-01", "Módulo de Pedidos"],
           ["Atender pedidos desde cualquier lugar (canal web)",
            "RF-03", "CU-02", "Tienda virtual"],
           ["Asegurar el cobro de los pedidos",
            "RF-05, RF-08", "CU-03", "Módulo de Cobros"],
           ["Controlar la entrega de los pedidos a domicilio",
            "RF-06", "CU-02", "Módulo de Delivery"],
           ["Mantener la carta actualizada",
            "RF-01", "CU-01", "Módulo de Carta"]],
          ancho_col=[6.0, 2.0, 2.4, 4.0],
          nota="Nota. Elaboración propia a partir de la matriz de "
               "trazabilidad definida por el equipo.")

titulo2(doc, "3.4. Requerimientos Funcionales y No Funcionales")
parrafo(doc,
        "Los requerimientos funcionales describen qué debe hacer el "
        "sistema, mientras que los no funcionales describen las "
        "características, restricciones o condiciones que debe cumplir "
        "(Pressman, 2014). A continuación se presenta la clasificación de "
        "los requerimientos del sistema de gestión de pedidos de Fogón "
        "Andino S.A.C.")
tabla_apa(doc, 4, "Requerimientos funcionales del sistema",
          ["ID", "Nombre", "Descripción"],
          [["RF-01", "Gestionar la carta de platos",
            "El sistema deberá permitir al administrador registrar, "
            "modificar, habilitar y deshabilitar los platos de la carta, "
            "incluyendo nombre, descripción, precio y categoría."],
           ["RF-02", "Registrar pedido en el local",
            "El sistema deberá permitir al mozo registrar el pedido de "
            "una mesa, indicando los platos y sus cantidades."],
           ["RF-03", "Registrar pedido en línea",
            "El sistema deberá permitir al cliente armar su pedido en la "
            "tienda virtual, consultar el stock disponible y confirmar el "
            "pedido."],
           ["RF-04", "Gestionar el estado del pedido",
            "El sistema deberá permitir actualizar y consultar el estado "
            "del pedido (registrado, en preparación, listo, entregado)."],
           ["RF-05", "Procesar pagos",
            "El sistema deberá integrarse con una pasarela de pago para "
            "autorizar transacciones con tarjeta y billeteras digitales."],
           ["RF-06", "Gestionar la entrega a domicilio",
            "El sistema deberá asignar un repartidor a cada pedido "
            "entregable y registrar la confirmación de la entrega."],
           ["RF-07", "Gestionar reservas de mesa",
            "El sistema deberá permitir al cliente reservar una mesa "
            "indicando fecha, hora y número de personas."],
           ["RF-08", "Emitir comprobantes",
            "El sistema deberá generar boletas y facturas electrónicas "
            "asociadas a cada pedido."],
           ["RF-09", "Generar reportes de ventas",
            "El sistema deberá generar reportes de ventas diarios y "
            "mensuales por plato, mesero y canal de venta."],
           ["RF-10", "Gestionar inventario y compras",
            "El sistema deberá registrar las entradas y salidas de insumos "
            "y generar órdenes de compra automáticas al alcanzar el stock "
            "mínimo."]],
          ancho_col=[1.6, 4.4, 8.4],
          nota="Nota. Elaboración propia.")
tabla_apa(doc, 5, "Requerimientos no funcionales del sistema",
          ["ID", "Categoría", "Descripción"],
          [["RNF-01", "Rendimiento",
            "El sistema deberá responder a las consultas de la carta y de "
            "estado de pedido en un tiempo máximo de 3 segundos bajo "
            "carga normal."],
           ["RNF-02", "Disponibilidad",
            "El sistema deberá mantener una disponibilidad mínima del "
            "99,5 % del tiempo durante el horario de operación."],
           ["RNF-03", "Seguridad",
            "El sistema deberá requerir autenticación de usuario y "
            "cifrar las transmisiones mediante TLS 1.2 o superior."],
           ["RNF-04", "Usabilidad",
            "La tienda virtual deberá ser utilizable por un cliente "
            "novato que complete un pedido en menos de 5 minutos."],
           ["RNF-05", "Escalabilidad",
            "El sistema deberá soportar hasta 500 usuarios concurrentes "
            "sin degradación del rendimiento."],
           ["RNF-06", "Compatibilidad",
            "La tienda virtual deberá funcionar en los navegadores "
            "principales y en dispositivos móviles."]],
          ancho_col=[1.8, 2.9, 9.7],
          nota="Nota. Elaboración propia.")
parrafo(doc,
        "Adicionalmente, se identifican las siguientes restricciones que "
        "limitan las alternativas de diseño e implementación: el "
        "desarrollo y operación del sistema deberá respetar la Ley N° "
        "29733 de Protección de Datos Personales del Perú; la solución "
        "deberá ejecutarse sobre infraestructura en la nube; y la "
        "implementación deberá quedar concluida dentro del plazo "
        "estipulado en el cronograma del proyecto.")

doc.add_page_break()

titulo2(doc, "3.5. Especificación de Casos de Uso")
parrafo(doc,
        "A continuación se especifican tres casos de uso del sistema "
        "considerando todas sus partes: identificador, nombre, actor "
        "principal, descripción, precondiciones, flujo principal, flujos "
        "alternativos y postcondiciones. Estos casos de uso se desprenden "
        "de los requerimientos funcionales RF-02, RF-03 y RF-05 "
        "respectivamente.")

# ---- CU-01
tabla_apa(doc, 6, "Especificación del caso de uso CU-01",
          ["Elemento", "Descripción"],
          [["ID / Nombre", "CU-01. Registrar pedido en el local"],
           ["Actor principal", "Mozo"],
           ["Descripción",
            "Este caso de uso permite al mozo registrar el pedido de un "
            "cliente en el local, asociándolo a una mesa y enviándolo a "
            "cocina."],
           ["Precondiciones",
            "El mozo ha iniciado sesión en el sistema y la mesa se "
            "encuentra disponible."],
           ["Flujo principal",
            "1. El mozo selecciona la mesa asignada.\n"
            "2. El sistema muestra la carta de platos disponibles.\n"
            "3. El mozo agrega los platos y sus cantidades.\n"
            "4. El sistema valida el stock de cada plato.\n"
            "5. El mozo confirma el pedido.\n"
            "6. El sistema registra el pedido, lo pone en estado "
            "\"registrado\" y lo envía a la cocina."],
           ["Flujos alternativos",
            "3a. Si un plato no tiene stock, el sistema lo informa y el "
            "mozo puede retirarlo del pedido o sugerir un sustituto.\n"
            "5a. Si el cliente desea agregar más platos, se retorna al "
            "paso 3."],
           ["Postcondiciones",
            "El pedido queda registrado y disponible para la cocina; la "
            "mesa cambia a estado \"ocupada\"."]],
          ancho_col=[3.4, 11.0],
          nota="Nota. Elaboración propia.")

# ---- CU-02
tabla_apa(doc, 7, "Especificación del caso de uso CU-02",
          ["Elemento", "Descripción"],
          [["ID / Nombre", "CU-02. Realizar pedido en línea con delivery"],
           ["Actor principal", "Cliente"],
           ["Descripción",
            "Este caso de uso permite al cliente armar un pedido en la "
            "tienda virtual, confirmar la disponibilidad, pagar en línea "
            "y solicitar la entrega a domicilio."],
           ["Precondiciones",
            "El cliente tiene acceso a la tienda virtual y ha ingresado "
            "una dirección de entrega válida."],
           ["Flujo principal",
            "1. El cliente consulta la carta de platos disponibles.\n"
            "2. El cliente selecciona los platos y las cantidades.\n"
            "3. El sistema verifica el stock de cada plato.\n"
            "4. El cliente confirma el pedido y la dirección de entrega.\n"
            "5. El cliente realiza el pago a través de la pasarela de "
            "pago.\n"
            "6. El sistema registra el pago y el pedido en estado "
            "\"registrado\".\n"
            "7. El sistema asigna un repartidor y notifica el tiempo "
            "estimado de entrega."],
           ["Flujos alternativos",
            "3a. Si un plato no tiene stock, el sistema lo notifica y "
            "permite retirarlo o sustituirlo.\n"
            "5a. Si el pago es rechazado, el sistema invita a reintentar "
            "con otro medio de pago; si el cliente cancela, no se "
            "registra el pedido."],
           ["Postcondiciones",
            "El pedido queda registrado y pagado; el repartidor recibe "
            "la asignación de la entrega."]],
          ancho_col=[3.4, 11.0],
          nota="Nota. Elaboración propia.")

# ---- CU-03
tabla_apa(doc, 8, "Especificación del caso de uso CU-03",
          ["Elemento", "Descripción"],
          [["ID / Nombre", "CU-03. Procesar pago y emitir comprobante"],
           ["Actor principal", "Cajero"],
           ["Descripción",
            "Este caso de uso permite al cajero procesar el pago de un "
            "pedido y emitir el comprobante electrónico correspondiente."],
           ["Precondiciones",
            "El cajero ha iniciado sesión y el pedido se encuentra en "
            "estado \"listo\"."],
           ["Flujo principal",
            "1. El cajero selecciona el pedido desde la lista de pedidos "
            "listos.\n"
            "2. El sistema muestra el detalle del pedido y el total a "
            "pagar.\n"
            "3. El cajero registra el medio de pago (efectivo, tarjeta o "
            "billetera digital).\n"
            "4. El sistema procesa el pago y actualiza el estado del "
            "pedido.\n"
            "5. El cajero solicita la emisión del comprobante.\n"
            "6. El sistema genera la boleta o factura electrónica."],
           ["Flujos alternativos",
            "4a. Si el pago con tarjeta es rechazado, el cajero registra "
            "un medio de pago alternativo.\n"
            "5a. Si el cliente no requiere comprobante, el flujo termina "
            "sin emitirlo, registrando la venta como sin comprobante."],
           ["Postcondiciones",
            "El pago queda registrado, el comprobante electrónico queda "
            "emitido y el pedido pasa a estado \"cerrado\"."]],
          ancho_col=[3.4, 11.0],
          nota="Nota. Elaboración propia.")

doc.add_page_break()

# ===============================================================
# 4. CONCLUSIONES
# ===============================================================
titulo1(doc, "4. Conclusiones")
parrafo(doc,
        "En el presente avance se modelaron los requerimientos del "
        "negocio de Fogón Andino S.A.C., una empresa ficticia del rubro "
        "gastronómico. Se identificaron siete actores del negocio y cinco "
        "casos de uso del negocio, se construyó el modelo de dominio con "
        "nueve conceptos y se elaboraron dos diagramas de actividades "
        "correspondientes a los procesos de atención en el local y de "
        "pedidos en línea con delivery. Asimismo, se elaboró la "
        "especificación de requerimientos de software, que incluye el "
        "diagrama de contexto, diez requerimientos funcionales y seis no "
        "funcionales clasificados, y tres especificaciones de casos de "
        "uso con todas sus partes.")
parrafo(doc,
        "Se concluye que el modelado del negocio permitió comprender la "
        "organización antes de automatizarla, tal como lo plantea "
        "Sommerville (2011), y que la trazabilidad establecida entre las "
        "necesidades del negocio, los requerimientos funcionales, los "
        "casos de uso y los componentes del sistema constituye una "
        "práctica fundamental de la gestión de requerimientos (CMMI "
        "Institute, 2023). Esta documentación servirá como insumo "
        "directo para la fase de arquitectura empresarial basada en "
        "TOGAF, que se desarrollará en la siguiente unidad del curso, "
        "pues define de manera clara qué procesos y funcionalidades "
        "deberán ser soportados por la arquitectura futura de la "
        "organización.")
parrafo(doc,
        "Finalmente, el equipo reconoce que la gestión de sus "
        "requerimientos se ubica en el nivel 2 (REQM) del modelo CMMI y "
        "que, para consolidar prácticas del nivel 3 (RD), será necesario "
        "ampliar la obtención de requerimientos a partir de las "
        "necesidades de todos los stakeholders y descomponerlos en "
        "requisitos de componentes en mayor detalle.")

doc.add_page_break()

# ===============================================================
# REFERENCIAS
# ===============================================================
titulo1(doc, "Referencias")
referencias = [
    "American Psychological Association. (2020). Publication manual of the "
    "American Psychological Association (7th ed.). "
    "https://doi.org/10.1037/0000165-000",
    "Booch, G., Jacobson, I., y Rumbaugh, J. (2006). El lenguaje unificado "
    "de modelado 2.0 (2.ª ed.). Addison Wesley.",
    "CMMI Institute. (2023). CMMI V3.0: Capability Maturity Model "
    "Integration. ISACA.",
    "ISO/IEC/IEEE. (2018). ISO/IEC/IEEE 29148:2018 Systems and software "
    "engineering—Life cycle processes—Requirements engineering. "
    "International Organization for Standardization.",
    "Jacobson, I., Booch, G., y Rumbaugh, J. (2000). El proceso unificado "
    "de desarrollo de software. Pearson Educación.",
    "Pressman, R. S. (2014). Ingeniería del software: un enfoque práctico "
    "(7.ª ed.). McGraw-Hill.",
    "Project Management Institute. (2021). Guía de los fundamentos para "
    "la dirección de proyectos (PMBOK Guide) (7.ª ed.). PMI.",
    "Sommerville, I. (2011). Ingeniería de software (9.ª ed.). Pearson "
    "Educación.",
]
for ref in referencias:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 2.0
    # Sangria francesa
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)
    run = p.add_run(ref)
    run.font.name = FUENTE
    run.font.size = Pt(12)

doc.save(SALIDA)
print("Informe generado:", SALIDA)
