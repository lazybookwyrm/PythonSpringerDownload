import pandas as pd
import requests
from bs4 import BeautifulSoup
import progressbar
import re

# Uses the Excel file provided by Springer
df = pd.read_excel(r'FreeEnglishTextbooks.xlsx') 
rowCount = df.shape[0]

# Asks the user what category they want to download
#(can be found under row L - English Package name)
print('')
print('Enter the category you would like to download (Enter "all" to download all categories)')
category = input()
downloadAll = "all"

# Asks the user what file location they would like to save the files in
print('')
print('Enter the file path you would like to save your files in ')
saveLocation = input();
saveLocation = saveLocation.replace("C:", "")
saveLocation = saveLocation.replace("\\", "/")

# Loops through book records matching the user's query
progress = progressbar.ProgressBar()
for p in progress(range(rowCount)):    
    if str(df.iloc[p, 11]) == category or category == downloadAll:
        url = df.iloc[p, 18]
        year = str(df.iloc[p, 4])
        author = str(df.iloc[p, 1])
        title = str(df.iloc[p, 0])
        filename = author + ' ('+year+') '+title
        filenameValid = re.sub("[/:*?<>|]", "-", filename)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        # Looks for EPUB file to download
        table = soup.find('a', attrs={'class': 'test-bookepub-link'})
        fileSaveLocation = saveLocation + '/' + filenameValid + '.epub'
        # Looks for PDF file if no EPUB file is found
        if table is None:
            table = soup.find('a', attrs={'class': 'test-bookpdf-link'})
            fileSaveLocation = saveLocation + '/' + filenameValid + '.pdf'
        table = table.get("href")
        link = "https://link.springer.com" + table

        # Downloads the file if it is not present in the folder
        try:
            with open(fileSaveLocation) as f:
                print(title, "has already been downloaded")
                f.close()
        except FileNotFoundError:
            r2 = requests.get(link)
            with open(fileSaveLocation, 'wb') as f:
                f.write(r2.content)
                f.close()
            print('Successfully downloaded ', title)

print('Successfully downloaded ' + category + ' titles')
exit