from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from sys_tools_api import get_wea
from sys_tools_api import get_city_code
from sys_tools_api import get_city_ll
from sys_tools_api import get_traffic_info
from sys_tools_api import get_alarm_user
@dataclass
class Context:
    """
    Runtime context passed into tools.

    This can contain information retrieved from the system,
    such as user identity and device-provided location.
    """
    user_id: str
    user_location: str | None = None


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """
    Get the user's current location by prompting input from the keyboard.
    Get the user's current location using IP geolocation.
    """

    location = input("\n请输入您的当前位置: ").strip()
    runtime.context.user_location = location
    print("\n获取用户实时位置已完成\n")

    return location


@tool
def get_specific_location(destination: str) -> str:
    """
    Resolve a place name mentioned by the user into a precise
    geographic location using a map geocoding service.

    Example:
    "Apple Park" -> "Apple Park, Cupertino, CA"
    """

    print("获取目的地已完成\n")

    return destination


@tool
def get_weather_for_user(runtime: ToolRuntime[Context]) -> str:
    """
    Retrieve real-time weather conditions for the user's location
    using a weather API service.
    """
    location = runtime.context.user_location

    if location is None:
        return "User location not available."
    city_code = get_city_code(location)
    print("结构地址转换模块已完成\n")
    data = get_wea(city_code)

    if data["status"] == "1":
        weather = data["lives"][0]
        print("获取用户位置实时天气已完成 \n")
        return f"{weather['city']} 当前天气 {weather['weather']}，气温 {weather['temperature']}°C"

    return "无法获取天气"

@tool
def get_traffic_for_specific_location(
    destination: str,
    runtime: ToolRuntime[Context]
) -> str:
    """
    Retrieve real-time traffic conditions between the user's
    current location and the specified destination using
    a map or navigation API.
    """

    user_location = runtime.context.user_location
    origin = get_city_ll(user_location)
    destination = get_city_ll(destination)
    print("具体地址转换经纬度已完成\n")
    traffic_info = get_traffic_info(origin, destination)
    print("交通路况查询已完成\n")

    return traffic_info

@tool
def get_alarm_for_user(time: str, message: str, runtime: ToolRuntime[Context]) -> str:
    """
    Create a reminder or alarm for the user at a specified time.

    This interacts with the user's reminder, calendar, or notification system.
    """

    user_id = runtime.context.user_id
    get_alarm_user(time, message)
    print("\n用户提醒已设置\n")

    return f"Alarm created for user {user_id} at {time}: {message}"
