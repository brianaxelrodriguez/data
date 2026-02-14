import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx

# Configuración de estilo "Textbook"
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern (estilo LaTeX)


def dibujar_red_flujo():
    # 1. Crear el grafo dirigido
    G = nx.DiGraph()

    # 2. Definir Nodos
    # Fuente (s) y Sumidero (t)
    G.add_node("s", pos=(-2, 0))
    G.add_node("t", pos=(5, 0))

    # Nodos del conjunto A (x = 0)
    nodos_A = ["a1", "a2", "a3", "a4"]
    pos_A = [(0, 1.5), (0, 0.5), (0, -0.5), (0, -1.5)]
    for n, p in zip(nodos_A, pos_A):
        G.add_node(n, pos=p)

    # Nodos del conjunto B (x = 3)
    nodos_B = ["b1", "b2", "b3", "b4"]
    pos_B = [(3, 1.5), (3, 0.5), (3, -0.5), (3, -1.5)]
    for n, p in zip(nodos_B, pos_B):
        G.add_node(n, pos=p)

    # 3. Definir Aristas (Flechas)
    # De s a todos los de A
    for a in nodos_A:
        G.add_edge("s", a)

    # De todos los de B a t
    for b in nodos_B:
        G.add_edge(b, "t")

    # Aristas entre A y B (algunas aleatorias para el ejemplo)
    edges_intermedios = [
        ("a1", "b1"),
        ("a1", "b2"),
        ("a2", "b2"),
        ("a2", "b3"),
        ("a2", "b1"),
        ("a3", "b3"),
        ("a3", "b4"),
        ("a4", "b4"),
        ("a4", "b2"),
    ]
    G.add_edges_from(edges_intermedios)

    # 4. Extraer posiciones para dibujar
    pos = nx.get_node_attributes(G, "pos")

    # --- DIBUJO ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # Dibujar nodos (pequeños puntos negros)
    nx.draw_networkx_nodes(G, pos, node_size=150, node_color="black", ax=ax)

    # Dibujar etiquetas s y t
    # Usamos offset para que la letra no quede encima del punto
    ax.text(-2.3, 0, "$s$", fontsize=20, ha="right", va="center")
    ax.text(5.3, 0, "$t$", fontsize=20, ha="left", va="center")

    # Dibujar aristas (flechas)
    # connectionstyle='arc3, rad=0.1' le da esa curvatura suave típica de los libros
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="black",
        width=1.5,
        arrowstyle="-|>",
        arrowsize=15,
        connectionstyle="arc3,rad=0.05",
        ax=ax,
    )

    # 5. Dibujar los Elipses (Conjuntos A y B)
    # Elipse para A
    ellipse_A = patches.Ellipse(
        (0, 0),
        width=1.5,
        height=4.5,
        angle=0,
        edgecolor="black",
        facecolor="none",
        lw=1.5,
    )
    ax.add_patch(ellipse_A)
    ax.text(0, 2.5, "$A$", fontsize=18, ha="center")  # Etiqueta A

    # Elipse para B
    ellipse_B = patches.Ellipse(
        (3, 0),
        width=1.5,
        height=4.5,
        angle=0,
        edgecolor="black",
        facecolor="none",
        lw=1.5,
    )
    ax.add_patch(ellipse_B)
    ax.text(3, 2.5, "$B$", fontsize=18, ha="center")  # Etiqueta B

    # Ajustes finales
    plt.axis("off")  # Quitar ejes cartesianos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    dibujar_red_flujo()
