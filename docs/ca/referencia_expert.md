# RadarCore: Especificació Tècnica (Swing Trading Engine)

Documentació orientada a l'analista financer i dissenyadors d'algoritmes quantitatius.
RadarCore és una terminal d'anàlisi basada en algoritmes de reversió a la mitjana (*Mean Reversion*) dins d'una tàctica de **Buy the Recovery**.

---

## 1. Algorisme de Detecció: "Buy the Recovery"
L'estratègia orquestrada al mòdul `src/strategies/buy_the_dip.py` identifica punts d'inflexió post-clímax baixista.

### Arquitectura de Control (Paràmetres configurables)
*   **Lookback Days**: Finestra temporal (N) de context per al càlcul del valor `MAX(High)`.
*   **Min Drop %**: Filtre de significança de la caiguda relativa `(High - Low) / High`.
*   **Min Rebound %**: Filtre de confirmació d'impuls des del pivot `(Current - Low) / Low`.
*   **Filtres de Liquitat**: Requereix `Market Cap > 10B` i `Volume > 1M` per garantir l'arbitratge.

---

## 2. Definició de Sortides i Gestió de Risc

*   **Stop Loss (SL)**: Referenciat al `Period_Low`. És el punt d'invalidació tècnica del setup de reversió.
*   **Target 1 (T1)**: Resistència dinàmica fixada al 85% del valor màxim del període (`Period_High * 0.85`).
*   **Target 2 (T2)**: Objectiu de retorn a la mitjana clàssic (100% de recuperació del rècord anterior).

---

## 3. Tipologia de Patrons (Pattern Recognition Engine)

1.  **L-BASE**: Perfil d'acumulació lateral. 
    *   *Mètrica*: `(Max_10d - Min_10d) / Min_10d < 8%` & `Dies_des_del_minim >= 10`.
2.  **V-RECOVERY**: Perfil de rebot explosiu.
    *   *Mètrica*: `Rebound >= 5%` amb rang de volatilitat expandit.

---

## 4. Context Relatiu (Sistèmic vs Idiosincràtic)

El sistema integra un càlcul de **Relative Momentum** comparant la caiguda de l'actiu amb la del benchmark SPY (S&P 500) durant la finestra temporal específica de l'actiu:
*   `Relative_Drop = Asset_Drop - SPY_Drop`.
*   Si `Relative_Drop < 5%`: **Sistèmic**. Risc creixent per dependència de la tendència macro.
*   Si `Relative_Drop >= 5%`: **Idiosincràtic**. Alpha pur.

---

## 5. Mètrica de Confiança (Confidence Score)

La puntuació final és un model ponderat de quatre factors binaris i escalars:
1.  **Drop Velocity** (30%): Escala `min(Drop_Pct / 40.0, 1.0)`.
2.  **Rebound Confirmation** (20%): Escala `min(Rebound_Pct / 10.0, 1.0)`.
3.  **Structural Strength** (25%): `L-BASE` aporta el 100% d'aquest pes; `V-RECOVERY` el 60%.
4.  **Market Alpha** (25%): Bonus del 100% si el descens és confirmat com a Idiosincràtic.
