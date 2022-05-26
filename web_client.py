import traceback

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from etf_gatheror import etf_gatheror

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = html.Div([
    html.H2("ETF数据查询工具"),
    html.Div([
        html.B("请输入etf代码，用英文逗号隔开："),
        dcc.Input(id='etf_codes', type='text', value='000697,001725,001685,000925,000696,001490,005802,001726', style={'width': '50%'}),
        html.Button('即时查询', id='adhoc_query'),
    ]),
    html.Div([
        dcc.Textarea(
            id='textarea_log', readOnly=False,
            style={'width': '100%', 'height': '500px'},
            value='查询中...'
        ),
        dcc.Clipboard(
            target_id="textarea_log",
            title="copy",
            style={
                "position": "absolute",
                "top": 0,
                "right": 20,
                "fontSize": 40,
            }
        )
    ], style={"position": "relative", 'width': '80%'})
])


@app.callback(
    Output('textarea_log', 'value'),
    Input('adhoc_query', 'n_clicks'),
    State('etf_codes', 'value')
)
def get_info_by_buttons(n_clicks1, etf_codes):
    etf_codes = etf_codes.split(',')

    try:
        result = etf_gatheror(etf_codes)
        result = map(lambda x: "\t".join(x), result)
        result = "\n".join(result)
    except:
        result = "出问题了，请联系开发人员（多半是etf代码输错了，比如多了空格或是用了中文逗号之类的），出错信息如下：\n\n" + traceback.format_exc()
    return result


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=1126, debug=False)
