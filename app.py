import streamlit as st

# 1. Configurazione Pagina Wide (Schermo Intero)
st.set_page_config(
    page_title="NutriSport PRO - Calcolatore Integrazione",
    page_icon="⚡",
    layout="wide"
)

# 2. CSS Personalizzato per Grafica & Cards Professionali
st.markdown("""
<style>
    /* Gradienti e Stile Headers */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF8717);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 25px;
    }
    
    /* Box & Card Custom */
    .card-box {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #FF4B4B;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .card-borraccia {
        background-color: #eef7ff;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .card-preworkout {
        background-color: #fff9e6;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #FFC107;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Font e Liste dentro le card */
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .ingredient-item {
        font-size: 1.05rem;
        padding: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER PRINCIPALE ---
st.markdown('<p class="main-title">⚡ NutriSport PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calcolatore Scientifico di Integrazione, Idratazione ed Elettroliti Fai-da-Te</p>', unsafe_allow_html=True)

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
sensib_caff = st.sidebar.selectbox("Sensibilità Caffeina", ["Nessuna", "Bassa / Media", "Alta"])

st.sidebar.markdown("---")
st.sidebar.header("🍫 Solidi & Integrazione Extra")
formato_carbo = st.sidebar.selectbox("Strategia Carboidrati", ["Tutto in Borraccia (Solo Liquidi)", "Misto (Liquidi + Barrette/Gel)"])
n_barrette = 0
if formato_carbo == "Misto (Liquidi + Barrette/Gel)":
    n_barrette = st.sidebar.number_input("Quante barrette/gel consumi? (30g carbo cad.)", min_value=1, max_value=10, value=2)

usa_citrullina = st.sidebar.checkbox("Citrullina Malato (Pre-workout)", value=True)
usa_potassio_calcio = st.sidebar.checkbox("Potassio e Calcio (Profilo Elettrolitico)", value=True)

# --- LOGICA DI CALCOLO ---
if intensita == "Bassa (Z1-Z2)":
    carbo_h = min(40, tolleranza_carbo)
elif intensita == "Media (Z3)":
    carbo_h = min(60, tolleranza_carbo)
else:
    carbo_h = tolleranza_carbo

carbo_totali = round(carbo_h * durata_ore)

carbo_solidi = n_barrette * 30
if carbo_solidi > carbo_totali:
    carbo_solidi = carbo_totali
    n_barrette = carbo_solidi // 30

carbo_liquidi = carbo_totali - carbo_solidi
malto = round(carbo_liquidi * (2/3))
fruttosio = round(carbo_liquidi * (1/3))

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

caffeina_mg = 0
if sensib_caff == "Bassa / Media":
    caffeina_mg = round(3 * peso)
elif sensib_caff == "Alta":
    caffeina_mg = round(1.5 * peso)


# --- DISPLAY METRICHE PRINCIPALI (CARDS IN ALTO) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌾 Carboidrati Totali", f"{carbo_totali} g", f"{carbo_h} g/ora")
with col2:
    st.metric("💧 Acqua Totale", f"{acqua_totale} L", f"{acqua_h} ml/ora")
with col3:
    st.metric("🧂 Sodio Totale", f"{sodio_mg_totali} mg", f"~{sale_cucina_g}g sale cucina")
with col4:
    st.metric("🍌 Potassio Totale", f"{potassio_mg} mg" if usa_potassio_calcio else "N/A", f"~{citrato_potassio_g}g polvere" if usa_potassio_calcio else "")

st.markdown("<br>", unsafe_allow_html=True)

# --- CORPO PRINCIPALE (DUE COLONNE) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    # CARD BORRACCIA
    html_borraccia = f"""
    <div class="card-borraccia">
        <div class="card-title" style="color: #1565C0;">🍾 Miscela Borraccia (Liquidi ed Elettroliti)</div>
        <p>Sciogliere il tutto in <b>{acqua_totale} Litri d'acqua</b> (divisi nelle borracce previste):</p>
        <hr style="margin: 10px 0;">
        <div class="ingredient-item">🔹 <b>Maltodestrine:</b> {malto} g</div>
        <div class="ingredient-item">🔹 <b>Fruttosio:</b> {fruttosio} g</div>
        <div class="ingredient-item">🔹 <b>Sale da Cucina Fino (Sodio):</b> {sale_cucina_g} g</div>
    """
    if usa_potassio_calcio:
        html_borraccia += f"""
        <div class="ingredient-item">🔹 <b>Citrato di Potassio (polvere):</b> {citrato_potassio_g} g <small>({potassio_mg}mg K+)</small></div>
        <div class="ingredient-item">🔹 <b>Citrato di Calcio (polvere):</b> {citrato_calcio_g} g <small>({calcio_mg}mg Ca2+)</small></div>
        """
    if eaa_g > 0:
        html_borraccia += f'<div class="ingredient-item">🔹 <b>Aminoacidi Essenziali (EAA):</b> {eaa_g} g</div>'
    
    html_borraccia += "<br><small>💡 <i>Aggiungi succo di 1 limone spremuto per migliorare il sapore e facilitare l'assorbimento.</i></small></div>"
    
    st.markdown(html_borraccia, unsafe_allow_html=True)

with col_right:
    # CARD PRE-WORKOUT & SPECIALISTICA
    html_pre = f"""
    <div class="card-preworkout">
        <div class="card-title" style="color: #B78103;">⚡ Integrazione Specialistica & Pre-Workout</div>
    """
    if citrullina_g > 0:
        html_pre += f"""
        <div class="ingredient-item">🧪 <b>L-Citrullina Malato (2:1):</b> <b>{citrullina_g} g</b></div>
        <div style="font-size:0.9rem; color:#555; margin-left:25px; margin-bottom:10px;">
        Sciogliere in 250-300 ml d'acqua e bere <b>30-45 min prima dello sforzo</b> (fornisce 4g Citrullina + 2g Acido Malico).
        </div>
        """
    if glicerolo_g > 0:
        html_pre += f"""
        <div class="ingredient-item">🧊 <b>Protocollo Glicerolo (Iperidratazione):</b> <b>{glicerolo_g} g</b></div>
        <div style="font-size:0.9rem; color:#555; margin-left:25px; margin-bottom:10px;">
        Sciogliere in 1 Litro d'acqua da bere <b>2 ore prima del via</b>.
        </div>
        """
    if caffeina_mg > 0:
        html_pre += f"""
        <div class="ingredient-item">☕ <b>Caffeina Anidra:</b> <b>{caffeina_mg} mg</b></div>
        <div style="font-size:0.9rem; color:#555; margin-left:25px;">
        Da assumere 45 min prima del via o divisa durante le fasi critiche dello sforzo.
        </div>
        """
    if citrullina_g == 0 and glicerolo_g == 0 and caffeina_mg == 0:
        html_pre += "<p>Nessun integratore pre-workout richiesto per questa configurazione.</p>"
        
    html_pre += "</div>"
    st.markdown(html_pre, unsafe_allow_html=True)

# --- STRATEGIA SOLIDI & RICETTE FAI-DA-TE ---
st.markdown("---")
st.subheader("🍫 Strategia Solidi & Ricettario Fai-da-Te")

if formato_carbo == "Misto (Liquidi + Barrette/Gel)" and n_barrette > 0:
    st.info(f"Hai scelto di apportare **{carbo_solidi}g di carboidrati** tramite **{n_barrette} solidi/gel** (30g carbo cad.), riducendo la quota da sciogliere in borraccia a **{carbo_liquidi}g**.")
    
    tab1, tab2, tab3 = st.tabs(["🌾 Rice Cakes Pro (Ciclismo)", "🍯 Barrette Avena & Datteri", "🧪 Gel Energetico Fai-da-Te"])
    
    with tab1:
        st.markdown("""
        #### 🍚 Rice Cakes Ciclismo (Stile Pro Tour)
        *Digeribilità immediata, perfette per evitare l'affaticamento gastrico durante uscite lunghe.*
        * **Resa:** 8 Porzioni da ~30g Carboidrati ciascuna.
        * **Ingredienti:** 250g Riso per minestre (Originario/Roma), 500ml Acqua, 30g Zucchero o Miele, 100g Philadelphia o Olio di cocco, Cannella/Marmellata.
        * **Preparazione:** 
            1. Stramangia il riso nell'acqua finché non ha assorbito tutto il liquido.
            2. A fuoco spento, incorporare il formaggio spalmabile e il miele/zucchero.
            3. Versa in una teglia (spessore 2 cm), compatta e lascia riposare in frigo tutta la notte.
            4. Taglia in 8 quadretti uguali e impacchetta con fogli d'alluminio.
        """)
    
    with tab2:
        st.markdown("""
        #### 🥣 Barrette Avena, Datteri e Miele (No-Cook)
        *Rilascio energetico graduale e costante per sforzi a media/bassa intensità.*
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
        *Pratico da mettere nelle Soft Flask morbide da 100ml.*
        * **Resa:** 2 Gel da ~30g Carboidrati ciascuno.
        * **Ingredienti:** 40g Maltodestrine, 20g Fruttosio, 35ml Acqua tiepida (o succo di limone), 1 pinch di sale.
        * **Preparazione:**
            1. Unisci le polveri secchi in un bicchiere.
            2. Versa l'acqua tiepida mescolando vigorosamente fino ad azzerare i grumi.
            3. Travasa nella soft flask ed è pronto all'uso.
        """)
else:
    st.write("Stai fornendo **il 100% dell'energia via borraccia**. Se desideri integrare solidi o preparare gel fai-da-te, seleziona la modalità **Misto** nel menu a sinistra.")
