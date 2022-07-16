#!/usr/bin/python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class Report:
    months_str = ['Styczen', 'Luty', 'Marzec', 'Kwiecien', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpien', 'Wrzesien', 'Pazdziernik', 'Listopad', 'Grudzien' ]
    filename_str=''
    title_str = ''
    headerstr=''
    cw_unit='m M^3'
    hw_unit='m M^3'
    co_unit='MJ'
    data=[['Numer mieszkania', 'Woda zimna ('+cw_unit+')', 'Woda ciepla ('+hw_unit+')', 'Ogrzewanie ('+co_unit+')']]
    elements = [Spacer(1, 4*cm)]

    def __init__(self, data):

        styleSheet = getSampleStyleSheet()
        P = Paragraph(''+self.headerstr+'',
            styleSheet["BodyText"])
        self.elements.append(P)
        self.elements.append(Spacer(1, 1*cm))

        month = data[0]
        year = data[1]
        self.filename_str='rozliczenie_'+str(month)+'_'+str(year)+'.pdf'
        self.title_str = 'Rozliczenie ' + str(month) + '.' + str(year)
        self.headerstr='Stan licznikow na koniec miesiaca: ' + self.months_str[month-1] + ' ' + str(year) + 'r.'
        self.doc = SimpleDocTemplate(self.filename_str, pagesize=A4)

    def set_data(self, new_data):
        for flat_data in new_data:
            flatno=flat_data['flatno']
            cw_count = flat_data['cw_count']
            hw_count = flat_data['hw_count']
            co_count = flat_data['co_count']
            self.data.append([str(flatno), str(cw_count), str(hw_count), str(co_count)])

    def generate(self, flat_max):
        t = Table(self.data, style=[('GRID', (0, 1), (-1, -1), 1, colors.black), ('GRID', (0, 0), (-1, -flat_max), 1, colors.green)])
        self.elements.append(t)
        self.doc.build(self.elements)
        return self.filename_str

def main():
    data = []
    for flat in range(1, 12):
        cw_count = 1.231
        hw_count = 1.232
        co_count = 1.233
        data.append([cw_count, hw_count, co_count])

    report = Report()
    report.set_data(data)
    report.generate()

if __name__ == '__main__':
    main()

