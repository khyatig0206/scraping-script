from pymongo import MongoClient

try:
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://khyatig0206:muskey2004@mycluster.yauzwsg.mongodb.net/')
    db = client['myown_client']  # Access the database
    collection = db['first_collection']  # Access the collection
    
    # Create a document to insert
    dictionary = {'name': 'khyati', 'age': 20}
    
    # Insert the document into the collection
    collection.insert_one(dictionary)
    
    print("Connection and insertion successful!")
except Exception as e:
    print(f"Connection or insertion failed: {e}")