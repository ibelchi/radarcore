import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.geometric_engine import fetch_historical_data, rank_tickers, get_feature_points
from intelligence.sentiment_analysis import analyze_catalysts, check_earnings
import os

st.set_page_config(page_title="Quant Assistant", layout="wide")

st.title("📈 Quantitative Trading Assistant")
st.markdown("Aquesta aplicació filtra tickers aplicant algoritmes geomètrics (DTW + ZigZag/PIP) i anàlisi de sentiment via IA.")

def load_tickers_from_csv(path="tickers.csv"):
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "Ticker" in df.columns:
            return df["Ticker"].tolist()
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuració")
    # Carregar llista base
    base_tickers = load_tickers_from_csv()
    
    # Text_area per permetre afegir o treure de forma ràpida a la UI
    tickers_input = st.text_area("Llista de Tickers (separats per coma)", value=", ".join(base_tickers))
    tickers_list = [x.strip().upper() for x in tickers_input.split(",") if x.strip()]
    
    run_btn = st.button("Executar Anàlisi", type="primary")

# --- UI PRINCIPAL ---
if 'ranking_df' not in st.session_state:
    st.session_state.ranking_df = pd.DataFrame()
if 'raw_data_dict' not in st.session_state:
    st.session_state.raw_data_dict = {}

if run_btn:
    if not tickers_list:
        st.warning("Per favor, introdueix com a mínim un ticker.")
    else:
        with st.spinner('Descarregant dades històriques i aplicant filtre geomètric (DTW)...'):
            # Iniciar el Core Geometric Module
            data_dict = fetch_historical_data(tickers_list, years=2)
            st.session_state.raw_data_dict = data_dict
            
            if data_dict:
                ranking_df = rank_tickers(data_dict)
                st.session_state.ranking_df = ranking_df
            else:
                st.error("No s'han pogut descarregar dades. Revisa si l'origen yfinance està limitant la IP (Rate Limit).")

        # Procedim al Sentiment si tenim ranking
        if not st.session_state.ranking_df.empty:
            with st.spinner('Realitzant Anàlisi de Sentiment i Cercant Earnings...'):
                # Ara apliquem sentiment als top d'aquest dataframe iterativament
                sentiments = []
                catalysts_list = []
                earnings_list = []
                
                for tk in st.session_state.ranking_df["Ticker"]:
                    # Sentiment Analysis
                    sc, ct = analyze_catalysts(tk)
                    sentiments.append(sc if sc is not None else "N/A")
                    catalysts_list.append(ct)
                    
                    # Earnings check
                    er = check_earnings(tk)
                    earnings_list.append(er)
                    
                st.session_state.ranking_df["Sentiment (IA)"] = sentiments
                st.session_state.ranking_df["Catalitzadors Clau"] = catalysts_list
                st.session_state.ranking_df["Earnings Date"] = earnings_list
                
        st.success("Anàlisi Completada!")

# MOSTRAR RESULTATS
if not st.session_state.ranking_df.empty:
    st.subheader("Top Tickers segons Bullish Swing DTW")
    
    # Fem que la taula es vegi maca amb format
    st.dataframe(
        st.session_state.ranking_df,
        column_config={
            "Geometric Score": st.column_config.NumberColumn(
                "Geom. Score",
                help="Distància DTW vers el patró ideal. Com més petit millor.",
                format="%.2f"
            ),
            "Price": st.column_config.NumberColumn(format="$%.2f")
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    st.subheader("Visualització Geomètrica")
    # Selecció per veure la gràfica d'un dels tickers de la taula
    selected_ticker = st.selectbox("Selecciona un ticker per veure la simplificació:", st.session_state.ranking_df["Ticker"].tolist())
    
    if selected_ticker and selected_ticker in st.session_state.raw_data_dict:
        df_real = st.session_state.raw_data_dict[selected_ticker]
        df_pivots = get_feature_points(df_real, order=10)
        
        # Plotly chart
        fig = go.Figure()
        
        # Línia real
        fig.add_trace(go.Scatter(
            x=df_real.index, 
            y=df_real['Close'], 
            mode='lines', 
            name='Preu Real',
            line=dict(color='blue', width=1)
        ))
        
        # Línia ZigZag
        fig.add_trace(go.Scatter(
            x=df_pivots.index, 
            y=df_pivots['Close'], 
            mode='lines+markers', 
            name='ZigZag / Pivots',
            line=dict(color='orange', width=2),
            marker=dict(size=6, color='red')
        ))
        
        fig.update_layout(
            title=f"Simplificació de la Corba per a {selected_ticker}",
            xaxis_title="Data",
            yaxis_title="Preu de Tancament ($)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
