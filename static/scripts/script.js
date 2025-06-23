for (let i = 0; i < charts.length; i++) {
  Highcharts.chart("chart" + i, {
    chart: { type: charts[i]["type"] },
    title: { text: charts[i]["title"] },
    series: charts[i]["series"],
    plotOptions: {
      column: { stacking: "percent" },
    },
    xAxis: { categories: charts[i]["categories"] },
    yAxis: { title: "" },
  });
}
