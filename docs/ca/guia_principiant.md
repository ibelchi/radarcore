# RadarCore: Guia d'Inversió (Conceptes i Pràctica)

Benvingut a **RadarCore**. Aquest manual t'ajudarà a entendre com funciona l'estratègia **Buy the Recovery** (Comprar la Recuperació) i com pots utilitzar aquest programari per aprendre sobre finances i swing trading des de zero.

---

## 1. Què és l'estratègia "Buy the Recovery"?

Històricament, molta gent ha sentit l'expressió "Buy the Dip" (comprar la caiguda). A RadarCore la anomenem **Buy the Recovery** perquè és més precisa: no comprem quan l'acció baixa (un "ganivet que cau"), sinó quan ja ha trobat un terra i comença a recuperar-se.

L'objectiu és aprofitar que el preu tendeix a tornar a la seva mitjana després d'un ensurt temporal.

---

## 2. Abans de començar: Configurant l'Escàner

Quan configures l'escàner, veus una sèrie de paràmetres. Aquí tens què signifiquen en llenguatge planer:

*   **Lookback Days (Dies de recerca)**: És quant de temps enrere mirem el passat per buscar el punt més alt de l'acció. Si poses 60 dies, busquem el "Rècord" de preu d'aquells 2 mesos per comparar-lo amb el preu d'avui.
*   **Min Drop % (Caiguda mínima)**: Quant "descompte" vols que tingui l'acció abans d'avisar-te. Si poses 15%, només busquem empreses que hagin caigut almenys un 15% des del seu màxim de 60 dies.
*   **Min Rebound % (Rebot mínim)**: És la confirmació de que ja no estem caient. Si poses 2%, vols que l'acció ja hagi pujat un 2% des del seu punt més baix.
*   **Symbol Limit**: Quantes empreses del mercat vols analitzar (0 per analitzar-les totes, però trigarà més).

---

## 3. Com es calcula la "Confidence" (Confiança)?

La nota de confiança (1-100%) que veus a cada oportunitat no és màgia negra; és la suma de la punts segons quatre factors:

1.  **Qualitat de la Caiguda (30%)**: Com més a prop estigui l'acció d'haver caigut un 40-50%, més confiança té el programa de que hi ha un gran recorregut de tornada.
2.  **Qualitat del Rebot (20%)**: Si el rebot és sòlid (entre un 5 i un 10%), el programa té més confiança en que la recuperació ja ha començat.
3.  **El Patró de Gràfic (25%)**:
    *   **L-BASE**: Guanya el màxim de punts. Significa que el preu s'ha quedat lateral, gairebé sense moure's en un racó durant dies. Això suggereix que els grans inversors rics estan "acumulant" la teva acció sense fer soroll.
    *   **V-RECOVERY**: Guanya menys punts de confiança perquè és una pujada molt ràpida i violenta que sol ser més inestable.
4.  **Context de Mercat (25%)**: Si la teva acció ha caigut per motius propis mentre el mercat sencer puja (**Caiguda Idiosincràtica**), el programa té més confiança en la seva recuperació solitària.

---

## 4. Conceptes Financers Clau

### Stop Loss (SL)
És el teu **fre de mà de seguretat**. Imagina que compres una acció a 10$. Si de sobte l'empresa segueix anant malament, l'Stop Loss és una ordre que diu al teu banc: "Si l'acció torna a baixar fins a 9$, ven-la immediatament". 
*   **Per què serveix?** Perquè si l'empresa fa fallida, tu només hauràs perdut l'1$ (del 10 al 9), però t'hauràs salvat de perdre els 10$. El RadarCore et marca aquesta línia en vermell als gràfics.

### Targets o Objectius (T1 i T2)
Són les teves "metes de venda" on reculls els guanys.
*   **T1 (Objectiu Conservador)**: És un punt mig de recuperació (habitualment marcat al 85% d'aproximació al màxim anterior). És on pots decidir vendre la meitat per assegurar beneficis ràpids.
*   **T2 (Objectiu Ideal)**: És el moment en què l'acció torna exactament al preu màxim que tenia abans de caure. És on l'estratègia "Buy the Recovery" es completa amb èxit total.

### Mercats de Referència (El cas de l'S&P 500)
Encara que pots escanejar l'IBEX 35 espanyol o el DAX alemany, el programa sempre fa servir el "Mercat Americà" (**SPY / S&P 500**) com a referència global. Per què? Perquè si la borsa americana cau fort, és molt difícil que qualsevol acció de qualsevol altre mercat pugi de forma sana. Ens serveix de termòmetre per saber si la caiguda de la teva empresa és un cas aïllat o si és el món sencer el que està en crisi.

---

## 5. Cas Pràctic: Interpretant els Gràfics

Quan obris un gràfic de Plotly al RadarCore, busca aquests 3 colors:

1.  **La Zona Vermella**: És el període on l'acció estava en caiguda lliure. El **Triangle Vermell** marca on va començar (el màxim).
2.  **El Triangle Groc**: És el **Pivot**. El moment on la caiguda es va aturar i l'acció va decidir que ja no baixaria més.
3.  **La Zona Verda**: És la fase de recuperació que estem intentant aprofitar. El nostre objectiu és anar pujant des del groc fins a la **Línia Verda Discontínua (T2)**.

## Regla d'Or: Diversificació
Mai posis tots els teus estalvis en una sola acció, per molta "Confidence" que tingui el programa. L'estratègia correcta consisteix a tenir, per exemple, 10 operacions diferents a la vegada. Així, si una et surt malament i salta l'**Stop Loss**, les altres 9 poden seguir el seu curs cap al **T2** i donar-te beneficis globals.
