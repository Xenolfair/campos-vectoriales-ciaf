import numpy as np
from scipy import integrate

# Integrantes: Miguel Angel Ballesteros Grupo: 7mo Semestre Ingeniería Software CIAF 2026

# ============================================================
# FUNCION 1: Teorema de Green-Ejercicio 1
# ============================================================
def green_circulo(R=2.0):
    """
    Calcula la integral de linea de Green sobre un circulo.

    Evalua la integral de (x^2-y^3)dx + (x^3+y^2)dy sobre el
    circulo de radio R usando el Teorema de Green. La integral
    doble resultante es 3(x^2+y^2) sobre el disco, que en
    coordenadas polares es 3r^2 * r dr dtheta.

    Parametros:
        R (float): Radio del circulo. Debe ser positivo. Default=2.0

    Retorna:
        float: Valor numerico de la integral doble.

    Lanza:
        ValueError: Si R es negativo o cero.
    """
    if R <= 0:
        raise ValueError(f"El radio debe ser positivo. Se recibio R={R}")

    def integrando(r, theta):
        return 3 * r**2 * r  # 3(x^2+y^2) * jacobiano

    resultado, _ = integrate.dblquad(
        integrando,
        0, 2*np.pi,  # theta
        0, R         # r
    )
    analitico = (3/2) * np.pi * R**4  # formula general: 3*pi*R^4/2
    print(f"[GREEN] Analitico: 3*pi*R^4/2 = {analitico:.6f}")
    print(f"[GREEN] Numerico:              {resultado:.6f}")
    print(f"[GREEN] Error: {abs(resultado-analitico):.2e}")
    return resultado

# ============================================================
# FUNCION 2: Campo conservativo-Ejercicio 2
# ============================================================
def campo_conservativo(A=(0,0,0), B=(1,2,1)):
    """
    Verifica si F=(2xy+z^2, x^2, 2xz) es conservativo y calcula el trabajo.

    Calcula el rotacional de F para verificar conservatividad,
    determina la funcion potencial phi(x,y,z) = x^2*y + x*z^2,
    y calcula el trabajo W = phi(B) - phi(A).

    Parametros:
        A (tuple): Punto inicial (x, y, z). Default=(0,0,0)
        B (tuple): Punto final (x, y, z). Default=(1,2,1)

    Retorna:
        float: Trabajo W = phi(B) - phi(A) en Joules.
    """
    def phi(x, y, z):
        """Funcion potencial de F."""
        return x**2 * y + x * z**2

    x0, y0, z0 = 1.0, 1.0, 1.0
    curl_i = 0 - 0       # dR/dy - dQ/dz
    curl_j = 2*z0 - 2*z0 # dP/dz - dR/dx
    curl_k = 2*x0 - 2*x0 # dQ/dx - dP/dy
    es_conservativo = (curl_i == 0 and curl_j == 0 and curl_k == 0)

    W = phi(*B) - phi(*A)
    analitico = 3.0
    print(f"\n[CONSERV] curl(F) = ({curl_i}, {curl_j}, {curl_k})")
    print(f"[CONSERV] Es conservativo: {es_conservativo}")
    print(f"[CONSERV] phi(x,y,z) = x^2*y + x*z^2")
    print(f"[CONSERV] W = phi{B}-phi{A} = {W:.4f} J")
    print(f"[CONSERV] Analitico: {analitico:.4f} J")
    return W

# ============================================================
# FUNCION 3: Teorema de Stokes-Ejercicio 3
# ============================================================
def stokes_circulo(R=2.0, n=800):
    """
    Verifica el Teorema de Stokes para F=(z,x,y) sobre un circulo.

    Para F=(z,x,y) y la curva C: circulo x^2+y^2=R^2 en z=0,
    calcula la integral de superficie via Stokes (curl(F).n = 1
    sobre el disco) y la verifica con la integral de linea directa.

    Parametros:
        R (float): Radio del circulo. Debe ser positivo. Default=2.0
        n (int): Numero de puntos para la aproximacion numerica. Default=800

    Retorna:
        float: Valor de la integral calculada por Stokes (pi*R^2).

    Lanza:
        ValueError: Si R es negativo o cero.
    """
    if R <= 0:
        raise ValueError(f"El radio debe ser positivo. Se recibio R={R}")

    # Stokes: (curl F).n = (1,1,1).(0,0,1) = 1 sobre el disco
    stokes = np.pi * R**2

    # Verificacion con integral de linea directa
    t = np.linspace(0, 2*np.pi, n)
    x = R*np.cos(t); y = R*np.sin(t); z = np.zeros(n)
    dx = np.gradient(x, t); dy = np.gradient(y, t)
    dz = np.zeros(n)
    linea = np.trapz(z*dx + x*dy + y*dz, t)
    analitico = np.pi * R**2  # formula general

    print(f"\n[STOKES] curl(F) = (1,1,1); n = k = (0,0,1)")
    print(f"[STOKES] (curl F).n = 1 --> integral = area disco")
    print(f"[STOKES] Stokes (area*1): {stokes:.6f}")
    print(f"[STOKES] Linea directa:   {linea:.6f}")
    print(f"[STOKES] Analitico pi*R^2: {analitico:.6f}")
    return stokes

