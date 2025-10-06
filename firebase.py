import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import numpy as np

cred = credentials.Certificate('bigcon-2025-firebase-adminsdk-fbsvc-4409b3177b.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bigcon-2025-default-rtdb.asia-southeast1.firebasedatabase.app'
})


df = pd.read_csv('dataset/sinhan/big_data_set3_f.csv', encoding='cp949')
df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

data_dict = {}
for _, row in df.iterrows():
    key = str(row['ENCODED_MCT'])
    record = row.to_dict()
    data_dict[key] = record

ref = db.reference('가맹점_월별_고객정보')
ref.set(data_dict)