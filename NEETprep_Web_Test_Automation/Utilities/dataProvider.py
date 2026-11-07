"""
dataProvider - reads test data rows from Excel/testdata.xlsx for data-driven tests.

Usage:
    @pytest.mark.parametrize("mobileNumber, otp", dataProvider.get_data("UserDetail"))

Returns a list of tuples, one tuple per non-empty row (header row 1 is skipped), e.g.
    [("9000000000", "876302")]

Sheets in testdata.xlsx:
    UserDetail  -> valid login (mobileNumber, otp)
    InvalidCred -> invalid login (valid mobileNumber, wrong otp)
"""
import openpyxl
import os


def get_data(sheetName):
    """
    Reads data from the Excel file and converts numeric values
    to clean strings (removing .0 from floats).
    """
    # 1. Construct the path to your excel file
    # This assumes your folder structure is ProjectRoot/Utilities/dataProvider.py
    # and ProjectRoot/Excel/testdata.xlsx (folder name is case-sensitive on Linux)
    base_path = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_path, "..", "Excel", "testdata.xlsx")

    # 2. Open the workbook; return no data (tests show as [NOTSET]) if the file is missing
    try:
        workbook = openpyxl.load_workbook(excel_path)
    except FileNotFoundError:
        print(f"Error: The file {excel_path} was not found.")
        return []

    # 3. Select the requested sheet
    sheet = workbook[sheetName]
    main_list = []

    # Iterate through rows starting from the second row (skipping headers)
    for row in range(2, sheet.max_row + 1):
        data_list = []
        for col in range(1, sheet.max_column + 1):
            value = sheet.cell(row=row, column=col).value

            # Empty cells are skipped
            if value is not None:
                # --- CLEANING LOGIC ---
                # Check if the value is a float (like 9000000000.0)
                if isinstance(value, float):
                    # Convert to int first to drop .0, then to string
                    value = str(int(value))
                else:
                    # Otherwise, just make it a string
                    value = str(value)

                data_list.append(value)

        # Only add to the main list if the row isn't empty
        if data_list:
            main_list.append(tuple(data_list))

    # 4. One tuple per row -> one test run per row with parametrize
    return main_list
