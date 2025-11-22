from typing import List, Literal

from pydantic import BaseModel, Field


class CryptoAnalysisRequest(BaseModel):
    coins: List[str] = Field(..., description="Provide the list of coins to be analyzed")


class CryptoCompareRequest(CryptoAnalysisRequest):
    pass


class CryptoComparison(BaseModel):
    winner: str
    summary: str
    reasons: List[str]


class CryptoComparisonResponse(BaseModel):
    comparison: CryptoComparison


class MarketFactor(BaseModel):
    factor: str = Field(
        description="A short, concise name or description of the market factor influencing the asset."
    )
    impact: str = Field(
        description="A clear explanation of how this factor affects the coin’s price or market behavior."
    )


class CryptoInsights(BaseModel):
    prediction: str = Field(
        description="A specific prediction or notable insight about the coin's potential price movement."
    )
    confidence: int = Field(
        ...,
        le=100,
        ge=0,
        description="Confidence level for the prediction (0–100)."
    )


class CoinMarketAnalysis(BaseModel):
    coin: str = Field(
        description="Name of the cryptocurrency being analyzed."
    )
    summary: str = Field(
        description="A concise summary of the coin’s current market status and performance."
    )
    sentiment: Literal["bullish", "bearish", "neutral"]
    key_factors: List[MarketFactor] = Field(
        description="A list of key market factors currently influencing the coin."
    )
    insights: List[CryptoInsights] = Field(
        description="A list of predictions and insights related to the coin’s future market behavior."
    )


class CryptoAnalysisResponse(BaseModel):
    analysis: List[CoinMarketAnalysis] = Field(
        description="Full market analysis results for all requested cryptocurrencies."
    )
