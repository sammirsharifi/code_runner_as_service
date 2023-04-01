import pika, os
from urllib.parse import quote
from dotenv import load_dotenv
from s3 import s3_download_object
from Database import table_insert
from message_broker import receive

load_dotenv()

"""jobMicro.py is our job Microservice that manages the runcode requests has sent by users."""

"""this function is provided to pass s3 receive function that gets jobs requests."""


def job_receive_callback(ch, method, properties, body):
    code_id = body.decode()
    add_job(code_id)


def add_job(code_id):
    try:
        code = s3_download_object(code_id)
        query = codeToQuerystring(code)
        info = {"id": code_id, "upload": code_id, "job": query, "status": "none"}
        table_insert("jobs", info)
        return True
    except Exception:
        return Exception


def codeToQuerystring(code):
    return quote(code)


"""this function will run to get new requests in the moment."""
receive("jobs", job_receive_callback)
