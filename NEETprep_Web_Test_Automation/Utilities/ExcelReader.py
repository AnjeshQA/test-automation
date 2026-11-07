"""
ExcelReader - low-level Excel helpers (row/column count, read a cell, write a cell).

STATUS: not used by any test. Tests use Utilities/dataProvider.py instead.

WARNING: the code at the bottom of this file runs on import/execution and WRITES
"DOB" into Excel/testdata.xlsx (sheet LoginTest, which does not exist -> it errors).
Run it only as a manual demo; do not import it from tests.
"""
import openpyxl


# Number of rows (including the header) in a sheet
def getRowCount(path, sheetName):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheetName]
    return sheet.max_row


# Number of columns in a sheet
def getColCount(path, sheetName):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheetName]
    return sheet.max_column


# Read one cell (row and column numbers start at 1)
def getCellData(path, sheetName, rowNum, colNum):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheetName]
    return sheet.cell(row=rowNum, column=colNum).value


# Write one cell and save the workbook
def setCellData(path, sheetName, rowNum, colNum, data):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[sheetName]
    sheet.cell(row=rowNum, column=colNum).value = data
    workbook.save(path)


# --- Manual demo below (runs when this file is executed/imported) ---
path = "..//excel//testdata.xlsx"
sheetName = "LoginTest"

rows = getRowCount(path,sheetName)
cols = getColCount(path,sheetName)

print(rows,"---",cols)

print(getCellData(path,sheetName,2,1))
setCellData(path,sheetName,1,4,"DOB")