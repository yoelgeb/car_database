# Main File to test functions
import pandas as pd
from car_database_queries import CarQuery

file_name = 'car_sales_table.csv'
csv_df = pd.read_csv(file_name)

#Transfering the csv file to the db file
#Comment out below if the table already exists and is filled with data

#csv_df.to_sql("car_sales", sqlite_connect, if_exists="replace")

query = CarQuery()

new_car = {"StockID" : len(query.read_data()) + 1, "Make" : "Test", "Model" : "Test", "ColorID": 9, "VehicleType" : "Test", "CostPrice" : 999999, "SpareParts" : 9,
            "LaborCost" : 999, "Registration_Date" : "Test", "Mileage" : 000, "PurchaseDate" : "Test"}


#print(query.update_car(new_car, 0, engine))
#query.add_car(new_car, engine)
#query.remove_cars("StockID", 5, engine)

#print(query.add_car(new_car))
print(query.read_data())

