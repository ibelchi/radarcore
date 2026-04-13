# RadarCore: Guia d'Inversió (Conceptes i Pràctica)

Benvingut a **RadarCore**. Aquest manual està dissenyat per portar-te des de zero fins a entendre com funciona el nostre assistent virtual. No amaguem com el programa pren les decisions; te n'ensenyarem la matemàtica, però amb exemples del món real.

---

## 1. Conceptes Fonamentals
El RadarCore no endevina el futur. Utilitza una estratègia que s'anomena **Swing Trading** basada en la "Reversió a la Mitjana" (Buy the Dip o Comprar la Caiguda).

Què vol dir això? Quan una empresa sana i forta cau bruscament de preu per pànic general o una mala notícia temporal, tendeix a "rebotar" fins a recuperar el seu valor real.

### El Cicle del Preu
- **Màxim (High)**: El preu més alt al qual s'ha pagat una acció en els últims mesos.
- **Mínim (Low) / Pivot**: El fons. El moment on tothom deixa de vendre i les primeres persones tornen a comprar.
- **Trencament (Breakout)**: El moment en què l'acció confirma que realment està pujant.

---

## 2. Com Calcula RadarCore una Oportunitat? (Les Matemàtiques)

RadarCore utilitza **tres pilars** abans de recomanar-te una acció. Tota la matemàtica està programada en percentatges perquè sigui aplicable tant a una acció de 10$ com a una de 1000$.

### Pilar A: La Caiguda Real (Drop %)
El programa busca un descompte (rebaixes). Si una acció valia 100$ i cau fins a 80$, ha fet una caiguda del 20%.
> **Fórmula matemàtica**: `((Preu Màxim - Preu Mínim) / Preu Màxim) * 100`

### Pilar B: La Confirmació del Rebot (Rebound %)
RadarCore *mai* compra cap acció mentre està caient (això és com intentar atrapar un ganivet caient). Espera a veure que des del fons (Mínim), l'acció ja ha començat a pujar una mica (un mínim del 2%).
> **Fórmula matemàtica**: `((Preu Actual - Preu Mínim) / Preu Mínim) * 100`

### Pilar C: El "Pattern" (La Forma del Gràfic)
El RadarCore observarà l'historial del preu i el classificarà:
* **L-BASE**: L'acció ha caigut i porta 10 o 15 dies gairebé sense moure's en un racó. Matemàticament: `Rang acumulat < 8% durant més de 10 dies`. Això significa que els grans fons institucionals (els rics) estan acumulant l'acció a poc a poc sense fer soroll. ÉS EL PATRÓ MÉS SEGUR.
* **V-RECOVERY**: Cau i rebota bruscament. Matemàticament: `Rebound > 5% en pocs dies`. És més ràpid, però més inestable.

---

## 3. El Context del Mercat: Sistèmic vs Idiosincràtic

RadarCore és intel·ligent i compara la caiguda de la teva acció amb la del mercat sencer (L'índex S&P 500, que engloba les 500 empreses més grans dels EUA).

* **Cau el Mercat i cau l'Acció (Sistèmica)**: L'S&P 500 cau un 10%, i la teva acció cau un 12%. El RadarCore ho analitza restant-ho: `12% - 10% = 2% d'estranya`. Si és inferior al 5%, l'App et dirà `"⚠️ Caiguda Sistèmica"`. No hi ha cap problema amb l'empresa, simplement tot el mercat està en crisi. Tarda més a recuperar-se.
* **El Mercat puja però l'Acció cau (Idiosincràtica)**: L'S&P 500 puja, però la teva acció cau temporalment. L'App et dirà `"✅ Caiguda Idiosincràtica"`. Aquesta és la millor situació! Indica que pot recuperar-se ràpid en solitari sense dependre dels inversors globals.

La "Confiança" (1-100%) que et dóna el RadarCore es calcula sumant punts d'aquests factors: Quina és la qualitat de la caiguda + És una L-BASE? + És Idiosincràtic?

---

## 4. Cas Pràctic: Passos en una Partida de RadarCore

Imagina que ets a la plataforma. Què has de fer?

1. **Escanejar (Scanner)**: Prem el botó "Run Scanner". RadarCore llegirà tota la borsa americana i descarregarà dades per trobar oportunitats "Buy the Dip".
2. **Llegir la Taula (History)**: Veus una empresa (ex: TSLA).
   - "Drop": 25% (Està a un quart de descompte).
   - "Rebound": 4% (Perfecte, el ganivet ja està a terra i estem a l'alça).
   - "Pattern": L-BASE (Més seguretat).
3. **Analitzar el Gràfic**: Obre'l. Veuràs el Target 1 (T1) calculat al 85% de la recuperació. Aquest és el teu primer objectiu de guany.
4. **Protegeix-te (Stop Loss - SL)**: Fixa't en la línia vermella. Si compres avui l'acció, has de configurar en el teu banc o xarxa que si el preu torna a baixar cap aquella línia vermella (el "Pivot"), venguis automàticament. Assumeixes una pèrdua petita (potser d'un 5%) per evitar perdre el gran capital. **Mai inverteixis sense un Stop Loss**.

## Regla d'Or pel Novell
No importa si la "Confidence" és del 99%. L'empresa pot tenir una mala notícia i quebrar l'endemà. Mai inverteixis tots els teus diners en 1 oportunitat del RadarCore, divideix-ho en 10. Això s'anomena **Risc Diversificat**.
