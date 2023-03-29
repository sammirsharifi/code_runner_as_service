import uuid
from Database import table_insert
from s3 import s3_put_object

"""this function gets uploaded file info & first get a unique id from def generate_id and then uploads the 
source code on the s3 by def s3_put_object and after that uploads the information about file on the database at the table <uploads>
by def table_insert"""


def upload_request_handler(info_dict):
    try:
        user_object = info_dict["user_object"]
        username = info_dict["token"]
        user_code = user_object["code"]
        code_language = user_object["language"]
        object_id = generate_id()
        s3_put_object(user_code, object_id)
        db_info = {"id": object_id, "email": username, "input": object_id, "language": code_language, "enable": 0}
        table_insert("uploads", db_info)

        return f"your code uploaded successfully. your file id is {object_id}."

    except Exception as e:
        return e


def generate_id():
    id = str(uuid.uuid4().int)[:4]
    return id
