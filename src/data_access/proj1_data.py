import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
from src.logger import logging

class Proj1Data:
    """
    A class to export MongoDB records as Dataframe.
    """

    def __init__(self)-> None:
        """
        Initializes the MongoDB client connection.
        """

        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas Dataframe.

        Parameters:
        -----------
        collection_name : str
            The name of the MongoDB collection to export
        database_name : Optional[str]
            Name of the database(optional). Defaults to DATABASE_NAME

        Returns:
        --------
        pd.Dataframe:
            Dataframe containing the collection data, with "_id" column removed and 'na' values replaced with NaN.
    
        """

        try:

            if database_name is None:

                """ If no specific database_name is provided, it uses the database that the MongoDBClient
                 was initialized with (i.e., self.mongo_client.database which points to DATABASE_NAME).
                 It then accesses the specified 'collection_name' within that default database."""
                
                collection = self.mongo_client.database[collection_name]

            else:
                
                """ If a 'database_name' is explicitly provided, it uses the raw MongoDB client
                (self.mongo_client.client) to access that specified database, and then the collection.
                This allows fetching from a different database than the default one set during initialization."""

                collection = self.mongo_client[database_name][collection_name]

            # Convert collection data to Dataframe and preprocess
            logging.info("Fetching data from MongoDB.")
            
            df = pd.DataFrame(list(collection.find()))

            logging.info(f"Data fetched with len: {len(df)}")

            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        
        except Exception as e:
            raise MyException(e, sys)
