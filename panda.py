import os

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# Load into a panda dataframe the csv user_info.csv

df = pd.read_csv("1500000_Sales_Records.csv")
open_ai_api_key = os.environ.get("OPENAI_API_KEY")


# Instantiate a LLM


llm = OpenAI(api_token=open_ai_api_key)

df = SmartDataframe(df, config={"llm": llm, "save_charts": True})
# print("Number of rows:")
# print(df.chat("How many lines in the file?"))
# print("Top 10 countries by profit")
# print(
#     df.chat(
#         "Give me the top 10 country per profit and give me the total number of sales for each country"
#     )
# )
# print("Average price per country per Item Type")
# print(df.chat("What is the average price per country per Item Type, limit to 20"))
print(
    df.chat(
        "Plot the average profit per country limit to 20 and put the item type volume"
    )
)
