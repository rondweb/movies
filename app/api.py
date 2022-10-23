import io
import json
import os
from json import JSONEncoder

import pandas as pd
from flask import jsonify
from flask_restx import Resource
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import api, app, db
from app.models import *


def map_headers(obj=None):
    """_summary_

    Args:
        obj (_type_, optional): Mapping headers of the csv file

    Returns:
        _type_: _description_
    """    
    obj = obj.lower()
    obj = obj.replace(" ", "_")
    return obj


def map_objects(dct: dict = None):
    """_summary_

    Args:
        dct (dict, optional): dictionary that contains the objects to be saved in the database

    Returns:
        _type_: object type and title
    """    
    genres = [Genre(name=it) for it in str(dct["genres"]).split(",")]
    title = Title(**dct)
    [title.lst_genres.append(gen) for gen in genres]
    
    if "titletype" in dct:
        type = Type(name=str(dct["titletype"]), description=str(dct["titletype"]))
        title.type = type 
        return type,title
    else:
        return [title]

def process_frame(df):
    type_and_titles = list(map(map_objects, df.to_dict(orient="records")))
    save_objects(type_and_titles)
    return len(df)

def import_dataframe_by_chunk():
    import multiprocessing as mp
    
    LARGE_FILE = "static//files//title.basics.tsv.gz"
    df = pd.read_csv(LARGE_FILE, compression="gzip", sep="	", header=0)
    column_headers = list(map(map_headers, df.columns.values.tolist()))
    print(column_headers)
    df.columns = column_headers

    CHUNKSIZE = 1000 # processing 100,000 rows at a time
    reader = pd.read_table(LARGE_FILE, chunksize=CHUNKSIZE)
    pool = mp.Pool(4) # use 4 processes

    funclist = []
    for df in reader:
            # process each data frame
            df.columns = column_headers
            f = pool.apply_async(process_frame,[df])
            funclist.append(f)
            
    result = 0
    for f in funclist:
            result += f.get(timeout=10) # timeout in 10 seconds

    print (f"There are {result} rows of data")
    return f"There are {result} rows of data"


def save_objects(lst_obj):
    """_summary_

    Args:
        lst_obj (_type_): list of objects to be saved in the database
    """    
    [db.session.add_all(obj) for obj in lst_obj]    
    db.session.commit()


@api.route("/movies")
class movies(Resource):
    """_summary_

    Args:
        Resource (_type_): Class movies and methods to import or expose the data
    """
    def get(self):
        return jsonify([tt.to_dict() for tt in Title.query.all()])

    def post(self):
        result = import_dataframe_by_chunk()
        return { result: result},201
        # df2 = df.head().to_dict(orient="records")

        # type_and_titles = list(map(map_objects, df.to_dict(orient="records")))
        # save_objects(type_and_titles)

# @app.route("/")
# def main():
#     return "Hello world Web App"

@app.before_first_request
def before_first_request():
    """Before first request let's create the database and the structures.

    Returns:
        _type_: _description_
    """
    db.drop_all()
    db.session.commit()
    db.create_all()
    return "All the database is truncated!"


@app.route("/truncate-db")
def delete_data_db(recreate=True):
    """Clean the dabase and the structures and recreate the database tables

    Args:
        recreate (bool, optional): Recreate the database. Defaults to True.

    Returns:
        _type_: _description_
    """
    db.drop_all()
    db.session.commit()
    if recreate:
        db.create_all()
    return "All the database is truncated!"
