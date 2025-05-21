# =========================================================================== #
# --- SEMINAR WORK (app.py) ------------------------------------------------- #
#     title:   Neuralink Compression Challenge: Web-based Interactive         #
#              Visualization of N1 Implant Signals and Inter-Channel          #
#              Correlations in Python                                         #
#     author:  Martin KUKRÁL                                                  #
#     subject: KIV/VI                                                         #
#     year:    2024/2025                                                      #
# =========================================================================== #
# ----------------- #
# Python   3.11.4   #
# ----------------- #
# dash     3.0.3    #
# numpy    1.25.2   #
# plotly   5.22.0   #
# ----------------- #
import numpy as np
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
from plotly.subplots import make_subplots




# === LOAD EVERYTHING PREPROCESSED ============================================
# load signals:
signals_data = np.load("data/signals.npy")                 # signals themselves
num_total_channels, num_total_samples = signals_data.shape # info about them

# load reorderings:
orderP_single = np.load("data/order_P_single.npy")     # Pearson + "single"
orderP_average = np.load("data/order_P_average.npy")   # Pearson + "average"
orderP_centroid = np.load("data/order_P_centroid.npy") # Pearson + "centroid"
orderP_ward = np.load("data/order_P_ward.npy")         # Pearson + "ward"
orderS_single = np.load("data/order_S_single.npy")     # Spearman + "single"
orderS_average = np.load("data/order_S_average.npy")   # Spearman + "average"
orderS_centroid = np.load("data/order_S_centroid.npy") # Spearman + "centroid"
orderS_ward = np.load("data/order_S_ward.npy")         # Spearman + "ward"
orderK_single = np.load("data/order_K_single.npy")     # Kendall + "single"
orderK_average = np.load("data/order_K_average.npy")   # Kendall + "average"
orderK_centroid = np.load("data/order_K_centroid.npy") # Kendall + "centroid"
orderK_ward = np.load("data/order_K_ward.npy")         # Kendall + "ward"

# load correlation matrices:
corrP = np.load("data/corrP.npy") # Pearson
corrS = np.load("data/corrS.npy") # Spearman
corrK = np.load("data/corrK.npy") # Kendall



# === WEB APPLICATION =========================================================
# base popup style to return to:
popup_base_style = {
    "position": "sticky",
    "top": "150px",
    "left": "30px",
    "zIndex": 1000,
    "padding": "0px",
    "border": "0px",
    "backgroundColor": "#daeaf5",
    "display": "none"
}

# define the app:
app = dash.Dash(__name__)
app.title = "Neuralink Compression Challenge: Data Visualization"

