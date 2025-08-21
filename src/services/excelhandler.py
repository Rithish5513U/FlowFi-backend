import pandas as pd
from extensions import db
from flask_jwt_extended import get_jwt_identity

transactions = db['transactions']

class ExcelHandler:
    def __init__(self):
        self.required_columns = ['date', 'description', 'withdrawals', 'deposits', 'balance']

    def process_uploaded_file(self, file_stream):
        """
        Function to process a single uploaded Excel file (in-memory) and store unique records to DB
        Inputs:
            file_stream -> BytesIO : Uploaded file stream from client
        Outputs:
            Tuple : (List of user's transactions in dict format, status code)
        """
        try:
            df = pd.read_excel(file_stream)
            df.columns = [column.lower() for column in df.columns]

            if not all(col in df.columns for col in self.required_columns):
                return {"error": "Invalid Excel format"}, 400

            df = df[self.required_columns]
            df.drop_duplicates(inplace=True)
            df.fillna(0, inplace=True)

            user_email = get_jwt_identity()
            existing_entry = transactions.find_one({"email": user_email})

            if existing_entry:
                existing_df = pd.DataFrame(existing_entry.get("data", []))
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.drop_duplicates(inplace=True)
                combined_data = combined_df.to_dict(orient='records')

                transactions.update_one(
                    {"email": user_email},
                    {"$set": {"data": combined_data}}
                )
            else:
                combined_data = df.to_dict(orient='records')
                transactions.insert_one({
                    "email": user_email,
                    "data": combined_data
                })

            return combined_data, 200

        except Exception as e:
            return {"error": str(e)}, 500
