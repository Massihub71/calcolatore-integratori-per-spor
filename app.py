import streamlit as st

# 1. Configurazione Pagina Wide (Schermo Intero)
st.set_page_config(
    page_title="NutriSport PRO - Calcolatore Integrazione",
    page_icon="⚡",
    layout="wide"
)

# --- HEADER PRINCIPALE ---
st.title("⚡ NutriSport PRO")
st.caption("Calcolatore Scientifico di Integrazione, Idratazione ed Elettroliti Fai-da-Te")

# --- SIDEBAR (PARAMETRI) ---
st.sidebar.header("📋 Parametri Allenamento")

peso = st.sidebar.number_input("Peso Corporeo (kg)", min_value=40, max_value=130, value=70)
durata_min = st.sidebar.slider("Durata Allenamento (minuti)", min_value=30, max_value=360, value=120, step=15)
durata_ore = durata_min / 60.0

sport = st.sidebar.selectbox("Disciplina", ["Ciclismo", "Corsa", "Nuoto", "Palestra / Potenza", "Triathlon"])
intensita = st.sidebar.select_slider("Intensità Sforzo", options=["Bassa (Z1-Z2)", "Media (Z3)", "Alta / Gara (Z4-Z5)"])
temp = st.sidebar.slider("Temperatura Ambientale (°C)", min_value=5, max_value=40, value=25)
sudorazione = st.sidebar.selectbox("Tasso di Sudorazione", ["Basso", "Medio", "Alto (Maglietta bianca di sale)"])
tolleranza_carbo = st.sidebar.slider("Tolleranza Carboidrati (g/ora)", min_value=30, max_value=120, value=60, step=10)

# Opzioni Caffeina chiarite e ordinate per tolleranza crescente
opzioni_caff = [
    "Nessuna / Disattivata (0 mg)",
    "Bassa Tolleranza / Sensibile (1.5 mg/kg)",
    "Media Tolleranza (3.0 mg/kg)",
    "Alta Tolleranza / Abituato (4.5 mg/kg)"
]
sensib_caff = st.sidebar.selectbox("Tolleranza alla Caffeina", opzioni_caff, index=2)

st.sidebar.divider()
st.sidebar.header("🍫 Solidi & Integrazione Extra")
formato_carbo = st.sidebar.selectbox("Strategia Carboidrati", ["Tutto in Borraccia (Solo Liquidi)", "Misto (Liquidi + Barrette/Gel)"])
n_barrette = 0
if formato_carbo == "Misto (Liquidi + Barrette/Gel)":
    n_barrette = st.sidebar.number_input("Quante barrette/gel consumi? (30g carbo cad.)", min_value=1, max_value=10, value=2)

usa_citrullina = st.sidebar.checkbox("Citrullina Malato (Pre-workout)", value=True)
usa_potassio_calcio = st.sidebar.checkbox("Potassio e Calcio (Profilo Elettrolitico)", value=True)

# --- LOGICA DI CALCOLO CARBOIDRATI (A SCAGLIONI E SCALATA SUL PESO) ---
if durata_min < 45:
    carbo_h = 0
elif durata_min < 75:
    # Breve durata: integrazione minima solo ad alta intensità
    base_carbo = 0 if intensita == "Bassa (Z1-Z2)" else (20 if intensita == "Media (Z3)" else 35)
    carbo_h = min(base_carbo, tolleranza_carbo)
elif durata_min < 150:
    # Media durata (1h15m - 2h30m)
    base_carbo = 35 if intensita == "Bassa (Z1-Z2)" else (50 if intensita == "Media (Z3)" else 65)
    # Aggiustamento dinamico sul peso corporeo (±10% per pesi estremi)
    factor_peso = 0.9 if peso < 60 else (1.1 if peso > 80 else 1.0)
    carbo_h = min(round(base_carbo * factor_peso), tolleranza_carbo)
else:
    # Lunga durata (> 2h30m)
    base_carbo = 45 if intensita == "Bassa (Z1-Z2)" else (65 if intensita == "Media (Z3)" else 90)
    factor_peso = 0.9 if peso < 60 else (1.1 if peso > 80 else 1.0)
    carbo_h = min(round(base_carbo * factor_peso), tolleranza_carbo)

carbo_totali = round(carbo_h * durata_ore)

