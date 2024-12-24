from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

def extract_model_with_bs4(url):
    """
    Extract the model from the product webpage.

    :param url: str, the URL of the product page
    :return: str, the extracted model or an error message
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the element with the class 'product-data-value'
        model_element = soup.find('span', {'class': 'product-data-value'})
        
        # Extract and return the text
        if model_element:
            return model_element.text.strip()
        else:
            return "Model information not found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"
    
# Load environment variables (if using .env file)
load_dotenv()

def connect_to_mongo():
    """
    Connect to the MongoDB database.
    :return: MongoDB client instance
    """
    try:
        mongo_uri = os.getenv("mongo_uri")  
        
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None