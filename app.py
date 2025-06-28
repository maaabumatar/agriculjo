from flask import Flask, render_template
from sklearn.linear_model import LinearRegression
import pandas as pd
import os

class Data:
    def __init__(self, data: list[dict]) -> None:
        self.years = []
        for item in data:
            for year, df in item.items():
                self.__dict__.update({f'_{year}': df})
                self.years.append(year)

class Chart:
    def __init__(self, title: str) -> None:
        self.title = title
    
    def set_categories(self, categories: list[str]) -> None:
        self.categories = categories
    
    def set_series(self, series: list[dict]) -> None:
        self.series = series

    def get_chart(self) -> dict:
        return self.__dict__

class column(Chart):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self.type = 'column'

class area(Chart):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self.type = 'area'

class line(Chart):
    def __init__(self, title):
        super().__init__(title)
        self.type = 'line'

def list_files() -> list[str]:
    files = os.listdir('data')
    return files

def cleanse_df(df: pd.DataFrame) -> pd.DataFrame:
    df['Crop'] = df['Crop'].str.replace('-','')
    for c in df.columns:
            if c == 'Crop':
                continue
            try:
                df[c] = df[c].str.replace(',','')
                df[c] = df[c].astype(float)
            except Exception as e:
                pass
    return df

def add_totals(df: pd.DataFrame) -> pd.DataFrame:
    df['Total Area'] = df['Winter Area'] + df['Summer Area']
    df['Total Production'] = df['Winter Production'] + df['Summer Production']
    df['Total Average Yield'] = df['Total Area'] / df['Total Production']
    return df

def prepare_dataframes(files: list[str]) -> Data:
    data = []
    for file in files:
        file = f'data/{file}'
        df = pd.read_csv(file)
        df = cleanse_df(df)
        df = add_totals(df)
        file = file.replace('data/', '')
        file = file.replace('.csv', '')
        data.append({int(file): df})
    data = Data(data)
    return data

def create_column_series(dataframe: pd.DataFrame, series_list: list[dict]) -> list[dict]:
    series: list[dict] = []
    for _ in series_list:
        name = _['name']
        data = _['data']
        data = list(dataframe[data])
        s = {'name': name, 'data': data}
        series.append(s)
    return series

def create_row_series(dataframes: pd.DataFrame, series_list: list[dict]) -> list[dict]:
    series: list[dict] = []
    for _ in series_list:
        name: str = _['name']
        data: list[float] = []
        for df in dataframes:
            total = df.loc[df['Crop'] == name, _['data']].iloc[0]
            total = float(total)
            data.append(total)
        s = {'name': name, 'data': data}
        series.append(s)
    return series

def create_column_charts(data: Data) -> list[dict]:
    charts =[]
    for year in data.years:
        df = data.__dict__[f'_{year}']
        column_chart = column(f'% Production of Crops in {year}')
        column_chart.categories = list(df['Crop'])
        series_list = [{'name': 'Winter Production', 'data': 'Winter Production'},
                       {'name': 'Summer Production', 'data': 'Summer Production'}]
        series = create_column_series(df, series_list)
        column_chart.series = series
        charts.append(column_chart.get_chart())
    return charts

def create_area_chart(data: Data, title: str, values: str) -> dict:
    dataframes = [data.__dict__[f'_{year}'] for year in data.years]
    area_chart = area(title)
    area_chart.categories = data.years
    series_list = [{'name': crop, 'data': values} for crop in list(dataframes[0]['Crop'])]
    series = create_row_series(dataframes, series_list)
    area_chart.series = series
    chart = area_chart.get_chart()
    return chart

def create_line_chart(df: pd.DataFrame, title: str) -> dict:
    chart = line(title)
    lines = ['Total Production', 'Winter Area', 'Summer Area']
    series = [{'name': li, 'data': list(df[li])} for li in lines]
    chart.series = series
    chart.categories = lines
    chart = chart.get_chart()
    return chart

def create_prediction_charts(df: pd.DataFrame, title: str) -> list[dict]:
    column_chart = line(title)
    column_chart.categories = list(df['Crop'])
    series_list = [{'name': 'Total Production (predicted)', 'data': 'Total Production (predicted)'},
                   {'name': 'Total Production', 'data': 'Total Production'},
                   {'name': 'Difference', 'data': 'Difference'}]
    series = create_column_series(df, series_list)
    column_chart.series = series
    return column_chart.get_chart()

def learn(data: Data):
    model = LinearRegression()
    for year in data.years:
        if year == 2023:
            continue
        try:
            df = pd.concat(df, data.__dict__[f'_{year}'], ignore_index=True)
        except:
            df = data.__dict__[f'_{year}']
    df = df[['Total Production', 'Winter Area', 'Summer Area']]
    X = df[['Winter Area', 'Summer Area']]
    y = df['Total Production']
    model.fit(X, y)
    df_2023 = data._2023[['Winter Area', 'Summer Area']]
    predicted_array = model.predict(df_2023)
    return predicted_array

def main() -> list[dict]:
    files = list_files()
    data = prepare_dataframes(files=files)
    
    column_charts = create_column_charts(data)
    column_charts = column_charts[-1::-1]
    charts = column_charts
    
    area_production_chart = create_area_chart(data=data, title='Production of Crops throughout the years', values='Total Production')
    charts.append(area_production_chart)

    area_planted_chart = create_area_chart(data=data, title='Planted area of Crops throughout the years', values='Total Area')
    charts.append(area_planted_chart)

    predicted_data = learn(data)
    df_2023 = data._2023
    df_2023['Total Production (predicted)'] = predicted_data
    df_2023['Difference'] = abs(df_2023['Total Production (predicted)'] - df_2023['Total Production'])
    df_2023 = df_2023[['Crop', 'Difference', 'Total Production (predicted)', 'Total Production']]
    prediction_chart = create_prediction_charts(df_2023, title='Predicted production for 2023')
    charts.append(prediction_chart)

    return charts

app = Flask(__name__)

@app.route('/')
def home():    
    charts = main()
    return render_template('index.html', charts=charts, charts_length=len(charts))

if __name__ == '__main__':
    app.run()