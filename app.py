import streamlit as st

st.set_page_config(page_title="Calcolatore Integrazione Sportiva PRO", page_icon="⚡")

st.title("⚡ Calcolatore Personalizzato di Integrazione Sportiva PRO")
st.write("Configura il tuo allenamento per calcolare liquidi, carboidrati, elettroliti avanzati, solidi e ricette fai-da-te.")

st.sidebar.header("📋 Parametri Atleta e Sessione")

# Inputs Utente principali
peso = st.sidebar.number_input("Peso Corporeo (kg)", min_value=40, max_value=130, value=70)
durata_min = st.sidebar.slider("Durata Allenamento (minuti)", min_value=30, max_value=360, value=120, step=15)
durata_ore = durata_min / 60.0

sport = st.sidebar.selectbox("Disciplina", ["Ciclismo", "Corsa", "Nuoto", "Palestra / Potenza", "Triathlon"])
intensita = st.sidebar.select_slider("Intensità Sforzo", options=["Bassa (Z1-Z2)", "Media (Z3)", "Alta / Gara (Z4-Z5)"])
temp = st.sidebar.slider("Temperatura Ambientale (°C)", min_value=5, max_value=40, value=25)
sudorazione = st.sidebar.selectbox("Tasso di Sudorazione", ["Basso", "Medio", "Alto (Maglietta bianca di sale)"])
tolleranza_carbo = st.sidebar.slider("Tolleranza Carboidrati (g/ora)", min_value=30, max_value=120, value=60, step=10)
sensib_caff = st.sidebar.selectbox("Sensibilità alla Caffeina", ["Nessuna", "Bassa / Media", "Alta"])

st.sidebar.header("🍫 Solidi & Supplementi Extra")
formato_carbo = st.sidebar.selectbox("Strategia Carboidrati", ["Tutto in Borraccia (Solo Liquidi)", "Misto (Liquidi + Barrette/Gel)"])
n_barrette = 0
if formato_carbo == "Misto (Liquidi + Barrette/Gel)":
    n_barrette = st.sidebar.number_input("Quante barrette o gel vuoi consumare? (30g carbo cad.)", min_value=1, max_value=10, value=2)

usa_citrullina = st.sidebar.checkbox("Aggiungi Citrullina Malato (Vasodilatazione / Resistenza)", value=True)
usa_potassio_calcio = st.sidebar.checkbox("Includi Potassio e Calcio (Bilancio Elettrolitico)", value=True)

# --- LOGICA DI CALCOLO ---

# 1. Carboidrati Totali
if intensita == "Bassa (Z1-Z2)":
    carbo_h = min(40, tolleranza_carbo)
elif intensita == "Media (Z3)":
    carbo_h = min(60, tolleranza_carbo)
else:
    carbo_h = tolleranza_carbo

carbo_totali = round(carbo_h * durata_ore)

# Ripartizione Barrette vs Borraccia
carbo_solidi = n_barrette * 30
if carbo_solidi > carbo_totali:
    carbo_solidi = carbo_totali
    n_barrette = carbo_solidi // 30

carbo_liquidi = carbo_totali - carbo_solidi
malto = round(carbo_liquidi * (2/3))
fruttosio = round(carbo_liquidi * (1/3))

# 2. Idratazione & Sodio
acqua_h = 500 if temp < 20 else (750 if temp <= 28 else 1000)
if sudorazione == "Alto (Maglietta bianca di sale)":
    acqua_h += 200

acqua_totale = round((acqua_h * durata_ore) / 1000, 2)

base_sodio_l = 600 if temp < 25 else 800
if sudorazione == "Alto (Maglietta bianca di sale)":
    base_sodio_l += 300

sodio_mg_totali = round(base_sodio_l * acqua_totale)
sale_cucina_g = round(sodio_mg_totali / 393.4, 1)

# 3. Altri Elettroliti
potassio_mg = round(300 * acqua_totale) if usa_potassio_calcio else 0
calcio_mg = round(150 * acqua_totale) if usa_potassio_calcio else 0

# 4. Ergogenici
citrullina_g = 6.0 if usa_citrullina else 0.0
glicerolo_g = round(1.1 * peso, 1) if (temp >= 26 or durata_ore >= 3) else 0.0
eaa_g = 10 if durata_ore >= 2.5 else 0

caffeina_mg = 0
if sensib_caff == "Bassa / Media":
    caffeina_mg = round(3 * peso)
elif sensib_caff == "Alta":
    caffeina_mg = round(1.5 * peso)

# --- OUTPUT RISULTATI ---

st.markdown("---")
st.subheader("🎯 Sintesi Fabbisogno Totale")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Carboidrati Totali", f"{carbo_totali} g", f"{carbo_h} g/h")
col2.metric("Acqua Totale", f"{acqua_totale} L", f"{acqua_h} ml/h")
col3.metric("Sodio Totale", f"{sodio_mg_totali} mg", f"~{sale_cucina_g}g sale")
col4.metric("Potassio Totale", f"{potassio_mg} mg" if usa_potassio_calcio else "N/A")

