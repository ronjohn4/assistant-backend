import json
import urllib.error
# import urllib.parse
import urllib.request
from pydantic import BaseModel, Field

from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.config import Config



ACTIONTYPE_CODES = {
    "pomodoro": 9,
    "stairclimber": 8,
    "weights": 7,
    "walk": 6,
    "coffee": 5,
    "sleep": 4,
    "bm": 3,
    "pee": 2,
    "water": 1,
}


#-------------------------------------------------------------------
# MyData tool
#-------------------------------------------------------------------
class MyDataResult(BaseModel):
    """Structured result"""
    text_response: str = Field(description="confirmation that the request was received"),


class MyDataInput(BaseModel):
    qty: str = Field(description="The quantity related to this action.")
    action_type: str = Field(description="The action taken.  Needs to be one of: water, pee, bm, sleep, coffee, walk, weights, stairclimber, pomodoro")

    # parser.add_argument("description_start", type=str, required=False, help="description_start problem (not required)")
    # parser.add_argument("description_end", type=str, required=False, help="description_end problem (not required)")
    # parser.add_argument("default_qty", type=str, required=False, help="default_qty problem (not required)")
    # parser.add_argument("uom", type=str, required=False, help="uom problem (not required)")
    # parser.add_argument("url", type=str, required=False, help="url problem (not required)")
    # parser.add_argument("group", type=int, required=False, help="group problem (not required)")
    # parser.add_argument("order", type=int, required=False, help="order problem (not required)")


@tool("mydata_tool", args_schema=MyDataInput, description="Used to log actions like eating and exercise.")
def mydata_tool(qty: str, action_type: str) -> MyDataResult:
    """Log personal actions like exercise and eating."""


    actiontypeid = ACTIONTYPE_CODES.get(action_type, None)

    try:
        with urllib.request.urlopen(f"{Config.API_BASE_URL}/api/actiontypes/{actiontypeid}") as response:
            if response.status != 200:
                pass
            action_type_data = json.loads(response.read().decode("utf-8"))

        payload = {
            "log_date": None,
            "event_date": None,    
            "qty": action_type_data['default_qty'],
            "actiontypeid": actiontypeid,
            "lat": None,
            "long": None
        }

        request = urllib.request.Request(
            f"{Config.API_BASE_URL}/api/actions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            if response.status != 201:
                pass

        result = MyDataResult(
            text_response=""
        )

        return result.model_dump_json()
    
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        return f"Could not log action '{action_type}': {e}."


# Need to comment out the @tool() decorator if calling directly
if __name__ == "__main__":
   print(mydata_tool("Pomodoro"))
