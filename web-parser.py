import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
from time import sleep


MAX_THREADS=30


def parse(url):
    try:
        api = requests.get(url) # Get URL using request
    except:
        return "Failed to get url"
    soup = BeautifulSoup(api.content, 'html.parser') # Initializing parsing using Beautifulsoup
    resList = soup.findAll(id="reveal_fullprofile") # Find all objects with id="reveal_fullprofile"
    # Creating lists for all data we need
    name = []
    lastname = []
    phonenumber = []
    email = []
    company = []
    # Adding data we found with findAll()
    for res in resList: 
        name.append(res.get('data-preferred_name'))
        lastname.append(res.get('data-last_name'))
        phonenumber.append(res.get('data-phone'))
        email.append(res.get('data-email'))
        company.append(res.get('data-company'))
    # Start creating Excel document with our data
    sleep(0.25)
    return name,lastname,phonenumber,email,company

def excel_creator(name,lastname,phonenumber,email,company): 
    df = pd.DataFrame({'Name': name,                    # Create a Pandas dataframe from data we received
                        'Lastname': lastname,
                        'Phone_number': phonenumber,
                        'Email': email,
                        'Company': company,})

    writer = pd.ExcelWriter('Broker_list.xlsx', engine='xlsxwriter') # Create Pandas Excel writer using xlsxwriter as our engine
    # Convert dataframe to an Xlsxwriter Excel object
    # Turn off defeault header and index to insert user defined header 
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False) 
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    # Get the dimensions of the dataframe 
    (max_row, max_col) = df.shape
    # Create a list of column headers, to use in add_table
    column_settings = []
    for header in df.columns:
        column_settings.append({'header': header})

    worksheet.add_table(0,0, max_row, max_col - 1, {'columns': column_settings}) # Add the table
    worksheet.set_column(0, max_col - 1, 12) # Making columns wider
    #Close Pandas Excel writer and output Excel file.
    writer.save()
    print("Done!")

def url_excutor(max):
    nameList = []
    lastnameList = []
    emailList = []
    phonenumberList=[]
    companyList = []
    for i in range(1,max+1):
        url = f'https://www.mortgageandfinancehelp.com.au/find-accredited-broker/?page={i}&query=&location=&_=1648481256495'
        name,lastname,email,phonenumber,company = parse(url)
        nameList.extend(name)
        lastnameList.extend(lastname)
        emailList.extend(email)
        phonenumberList.extend(phonenumber)
        companyList.extend(company)
    excel_creator(nameList,lastnameList,emailList,phonenumberList,companyList)

def main():
    url_excutor(498)


if __name__ == "__main__":
    main()
