from pymongo import MongoClient
from datetime import datetime
<<<<<<< HEAD

from dotenv import load_dotenv
import os
from backend.utils.helper import connect_to_mongo

load_dotenv()

def track_price_bestbuy(db_name, collection_name, model, product_title, price, url):
=======
import certifi
from dotenv import load_dotenv
import os


load_dotenv()

def track_price(db_name, collection_name, model, product_title, price, url, 
                mongo_uri=os.getenv("mongo_uri")):
>>>>>>> ee438e8b9db29d1df14d91d63e86c87f7613779e
    """
    Track the price of a PC over time.

    :param db_name: str, name of the database
    :param collection_name: str, name of the collection
    :param model: str, the unique identifier for the product
    :param product_title: str, the product's title
    :param price: float, the current price of the product
    :param url: str, the URL of the product
    :param mongo_uri: str, the MongoDB connection URI
    :return: str, result of the operation
    """
    try:
        # Connect to MongoDB
<<<<<<< HEAD
        client = connect_to_mongo()

        
=======
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
>>>>>>> ee438e8b9db29d1df14d91d63e86c87f7613779e

        # Access the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Define the update operation
        update_query = {"model": model}
        update_data = {
            "$set": {
                "product_title": product_title,
                "url": url
            },
            "$push": {
                "price_history": {
                    "price": price,
                    "date": datetime.utcnow()
                }
            }
        }

        # Perform the update with upsert=True
        result = collection.update_one(update_query, update_data, upsert=True)

        if result.upserted_id:
            return f"New record inserted with ID: {result.upserted_id}"
        else:
            return f"Record updated for model: {model}"

    except Exception as e:
<<<<<<< HEAD
        return f"Error tracking price: {e}"
=======
        return f"Error tracking price: {e}"

>>>>>>> ee438e8b9db29d1df14d91d63e86c87f7613779e
