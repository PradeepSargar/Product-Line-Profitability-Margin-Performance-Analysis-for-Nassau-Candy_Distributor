# Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis

An executive decision support and business intelligence platform built to analyze product line profitability, margin dispersion, revenue concentration, and cost exposure for Nassau Candy Distributor.

---

## 🌟 Executive Summary & Key Business Findings

- **Overall Portfolio Health:** Total Sales of **$141,783.63**, generating **$93,442.80** in Gross Profit with a robust **65.91%** Gross Margin across **10,194** transactions.
- **Profit Concentration (Pareto):** Extreme profitability concentration — the **top 5 products account for 95.06% of Gross Profit** and **92.88% of Revenue**.
- **Division Dominance:** The **Chocolate** division represents **95.06%** of total gross profit, while Other (4.64%) and Sugar (0.30%) represent secondary volume.
- **Geographic Margin Stability:** Gross margins show remarkable uniformity across all 4 sales regions, spanning a narrow band of only **0.96 percentage points** (Interior: 66.43% vs Atlantic: 65.47%).
- **Margin Risk Screening:** **7 of 15 products** meet portfolio-relative margin compression criteria (Gross Margin < median 62.31% and Cost-to-Sales > median 37.69%), warranting pricing and vendor procurement audits.

---

## 📐 Project Architecture

```
Product Line Profitability & Margin Performance Analysis/
│
├── data/
│   └── raw/
│       └── Nassau Candy Distributor.csv      # Source CSV dataset (10,194 records, 18 columns)
│
├── src/                                      # Reusable analytical backend & UI modules
│   ├── data/
│   │   ├── loader.py                         # Data loading, date parsing, and schema validation
│   │   └── cleaning.py                       # Data cleaning & feature engineering pipeline
│   │
│   ├── analysis/
│   │   ├── profitability.py                  # Portfolio KPIs, product profitability & time trends
│   │   ├── product_analysis.py               # SKU rankings, top-N drivers & contribution metrics
│   │   ├── pareto.py                         # 80/20 cumulative revenue & profit concentration
│   │   ├── division_analysis.py              # Business unit aggregation & margin spreads
│   │   ├── regional_analysis.py              # Regional performance & geographic stability
│   │   ├── segmentation.py                   # 2×2 Strategic matrix (Core, Volume, Niche, Underperformer)
│   │   └── risk_analysis.py                  # Margin compression & risk screening diagnostics
│   │
│   ├── visualization/
│   │   └── charts.py                         # Reusable Plotly chart builders with corporate theme
│   │
│   └── ui/
│       ├── styles.py                         # Custom executive-grade CSS styling & status badges
│       ├── kpi_cards.py                      # Executive metric cards & grid layout
│       ├── tables.py                         # Formatted, sortable interactive dataframes
│       ├── filters.py                        # Sidebar controls, active filter indicator & Data Quality audit
│       └── insights.py                       # Dynamic, evidence-based business findings & implications
│
├── tests/
│   └── test_dashboard_integration.py         # Automated integration and reconciliation test suite
│
├── app.py                                    # Streamlit entrypoint
├── requirements.txt                          # Dependencies (streamlit, plotly, pandas, numpy)
└── README.md
```

---

## 🖥️ Streamlit Dashboard Sections

1. **Executive Overview:**
   - 8 dynamic KPI metric cards (Revenue, Gross Profit, Gross Margin %, Units, Products, Divisions, Top 5 Profit Share, Margin Risk Flags).
   - High-level executive charts: Top SKUs by Gross Profit, Revenue vs Profit Share, Profit Pareto curve, and Monthly Trend.
   - Dynamic business findings and strategic implications panel.

2. **Product Profitability & Pareto Analysis:**
   - Interactive, sortable Product Leaderboard with currency and percentage formatting.
   - Horizontal bar charts for Gross Profit and Gross Margin % (with portfolio average reference line).
   - Revenue vs Profit Contribution disparity scatter plot.
   - Revenue Pareto & Profit Pareto charts with 80% threshold markers and concentration metrics.

3. **Division & Regional Performance:**
   - Division breakdown tables and side-by-side revenue/profit/margin charts.
   - Regional breakdown and geographic stability analysis highlighting the tight 0.96 pp margin spread.
   - Transaction-level Gross Margin % box plots across divisions and territories.

4. **Strategic Matrix & Segmentation:**
   - 2×2 Strategic Product Matrix (Gross Margin % vs Gross Profit with median crosshair thresholds and bubble sizes representing revenue).
   - Segment summaries across **Core Drivers**, **Volume Drivers**, **Niche Gems**, and **Underperformers**.

5. **Risk Screening & Diagnostics:**
   - Portfolio-relative screening diagnostics for low-margin / high-cost products.
   - Flagged product investigation table.
   - Cost vs Sales scatter diagnostics with break-even parity reference line.
   - Longitudinal time trends (Monthly Sales, GP, Margin %; Yearly comparison).
   - Methodological note detailing the documented Order Date vs Ship Date anomaly.

---

## ⚙️ Quickstart & Execution

### 1. Environment Setup
```bash
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

### 3. Run Automated Validation & Reconciliation Tests
```bash
python -m unittest tests/test_dashboard_integration.py
```

---

## 🛡️ Analytical Controls & Reconciliation Standards

| Control Dimension | Validated Benchmark | Reconciled App Output | Status |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | \$141,783.63 | \$141,783.63 | PASS |
| **Total Gross Profit** | \$93,442.80 | \$93,442.80 | PASS |
| **Total Cost** | \$48,340.83 | \$48,340.83 | PASS |
| **Gross Margin %** | 65.91% | 65.91% | PASS |
| **Total Transactions** | 10,194 | 10,194 | PASS |
| **Unique Products** | 15 | 15 | PASS |
| **Operating Divisions** | 3 | 3 | PASS |
| **Sales Regions** | 4 | 4 | PASS |
| **Top 5 Profit Contribution** | 95.06% | 95.06% | PASS |
| **Top 5 Revenue Contribution** | 92.88% | 92.88% | PASS |
| **Margin Risk Flagged SKUs** | 7 of 15 | 7 of 15 | PASS |
| **Regional Margin Spread** | 0.96 pp | 0.96 pp | PASS |
