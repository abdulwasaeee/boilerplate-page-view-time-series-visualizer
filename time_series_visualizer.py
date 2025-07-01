import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import numpy as np
np.float = float  # Monkey-patch for deprecated alias


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"]=pd.to_datetime(df["date"])
df.set_index("date",inplace=True)


# Clean data
df = df[(df["value"]>=df["value"].quantile(0.025)) & (df["value"]<=df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    fig,ax=plt.subplots(figsize=(15,5))

    ax.plot(df.index,df["value"],color="red",linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    df_grouped['month'] = pd.Categorical(df_grouped['month'], categories=month_order, ordered=True)
    # Draw bar plot
    fig=plt.figure(figsize=(15,5))

    sns.barplot(data=df_grouped, x='year', y='value', hue='month', hue_order=month_order, palette='tab10')

    # Customize the plot
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.title('')
    plt.legend(title='Months')


    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month

    # Sort by month number to keep month order consistent
    df_box = df_box.sort_values('month_num')

    # Draw box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    # Left: Year-wise Box Plot (Trend)
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Right: Month-wise Box Plot (Seasonality)
    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
