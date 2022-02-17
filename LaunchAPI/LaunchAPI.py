from re import T
from numpy import row_stack, select
import requests
import pandas as pd
import xlsxwriter

class Access_API: # Class to do RESTful operations
    def __init__(self):
        api_url = "https://api.spacexdata.com/v3/launches" 
        response = requests.get(api_url)
        self.result = response.json() 
            
class Data_SRC: #Use like Data Access Object
    def __init__(self):
        access_api = Access_API()
        dateframe = pd.json_normalize(access_api.result) #This is a Nested JSON
        dateframe.columns = dateframe.columns.map(lambda x: x.split(".")[-1])
        self.result = dateframe

    def frequentlyYear(self): #Years that most appear
        year_most_frequently = self.result['launch_year'].value_counts().idxmax()
        return(year_most_frequently)

    def launcSite(self): #Launch site with most launchs
        launch_site =  self.result['site_name_long'].value_counts().idxmax()
        return str(launch_site)
    
    def totalLaunch(self): #Total of Launchs between 19-21
        total_launch =  self.result.loc[( self.result['launch_year'] > '2018') & ( self.result['launch_year'] < '2022' )].count()
        return(total_launch['flight_number'])

class Create_XLSX: #Create an Excel file
    def __init__(self):
        select_data = Data_SRC()
        workbook = xlsxwriter.Workbook('Expenses01.xlsx')
        worksheet = workbook.add_worksheet()

        expenses = (
            [ 'Ano com mais lancamentos', select_data.frequentlyYear() ], 
            [ 'Local com mais lancamentos', str(select_data.launcSite()) ] ,
            [ 'Total de Lancamentos entre 2019 e 2021' , select_data.totalLaunch() ],
        )

        row = 0
        column = 0
        
        for item, cost in (expenses):
            worksheet.write(row, column, item)
            worksheet.write(row + 1, column, cost)
            column += 1

        workbook.close()

create_file = Create_XLSX()