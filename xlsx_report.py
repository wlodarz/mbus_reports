import xlsxwriter

def cell2name(row, column):
    col_array = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return col_array[column]+str(row+1)


class xlsx_report:
    def __init__(self, month, year, co_cost, cw_cost, hw_cost):
        self.month = month
        self.year = year
        self.co_cost = co_cost
        self.cw_cost = cw_cost
        self.hw_cost = hw_cost

    def write(self, readings):
        # fields position configuration
        row_data = 0
        col_data = 0

        row_taryfa = 0
        col_taryfa = 4

        row_mieszkania = 5
        col_mieszkania = 0

        row_odczyt_aktualny = 5
        col_odczyt_aktualny = 2

        row_odczyt_poprzedni = 5
        col_odczyt_poprzedni = 6

        row_roznica = 5
        col_roznica = 10

        row_koszt = 5
        col_koszt = 14

        row_suma = 5
        col_suma = 18

        filename = 'rozliczenie_'+str(self.month)+'_'+str(self.year)+'.xlsx'
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        bold_format = workbook.add_format({'bold' : True})
        green_format = workbook.add_format({'bg_color' : 'lime'})

        worksheet.set_column(row_data, col_data, 15)
        worksheet.write(row_data, col_data, 'Rozliczenie za miesiac', bold_format)
        worksheet.write(row_data, col_data+2, str(self.month)+'/'+str(self.year))

        # Some data we want to write to the worksheet.
        tariff = (
            ['Koszt 1kWh CO', self.co_cost],
            ['Koszt 1kWh CW', self.cw_cost],
            ['Koszt 1kWh HW', self.hw_cost],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        worksheet.write(row_taryfa, col_taryfa, 'Taryfa', bold_format)
        worksheet.set_column(row_taryfa, col_taryfa, 12)

        # Iterate over the data and write it out row by row.
        row = 0
        for item, cost in (tariff):
            worksheet.write(row_taryfa+1+row, col_taryfa,     item)
            worksheet.write(row_taryfa+1+row, col_taryfa+2, cost, green_format)
            worksheet.write(row_taryfa+1+row, col_taryfa+3, 'PLN')
            row += 1

        worksheet.write(row_mieszkania, col_mieszkania, 'Mieszkanie', bold_format)
        worksheet.set_column(row_mieszkania, col_mieszkania, 10)

        worksheet.write(row_odczyt_aktualny, col_odczyt_aktualny+1, 'Stan aktualny', bold_format)
        worksheet.write(row_odczyt_aktualny+1, col_odczyt_aktualny, 'CO')
        worksheet.write(row_odczyt_aktualny+1, col_odczyt_aktualny+1, 'CW')
        worksheet.write(row_odczyt_aktualny+1, col_odczyt_aktualny+2, 'HW')

        worksheet.write(row_odczyt_poprzedni, col_odczyt_poprzedni+1, 'Stan poprzedni', bold_format)
        worksheet.write(row_odczyt_poprzedni+1, col_odczyt_poprzedni, 'CO')
        worksheet.write(row_odczyt_poprzedni+1, col_odczyt_poprzedni+1, 'CW')
        worksheet.write(row_odczyt_poprzedni+1, col_odczyt_poprzedni+2, 'HW')

        worksheet.write(row_roznica, col_roznica+1, 'Roznica', bold_format)
        worksheet.write(row_roznica+1, col_roznica, 'CO')
        worksheet.write(row_roznica+1, col_roznica+1, 'CW')
        worksheet.write(row_roznica+1, col_roznica+2, 'HW')

        worksheet.write(row_koszt, col_koszt+1, 'Koszt', bold_format)
        worksheet.write(row_koszt+1, col_koszt, 'CO')
        worksheet.write(row_koszt+1, col_koszt+1, 'CW')
        worksheet.write(row_koszt+1, col_koszt+2, 'HW')

        worksheet.write(row_suma, col_suma, 'Suma', bold_format)

        row = 0
        for flat, costs in readings:
            worksheet.write(row_mieszkania+2+row, col_mieszkania, flat)

            worksheet.write(row_odczyt_aktualny+2+row, col_odczyt_aktualny, costs[0])
            worksheet.write(row_odczyt_aktualny+2+row, col_odczyt_aktualny+1, costs[1])
            worksheet.write(row_odczyt_aktualny+2+row, col_odczyt_aktualny+2, costs[2])

            worksheet.write(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni, costs[3])
            worksheet.write(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni+1, costs[4])
            worksheet.write(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni+2, costs[5])

            roznica_co_formula = '{='+cell2name(row_odczyt_aktualny+2+row, col_odczyt_aktualny)+'-'+cell2name(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni)+'}'
            roznica_cw_formula = '{='+cell2name(row_odczyt_aktualny+2+row, col_odczyt_aktualny+1)+'-'+cell2name(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni+1)+'}'
            roznica_hw_formula = '{='+cell2name(row_odczyt_aktualny+2+row, col_odczyt_aktualny+2)+'-'+cell2name(row_odczyt_poprzedni+2+row, col_odczyt_poprzedni+2)+'}'

            cost_co_formula = '{='+cell2name(row_roznica+2+row, col_roznica)+'*'+cell2name(row_taryfa+1, col_taryfa+2)+'}'
            cost_cw_formula = '{='+cell2name(row_roznica+2+row, col_roznica+1)+'*'+cell2name(row_taryfa+2, col_taryfa+2)+'}'
            cost_hw_formula = '{='+cell2name(row_roznica+2+row, col_roznica+2)+'*'+cell2name(row_taryfa+3, col_taryfa+2)+'}'

            sum_co_formula = '{='+cell2name(row_koszt+2+row, col_koszt)+'+'+cell2name(row_koszt+2+row, col_koszt+1)+'+'+cell2name(row_koszt+2+row, col_koszt+2)+'}'
            # sum_cw_formula = '{=Q'+str(row+2)+'+'+'R'+str(row+2)+'+'+'S'+str(row+2)+'}'
            # sum_hw_formula = '{=Q'+str(row+3)+'+'+'R'+str(row+3)+'+'+'S'+str(row+3)+'}'

            worksheet.write_formula(cell2name(row_roznica+2+row, col_roznica), roznica_co_formula)
            worksheet.write_formula(cell2name(row_roznica+2+row, col_roznica+1), roznica_cw_formula)
            worksheet.write_formula(cell2name(row_roznica+2+row, col_roznica+2), roznica_hw_formula)

            worksheet.write_formula(cell2name(row_koszt+2+row, col_koszt), cost_co_formula)
            worksheet.write_formula(cell2name(row_koszt+2+row, col_koszt+1), cost_cw_formula)
            worksheet.write_formula(cell2name(row_koszt+2+row, col_koszt+2), cost_hw_formula)

            worksheet.write_formula(cell2name(row_suma+2+row, col_suma), sum_co_formula)

            row += 1

        workbook.close()


if __name__=='__main__':
    readings = (
            [2, [430, 240, 350, 200, 210, 220]],
            [3, [440, 340, 450, 300, 310, 320]],
            [4, [530, 440, 550, 400, 410, 420]],
            [5, [730, 540, 650, 500, 510, 520]],
            )
    xls = xlsx_report(7,2022, 4.5, 5.5, 6.5)
    xls.write(readings)

