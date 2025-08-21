import yfinance as yf
from typing import List
from models.stocksSchema import StockData
from models.userModel import User
from extensions import db

users = db['users']
SYMBOLS = [
        "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
        "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
        "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", 
        "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", 
        "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", 
        "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS", 
        "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", 
        "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", 
        "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", 
        "SBIN.NS", "SHREECEM.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", 
        "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", 
        "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
    ]

def fetchStocks(symbols = SYMBOLS) -> List[StockData]:
    stocks = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info

            last_price = info.get("last_price", 0)
            previous_close = info.get("previous_close", 0)

            change = round(last_price - previous_close, 2)
            pchange = round((change / previous_close) * 100, 2) if previous_close else 0

            stock = StockData(
                symbol=symbol,
                open=info.get("open"),
                dayHigh=float(info.get("day_high") or 0.0),
                dayLow=float(info.get("day_low") or 0.0),
                lastPrice=last_price,
                previousClose=previous_close,
                change=change,
                pChange=pchange,
            )
            stocks.append(stock)

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return stocks

def save_user(user: User) -> bool:
    try:
        result = users.update_one(
            {"email": user.email},
            {"@set": user.model_dump()}
        )
        
        return result.modified_count == 1
    
    except Exception as e:
        print(f"Error saving user: {e}")
        return False
