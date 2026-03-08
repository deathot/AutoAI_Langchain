from langchain_deepseek import ChatDeepSeek
import os
import requests
import subprocess
from langchain_deepseek import ChatDeepSeek

os.environ["DEEPSEEK_API_KEY"] = "your api key"
web_api_key = "your api key"

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def get_wea(city: str) -> dict:
    url_wea = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
    params_wea = {
        "key": web_api_key,
        "city": city,
        "extensions":"base",
    }
    res_wea = requests.get(url_wea, params=params_wea)
    return res_wea.json()

def get_city_code(city: str) -> int:
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    params = {
        "key": web_api_key,
        "address": city
    }
    res = requests.get(url, params=params).json()
    return res["geocodes"][0]["adcode"]

def get_city_ll(city: str) -> int:
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    params = {
        "key": web_api_key,
        "address": city
    }
    res = requests.get(url, params=params).json()
    return res["geocodes"][0]["location"]

def get_traffic_info(origin, destination):
    url = "https://restapi.amap.com/v5/direction/driving?parameters"
    params = {
        "key": web_api_key,
        "origin": origin,
        "destination": destination,
        "strategy": 2,
        "show_fields": "cost,tmcs"
    }
    res = requests.get(url, params=params).json()
    return res

def get_alarm_user(time_str, message):

    script = (
        'tell application "Reminders"\n'
        'activate\n'
        'if not (exists list "AI") then\n'
        'make new list with properties {name:"AI"}\n'
        'end if\n'
        'tell list "AI"\n'
        f'make new reminder with properties {{name:"{message}", remind me date:date "{time_str}"}}\n'
        'end tell\n'
        'end tell'
    )
    subprocess.run(["osascript", "-e", script])
    return "\n"