# define the application layout:
app.layout = html.Div([

    # sidebar:
    html.Div([ 
        html.H1("NEURALINK COMPRESSION CHALLENGE 🧠"),
        html.H2("DATA VISUALIZATION"),
        html.Br(),
        html.Div([ 
            html.Button("Signal View", id="signal-btn", className="switcher", n_clicks=0),
            html.Button("Image View", id="image-btn", className="switcher", n_clicks=0),
            html.Button("Correlation", id="corr-btn", className="switcher", n_clicks=0),
        ], style={"display": "flex", "flexDirection": "column", "gap": "10px"}),
        html.Br(),
        html.H3("SET RANGE"),

        # popup for channels:
        html.Div([ 
            html.Div([ 
                dcc.Input(id="channel-start", type="number", min=1, max=num_total_channels, step=1, value=1),
                dcc.Input(id="channel-end", type="number", min=1, max=num_total_channels, step=1, value=10, style={"marginLeft": "10px"}),
                html.Button("OK", id="channel-apply", className="ok-button", n_clicks=0, style={"marginLeft": "10px"}),
            ], style={ 
                "background": "#daeaf5", "width": "fit-content", "padding": "5px", "border": "0px", "borderRadius": "10px"
            })
        ], id="channel-popup", style=popup_base_style),

        # label that triggers channel popup:
        html.Label("channels 👈", id="channel-label", className="slider-label", n_clicks=0, style={"cursor": "pointer"}), 
        dcc.RangeSlider( 
            id="channel-slider", 
            min=1, 
            max=num_total_channels, 
            step=1, 
            value=[1, 10], 
            marks={i: str(i) for i in range(100, num_total_channels, 100)}, 
            tooltip={"placement": "bottom", "always_visible": True} 
        ), 

        # popup for samples:
        html.Div([ 
            html.Div([ 
                dcc.Input(id="sample-start", type="number", min=0, max=num_total_samples-1, step=1, value=0),
                dcc.Input(id="sample-end", type="number", min=0, max=num_total_samples-1, step=1, value=1000, style={"marginLeft": "10px"}),
                html.Button("OK", id="sample-apply", className="ok-button", n_clicks=0, style={"marginLeft": "10px"}),
            ], style={ 
                "background": "#daeaf5", "width": "fit-content", "padding": "5px", "border": "0px", "borderRadius": "10px"
            })
        ], id="sample-popup", style=popup_base_style), 

        # label that triggers samples popup:
        html.Label("samples 👈", id="sample-label", className="slider-label", n_clicks=0, style={"cursor": "pointer"}), 
        dcc.RangeSlider( 
            id="sample-slider", 
            min=0, 
            max=num_total_samples - 1, 
            step=100, 
            value=[0, 1000], 
            marks={i: str(i) for i in range(20000, num_total_samples, 20000)}, 
            tooltip={"placement": "bottom", "always_visible": True} 
        ),
        html.Br(),

        # sort options:
        html.H3("SORT OPTIONS"),
        html.Label("ordering method", className="dropdown-label"),
        dcc.Dropdown(
            id="method-dropdown",
            options=[
                {"label": "default", "value": "default"},
                {"label": "Nearest Point", "value": "single"},
                {"label": "UPGMA", "value": "average"},
                {"label": "UPGMC", "value": "centroid"},
                {"label": "Ward", "value": "ward"},
            ],
            value="default",
            clearable=False,
            className="dropdown",
            style={"width": "100%"}
        ),

        # correlation formulas:
        html.Label("correlation formula", id="corr-label", className="dropdown-label"),
        dcc.Dropdown(
            options=[
                {"label": "Pearson", "value": "pearson"},
                {"label": "Sperman", "value": "spearman"},
                {"label": "Kendall", "value": "kendall"},
            ],
            value="pearson",
            clearable=False,
            className="dropdown",
            id="corr-dropdown",
            style={"width": "100%"}
        ),
        html.Br(),

        # additional options:
        html.H3("ADDITIONAL OPTIONS"),
        dcc.RadioItems(
            id="overlay-choice",
            options=[
                {"label": "separate plots", "value": "separate"},
                {"label": "overlay plots", "value": "overlay"}
            ],
            value="separate",
            labelClassName="custom-radio-label",
            labelStyle={
                "display": "inline-flex",
                "align-items": "center",
                "margin-left": "10px",
                "color": "rgb(119, 136, 153)",
                "font-size": "10pt",
                "cursor": "pointer",
            }
        )
    ], style={ 
        "width": "20vw", "height": "100vh", 
        "float": "left", "padding": "20px", "position": "absolute",
        "backgroundColor": "#daeaf5", "box-shadow": "0px 4px 12px lightslategray" 
    }), 

    # canvas for plots:
    html.Div([ 
        dcc.Store(id="current-view-store", storage_type="memory", data="signal-btn"),
        dcc.Graph(id="signals-plot", config={"displayModeBar": True}) 
    ], style={ 
        "width": "80vw", "height": "100vh", 
        "float": "right", "padding": "20px", "overflowY": "scroll" 
    }) 
])

# === CALLBACKS ===============================================================
# channel popups:
@app.callback(
    Output("channel-slider", "value"),
    Output("channel-popup", "style"),
    Input("channel-label", "n_clicks"),
    Input("channel-apply", "n_clicks"),
    State("channel-popup", "style"),
    State("channel-start", "value"),
    State("channel-end", "value"),
    prevent_initial_call=True
)
def handle_channel_popup(label_clicks, apply_clicks, current_style, start_val, end_val):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "channel-label":
        new_display = "none" if current_style.get("display") == "block" else "block"
        return dash.no_update, {**popup_base_style, "display": new_display}
    elif triggered_id == "channel-apply":
        start_val = max(0, min(start_val, num_total_channels - 1))
        end_val = max(0, min(end_val, num_total_channels - 1))
        start_val, end_val = sorted([start_val, end_val])
        return [start_val, end_val], {**popup_base_style, "display": "none"}
    return dash.no_update, current_style

