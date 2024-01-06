import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()

# print(data)

def get_sales_data():
    """
    Get sales figures from user
    """
    while True:
            
        print("Please enter sales data from the last market:")
        print("Data should be six numbers separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        
        data_str = input("Enter data here:")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            break
        
    return sales_data
        
    # print(f'Data provided is {data_list}')
    
def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if string cannot be converted to int,
    or if there isn't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f'Exactly 6 values required, you provided {len(values)}')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    
    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock, calculate surplus for each item type
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # pprint(stock)
    stock_row = [int(num) for num in stock[-1]]
    # print(f'Stock row: {stock_row}')
    # print(f'Sales row: {sales_row}')
    surplus = [x-y for x,y in (zip(stock_row, sales_row))]
    return surplus
    
    
def update_worksheet(data, worksheet):
    """
    Receive a list with integers
    Update the relevant worksheet, add new row with the list data provided
    """ 
    print(f"Updating {worksheet} worksheet ... \n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet.capitalize()} worksheet updated successfully.\n")
   
   
def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    collecting the last 5 entries for each sandwich, and
    returns the data as a list of lists.  
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    
    columns = []
    for i in range(1, len(sales.row_values(1))+1):          # loop through all columns, their amount is equal to row length
        columns.append(sales.col_values(i)[-5:])   # remove the headers
    pprint(columns)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")    
    
print("Welcome to Love Sandwiches Data Automation!")
# main()
get_last_5_entries_sales()    