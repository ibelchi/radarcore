import yfinance as yf
import pandas as pd
import requests
from io import StringIO
import logging

logger = logging.getLogger(__name__)

def get_sp500_symbols() -> list:
    """Obtenir la llista actual de símbols del S&P 500 des de la Viquipèdia."""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        # Alguns símbols tenen punts en lloc de guions a yfinance (ej. BRK.B -> BRK-B)
        symbols = df['Symbol'].str.replace('.', '-', regex=False).tolist()
        return symbols
    except Exception as e:
        logger.error(f"Error obtenint símbols del S&P500: {e}")
        return []

def get_market_symbols(market: str) -> list:
    """
    Obtenir llista de símbols segons el mercat seleccionat. 
    Utilitza llistes hardcodejades on l'scraping és fràgil per mantenir la simplicitat màxima.
    """
    market = market.lower()
    
    if market == "sp500":
        return get_sp500_symbols()
        
    hardcoded_markets = {
        "ibex35": ["ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRIF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUI.MC", "REP.MC", "ROVI.MC", "SCYR.MC", "SOL.MC", "TEF.MC", "UNI.MC"],
        "dax40": ["ADS.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BEI.DE", "BMW.DE", "BNR.DE", "CBK.DE", "CON.DE", "1COV.DE", "DTG.DE", "DBK.DE", "DB1.DE", "DPW.DE", "DTE.DE", "EOAN.DE", "FRE.DE", "HNR1.DE", "HEI.DE", "HEN3.DE", "IFX.DE", "MRK.DE", "MBG.DE", "MTX.DE", "MUV2.DE", "PAH3.DE", "PUM.DE", "QIA.DE", "RHM.DE", "RWE.DE", "SAP.DE", "SRT.DE", "SIE.DE", "ENR.DE", "SHL.DE", "SY1.DE", "VOW3.DE", "VNA.DE", "ZAL.DE"],
        "eurostoxx50": ["ADS.DE", "ADYEN.AS", "AD.AS", "AI.PA", "ALV.DE", "ABI.BR", "ASML.AS", "CS.PA", "BAS.DE", "BAYN.DE", "BBVA.MC", "SAN.MC", "BMW.DE", "BNP.PA", "CRG.IR", "DTE.DE", "DPW.DE", "ENEL.MI", "ENI.MI", "FLTR.IR", "EL.PA", "RMS.PA", "IBE.MC", "ITX.MC", "IFX.DE", "INGA.AS", "ISP.MI", "KER.PA", "OR.PA", "MC.PA", "MBG.DE", "MUV2.DE", "PHIA.AS", "PRX.AS", "SAF.PA", "SAN.PA", "SAP.DE", "SU.PA", "SIE.DE", "STE.PA", "STMPA.PA", "TTE.PA", "VCI.PA", "VOW3.DE", "VNA.DE", "NOKIA.HE"],
        "nifty50": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "AXISBANK.NS", "HCLTECH.NS", "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "WIPRO.NS", "ULTRACEMCO.NS", "NTPC.NS", "POWERGRID.NS", "M&M.NS", "TATASTEEL.NS", "CIPLA.NS", "HEROMOTOCO.NS", "EICHERMOT.NS", "GRASIM.NS", "DIVISLAB.NS", "BAJAJFINSV.NS", "BPCL.NS", "BRITANNIA.NS", "COALINDIA.NS", "DRREDDY.NS", "HINDALCO.NS", "INDUSINDBK.NS", "ONGC.NS", "TATAMOTORS.NS", "UPL.NS", "JSWSTEEL.NS", "HDFCLIFE.NS", "SBILIFE.NS", "APOLLOHOSP.NS", "ADANIPORTS.NS", "TECHM.NS"]
    }
    
    if market in hardcoded_markets:
        return hardcoded_markets[market]
        
    if market == "nasdaq100":
        try:
            url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            tables = pd.read_html(StringIO(res.text), match='Ticker')
            return tables[0]['Ticker'].str.replace('.', '-', regex=False).tolist()
        except Exception as e:
            logger.error(f"Error scraping NASDAQ: {e}")
            return ["AAPL", "MSFT", "GOOG", "AMZN", "META", "NVDA", "TSLA", "AVGO", "COST", "PEP", "CSCO"]
            
    if market == "nikkei225":
        try:
            url = 'https://en.wikipedia.org/wiki/Nikkei_225'
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            tables = pd.read_html(StringIO(res.text))
            for df in tables:
                if 'Ticker' in df.columns or 'Code' in df.columns:
                    col = 'Ticker' if 'Ticker' in df.columns else 'Code'
                    return (df[col].astype(str) + ".T").tolist()
            return []
        except Exception as e:
            logger.error(f"Error scraping Nikkei 225: {e}")
            return ["7203.T", "6758.T", "9984.T", "8306.T", "9432.T", "7974.T", "8035.T"]
            
    return []

def get_historical_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Obtenir dades històriques EOD (End of Day) per a un símbol específic.
    period format aleviat de yfinance (e.g. '1mo', '3mo', '6mo', '1y', '2y')
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            logger.warning(f"No hi ha dades històriques per {symbol}")
        return df
    except Exception as e:
        logger.error(f"Error obtenint dades de {symbol}: {e}")
        return pd.DataFrame()

def get_company_info(symbol: str) -> dict:
    """Obtenir informació bàsica de l'empresa (capitalització, sector, etc.)."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "market_cap": info.get("marketCap", 0),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "short_name": info.get("shortName", symbol),
            "currency": info.get("currency", "USD")
        }
    except Exception as e:
        logger.error(f"Error obtenint informació de la companyia {symbol}: {e}")
        return {}
