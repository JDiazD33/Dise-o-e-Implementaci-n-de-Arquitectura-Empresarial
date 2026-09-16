# -*- coding: utf-8 -*-
"""Genera la presentacion del Avance 1 (Fogón Andino S.A.C.)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "Avance1_Fogon_Andino.pptx")

AZUL = RGBColor(0x1F, 0x3A, 0x5F)
AZUL_MEDIO = RGBColor(0x4A, 0x6F, 0xA5)
NARANJA = RGBColor(0xD9, 0x8E, 0x32)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_TEXTO = RGBColor(0x33, 0x33, 0x33)
FONDO = RGBColor(0xF7, 0xFA, 0xFC)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


def diapositiva_titulo(titulo, subtitulo):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fondo = s.background.fill
    fondo.solid()
    fondo.fore_color.rgb = AZUL
    # Barra decorativa
    barra = s.shapes.add_shape(1, Inches(0), Inches(6.9), Inches(13.333),
                               Inches(0.6))
    barra.fill.solid()
    barra.fill.fore_color.rgb = NARANJA
    barra.line.fill.background()
    # Titulo
    tb = s.shapes.add_textbox(Inches(1), Inches(2.3), Inches(11.3), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = titulo
    r.font.size = Pt(40)
    r.font.bold = True
    r.font.color.rgb = BLANCO
    r.font.name = "Calibri"
    # Subtitulo
    tb2 = s.shapes.add_textbox(Inches(1.5), Inches(4.0), Inches(10.3),
                               Inches(1.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = subtitulo
    r2.font.size = Pt(20)
    r2.font.color.rgb = RGBColor(0xD8, 0xE4, 0xF0)
    r2.font.name = "Calibri"
    return s


def diapositiva_contenido(titulo, bullets, notas=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fondo = s.background.fill
    fondo.solid()
    fondo.fore_color.rgb = FONDO
    # Encabezado
    enc = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333),
                             Inches(1.0))
    enc.fill.solid()
    enc.fill.fore_color.rgb = AZUL
    enc.line.fill.background()
    tf = enc.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.5)
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = titulo
    r.font.size = Pt(28)
    r.font.bold = True
    r.font.color.rgb = BLANCO
    r.font.name = "Calibri"
    # Contenido
    tb = s.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1),
                              Inches(5.6))
    tfb = tb.text_frame
    tfb.word_wrap = True
    for i, b in enumerate(bullets):
        p = tfb.paragraphs[0] if i == 0 else tfb.add_paragraph()
        p.space_after = Pt(10)
        r = p.add_run()
        r.text = "• " + b
        r.font.size = Pt(18)
        r.font.color.rgb = GRIS_TEXTO
        r.font.name = "Calibri"
    if notas:
        s.notes_slide.notes_text_frame.text = notas
    return s


def diapositiva_imagen(titulo, archivo, nota=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fondo = s.background.fill
    fondo.solid()
    fondo.fore_color.rgb = FONDO
    enc = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333),
                             Inches(0.8))
    enc.fill.solid()
    enc.fill.fore_color.rgb = AZUL
    enc.line.fill.background()
    tf = enc.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.5)
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = titulo
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = BLANCO
    r.font.name = "Calibri"
    path = os.path.join(BASE, archivo)
    pic = s.shapes.add_picture(path, Inches(0.7), Inches(1.0),
                               height=Inches(6.2))
    # Centrar horizontalmente
    pic.left = Emu(int((prs.slide_width - pic.width) / 2))
    if nota:
        s.notes_slide.notes_text_frame.text = nota
    return s


def diapositiva_tabla(titulo, encabezados, filas, nota=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fondo = s.background.fill
    fondo.solid()
    fondo.fore_color.rgb = FONDO
    enc = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333),
                             Inches(0.8))
    enc.fill.solid()
    enc.fill.fore_color.rgb = AZUL
    enc.line.fill.background()
    tf = enc.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.5)
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = titulo
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = BLANCO
    r.font.name = "Calibri"
    n_filas = 1 + len(filas)
    n_cols = len(encabezados)
    grafico = s.shapes.add_table(n_filas, n_cols, Inches(0.5), Inches(1.0),
                                 Inches(12.3), Inches(0.4 * n_filas))
    tabla = grafico.table
    for j, h in enumerate(encabezados):
        c = tabla.cell(0, j)
        c.text = h
        for pa in c.text_frame.paragraphs:
            for ru in pa.runs:
                ru.font.bold = True
                ru.font.size = Pt(13)
                ru.font.color.rgb = BLANCO
                ru.font.name = "Calibri"
        c.fill.solid()
        c.fill.fore_color.rgb = AZUL_MEDIO
    for i, fila in enumerate(filas):
        for j, v in enumerate(fila):
            c = tabla.cell(i + 1, j)
            c.text = str(v)
            for pa in c.text_frame.paragraphs:
                for ru in pa.runs:
                    ru.font.size = Pt(12)
                    ru.font.color.rgb = GRIS_TEXTO
                    ru.font.name = "Calibri"
            c.fill.solid()
            c.fill.fore_color.rgb = BLANCO if i % 2 else RGBColor(0xEC, 0xF1, 0xF8)
    if nota:
        s.notes_slide.notes_text_frame.text = nota
    return s


# ---------------------------------------------------------------
# 1. Portada
# ---------------------------------------------------------------
s = diapositiva_titulo(
    "Modelado de Requerimientos del Negocio de Fogón Andino S.A.C.",
    "Avance 1 | Curso: Diseño e Implementación de Arquitectura Empresarial\n"
    "Universidad Tecnológica del Perú\n"
    "Integrantes: [Estudiante 1], [Estudiante 2], [Estudiante 3], "
    "[Estudiante 4]\nDocente: Ing. Jair Darnley Vásquez Aguirre")

# ---------------------------------------------------------------
# 2. Agenda
# ---------------------------------------------------------------
diapositiva_contenido("Agenda", [
    "Presentación de la empresa y sus procesos",
    "Modelado del negocio: actores, casos de uso y modelo de dominio",
    "Diagramas de actividades de los procesos clave",
    "Especificación de requerimientos de software (SRS)",
    "Nivel de madurez CMMI del equipo",
    "Conclusiones y próximos pasos",
])

# ---------------------------------------------------------------
# 3. La empresa
# ---------------------------------------------------------------
diapositiva_contenido("1. Presentación de la Empresa", [
    "Fogón Andino S.A.C.: restaurante de comida peruana en Miraflores, "
    "Lima.",
    "Capacidad para 80 comensales en 20 mesas; ~350 clientes diarios "
    "entre local y delivery.",
    "18 colaboradores: mozos, cocineros, cajeros, administrador y "
    "repartidores.",
    "Situación actual: procesos manuales y desintegrados que generan "
    "demoras y errores de registro.",
    "Decisión estratégica: transformación digital con un sistema de "
    "gestión de pedidos integrado.",
], notas="La empresa es ficticia, creada para fines académicos. "
         "Los volúmenes y tiempos son estimaciones razonables.")

# ---------------------------------------------------------------
# 4. Procesos del negocio
# ---------------------------------------------------------------
diapositiva_contenido("2. Actividad Principal y Procesos", [
    "Actividad principal: preparación y comercialización de comida "
    "peruana, en local y a domicilio.",
    "Proceso 1 – Atención de pedido en el local: recepción, toma de "
    "pedido, cocina, cobro.",
    "Proceso 2 – Pedido en línea con delivery: tienda virtual, stock, "
    "pago, preparación y entrega.",
    "Proceso 3 – Gestión de la carta e insumos: platos y "
    "abastecimiento de proveedores.",
    "Proceso 4 – Reservas y cobros: reserva de mesas y emisión de "
    "comprobantes.",
], notas="Para este avance se modelaron los dos procesos más "
         "relevantes: atención en el local y pedido online.")

# ---------------------------------------------------------------
# 5. Actores
# ---------------------------------------------------------------
diapositiva_tabla("3. Actores del Negocio",
                  ["Actor", "Tipo", "Rol principal"],
                  [["Cliente", "Externo", "Consume en el local o pide delivery"],
                   ["Mozo", "Interno", "Atiende al comensal y toma el pedido"],
                   ["Chef / Cocinero", "Interno", "Prepara los platos"],
                   ["Cajero", "Interno", "Cobra y emite comprobantes"],
                   ["Repartidor", "Externo", "Entrega los pedidos a domicilio"],
                   ["Proveedor", "Externo", "Abastece de insumos a la cocina"],
                   ["Administrador", "Interno", "Gestiona carta y reportes"]],
                  nota="7 actores identificados, externos e internos.")

# ---------------------------------------------------------------
# 6. Casos de uso del negocio
# ---------------------------------------------------------------
diapositiva_imagen("4. Casos de Uso del Negocio",
                   "fig1_casos_uso_negocio.png",
                   nota="5 casos de uso del negocio: Realizar Pedido, "
                        "Preparar Comida, Cobrar Pedido, Entregar a "
                        "Domicilio y Abastecer Insumos.")

# ---------------------------------------------------------------
# 7. Modelo de dominio
# ---------------------------------------------------------------
diapositiva_imagen("5. Modelo de Dominio",
                   "fig2_modelo_dominio.png",
                   nota="Conceptos: Cliente, Pedido, DetallePedido, Plato, "
                        "Mesa, Reserva, Empleado, Repartidor y Boleta, "
                        "con sus relaciones y multiplicidades.")

# ---------------------------------------------------------------
# 8. Diagrama de actividades 1
# ---------------------------------------------------------------
diapositiva_imagen("6. Actividades: Atención en el Local",
                   "fig3_actividades_local.png",
                   nota="Proceso que va desde la recepción del cliente "
                        "hasta el cobro y la liberación de la mesa.")

# ---------------------------------------------------------------
# 9. Diagrama de actividades 2
# ---------------------------------------------------------------
diapositiva_imagen("7. Actividades: Pedido en Línea con Delivery",
                   "fig4_actividades_online.png",
                   nota="Incluye validación de stock, pago en línea y "
                        "asignación del repartidor.")

# ---------------------------------------------------------------
# 10. Diagrama de contexto
# ---------------------------------------------------------------
diapositiva_imagen("8. Diagrama de Contexto del Sistema",
                   "fig5_diagrama_contexto.png",
                   nota="Sistema central con 6 tipos de usuario y 2 "
                        "sistemas externos: pasarela de pago y proveedores.")

# ---------------------------------------------------------------
# 11. Requerimientos funcionales
# ---------------------------------------------------------------
diapositiva_tabla("9. Requerimientos Funcionales",
                  ["ID", "Nombre"],
                  [["RF-01", "Gestionar la carta de platos"],
                   ["RF-02", "Registrar pedido en el local"],
                   ["RF-03", "Registrar pedido en línea"],
                   ["RF-04", "Gestionar el estado del pedido"],
                   ["RF-05", "Procesar pagos"],
                   ["RF-06", "Gestionar la entrega a domicilio"],
                   ["RF-07", "Gestionar reservas de mesa"],
                   ["RF-08", "Emitir comprobantes"],
                   ["RF-09", "Generar reportes de ventas"],
                   ["RF-10", "Gestionar inventario y compras"]],
                  nota="10 requerimientos funcionales especificados en la "
                        "SRS del informe.")

# ---------------------------------------------------------------
# 12. Requerimientos no funcionales
# ---------------------------------------------------------------
diapositiva_tabla("10. Requerimientos No Funcionales",
                  ["ID", "Categoría", "Descripción"],
                  [["RNF-01", "Rendimiento", "Respuesta < 3 segundos"],
                   ["RNF-02", "Disponibilidad", "99,5 % del tiempo"],
                   ["RNF-03", "Seguridad", "Autenticación y TLS 1.2+"],
                   ["RNF-04", "Usabilidad", "Pedido en < 5 minutos"],
                   ["RNF-05", "Escalabilidad", "500 usuarios concurrentes"],
                   ["RNF-06", "Compatibilidad", "Web y móvil"]],
                  nota="Restricciones adicionales: Ley 29733 de "
                        "protección de datos, infraestructura en la nube "
                        "y cumplimiento del cronograma.")

# ---------------------------------------------------------------
# 13. CMMI
# ---------------------------------------------------------------
diapositiva_contenido("11. Nivel de Madurez CMMI del Equipo", [
    "Nivel 2 – Gestión de Requerimientos (REQM): requerimientos "
    "documentados, clasificados y controlados.",
    "Se mantiene la trazabilidad mediante una matriz que conecta "
    "necesidades, RF, casos de uso y componentes.",
    "Procedimiento de control de cambios: todo cambio se registra, "
    "analiza y aprueba.",
    "Prácticas iniciales del Nivel 3 (RD): obtención de requerimientos "
    "a partir de las necesidades de los stakeholders.",
    "Objetivo: consolidar el nivel 3 en los siguientes avances.",
], notas="Ubicamos al equipo en el nivel 2 (REQM) con prácticas "
         "iniciales del nivel 3 (RD).")

# ---------------------------------------------------------------
# 14. Casos de uso del sistema
# ---------------------------------------------------------------
diapositiva_contenido("12. Especificación de Casos de Uso", [
    "CU-01: Registrar pedido en el local (actor: Mozo).",
    "CU-02: Realizar pedido en línea con delivery (actor: Cliente).",
    "CU-03: Procesar pago y emitir comprobante (actor: Cajero).",
    "Cada especificación incluye: ID, actor principal, descripción, "
    "precondiciones, flujo principal, flujos alternativos y "
    "postcondiciones.",
    "Estos casos de uso dan trazabilidad a los RF-02, RF-03 y RF-05.",
], notas="Las tres especificaciones completas se encuentran en el "
         "informe (Tablas 6, 7 y 8).")

# ---------------------------------------------------------------
# 15. Conclusiones
# ---------------------------------------------------------------
diapositiva_contenido("13. Conclusiones", [
    "Se modeló el negocio de Fogón Andino S.A.C.: 7 actores, 5 casos "
    "de uso del negocio y 9 conceptos en el modelo de dominio.",
    "Se elaboraron 2 diagramas de actividades de los procesos más "
    "relevantes.",
    "Se elaboró la SRS: diagrama de contexto, 10 RF y 6 RNF "
    "clasificados, y 3 especificaciones de casos de uso.",
    "La trazabilidad establecida es insumo directo para la fase de "
    "arquitectura empresarial (TOGAF) de la Unidad 2.",
    "Próximo paso: definir la arquitectura empresarial basada en "
    "TOGAF a partir de estos requerimientos.",
])

prs.save(SALIDA)
print("Presentacion generada:", SALIDA)
print("Diapositivas:", len(prs.slides.__iter__.__self__._sldIdLst))
