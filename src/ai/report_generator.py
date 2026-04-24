from dotenv import load_dotenv
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.ai.rag_engine import RAGEngine

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, provider: str = "google", model_name: str = "gemini-flash-latest", api_key: str = None):
        """
        Initializes the LLM report generator with multiple provider support.
        :param provider: 'google' or 'openai'
        :param model_name: Name of the model (e.g., 'gemini-1.5-flash' or 'gpt-4o')
        :param api_key: Optional API key (overrides environment variable)
        """
        # If no key is provided, try to get it from environment
        if not api_key:
            if provider == "google":
                api_key = os.getenv("GOOGLE_API_KEY", "").strip()
            elif provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY", "").strip()

        if provider == "google":
            self.llm = ChatGoogleGenerativeAI(
                model=model_name, 
                temperature=0.2,
                google_api_key=api_key if api_key else None
            )
        elif provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.2,
                api_key=api_key if api_key else None
            )
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

        self.rag = RAGEngine()
        
    def generate_report(self, symbol: str, strategy_name: str, tech_reason: str, current_price: float, metrics: dict = None, language: str = "English") -> str:
        """Groups RAG knowledge with technical findings to provide a summary in the selected language."""
        
        # Consult the RAG knowledge base for user criteria
        # or general advice on swing trading and the specific strategy.
        user_knowledge = self.rag.similarity_search(f"Investment criteria and risk factors for {strategy_name} in stocks", k=3)
        
        # Ensure default empty dictionary for metrics
        metrics = metrics or {}
        
        prompt = PromptTemplate.from_template("""
You are an Expert Equity Analyst & Data Engineer specializing in swing trading.

Your task is to generate a structured fundamental analysis report to accompany the detected trading signal.

CURRENT MARKET DATA (FRESH):
Ticker: {symbol}
Current Price: {current_price}
Recent High ({lookback_days} days): {period_high}
Recent Low ({lookback_days} days): {period_low}
Drop: {drop_pct}% | Rebound: {rebound_pct}%
Market Cap: {market_cap} B USD
Average Volume: {volume} M
PER (Trailing): {per}
EPS (Forward): {eps}
Dividend Yield: {dividend_yield}%
Next Earnings: {next_earnings}

THEORETICAL KNOWLEDGE AND USER CRITERIA (RAG):
{user_knowledge}

---
STRUCTURE INSTRUCTIONS:
Generate the report exactly with these points. It is CRUCIAL to label each data source:

1. Executive Summary and Score (CONTEXTUAL/SYNTHETIC DATA):
   - Fundamental Score: [0-100]
   - Fundamental Risk Level: [Low / Medium / High / Critical]
   - One-sentence thesis.

2. Risk Calendar and Catalysts (FRESH DATA):
   - Next Earnings: {next_earnings} (Alert if < 7 days).
   - Ex-Dividend Date: {dividend_yield}% (Current dividend).

3. Financial Health and Valuation (MIXED DATA):
   - EPS: {eps} and PER: {per} (FRESH DATA).
   - General Health, Debt, and Margins (CONTEXTUAL DATA based on Gemini model: Evaluate according to your knowledge of the ticker).

4. "Smart Money" Flow (CONTEXTUAL DATA):
   - Institutional Ownership, Insider Trading, and Analyst Sentiment.
   - (This section is based exclusively on model training data, not real-time).

5. Sectorial Context (CONTEXTUAL DATA):
   - Relative Sector Strength and Macro correlations.

6. Final Summary and Verdict:
   - Pros and Cons.
   - Fundamental Verdict: [APPROVED / CAUTION / DISCARDED].

---
CRITICAL LOGIC:
* If current data is bad despite the chart, be cautious.
* If the RAG context says you don't want to invest in this company, the verdict must be DISCARDED.
* Always respond in {language}.

---
TRANSPARENCY NOTICE AT THE END OF THE REPORT (in {language}):
Always add a note indicating that sections marked as 'CONTEXTUAL' are based on the AI model's knowledge and may not reflect last-minute corporate changes.
""")
        
        formatted_prompt = prompt.format(
            symbol=symbol,
            strategy_name=strategy_name,
            current_price=metrics.get("current_price", current_price),
            tech_reason=tech_reason,
            user_knowledge=user_knowledge,
            lookback_days=metrics.get("lookback_days", "?"),
            period_high=metrics.get("period_high", "?"),
            period_low=metrics.get("period_low", "?"),
            drop_pct=round(metrics.get("drop_pct", 0), 2) if metrics.get("drop_pct") is not None else "?",
            rebound_pct=round(metrics.get("rebound_pct", 0), 2) if metrics.get("rebound_pct") is not None else "?",
            market_cap=round(metrics.get("market_cap", 0), 2) if metrics.get("market_cap") is not None else "?",
            volume=round(metrics.get("volume", 0), 2) if metrics.get("volume") is not None else "?",
            per=metrics.get("per", "N/A"),
            eps=metrics.get("eps", "N/A"),
            dividend_yield=metrics.get("dividend_yield", "N/A"),
            next_earnings=metrics.get("next_earnings", "N/A"),
            language=language
        )
        
        import time
        for attempt in range(2): # Try twice
            try:
                response = self.llm.invoke(formatted_prompt)
                content = response.content
                if isinstance(content, list):
                    # Concatenate all text parts if the response is a list
                    content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
                return content
            except Exception as e:
                err_msg = str(e).lower()
                if "resource_exhausted" in err_msg or "429" in err_msg:
                    if attempt == 0:
                        logger.warning(f"Rate limit hit for {symbol}. Retrying in 15s...")
                        time.sleep(15)
                        continue
                    else:
                        return f"Error: API Quota Exceeded (429). You are on a Free Tier and have exceeded the limits for this model. Please wait a minute or switch to 'gemini-flash-latest' which has higher limits."
                
                logger.error(f"Error invoking LLM for reports: {e}")
                return f"Error from AI generating the report ({e}). Check if your Google API Key is valid."
        return "Critical: Failed to generate report after retries."
