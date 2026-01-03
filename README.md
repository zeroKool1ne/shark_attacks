# Shark Attacks Data Analysis

A comprehensive data science project analyzing global shark attack patterns using the GSAF dataset. Built with modular, production-ready code and professional Jupyter notebooks.

**Program:** Ironhack Data Science Bootcamp - Week 7
**Author:** dv
**Date:** January 2026

---

## 📋 Project Overview

This project analyzes historical shark attack data to uncover patterns and insights about when, where, and under what circumstances shark attacks occur. Through rigorous data cleaning, exploratory analysis, and hypothesis testing, we provide actionable insights for risk assessment and business strategy.

### Research Hypotheses

**H1: Geographic Hotspots**
Shark attacks are concentrated in specific regions, with USA, Australia, and South Africa accounting for >60% of all attacks.

**H2: Activity-Based Risk**
Surfing and swimming combined account for >30% of documented attacks.

**H3: Gender Disparity**
Males are attacked significantly more often than females (~7:1 ratio).

**H4: Temporal Trends**
Documented shark attacks have increased significantly over recent decades.

### Business Case: SafeSurf Analytics

**Goal:** Optimize surf shop locations through data-driven risk assessment.

**Objectives:**
- Identify safe locations with high surfing activity but low shark attack risk
- Perform risk analysis for potential new shop locations
- Provide data-driven safety guidelines for customers
- Optimize insurance costs through geographic risk profiling

---

## 🗂️ Project Structure

```
shark_attacks/
├── data/
│   ├── shark_attacks.csv          # Raw dataset (GSAF)
│   └── shark_attacks_cleaned.csv  # Cleaned dataset
├── notebooks/
│   ├── 01_eda.ipynb               # Exploratory Data Analysis
│   ├── 02_hypothesis_testing.ipynb # Statistical hypothesis testing
│   └── 03_conclusions.ipynb       # Business insights & recommendations
├── reports/
│   ├── h1_geographic.png          # Geographic distribution plot
│   ├── h2_activities.png          # Activity analysis plot
│   ├── h3_gender.png              # Gender analysis plot
│   ├── h4_temporal.png            # Temporal trends plot
│   ├── species.png                # Species distribution plot
│   ├── age_distribution.png       # Age demographics plot
│   ├── fatality.png               # Fatality analysis plot
│   └── risk_score.png             # Risk score visualization
├── src/
│   ├── __init__.py                # Package initialization
│   ├── cleaning.py                # DataCleaner class (OOP design)
│   ├── analysis.py                # Analysis functions
│   └── visualization.py           # Plotting functions
├── PRESENTATION.md                 # Presentation outline
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
└── .gitignore
```

---

## 🛠️ Technologies & Tools

**Core Stack:**
- Python 3.11+
- pandas - Data manipulation
- numpy - Numerical computing
- matplotlib - Visualization
- seaborn - Statistical plots
- Jupyter - Interactive notebooks

**Design Patterns:**
- Object-Oriented Programming (DataCleaner class)
- Modular function design
- Method chaining
- Clean code principles

---

## 📊 Dataset

**Source:** Global Shark Attack File (GSAF)
**Size:** ~7,000 incidents
**Timespan:** 1500s - 2025
**Original columns:** 257
**Cleaned columns:** 21

**Key Fields:**
- Geographic: Country, State, Location
- Temporal: Date, Year
- Demographic: Sex, Age, Name
- Incident: Activity, Type, Fatal Y/N, Species
- Details: Injury description, Time, Source

---

## 🧹 Data Cleaning Pipeline

### DataCleaner Class (OOP Design)

Professional class-based cleaning pipeline with method chaining:

```python
from src import DataCleaner

cleaner = DataCleaner(df, verbose=True)
df_clean = cleaner.clean_all()
```

### Cleaning Techniques Applied

1. **Empty Column Removal**
   - Removed 236 columns (92% of original)
   - Dropped unnamed columns with >95% missing data

2. **Duplicate Detection**
   - Scanned for duplicate rows
   - 0 duplicates found (data integrity confirmed)

3. **String Standardization**
   - Country: 210 unique values (e.g., "USA", "US" → "USA")
   - Activity: 1,547 unique values (Title case)
   - Species: 1,629 unique values (standardized names)

4. **Categorical Formatting**
   - Sex: 10 variants → 2 (M, F) + NaN
   - Fatal Y/N: 12 variants → 2 (Y, N) + NaN
   - Type: Removed invalid entries

5. **Date Parsing with Regex**
   - Extracted dates from formats like "27th November 2025"
   - Created Date_Parsed column

6. **Age Extraction**
   - Parsed 4,041 ages from mixed formats
   - Handled: "25", "teen" → 15, "20s" → 20
   - Validated range: 0-120 years

7. **Missing Value Handling**
   - Threshold-based approach (70%)
   - Preserved valuable information

**All cleaning functions are silent by default** (no print statements unless `verbose=True`)

---

## 📈 Key Findings

### Hypothesis Validation Results

✅ **H1: Geographic Hotspots - VALIDATED**
- USA, Australia, South Africa: **66.4%** of all attacks
- USA: 2,575 | Australia: 1,514 | South Africa: 599

