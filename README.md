# 🌿 Agriculjo — Jordan’s Agricultural Production Visualizer

**Agriculjo** is a full-stack Flask web app that transforms raw agricultural production data from Jordan’s Department of Statistics (DoS) into clean, interactive dashboards. It automates the process from spreadsheet to browser, using Pandas and Highcharts to turn reports into insights.

## 🧾 Data Preparation

- Crop production data (up to 2023) is extracted from official DoS spreadsheets.
- Standardized using custom Google Sheets macros.
- Exported as `.csv` files into the `/data` directory.

## ⚙️ Backend Processing

- Flask app reads, cleans, and reshapes data using Pandas.
- Modular functions generate Highcharts-compatible chart dictionaries.
- Charts are passed to the frontend via `render_template()` and embedded with Jinja2.

## 📊 Frontend Visualization

- Highcharts renders production trends across 27 crop types by year and season.
- JavaScript dynamically builds the charts from Python-passed configs.
- Styles and scripts are handled in `/static/css/styles.css` and `/static/scripts/script.js`.

## 📈 Predictive Insight Included

- A Scikit-learn linear regression model forecasts **total production for 2023**.
- It learns from historical `Winter Area` and `Summer Area` features.
- The prediction appears alongside historical data in a dedicated chart.

## 🗂 Project Structure

```
agriculjo/
├── data/                   # CSVs per year
├── static/
│   ├── css/
│   │   └── styles.css
│   └── scripts/
│       └── script.js
├── templates/
│   └── index.html
├── app.py
└── README.md
```

## 🚀 Live Demo

🔗 https://agriculjo.onrender.com  
_Note: may take a minute to load if inactive._

## 📁 Source Code

GitHub: [maaabumatar/agriculjo](https://github.com/maaabumatar/agriculjo)
