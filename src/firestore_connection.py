import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Initialize Firestore
cred = credentials.Certificate('../cred/drug-shop-23f6f-firebase-adminsdk-f3wxc-06cc8426b3.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
csv_file_path = '../resources/produk_clean.csv'

# Read CSV file into pandas DataFrame
df = pd.read_csv(csv_file_path)

# Convert DataFrame to dictionary
data_dict = df.to_dict(orient='records')

# Upload data to Firestore
for doc_data in data_dict:
    # Assuming 'collection_name' is the name of the collection in Firestore
    doc_ref = db.collection('produk').document()  # Auto-generate document ID
    doc_ref.set(doc_data)
    print(f"Document {doc_ref.id} uploaded successfully.")

print("CSV data uploaded to Firestore.")