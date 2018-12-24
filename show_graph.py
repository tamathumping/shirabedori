import pandas as pd
import json
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import  DatetimeTickFormatter
from bokeh.embed import components
from bokeh.layouts import row

def data_to_graph(status_list: dict):
    """
    retweet_searchで取得したツイートデータをpandasで時間ごとにカウント。
    vokehでグラフ化。
    :param status_list:twythonで取得したリツイートの辞書。
    :return:vokeh出力用のjson
    """
    #pandasで処理するためjson.dump
    data = json.dumps(status_list)
    df = pd.read_json(data)
    #datetimeオブジェクトをindexにして、1時間ごとのリツイート数をカウント
    df.set_index('created_at', inplace=True)
    dd = df.resample('1H').count()

    #dataframeからbokehのデータソースに変換。
    source = ColumnDataSource(dd)
    p = figure(height=400, x_axis_type="datetime", title='Number of tweets', x_axis_label='Date', y_axis_label='Retweet')
    # HoverToolを追加。
    p.add_tools(HoverTool(
        tooltips=[
            ("date", "@created_at{%m/%d/%H:%M}"),
            ("count", "@{id}")
        ],
        formatters={'created_at': 'datetime'},
        mode='vline'
    ))

    p.line(x="created_at", y="id", alpha=0.5, color="red", line_width=3, line_join="round", source=source)
    #グラフの日時表示設定
    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%m/%d'], hours=['%H:%M'])
    p.background_fill_color = "#f2f7ff"
    p.background_fill_alpha = 0.5
    #responsiveでグラフのwidth表示
    p = row(p, sizing_mode="scale_width")
    script, div = components(p)

    return script, div