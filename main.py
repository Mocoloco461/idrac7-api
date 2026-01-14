import requests
import urllib3
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IP = os.getenv("IP")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


# power on/off
def onoff(mode:str):
    response = requests.post(
        f"https://{IP}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        auth=(USER,PASSWORD),
        json={"ResetType": f"{mode}"},
        verify=False,
        timeout=10
    )
    if response.status_code in [200,204]:
        return {"message": f"The server is turned {mode}", "statut_code":response.status_code}
    return {"error": "Failed to execute command", "details": response.text, "status_code": response.status_code}




@app.get("/status")
def status():
    response = requests.get(
        f"https://{IP}/redfish/v1/Systems/System.Embedded.1",
        auth=(USER,PASSWORD),
        verify=False,
        timeout=10
    )
    data = response.json()
    server_status = data.get("PowerState")
    return {"Status":server_status}


@app.post("/on")
def power_on():
    return onoff("On")

@app.post("/off")
def power_off():
    return onoff("GracefulShutdown")
