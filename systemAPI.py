from fastapi import FastAPI, Request
from system import upload_request_handler

app = FastAPI()


@app.post("/upload")
async def root(request: Request):
    try:
        """ http request contains a json like this :
         json = { "token":"user_email" , "user_object":{"code":user_code , "language":code_language}}"""""

        infos = await request.json()
        user_object = infos["user_object"]
        user_token = infos["token"]
        info_dict = {"user_object": user_object, "token": user_token}
        response_message = upload_request_handler(info_dict)
        return response_message
    except Exception:
        return "bad request."
