from dotenv import load_dotenv
import os
import requests

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_price(symbol: str) -> str:
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "price" in data:
        return f"The price of {symbol} is ${data['price']}."
    else:
        return f"Could not fetch the price for {symbol}. Reason: {data.get('message', 'Unknown error')}"

def get_earnings_report(symbol: str) -> str:
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        report = data[0]
        return (
            f"Earnings Report for {symbol}:\n"
            f"Date: {report.get('date', 'N/A')}\n"
            f"Revenue: ${report.get('revenue', 'N/A'):,}\n"
            f"Net Income: ${report.get('netIncome', 'N/A'):,}\n"
            f"EPS: {report.get('eps', 'N/A')}\n"
            f"Link to Report: https://financialmodelingprep.com/financial-summary/{symbol}"
        )
    else:
        return f"Could not fetch earnings report for {symbol}."

def get_company_news(company: str) -> list:
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company}&pageSize=5&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok":
        articles = data.get("articles", [])
        news_list = []
        for article in articles:
            news_list.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt")
            })
        return news_list
    else:
        return []

def get_dividend_yield(symbol: str) -> str:
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=1&apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        metrics = data[0]
        dividend_yield = metrics.get("dividendYield")
        if dividend_yield is not None:
            dividend_percent = round(dividend_yield * 100, 2)
            return f"Dividend Yield for {symbol} is {dividend_percent}%."
        else:
            return f"No dividend yield data available for {symbol}."
    else:
        return f"Could not fetch dividend yield for {symbol}."
