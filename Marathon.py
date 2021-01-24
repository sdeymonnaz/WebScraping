import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "https://www.hubertiming.com/results/2018MLK"
html = urlopen(url)

soup = BeautifulSoup(html)

title = soup.title
print(title)
print(title.text)

'''
links = soup.find_all('a', href=True)
for link in links:
    print(link['href'])
'''

data = []
allrows = soup.find_all('tr')
for row in allrows:
    row_list = row.find_all('td')
    dataRow = []
    for cell in row_list:
        dataRow.append(cell.text)
    data.append(dataRow)
data = data[5:]

headers_list = []
col_headers = soup.find_all('th')
for col in col_headers:
    headers_list.append(col.text)


df = pd.DataFrame(data)
#print(df.head(2))
#print(df.tail(2))

df.columns = headers_list
print(df.head())

df.info()

print(df.shape)
df2 = df.dropna(how='any')
print(df2.shape)

print(df2['Chip Time'])

print(len(df.iloc[1]['Chip Time']))


#%%
print(df2.shape)

df2 = df2.rename(columns={'Chip Time':'ChipTime'})

df2['ChipTime_minutes'] = pd.to_timedelta(
    np.where(df2['ChipTime'].str.count(':') == 1, '00:' + df2['ChipTime'], df2['ChipTime']))

df2['ChipTime_minutes'] = df2['ChipTime_minutes'].astype('timedelta64[s]') / 60

df2[['ChipTime_minutes']].info()

#%%

plt.bar(df2['Gender'], df2['ChipTime_minutes'])
plt.xlabel('Gender')
plt.ylabel('Chiptime_minutes')
plt.title('Comparison of average minutes run by gender')

#%%
df2.describe(include=[np.number])

#%%
df2.boxplot(column='ChipTime_minutes', by='Gender')
plt.ylabel('Run time')

#%%
df2['Age_i'] = round(pd.to_numeric(df2['Age'], errors='coerce'))
df2.dropna(how='any', inplace=True)

plt.scatter(df2['ChipTime_minutes'], df2['Age_i'])
plt.show()






