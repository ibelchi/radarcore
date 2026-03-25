import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def fetch_historical_data(tickers, years=2):
    """
    Descarrega les dades històriques dels darrers `years` anys per a una llista de tickers.
    A causa dels recents bloquejos de Yahoo Finance, fa servir l'API gratuïta 'stooq'.
    """
    import pandas_datareader.data as web
    import datetime
    
    data_dict = {}
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * years)
    
    for ticker in tickers:
        df = None
        # Preparem variants per a la cerca (stooq a vegades requereix el sufix .US o similars)
        variants = [ticker] if '.' in ticker else [ticker, f"{ticker}.US"]
        
        for variant in variants:
            try:
                # Baixem de stooq
                df = web.DataReader(variant, 'stooq', start=start_date, end=end_date)
                if not df.empty:
                    # Stooq les ordena de més recents a més antics (decreixent), cal girar l'índex
                    df = df.sort_index(ascending=True)
                    if 'Close' in df.columns:
                        break # Hem tingut èxit
            except Exception:
                pass
                
        if df is not None and not df.empty:
            data_dict[ticker] = df[['Close']].copy()
        else:
            print(f"Avís: No s'han pogut descarregar dades per al ticker {ticker}.")
            
    return data_dict

def get_feature_points(df, order=10):
    """
    Simplifica la corba identificant els extrems locals (Pivots) usant argrelextrema de scipy.
    `order` indica quants dies al voltant s'ha de considerar per ser un màxim o mínim relatiu.
    """
    prices = df['Close'].values
    # Trobem índexs dels mínims i màxims
    local_min_idx = argrelextrema(prices, np.less_equal, order=order)[0]
    local_max_idx = argrelextrema(prices, np.greater_equal, order=order)[0]
    
    # Combinem i treiem duplicats (per si mateix valor dóna dos cops)
    extrema_idx = np.unique(np.concatenate((local_min_idx, local_max_idx)))
    extrema_idx.sort()
    
    # Ens quedem només amb els preus filtrats
    filtered_df = df.iloc[extrema_idx].copy()
    
    # Afegim també l'últim punt actual encara que no sigui un extrem per veure la formació del breakout
    if len(prices) - 1 not in extrema_idx:
        p_last = df.iloc[[-1]]
        filtered_df = pd.concat([filtered_df, p_last])
    
    return filtered_df

def calculate_dtw_score(filtered_df):
    """
    Compara la seqüència dels darrers pivots simplificats amb un patró ideal de "Bullish Swing + Breakout".
    - El patró ideal és: Low -> Higher High -> Higher Low -> Breakout.
    - Els normalitzem de [0 a 1] per a la comparativa amb DTW.
    Retorna la distància (com més baixa, més s'assembla al patró).
    """
    if len(filtered_df) < 4:
        return np.inf  # Si no hi ha prou punts, assignem "infinit" a la distància.

    # Agafem els últims 4 punts de la corba simplificada (intentarem agafar L, H, HL, B)
    # Per asegurar una alternança correcta asseguem que no hi hagi punts plans.
    prices = filtered_df['Close'].values[-4:]
    
    # Normalització (Min-Max) entre 0 i 1 perquè no importi si el preu és 10$ o 1000$
    min_p = np.min(prices)
    max_p = np.max(prices)
    if max_p - min_p == 0:
        return np.inf
    
    normalized_prices = (prices - min_p) / (max_p - min_p)
    
    # El nostre patró Bullish amb intenció de Breakout ideal:
    # 1. Low: 0.0
    # 2. Primera Resistència (High): 0.6
    # 3. Pullback (Higher Low): 0.3
    # 4. Breakout (Superant l'últim màxim): 1.0 (o fins i tot pot pujar més, però amb [0,1] està bé)
    ideal_pattern = np.array([0.0, 0.6, 0.3, 1.0])
    
    # Usant fastdtw per calcular la distància (mesura la diferència de forma, no només lineal)
    distance, _ = fastdtw(normalized_prices.reshape(-1, 1), ideal_pattern.reshape(-1, 1), dist=euclidean)
    
    return distance

def rank_tickers(data_dict):
    """
    Itera sobre les dades de cada ticker, extreu els punts i calcula el seu rating DTW.
    Retorna un DataFrame ordenat de menys a més distància.
    """
    results = []
    
    for ticker, df in data_dict.items():
        if df.empty or len(df) < 30: continue
            
        # Simplifiquem la corba
        filtered_df = get_feature_points(df, order=10)
        
        # Calculem DTW score sobre els darrers pivots
        score = calculate_dtw_score(filtered_df)
        
        # Guardem els resultats
        # També guardem el darrer preu
        current_price = df['Close'].iloc[-1]
        results.append({
            'Ticker': ticker,
            'Price': round(current_price, 2),
            'Geometric Score': score
        })
        
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        # Ordenem: la distància més baixa (més semblant al patró) primer
        results_df = results_df.sort_values(by='Geometric Score', ascending=True)
        # Només top 10
        results_df = results_df.head(10).reset_index(drop=True)
        
    return results_df

# Testing bloc (es podria borrar o posar en scripts/test)
if __name__ == "__main__":
    tks = ["AAPL", "MSFT", "GOOGL"]
    print("Descarregant dades per fer un test ràpid...")
    d = fetch_historical_data(tks, years=1)
    ranking = rank_tickers(d)
    print("\nRanking provisional (sense sentiment):")
    print(ranking)
