from fastapi import Body, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI,Depends,status
import json
import pandas as pd
from domain.eeg_app_aggregate.repository_eeg import EEGRepo
from application.render_user_dashboard import create_dash_app
from application.functions import plot_figure11
from application.functions import plot_figure22
from application.functions import plot_figure33
from application.functions import plot_figure44


app = FastAPI()

@app.get("/eegdata/")
async def get_eeg_data():
    eeg_data = EEGRepo.fetch_all_eeg()
    return (eeg_data)

@app.get("/eegdata/{profile_id}")
async def get_eeg_data_by_profile_id(profile_id):
    eeg_data = EEGRepo.fetch_eeg_by_id(profile_id)['values']
    df_all_sessions = pd.DataFrame()
    for i in range(len(eeg_data)):
        print(i)
        df = pd.DataFrame(eeg_data[i]['eeg_data_info']['eeg_data_values'])
        df['Session'] = "Session " + str(i+1)
        df_all_sessions = pd.concat([df_all_sessions, df], axis=0)
    print("finito")
    return df_all_sessions.to_dict('records')

@app.post("/render_plot1/")
async def render_plot1(eeg_data: str = Form()):
    print(json.loads(eeg_data))
    return plot_figure11(json.loads(eeg_data))

@app.post("/render_plot2/")
async def render_plot2(eeg_data: str = Form()):
    print("CU2")
    print(json.loads(eeg_data))    
    return plot_figure22(json.loads(eeg_data))

@app.post("/render_plot3/")
async def render_plot3(eeg_data: str = Form()):
    print("CU2")
    print(json.loads(eeg_data))    
    return plot_figure33(json.loads(eeg_data))

@app.post("/render_plot4/")
async def render_plot3(eeg_data: str = Form()):
    return plot_figure44(json.loads(eeg_data))


templates = Jinja2Templates(directory="user_interface/templates")

from re import template
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import requests
from fastapi.middleware.wsgi import WSGIMiddleware

@app.get("/")
async def forward_to_docs():
    return RedirectResponse(url="/docs/", status_code=status.HTTP_302_FOUND)

@app.get("/newsession/{profile_id}")
async def new_session(request: Request, profile_id: str):
    profile_info = json.loads(requests.get(f"https://group208-choose-profile.azurewebsites.net/profile/{profile_id}").text)["profileinfo"]
    return {"profile_info": profile_info, "profile_id": profile_id}
    return templates.TemplateResponse("new_session.html", {"request": request, "profile_info": profile_info, "profile_id": profile_id})

from domain.eeg_app_aggregate.factory_eeg import eegFactoryInstance
from domain.eeg_app_aggregate.repository_eeg import eegRepositoryInstance
from infrastructure.useful_functions import random_eeg_processed_fake_data

# @app.post("/simulate_new_session/")
@app.post("/simulate_new_session/")
async def record_session(profile_id: str = Form(), time: int = Form()):
    new_eeg = eegFactoryInstance.create_eeg(eeg_values=random_eeg_processed_fake_data(int(time)*20)).__dict__
    try:
        eegRepositoryInstance.save_eeg_to_db(eeg_values=new_eeg, profile_id=profile_id)
    except Exception as e:
        return { "status": "success", "message": str(e)}
    return {"status": "success"}
    return RedirectResponse(url=f"/dash/{profile_id}", status_code=status.HTTP_302_FOUND)


# from typing import Optional, List
# # from application.functions import plot_figure3
# import pandas as pd
# from pydantic import Json, BaseModel

# #ass


# app.mount("/user_interface", StaticFiles(directory="user_interface"), name="static")
# templates = Jinja2Templates(directory="user_interface/templates")

# @app.get("/url")
# async def get_url(request: Request):
#     return {"the_url_i_want": "/".join(request.url._url.split("/")[0:3])}

# @app.get("/")
# async def forward_to_docs():
#     return RedirectResponse(url="/docs/", status_code=status.HTTP_302_FOUND)

# app.mount("/dash/{profile_id}", WSGIMiddleware(create_dash_app(requests_pathname_prefix="/dash/{profile_id}").server))