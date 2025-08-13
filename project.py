from data.fred_data import FRED_API
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# load environment variables
load_dotenv()
"""
-Final Project instructions:
1. Your project must be implemented in Python
2. Your project must have a main function and three or more additional functions
3. Your main function must be in a file called project.py
4. Your other 3 custom functions must be in project.py and not nested under any other functions or classes
5. project.py must be in the root directory
6. Your test function must be in a file called test_project.py,which should be in project root directory
7. Test functions must have the same name as the custom function being tested prepended with test_custom()
8. Any pip-installable libraries that your project needs must be listed, in <requirements.txt>:which should
be in the root of your project.

--
-----------------Project Explanation---------------------------
This project collects valuable data regarding Economical health.
The data focuses on the GDP indicator.
GDP(Gross Domestic Product) a common measure of economic output,adjusted for inflation
*Primary focus: GDPC1. Series ID  GDPC1
-Nominal Gross Domestic Product - This GDP not adjusted for inflation
- GDP Growth Rate: series example: A191RL1Q225SBEA(Real GDP,Percent Change from Preceding
Period, Seasonally Adjusted Annual Rate.
- GDP per capita: Focus is on individual prosperity
------Other components that could give a deeper insight on GDP health------
Personal Consumption Expenditures(PCE)
Gross Private Domestic investment(GDPI)
Government Consumption Expenditures and Gross Investment(GCE)
Net Exports(usually derived from exports and imports)
- Data Sample frequency: quarterly observations
------Useful FRED Series IDs------
GDPC1: Real Gross Domestic Product (Billions of Chained 2017 Dollars, Quarterly, Seasonally Adjusted Annual Rate)

A191RL1Q225SBEA: Real Gross Domestic Product, Percent Change from Preceding Period (Quarterly, Seasonally Adjusted Annual Rate)

UNRATE: Unemployment Rate (Percent, Monthly, Seasonally Adjusted) - While not GDP, it's a critical related indicator for economic health.

CPIAUCSL: Consumer Price Index for All Urban Consumers: All Items (Index 1982-84=100, Monthly, Seasonally Adjusted) - Useful for discussing inflation context.

USREC: Recession Indicators (Monthly, values are 0 or 1 where 1 indicates a recession) - Excellent for adding context to GDP charts.


-----Project Libraries used in project-------
1.For Data Acquisition: fredapi
--Purpose: Access economical data from the Federal Reserve Economic Data(FRED) database.
2.For Data manipulation and preperation:pandas
--Purpose: Cleans and filters data, arranging it into a use df
3.For Visualization:plotly
--Purpse: Creates web based statistical graphics.
4.For Dashboard Framework: shiny
--Purpose: Handles the Ui layout and input widgets

-----Project Flow----
Start:With implementing logs for tracking
1st. Begin with the data fetching and processing
2nd. Plot data
"""
def main():

    print("Hello, World")
def function_1():
    ...
def function_2():
    ...
def function_3():
    ...

if __name__=="__main__":
    main()