✅ **H2: Activity-Based Risk - VALIDATED**
- Surfing + Swimming: **36.5%** of all attacks
- Surfing: 1,146 | Swimming: 1,057

✅ **H3: Gender Disparity - VALIDATED**
- Male:Female ratio: **7.0:1** (5,666 males vs 808 females)
- Male victims: 87.5% of total

✅ **H4: Temporal Trends - VALIDATED**
- **257% increase** comparing early (1900-1940s) to recent decades (1970-2020s)
- Driven by: improved reporting, coastal population growth, water sports participation

### Additional Insights

📊 **Demographics:**
- Most common age: 24 years (median)
- Peak risk group: Males aged 15-30

🦈 **Species:**
- Top 3: White Shark (201), Tiger Shark (90), Bull Shark (78)
- Many incidents have unconfirmed species

⚠️ **Outcomes:**
- Overall fatality rate: **23.2%**
- Most attacks (77%) are survivable
- Medical response time is critical

🌍 **Geographic Risk:**
- Australia/South Africa: Higher fatality rates (~20%)
- USA: Lower fatality rate (~8%) - better emergency response

### Business Recommendations

**SafeSurf Analytics - Location Strategy:**

1. **Low Risk Markets (Risk Score <30):**
   - New Zealand
   - Brazil
   - Recommended for expansion

2. **Medium Risk Markets (30-50):**
   - Australia (high volume, moderate fatality)
   - Viable with proper insurance

3. **High Risk Markets (>50):**
   - USA (very high volume)
   - Reunion Island (very high fatality)
   - Require premium positioning

4. **Strategic Insights:**
   - Target young adult males (15-30) for marketing
   - Develop surfing-specific safety products
   - Use regional data for insurance pricing

---

## 🚀 Installation & Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Cleaning Pipeline

```python
from src import clean_data

# Clean data (silent mode)
df = clean_data('data/shark_attacks.csv', save_cleaned=True, verbose=False)
```

### 3. Run Analysis

```python
from src import analyze_geographic_hotspots, plot_top_countries

# Analyze
results = analyze_geographic_hotspots(df)

# Visualize
plot_top_countries(results['top_countries'], results['top3_percentage'])
```

### 4. Explore Notebooks

```bash
jupyter notebook notebooks/
```

**Notebook Workflow:**
1. `01_eda.ipynb` - Exploratory Data Analysis
2. `02_hypothesis_testing.ipynb` - Statistical validation
3. `03_conclusions.ipynb` - Business insights

---

## 📊 Visualizations

All notebooks include professional visualizations:

- Geographic distribution (bar charts)
- Activity-based risk analysis
- Gender distribution & fatality comparison
- Temporal trends (decade & yearly)
- Species involvement
- Age distribution (histogram & box plot)
- Fatality analysis by country
- Risk score assessment (color-coded)

All plots are saved to `reports/` directory as high-resolution PNGs (300 DPI).

---

## 💻 Code Features

### Modular Architecture

**src/cleaning.py** - `DataCleaner` class
```python
class DataCleaner:
    """Professional OOP cleaning pipeline with method chaining."""
    def clean_all(self) -> pd.DataFrame
    def get_cleaning_report(self) -> dict
```

**src/analysis.py** - Analysis functions
```python
analyze_geographic_hotspots(df) -> dict
analyze_activity_risk(df) -> dict
calculate_surf_risk_score(df) -> pd.DataFrame
```

**src/visualization.py** - Plotting functions
```python
plot_top_countries(data, save_path=None)
plot_temporal_trends(data, save_path=None)
set_plot_style()  # Consistent styling
```

### Clean Code Principles

✅ No print statements (unless verbose mode)
✅ Comprehensive docstrings
✅ Type hints where applicable
✅ Method chaining support
✅ Modular, reusable functions
✅ Professional naming conventions

---

## 📚 Project Timeline

**Ironhack Week 7 - Weekend Sprint**

**Day 1-2:** Data exploration & hypothesis formulation
**Day 3:** Data cleaning implementation
**Day 4:** EDA & visualization
**Day 5:** Hypothesis testing & validation
**Day 6:** Business insights & presentation prep

---

## 🎓 Learning Outcomes

**Technical Skills:**
- Advanced pandas operations
- Object-oriented programming in data science
- Regex for text parsing
- Statistical hypothesis testing
- Professional visualization with matplotlib/seaborn

**Data Science Workflow:**
- EDA best practices
- Hypothesis-driven analysis
- Business insight generation
- Clean code architecture

**Soft Skills:**
- Presenting technical findings
- Business storytelling with data
- Professional documentation

---

## 📝 License

This project is part of the Ironhack Data Science Bootcamp curriculum.

---

## 🙏 Acknowledgments

- **Dataset:** Global Shark Attack File (GSAF)
- **Program:** Ironhack Data Science Bootcamp
- **Mentors:** Ironhack instructors and community

---

## 📧 Contact

**Author:** dv
**Program:** Ironhack Data Science Bootcamp
**Project Week:** Week 7 - Data Cleaning & EDA

---

**⭐ If you found this project helpful, please star the repository!**