# Gestione Solidi vs Liquidi
if carbo_totali > 0:
    carbo_solidi = n_barrette * 30
    if carbo_solidi > carbo_totali:
        carbo_solidi = carbo_totali
        n_barrette = carbo_solidi // 30
    carbo_liquidi = carbo_totali - carbo_solidi
else:
    carbo_solidi = 0
    carbo_liquidi = 0
    n_barrette = 0

malto = round(carbo_liquidi * (2/3))
fruttosio = round(carbo_liquidi * (1/3))

# --- LOGICA DI CALCOLO IDRATAZIONE ED ELETTROLITI ---
acqua_h = 500 if temp < 20 else (750 if temp <= 28 else 1000)
if sudorazione == "Alto (Maglietta bianca di sale)":
    acqua_h += 200

acqua_totale = round((acqua_h * durata_ore) / 1000, 2)

base_sodio_l = 600 if temp < 25 else 800
if sudorazione == "Alto (Maglietta bianca di sale)":
    base_sodio_l += 300

sodio_mg_totali = round(base_sodio_l * acqua_totale)
sale_cucina_g = round(sodio_mg_totali / 393.4, 1)

potassio_mg = round(300 * acqua_totale) if usa_potassio_calcio else 0
calcio_mg = round(150 * acqua_totale) if usa_potassio_calcio else 0

citrato_potassio_g = round(potassio_mg / 380, 1) if usa_potassio_calcio else 0.0
citrato_calcio_g = round(calcio_mg / 210, 1) if usa_potassio_calcio else 0.0

citrullina_g = 6.0 if usa_citrullina else 0.0
glicerolo_g = round(1.1 * peso, 1) if (temp >= 26 or durata_ore >= 3) else 0.0
eaa_g = 10 if durata_ore >= 2.5 else 0

# --- LOGICA CAFFEINA CORRETTA ---
if "1.5 mg/kg" in sensib_caff:
    caffeina_mg = round(1.5 * peso)
elif "3.0 mg/kg" in sensib_caff:
    caffeina_mg = round(3.0 * peso)
elif "4.5 mg/kg" in sensib_caff:
    caffeina_mg = round(4.5 * peso)
else:
    caffeina_mg = 0

# --- METRICHE PRINCIPALI ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌾 Carboidrati Totali", f"{carbo_totali} g", f"{carbo_h} g/ora")
col2.metric("💧 Acqua Totale", f"{acqua_totale} L", f"{acqua_h} ml/ora")
col3.metric("🧂 Sodio Totale", f"{sodio_mg_totali} mg", f"~{sale_cucina_g}g sale")
col4.metric("🍌 Potassio Totale", f"{potassio_mg} mg" if usa_potassio_calcio else "N/A", f"~{citrato_potassio_g}g polvere" if usa_potassio_calcio else "")

st.divider()

# --- CORPO PRINCIPALE ---
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        st.subheader("🍾 Miscela Borraccia (Liquidi ed Elettroliti)")
        st.write(f"Sciogliere il tutto in **{acqua_totale} Litri d'acqua** (divisi nelle borracce previste):")
        st.divider()
        if carbo_totali == 0:
            st.info("💡 Per allenamenti sotto i 45 minuti non è necessario integrare carboidrati. Mantieni solo l'idratazione e gli elettroliti.")
        st.markdown(f"🔹 **Maltodestrine:** {malto} g")
        st.markdown(f"🔹 **Fruttosio:** {fruttosio} g")
        st.markdown(f"🔹 **Sale da Cucina Fino (Sodio):** {sale_cucina_g} g")
        
        if usa_potassio_calcio:
            st.markdown(f"🔹 **Citrato di Potassio (polvere):** {citrato_potassio_g} g *(~{potassio_mg} mg K+)*")
            st.markdown(f"🔹 **Citrato di Calcio (polvere):** {citrato_calcio_g} g *(~{calcio_mg} mg Ca²⁺)*")
            
        if eaa_g > 0:
            st.markdown(f"🔹 **Aminoacidi Essenziali (EAA):** {eaa_g} g")
            
        st.divider()
        st.caption("💡 *Aggiungi succo di 1 limone spremuto per migliorare il sapore e facilitare l'assorbimento.*")

