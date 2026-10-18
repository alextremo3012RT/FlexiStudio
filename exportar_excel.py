"""Exporta únicamente las filas visibles/filtradas y protege contra fórmulas inyectadas."""
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
import xlsxwriter


def exportar(nombre_tabla, campos, filas, destino):
    destino = Path(destino)
    if not filas:
        raise ValueError('No hay resultados para exportar.')
    if len(filas) > 1_048_575:
        raise ValueError('Excel admite como máximo 1,048,575 registros por hoja.')
    wb = xlsxwriter.Workbook(str(destino), {'strings_to_formulas': False, 'strings_to_urls': False})
    try:
        hoja = wb.add_worksheet('Datos')
        hoja.hide_gridlines(2)
        cab = wb.add_format({'bold': True, 'bg_color': '#E6002B', 'font_color':'#FFFFFF',
                             'border':0, 'valign':'vcenter'})
        txt = wb.add_format({'font_color': '#303035', 'bg_color': '#F3F3F3'})
        alterno = wb.add_format({'font_color': '#303035', 'bg_color': '#E6E6E8'})
        precio = wb.add_format({'num_format': '#,##0.00', 'bg_color': '#F3F3F3'})
        precio_alt = wb.add_format({'num_format': '#,##0.00', 'bg_color': '#E6E6E8'})
        fecha = wb.add_format({'num_format':'yyyy-mm-dd hh:mm', 'bg_color':'#F3F3F3'})
        fecha_alt = wb.add_format({'num_format':'yyyy-mm-dd hh:mm', 'bg_color':'#E6E6E8'})
        for col, (_, titulo) in enumerate(campos):
            hoja.write(0, col, titulo, cab)
            hoja.set_column(col, col, min(45, max(16, len(titulo) + 6)))
        hoja.set_row(0, 28)
        for n, fila in enumerate(filas, start=1):
            for idx, (key, _) in enumerate(campos):
                valor = fila.get(key)
                base = alterno if n % 2 == 0 else txt
                if valor is None:
                    hoja.write_blank(n, idx, None, base)
                elif isinstance(valor, bool):
                    hoja.write_string(n, idx, 'Sí' if valor else 'No', base)
                elif isinstance(valor, (date, datetime)):
                    if isinstance(valor, date) and not isinstance(valor, datetime):
                        valor = datetime.combine(valor, datetime.min.time())
                    hoja.write_datetime(n, idx, valor, fecha_alt if n % 2 == 0 else fecha)
                elif isinstance(valor, (float, Decimal, int)):
                    hoja.write_number(n, idx, float(valor), precio_alt if n % 2 == 0 else precio)
                else:
                    # Siempre escribir texto explícito: =SUM(), +cmd y URLs no se ejecutan.
                    hoja.write_string(n, idx, str(valor), base)
        hoja.freeze_panes(1, 0)
        hoja.autofilter(0, 0, len(filas), len(campos)-1)
        hoja.set_landscape()
        hoja.fit_to_pages(1, 0)
        hoja.set_header('&CFLEXI · REPORTE')
        hoja.set_footer('&CGenerado desde Flexi Studio &P / &N')
    finally:
        wb.close()
    return destino
