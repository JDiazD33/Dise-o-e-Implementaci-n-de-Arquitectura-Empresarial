# -*- coding: utf-8 -*-
"""Genera los diagramas UML del Avance 1 - Fogón Andino S.A.C."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Circle, FancyArrowPatch, Rectangle
import matplotlib.patheffects as pe
import os

OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams["font.family"] = "DejaVu Sans"

AZUL = "#4A6FA5"
AZUL_CLARO = "#E8F0FE"
NARANJA = "#D98E32"
NARANJA_CLARO = "#FFF3E0"
GRIS_BORDE = "#6B7280"
VERDE = "#5B8C5A"


def guardar(fig, nombre):
    path = os.path.join(OUT, nombre)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK:", nombre)


# ---------------------------------------------------------------
# Funcion auxiliar: actor (stick figure)
# ---------------------------------------------------------------
def dibujar_actor(ax, x, y, nombre, dx=0.0, dy=0.0):
    """Dibuja un actor stick figure con etiqueta debajo."""
    s = 1.0  # escala
    # cabeza
    ax.add_patch(Circle((x, y + 0.42 * s), 0.11 * s, fill=False,
                        lw=1.6, edgecolor="black", zorder=5))
    # cuerpo
    ax.plot([x, x], [y + 0.31 * s, y - 0.05 * s], color="black", lw=1.6, zorder=5)
    # brazos
    ax.plot([x - 0.18 * s, x + 0.18 * s], [y + 0.18 * s, y + 0.18 * s],
            color="black", lw=1.6, zorder=5)
    # piernas
    ax.plot([x, x - 0.16 * s], [y - 0.05 * s, y - 0.38 * s],
            color="black", lw=1.6, zorder=5)
    ax.plot([x, x + 0.16 * s], [y - 0.05 * s, y - 0.38 * s],
            color="black", lw=1.6, zorder=5)
    ax.text(x, y - 0.62 * s, nombre, ha="center", va="top",
            fontsize=9, fontweight="bold", zorder=5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec=GRIS_BORDE, lw=0.8))
    return (x, y + 0.2 * s)  # punto de conexion aproximado


def linea(ax, p1, p2, lw=1.1, color="black", estilo="-"):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw,
            linestyle=estilo, zorder=1)


# ===============================================================
# FIGURA 1 - Diagrama de casos de uso del negocio
# ===============================================================
def diagrama_casos_uso():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10.5)
    ax.axis("off")

    # Caja del negocio
    ax.add_patch(FancyBboxPatch((5.2, 0.6), 5.6, 9.3,
                                boxstyle="round,pad=0.15",
                                fc="#F7FAFC", ec=AZUL, lw=1.8, zorder=0))
    ax.text(8.0, 9.95, "Fogón Andino S.A.C. (Negocio)",
            ha="center", va="top", fontsize=10, fontweight="bold", color=AZUL)

    casos = [
        ("CU-N1\nRealizar Pedido", 6.9, 8.0, 1.45),
        ("CU-N2\nPreparar Comida", 9.1, 8.0, 1.45),
        ("CU-N3\nCobrar Pedido", 6.9, 5.2, 1.45),
        ("CU-N4\nEntregar Pedido\na Domicilio", 9.1, 5.2, 1.55),
        ("CU-N5\nAbastecer Insumos", 8.0, 2.3, 1.55),
    ]
    pos_casos = {}
    for nombre, cx, cy, w in casos:
        ax.add_patch(Ellipse((cx, cy), w, 0.95, fc=NARANJA_CLARO,
                             ec=NARANJA, lw=1.5, zorder=3))
        ax.text(cx, cy, nombre, ha="center", va="center", fontsize=8,
                zorder=4)
        pos_casos[nombre.split("\n")[0]] = (cx, cy)

    # Actores izquierda
    a_cli = dibujar_actor(ax, 2.6, 7.6, "Cliente")
    a_prov = dibujar_actor(ax, 2.6, 2.2, "Proveedor")
    # Actores derecha
    a_mozo = dibujar_actor(ax, 13.4, 8.2, "Mozo")
    a_chef = dibujar_actor(ax, 13.4, 5.9, "Chef / Cocina")
    a_caj = dibujar_actor(ax, 13.4, 3.6, "Cajero")
    a_rep = dibujar_actor(ax, 2.6, 5.0, "Repartidor")

    def con(actor_pt, caso_key, lado="izq"):
        cx, cy = pos_casos[caso_key]
        if lado == "izq":
            p2 = (cx - 0.72, cy)
        else:
            p2 = (cx + 0.72, cy)
        linea(ax, actor_pt, p2, lw=1.0, color=GRIS_BORDE)

    # Conexiones
    con(a_cli, "CU-N1", "izq")
    con(a_cli, "CU-N3", "izq")
    con(a_cli, "CU-N4", "izq")
    con(a_mozo, "CU-N1", "der")
    con(a_chef, "CU-N2", "der")
    con(a_chef, "CU-N5", "der")
    con(a_prov, "CU-N5", "izq")
    con(a_caj, "CU-N3", "der")
    con(a_rep, "CU-N4", "izq")

    guardar(fig, "fig1_casos_uso_negocio.png")


# ===============================================================
# FIGURA 2 - Modelo de dominio
# ===============================================================
def caja_dominio(ax, x, y, nombre, atributos, w=2.9, ah=0.32):
    """Caja de clase de dominio: nombre + atributos."""
    h = 0.55 + ah * len(atributos)
    # seccion nombre
    ax.add_patch(Rectangle((x, y + h - 0.55), w, 0.55, fc="#DCE6F2",
                           ec=AZUL, lw=1.4, zorder=3))
    ax.text(x + w / 2, y + h - 0.28, nombre, ha="center", va="center",
            fontsize=9.5, fontweight="bold", zorder=4)
    # seccion atributos
    ax.add_patch(Rectangle((x, y), w, h - 0.55, fc="white", ec=AZUL,
                           lw=1.4, zorder=3))
    for i, a in enumerate(atributos):
        ax.text(x + 0.12, y + h - 0.55 - 0.24 - i * ah, a, ha="left",
                va="center", fontsize=7.6, zorder=4)
    return (x, y, x + w, y + h, x + w / 2, y + h / 2)


def linea_rel(ax, c1, c2, x1, y1, x2, y2, mult1="", mult2="", et="",
              curva=0.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=GRIS_BORDE, lw=1.1),
                zorder=1)
    if et:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, et, ha="center",
                va="bottom", fontsize=7.2, style="italic", color="#333333")
    if mult1:
        ax.text(x1 + 0.08, y1 + 0.14, mult1, fontsize=7.2, color="#333333")
    if mult2:
        ax.text(x2 - 0.08, y2 + 0.14, mult2, ha="right", fontsize=7.2,
                color="#333333")


def diagrama_dominio():
    fig, ax = plt.subplots(figsize=(13.5, 8.6))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12.5)
    ax.axis("off")

    ax.text(10, 12.2, "Modelo de Dominio - Fogón Andino S.A.C.",
            ha="center", va="top", fontsize=11, fontweight="bold", color=AZUL)

    cliente = caja_dominio(ax, 1.2, 8.6, "Cliente",
                           ["- id_cliente : Integer",
                            "- nombres : String",
                            "- telefono : String",
                            "- direccion : String"])
    pedido = caja_dominio(ax, 8.2, 8.9, "Pedido",
                          ["- id_pedido : Integer",
                           "- fecha : Date",
                           "- estado : String",
                           "- total : Decimal"])
    detalle = caja_dominio(ax, 8.4, 4.6, "DetallePedido",
                           ["- id_detalle : Integer",
                            "- cantidad : Integer",
                            "- subtotal : Decimal"])
    plato = caja_dominio(ax, 14.6, 4.6, "Plato",
                         ["- id_plato : Integer",
                          "- nombre : String",
                          "- precio : Decimal",
                          "- categoria : String"])
    mesa = caja_dominio(ax, 1.4, 4.9, "Mesa",
                        ["- numero : Integer",
                         "- capacidad : Integer",
                         "- estado : String"])
    reserva = caja_dominio(ax, 1.2, 1.2, "Reserva",
                           ["- id_reserva : Integer",
                            "- fecha : Date",
                            "- hora : Time",
                            "- nro_personas : Integer"])
    empleado = caja_dominio(ax, 8.3, 1.2, "Empleado",
                            ["- id_empleado : Integer",
                             "- nombres : String",
                             "- rol : String"])
    boleta = caja_dominio(ax, 14.8, 9.0, "Boleta",
                          ["- id_boleta : Integer",
                           "- serie : String",
                           "- numero : String",
                           "- total : Decimal"])
    repartidor = caja_dominio(ax, 15.0, 1.2, "Repartidor",
                              ["- id_repartidor : Integer",
                               "- nombres : String",
                               "- vehiculo : String"])

    # Relaciones (x1,y1) -> (x2,y2)
    linea_rel(ax, 0, 0, cliente[2], cliente[4] - 0.6, pedido[0], pedido[4] + 0.2,
              "1", "*", "realiza")
    linea_rel(ax, 0, 0, pedido[0] + 0.2, pedido[1], detalle[0] + 0.1, detalle[3],
              "1", "*", "contiene")
    linea_rel(ax, 0, 0, plato[0], plato[4], detalle[2], detalle[4],
              "1", "*", "se incluye")
    linea_rel(ax, 0, 0, mesa[2], mesa[4], pedido[0], pedido[4] - 0.9,
              "1", "*", "se asigna")
    linea_rel(ax, 0, 0, reserva[3], reserva[4] - 0.9, mesa[0] + 0.4, mesa[1],
              "*", "1", "reserva")
    linea_rel(ax, 0, 0, cliente[1] + 0.5, cliente[1], reserva[2] - 0.3, reserva[3],
              "1", "*", "solicita")
    linea_rel(ax, 0, 0, pedido[2], pedido[4] + 0.3, boleta[0], boleta[4] + 0.1,
              "1", "0..1", "genera")
    linea_rel(ax, 0, 0, empleado[3], empleado[4] + 0.7, pedido[1] + 0.4, pedido[1],
              "1", "*", "atiende")
    linea_rel(ax, 0, 0, repartidor[3], repartidor[4] + 0.8, detalle[1] + 0.3, detalle[1],
              "1", "*", "entrega")

    guardar(fig, "fig2_modelo_dominio.png")


# ===============================================================
# Diagrama de actividades (plantilla reutilizable)
# ===============================================================
def diagrama_actividades(nombre_archivo, titulo, nodos, aristas,
                         ancho=9.5, alto=13.0):
    """
    nodos: lista (id, x, y, etiqueta, tipo)
      tipo: "ini" | "fin" | "act" | "dec"
    aristas: lista (id_origen, id_destino, etiqueta, condicion)
    Las coords se dan con y creciendo hacia abajo.
    """
    fig, ax = plt.subplots(figsize=(ancho, alto))
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, 20)
    ax.axis("off")

    ax.text(0, 19.6, titulo, ha="center", va="top", fontsize=11,
            fontweight="bold", color=AZUL)

    pos = {}
    for nid, x, y, etiqueta, tipo in nodos:
        yy = 18.5 - y  # invertir eje
        pos[nid] = (x, yy)
        if tipo == "ini":
            ax.add_patch(Circle((x, yy), 0.30, fc="black", ec="black", zorder=5))
        elif tipo == "fin":
            ax.add_patch(Circle((x, yy), 0.30, fc="white", ec="black",
                                lw=2.0, zorder=5))
            ax.add_patch(Circle((x, yy), 0.17, fc="black", ec="black", zorder=6))
        elif tipo == "act":
            ax.add_patch(FancyBboxPatch((x - 1.85, yy - 0.34), 3.7, 0.68,
                                        boxstyle="round,pad=0.06",
                                        fc=AZUL_CLARO, ec=AZUL, lw=1.4,
                                        zorder=3))
            ax.text(x, yy, etiqueta, ha="center", va="center", fontsize=8.6,
                    zorder=4)
        elif tipo == "dec":
            ax.plot([x, x + 1.05, x, x - 1.05], [yy + 0.62, yy, yy - 0.62, yy],
                    color=NARANJA, lw=1.5, zorder=3)
            ax.fill([x, x + 1.05, x, x - 1.05], [yy + 0.62, yy, yy - 0.62, yy],
                    fc=NARANJA_CLARO, zorder=2)
            ax.text(x, yy, etiqueta, ha="center", va="center", fontsize=8.4,
                    zorder=4)

    from matplotlib.patches import FancyArrowPatch

    for o, d, et, cond in aristas:
        x1, y1 = pos[o]
        x2, y2 = pos[d]
        retroceso = y2 > y1  # flecha que regresa hacia arriba
        misma_altura = abs(y1 - y2) < 0.01
        if misma_altura:
            shrink = 14 if x1 != x2 else 2
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    connectionstyle="arc3,rad=0",
                                    arrowstyle="-|>", mutation_scale=14,
                                    color=GRIS_BORDE, lw=1.3, zorder=2,
                                    shrinkA=shrink, shrinkB=shrink)
            ax.add_patch(arrow)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.25
        elif retroceso:
            rad = -0.55 if x1 >= x2 else 0.55
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    connectionstyle=f"arc3,rad={rad}",
                                    arrowstyle="-|>", mutation_scale=14,
                                    color=GRIS_BORDE, lw=1.3, zorder=2,
                                    shrinkA=6, shrinkB=6)
            ax.add_patch(arrow)
            mx, my = (x1 + x2) / 2 - 1.6, (y1 + y2) / 2
        else:
            arrow = FancyArrowPatch((x1, y1 - 0.42), (x2, y2 + 0.52),
                                    connectionstyle="arc3,rad=0",
                                    arrowstyle="-|>", mutation_scale=14,
                                    color=GRIS_BORDE, lw=1.3, zorder=2,
                                    shrinkA=2, shrinkB=2)
            ax.add_patch(arrow)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if cond:
            ax.text(mx + 0.15, my, cond, fontsize=8.0, color="#B03A2E",
                    va="center", ha="left",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white",
                              ec="#B03A2E", lw=0.6))

    guardar(fig, nombre_archivo)


# ===============================================================
# FIGURA 3 - Actividades: atencion de pedido en el local
# ===============================================================
def actividades_local():
    nodos = [
        ("ini", 0, 0.5, "", "ini"),
        ("a1", 0, 1.9, "Recibir al cliente y asignar mesa", "act"),
        ("a2", 0, 3.3, "Entregar la carta al cliente", "act"),
        ("a3", 0, 4.7, "Tomar el pedido del cliente", "act"),
        ("d1", 0, 6.3, "¿Pedido completo?", "dec"),
        ("a4", 0, 8.0, "Enviar el pedido a cocina", "act"),
        ("a5", 0, 9.4, "Preparar los platos", "act"),
        ("a6", 0, 10.8, "Servir la comida en la mesa", "act"),
        ("a7", 0, 12.1, "El cliente disfruta la comida", "act"),
        ("a8", 0, 13.4, "Solicitar la cuenta y emitir boleta", "act"),
        ("a9", 0, 14.7, "Cobrar y liberar la mesa", "act"),
        ("fin", 0, 16.0, "", "fin"),
    ]
    aristas = [
        ("ini", "a1", "", ""),
        ("a1", "a2", "", ""),
        ("a2", "a3", "", ""),
        ("a3", "d1", "", ""),
        ("d1", "a4", "", "Sí"),
        ("d1", "a3", "", "No"),
        ("a4", "a5", "", ""),
        ("a5", "a6", "", ""),
        ("a6", "a7", "", ""),
        ("a7", "a8", "", ""),
        ("a8", "a9", "", ""),
        ("a9", "fin", "", ""),
    ]
    diagrama_actividades("fig3_actividades_local.png",
                         "Proceso de Atención de Pedido en el Local",
                         nodos, aristas)


# ===============================================================
# FIGURA 4 - Actividades: pedido online con delivery
# ===============================================================
def actividades_online():
    nodos = [
        ("ini", 0, 0.5, "", "ini"),
        ("a1", 0, 1.9, "El cliente ingresa a la web/app", "act"),
        ("a2", 0, 3.3, "Consultar la carta de platos", "act"),
        ("a3", 0, 4.7, "Seleccionar platos y cantidades", "act"),
        ("a4", 0, 6.1, "Confirmar el pedido", "act"),
        ("d1", 0, 7.7, "¿Hay stock disponible?", "dec"),
        ("a5", 0, 9.4, "Registrar el pedido en el sistema", "act"),
        ("a6", 0, 10.8, "Procesar el pago en línea", "act"),
        ("d2", 0, 12.4, "¿Pago aprobado?", "dec"),
        ("a7", 0, 14.1, "Enviar el pedido a cocina", "act"),
        ("a8", 0, 15.4, "Preparar y empaquetar la comida", "act"),
        ("a9", 0, 16.7, "Asignar repartidor y entregar", "act"),
        ("fin", 0, 18.0, "", "fin"),
        ("x1", -3.6, 7.7, "Notificar falta de stock", "act"),
    ]
    aristas = [
        ("ini", "a1", "", ""),
        ("a1", "a2", "", ""),
        ("a2", "a3", "", ""),
        ("a3", "a4", "", ""),
        ("a4", "d1", "", ""),
        ("d1", "a5", "", "Sí"),
        ("d1", "x1", "", "No"),
        ("x1", "a2", "", ""),
        ("a5", "a6", "", ""),
        ("a6", "d2", "", ""),
        ("d2", "a7", "", "Sí"),
        ("a7", "a8", "", ""),
        ("a8", "a9", "", ""),
        ("a9", "fin", "", ""),
    ]
    diagrama_actividades("fig4_actividades_online.png",
                         "Proceso de Pedido Online con Delivery",
                         nodos, aristas, ancho=9.5, alto=13.5)


# ===============================================================
# FIGURA 5 - Diagrama de contexto (estilo DFD: proceso unico,
# entidades externas y flujos de datos) - segun S06
# ===============================================================
def diagrama_contexto():
    import numpy as np
    fig, ax = plt.subplots(figsize=(13, 8.8))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12.4)
    ax.axis("off")

    ax.text(9.0, 12.1, "Diagrama de Contexto - Sistema de Gestión de Pedidos",
            ha="center", va="top", fontsize=11, fontweight="bold", color=AZUL)

    cx, cy, r = 9.0, 6.0, 1.75

    # Entidades externas: (angulo, nombre, flujo hacia el sistema,
    #                       flujo desde el sistema)
    ents = [
        (128, "Cliente", "Consultas,\npedidos y pagos",
         "Estado del pedido\ny confirmación"),
        (180, "Mozo", "Pedidos de\nmesa", "Cuenta y estado\ndel pedido"),
        (232, "Repartidor", "Confirmación de\nentrega",
         "Asignación de\npedidos"),
        (52,  "Chef / Cocina", "Estado de\npreparación",
         "Pedidos por\npreparar"),
        (0,   "Cajero", "Comprobantes\nemitidos", "Cobros y\nboletas"),
        (308, "Administrador", "Configuración\ny consultas",
         "Indicadores\nde gestión"),
        (90,  "Proveedores", "Insumos y\nfacturas",
         "Órdenes de\ncompra"),
        (270, "Pasarela de Pago", "Resultado de la\ntransacción",
         "Solicitud de\npago"),
    ]

    # --- Dibujar flechas primero (quedan debajo de cajas y circulo) ---
    for ang, nombre, flujo_in, flujo_out in ents:
        rad = np.radians(ang)
        dist = 4.9
        ex, ey = cx + dist * np.cos(rad), cy + dist * np.sin(rad)
        e = np.array([np.cos(rad), np.sin(rad)])      # centro -> entidad
        p = np.array([-e[1], e[0]])                   # perpendicular
        circ_in = np.array([cx, cy]) + e * (r + 0.18)
        pos = np.array([ex, ey])
        # Flecha entidad -> sistema (offset +p)
        A = pos + 0.22 * p
        B = circ_in + 0.22 * p
        ax.annotate("", xy=(B[0], B[1]), xytext=(A[0], A[1]),
                    arrowprops=dict(arrowstyle="-|>", color=AZUL, lw=1.5),
                    zorder=2)
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        ax.text(mx + 0.80 * p[0], my + 0.80 * p[1], flujo_in, ha="center",
                va="center", fontsize=7.0, color="#333333", zorder=2,
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec="#BBBBBB", lw=0.6))
        # Flecha sistema -> entidad (offset -p)
        C = circ_in - 0.22 * p
        D = pos - 0.22 * p
        ax.annotate("", xy=(D[0], D[1]), xytext=(C[0], C[1]),
                    arrowprops=dict(arrowstyle="-|>", color=VERDE, lw=1.5),
                    zorder=2)
        mx2, my2 = (C[0] + D[0]) / 2, (C[1] + D[1]) / 2
        ax.text(mx2 - 0.80 * p[0], my2 - 0.80 * p[1], flujo_out, ha="center",
                va="center", fontsize=7.0, color="#333333", zorder=2,
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec="#BBBBBB", lw=0.6))

    # --- Proceso central (sistema como unico proceso) ---
    ax.add_patch(Circle((cx, cy), r, fc="#DCE6F2", ec=AZUL, lw=2.2, zorder=4))
    ax.text(cx, cy + 0.85, "0", fontsize=15, fontweight="bold",
            ha="center", va="center", zorder=5)
    ax.text(cx, cy + 0.12, "Sistema de Gestión", ha="center", va="center",
            fontsize=10.5, fontweight="bold", zorder=5)
    ax.text(cx, cy - 0.48, "de Pedidos", ha="center", va="center",
            fontsize=10.5, fontweight="bold", zorder=5)
    ax.text(cx, cy - 1.15, "Fogón Andino S.A.C.", ha="center", va="center",
            fontsize=8.0, style="italic", color="#333333", zorder=5)

    # --- Entidades externas (rectangulos) por encima de las flechas ---
    for ang, nombre, fi, fo in ents:
        rad = np.radians(ang)
        dist = 4.9
        ex, ey = cx + dist * np.cos(rad), cy + dist * np.sin(rad)
        ax.add_patch(FancyBboxPatch((ex - 1.35, ey - 0.52), 2.7, 1.04,
                                    boxstyle="round,pad=0.08",
                                    fc="white", ec=GRIS_BORDE, lw=1.3,
                                    zorder=5))
        ax.text(ex, ey, nombre, ha="center", va="center", fontsize=8.6,
                fontweight="bold", zorder=6)

    # Leyenda
    ax.plot([12.6, 13.3], [11.35, 11.35], color=AZUL, lw=1.5)
    ax.annotate("", xy=(13.3, 11.35), xytext=(12.6, 11.35),
                arrowprops=dict(arrowstyle="-|>", color=AZUL, lw=1.5))
    ax.text(13.45, 11.35, "Flujo hacia el sistema", fontsize=7.2,
            va="center", ha="left")
    ax.plot([12.6, 13.3], [10.75, 10.75], color=VERDE, lw=1.5)
    ax.annotate("", xy=(13.3, 10.75), xytext=(12.6, 10.75),
                arrowprops=dict(arrowstyle="-|>", color=VERDE, lw=1.5))
    ax.text(13.45, 10.75, "Flujo desde el sistema", fontsize=7.2,
            va="center", ha="left")

    guardar(fig, "fig5_diagrama_contexto.png")


if __name__ == "__main__":
    diagrama_casos_uso()
    diagrama_dominio()
    actividades_local()
    actividades_online()
    diagrama_contexto()
    print("Todos los diagramas generados.")
