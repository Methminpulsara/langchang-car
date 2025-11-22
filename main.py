import json
import os
from typing import List

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from model import *

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
COINGECKO_URL = os.getenv("COINGECKO_URL")


def get_crypto_insights(coin_list: List[str]):
    params = {
        "ids": ",".join(coin_list),
        "vs_currency": "usd"
    }

    resp = requests.get(COINGECKO_URL, params=params)

    return resp.json()


response_prompt = ChatPromptTemplate.from_template(
    """
    You are a "CryptoAnalyst AI" - a professional crypto market analyst.

You will be given recent market for data for several crypto currencies (price, market cap, volume, 24h change)

{market_data}

- Provide 3 key_factors and 3 insights per coin
- Base your reasoning on give metrics (e.g, price change %, market cap trends).
    """
)

response_llm = ChatOpenAI(model='meta-llama/llama-3.3-70b-instruct:free',
                          api_key=OPENROUTER_KEY,
                          base_url=OPENROUTER_URL
                          ).with_structured_output(CryptoAnalysisResponse)

response_chain = response_prompt | response_llm  # LCEL - langchain Expression language

resp = response_chain.invoke({'market_data': json.dumps(get_crypto_insights(['bitcoin', 'ethereum']) , indent=2)})
# dump eken wenne return wena json eke STRING krnawa ekh inject wenw promt ekt {----}


print(resp)
