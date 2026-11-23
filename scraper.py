import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


#url='https://books.toscrape.com/'
url='https://lcfe.ng/market-data.php'

conn=create_engine('mssql+pymssql://127.0.0.1/iswipe_cohort_3b')

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
response = requests.get(url, headers=headers)
content=BeautifulSoup(response.text, "html.parser")

results=content.find('table')

table={
  'date':[],
  'commodities':[],
  'location':[],
  'unit':[],
  'price':[]       
     }

def re_map(items):

    table['date'].append(items[0].text)
    table['commodities'].append(items[1].text)
    table['location'].append(items[2].text)
    table['unit'].append(items[3].text)
    table['price'].append(items[4].text)
    
    
    
result_set=results.find_all('tr')

for result in result_set:
    row=result.find_all('td')
    if row:
        re_map(row)

  
data=pd.DataFrame(table)
print(data[['date','commodities','unit','price','location']])


data.to_csv('lcfe_agric_data.csv', index=False)

data.to_sql('agric_data',if_exists='append', con=conn, index=False)
