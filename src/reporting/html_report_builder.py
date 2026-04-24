import datetime
import os
from src.data.macro_fetcher import get_macro_context
from src.utils.analysis_utils import is_not_recommended_today

def generate_html_report(opportunities: list, macro_data: dict = None, scan_config: dict = None) -> str:
    """
    Generates a self-contained HTML report based on the Trazo design.
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%d %b %Y")
    time_str = now.strftime("%H:%M")
    
    # Macro block
    if macro_data is None:
        macro_data = get_macro_context()
    macro_html = ""
    alerta_vix = macro_data.get("alerta_vix", False)
    
    tickers_macro = ["SPY", "QQQ", "VIX", "TNX", "DXY"]
    
    for symbol in tickers_macro:
        data = macro_data.get(symbol, {})
        if not data: continue
        label = data.get("name", symbol)
        val = data.get("value", 0)
        pct = data.get("change_pct", 0)
        cls = "pos" if pct >= 0 else "neg"
        macro_html += f"""
        <div class="macro-tile">
            <div class="lbl">{label}</div>
            <div class="val">{val:,.2f}</div>
            <div class="pct {cls}">{pct:+.2f}%</div>
        </div>
        """

    # Banner VIX
    vix_banner = ""
    if alerta_vix:
        vix_banner = f"""
        <div style="background: var(--red); color: white; padding: 10px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold;">
            ⚠️ VOLATILITY ALERT: Elevated VIX ({macro_data.get('VIX', {}).get('value', 0):.2f})
        </div>
        """

    # Processar oportunitats
    # Ordenar per score si existeix
    all_opps = []
    for op in opportunities:
        m = op.metrics or {}
        score = m.get("bucket_score", 0)
        all_opps.append((op, score))
    
    all_opps.sort(key=lambda x: x[1], reverse=True)
    
    top_5 = []
    not_recommended = []
    
    for op, score in all_opps:
        m = op.metrics or {}
        is_risky, reason = is_not_recommended_today(m)
        if is_risky:
            not_recommended.append((op, reason))
        elif len(top_5) < 5:
            top_5.append(op)

    # Oportunitats Principals HTML
    opps_html = ""
    for op in top_5:
        m = op.metrics or {}
        ticker = op.symbol
        name = op.company_name or ticker
        price = op.current_price or 0
        bucket = m.get("bucket", "N/A")
        phase = m.get("phase", "N/A")
        rsi = m.get("rsi_14")
        vol_ratio = m.get("vol_ratio_3m")
        explanation = op.explanation or "No AI analysis available."
        
        # R/R and levels
        entry = m.get("entry_price", 0)
        stop = op.stop_loss or 0
        target = op.target_price or 0
        rr = m.get("risk_reward", 0)
        
        rsi_str = f"RSI14 <b>{rsi:.1f}</b>" if rsi is not None else "RSI N/A"
        vol_str = f"Vol 3M <b>{vol_ratio:.1f}x</b>" if vol_ratio is not None else ""
        vol_badge = '<div class="badge media" style="background: rgba(96,165,250,0.15); color: var(--blue);">🔵 Institutional Volume</div>' if vol_ratio and vol_ratio >= 2.0 else ""
        
        opps_html += f"""
        <div class="opp priority">
          {vol_badge}
          <div class="ticker"><span class="sym">{ticker}</span><span class="name">{name}</span></div>
          <div class="price-row"><span class="price">${price:.2f}</span></div>
          <div class="tags">
            <span class="tag swing">Bucket: {bucket}</span>
            <span class="tag riser">Phase: {phase}</span>
          </div>
          <div class="levels">
            <div class="lvl"><div class="lvl-lbl">Entry</div><div class="lvl-val entry">${entry:.2f}</div></div>
            <div class="lvl"><div class="lvl-lbl">Stop</div><div class="lvl-val stop">${stop:.2f}</div></div>
            <div class="lvl"><div class="lvl-lbl">Target</div><div class="lvl-val t1">${target:.2f}</div></div>
            <div class="lvl"><div class="lvl-lbl">R/R</div><div class="lvl-val">{rr:.2f}x</div></div>
          </div>
          <div class="indicators">
            <span class="ind">{rsi_str}</span>
            <span class="ind">{vol_str}</span>
          </div>
          <div class="reasoning">
            <span class="label">RadarCore Analysis</span>
            {explanation}
          </div>
        </div>
        """

    # No entrar avui HTML
    not_rec_html = ""
    for op, reason in not_recommended:
        not_rec_html += f"""
        <tr>
            <td><b>{op.symbol}</b></td>
            <td>{op.metrics.get('bucket', 'N/A')}</td>
            <td class="num">{op.metrics.get('rsi_14', 'N/A')}</td>
            <td style="color: var(--red)">{reason}</td>
        </tr>
        """
    
    if not not_rec_html:
        not_rec_html = "<tr><td colspan='4'>No opportunities filtered today.</td></tr>"

    # Pla per demà HTML (Top 3)
    plan_html = ""
    plan_opps = top_5[:3]
    for op in plan_opps:
        m = op.metrics or {}
        plan_html += f"""
        <div class="plan-card">
          <h3>{op.symbol}</h3>
          <ul>
            <li><b>Suggested Entry:</b> ${m.get('entry_price', 0):.2f}</li>
            <li><b>Stop Loss:</b> ${op.stop_loss or 0:.2f}</li>
            <li><b>Estimated R/R:</b> {m.get('risk_reward', 0):.2f}x</li>
          </ul>
        </div>
        """

    # HTML Complet
    full_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>RadarCore · Report {date_str}</title>
<style>
  :root {{
    --bg: #0b0d10;
    --bg-alt: #11141a;
    --bg-card: #161b22;
    --bg-card-hi: #1c2230;
    --line: #232a35;
    --line-soft: #1a1f29;
    --text: #e8edf2;
    --text-dim: #98a2b3;
    --text-faint: #6b7686;
    --gold: #c9a35c;
    --gold-bright: #e8c98e;
    --green: #4ade80;
    --green-soft: #1f3a2a;
    --red: #f87171;
    --red-soft: #3a1f24;
    --amber: #fbbf24;
    --amber-soft: #3a2e15;
    --blue: #60a5fa;
    --blue-soft: #1e2a3d;
    --purple: #a78bfa;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; line-height: 1.55; }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 28px 24px 96px; }}
  header.top {{ border-bottom: 1px solid var(--line); padding-bottom: 22px; margin-bottom: 28px; }}
  header.top h1 {{ font-size: 26px; margin: 0 0 4px 0; font-weight: 600; }}
  header.top h1 .accent {{ color: var(--gold); }}
  header.top .meta {{ color: var(--text-dim); font-size: 13px; }}
  section {{ margin-bottom: 42px; }}
  section > h2.heading {{ font-size: 18px; margin: 0 0 18px 0; padding-bottom: 8px; border-bottom: 1px solid var(--line); font-weight: 600; }}
  .macro-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 14px; }}
  .macro-tile {{ background: var(--bg-card); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; }}
  .macro-tile .lbl {{ color: var(--text-faint); font-size: 11px; text-transform: uppercase; }}
  .macro-tile .val {{ font-size: 18px; font-weight: 600; margin-top: 4px; }}
  .pos {{ color: var(--green); }}
  .neg {{ color: var(--red); }}
  .opp-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
  @media (max-width: 760px) {{ .opp-grid {{ grid-template-columns: 1fr; }} }}
  .opp {{ background: var(--bg-card); border: 1px solid var(--line); border-radius: 14px; padding: 20px 22px; position: relative; }}
  .opp.priority {{ border-color: var(--gold); }}
  .opp .badge {{ position: absolute; top: 14px; right: 14px; font-size: 10px; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }}
  .opp .ticker {{ display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px; }}
  .opp .sym {{ font-size: 22px; font-weight: 700; }}
  .opp .price {{ font-size: 20px; font-weight: 600; }}
  .tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }}
  .tag {{ font-size: 11px; padding: 3px 8px; border-radius: 4px; background: var(--bg-card-hi); color: var(--text-dim); border: 1px solid var(--line); }}
  .tag.swing {{ color: var(--blue); border-color: rgba(96,165,250,0.3); }}
  .tag.riser {{ color: var(--green); border-color: rgba(74,222,128,0.3); }}
  .levels {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; background: var(--bg-card-hi); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; font-size: 12px; }}
  .lvl-lbl {{ color: var(--text-faint); font-size: 10px; text-transform: uppercase; }}
  .lvl-val {{ color: var(--text); font-weight: 600; }}
  .lvl-val.entry {{ color: var(--gold-bright); }}
  .lvl-val.stop {{ color: var(--red); }}
  .indicators {{ display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; margin-bottom: 12px; color: var(--text-dim); }}
  .indicators b {{ color: var(--text); }}
  .reasoning {{ color: var(--text); font-size: 13px; border-top: 1px dashed var(--line); padding-top: 12px; }}
  .reasoning .label {{ color: var(--gold); font-weight: 600; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 4px; }}
  table.t {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  table.t th, table.t td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line-soft); }}
  table.t th {{ color: var(--text-faint); font-size: 11px; text-transform: uppercase; }}
  .plan {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }}
  .plan-card {{ background: var(--bg-card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; }}
  .plan-card h3 {{ margin: 0 0 8px 0; font-size: 13px; text-transform: uppercase; color: var(--gold); }}
  footer {{ margin-top: 60px; padding-top: 22px; border-top: 1px solid var(--line); color: var(--text-faint); font-size: 12px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
    {vix_banner}
    <header class="top">
        <h1>RadarCore Report <span class="accent">— {date_str}</span></h1>
        <div class="meta">Market analysis generated at {time_str}</div>
    </header>

    <section id="macro">
        <h2 class="heading">Macro Context</h2>
        <div class="macro-grid">
            {macro_html}
        </div>
    </section>

    <section id="oportunidades">
        <h2 class="heading">Main Opportunities (Top 5 by Score)</h2>
        <div class="opp-grid">
            {opps_html}
        </div>
    </section>

    <section id="no-entrar">
        <h2 class="heading">No Entry Today (High Risk)</h2>
        <table class="t">
            <thead>
                <tr><th>Ticker</th><th>Bucket</th><th>RSI</th><th>Reason</th></tr>
            </thead>
            <tbody>
                {not_rec_html}
            </tbody>
        </table>
    </section>

    <section id="plan">
        <h2 class="heading">Plan for Tomorrow</h2>
        <div class="plan">
            {plan_html}
        </div>
    </section>

    <footer>
        RadarCore Assistant · Automatically generated · {date_str}
    </footer>
</div>
</body>
</html>"""
    return full_html
