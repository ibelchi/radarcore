import os
import datetime
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

# Constants
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# Initialization for LLM providers
if LLM_PROVIDER == "gemini":
    from google import genai
    # Note: genai client is initialized down in the function to avoid errors if key isn't set yet
elif LLM_PROVIDER == "openai":
    import openai
# Ollama could be called via requests module directly

def get_llm_response(prompt: str) -> str:
    """
    Wrapper que escull el proveedor de IA configurat i envia el prompt.
    Té degradació gràcil: si falla, retorna un error string que serà gestionat amunt.
    """
    try:
        if LLM_PROVIDER == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key == "tu_clau_de_gemini_aqui":
                raise Exception("API Key de Gemini no configurada.")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text

        elif LLM_PROVIDER == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("API Key d'OpenAI no configurada.")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif LLM_PROVIDER == "ollama":
            import requests
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama3")
            res = requests.post(f"{host}/api/generate", json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })
            if res.status_code == 200:
                return res.json().get("response", "")
            else:
                raise Exception(f"Ollama error: {res.status_code}")
        else:
            raise Exception("Proveïdor LLM desconegut.")
            
    except Exception as e:
        print(f"Error LLM ({LLM_PROVIDER}): {str(e)}")
        return "ERROR_LLM"

def analyze_catalysts(ticker: str):
    """
    Busca notícies recents via yfinance, construeix el prompt per analitzar catalitzadors 
    i extreu un Sentiment Score (-1 a 1).
    Retorna: (sentiment_score, catalysts_found_list)
    """
    try:
        tk = yf.Ticker(ticker)
        # Obtenir notícies
        news = tk.news
        if not news:
            return 0, "Sense notícies recents"
            
        headlines = [item.get("title", "") for item in news[:10]] # últims 10 titulars
        news_text = "\\n- ".join(headlines)
        
        prompt = f"""
Actua com un analista quantitatiu professional. Aquí tens els darrers titulars de {ticker}:
- {news_text}

Analitza si hi ha algun d'aquests catalitzadors crítics: 'Share Buybacks', 'Insider Buying', 'Guidance Upgrades', 'Class Action Suits', o 'Management Changes'.
1. Assigna un "Sentiment Score" estrictament numèric entre -1.0 (molt negatiu) i +1.0 (molt positiu). Si és neutral o no hi ha catalitzadors rellevants, assigna 0.0.
2. Llista breument els catalitzadors detectats en poques paraules.

Estructura exactament la teva resposta així (sense introduccions ni altres paraules):
SCORE: [número]
CATALITZADORS: [text breu o 'Cap detectat']
"""
        response = get_llm_response(prompt)
        
        if response == "ERROR_LLM":
            return None, "Sentiment: No disponible"
            
        # Parse output
        parts = response.split('\\n')
        score = 0.0
        cats = "Cap detectat"
        for p in parts:
            if "SCORE:" in p.upper():
                try:
                    score_str = p.upper().replace("SCORE:", "").strip()
                    score = float(score_str)
                except:
                    pass
            elif "CATALITZADORS:" in p.upper() or "CATALIZADORES:" in p.upper():
                cats = p.upper().replace("CATALITZADORS:", "").replace("CATALIZADORES:", "").strip()
                
        return score, cats
        
    except Exception as e:
        print(f"Error analitzant catalitzadors per {ticker}: {e}")
        return None, "Sentiment: No disponible"

def check_earnings(ticker: str):
    """
    Cerca la propera data d'earnings. 
    Retorna '(Data) - AVÍS CRÍTIC' si queden menys de 3 dies, sinó '(Data)' o 'N/A'.
    """
    try:
        tk = yf.Ticker(ticker)
        has_earnings = tk.calendar
        # Dependrà de la versió de yfinance. De vegades retorna un dict o dataframe
        """
        Amb yfinance nou, tk.calendar pot retornar un dict amb "Earnings Date".
        """
        # A yfinance 0.2.x, 'tk.calendar' sovint no va bé directament, intentem fer servir tk.earnings_dates
        edts = tk.get_earnings_dates(limit=5)
        if edts is not None and not edts.empty:
            # Agafem les dates futures
            now = datetime.datetime.now(datetime.timezone.utc)
            future_dates = edts[edts.index > now].index.sort_values()
            
            if len(future_dates) > 0:
                next_date = future_dates[0]
                days_left = (next_date - now).days
                date_str = next_date.strftime("%Y-%m-%d")
                
                if days_left <= 3:
                    return f"{date_str} (AVÍS CRÍTIC: <3 dies)"
                else:
                    return f"{date_str} ({days_left}d)"
        
        return "N/A"
    except Exception as e:
        return "N/A"
