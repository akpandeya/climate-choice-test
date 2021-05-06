"""A program which zips itself and uploads it to a specified slack channel.
Dependencies: 
1. requests: Makes it easy to make http request using python
2. python-dotenv : Storing the tokens/passwords in a program is unsafe and 
this package makes it easy to read variables from a file.

Time taken: Around 1h

"""

import requests
import os
from zipfile import ZipFile
from dotenv import dotenv_values
import json

__author__ = "Avanindra Kumar Pandeya"
__version__ = "0.1"
__email__ = "akpandeya1@gmail.com"

    
def get_channel_token(channel : str) -> str:
    """Reads the .env file in the scope for token corresponding to the channel and returns the token if found else None
        e.g. For channel C0218NDGUGL, we need to store C0218NDGUGL_TOKEN variable in the .env file like:
        C0218NDGUGL_TOKEN=secret-key
    Args:
        channel (str): Channel Id

    Returns:
        str: Token found in the .env file or None if not found
    """    
    config = dotenv_values(".env")

    token = config.get(f'{channel}_TOKEN')
    return token

def upload_file_to_channel(channel : str, initial_comment: str, file: str) -> None:
    """This method uploads a file to the slack channel using file upload api
        Description of the file upload api by slack: https://api.slack.com/messaging/files/uploading
    Args:
        channel (str): The ID of channel
        initial_comment (str): POST parameter from Slack
        file (str): file which needs to be uploaded to the 
    """    
    URL =  "https://slack.com/api/files.upload"
    
    files = {
        'file': (file, open(file, 'rb')),
        'initial_comment': (None, initial_comment),
        'channels': (None, channel),
    }

    token = get_channel_token(channel)
    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    
    res = requests.post(URL, files=files, headers=headers, )
    
    print(res.json(), res.status_code)

COMPRESSED_FILE_NAME = 'avanindra_coding_challenge.zip' # Name of the compressed file

file = os.path.basename(__file__) # Reading the name of current file

with ZipFile(COMPRESSED_FILE_NAME,'w') as zip: #Zipping the file
    zip.write(file)

channel = "C02115KHLUT"

upload_file_to_channel(channel, COMPRESSED_FILE_NAME[:-4], COMPRESSED_FILE_NAME)