# RadarCore: Especificació Tècnica (Swing Trading Engine)

Documentació orientada a l'analista financer i dissenyadors d'algoritmes quantitatius.
RadarCore és una terminal d'anàlisi basada en algoritmes de reversió a la mitjana (*Mean Reversion*) dissenyada específicament per a l'ecosistema de Swing Trading.

---

## 1. Algorisme de Detecció: "Buy The Dip"
La matriu d'avaluació es troba al mòdul `src/strategies/buy_the_dip.py`. No busca mínims absoluts històrics, sinó regressions a la mitjana dins de finestres de volatilitat de curt termini.

### Arquitectura Paramètrica Inicial
*   `lookback_days` = 60 dies (Finestra de context per identificar el darrer clímax de l'actiu).
*   `min_drop_pct` = 15.0% (Límit de significança per considerar l'estrès de preu).
*   `min_rebound_pct` = 2.0% (Confirmació tècnica del gir d'inversió).

L'algoritme processa el preu iterant una sola vegada les mètriques d'alta liquiditat per filtrar el soroll del "penny stock" (requereix `min_market_cap_b` > 10 i volums > 1M).

---

## 2. Formalització del Càlcul Tècnic

A diferència dels screnners "vanilla", RadarCore corregeix l'apreciació del "Drop" tancant sempre la lectura en el mínim local tècnic, no pas contra el tick real-time.

*   **Caiguda Real**:
    ```
    Drop_From_High (%) = ((Period_High - Period_Low) / Period_High) * 100
    ```
    *(Amb això evitem el risc descartar models tècnics consolidats que pateixin de gap-ups des de mitjanit).*

*   **Punt de Fricció (Rebound)**:
    ```
    Rebound (%) = ((Current_Price - Period_Low) / Period_Low) * 100
    ```

---

## 3. Tipologia de Patrons (Pattern Recognition Engine)

L'arquitectura analitza micro-cicles (finestres de 10-15 dies) pel darrer extrem buscant divergències entre volums direccionals subjacents:

1.  **L-BASE**: Perfil de consolidació. Defineix zones d'acumulació institucional on l'impacte de descens (Bear Trend) s'ha esgotat contra un mur de liquiditat estancada (sideways).
    *   *Regles*: `(Max_price_10d - Min_price_10d) / Min_price_10d < 8%` i `Days_Since_Period_Low >= 10`.
2.  **V-RECOVERY**: Clàssic *Snap-back* produint-se un estrès altament emocional on l'oferta s'extingeix immediatament contra compres a mercat massives.
    *   *Regles*: `Rebound >= 5%` amb un alt rang implícit.

---

## 4. Contextualització Relativa (The Systemic Filter)

Una caiguda agressiva sota un marc "Macro-Bear" manca d'atracció beta-ajustada. Per aquest motiu, RadarCore orquestra un descarregador paral·lel del SPY (representant de risc de mercat Beta=1) de "Zero-Retenció".

Càlcul diferencial:
```
Relative_Drop_Pct  = (Drop_From_High_Pct_{Asset}) - (Drop_Pct_{SPY})
```
*   Si `Relative_Drop_Pct < 5.0%` = **Sistèmic**. El mercat arrossega l'actiu. L'operador d'arbitratge ha d'avançar en alerta.
*   Si `Relative_Drop_Pct >= 5.0%` = **Idiosincràtic**. Alpha en brut potencial per al Swing.

---

## 5. Confidence Score (Model d'Avaluació)

La rúbrica d'oportunitats del RadarCore (`0-100%`) està calibrada sintèticament en 4 dimensions per al "setup":

1.  **Mass Drop** (30% MAX): Puntuació lliure a `min(Drop_Pct / 40.0, 1.0)`.
2.  **Rebound Validation** (20% MAX): Valida impuls actiu: `min(Rebound_Pct / 10.0, 1.0)`.
3.  **Pattern Architecture** (25% MAX): L'assignació de risc-rendiment afavoreix `L-BASE (25%)` per sobre de `V-RECOVERY (15%)` basat en taxa de supervivència de breakouts comercials.
4.  **Market Decoupling** (25% MAX): Aporta Alpha si el model demostra un fenomen de descens `is_systemic == False` per evitar atrapaments d'indexació per al model direccional.

El gràfic (generat de forma procedimental amb Plotly, sense pes addicional en I/O de l'app de streamlit) es superposa via vectors pre-computats que ofereixen guies clares com `T_1=Period_high * 0.85` de línia objectiu.
