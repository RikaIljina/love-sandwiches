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
    print(f'Stock row: {stock_row}')
    print(f'Sales row: {sales_row}')
    surplus = [x-y for x,y in (zip(stock_row, sales_row))]
    return surplus
    

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet ... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print("Updating surplus worksheet ... \n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)
    
    
print("Welcome to Love Sandwiches Data Automation!")
main()
    