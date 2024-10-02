import pandas as pd

# Initialize x as a global variable
x = None  # This will hold the DataFrame

def set_x(dataframe):
    global x  # Declare x as a global variable to modify it
    x = dataframe  # Assign the DataFrame to x
   
    
    
    y = len(x)
    print(y)

def use_data():
    if x is not None:
        print("Process:")
        print(x.head())  # Print the first few rows of the DataFrame
    else:
        print("No data available")

    
use_data()