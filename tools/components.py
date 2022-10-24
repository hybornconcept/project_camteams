import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from tools.database import fetch_drivers
import numpy as np

# spacing function


def spacer(number):
    for i in range(number):
        st.markdown(
            '<br/>', unsafe_allow_html=True)


def card_kpis(kpi, title, font):
    formatic = f"""
        <div class="card text-bg-dark " style="height:50vh;margin-top:12vh;">
        <div class="card-header border-secondary rounded-top-3" style="background-color:#262837;">KPIs</div>
            <div class="card-body rounded-4" style="background-color:#262837;">"""
    for (a, b, c) in zip(kpi, title, font):
        formatic += f"""
        <div class="row mb-4">
            <div class="col-md-4 text-bg-transparent row align-items-center  ms-1" style="max-height:8vh;">
                    <div class=" d-flex justify-content-center align-items-center mx-auto rounded-circle p-3" style=" width:3.5rem; border:1px solid #00DBD6;">
                        <i class="bi bi-{c}" style="font-size:15px"></i>
                    </div>
            </div>
                <div class="col-md-8">
                    <p class="display-6  p-0 mb-0 text-nowrap">{a}</p>
                    <p class="text-small text-muted mb-0 fst-italic">{b}</p>
                 </div>
            </div>
                <hr style="margin-bottom:1vh;">
             """
    formatic += f"""</div> </div>"""
    return formatic


@st.cache
def sanitize():
    # fetch data
    # drivers = fetch_drivers()
    # main_df = pd.DataFrame(drivers)
    # main_df = pd.json_normalize(drivers)
    # new_names = ([i.split('.')[1] if "." in i else i for i in main_df.columns])
    # main_df.columns = new_names
    # s = main_df.columns.to_series().groupby(main_df.columns)
    # main_df.columns = np.where(s.transform('size') > 1,
    #                            main_df.columns + s.cumcount().add(1).astype(str),
    #                            main_df.columns)
    # main_df['date_of_entry'] = pd.to_datetime(
    #     main_df['key'], unit='ms').dt.date
    # main_df = main_df.drop(['ip', 'accuracy', 'altitude',
    #                         'altitudeAccuracy', 'heading', 'speed', 'key'], axis=1)
    # clean data
    main_df = pd.read_csv(r"Book1.csv")
    main_df['latitude2'].fillna(value=main_df['latitude1'], inplace=True)
    main_df['longitude2'].fillna(value=main_df['longitude1'], inplace=True)
    cols = ['cam_teams', 'entry', 'residence_area',
            'type_of_structural_driver']
    main_df[cols] = main_df[cols].astype('category')
    main_df = main_df.drop(['latitude1', 'longitude1'], axis='columns').rename(
        {'latitude2': 'lat', 'longitude2': 'lon'}, axis='columns')
    main_df['date'] = pd.to_datetime(
        '1900-01-01') + pd.to_timedelta(main_df['date_of_entry'], 'D')
    # main_df['date'] = main_df['date_of_entry'].dt.date
    final_df = main_df.dropna(subset=['date_of_entry'])
    final_df.shape
    return final_df


def barchart(df, col1, col2):
    spacer(2)
    st.subheader("Level of Effort By CAM Teams")
    dfplot = df.groupby(col1)[col2].agg(
        ['count']).reset_index().sort_values('count', ascending=False)
    color_discrete_sequence = ['#00C0BB']*len(dfplot)
    fig = px.bar(dfplot, x=col1, y='count', text='count', color_discrete_sequence=color_discrete_sequence,
                 labels={
                     "cam_teams": "CAM Teams",
                     "count": "Number of Structural Drivers",
                 },)

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      yaxis=dict(showgrid=False),
                      xaxis=dict(showgrid=False),
                      font=dict(size=12),
                      font_family="Montserrat",
                      font_color="white",
                      height=400,
                      )
    return st.plotly_chart(fig, use_container_width=True)


def trendchart(df, col1, col2):
    spacer(2)
    st.subheader("Trend of Level of Effort")
    dfplot = df.groupby(col1)[col2].agg(
        ['count']).reset_index().sort_values(col1, ascending=False)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=dfplot[col1], y=dfplot['count'], text=dfplot['count'], marker=dict(size=10), mode='lines+markers+text', fill='tonexty', textposition='top center', line_color='#00C0BB'))
    fig_trend.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            yaxis=dict(showgrid=False),
                            xaxis=dict(showgrid=False),
                            font=dict(size=10),
                            font_family="Montserrat",
                            font_color="white",
                            height=400,
                            )
    fig_trend.update_yaxes(
        title_text="Total Entry")
    fig_trend.update_xaxes(
        title_text="Date of Entry")
    return st.plotly_chart(fig_trend, use_container_width=True)

# ------------------------------pie chart-----------------------------------------------------


def pie_chart(df, col1, col2):

    # Use `hole` to create a donut-like pie chart
    colors = ['#00C8C3', '#00B6EC', '#E0FFFF']
    dfplot = df.groupby(col1)[col2].agg(
        ['count']).reset_index().sort_values('count', ascending=False)
    fig = go.Figure(
        data=[go.Pie(labels=dfplot[col1], values=dfplot['count'], hole=.3)])
    fig.update_traces(textinfo='label+percent+value',
                      hoverinfo='label+percent+value', textfont_size=15,  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(size=12),
                      showlegend=False,
                      height=400,
                      )
    st.plotly_chart(fig, use_container_width=True)

# download data


def filedownload(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="CRSMapData.csv">Download CSV File</a>'
    return href
