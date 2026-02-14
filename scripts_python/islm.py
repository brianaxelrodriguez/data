import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

# --- CONFIGURACIÓN ECONÓMICA ---
Cy, Iy, Ii = 0.45, 0.1, -25
Ly, Li = 0.35, -40
T, I0, L0 = 200, 400, 200

Y_range = np.linspace(0, 6000, 2000)
M_range = np.linspace(0, 4000, 2000)

fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2, figsize=(15, 9))
plt.subplots_adjust(bottom=0.25, hspace=0.4, wspace=0.3)

# --- VALORES INICIALES (Referencia Ms=700, G=500) ---
G_init = 500
i_init = 15.0  # Tasa inicial de partida

# --- OBJETOS DINÁMICOS ---
(line_da,) = ax12.plot([], [], "forestgreen", lw=3)
line_ms = ax21.axvline(0, color="blue", lw=3, label="Ms (Endógena)")
(line_md,) = ax21.plot([], [], "crimson", lw=3, label="Md")
(line_is,) = ax22.plot([], [], "red", lw=3)
(line_lm,) = ax22.plot([], [], "blue", lw=3)  # Horizontal (i-target)
(point_eq,) = ax22.plot([], [], "black", marker="o", markersize=10, zorder=10)

# Proyecciones
proj_y_goods = ax12.axvline(0, color="black", ls=":", alpha=0.5)
proj_y_islm = ax22.axvline(0, color="black", ls=":", alpha=0.5)
proj_i_islm = ax22.axhline(0, color="black", ls=":", alpha=0.5)
proj_i_money = ax21.axhline(0, color="black", ls=":", alpha=0.5)

ax12.set_title("MERCADO DE BIENES")
ax21.set_title("MERCADO DE DINERO")
ax22.set_title("MODELO IS-LM")
ax12.plot(Y_range, Y_range, "k-", alpha=0.1)

text_stats = ax11.text(
    0.05,
    0.95,
    "",
    transform=ax11.transAxes,
    verticalalignment="top",
    family="monospace",
    fontweight="bold",
)
ax11.axis("off")

# --- SLIDERS (G y Tasa de Interés i como instrumento) ---
s_g = Slider(plt.axes([0.15, 0.12, 0.25, 0.03]), "Gasto (G)", 100, 1000, valinit=G_init)
s_i = Slider(plt.axes([0.15, 0.07, 0.25, 0.03]), "Tasa BC (i)", 1.0, 40, valinit=i_init)


def update(val):
    G_act = s_g.val
    i_target = s_i.val

    # 1. RESOLUCIÓN MODERNA (i es el ancla)
    # De la IS: Y = [C(-T) + I(i) + G] / (1 - Cy - Iy)
    Y_eq = (G_act + I0 - Cy * T + Ii * i_target) / (1 - Cy - Iy)
    Y_eq = max(0, Y_eq)

    # 2. MERCADO DE DINERO: La Oferta se ajusta a la Demanda (Ms = Md)
    # Ms = L0 + Ly*Y + Li*i
    Ms_endogena = L0 + Ly * Y_eq + Li * i_target
    Ms_endogena = max(100, Ms_endogena)

    # ACTUALIZACIÓN DE GRÁFICOS
    # Mercado de Bienes
    line_da.set_data(
        Y_range, (Cy + Iy) * Y_range + (I0 + G_act - Cy * T + Ii * i_target)
    )
    proj_y_goods.set_xdata([Y_eq, Y_eq])

    # Mercado de Dinero (La Ms "salta" para interceptar a la Md en i_target)
    line_ms.set_xdata([Ms_endogena, Ms_endogena])
    line_md.set_data(M_range, (M_range - L0 - Ly * Y_eq) / Li)
    proj_i_money.set_ydata([i_target, i_target])

    # IS-LM
    line_is.set_data(Y_range, (Y_range * (1 - Cy - Iy) + Cy * T - G_act - I0) / Ii)
    line_lm.set_data(
        Y_range, np.full_like(Y_range, i_target)
    )  # LM horizontal en i_target

    point_eq.set_data([Y_eq], [i_target])
    proj_y_islm.set_xdata([Y_eq, Y_eq])
    proj_i_islm.set_ydata([i_target, i_target])

    # Monitor de Variables (Estado del Sistema)
    stats = (
        f"ESTADO DEL SISTEMA (i-Targeting)\n"
        f"---------------------------------\n"
        f"Producto (Y)     : {Y_eq:.1f}\n"
        f"Tasa BC (i)      : {i_target:.2f}%\n"
        f"Oferta Mon. (Ms) : {Ms_endogena:.1f} (Acomodaticia)\n"
        f"Demanda Mon. (Md): {L0 + Ly * Y_eq + Li * i_target:.1f}\n"
        f"Inversión (I)    : {max(0, I0 + Iy * Y_eq + Ii * i_target):.1f}\n"
        f"Gasto (G)        : {G_act:.1f}"
    )
    text_stats.set_text(stats)

    for ax in [ax12, ax21, ax22]:
        ax.set_xlim(0, 5000)
        ax.set_ylim(0, 50 if ax != ax12 else 5000)
    fig.canvas.draw_idle()


# --- SHOCKS Y ANIMACIÓN ---
anims = {"G": {"active": False, "step": 0}, "i": {"active": False, "step": 0}}


def animate_master(frame):
    for k in anims:
        if anims[k]["active"]:
            anims[k]["step"] += 1
            if k == "G":
                s_g.set_val(G_init + 300 * np.sin(anims[k]["step"] * 0.05))
            else:
                s_i.set_val(i_init + 10 * np.sin(anims[k]["step"] * 0.05))


btn_g = Button(plt.axes([0.45, 0.02, 0.1, 0.04]), "Shock G")
btn_i = Button(plt.axes([0.56, 0.02, 0.1, 0.04]), "Shock i")
btn_pause = Button(plt.axes([0.67, 0.02, 0.1, 0.04]), "PAUSE")
btn_reset = Button(plt.axes([0.78, 0.02, 0.12, 0.04]), "RESET")

btn_g.on_clicked(lambda e: anims["G"].update({"active": not anims["G"]["active"]}))
btn_i.on_clicked(lambda e: anims["i"].update({"active": not anims["i"]["active"]}))
btn_pause.on_clicked(lambda e: [anims[k].update({"active": False}) for k in anims])
btn_reset.on_clicked(lambda e: [s_g.set_val(G_init), s_i.set_val(i_init)])

s_g.on_changed(update)
s_i.on_changed(update)
ani = animation.FuncAnimation(fig, animate_master, interval=30, cache_frame_data=False)
update(None)
plt.show()
