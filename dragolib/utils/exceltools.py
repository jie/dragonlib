import xlwt
from io import BytesIO


def export_excel(data, sheet="Sheet1", headers=[]):
    ws = xlwt.Workbook()
    w = ws.add_sheet(sheet)

    for index, item in enumerate(headers):
        w.write(0, index, item)

    if len(headers) == 0:
        start = 0
    else:
        start = 1
    for index, items in enumerate(data, start=start):
        for i in range(len(items)):
            w.write(index, i, items[i])
    sio = BytesIO()
    ws.save(sio)

    sio.seek(0)
    return sio


def export_style_excel(data, sheet="Sheet1", headers=[]):
    headerStyle = xlwt.XFStyle()
    # alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    headerStyle.alignment = alignment

    headerFont = xlwt.Font()
    headerFont.height = 300
    headerStyle.font = headerFont
    headerPattern = xlwt.Pattern()
    headerPattern.pattern = xlwt.Pattern.SOLID_PATTERN
    headerPattern.pattern_fore_colour = 5
    headerStyle.pattern = headerPattern

    headerBorders = xlwt.Borders()
    headerBorders.left = xlwt.Borders.DASHED
    headerBorders.right = xlwt.Borders.DASHED
    headerBorders.top = xlwt.Borders.DASHED
    headerBorders.bottom = xlwt.Borders.DASHED
    headerBorders.left_colour = 0x40
    headerBorders.right_colour = 0x40
    headerBorders.top_colour = 0x40
    headerBorders.bottom_colour = 0x40
    headerStyle.borders = headerBorders

    ws = xlwt.Workbook()
    sh = ws.add_sheet(sheet)

    for index, items in enumerate(headers):
        for i in range(len(items)):
            sh.write(index, i, items[i], headerStyle)

    if len(headers) == 0:
        start = 0
    else:
        start = 1
    for index, items in enumerate(data, start=start):
        for i in range(len(items)):
            sh.write(index, i, items[i])

    # tall_style = xlwt.easyxf('font:height 720')
    tall_style = xlwt.easyxf('font:height 2000')
    sh.row(0).set_style(tall_style)
    for index, item in enumerate(headers[0]):
        sh.col(index).width = 256 * 20
    sio = BytesIO()
    ws.save(sio)

    sio.seek(0)
    return sio
