from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from models.vehicle import Car, CarResponse, CarAnalysis
from fastapi import FastAPI

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")

summerlize_llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_KEY"),
    base_url="https://openrouter.ai/api/v1",  # MUST be root URL
    model="meta-llama/llama-3.3-70b-instruct:free"
)

summarizer_promt = ChatPromptTemplate.from_template(
    """Extract car price in rupees, manufacture year, and mileage for the given car model:
                {car_model}

                Using this information:
                {docs}
            """
)

summarize_chain = summarizer_promt | summerlize_llm

response_pormt = ChatPromptTemplate.from_template(
    """
You are an automotive assistance helping users find the best car deals.
Here is a summarized list of car ads for {car_model}.

{summary}

Highlight key insight, provide a 2-3 summary , also provide best average price to buy
""")

anaylize_llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="meta-llama/llama-3.3-70b-instruct:free"
).with_structured_output(CarResponse)

analysis_chain = response_pormt | anaylize_llm

app = FastAPI()


@app.get("/car-ads/{car_model}", response_model=CarResponse)
def car_analysis(car_model: str):


    urls = [
        f"https://ikman.lk/en/ads?query={car_model}",
        f"https://patpat.lk/en/sri-lanaka/vehicle/car/toyota/{car_model}"
    ]
    website_loader = WebBaseLoader(urls)
    docs = website_loader.load()

    ads_summary = summarize_chain.invoke({
        "car_model": car_model,
        "docs": "\n".join([doc.page_content for doc in docs])
    })

    # Promt eke dena vearibels names match wenn one
    final_output = analysis_chain.invoke({"car_model": car_model,
                                          "summary": ads_summary
                                          })

    return final_output
