from dataclasses import dataclass
from typing import Optional


@dataclass
class ResponseFormat:
    """
    Structured response schema for the life assistant agent.
    """

    # Main message returned to the user
    message: str

    # User location retrieved from get_user_location
    user_location: Optional[str] = None

    # Destination resolved from get_specific_location
    destination: Optional[str] = None

    # Weather information retrieved from get_weather_for_user
    weather_summary: Optional[str] = None

    # Traffic information retrieved from get_traffic_for_specific_location
    traffic_summary: Optional[str] = None

    # Whether an alarm/reminder was created
    alarm_created: bool = False