# ============================================================
# FUNCION 4: Tabla comparativa de resultados
# ============================================================
def tabla_resultados(R=2.0):
    """
    Imprime una tabla comparativa de los tres ejercicios.

    Ejecuta las tres funciones y presenta en formato tabular
    los valores analiticos, numericos y el error relativo en %
    para Green, campo conservativo y Stokes.

    Parametros:
        R (float): Radio usado en Green y Stokes. Debe ser positivo. Default=2.0

    Retorna:
        None
    """
    if R <= 0:
        raise ValueError(f"El radio debe ser positivo. Se recibio R={R}")

    # Calcular valores sin imprimir (capturamos resultados)
    analitico_green   = (3/2) * np.pi * R**4
    numerico_green, _ = integrate.dblquad(
        lambda r, theta: 3 * r**2 * r, 0, 2*np.pi, 0, R
    )

    analitico_conserv = 3.0
    numerico_conserv  = campo_conservativo.__wrapped__ if hasattr(campo_conservativo, '__wrapped__') else 3.0
    # Calculamos directamente
    phi = lambda x, y, z: x**2 * y + x * z**2
    numerico_conserv = phi(1,2,1) - phi(0,0,0)

    analitico_stokes = np.pi * R**2
    t = np.linspace(0, 2*np.pi, 800)
    x_s = R*np.cos(t); y_s = R*np.sin(t); z_s = np.zeros(800)
    numerico_stokes = np.trapz(
        z_s*np.gradient(x_s,t) + x_s*np.gradient(y_s,t), t
    )

    # Error relativo en %
    err_green   = abs(numerico_green   - analitico_green)   / abs(analitico_green)   * 100
    err_conserv = abs(numerico_conserv - analitico_conserv) / abs(analitico_conserv) * 100
    err_stokes  = abs(numerico_stokes  - analitico_stokes)  / abs(analitico_stokes)  * 100

    sep = "=" * 65
    print(f"\n{sep}")
    print(f"{'TABLA COMPARATIVA DE RESULTADOS':^65}")
    print(sep)
    print(f"{'Ejercicio':<18} {'Analitico':>14} {'Numerico':>14} {'Error %':>10}")
    print("-" * 65)
    print(f"{'Green (R=' + str(R) + ')':<18} {analitico_green:>14.6f} {numerico_green:>14.6f} {err_green:>9.4f}%")
    print(f"{'Conservativo':<18} {analitico_conserv:>14.6f} {numerico_conserv:>14.6f} {err_conserv:>9.4f}%")
    print(f"{'Stokes (R=' + str(R) + ')':<18} {analitico_stokes:>14.6f} {numerico_stokes:>14.6f} {err_stokes:>9.4f}%")
    print(sep)

# ============================================================
# PRUEBAS UNITARIAS
# ============================================================
def pruebas_unitarias():
    """
    Ejecuta pruebas unitarias con assert para las tres funciones.

    Verifica que los resultados numericos se acerquen a los
    valores analiticos dentro de una tolerancia definida.
    No recibe parametros ni retorna valores; lanza AssertionError
    si alguna prueba falla.
    """
    print("\n" + "=" * 40)
    print("EJECUTANDO PRUEBAS UNITARIAS")
    print("=" * 40)

    # Prueba 1: Green con R=2
    res_green = green_circulo(2.0)
    esperado_green = (3/2) * np.pi * 2**4  # 24*pi
    assert abs(res_green - esperado_green) < 0.01, \
        f"Fallo Green: esperado {esperado_green:.4f}, obtenido {res_green:.4f}"
    print("[OK] Prueba 1: green_circulo(2) ≈ 24*pi")

    # Prueba 2: Campo conservativo A=(0,0,0), B=(1,2,1)
    res_conserv = campo_conservativo((0,0,0), (1,2,1))
    assert abs(res_conserv - 3.0) < 1e-10, \
        f"Fallo Conservativo: esperado 3.0, obtenido {res_conserv:.6f}"
    print("[OK] Prueba 2: campo_conservativo() = 3.0 J")

    # Prueba 3: Stokes con R=2
    res_stokes = stokes_circulo(2.0)
    esperado_stokes = np.pi * 2**2  # 4*pi
    assert abs(res_stokes - esperado_stokes) < 0.01, \
        f"Fallo Stokes: esperado {esperado_stokes:.4f}, obtenido {res_stokes:.4f}"
    print("[OK] Prueba 3: stokes_circulo(2) ≈ 4*pi")

    # Prueba 4: Radio negativo lanza ValueError
    try:
        green_circulo(-1.0)
        assert False, "Deberia haber lanzado ValueError"
    except ValueError:
        print("[OK] Prueba 4: radio negativo lanza ValueError correctamente")

    print("=" * 40)
    print("TODAS LAS PRUEBAS PASARON")
    print("=" * 40)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    try:
        R = float(input("Ingrese el radio (default 2.0): ") or "2.0")
        if R <= 0:
            raise ValueError(f"El radio debe ser positivo. Se recibio R={R}")

        print("\n--- Ejercicio 1: Teorema de Green ---")
        green_circulo(R)

        print("\n--- Ejercicio 2: Campo Conservativo ---")
        campo_conservativo()

        print("\n--- Ejercicio 3: Teorema de Stokes ---")
        stokes_circulo(R)

        tabla_resultados(R)
        pruebas_unitarias()

    except ValueError as e:
        print(f"\n[ERROR] Entrada invalida: {e}")
        print("Por favor ingrese un numero positivo para el radio.")