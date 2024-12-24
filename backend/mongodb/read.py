from pymongo import MongoClient
from dotenv import load_dotenv
import os
from backend.utils.helper import connect_to_mongo
from backend.utils.helper import extract_model_with_bs4



client = connect_to_mongo()

def read_from_collection(client, database_name, collection_name, query=None):
    """
    Read documents from a MongoDB collection.

    :param client: MongoClient instance
    :param database_name: str, name of the database
    :param collection_name: str, name of the collection
    :param query: dict, query filter for the collection (default: None)
    :return: List of documents matching the query
    """
    try:
        db = client[database_name]
        collection = db[collection_name]

        if query is None:
            query = {}

        # Retrieve the documents
        documents = collection.find(query)

        # Convert the cursor to a list
        return list(documents)
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return []

def get_bestbuy_prebuilt(url): 
    """
    Main function to connect and read from MongoDB.
    """
    client = connect_to_mongo()
    
    model = extract_model_with_bs4(url)
    print(model)
    if client:
        database_name = "prebuilts"
        collection_name = "bestbuy"
        
        # Example query: Find all documents where "price" > 500
        query = {"model": model}
        
        documents = read_from_collection(client, database_name, collection_name, query)

        print("Documents retrieved:")
        documentFinal= []
        for doc in documents:
            
            documentFinal.append(doc)

        return documents            

        # Close the MongoDB connection
        client.close()
