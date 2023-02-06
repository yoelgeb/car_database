import pandas as pd
import car_database 
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, select

class CarQuery:
    engine = sqlalchemy.create_engine(car_database.SQLITE_CONNECTION_STRING)
    Base = declarative_base()

    #Setting Up/Connecting to the database
    class Car(Base):
        __tablename__ = "car_sales"

        StockID = Column(Integer, primary_key= True)
        Make = Column(String)
        Model = Column(String)
        ColorID = Column(Integer)
        VehicleType = Column(String)
        CostPrice = Column(Integer)
        SpareParts = Column(Integer)
        LaborCost = Column(Integer)
        Registration_Date = Column(String)
        Mileage = Column(Integer)
        PurchaseDate = Column(String)

    Base.metadata.create_all(engine)

    def __init__(self):
        self.df = pd.read_sql(select(self.Car), self.engine.connect())

    def read_data(self):
        return self.df

    def read_data_id(self, id):
        return self.df.loc[self.df["StockID"] == id]

    # Returns dictionaries of cars with the lowest and highest prices and labor costs
    def max_price(self):
        return self.df.loc[self.df["CostPrice"] == self.df["CostPrice"].max()].to_dict('index')

    def min_price(self):
        return self.df.loc[self.df["CostPrice"] == self.df["CostPrice"].min()].to_dict('index')

    def max_labor_cost(self):
        return self.df.loc[self.df["LaborCost"] == self.df["LaborCost"].max()].to_dict('index')

    def min_labor_cost(self):
        return self.df.loc[self.df["LaborCost"] == self.df["LaborCost"].min()].to_dict('index') 


    # Number of Different Makes of Cards
    def num_of_makes(self):
        makes = len(self.df.groupby(by=["Make"]).count())
        return makes

    #Number of cars for each make
    def num_of_each_make(self):
        num_makes = self.df.groupby(by=["Make"]).size().to_dict()
        return num_makes
    
    # Total made from selling all cards
    def total_made(self):
        total = self.df["CostPrice"].sum()
        return f"${total}"

    # Returns a dictionary of cars within $2000 of price given by user
    def price_range(self, price):
        return self.df.loc[(self.df["CostPrice"] <= price + 2000) & (self.df["CostPrice"] >= price - 2000)].to_dict('index')

    # Returns a dictionary of all cars of a certain color id (1 - 9 Inclusive)
    def color_choice(self, color_id):
        return self.df.loc[self.df["ColorID"] == color_id].to_dict('index')

    #   Returns the make with the highest average car cost
    def highest_avg_make(self):
        avg = self.df.groupby(by=["Make"]).mean()[["CostPrice"]]
        avg = avg.reset_index()
        return avg.loc[avg['CostPrice'] == avg['CostPrice'].max()][['Make']].values[0][0]

    def add_car(self, values):
        # stock_id, make, model, color_id, vehicle_type, cost_price, spare_parts, labor_cost, reg_date, milage, pur_date
        # Values should be a dictionary
        add = pd.DataFrame(values, index=[0])
        return add.to_sql("car_sales", self.engine, if_exists='append')
    
    def update_car(self, car_dict, id):
        # User passes in a car to replace a car at current id
        car_dict["StockID"] = id
        self.df.loc[self.df['StockID'] == id] = pd.Series(car_dict)
        return self.df.to_sql("car_sales", self.engine, if_exists='replace')

    def remove_cars(self, key, value):
        # User passes in a key they want to delete based on, and then pass a value based on the key to delete all cars that match
        self.df = self.df[self.df[key] != value]
        return self.df.to_sql("car_sales", self.engine, if_exists='replace')
