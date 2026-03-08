from sys_prompt import SYSTEM_PROMPT
from sys_tools_api import model
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from sys_tools import Context
from sys_respn_format import ResponseFormat
from sys_memory import checkpointer
from langchain_core.messages import HumanMessage
from sys_tools import (
    get_user_location,
    get_specific_location,
    get_weather_for_user,
    get_traffic_for_specific_location,
    get_alarm_for_user
)

tools = [
    get_user_location,
    get_specific_location,
    get_weather_for_user,
    get_traffic_for_specific_location,
    get_alarm_for_user,
]

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=tools,
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "1"
    },
    "verbose": False
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "晚上8点, 我要去南开大悦城"}]},
    config=config,
    context=Context(user_id="1",)
)
print(response["structured_response"].message)

# import sys

# while True:
#     user_input = input(">>> ")

#     if user_input.lower() in ["exit", "quit"]:
#         break

#     print("SYSTEM_PROMPT length:", len(SYSTEM_PROMPT))
#     print("Messages size:", sys.getsizeof({"messages":[{"role":"user","content":user_input}]}))

#     response = agent.invoke(
#         {
#             "messages": [HumanMessage(content=user_input)]
#         },
#         config=config,
#         context=Context(user_id="1")
#     )

#     if "structured_response" in response:
#         print(response["structured_response"].message)