with col_right:
    with st.container(border=True):
        st.subheader("⚡ Integrazione Specialistica & Pre-Workout")
        
        has_preworkout = False
        
        if citrullina_g > 0:
            has_preworkout = True
            st.markdown(f"🧪 **L-Citrullina Malato (2:1):** **{citrullina_g} g**")
            st.caption("Sciogliere in 250-300 ml d'acqua e bere **30-45 min prima dello sforzo**.")
            st.divider()
            
        if glicerolo_g > 0:
            has_preworkout = True
            st.markdown(f"🧊 **Protocollo Glicerolo (Iperidratazione):** **{glicerolo_g} g**")
            st.caption("Sciogliere in 1 Litro d'acqua da bere **2 ore prima del via**.")
            st.divider()
            
        if caffeina_mg > 0:
            has_preworkout = True
            st.markdown(f"☕ **Caffeina Anidra:** **{caffeina_mg} mg**")
            st.caption("Da assumere 45 min prima del via o divisa durante lo sforzo.")
            
        if not has_preworkout:
            st.info("Nessun integratore pre-workout richiesto per questa configurazione.")

# --- STRATEGIA SOLIDI & RICETTE ---
st.divider()
st.subheader("🍫 Strategia Solidi & Ricettario Fai-da-Te")

if formato_carbo == "Misto (Liquidi + Barrette/Gel)" and n_barrette > 0 and carbo_totali > 0:
    st.info(f"Hai scelto di apportare **{carbo_solidi}g di carboidrati** tramite **{n_barrette} solidi/gel** (30g carbo cad.), riducendo la quota in borraccia a **{carbo_liquidi}g**.")
    
    tab1, tab2, tab3 = st.tabs(["🌾 Rice Cakes Pro (Ciclismo)", "🍯 Barrette Avena & Datteri", "🧪 Gel Energetico Fai-da-Te"])
    
    with tab1:
        st.markdown("""
        #### 🍚 Rice Cakes Ciclismo (Stile Pro Tour)
        * **Resa:** 8 Porzioni da ~30g Carboidrati ciascuna.
        * **Ingredienti:** 250g Riso per minestre, 500ml Acqua, 30g Zucchero o Miele, 100g Philadelphia o Olio di cocco, Cannella/Marmellata.
        * **Preparazione:** 
            1. Cuoci il riso nell'acqua finché non ha assorbito tutto il liquido.
            2. A fuoco spento, incorpora il formaggio spalmabile e il miele/zucchero.
            3. Versa in una teglia (spessore 2 cm), compatta e lascia riposare in frigo tutta la notte.
            4. Taglia in 8 quadretti uguali e avvolgi in fogli d'alluminio.
        """)
    
    with tab2:
        st.markdown("""
        #### 🥣 Barrette Avena, Datteri e Miele (No-Cook)
        * **Resa:** 6 Barrette da ~30g Carboidrati ciascuna.
        * **Ingredienti:** 120g Fiocchi d'avena piccoli, 100g Datteri denocciolati, 40g Miele, 1 pizzico di sale.
        * **Preparazione:**
            1. Frulla i datteri con 2 cucchiai d'acqua tiepida fino a creare una crema densa.
            2. Impasta a mano in una ciotola insieme all'avena, al miele e al sale.
            3. Stendi il composto su una pirofila, compattandolo con cura.
            4. Riponi in freezer per 30 minuti prima di tagliare 6 barrette.
        """)
        
    with tab3:
        st.markdown("""
        #### 🧪 Gel Energetico Fai-da-Te (Ratio 2:1)
        * **Resa:** 2 Gel da ~30g Carboidrati ciascuno.
        * **Ingredienti:** 40g Maltodestrine, 20g Fruttosio, 35ml Acqua tiepida (o succo di limone), 1 pizzico di sale.
        * **Preparazione:**
            1. Unisci le polveri secche in un bicchiere.
            2. Versa l'acqua tiepida mescolando vigorosamente fino ad azzerare i grumi.
            3. Travasa nella soft flask ed è pronto all'uso.
        """)
else:
    st.write("Stai fornendo **il 100% dell'energia via borraccia** (o lo sforzo non richiede integrazione solida). Se desideri integrare solidi, seleziona la modalità **Misto** nel menu a sinistra.")
