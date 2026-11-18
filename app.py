import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇪🇹 Ethiopian Car Price Predictor",
    page_icon="🇪🇹",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background: linear-gradient(135deg, #0f3460, #16213e);
        color: white;
        border-radius: 10px;
        padding: 12px 0;
        font-size: 1rem;
        font-weight: 700;
        width: 100%;
        border: none;
    }
    .stButton>button:hover { opacity: 0.9; }
    .result-card {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        margin-top: 16px;
    }
    .price-text {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2e7d32;
    }
    .info-text {
        font-size: 0.9rem;
        color: #555;
        margin-top: 8px;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ── Load & train model ────────────────────────────────────────────────────────
@st.cache_resource
def load_and_train():
    df = pd.read_csv("ethiopia_car_data.csv")

    # Feature engineering
    df["Car_Age"] = 2026 - df["Year"]

    # Encode categoricals
    df_model = df.copy()
    df_model = pd.get_dummies(df_model,
                               columns=["Fuel_Type", "Seller_Type", "Transmission"],
                               drop_first=True)
    df_model.drop(columns=["Car_Name", "Year"], inplace=True)

    X = df_model.drop(columns=["Selling_Price_ETB"])
    y = df_model["Selling_Price_ETB"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return model, df, X.columns.tolist(), r2, mae, rmse

model, df, feature_cols, r2, mae, rmse = load_and_train()

# ── Present price lookup (average from dataset) ───────────────────────────────
present_price_map = df.groupby("Car_Name")["Present_Price_ETB"].mean().to_dict()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🇪🇹 Ethiopian Used Car Price Predictor")
st.markdown("Predict the **selling price** of a used car in **Ethiopian Birr (ETB)** using Machine Learning.")
st.markdown("---")

# ── Sidebar — model info ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Model Performance")
    st.metric("R² Score",  f"{r2:.3f}",  help="Closer to 1.0 = better")
    st.metric("MAE",       f"{mae:,.0f} ETB",  help="Average prediction error")
    st.metric("RMSE",      f"{rmse:,.0f} ETB", help="Root mean squared error")
    st.markdown("---")
    st.markdown("### 📂 Dataset")
    st.markdown(f"**{len(df)} listings** · **{df['Car_Name'].nunique()} car models**")
    st.markdown("Sources: [mekina.net](https://mekina.net) · [jiji.com.et](https://jiji.com.et)")
    st.markdown("---")
    st.markdown("### 🔬 Algorithm")
    st.markdown("**Linear Regression** (scikit-learn)")
    st.markdown("Features: Present Price, Car Age, Km Driven, Fuel, Transmission, Seller, Owners")

# ── Input form ────────────────────────────────────────────────────────────────
car_names = sorted(df["Car_Name"].unique().tolist())

col1, col2 = st.columns(2)

with col1:
    car_name = st.selectbox("🚗 Car Model", car_names)
    year     = st.number_input("📅 Year of Manufacture", min_value=2000, max_value=2026,
                                value=2018, step=1)
    kms      = st.number_input("📏 Kilometers Driven", min_value=0, max_value=500000,
                                value=60000, step=5000)

with col2:
    fuel         = st.selectbox("⛽ Fuel Type",     ["Petrol", "Diesel"])
    transmission = st.selectbox("⚙️ Transmission",  ["Manual", "Automatic"])
    seller       = st.selectbox("🏪 Seller Type",   ["Dealer", "Individual"])
    owners       = st.selectbox("👤 Previous Owners", [0, 1, 2, 3],
                                 format_func=lambda x: f"{x} {'(First owner)' if x==0 else ''}")

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("🔍 Predict Price"):
    # Build input row matching training columns
    car_age       = 2026 - year
    present_price = present_price_map.get(car_name, df["Present_Price_ETB"].mean())

    input_data = {
        "Present_Price_ETB":      present_price,
        "Kms_Driven":             kms,
        "Owner":                  owners,
        "Car_Age":                car_age,
        "Fuel_Type_Petrol":       1 if fuel == "Petrol" else 0,
        "Seller_Type_Individual": 1 if seller == "Individual" else 0,
        "Transmission_Manual":    1 if transmission == "Manual" else 0,
    }

    input_df = pd.DataFrame([input_data])

    # Align columns with training set
    for col in feature_cols:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_cols]

    prediction = model.predict(input_df)[0]
    prediction = max(prediction, 800000)
    prediction = round(prediction / 50000) * 50000

    etb_m = prediction / 1_000_000

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:0.85rem;color:#555;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">
            Estimated Selling Price
        </div>
        <div class="price-text">{etb_m:.2f} Million ETB</div>
        <div class="info-text">
            {car_name} · {year} · {kms:,} km · {fuel} · {transmission} · {seller}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show comparable listings from dataset
    st.markdown("#### 📋 Similar listings in our dataset")
    similar = df[df["Car_Name"] == car_name].copy()
    similar = similar[["Car_Name","Year","Selling_Price_ETB","Kms_Driven",
                        "Fuel_Type","Transmission","Seller_Type","Owner"]]
    similar = similar.sort_values("Year", ascending=False).head(5).reset_index(drop=True)
    similar["Selling_Price_ETB"] = similar["Selling_Price_ETB"].apply(lambda x: f"{x:,}")
    similar["Kms_Driven"]        = similar["Kms_Driven"].apply(lambda x: f"{x:,}")
    st.dataframe(similar, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:0.8rem;'>"
    "Prices calibrated from mekina.net & jiji.com.et · November 2026 · "
    "Built with Python, scikit-learn & Streamlit"
    "</p>",
    unsafe_allow_html=True
)
