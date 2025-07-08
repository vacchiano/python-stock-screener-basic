import yfinance as yf
from tabulate import tabulate

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    try:
        info = stock.get_info()
        market_cap = info.get("marketCap", None)
        enterprise_value = info.get("enterpriseValue", None)
        total_cash = info.get("totalCash", None)


        ev_cash_ratio = (enterprise_value / total_cash) if enterprise_value and total_cash else None

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


    return {
        "Ticker": ticker,
        "Market Cap": market_cap,
        "EV": enterprise_value,
        "Cash": total_cash,
        "EV/Cash": ev_cash_ratio,
    }

def format_number(num):
    if num is None:
        return "-"
    
    is_neg = num < 0
    num = abs(num)

    if num > 1e9:
        formatted = f"${num/1e9:.1f}B"
    elif num > 1e6:
        formatted = f"${num/1e6:.1f}M"
    else:
        formatted = f"${num:,.0f}"

    return f"-{formatted}" if is_neg else formatted

def main():
    with open("tickers.txt") as f:
        tickers = [line.strip().upper() for line in f if line.strip()]

    results = []
    for ticker in tickers:
        data = get_stock_data(ticker)
        results.append([
            data["Ticker"],
            format_number(data["Market Cap"]),
            format_number(data["EV"]),
            format_number(data["Cash"]),
            f"{data['EV/Cash']:.2f}" if data["EV/Cash"] else "-",
        ])

    headers = ["Tickers", "Market Cap", "EV", "Cash", "EV/Cash"]
    print(tabulate(results, headers=headers, tablefmt="pretty"))

if __name__ == "__main__":
    main()