import json
from datetime import datetime

import requests

from Database import table_read, table_update

"""{
  "timeStamp": 1676969214607,
  "status": 200,
  "output": "12\n",
  "error": "",
  "language": "py",
  "info": "Python 3.6.9"
}"""


def update_results_jobs(response_json, code_id):
    if response_json["status"] == 200:
        output = response_json["output"]
    else:
        output = response_json["error"]
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    table_update("jobs", "status=\"executed\"", f"id={code_id}")
    table_update("results", f"output=\"{output}\" , status = \"done\" , execute_date=\"{date}\"", f"id={code_id}")
    return output


"""this function runs the job on codeX server."""


def run_code(job):
    response = requests.post(url='https://api.codex.jaagrav.in', data=job,
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'}, )

    return response.json()


def send_email(user_email, code_id, message):
    message = f"Dear {user_email} your code with id:{code_id} is :\n " + message


"""manager function gets code_id and job then runs the code and gets the response and calls update_result_jobs """


def manager(code):
    code_id, job = code
    response_json = run_code(job)
    update_results_jobs(response_json, code_id)
    # user_email = table_read("uploads", "email", f"id = {code_id}]")
    # send_email(user_email, code_id, email_message)


while True:
    readyCodes = table_read("jobs", "id,job", "status=\"none\"")
    for code in readyCodes:
        manager(code)