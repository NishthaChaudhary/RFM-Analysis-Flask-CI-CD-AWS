from flask import Flask, send_file, render_template, request,make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
application = Flask(__name__)
import pandas as pd
import os
import csv
import tablib
from io import StringIO
from werkzeug.wrappers import Response
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from rfm_analysis import view_segfile
from rfm_analysis import view_file
from rfm_analysis import plot1
from rfm_analysis import plot2
from rfm_analysis import plot_seg
#from rfm_analysis import catplots

@application.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@application.route('/data', methods=['GET','POST'])

def data():
    if request.method=='POST':
        f1=request.form['csvfile']
        d1=view_segfile(f1)
        return render_template('data.html', data=d1.to_html(header=True, index=True))

@application.route('/download')
def download_file():
    v='rfm_report.csv'
    return send_file(v,as_attachment=True)


@application.route('/score', methods=['GET','POST'])
def show_score():
    if request.method=='POST':
        f2=request.form['csvfile']
        d2=view_segfile(f2)
        view_file(f2)
        plot1(d2)
        plot2(d2)
        return render_template("score.html")

@application.route('/segments', methods=['GET','POST'])
def show_segments():
    if request.method=='POST':
        f3=request.form['csvfile']
        d3=view_segfile(f3)
        plot_seg(d3)
        sns.catplot(x="Segment", y="monetary value", kind="bar", data=d3, aspect=2)
        plt.savefig('static/gg.png')
        plt.close()
        sns.catplot(x="Segment", y="recency", kind="bar", data=d3, aspect=2)
        plt.savefig('static/hh.png')
        plt.close()
        sns.catplot(x="Segment", y="frequency", kind="bar", data=d3, aspect=2)
        plt.savefig('static/ii.png')
        plt.close()
        return render_template("segments.html")

if __name__ == "__main__":
    application.run()
