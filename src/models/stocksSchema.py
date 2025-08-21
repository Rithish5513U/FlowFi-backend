from pydantic import BaseModel

class StockData(BaseModel):
    symbol: str
    open: float
    dayHigh: float
    dayLow: float
    lastPrice: float
    previousClose: float
    change: float
    pChange: float
