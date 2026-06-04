from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

OUTPUT = "informe.pdf"

def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=14,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=colors.HexColor('#1a5276'),
        spaceBefore=8, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=13,
        spaceAfter=3
    )
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#555555')
    )

    story = []

    # Encabezado
    story.append(Paragraph(
        "Informe Parcial Final — Calculo Multivariado", title_style
    ))
    story.append(Paragraph(
        "Miguel Angel Ballesteros &nbsp;|&nbsp; 7mo Semestre Ingenieria de Software &nbsp;|&nbsp; CIAF 2026-1",
        small_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5,
                             color=colors.HexColor('#1a5276'), spaceAfter=8))

    # ---- Seccion 1: Resumen de resultados ----
    story.append(Paragraph("1. Resumen de los 3 resultados", h2_style))

    tabla_data = [
        ["Ejercicio", "Teorema", "Valor Analitico", "Valor Numerico", "Error %"],
        ["Ejercicio 1", "Green",
         "24π ≈ 75.3982", "75.3982", "< 0.001%"],
        ["Ejercicio 2", "Campo Conservativo",
         "W = 3.0000 J", "3.0000 J", "0.0000%"],
        ["Ejercicio 3", "Stokes",
         "4π ≈ 12.5664", "12.5621", "< 0.04%"],
    ]
    tabla = Table(tabla_data, colWidths=[3.2*cm, 4*cm, 4*cm, 3.8*cm, 2.5*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.HexColor('#eaf2ff'), colors.white]),
        ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#aaaaaa')),
        ('ALIGN',        (2,1), (-1,-1), 'CENTER'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "El Teorema de Green convierte una integral de linea cerrada en una integral doble "
        "usando Q<sub>x</sub> - P<sub>y</sub> = 3(x<super>2</super>+y<super>2</super>), "
        "que en polares da (3/2)piR<super>4</super>. "
        "El campo F=(2xy+z<super>2</super>, x<super>2</super>, 2xz) es conservativo "
        "(curl F = 0) con potencial phi=x<super>2</super>y+xz<super>2</super>, "
        "permitiendo calcular el trabajo solo con los extremos. "
        "Para Stokes, curl(F)=(1,1,1) con normal k da una integral igual al area del disco piR<super>2</super>, "
        "verificada por integracion numerica de la linea.",
        body_style
    ))

    # ---- Seccion 2: Aplicacion en software ----
    story.append(Paragraph("2. Aplicacion en proyectos de software", h2_style))
    apps = [
        ("<b>Motores de fisica (videojuegos/simulacion):</b> El calculo de trabajo "
         "mediante campos conservativos se usa en simuladores de particulas y motores "
         "como Unity Physics o Bullet para determinar energia potencial sin integrar trayectorias."),
        ("<b>Graficos 3D y rendering:</b> El Teorema de Stokes aparece en el calculo "
         "de normales de superficies y flujo de luz en shaders (ej. irradiance maps). "
         "La integral de superficie se reduce a una integral de contorno mas eficiente."),
        ("<b>Vision computacional y geometria computacional:</b> El Teorema de Green "
         "calcula areas de poligonos arbitrarios en O(n), base de algoritmos como "
         "el calculo de area en OpenCV o CGAL."),
        ("<b>CFD y simulacion de fluidos:</b> Los tres teoremas son el fundamento "
         "matematico de solvers de ecuaciones de Navier-Stokes usados en software "
         "como OpenFOAM para modelar flujo de fluidos en ingenieria."),
    ]
    for item in apps:
        story.append(Paragraph(f"&bull; {item}", body_style))

    # ---- Seccion 3: Dificultades ----
    story.append(Paragraph("3. Dificultades encontradas y soluciones", h2_style))
    difs = [
        ("<b>Orden de limites en dblquad:</b> scipy.integrate.dblquad recibe "
         "primero el limite de la variable exterior (theta) y luego el interior (r), "
         "al contrario de la notacion matematica. Se resolvio revisando la documentacion "
         "y verificando con el valor analitico."),
        ("<b>Valor analitico de Green:</b> El enunciado tenia hardcodeado 24*pi solo "
         "para R=2. Se generalizo a la formula (3/2)*pi*R<super>4</super> para que "
         "las pruebas unitarias funcionen con cualquier radio."),
        ("<b>Precision de la integral de linea en Stokes:</b> np.trapz introduce "
         "error de discretizacion en el borde circular. Se aumento n=800 puntos "
         "para reducir el error relativo por debajo del 0.04%."),
        ("<b>Visualizacion 3D semitransparente:</b> mpl_toolkits.mplot3d no soporta "
         "transparencia real en plot_surface con todos los backends. Se uso alpha=0.35 "
         "y se valido visualmente que el borde rojo fuera visible sobre el disco."),
    ]
    for item in difs:
        story.append(Paragraph(f"&bull; {item}", body_style))

    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#aaaaaa'), spaceBefore=8))
    story.append(Paragraph(
        "Repositorio: github.com/[usuario]/campos-vectoriales-ciaf &nbsp;|&nbsp; "
        "Lenguaje: Python 3.x &nbsp;|&nbsp; Librerias: NumPy, SciPy, Matplotlib",
        small_style
    ))

    doc.build(story)
    print(f"[OK] {OUTPUT} generado.")

if __name__ == "__main__":
    build()
