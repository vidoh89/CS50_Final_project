import plotly.express as px

fig= px.line(x=["a","b","c"], y=[1,3,2],title='sample figure')
output_file = 'gdp_and_growth_rate_graph_practice.html'
fig.write_html(output_file, auto_open=True)

fig.show()