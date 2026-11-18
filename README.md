# 🇪🇹 Ethiopian Used Car Price Predictor

A machine learning project that predicts the **selling price of used cars in Ethiopia** in **Ethiopian Birr (ETB)** using Linear Regression — plus a simple browser-based frontend for instant predictions.

> Data inspired by real Ethiopian car market listings from [mekina.net](https://www.mekina.net/) and [jiji.com.et](https://jiji.com.et/cars).

---

## � Quick Start (No Python Required)

Just open **`car_price_predictor.html`** in your browser — fill in the form and get an instant price estimate.

---

## 🚗 Ethiopian Car Market Context

| Brand | Popular Models | Avg Price Range (ETB) |
|---|---|---|
| Toyota | Corolla, Hilux, Land Cruiser, RAV4 | 2.1M – 35M |
| Hyundai | i10, Avante, Tucson, Santa Fe | 1.5M – 18M |
| Suzuki | Dzire, Swift, Ertiga | 2.1M – 5.9M |
| Nissan | Patrol | 10.5M – 29M |
| Honda | Accord | 4.2M – 12M |

> 💱 Currency: **Ethiopian Birr (ETB)** — approx. 1 USD ≈ 130 ETB (2026)

---

## 📦 Dataset

`ethiopia_car_data.csv` — 227 used car listings with the following features:

| Column | Description |
|---|---|
| `Car_Name` | Model name (Toyota Corolla, Hilux, etc.) |
| `Year` | Manufacturing year |
| `Selling_Price_ETB` | **Target** — actual selling price in ETB |
| `Present_Price_ETB` | Current showroom/market price in ETB |
| `Kms_Driven` | Total kilometers driven |
| `Fuel_Type` | Petrol or Diesel |
| `Seller_Type` | Dealer or Individual |
| `Transmission` | Manual or Automatic |
| `Owner` | Number of previous owners |

---

## 🧠 How the Model Works

The notebook (`Ethiopian Car Price Prediction.ipynb`) trains a **Linear Regression** model using scikit-learn. Here's the full pipeline:

1. **Feature Engineering** — adds `Car_Age = 2026 − Year`
2. **Preprocessing** — one-hot encodes categorical columns (Fuel_Type, Seller_Type, Transmission)
3. **Train/Test Split** — 80% training, 20% testing
4. **Model Training** — `sklearn.linear_model.LinearRegression`
5. **Evaluation** — R², MAE, RMSE, actual vs predicted plot

Key patterns the model learns:
- Higher `Present_Price_ETB` → Higher selling price
- Older cars (`Car_Age` ↑) → Lower price
- More `Kms_Driven` → Lower price
- Diesel vehicles (Hilux, Land Cruiser) → Premium pricing

---

## �️ Project Files

| File | Description |
|---|---|
| `car_price_predictor.html` | ✅ Simple browser frontend — open and use instantly |
| `Ethiopian Car Price Prediction.ipynb` | Full ML notebook with training, charts, evaluation |
| `ethiopia_car_data.csv` | Training dataset (227 listings) |
| `Car Price Prediction.ipynb` | Original USD-based notebook (reference only) |

---

## 🔬 Running the Notebook (Optional)

If you want to explore the full ML training process:

```bash
pip install pandas matplotlib seaborn scikit-learn notebook
python -m jupyter notebook
```

Then open **`Ethiopian Car Price Prediction.ipynb`**.

---

## 🔧 Future Improvements

- Add more real listings from [mekina.net](https://www.mekina.net/) or [jiji.com.et](https://jiji.com.et/cars)
- Try Random Forest or XGBoost for better accuracy
- Add features: car condition, region (Addis Ababa, Dire Dawa, Hawassa), import status
- Deploy the web frontend online (GitHub Pages, Netlify)

---

## 📄 License

MIT License
"# Used-Car-Price-Prediction" 
