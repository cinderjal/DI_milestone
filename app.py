import pandas as pd
import numpy as np
import Quandl
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh import embed
from bokeh.embed import components 
from datetime import datetime,timedelta

from flask import Flask, render_template, request, redirect



app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
        
def make_plot():
    ticker = request.form['ticker']
    options = request.form.getlist('options')
    
    print ticker
        
    ticker_options = pd.read_csv('static/WIKI_tickers.csv')
    ticker_dict=ticker_options.set_index(ticker_options.columns[0])[ticker_options.columns[1]].to_dict()

    quandl_ticker='WIKI/'+ticker.upper()

    if quandl_ticker in ticker_dict:
        title = ticker.upper()+': '+ticker_dict[quandl_ticker]  
        
        today = datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')

        data = Quandl.get(quandl_ticker, trim_start=start_date, trim_end=end_date,authtoken='5CuPA7VjjoTFsLezZMzr')
    
        p = figure(title=title, x_axis_label="Date", y_axis_label="Price USD", x_axis_type = "datetime")

        if 'Open' in options:
            p.line(data.index, data['Open'], color='blue', legend='Open')
        if 'High' in options:
            p.line(data.index, data['High'], color='red', legend='High')
        if 'Low' in options:
            p.line(data.index, data['Low'], color='black', legend='Low')
        if 'Close' in options:
            p.line(data.index, data['Close'], color='green', legend='Close')
        return p
    else:
        p = 0
        return p
    
@app.route('/plot_ticker', methods=['GET', 'POST'])
def show_plot():
    p=make_plot()
    if p == 0:
        return render_template('error.html')
    else:
        script, div = embed.components(p)
        return render_template('plot.html', script=script, div=div)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
