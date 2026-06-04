import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from vector_engine import green_circulo, campo_conservativo, stokes_circulo

# ============================================================
# PRUEBAS UNITARIAS - vector_engine.py
# ============================================================

def test_green_circulo_radio_2():
    """Green con R=2 debe aproximarse a (3/2)*pi*2^4 = 24*pi."""
    resultado = green_circulo(2.0)
    esperado = (3/2) * np.pi * 2**4
    assert abs(resultado - esperado) < 0.01, (
        f"Green R=2: esperado {esperado:.4f}, obtenido {resultado:.4f}"
    )

def test_green_circulo_radio_1():
    """Green con R=1 debe aproximarse a (3/2)*pi."""
    resultado = green_circulo(1.0)
    esperado = (3/2) * np.pi
    assert abs(resultado - esperado) < 0.01, (
        f"Green R=1: esperado {esperado:.4f}, obtenido {resultado:.4f}"
    )

def test_campo_conservativo_trabajo():
    """Trabajo de A=(0,0,0) a B=(1,2,1) debe ser 3.0 J."""
    resultado = campo_conservativo((0, 0, 0), (1, 2, 1))
    assert abs(resultado - 3.0) < 1e-10, (
        f"Conservativo: esperado 3.0, obtenido {resultado:.6f}"
    )

def test_campo_conservativo_trabajo_cero():
    """Trabajo de un punto a si mismo debe ser 0."""
    resultado = campo_conservativo((1, 1, 1), (1, 1, 1))
    assert abs(resultado) < 1e-10, (
        f"Trabajo A->A: esperado 0, obtenido {resultado:.6f}"
    )

def test_stokes_circulo_radio_2():
    """Stokes con R=2 debe ser pi*R^2 = 4*pi."""
    resultado = stokes_circulo(2.0)
    esperado = np.pi * 2**2
    assert abs(resultado - esperado) < 0.01, (
        f"Stokes R=2: esperado {esperado:.4f}, obtenido {resultado:.4f}"
    )

def test_green_radio_negativo():
    """Radio negativo debe lanzar ValueError."""
    with pytest.raises(ValueError):
        green_circulo(-1.0)

def test_stokes_radio_negativo():
    """Radio negativo debe lanzar ValueError."""
    with pytest.raises(ValueError):
        stokes_circulo(-3.0)
