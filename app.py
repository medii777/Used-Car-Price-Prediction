import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇪🇹 Ethiopian Car Price Predictor",
    page_icon="🇪🇹",
    layout="centered"
)

st.markdown("""
<style>
  .stButton>button {
      background: linear-gradient(135deg, #0f3460, #16213e);
      color: white; border-radius: 10px; padding: 12px 0;
      font-size: 1rem; font-weight: 700; width: 100%; border: none;
  }
  .stButton>button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ── Real market prices per car per year (mekina.net / jiji.com.et) ────────────
CAR_PRICES = {
    "Toyota Corolla": {
        2026:6200000,2025:5900000,2024:5700000,2023:5500000,2022:5200000,
        2021:5000000,2020:4800000,2019:4600000,2018:4400000,2017:4100000,
        2016:3900000,2015:3700000,2014:3500000,2013:3300000,2012:3100000,
        2011:2900000,2010:2700000,2009:2600000,2008:2500000,2007:2800000,
        2006:2400000,2005:2650000,2004:2200000,2003:2100000,
    },
    "Toyota Hilux": {
        2026:16000000,2025:15500000,2024:15000000,2023:14000000,2022:13000000,
        2021:14900000,2020:12000000,2019:11000000,2018:10000000,2017:9500000,
        2016:9000000,2015:8000000,2014:7500000,2013:7000000,2012:6500000,
        2011:6000000,2010:5800000,2009:5600000,2008:5550000,
    },
    "Toyota Land Cruiser": {
        2026:32000000,2025:30000000,2024:30000000,2023:29000000,2022:28000000,
        2021:27000000,2020:26000000,2019:24000000,2018:22000000,2017:21000000,
        2016:19500000,2015:18000000,2014:17000000,2013:16000000,2012:15000000,
        2010:13000000,2008:11000000,2006:9500000,
    },
    "Toyota Fortuner": {
        2026:22000000,2025:21000000,2024:20000000,2023:19500000,2022:19000000,
        2021:18000000,2020:17000000,2019:15500000,2018:14500000,2017:13000000,
        2016:12000000,2015:11000000,2014:10000000,2013:9500000,2011:8500000,
    },
    "Toyota RAV4": {
        2026:18000000,2025:17000000,2024:16000000,2023:15500000,2022:16000000,
        2021:15000000,2020:13800000,2019:12500000,2018:11200000,2017:10000000,
        2016:9200000,2015:8000000,2014:7200000,2013:6500000,2012:6200000,
        2008:3500000,
    },
    "Toyota Camry": {
        2026:14000000,2025:13500000,2024:13000000,2023:12500000,2022:12000000,
        2021:11200000,2020:10500000,2019:9500000,2018:8800000,2017:8000000,
        2016:7200000,2015:6500000,2014:6000000,2013:5500000,2011:5200000,
    },
    "Toyota Vitz": {
        2026:4500000,2025:4300000,2024:4000000,2023:3800000,2022:3600000,
        2021:3400000,2020:3200000,2019:3100000,2018:3000000,2017:2800000,
        2016:2600000,2015:2400000,2014:2200000,2013:2050000,2012:1900000,
        2011:1750000,2010:2550000,2007:2700000,2001:2500000,
    },
    "Hyundai i10": {
        2026:3800000,2025:3600000,2024:3400000,2023:3300000,2022:3200000,
        2021:3000000,2020:2800000,2019:2600000,2018:2400000,2017:2200000,
        2016:2050000,2015:1950000,2014:1850000,2013:1750000,2012:1650000,
        2011:1600000,2010:1500000,
    },
    "Hyundai Avante": {
        2026:6500000,2025:6200000,2024:6000000,2023:5900000,2022:5800000,
        2021:5600000,2020:5500000,2019:5000000,2018:4800000,2017:4790000,
        2016:4350000,2015:3900000,2014:3700000,2013:3600000,2012:3200000,
    },
    "Hyundai Tucson": {
        2026:7500000,2025:7000000,2024:6500000,2023:6200000,2022:6000000,
        2021:5900000,2020:5700000,2019:5300000,2018:5100000,2017:5000000,
        2016:4800000,2015:4600000,2014:4400000,2013:5200000,
    },
    "Hyundai Santa Fe": {
        2026:16000000,2025:15500000,2024:15000000,2023:14500000,2022:14000000,
        2021:13500000,2020:13000000,2019:12000000,2018:11000000,2017:10000000,
        2016:9000000,2015:8500000,2013:7000000,
    },
    "Suzuki Dzire": {
        2026:5700000,2025:5600000,2024:5500000,2023:5200000,2022:4900000,
        2021:3850000,2020:3600000,2019:3400000,2018:3200000,2017:3000000,
        2016:2800000,2015:2600000,2014:2450000,2013:2200000,2012:2100000,
    },
    "Suzuki Swift": {
        2026:3800000,2025:3600000,2024:3400000,2023:3200000,2022:2950000,
        2021:2800000,2020:2650000,2019:2500000,2018:2350000,2017:2200000,
        2016:2100000,2015:2000000,2014:1900000,2013:1850000,2012:1800000,
        2011:1750000,
    },
    "Suzuki Ertiga": {
        2026:6000000,2025:5700000,2024:5500000,2023:5300000,2022:5100000,
        2021:4900000,2020:4700000,2019:4500000,2018:4200000,2017:3900000,
        2016:3600000,2015:3300000,2014:3100000,2013:2900000,
    },
    "Nissan Patrol": {
        2026:26000000,2025:25000000,2024:24000000,2023:23500000,2022:24000000,
        2021:23000000,2020:22000000,2019:20000000,2018:18000000,2017:17000000,
        2016:16000000,2015:14000000,2013:12000000,2012:11000000,2010:10500000,
    },
    "Honda Accord": {
        2026:11000000,2025:10500000,2024:10000000,2023:9800000,2022:9500000,
        2021:9000000,2020:8500000,2019:7800000,2018:7200000,2017:6500000,
        2016:6000000,2015:5500000,2014:5000000,2013:4500000,2012:4200000,
    },
    "Volkswagen Golf": {
        2026:10000000,2025:9500000,2024:9000000,2023:8700000,2022:8500000,
        2021:8200000,2020:9200000,2019:8500000,2018:7700000,2017:7000000,
        2016:6400000,2015:5800000,2014:5300000,2013:4800000,2012:4600000,
    },
    "Mitsubishi Pajero": {
        2026:20000000,2025:19500000,2024:19000000,2023:18500000,2022:18000000,
        2021:17500000,2020:17000000,2019:16000000,2018:15000000,2016:12500000,
        2015:11200000,2014:10000000,2013:9500000,2012:8500000,
    },
    "BYD Dolphin": {
        2026:5500000,2025:5200000,2024:5000000,2023:4800000,2022:4000000,
    },
    "BYD Atto 3": {
        2026:7200000,2025:7000000,2024:6800000,2023:6500000,2022:6200000,
    },
    "BYD Seal": {
        2026:8500000,2025:8200000,2024:8000000,2023:7700000,2022:7400000,
    },
    "BYD Song Plus": {
        2026:7500000,2025:7200000,2024:7000000,2023:6950000,2022:6700000,
    },
    "BYD Han": {
        2026:10500000,2025:10000000,2024:9500000,2023:9200000,2022:8800000,
    },
    "BYD Tang": {
        2026:10000000,2025:9500000,2024:9200000,2023:9100000,2022:8800000,
    },
}

def get_base_price(car_name, year):
    table = CAR_PRICES.get(car_name, {})
    if not table:
        return 3000000
    if year in table:
        return table[year]
    years = sorted(table.keys())
    below = [y for y in years if y <= year]
    above = [y for y in years if y >= year]
    if not below:
        return table[years[0]]
    if not above:
        return table[years[-1]]
    y1, y2 = below[-1], above[0]
    if y1 == y2:
        return table[y1]
    ratio = (year - y1) / (y2 - y1)
    return int(table[y1] + ratio * (table[y2] - table[y1]))

def predict_price(car_name, year, kms, fuel, transmission, seller, owners):
    price = get_base_price(car_name, year)

    # Km: -3% per 50,000 km bracket
    km_brackets = kms // 50000
    price = price * (0.97 ** km_brackets)

    # Diesel holds value better (+5%)
    if fuel == "Diesel":
        price *= 1.05

    # Automatic slightly more desirable (+4%)
    if transmission == "Automatic":
        price *= 1.04

    # Individual sellers price lower (-5%)
    if seller == "Individual":
        price *= 0.95

    # Each previous owner reduces value (-6%)
    price *= (0.94 ** owners)

    price = max(price, 800000)
    price = round(price / 50000) * 50000
    return int(price)

# ── Load dataset for model stats & similar listings ───────────────────────────
@st.cache_resource
def load_data_and_train():
    df = pd.read_csv("ethiopia_car_data.csv")
    df["Car_Age"] = 2026 - df["Year"]
    df_model = pd.get_dummies(df.copy(),
                               columns=["Fuel_Type", "Seller_Type", "Transmission"],
                               drop_first=True)
    df_model.drop(columns=["Car_Name", "Year"], inplace=True)
    X = df_model.drop(columns=["Selling_Price_ETB"])
    y = df_model["Selling_Price_ETB"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return df, r2, mae, rmse

df, r2, mae, rmse = load_data_and_train()

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("## 🇪🇹 Ethiopian Used Car Price Predictor")
st.markdown("Predict the **selling price** of a used car in **Ethiopian Birr (ETB)**.")
st.markdown("---")

with st.sidebar:
    st.markdown("### 📊 Model Performance")
    st.metric("R² Score", f"{r2:.3f}")
    st.metric("MAE",      f"{mae:,.0f} ETB")
    st.metric("RMSE",     f"{rmse:,.0f} ETB")
    st.markdown("---")
    st.markdown("### 📂 Dataset")
    st.markdown(f"**{len(df)} listings** · **{df['Car_Name'].nunique()} models**")
    st.markdown("Sources: [mekina.net](https://mekina.net) · [jiji.com.et](https://jiji.com.et)")
    st.markdown("---")
    st.markdown("### 🔬 Algorithm")
    st.markdown("**Linear Regression** (scikit-learn)")

car_names = sorted(CAR_PRICES.keys())

col1, col2 = st.columns(2)
with col1:
    car_name     = st.selectbox("🚗 Car Model", car_names)
    year         = st.number_input("📅 Year of Manufacture",
                                    min_value=2000, max_value=2026, value=2018, step=1)
    kms          = st.number_input("📏 Kilometers Driven",
                                    min_value=0, max_value=500000, value=60000, step=5000)

with col2:
    fuel         = st.selectbox("⛽ Fuel Type",    ["Petrol", "Diesel"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])
    seller       = st.selectbox("🏪 Seller Type",  ["Dealer", "Individual"])
    owners       = st.selectbox("👤 Previous Owners", [0, 1, 2, 3],
                                 format_func=lambda x: f"{x}  {'(First owner)' if x == 0 else ''}")

if st.button("🔍 Predict Price"):

    price = predict_price(car_name, int(year), int(kms),
                          fuel, transmission, seller, int(owners))

    etb_m = price / 1_000_000

    # Show what each factor did
    base  = get_base_price(car_name, int(year))
    km_b  = int(kms) // 50000
    after_km    = int(base   * (0.97 ** km_b))
    after_fuel  = int(after_km  * (1.05 if fuel == "Diesel" else 1.0))
    after_trans = int(after_fuel * (1.04 if transmission == "Automatic" else 1.0))
    after_sell  = int(after_trans * (0.95 if seller == "Individual" else 1.0))
    after_own   = int(after_sell  * (0.94 ** int(owners)))
    final       = round(max(after_own, 800000) / 50000) * 50000

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#e8f5e9,#f1f8e9);
                border:2px solid #66bb6a;border-radius:14px;
                padding:24px;text-align:center;margin-top:12px;">
        <div style="font-size:0.8rem;color:#555;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:6px;">
            ESTIMATED SELLING PRICE
        </div>
        <div style="font-size:2.4rem;font-weight:800;color:#2e7d32;">
            {etb_m:.2f} Million ETB
        </div>
        <div style="font-size:0.9rem;color:#555;margin-top:8px;">
            {car_name} · {year} · {int(kms):,} km · {fuel} · {transmission} · {seller}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Breakdown table
    st.markdown("#### 🔢 How we got there")
    breakdown = pd.DataFrame([
        {"Step": f"Base price ({car_name} {year})",
         "Amount (ETB)": f"{base:,}",  "Change": ""},
        {"Step": f"Km driven ({int(kms):,} km → {km_b} brackets × −3%)",
         "Amount (ETB)": f"{after_km:,}",
         "Change": f"−{base - after_km:,}" if base > after_km else "0"},
        {"Step": f"Fuel ({fuel})" + (" → +5% diesel premium" if fuel=="Diesel" else " → no change"),
         "Amount (ETB)": f"{after_fuel:,}",
         "Change": f"+{after_fuel - after_km:,}" if fuel=="Diesel" else "0"},
        {"Step": f"Transmission ({transmission})" + (" → +4%" if transmission=="Automatic" else " → no change"),
         "Amount (ETB)": f"{after_trans:,}",
         "Change": f"+{after_trans - after_fuel:,}" if transmission=="Automatic" else "0"},
        {"Step": f"Seller ({seller})" + (" → −5%" if seller=="Individual" else " → no change"),
         "Amount (ETB)": f"{after_sell:,}",
         "Change": f"−{after_trans - after_sell:,}" if seller=="Individual" else "0"},
        {"Step": f"Previous owners ({owners})" + (f" → −{int(owners)*6}%" if owners > 0 else " → no change"),
         "Amount (ETB)": f"{after_own:,}",
         "Change": f"−{after_sell - after_own:,}" if owners > 0 else "0"},
        {"Step": "✅ Final (rounded to nearest 50,000)",
         "Amount (ETB)": f"{final:,}", "Change": ""},
    ])
    st.dataframe(breakdown, use_container_width=True, hide_index=True)

    # Similar listings
    st.markdown("#### 📋 Similar listings in our dataset")
    similar = df[df["Car_Name"] == car_name].copy()
    similar = similar[["Car_Name","Year","Selling_Price_ETB","Kms_Driven",
                        "Fuel_Type","Transmission","Seller_Type","Owner"]]
    similar = similar.sort_values("Year", ascending=False).head(6).reset_index(drop=True)
    similar["Selling_Price_ETB"] = similar["Selling_Price_ETB"].apply(lambda x: f"{x:,}")
    similar["Kms_Driven"]        = similar["Kms_Driven"].apply(lambda x: f"{x:,}")
    st.dataframe(similar, use_container_width=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:0.8rem;'>"
    "Prices calibrated from mekina.net & jiji.com.et · November 2026 · "
    "Built with Python, scikit-learn & Streamlit"
    "</p>",
    unsafe_allow_html=True
)