# samples popup:
@app.callback(
    Output("sample-slider", "value"),
    Output("sample-popup", "style"),
    Input("sample-label", "n_clicks"),
    Input("sample-apply", "n_clicks"),
    State("sample-popup", "style"),
    State("sample-start", "value"),
    State("sample-end", "value"),
    prevent_initial_call=True
)
def handle_sample_popup(label_clicks, apply_clicks, current_style, start_val, end_val):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "sample-label":
        new_display = "none" if current_style.get("display") == "block" else "block"
        return dash.no_update, {**popup_base_style, "display": new_display}
    elif triggered_id == "sample-apply":
        start_val = max(0, min(start_val, num_total_samples - 1))
        end_val = max(0, min(end_val, num_total_samples - 1))
        start_val, end_val = sorted([start_val, end_val])
        return [start_val, end_val], {**popup_base_style, "display": "none"}
    return dash.no_update, current_style

# plots:
@app.callback(
    Output("signals-plot", "figure"),
    Output("current-view-store", "data"),
    Output("channel-start", "value"),
    Output("channel-end", "value"),
    Output("sample-start", "value"),
    Output("sample-end", "value"),
    Input("signal-btn", "n_clicks"),
    Input("image-btn", "n_clicks"),
    Input("corr-btn", "n_clicks"),
    Input("channel-slider", "value"),
    Input("sample-slider", "value"),
    Input("method-dropdown", "value"),
    Input("corr-dropdown", "value"),
    Input("overlay-choice", "value"),
    State("current-view-store", "data")
)
def update_plot(signal_clicks, image_clicks, corr_clicks, channel_range, sample_range, method, correlation, overlay, current_view):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "signal-btn"
    # pick the plot based on what is triggered:
    if triggered == "signal-btn":
        current_view = "signal-btn"
    elif triggered == "image-btn":
        current_view = "image-btn"
    elif triggered == "corr-btn":
        current_view = "corr-btn"
    # pick reordering:
    if method == "default":
        order = range(num_total_channels)
    elif method == "single":
        if correlation == "pearson":
            order = orderP_single
        elif correlation == "spearman":
            order = orderS_single
        elif correlation == "kendall":
            order = orderK_single
    elif method == "average":
        if correlation == "pearson":
            order = orderP_average
        elif correlation == "spearman":
            order = orderS_average
        elif correlation == "kendall":
            order = orderK_average
    elif method == "centroid":
        if correlation == "pearson":
            order = orderP_centroid
        elif correlation == "spearman":
            order = orderS_centroid
        elif correlation == "kendall":
            order = orderK_centroid
    elif method == "ward":
        if correlation == "pearson":
            order = orderP_ward
        elif correlation == "spearman":
            order = orderS_ward
        elif correlation == "kendall":
            order = orderK_ward
    # info about signals:
    start_ch, end_ch = sorted(channel_range)
    start_ch -= 1
    start_samp, end_samp = sorted(sample_range)
    # prevent out-of-bounds:
    start_ch = max(0, min(start_ch, signals_data.shape[0] - 1))
    end_ch = max(0, min(end_ch, signals_data.shape[0]))
    start_samp = max(0, min(start_samp, signals_data.shape[1] - 1))
    end_samp = max(0, min(end_samp, signals_data.shape[1]))
    # ensure non-empty range:
    if end_ch <= start_ch or end_samp <= start_samp:
        return go.Figure().update_layout(title="Invalid selection: No data to display"), current_view

    # if image view is selected:
    if current_view == "image-btn":
        # reorder and slice:
        ordered_channels = np.array(order)[start_ch:end_ch]
        data = signals_data[ordered_channels, start_samp:end_samp]
        num_channels = data.shape[0]
        # make tickvals:
        tick_vals_x = list(range(start_samp, end_samp))
        tick_vals_y = list(range(start_ch+1, end_ch+1))
        # deal with overflow:
        MAX_COLS = 50000
        orig_cols = data.shape[1]
        downsampled = False
        if orig_cols > MAX_COLS:
            data = data[:, ::2]
            tick_vals_x = tick_vals_x[::2]
            downsampled = True
        # deal with labels:
        max_labels = 50
        if num_channels > max_labels:
            showlabels = False
        else:
            showlabels = True
        # make heatmap:
        fig = go.Figure(data=go.Heatmap(z=data, colorscale="RdYlGn", zmid=0, hovertemplate="Channel: %{y}<br>Sample: %{x}<br>Voltage: %{z}<extra></extra>"))
        # update the layout:
        fig.update_layout(
            title=f'Image View {"(downsampled)" if downsampled else ""}',
            height=750,
            width=1320,
            autosize=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_yaxes(
            showticklabels=showlabels,
            tickmode="array",
            tickvals=list(range(data.shape[0]+1)),
            ticktext=ordered_channels
        )
        fig.update_traces(
            x=tick_vals_x,
            y=tick_vals_y
        )
    

    # if correlation view is selected:
    elif current_view == "corr-btn":
        # pick the correlation matrix based on selection:
        if correlation == "pearson":
            corr = corrP
        if correlation == "spearman":
            corr = corrS
        if correlation == "kendall":
            corr = corrK
        # reorder the correlation matrix:
        ordered_channels = np.array(order)[start_ch:end_ch]
        corr_order = corr[np.ix_(ordered_channels, ordered_channels)]
        num_channels = corr_order.shape[0]
        # make the heatmap:
        fig = go.Figure(data=go.Heatmap(z=corr_order, colorscale="RdYlBu", zmin=-1, zmax=1, zmid=0, hovertemplate="Channel A: %{y}<br>Channel B: %{x}<br>Correlation: %{z}<extra></extra>"))
        # make tickvals:
        tick_vals_x = list(range(start_ch+1, end_ch+1))
        tick_vals_y = list(range(start_ch+1, end_ch+1))
        # deal with labels:
        max_labels = 50
        if num_channels > max_labels:
            showlabels = False
        else:
            showlabels = True
        # update the layout:
        fig.update_yaxes(
            autorange="reversed",
            showticklabels=showlabels,
            tickmode="array",
            tickvals=list(range(corr_order.shape[0]+1)),
            ticktext=ordered_channels
        )
        fig.update_xaxes(
            showticklabels=showlabels,
            tickmode="array",
            tickvals=list(range(corr_order.shape[0]+1)),
            ticktext=ordered_channels
        )
        fig.update_traces(
            x=tick_vals_x,
            y=tick_vals_y
        )
        fig.update_layout(
            title=f"Correlation Matrix ({correlation})",
            height=800,
            width=800
        )


    # if signal view is selected (default):
    else:
        # reorder and slice:
        ordered_channels = np.array(order)[start_ch:end_ch]
        data = signals_data[ordered_channels, start_samp:end_samp]
        num_channels = data.shape[0]
        # determine the overlay setting:
        if overlay == "separate":
            fig = make_subplots(
                rows=num_channels,
                cols=1,
            )
            fig.update_layout(
                height=num_channels * 150,
                title="Signal View (separate)",
                showlegend=False,
                margin=dict(l=40, r=20, t=40, b=20),
                hovermode="x unified",
                plot_bgcolor="#daeaf5"
            )
            for i in range(num_channels):
                fig.add_trace(
                    go.Scatter(x=np.arange(start_samp, end_samp), y=data[i], mode="lines", name=f"Ch{ordered_channels[i] + 1}"),
                    row=i + 1, col=1
                )
                fig.update_yaxes(
                    title_text=f"Ch{ordered_channels[i] + 1}",
                    row=i + 1, col=1,
                    zerolinecolor="rgb(119, 136, 153)",
                    zerolinewidth=1
                )
                fig.update_xaxes(
                    matches="x",
                    row=i + 1,
                    col=1
                )
            fig.update_xaxes(range=[start_samp, end_samp])
        elif overlay == "overlay":
            fig = go.Figure()
            fig.update_layout(
                title="Signal View (overlay)",
                showlegend=True,
                xaxis_title="samples",
                yaxis_title="voltage",
                height=750,
                width=1320,
                hovermode="x unified",
                plot_bgcolor="#daeaf5"
            )
            for i in range(data.shape[0]):
                fig.add_trace(
                    go.Scatter(
                        y=data[i],
                        x=np.arange(data.shape[1]),
                        mode="lines",
                        name=f"Ch{ordered_channels[i] + 1}"
                    )
                )
            fig.update_yaxes(
                zerolinecolor="rgb(119, 136, 153)",
                zerolinewidth=1
            )
    return fig, current_view, start_ch, end_ch, start_samp, end_samp


# start the application on "http://127.0.0.1:8050/":
if __name__ == "__main__":
    app.run(debug=True)