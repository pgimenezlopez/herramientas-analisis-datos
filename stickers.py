import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def generar_planilla_pdf(nombre_archivo="Pegatinas_5to_Ano.pdf"):
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho_hoja, alto_hoja = A4
    
    # Listas con los nombres de la imagen
    hoja_1 = ["Facu G", "Facu R", "Juani", "Emi", "Carlotta", "Emma", "Agus B", "Agus L", "Agus N"]
    hoja_2 = ["Sofi J", "Sofi S", "Juanita", "Lucas", "Mateo", "Guille", "Lucas", "Mateo", "Juli","Elo", "Paul"]
    
    # --- CONFIGURACIÓN DE MEDIDAS (Ajustá esto según tu planilla física) ---
    radio = 27.5 * mm         # Radio del sticker (55mm de diámetro total)
    margen_izq = 30 * mm      # Distancia desde el borde izquierdo al centro del 1er sticker
    margen_sup = 250 * mm     # Distancia desde el borde inferior al centro de la 1era fila
    distancia_x = 75 * mm     # Separación horizontal entre los centros de los stickers
    distancia_y = 75 * mm     # Separación vertical entre los centros de los stickers
    
    def dibujar_grilla(nombres):
        # Texto superior
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawCentredString(ancho_hoja / 2, alto_hoja - 15*mm, "Plantilla para Pegatinas de Cumpleaños - 5to Año 2026")
        
        for i, nombre in enumerate(nombres):
            fila = i // 3
            col = i % 3
            
            # Calcular el centro exacto de cada pegatina
            x = margen_izq + (col * distancia_x)
            y = margen_sup - (fila * distancia_y)
            
            # Borde circular celeste
            c.setStrokeColorRGB(0.51, 0.68, 0.83)
            c.setLineWidth(2.5)
            c.circle(x, y, radio)
            
            # Textos internos
            c.setFillColorRGB(0.1, 0.15, 0.22) # Azul oscuro
            
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(x, y + 8*mm, "5to AÑO")
            
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(x, y - 2*mm, nombre)
            
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x, y - 12*mm, "— 2026 —")
            
        c.showPage()
    
    # Generar ambas carillas
    dibujar_grilla(hoja_1)
    dibujar_grilla(hoja_2)
    c.save()
    print(f"¡Planilla generada con éxito! Archivo: {nombre_archivo}")

if __name__ == "__main__":
    generar_planilla_pdf()