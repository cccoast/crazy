from dbfpy import dbf
from time import sleep
from win32com import client

def dbf2xls(dbfilename, exfilename):
    db = dbf.Dbf(dbfilename, True)
    ex = client.Dispatch('Excel.Application')
    wk = ex.Workbooks.Add()
    ws = wk.ActiveSheet
    ex.Visible = True
    sleep(1)

    r = 1
    c = 1
    for field in db.fieldNames:
        ws.Cells(r,c).Value = field
        c = c+1

    r = 2
    for record in db:
        c = 1
        for field in db.fieldNames:
            ws.Cells(r,c).Value = record[field]
            c = c+1
        r = r+1

    wk.SaveAs(exfilename)
    wk.Close(False)
    ex.Application.Quit()

    db.close()