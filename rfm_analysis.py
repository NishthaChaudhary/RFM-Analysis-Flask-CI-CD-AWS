# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import numpy as np
import csv
import datetime as dt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


##Create a file with single score and save bar plots for R,F and M that are displayed in score page

def view_file(file):
    import io
    fff = pd.read_csv(file,delimiter='|')
    ff=fff[fff.transaction_date.str.contains('(\d{1,2})[/](\d{1,2})[/](\d{4})')]
    ff=ff.dropna()
    ff.reset_index(drop=True, inplace=True)
    ff['transaction_date']=pd.to_datetime(ff['transaction_date'],format= '%m/%d/%Y')
    ff['prod_price_net']=ff['prod_price_net'].astype('float64')
    sd=dt.datetime(2020,3,14)
    ff['hist']=sd-ff['transaction_date']
    ff['hist'].astype('timedelta64[D]')
    ff['hist']=ff['hist']/np.timedelta64(1,'D')

    rfm=ff.groupby('cont_id').agg({'hist':lambda x:x.min(), 'cont_id':lambda x:len(x),
                          'prod_price_net':lambda x:x.sum()})

    rfm.rename(columns={'hist':'recency','cont_id':'frequency',
                              'prod_price_net':'monetary value'},inplace=True)

    quintiles = rfm[['recency', 'frequency', 'monetary value']].quantile([.25, .50, .75]).to_dict()

    def r_score(x,l,d):
        if x <= d[l][.25]:
            return 4
        elif x <= d[l][.50]:
            return 3
        elif x <= d[l][.75]:
            return 2
        else:
            return 1

    def fm_score(x,l,d):
        if x <= d[l][.25]:
            return 1
        elif x <= d[l][.50]:
            return 2
        elif x <= d[l][.75]:
            return 3
        else:
            return 4

    rfmS=rfm.copy()
    rfmS['R_Quartile']=rfmS['recency'].apply(r_score,args=('recency',quintiles,))
    rfmS['F_Quartile']=rfmS['frequency'].apply(fm_score,args=('frequency',quintiles,))
    rfmS['M_Quartile']=rfmS['monetary value'].apply(fm_score,args=('monetary value',quintiles,))

    rfmS['RFMClass']=rfmS.R_Quartile.map(str) \
    +rfmS.F_Quartile.map(str) \
    +rfmS.M_Quartile.map(str)

    rfmS['Total Score'] = rfmS['R_Quartile'] + rfmS['F_Quartile'] +rfmS['M_Quartile']
    r1=rfmS.groupby(by='Total Score')['monetary value'].mean()
    r2=rfmS.groupby(by='Total Score')['frequency'].mean()
    r3=rfmS.groupby(by='Total Score')['recency'].mean()
    import matplotlib.pyplot as plt
    #fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14, 5))
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(4, 6))
    r1.plot(ax=axes[0],kind='bar')
    r2.plot(ax=axes[1], kind='bar')
    r3.plot(ax=axes[2], kind='bar')
    plt.savefig('static/z.png');



##Create a file that classicfies customers within segments
def view_segfile(p):
    import io
    ppp = pd.read_csv(p,delimiter='|')
    result=pd.DataFrame
    pp=ppp[ppp.transaction_date.str.contains('(\d{1,2})[/](\d{1,2})[/](\d{4})')]
    pp=pp.dropna()
    pp.reset_index(drop=True, inplace=True)
    pp['transaction_date']=pd.to_datetime(pp['transaction_date'],format= '%m/%d/%Y')
    pp['prod_price_net']=pp['prod_price_net'].astype('float64')
    sd=dt.datetime(2020,3,14)
    pp['hist']=sd-pp['transaction_date']
    pp['hist'].astype('timedelta64[D]')
    pp['hist']=pp['hist']/np.timedelta64(1,'D')

    rfm_table=pp.groupby('cont_id').agg({'hist':lambda x:x.min(), 'cont_id':lambda x:len(x),
                          'prod_price_net':lambda x:x.sum()})

    rfm_table.rename(columns={'hist':'recency','cont_id':'frequency',
                              'prod_price_net':'monetary value'},inplace=True)

    quintiles = rfm_table[['recency', 'frequency', 'monetary value']].quantile([.25, .50, .75]).to_dict()

    def r_score(x,l,d):
        if x <= d[l][.25]:
            return 4
        elif x <= d[l][.50]:
            return 3
        elif x <= d[l][.75]:
            return 2
        else:
            return 1

    def fm_score(x,l,d):
        if x <= d[l][.25]:
            return 1
        elif x <= d[l][.50]:
            return 2
        elif x <= d[l][.75]:
            return 3
        else:
            return 4

    rfmSeg=rfm_table.copy()
    rfmSeg['R_Quartile']=rfmSeg['recency'].apply(r_score,args=('recency',quintiles,))
    rfmSeg['F_Quartile']=rfmSeg['frequency'].apply(fm_score,args=('frequency',quintiles,))
    rfmSeg['M_Quartile']=rfmSeg['monetary value'].apply(fm_score,args=('monetary value',quintiles,))

    rfmSeg['RFMClass']=rfmSeg.R_Quartile.map(str) \
    +rfmSeg.F_Quartile.map(str) \
    +rfmSeg.M_Quartile.map(str)

    rfmSeg['Total Score'] = rfmSeg['R_Quartile'] + rfmSeg['F_Quartile'] +rfmSeg['M_Quartile']
    result=rfmSeg.copy()
    rfmSeg=rfmSeg.reset_index()

    def rfm_level(df):
        if df['Total Score'] >= 9:
            return 'Require Activation'
        elif ((df['Total Score'] >= 8) and (df['Total Score'] < 9)):
            return 'Needs Attention'
        elif ((df['Total Score'] >= 7) and (df['Total Score'] < 8)):
            return 'Promising'
        elif ((df['Total Score'] >= 6) and (df['Total Score'] < 7)):
            return 'Potential'
        elif ((df['Total Score'] >= 5) and (df['Total Score'] < 6)):
            return 'Loyal'
        elif ((df['Total Score'] >= 4) and (df['Total Score'] < 5)):
            return 'Champions'
        else:
            return 'Can\'t Loose Them'

    rfmSeg['Segment'] = rfmSeg.apply(rfm_level, axis=1)
    return rfmSeg

