import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from io import BytesIO

def check_regex(regex, value):
    x = re.fullmatch(regex, value)
    return x


def prescription_letter(data):
    buffer = BytesIO()  
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setStrokeColorCMYK(0.97, 0.42, 0, 0)
    p.setLineWidth(2)
    p.drawImage("doctor_portal/icon3.png", x = 430, y = 710, width=130, height=130)
    p.line(0, 710, 600, 710)
    p.setFillColorCMYK(0.97, 0.42, 0, 0)
    p.setFont("Helvetica-Bold", 35)
    p.drawCentredString(x=200,y=780,text= "Dr Mukesh Ranjan")
    p.setFont('Helvetica',15)
    p.drawCentredString(x=90,y=760,text= "Nephrologist")

    text = p.beginText()
    text.setFillColor(aColor='black')
    text.setCharSpace(0.9)  
    text.setFont('Helvetica-Bold',10)
    text.setTextOrigin(50, 680)
    text.textLine(f'Name: __________________________________________')
    text.textLine(" ")
    text.textLine(f'Phone Number: _____________________ ')
    text.textLine(" ")
    text.textLine(f'Diagnosis:___________________________________________________________________')
    text.textLine(" ")
    p.drawText(text)
    p.setFillColor(aColor='black')
    p.setFont('Helvetica-Bold',10)
    p.drawCentredString(x=452,y=680, text="Date: _______________________",charSpace=0.9)
    p.drawCentredString(x=345,y=655,text="Gender:______________",charSpace=0.9)
    p.drawCentredString(x=479,y=655,text="Weight:_____________",charSpace=0.9)

    p.drawImage("doctor_portal/rximage.avif", x = 30, y = 500, width=80, height=80)

    p.setStrokeColorCMYK(0.97, 0.42, 0, 0)
    p.line(0, 50, 600, 50)
    p.setLineWidth(2)

    p.setStrokeColorCMYK(0.51, 0.22, 0, 0.55)
    p.setFont('Courier', 17)
    p.drawCentredString(x=100,y=20,text="Nano Health",charSpace=0.9)
    p.setFont('Helvetica', 13)

    p.drawImage("doctor_portal/location_icon.png", x = 331, y = 17, width=15, height=15)
    p.drawCentredString(x=450,y=20,text="Near KIET Goup of Institutions",charSpace=0.9)
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer,as_attachment=True, filename='prescription.pdf')

