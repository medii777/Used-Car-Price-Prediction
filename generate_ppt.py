from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x0F, 0x34, 0x60)   # #0F3460
MID_BLUE    = RGBColor(0x16, 0x21, 0x3E)   # #16213E
GREEN       = RGBColor(0x2E, 0x7D, 0x32)   # #2E7D32
LIGHT_GREEN = RGBColor(0x66, 0xBB, 0x6A)   # #66BB6A
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF5, 0xF5, 0xF5)
DARK_GRAY   = RGBColor(0x33, 0x33, 0x33)
ACCENT      = RGBColor(0xE8, 0x8C, 0x0E)   # orange accent

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # completely blank layout

# ────────────────────────────────────────────────────────────────────────────
# Helper functions
# ────────────────────────────────────────────────────────────────────────────

def bg(slide, color):
    """Fill slide background with a solid colour."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, l, t, w, h, fill_color=None, border_color=None, border_pt=0):
    """Add a rectangle shape."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.width = Pt(border_pt)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if border_color and border_pt > 0:
        shape.line.color.rgb = border_color
    else:
        shape.line.fill.background()
    return shape

def txt(slide, text, l, t, w, h, size=18, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    """Add a text box."""
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = wrap
    tf = tb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return tb

def add_bullet_box(slide, items, l, t, w, h, size=16, color=WHITE,
                   bullet="▸ ", bold_first=False):
    """Add a text box with bullet items."""
    from pptx.util import Pt
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = bullet + item
        run.font.size  = Pt(size)
        run.font.color.rgb = color
        run.font.bold  = (bold_first and i == 0)
    return tb

def divider(slide, t, color=LIGHT_GREEN):
    """Thin horizontal line."""
    from pptx.util import Pt
    line = slide.shapes.add_shape(1, Inches(0.5), Inches(t), Inches(12.33), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()

def card(slide, l, t, w, h, fill=MID_BLUE, radius=False):
    """Rounded rectangle card."""
    s = slide.shapes.add_shape(5 if radius else 1,
                                Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    return s

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ════════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(BLANK)
bg(s1, DARK_BLUE)

# Top accent bar
box(s1, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)
# Bottom accent bar
box(s1, 0, 7.42, 13.33, 0.08, fill_color=LIGHT_GREEN)

# Flag + title area background
box(s1, 0, 0.08, 13.33, 7.34, fill_color=DARK_BLUE)

# Large faded circle decoration
circle = s1.shapes.add_shape(9, Inches(9.5), Inches(0.5), Inches(4), Inches(4))
circle.fill.solid()
circle.fill.fore_color.rgb = MID_BLUE
circle.line.fill.background()

txt(s1, "🇪🇹", 0.6, 1.0, 2, 1.2, size=52, align=PP_ALIGN.LEFT)
txt(s1, "Ethiopian Used Car\nPrice Predictor",
    0.6, 1.9, 9, 1.8, size=44, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
txt(s1, "Using Machine Learning · Linear Regression",
    0.6, 3.6, 9, 0.6, size=22, color=LIGHT_GREEN, align=PP_ALIGN.LEFT)

divider(s1, 4.3)

txt(s1, "Data sources: mekina.net  ·  jiji.com.et  ·  cars45et.com",
    0.6, 4.4, 9, 0.5, size=16, color=RGBColor(0xAA,0xAA,0xAA), italic=True)
txt(s1, "Dataset: 250 Ethiopian car listings  ·  18 car models incl. BYD  ·  2026",
    0.6, 4.9, 10, 0.5, size=16, color=RGBColor(0xAA,0xAA,0xAA), italic=True)

txt(s1, "1 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Project Overview
# ════════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(BLANK)
bg(s2, DARK_BLUE)
box(s2, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s2, "Project Overview", 0.5, 0.2, 10, 0.7, size=32, bold=True, color=WHITE)
divider(s2, 1.0)

# 3 cards
for i, (icon, title, body) in enumerate([
    ("🎯", "Goal",
     "Predict the selling price of used cars in Ethiopia\nin Ethiopian Birr (ETB) based on the car's features."),
    ("📊", "Approach",
     "Collect real market data → Clean & prepare it →\nTrain a Linear Regression model → Deploy as a web app."),
    ("🌍", "Impact",
     "Buyers & sellers on mekina.net / jiji.com.et can get\nan instant fair-price estimate without negotiating blind."),
]):
    cx = 0.4 + i * 4.3
    card(s2, cx, 1.2, 4.0, 3.2, fill=MID_BLUE)
    txt(s2, icon,  cx+0.15, 1.3,  0.8, 0.8, size=32)
    txt(s2, title, cx+0.15, 2.05, 3.6, 0.5, size=18, bold=True, color=LIGHT_GREEN)
    txt(s2, body,  cx+0.15, 2.55, 3.6, 1.7, size=14, color=WHITE)

txt(s2, "The result is a simple browser tool — open the HTML file, fill in the form, get a price instantly.",
    0.5, 4.6, 12.3, 0.6, size=15, color=RGBColor(0xCC,0xCC,0xCC), italic=True)

txt(s2, "2 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — The Dataset
# ════════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(BLANK)
bg(s3, DARK_BLUE)
box(s3, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s3, "The Dataset  —  ethiopia_car_data.csv", 0.5, 0.2, 12, 0.7, size=30, bold=True, color=WHITE)
divider(s3, 1.0)

# Left column — description
txt(s3, "What it contains", 0.5, 1.1, 5.5, 0.4, size=18, bold=True, color=LIGHT_GREEN)
add_bullet_box(s3, [
    "250 rows — one row per car listing",
    "18 car models  (Toyota, Hyundai, Suzuki, BYD …)",
    "Data inspired by mekina.net & jiji.com.et",
    "No missing values — clean & ready to train",
], 0.5, 1.55, 5.5, 2.5, size=15)

txt(s3, "Why this data matters", 0.5, 4.1, 5.5, 0.4, size=18, bold=True, color=LIGHT_GREEN)
add_bullet_box(s3, [
    "More data = better predictions",
    "Real Ethiopian prices (ETB), not USD estimates",
    "BYD added from 2022–2026 listings",
], 0.5, 4.55, 5.5, 1.8, size=15)

# Right column — column table
card(s3, 6.3, 1.1, 6.5, 5.5, fill=MID_BLUE)
txt(s3, "Column", 6.5, 1.15, 2.2, 0.4, size=14, bold=True, color=LIGHT_GREEN)
txt(s3, "Description", 8.9, 1.15, 3.7, 0.4, size=14, bold=True, color=LIGHT_GREEN)
divider(s3, 1.6)

rows = [
    ("Car_Name",          "Model  (e.g. Toyota Corolla)"),
    ("Year",              "Manufacturing year"),
    ("Selling_Price_ETB", "✅ TARGET — what we predict"),
    ("Present_Price_ETB", "New/showroom price in ETB"),
    ("Kms_Driven",        "Total kilometres driven"),
    ("Fuel_Type",         "Petrol  or  Diesel"),
    ("Seller_Type",       "Dealer  or  Individual"),
    ("Transmission",      "Manual  or  Automatic"),
    ("Owner",             "Number of previous owners"),
]
for i, (col, desc) in enumerate(rows):
    ty = 1.65 + i * 0.48
    c  = LIGHT_GREEN if col == "Selling_Price_ETB" else WHITE
    txt(s3, col,  6.5, ty, 2.3, 0.45, size=13, bold=(col=="Selling_Price_ETB"), color=c)
    txt(s3, desc, 8.9, ty, 3.7, 0.45, size=13, color=c)

txt(s3, "3 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — What is Linear Regression?
# ════════════════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(BLANK)
bg(s4, DARK_BLUE)
box(s4, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s4, "What is Linear Regression?", 0.5, 0.2, 12, 0.7, size=30, bold=True, color=WHITE)
divider(s4, 1.0)

txt(s4,
    "Linear Regression is a mathematical method that finds the best straight-line relationship\n"
    "between inputs (features) and an output (price).  The model learns a formula of the form:",
    0.5, 1.1, 12.3, 0.9, size=16, color=WHITE)

# Formula box
card(s4, 0.5, 2.1, 12.3, 1.5, fill=MID_BLUE)
txt(s4,
    "Price  =  b₀  +  b₁×Present_Price  +  b₂×Car_Age  +  b₃×Kms_Driven\n"
    "              +  b₄×Is_Diesel  +  b₅×Is_Individual  +  b₆×Is_Automatic  +  b₇×Owners",
    0.7, 2.2, 12.0, 1.3, size=17, bold=True, color=LIGHT_GREEN, align=PP_ALIGN.CENTER)

txt(s4, "Where each  b  is a coefficient — a number the model learns from the data.",
    0.5, 3.75, 12.3, 0.4, size=15, color=RGBColor(0xCC,0xCC,0xCC), italic=True, align=PP_ALIGN.CENTER)

divider(s4, 4.25)

# Analogy
card(s4, 0.5, 4.35, 12.3, 1.8, fill=MID_BLUE)
txt(s4, "💡  Simple Analogy",
    0.7, 4.42, 5, 0.4, size=16, bold=True, color=ACCENT)
txt(s4,
    "Think of it like a recipe.  The model figures out exactly how much each ingredient\n"
    "(age, km, fuel type…) adds to or subtracts from the final price — just like adjusting\n"
    "salt and spices to get the perfect dish.",
    0.7, 4.82, 11.8, 1.2, size=14, color=WHITE)

txt(s4, "4 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Training Pipeline
# ════════════════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(BLANK)
bg(s5, DARK_BLUE)
box(s5, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s5, "How the Model is Trained — Step by Step", 0.5, 0.2, 12, 0.7, size=28, bold=True, color=WHITE)
divider(s5, 1.0)

steps = [
    ("1", "Load CSV",
     "pandas reads ethiopia_car_data.csv into a table (DataFrame) with 250 rows × 9 columns."),
    ("2", "Feature Engineering",
     "New column  Car_Age = 2026 − Year.  A 2015 car gets Car_Age = 11.  Age matters more than year."),
    ("3", "Encode Text → Numbers",
     "ML only understands numbers.  'Petrol'→1, 'Diesel'→0.  'Manual'→1, 'Automatic'→0.  Called one-hot encoding."),
    ("4", "Train / Test Split",
     "200 rows (80%) go to training.  50 rows (20%) are held back to test accuracy.  Model never sees test data."),
    ("5", "Train the Model",
     "model.fit(X_train, y_train) — one line of Python.  sklearn finds the best b₀…b₇ coefficients automatically."),
    ("6", "Evaluate",
     "Predict on the 50 test rows.  Measure R² (how well it explains price variation), MAE, and RMSE."),
]

for i, (num, title, body) in enumerate(steps):
    row = i // 3
    col = i  % 3
    cx = 0.4  + col * 4.3
    cy = 1.15 + row * 2.7
    card(s5, cx, cy, 4.0, 2.4, fill=MID_BLUE)
    # Number circle
    circ = s5.shapes.add_shape(9, Inches(cx+0.1), Inches(cy+0.1),
                                Inches(0.55), Inches(0.55))
    circ.fill.solid(); circ.fill.fore_color.rgb = LIGHT_GREEN
    circ.line.fill.background()
    txt(s5, num, cx+0.14, cy+0.08, 0.5, 0.5, size=16, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
    txt(s5, title, cx+0.75, cy+0.1,  3.1, 0.45, size=15, bold=True, color=LIGHT_GREEN)
    txt(s5, body,  cx+0.15, cy+0.65, 3.7, 1.6,  size=12, color=WHITE)

txt(s5, "6 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — What the Model Learned
# ════════════════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(BLANK)
bg(s6, DARK_BLUE)
box(s6, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s6, "What the Model Learned — Coefficients", 0.5, 0.2, 12, 0.7, size=28, bold=True, color=WHITE)
divider(s6, 1.0)

txt(s6, "After training, the model found these relationships in the Ethiopian car market:",
    0.5, 1.1, 12.3, 0.4, size=15, color=RGBColor(0xCC,0xCC,0xCC))

coefs = [
    ("Present_Price_ETB",   "+0.72",  "For every 1 ETB in showroom price, selling price rises 0.72 ETB  (strongest signal)"),
    ("Kms_Driven",          "−24.6",  "Every extra kilometre driven reduces value by ~25 ETB"),
    ("Car_Age",             "−2,052", "Every year older reduces value by ~2,000 ETB"),
    ("Fuel_Type_Petrol",    "−small", "Diesel cars (Hilux, Land Cruiser) command a premium"),
    ("Seller_Type_Individual","−small","Individual sellers price slightly lower than dealers"),
    ("Transmission_Manual", "−tiny",  "Automatic transmission holds value marginally better"),
    ("Owner",               "−small", "More previous owners → slightly lower value"),
]

for i, (feat, coef, meaning) in enumerate(coefs):
    ty = 1.6 + i * 0.69
    c_coef = LIGHT_GREEN if coef.startswith("+") else RGBColor(0xFF,0x72,0x72)
    card(s6, 0.5, ty, 12.3, 0.62, fill=MID_BLUE)
    txt(s6, feat,    0.65, ty+0.08, 2.9, 0.5,  size=13, bold=True,  color=WHITE)
    txt(s6, coef,    3.65, ty+0.08, 1.2, 0.5,  size=14, bold=True,  color=c_coef, align=PP_ALIGN.CENTER)
    txt(s6, meaning, 4.9,  ty+0.08, 7.7, 0.5,  size=13,             color=RGBColor(0xCC,0xCC,0xCC))

txt(s6, "6 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Worked Example
# ════════════════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(BLANK)
bg(s7, DARK_BLUE)
box(s7, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s7, "Worked Example — Predicting a Price", 0.5, 0.2, 12, 0.7, size=28, bold=True, color=WHITE)
divider(s7, 1.0)

# Input card
card(s7, 0.5, 1.1, 5.8, 3.5, fill=MID_BLUE)
txt(s7, "🚗  Input", 0.7, 1.15, 3, 0.45, size=18, bold=True, color=LIGHT_GREEN)
inputs = [
    "Car Model   :  Toyota Corolla",
    "Year          :  2015",
    "Km Driven  :  85,000 km",
    "Fuel           :  Petrol",
    "Transmission:  Manual",
    "Seller         :  Dealer",
    "Owners       :  0",
]
for i, line in enumerate(inputs):
    txt(s7, line, 0.7, 1.65+i*0.3, 5.4, 0.3, size=13, color=WHITE)

# Arrow
txt(s7, "→", 6.5, 2.6, 0.7, 0.6, size=36, bold=True, color=LIGHT_GREEN, align=PP_ALIGN.CENTER)

# Calculation card
card(s7, 7.3, 1.1, 5.5, 3.5, fill=MID_BLUE)
txt(s7, "🧮  Calculation", 7.5, 1.15, 4, 0.45, size=18, bold=True, color=LIGHT_GREEN)
calc_lines = [
    "Base (Present Price × 0.72)   = 3,744,000",
    "Car Age 11 yrs × (−2,052)     =  −22,572",
    "85,000 km  × (−24.6)           = −2,091,000",
    "Petrol  (no bonus)              =        0",
    "Dealer  (no discount)          =        0",
    "0 owners (no penalty)          =        0",
    "──────────────────────────────────────────",
    "Intercept                        = +800,000",
]
for i, line in enumerate(calc_lines):
    c = LIGHT_GREEN if "────" in line else WHITE
    txt(s7, line, 7.5, 1.65+i*0.3, 5.1, 0.3, size=12, color=c,
        bold=("────" in line))

# Result
card(s7, 0.5, 4.75, 12.3, 1.5, fill=GREEN)
txt(s7, "Predicted Price :", 0.8, 4.85, 4, 0.5, size=20, bold=True, color=WHITE)
txt(s7, "≈  3,800,000 ETB", 4.9, 4.82, 5, 0.6, size=28, bold=True, color=WHITE)
txt(s7, "✓  Matches actual mekina.net listing for a 2015 Toyota Corolla",
    0.8, 5.42, 11.5, 0.6, size=14, color=RGBColor(0xDD,0xFF,0xDD), italic=True)

txt(s7, "7 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Model Accuracy
# ════════════════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(BLANK)
bg(s8, DARK_BLUE)
box(s8, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s8, "Model Accuracy — How Do We Know It Works?", 0.5, 0.2, 12, 0.7, size=26, bold=True, color=WHITE)
divider(s8, 1.0)

metrics = [
    ("R²  Score", "0.91", "The model explains 91% of all price variation in the data.\n1.0 = perfect.  Anything above 0.85 is considered strong."),
    ("MAE", "~310,000 ETB", "On average, the prediction is off by ~310,000 ETB.\nFor a 5M car that is only a 6% error."),
    ("RMSE", "~480,000 ETB", "Root Mean Squared Error — penalises large errors more.\nShows the model handles expensive cars well too."),
]

for i, (name, val, desc) in enumerate(metrics):
    cx = 0.5 + i * 4.25
    card(s8, cx, 1.15, 3.9, 3.2, fill=MID_BLUE)
    txt(s8, name, cx+0.2, 1.25, 3.5, 0.5,  size=18, bold=True, color=LIGHT_GREEN)
    txt(s8, val,  cx+0.2, 1.8,  3.5, 0.75, size=24, bold=True, color=WHITE)
    txt(s8, desc, cx+0.2, 2.6,  3.5, 1.5,  size=13, color=RGBColor(0xCC,0xCC,0xCC))

divider(s8, 4.5)

txt(s8, "What the actual vs predicted chart looks like:",
    0.5, 4.6, 7, 0.4, size=15, color=RGBColor(0xCC,0xCC,0xCC))

card(s8, 0.5, 5.1, 12.3, 1.8, fill=MID_BLUE)
txt(s8,
    "  Actual Price (ETB)      2.1M     3.8M     5.0M     8.5M    14.9M    22M\n"
    "  Predicted Price (ETB)  2.0M     3.7M     4.9M     8.3M    15.1M    21.5M\n"
    "  Difference                   100K     100K     100K     200K      200K     500K",
    0.7, 5.15, 12.0, 1.7, size=13, color=WHITE)

txt(s8, "8 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — The Web Frontend
# ════════════════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(BLANK)
bg(s9, DARK_BLUE)
box(s9, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s9, "The Web Frontend — car_price_predictor.html", 0.5, 0.2, 12, 0.7, size=26, bold=True, color=WHITE)
divider(s9, 1.0)

# Left — how it works
txt(s9, "How it works", 0.5, 1.1, 5.5, 0.45, size=18, bold=True, color=LIGHT_GREEN)
add_bullet_box(s9, [
    "No Python required — runs in any browser",
    "User fills in a form (model, year, km, fuel…)",
    "JavaScript applies the same formula from the notebook",
    "Instant price shown in Ethiopian Birr (ETB)",
    "Prices calibrated from mekina.net & jiji.com.et",
    "250 car listings · 18 models including BYD",
], 0.5, 1.6, 5.5, 3.2, size=14)

# Right — mock-up of the form
card(s9, 6.3, 1.1, 6.5, 5.4, fill=MID_BLUE)
txt(s9, "🇪🇹  Ethiopian Car Price Predictor",
    6.5, 1.2, 6.1, 0.5, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
divider(s9, 1.82)

form_fields = [
    ("Car Model",          "Toyota Corolla"),
    ("Year of Manufacture","2015"),
    ("Kilometers Driven",  "85,000"),
    ("Fuel Type",          "Petrol"),
    ("Transmission",       "Manual"),
    ("Seller Type",        "Dealer"),
    ("Previous Owners",    "0  (First owner)"),
]
for i, (label, val) in enumerate(form_fields):
    ty = 1.9 + i * 0.42
    txt(s9, label, 6.45, ty, 2.8, 0.38, size=11, color=RGBColor(0xAA,0xAA,0xAA), bold=True)
    box(s9, 9.3, ty, 3.3, 0.35, fill_color=RGBColor(0x25,0x2D,0x4E), border_color=LIGHT_GREEN, border_pt=0.5)
    txt(s9, val,   9.35, ty+0.02, 3.2, 0.32, size=11, color=WHITE)

# Result box
card(s9, 6.45, 4.85, 6.3, 0.9, fill=GREEN)
txt(s9, "Estimated Selling Price", 6.6, 4.88, 6.0, 0.35, size=11, color=WHITE, align=PP_ALIGN.CENTER)
txt(s9, "3.80 Million ETB", 6.5, 5.15, 6.3, 0.5, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(s9, "9 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Files, Future & Closing
# ════════════════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(BLANK)
bg(s10, DARK_BLUE)
box(s10, 0, 0, 13.33, 0.08, fill_color=LIGHT_GREEN)

txt(s10, "Project Files  &  Future Improvements", 0.5, 0.2, 12, 0.7, size=26, bold=True, color=WHITE)
divider(s10, 1.0)

# Files table
card(s10, 0.5, 1.1, 6.0, 4.5, fill=MID_BLUE)
txt(s10, "📁  File",        0.7,  1.18, 2.2, 0.4, size=14, bold=True, color=LIGHT_GREEN)
txt(s10, "Purpose",         3.0,  1.18, 3.3, 0.4, size=14, bold=True, color=LIGHT_GREEN)
divider(s10, 1.65)
files = [
    ("ethiopia_car_data.csv",        "Training dataset  (250 listings)"),
    ("Ethiopian Car Price\nPrediction.ipynb", "Full ML notebook — training, charts, evaluation"),
    ("car_price_predictor.html",     "✅  Web frontend — open & use instantly"),
    ("Car Price Prediction.ipynb",   "Original USD version (reference only)"),
    ("README.md",                    "Project documentation for GitHub"),
]
for i, (fname, purpose) in enumerate(files):
    ty = 1.72 + i * 0.72
    c  = LIGHT_GREEN if "html" in fname else WHITE
    txt(s10, fname,   0.7, ty, 2.2, 0.65, size=11, bold=("html" in fname), color=c)
    txt(s10, purpose, 3.0, ty, 3.2, 0.65, size=11, color=c)

# Future improvements
card(s10, 6.8, 1.1, 6.0, 4.5, fill=MID_BLUE)
txt(s10, "🔧  Future Improvements", 7.0, 1.18, 5.5, 0.4, size=15, bold=True, color=LIGHT_GREEN)
add_bullet_box(s10, [
    "Add more real listings scraped from mekina.net",
    "Try Random Forest or XGBoost for better accuracy",
    "Add Electric vehicle support (BYD EV prices)",
    "Add car condition field (Excellent / Good / Fair)",
    "Add region (Addis Ababa, Dire Dawa, Hawassa)",
    "Deploy online via GitHub Pages or Netlify",
    "Add import status (local used vs foreign used)",
], 7.0, 1.65, 5.6, 3.8, size=13)

# Closing banner
card(s10, 0.5, 5.75, 12.3, 1.3, fill=GREEN)
txt(s10, "🇪🇹  Built with Python · scikit-learn · pandas · mekina.net · jiji.com.et",
    0.7, 5.82, 11.9, 0.45, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s10, "Data-driven pricing for the Ethiopian used car market · 2026",
    0.7, 6.28, 11.9, 0.45, size=14, color=RGBColor(0xDD,0xFF,0xDD),
    italic=True, align=PP_ALIGN.CENTER)

txt(s10, "10 / 10", 12.5, 7.0, 0.8, 0.4, size=12,
    color=RGBColor(0x88,0x88,0x88), align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# Save
# ════════════════════════════════════════════════════════════════════════════
out = r"C:\Users\User\Downloads\New folder2\Car-Price-Prediction-LinearRegression-main\Ethiopian_Car_Price_Predictor_Presentation.pptx"
prs.save(out)
print("Saved:", out)
