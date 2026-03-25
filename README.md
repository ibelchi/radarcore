# Quantitative Trading Assistant

Aplicació de terminal i Streamlit per al filtratge de valors en dues etapes: Geomètrica i Sentiment per IA.

## Característiques

### 1. Motor Geomètric (Core)
- **Ingesta de dades**: Descàrrega automàtica de dades històriques (2 anys) via `stooq`.
- **Simplificació de corba**: Algorisme de pivots (mínims i màxims locals) usant `PIP/ZigZag`.
- **Pattern Matching**: Detecció de patrons "Bullish Swing" (Low -> Higher High -> Higher Low -> Breakout) mitjançant **Dynamic Time Warping (DTW)**.
- **Ranking**: Classificació dels top 10 valors que millor s'ajusten al patró.

### 2. Anàlisi de Sentiment (IA)
- **Catalitzadors**: Cerca de notícies recents i detecció de Buybacks, Insider Buying, Upgrades, etc.
- **Sentiment Score**: Puntuació de -1 a +1 generada per un LLM.
- **Factor Earnings**: Avís crític si falten menys de 3 dies per als resultats.
- **Fail-Safe**: L'aplicació funciona de manera degradada si la IA no està disponible.

## Instal·lació

1. Clonar el repositori:
   ```bash
   git clone <url-del-repositori>
   cd assessor
   ```

2. Instal·lar dependències:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar les claus d'API:
   Crea un fitxer `.env` basat en el template (o modifica el que ja existeix) amb les teves claus de Google Gemini o OpenAI.

## Ús

Executa l'aplicació amb Streamlit:
```bash
streamlit run app.py
```
O utilitza el fitxer `run_app.bat` en sistemes Windows.

## Arquitectura

- `app.py`: Interfície d'usuari amb Streamlit i Plotly.
- `core/geometric_engine.py`: Lògica de processament de preus i DTW.
- `intelligence/sentiment_analysis.py`: Integració amb LLMs i anàlisi de notícies.
- `tickers.csv`: Llista personalitzable de valors a analitzar.