##Plot for "Distribution of R,C,F "
def plot1(p1):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(4,6))
    for i, p in enumerate(['R_Quartile', 'F_Quartile']):
        parameters = {'R_Quartile':'recency', 'F_Quartile':'frequency'}
        y = p1[p].value_counts().sort_index()
        x = y.index
        ax = axes[i]
        bars = ax.bar(x, y, color='pink')
        ax.set_frame_on(True)
        ax.tick_params(left=False, labelleft=False, bottom=False)
        #ax.set_title('Distribution of {}'.format(parameters[p]),
                    #fontsize=14)
        for bar in bars:
            value = bar.get_height()
            if value == y.max():
                bar.set_color('crimson')
            ax.text(bar.get_x() + bar.get_width() / 2,
                    value - 4,
                    '{}\n({}%)'.format(int(value), int(value * 100 / y.sum())),
                   ha='center',
                   va='top',
                   color='k')
    plt.savefig('static/a.png')


def plot2(p2):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(nrows=4, ncols=4,
                             sharex=False, sharey=True,
                             figsize=(9,4))

    r_range = range(1, 5)
    f_range = range(1, 5)
    for r in r_range:
        for f in f_range:
            y = p2[(p2['R_Quartile'] == r) & (p2['F_Quartile'] == f)]['M_Quartile'].value_counts().sort_index()
            x = y.index
            ax = axes[r - 1, f - 1]
            bars = ax.bar(x, y, color='pink')
            if r == 4:
                if f == 2:
                    ax.set_xlabel('{}\nF_Quartile'.format(f), va='top')
                else:
                    ax.set_xlabel('{}\n'.format(f), va='top')
            if f == 1:
                if r == 2:
                    ax.set_ylabel('R_Quartile\n{}'.format(r))
                else:
                    ax.set_ylabel(r)
            ax.set_frame_on(False)
            ax.tick_params(left=False, labelleft=False, bottom=False)
            ax.set_xticks(x)
            ax.set_xticklabels(x, fontsize=8)

            for bar in bars:
                value = bar.get_height()
                if value == y.max():
                    bar.set_color('crimson')
                ax.text(bar.get_x() + bar.get_width() / 2,
                        value,
                        int(value),
                        ha='center',
                        va='bottom',
                        color='k')
    #fig.suptitle('Distribution of M for each F and R',
                 #fontsize=14)
    plt.tight_layout()
    plt.savefig('static/b.png')


def plot_seg(seg_file):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rfm_level_agg = seg_file.groupby('Segment').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary value': ['mean', 'count']
    }).round(1)

    import squarify
    rfm_level_agg.columns = rfm_level_agg.columns.droplevel()
    rfm_level_agg.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
    fig = plt.gcf()
    ax = fig.add_subplot()
    fig.set_size_inches(9,4)
    num= [str(i) for i in rfm_level_agg['Count']]
    perc = [str('{:8.2f}'.format(i/rfm_level_agg['Count'].sum()*100)) + "%" for i in rfm_level_agg['Count']]
    lbl = [el[0] + "[" + el[1] + "]" + ":" +el[2] for el in zip(['Can\'t Loose Them',
                     'Champions',
                     'Loyal',
                     'Needs Attention',
                     'Potential',
                     'Promising',
                     'Require Activation'], num, perc)]
    squarify.plot(sizes=rfm_level_agg['Count'], label=lbl, text_kwargs={'fontsize':7, 'fontname':"Arial Narrow"}, alpha=0.8 )

    #plt.title("RFM Segments",fontsize=18,fontweight="bold")
    plt.axis('off')
    plt.savefig('static/f.png')


# def catplots(seg):
#     # import seaborn as sns
#     # import matplotlib
#     # matplotlib.use('Agg')
#     # import matplotlib.pyplot as plt
#     sns.catplot(x="Segment", y="monetary value", kind="bar", data=seg, aspect=2)
#     plt.savefig('static/gg.png')
#
#     sns.catplot(x="Segment", y="recency", kind="bar", data=seg, aspect=2)
#     plt.savefig('static/hh.png')
#
#     sns.catplot(x="Segment", y="frequency", kind="bar", data=seg, aspect=2)
#     plt.savefig('static/ii.png')
