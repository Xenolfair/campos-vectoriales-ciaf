import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Integrantes: Miguel Angel Ballesteros  Grupo: 7mo Semestre Ingenieria Software CIAF 2026

# ============================================================
# FIGURA 1: Campo vectorial + curva (Ejercicio 1 - Green)
# ============================================================
def figura_green():
    """
    Genera la figura del campo vectorial F=(x^2-y^3, x^3+y^2) con el
    circulo x^2+y^2=4 superpuesto.

    Grafica el campo vectorial coloreado por magnitud, el circulo
    en rojo y una flecha indicando la direccion antihoraria.

    Retorna:
        None. Guarda fig_green.png en el directorio actual.
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    # Malla de puntos
    x = np.linspace(-2.8, 2.8, 18)
    y = np.linspace(-2.8, 2.8, 18)
    X, Y = np.meshgrid(x, y)

    # Campo F = (x^2 - y^3,  x^3 + y^2)
    U = X**2 - Y**3
    V = X**3 + Y**2
    magnitud = np.sqrt(U**2 + V**2)

    # Quiver coloreado por magnitud
    q = ax.quiver(X, Y, U/magnitud, V/magnitud, magnitud,
                  cmap='viridis', scale=22, width=0.004, alpha=0.85)
    cbar = fig.colorbar(q, ax=ax, shrink=0.85)
    cbar.set_label('|F|', fontsize=11)

    # Circulo x^2 + y^2 = 4 (R=2) en rojo
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(2*np.cos(theta), 2*np.sin(theta), 'r-', linewidth=2.5,
            label=r'$x^2+y^2=4$')

    # Flecha antihoraria en el circulo (angulo 45 grados)
    t0 = np.pi / 4
    ax.annotate('', xy=(2*np.cos(t0+0.25), 2*np.sin(t0+0.25)),
                xytext=(2*np.cos(t0), 2*np.sin(t0)),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.2))
    ax.text(1.7, 1.85, 'antihorario', color='red', fontsize=9)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.set_title(r'Campo vectorial $\mathbf{F}=(x^2-y^3,\; x^3+y^2)$ — Teorema de Green',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.savefig('fig_green.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("[OK] fig_green.png guardada.")


# ============================================================
# FIGURA 2: Curvas de nivel + gradiente (Ejercicio 2 - Conservativo)
# ============================================================
def figura_potencial():
    """
    Genera la figura de curvas de nivel de phi(x,y)=x^2*y y su gradiente.

    Muestra las curvas de nivel con contourf/contour, el campo gradiente
    nabla(phi)=(2xy, x^2) con quiver, y marca los puntos A=(0,0) y B=(1,2).

    Retorna:
        None. Guarda fig_potencial.png en el directorio actual.
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    x = np.linspace(-2, 2, 300)
    y = np.linspace(-1, 3, 300)
    X, Y = np.meshgrid(x, y)

    # Funcion potencial phi(x,y) = x^2 * y
    PHI = X**2 * Y

    # Curvas de nivel rellenas y contorno
    niveles = np.linspace(-4, 4, 25)
    cf = ax.contourf(X, Y, PHI, levels=niveles, cmap='RdYlBu_r', alpha=0.75)
    cs = ax.contour(X, Y, PHI, levels=niveles[::3], colors='k', linewidths=0.8, alpha=0.6)
    ax.clabel(cs, inline=True, fontsize=8, fmt='%.1f')
    cbar = fig.colorbar(cf, ax=ax, shrink=0.85)
    cbar.set_label(r'$\varphi(x,y)=x^2 y$', fontsize=11)

    # Campo gradiente nabla(phi) = (2xy, x^2)
    xg = np.linspace(-2, 2, 14)
    yg = np.linspace(-1, 3, 14)
    XG, YG = np.meshgrid(xg, yg)
    dPHI_dx = 2 * XG * YG
    dPHI_dy = XG**2
    mag_g = np.sqrt(dPHI_dx**2 + dPHI_dy**2)
    mag_g[mag_g == 0] = 1  # evitar division por cero
    ax.quiver(XG, YG, dPHI_dx/mag_g, dPHI_dy/mag_g,
              color='navy', scale=20, width=0.004,
              alpha=0.8, label=r'$\nabla\varphi=(2xy,\,x^2)$')

    # Puntos A y B
    ax.plot(0, 0, 'g*', markersize=16, label='A=(0,0)', zorder=5)
    ax.plot(1, 2, 'm*', markersize=16, label='B=(1,2)', zorder=5)
    ax.annotate('A=(0,0)', xy=(0, 0), xytext=(0.15, 0.25),
                fontsize=10, color='green', fontweight='bold')
    ax.annotate('B=(1,2)', xy=(1, 2), xytext=(1.15, 2.2),
                fontsize=10, color='purple', fontweight='bold')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 3)
    ax.set_title(r'Curvas de nivel de $\varphi=x^2 y$ y gradiente — Campo Conservativo',
                 fontsize=11, fontweight='bold')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.savefig('fig_potencial.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("[OK] fig_potencial.png guardada.")


# ============================================================
# FIGURA 3: Superficie 3D + borde (Ejercicio 3 - Stokes)
# ============================================================
def figura_stokes():
    """
    Genera la figura 3D del disco z=0, x^2+y^2<=4 con su borde y vector normal.

    Muestra el disco semitransparente como superficie, el circulo borde
    en rojo y el vector normal n=k desde el centro del disco.

    Retorna:
        None. Guarda fig_stokes.png en el directorio actual.
    """
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')

    R = 2.0

    # Disco z=0, x^2+y^2 <= R^2 (superficie semitransparente)
    r_vals = np.linspace(0, R, 40)
    theta_vals = np.linspace(0, 2*np.pi, 80)
    r_grid, theta_grid = np.meshgrid(r_vals, theta_vals)
    X_disk = r_grid * np.cos(theta_grid)
    Y_disk = r_grid * np.sin(theta_grid)
    Z_disk = np.zeros_like(X_disk)

    ax.plot_surface(X_disk, Y_disk, Z_disk,
                    color='cyan', alpha=0.35,
                    edgecolor='none',
                    label='Disco $x^2+y^2 \leq 4$, $z=0$')

    # Borde C: circulo x^2+y^2=R^2, z=0 en rojo
    theta_c = np.linspace(0, 2*np.pi, 300)
    xc = R * np.cos(theta_c)
    yc = R * np.sin(theta_c)
    zc = np.zeros_like(theta_c)
    ax.plot(xc, yc, zc, 'r-', linewidth=2.5, label=r'Borde $C$: $x^2+y^2=4$')

    # Flecha antihoraria sobre el borde
    t0 = np.pi / 4
    ax.quiver(R*np.cos(t0), R*np.sin(t0), 0,
              -np.sin(t0)*0.5, np.cos(t0)*0.5, 0,
              color='red', linewidth=2, arrow_length_ratio=0.4)

    # Vector normal n = k desde el centro
    ax.quiver(0, 0, 0, 0, 0, 1.5,
              color='darkgreen', linewidth=3,
              arrow_length_ratio=0.2,
              label=r'Normal $\mathbf{n}=\mathbf{k}$')
    ax.text(0.1, 0.1, 1.6, 'n = k', color='darkgreen', fontsize=11, fontweight='bold')

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-0.3, 2.0)
    ax.set_title(r'Disco $x^2+y^2\leq 4$, $z=0$ — Teorema de Stokes',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.set_zlabel('z', fontsize=11)
    ax.legend(loc='upper left', fontsize=9)

    plt.savefig('fig_stokes.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("[OK] fig_stokes.png guardada.")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Generando figuras para el Parcial Final - Calculo Multivariado")
    print("=" * 60)
    figura_green()
    figura_potencial()
    figura_stokes()
    print("=" * 60)
    print("Listo. Se generaron: fig_green.png, fig_potencial.png, fig_stokes.png")
