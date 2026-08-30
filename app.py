
import streamlit as st

st.set_page_config(page_title="Calcolatore Integrazione Sportiva", page_icon="⚡")

st.title("⚡ Calcolatore Personalizzato di Integrazione")
st.write("Inserisci i dati della tua sessione per ottenere i dosaggi e la ricetta esatta.")

st.sidebar.header("📋 Parametri Atleta e Sessione")

# Inputs Utente
peso = st.sidebar.number_input("Peso Corporeo (kg)", min_value=40, max_value=130, value=70)
durata_min = st.sidebar.slider("Durata Allenamento (minuti)", min_value=30, max_value=360, value=120, step=15)
durata_ore = durata_min / 60.0

sport = st.sidebar.selectbox("Disciplina", ["Ciclismo", "Corsa", "Nuoto", "Palestra / Potenza", "Triathlon"])
intensita = st.sidebar.select_slider("Intensità Sforzo", options=["Bassa (Z1-Z2)", "Media (Z3)", "Alta / Gara (Z4-Z5)"])
temp = st.sidebar.slider("Temperatura Ambientale (°C)", min_value=5, max_value=40, value=25)
sudorazione = st.sidebar.selectbox("Tasso di Sudorazione", ["Basso", "Medio", "Alto (Maglietta bianca di sale)"])
tolleranza_carbo = st.sidebar.slider("Tolleranza Carboidrati (g/ora)", min_value=30, max_value=120, value=60, step=10)
sensib_caff = st.sidebar.selectbox("Sensibilità alla Caffeina", ["Nessuna", "Bassa / Media", "Alta"])

# Logica di Calcolo
if intensita == "Bassa (Z1-Z2)":
    carbo_h = min(40, tolleranza_carbo)
elif intensita == "Media (Z3)":
    carbo_h = min(60, tolleranza_carbo)
else:
    carbo_h = tolleranza_carbo

carbo_totali = round(carbo_h * durata_ore)
malto = round(carbo_totali * (2/3))
fruttosio = round(carbo_totali * (1/3))

# Idratazione e Sodio
acqua_h = 500 if temp < 20 else (750 if temp <= 28 else 1000)
if sudorazione == "Alto (Maglietta bianca di sale)":
    acqua_h += 200

acqua_totale = round((acqua_h * durata_ore) / 1000, 2) # in litri

base_sodio_l = 600 if temp < 25 else 800
if sudorazione == "Alto (Maglietta bianca di sale)":
    base_sodio_l += 300

sodio_mg_totali = round(base_sodio_l * acqua_totale)
sale_cucina_g = round(sodio_mg_totali / 393.4, 1) # 1g sale = 393.4mg Sodio

# Integrazione Avanzata
glicerolo_g = round(1.1 * peso, 1) if (temp >= 26 or durata_ore >= 3) else 0
eaa_g = 10 if durata_ore >= 2.5 else 0

caffeina_mg = 0
if sensib_caff == "Bassa / Media":
    caffeina_mg = round(3 * peso)
elif sensib_caff == "Alta":
    caffeina_mg = round(1.5 * peso)

# Output Risultati
st.markdown("---")
st.subheader("🎯 Risultati dell'Integrazione Totale")

col1, col2, col3 = st.columns(3)
col1.metric("Carboidrati Totali", f"{carbo_totali} g", f"{carbo_h} g/ora")
col2.metric("Acqua Consigliata", f"{acqua_totale} L", f"{acqua_h} ml/ora")
col3.metric("Sale da Cucina Totale", f"{sale_cucina_g} g", f"~{sodio_mg_totali} mg Sodio")

st.markdown("---")
st.subheader("🧪 Ripartizione Ingredienti Fai-da-Te")

st.write(f"**Carboidrati (Rapporto 2:1):**")
st.write(f"- Maltodestrine: **{malto} g**")
st.write(f"- Fruttosio: **{fruttosio} g**")

if glicerolo_g > 0:
    st.info(f"💡 **Protocollo Glicerolo (Caldo/Lunga Durata):** Aggiungi **{glicerolo_g} g** di glicerolo in 1 Litro d'acqua da bere 2 ore prima del via.")

if eaa_g > 0:
    st.write(f"- **Aminoacidi Essenziali (EAA):** {eaa_g} g (da sciogliere nella borraccia).")

if caffeina_mg > 0:
    st.write(f"- **Caffeina Anidra:** {caffeina_mg} mg (assunta 45 min prima dello sforzo o divisa a metà gara).")

st.markdown("---")
st.subheader("🍾 Ricetta Pratica per la Borraccia")
st.success(f"Sciogli in **{acqua_totale} Litri d'acqua** (divisi nelle tue borracce):\n"
           f"- {malto} g di Maltodestrine\n"
           f"- {fruttosio} g di Fruttosio\n"
           f"- {sale_cucina_g} g di Sale da Cucina fino\n"
           f"- Succo di 1-2 limoni per il gusto")
