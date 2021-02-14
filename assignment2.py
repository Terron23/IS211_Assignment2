import urllib.request
import datetime
import ssl
import argparse
import logging



def downloadData(url):
    """
    Function - downloads data from a csv via url
    args:
        url - api to call in order to download csv
    vars:
        context - Added to circumvent an ssl error in the the urlib package
        csv_data - data from url in binary format
        csv_content - data from url in human readable format
    """
    context = ssl._create_unverified_context()
    csv_data=urllib.request.urlopen(url, context=context)
    csv_content=csv_data.read().decode()
    return csv_content

def logger(message):
    """
    Function - Logs Errors to a file
    args:
        message - Text to append to the logger file
    vars:
        LOG_FILENAME - Name of ouput file
    """
    LOG_FILENAME = 'assignment2.txt'
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.DEBUG,
    )
    logging.debug(f'Error: {message}')

def processData(csv):
    """
    Function - Processes data in csv. Loops through each row and rolls data up into a dictionary.
    args:
        csv - file which will be processed  
    """
    obj = {}
    for row in csv.splitlines():
        # row variable is a list that represents a row in csv
        ls = row.split(",")
        try:
            obj[int(ls[0])] = (ls[1], datetime.datetime.strptime(ls[2], '%d/%m/%Y'))
        except:
            logger(f'{ls[0]} has invalid birthdate {ls[2]}')
    return obj

def displayPerson(id, personData):
    """
    Function - Prints data about user which corresponds to the id.  
    """
    if id in personData.keys():
        print(f'Person #{id} is {personData[id][0]} with a birthday of {personData[id][1].date()}')
    else:
        print(f"No User found with id = {id}")


def main(url):
    try:
        csvData = downloadData(url)
    except:
        logger("Invalid Url")

    personData = processData(csvData)
    id = 1
    while id > 0:
        try:
            id = int(input("Enter User Id to exit the program enter a number <= 0: "))
            if id > 0:
                displayPerson(id, personData)
            else:
                print("Terminating...")
        except:
            #Added to account for non integers
            id = 1
            print("Invalid input! Please enter a number.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.set_defaults(method = downloadData)
    parser.add_argument('url', type = str, help="Url String")
    args = parser.parse_args()
    main(args.url)
    


    
    