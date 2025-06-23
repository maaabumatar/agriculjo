from flask import Flask, render_template
import pandas as pd
import os

data_years = os.listdir('data')
data_years = [int(file.replace('.csv','')) for file in data_years]
data_years.sort(reverse=True)

def get_crop_data() -> list:
    files = [f'data/{file}.csv' for file in data_years]
    files = ['data/' + str(data_years[0] + i) + '.csv' for i in range(len(data_years))]
    files = [f'data/{file}.csv' for file in data_years]
    data = []
    for file in files:
        df = pd.read_csv(file)
        df['Crop'] = df['Crop'].str.replace('-','')
        for c in df.columns:
            if c == 'Crop':
                continue
            try:
                df[c] = df[c].str.replace(',','')
                df[c] = df[c].astype(float)
            except:
                pass
        df['Total Area'] = df['Winter Area'] + df['Summer Area']
        df['Total Production'] = df['Winter Production'] + df['Summer Production']
        df['Total Average Yield'] = df['Total Area'] / df['Total Production']
        data.append({int(file[5:-4]): df.copy()})
    return data

def create_chart(chart_title: str, series: list[dict], categories: list[str], chart_type = 'column') -> dict:
    chart = {'type': chart_type,
             'title': chart_title,
             'series': series,
             'categories': categories}
    return chart

def create_production_charts() -> tuple[list, list]:
    data = get_crop_data()
    charts = []
    for i, year in enumerate(data_years):
        df = data[i][year]
        series = []
        for name in ['Total Production', 'Winter Production', 'Summer Production']:
            s = {'name': name, 'data': list(df[name])}
            series.append(s)
        categories = list(df['Crop'])
        chart = create_chart(chart_title=f'% Production (Metered Tonne) per Crop type ({year})', series=series, categories=categories)
        charts.append(chart)
    return charts

def create_area_charts() -> tuple[list, list]:
    data = get_crop_data()
    charts = []
    for i, year in enumerate(data_years):
        df = data[i][year]
        series = []
        for name in ['Total Area', 'Winter Area', 'Summer Area']:
            s = {'name': name, 'data': list(df[name])}
            series.append(s)
        categories = list(df['Crop'])
        chart = create_chart(chart_title=f'% Planted Area (Dunum) per Crop type ({year})', series=series, categories=categories)
        charts.append(chart)
    return charts

def create_annual_area_chart() -> dict:
    data = get_crop_data()
    df = pd.DataFrame()
    df['Crop'] = []
    for i, year in enumerate(data_years):
        df = pd.merge(df, data[i][year]['Crop'], how='outer')
    
    crops = list(df['Crop'])
    series = []
    for crop in crops:
        areas = []
        for i, year in enumerate(data_years):
            df = data[i][year]
            area = float(df.loc[df['Crop'] == crop, 'Total Area'].iloc[0])
            areas.append(area)
        s = {'name': crop, 'data': areas}
        series.append(s)
    categories = data_years
    chart = create_chart(chart_title=f'Planted Area (Dunum) per year', series=series, categories=categories, chart_type='area')
    return chart

def create_annual_production_chart() -> dict:
    data = get_crop_data()
    df = pd.DataFrame()
    df['Crop'] = []
    for i, year in enumerate(data_years):
        df = pd.merge(df, data[i][year]['Crop'], how='outer')
    
    crops = list(df['Crop'])
    series = []
    for crop in crops:
        productions = []
        for i, year in enumerate(data_years):
            df = data[i][year]
            production = float(df.loc[df['Crop'] == crop, 'Total Production'].iloc[0])
            productions.append(production)
        s = {'name': crop, 'data': productions}
        series.append(s)
    categories = data_years
    chart = create_chart(chart_title=f'Production (Metered Tonne) per year', series=series, categories=categories, chart_type='area')
    return chart

app = Flask(__name__)

@app.route('/')
def home():
    charts: list
    charts = create_production_charts()
    chart = create_annual_production_chart()
    charts.append(chart)
    chart = create_annual_area_chart()
    charts.append(chart)
    charts2 = create_area_charts()
    for chart in charts2:
        charts.append(chart)
    return render_template('index.html', charts=charts, charts_length=len(charts))

app.run()