st.markdown("---")
st.subheader("🍫 Strategia Solidi & Gel")
if formato_carbo == "Misto (Liquidi + Barrette/Gel)" and n_barrette > 0:
    st.write(f"- **Barrette / Gel (30g carbo ciascuno):** **{n_barrette} pezzi** (totale {carbo_solidi}g carboidrati).")
    st.write(f"- **Carboidrati rimanenti da sciogliere in acqua:** **{carbo_liquidi}g**")
    
    st.markdown("### 👨‍🍳 Guida alla Preparazione Solidi Fai-da-Te")
    tab1, tab2, tab3 = st.tabs(["🌾 Rice Cakes Pro (Bici)", "🍯 Barrette Avena & Datteri", "🧪 Gel Energetico Fai-da-Te"])
    
    with tab1:
        st.markdown("""
        **Rice Cakes Ciclismo (Stile World Tour)**
        *Facili da masticare in sella, ad altissima digeribilità (~30g carbo a mattonella).*
        
        **Ingredienti per 8 porzioni:**
        - 250g Riso per minestre (Originario o Roma)
        - 500ml Acqua
        - 2 cucchiai di Zucchero o Miele (~30g)
        - 100g Formaggio fresco spalmabile (es. Philadelphia) o Olio di cocco
        - Marmellata o Cannella a piacere
        
        **Preparazione:**
        1. Cuoci il riso nell'acqua finché non la assorbe del tutto e diventa molto morbido.
        2. A fuoco spento, mescola il formaggio spalmabile, lo zucchero e la marmellata.
        3. Stendi il composto in una teglia rettangolare livellandolo a 2 cm d'altezza.
        4. Lascia in frigorifero per tutta la notte.
        5. Taglia in 8 rettangoli uguali e avvolgili nella carta d'alluminio.
        """)
        
    with tab2:
        st.markdown("""
        **Barrette Avena, Datteri e Miele (Senza Cottura)**
        *Forniscono carboidrati a rilascio graduale per uscite lunghe (~30g carbo a barretta).*
        
        **Ingredienti per 6 barrette:**
        - 120g Fiocchi d'avena leggeri
        - 100g Datteri denocciolati
        - 2 cucchiai di Miele (~40g)
        - 1 pizzico di sale fino
        
        **Preparazione:**
        1. Frulla i datteri con 2 cucchiai d'acqua tiepida fino a ottenere una pasta.
        2. In una ciotola unisci l'avena, la pasta di datteri, il miele e il sale. Impasta con le mani.
        3. Stendi e compatisci bene sul fondo di un contenitore.
        4. Metti in freezer per 30 minuti, poi taglia in 6 barrette.
        """)
        
    with tab3:
        st.markdown("""
        **Gel Energetico Fai-da-Te (Ratio 2:1)**
        *Perfetto per la corsa o la bici da mettere nelle Soft Flask riutilizzabili.*
        
        **Ingredienti per 2 Gel (~30g carbo cad.):**
        - 40g Maltodestrine in polvere
        - 20g Fruttosio in polvere
        - 35ml Acqua tiepida (o succo di limone)
        - 1 pizzico di sale (~0.5g)
        
        **Preparazione:**
        1. Mescola le polveri in una tazza.
        2. Aggiungi l'acqua tiepida mescolando fino a sciogliere i grumi.
        3. Versa la gelatina ottenuta in una miniborraccia morbida (Soft Flask da 100ml).
        """)
else:
    st.write("Hai scelto di assumere **tutti i carboidrati in formato liquido** nella borraccia.")

st.markdown("---")
st.subheader("🧪 Ricetta Miscela per la Borraccia")

st.write(f"**Carboidrati Liquidi (Rapporto 2:1):**")
st.write(f"- **Maltodestrine:** {malto} g")
st.write(f"- **Fruttosio:** {fruttosio} g")

st.write(f"**Elettroliti e Minerali:**")
st.write(f"- **Sale da cucina (Sodio):** {sale_cucina_g} g")
if usa_potassio_calcio:
    st.write(f"- **Citrato o Cloruro di Potassio:** {potassio_mg} mg (~{round(potassio_mg/1000, 2)}g)")
    st.write(f"- **Calcio:** {calcio_mg} mg (~{round(calcio_mg/1000, 2)}g)")

st.markdown("---")
st.subheader("⚡ Integrazione Specialistica & Pre-Workout")

if citrullina_g > 0:
    st.write(f"- **L-Citrullina Malato:** **{citrullina_g} g** (da assumere 30-45 minuti prima dell'allenamento).")

if glicerolo_g > 0:
    st.info(f"💡 **Protocollo Glicerolo (Iperidratazione):** Sciogli **{glicerolo_g} g** di glicerolo in 1 Litro d'acqua da bere 2 ore prima del via.")

if eaa_g > 0:
    st.write(f"- **Aminoacidi Essenziali (EAA):** **{eaa_g} g** (da aggiungere nella borraccia per la protezione muscolare).")

if caffeina_mg > 0:
    st.write(f"- **Caffeina Anidra:** **{caffeina_mg} mg** (assunta pre-gara o divisa durante lo sforzo).")
