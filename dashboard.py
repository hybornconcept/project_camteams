
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dateutil import parser
from datetime import datetime

# ------------PAGE SETTINGS
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
# -----------Font CDN----------------------

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css">""", unsafe_allow_html=True)
# --- STREAMLIT STYLE ---
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
 integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)

hide_st_style = """
            <style>
            div.css-1fv8s86.e16nr0p33 >hr{margin-top:4vh;}
            div.css-zt5igj.e16nr0p32{margin-top:-3vh;}
            div.stMarkdown{margin-top:-4vh}
            span.css-10trblm.e16nr0p30{margin-top:0px}
            div.object-key-val{display:none}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ------------Spacer function-------------------


def spacer(number):
    for i in range(number):
        st.markdown(
            '<br/>', unsafe_allow_html=True)


# ------Title------------
st.markdown(f'''<h1><i class="bi bi-bar-chart-line" style="font-size:40px"></i>  Community Case Identification Dashboard</h1>''', unsafe_allow_html=True)
'---'

df = pd.read_csv(r"../cam_tools/CAM_TEST_DATA.csv")
df['tested'] = 1
df['Age'] = 2022 - df.year_of_birth
df["age_group"] = pd.cut(x=df['Age'], bins=[0, 14, 100],
                         labels=["children", "Adult"])

df['Timestamp2'] = datetime.fromtimestamp(df['Timestamp']).strftime("%Y-%m-%d")


# ---SIDEBAR---
st.sidebar.header('User Filter Data')

# --- text_result Filter ------------
st.sidebar.markdown("---", unsafe_allow_html=True)
age = st.sidebar.multiselect(
    "Test Result:",
    df.age_group.unique().tolist(), df.age_group.unique().tolist())

# --- Date Filter ------------
st.sidebar.markdown("---", unsafe_allow_html=True)
start_date = st.sidebar.date_input(
    "Start Date:",
    parser.parse(str(pd.to_datetime(df['Timestamp']).min())))


end_date = st.sidebar.date_input(
    "End Date:",
    parser.parse(str(pd.to_datetime(df['Timestamp']).max())))

# ---SexFilter ------------
st.sidebar.markdown("---", unsafe_allow_html=True)
sex = st.sidebar.multiselect(
    "Gender:",
    df.sex.unique().tolist(), df.sex.unique().tolist())

# --- CAM Team Filter ------------
st.sidebar.markdown("---", unsafe_allow_html=True)
cam_teams = st.sidebar.multiselect(
    "CAM Teams:",
    df.cam_teams.unique().tolist(), df.cam_teams.unique().tolist())


# ----------------------------------------------------------------  filtering the dataframe  --------------------------

filtered_df = df[(df['Timestamp2'] >= str(start_date)) & (df['Timestamp2'] < str(end_date)) & (
    df.sex.isin(sex)) & (df.age_group.isin(age)) & (df.cam_teams.isin(cam_teams))]


# -----------------------Metrics -------------------------------


def kpi_details(color, indicator, data, icon, achieve, percent):

    return f"""
<div class="card  bg-dark mx-4 mt-5" style="max-height:14vh;">
  <div class="row ">
  <div class="col-md-4 bg-{color} row align-items-center" style="max-height:14vh;">
    <div class=" d-flex justify-content-center align-items-center mx-auto rounded-circle p-2" style=" width:3.5rem; border:1px solid white;">
     <i class="bi bi-{icon}" style="font-size:25px"></i>
     </div>
   </div>
    <div class="col-md-8">
      <div class="card-body mx-1" >
        <p class="text-muted">{indicator} </p>
        <h5 class="card-title display-4 mt-4">{data}</h5>
        <p style="font-size:20px;margin-top:-2.5vh;" ><small class="text-muted"><i class="bi bi-arrow-down-short" ></i>{achieve} <em>{percent}</em></small></p>
      </div>
    </div>
  </div>
</div>
    """


col1, col2, col3, col4 = st.columns(4)

indicator = ['HTS_TST', 'HTS_POS', 'TX_NEW']
data = [299, 200, 566]
percents = ['2%', '4%', '5%']

icons = ['bandaid', 'person-plus', 'person-check']
index_pos = filtered_df['testing_modality'].tolist().count(
    'Geneology Testing') + filtered_df['testing_modality'].tolist().count('Sexual Network Testing')
testing_yield = (
    filtered_df.shape[0]/filtered_df['test_result'].tolist().count('Positive'))
linkage_rate = (df['linked'].tolist().count('Yes') /
                df['test_result'].tolist().count('Positive'))
ict_contribution = (
    index_pos/filtered_df['linked'].tolist().count('Yes'))

with col1:
    st.markdown(kpi_details('primary',
                            'HTS_TST', filtered_df.shape[0], 'bandaid', '', ''), unsafe_allow_html=True)


with col2:
    st.markdown(kpi_details('success', 'HTS_POS', filtered_df['test_result'].tolist().count(
        'Positive'), 'person-plus', '{:.0%}'.format(testing_yield), 'Testing Yield'), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_details('info', 'TX_NEW', filtered_df['linked'].tolist().count('Yes'), 'person-check', '{:.0%}'.format(
        linkage_rate), 'Linkage_rate'), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_details('secondary', 'INDEX_POS', index_pos, 'layout-wtf', '{}%'.format(
        ict_contribution), 'ICT Contribution'), unsafe_allow_html=True)

# --------------------------------first TABS ------------------------------------------------------------------------------------

# function deliver_dataframe  ---------------------


def deliver_dataframe(*columns):
    return filtered_df.groupby([*columns]).size().reset_index().rename(columns={0: 'total'})


spacer(3)
tab1, tab2 = st.tabs(["Testing Modality", "Case_Identification"])

with tab1:
    spacer(3)
    st.header("HTS_TST | Testing Modality")
    modality_df = deliver_dataframe('testing_modality')  # using deliver
    fig_total_tested = px.treemap(modality_df, path=["testing_modality"],
                                  values="total", title="")
    fig_total_tested.data[0].textinfo = "label+text+value"
    fig_total_tested.update_layout(
        font=dict(
            family="Open Sans",
            size=15,  # Set the font size here

        )
    )

    fig_total_tested.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_total_tested, use_container_width=True)


with tab2:
    spacer(3)
    st.header("HTS_TST | HTS_POS | Testing yield")
    yield_df = deliver_dataframe('testing_modality', 'test_result')
    new_df = yield_df.pivot_table(
        index='testing_modality', columns='test_result', values='total', aggfunc='sum').reset_index()
    new_df['Positive'] = pd.to_numeric(
        new_df.Positive, errors='coerce').fillna(0)
    new_df['tested'] = new_df['Positive'] + new_df['Negative']
    new_df['yield'] = (new_df['Positive'] / new_df['tested'])*100

    # Make subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=new_df['testing_modality'],
            y=new_df['yield'],
            text=new_df['yield'],
            # mode='lines+text+markers',
            name='testing_yield',
            textposition='top right',
            textfont=dict(color='#E58606'),
            mode='lines+markers+text',
            marker=dict(color='#5D69B1', size=10),
            texttemplate='%{text:.1f}%'
        ),
        secondary_y=True,

    )

    fig.add_trace(
        go.Bar(
            x=new_df["testing_modality"], y=new_df['tested'], text=new_df['tested'],
            name='HTS_TST',

        ),
        secondary_y=False,

    )

    fig.add_trace(
        go.Bar(
            x=new_df["testing_modality"], y=new_df['Positive'], text=new_df['Positive'],
            name='HTS_POS',

        ),
        secondary_y=False,

    )
    fig.update_yaxes(
        title_text="<b>Tested / Positive</b>", secondary_y=False,)
    fig.update_yaxes(
        title_text="<b>%Yield</b>", secondary_y=True,
        zeroline=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      yaxis=dict(showgrid=False),

                      font=dict(size=15)

                      )
    fig['layout']['yaxis1']['showgrid'] = False
    fig['layout']['yaxis2']['showgrid'] = False
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------Second Tab---------------------------------------------------
    spacer(3)
# declaring the second tabs-----------=------------------------------------------------------------
trend_tab, cam_pos_tab, linkage_tab = st.tabs(
    ["Case Identification Trend", "CAM Team Achievement", "Linkage_rate"])

# Case Identification Trend tab-----------------------------------------------------------
with trend_tab:
    spacer(3)
    st.header("Case Identification Trend")
    trend_df = deliver_dataframe('Timestamp', 'test_result').pivot_table(index='Timestamp', columns='test_result',
                                                                         values='total', aggfunc='sum').reset_index()
    trend_df['Positive'] = pd.to_numeric(
        trend_df.Positive, errors='coerce').fillna(0)
    trend_df['Negative'] = pd.to_numeric(
        trend_df.Negative, errors='coerce').fillna(0)
    trend_df['new_total'] = trend_df['Positive'] + trend_df['Negative']
    trend_df.head()

    fig_trend = go.Figure()

    fig_trend.add_trace(go.Scatter(
        x=trend_df['Timestamp'], y=trend_df['new_total'], text=trend_df['new_total'], marker=dict(size=10), mode='lines+markers+text', fill='tonexty', name='HTS_TST', textposition='top center'))

    fig_trend.add_trace(go.Scatter(
        x=trend_df['Timestamp'], y=trend_df['Positive'], text=new_df['Positive'], marker=dict(size=10), mode='lines+markers+text', fill='tozeroy', name='HTS_POS', textposition='top center')
    )
    fig_trend.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig_trend.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            yaxis=dict(showgrid=False),
                            xaxis=dict(showgrid=False),
                            font=dict(size=18),


                            )
    st.plotly_chart(fig_trend, use_container_width=True)

# HTS_POS | CAM Teams Trend tab-----------------------------------------------------------
with cam_pos_tab:
    spacer(3)
    st.header("HTS_POS | CAM Teams")
    fig_cam_achieve = px.treemap(new_df, path=["testing_modality"],
                                 values="Positive")
    fig_cam_achieve.data[0].textinfo = "label+text+value"
    fig_cam_achieve.update_layout(
        font=dict(
            family="Open Sans",
            size=15,  # Set the font size here

        )
    )
    fig_cam_achieve.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_cam_achieve, use_container_width=True)

# Linkage rate Trend tab-----------------------------------------------------------
with linkage_tab:
    spacer(3)
    st.header("Linkage rate")
    use_df = deliver_dataframe('Timestamp', 'linked', 'test_result')
    [use_df['test_result'] == 'Positive']
    linked_df = use_df.pivot_table(index='Timestamp', columns=[
                                   'linked'], values='total', aggfunc='sum').reset_index()
    linked_df['total_pos'] = linked_df['No'] + linked_df['Yes']
    linked_df['Linkage'] = (linked_df['Yes'] / linked_df['total_pos'])*100

    # Make subplots
    fig_link = make_subplots(specs=[[{"secondary_y": True}]])
    fig_link.add_trace(
        go.Scatter(
            x=linked_df['Timestamp'],
            y=linked_df['Linkage'],
            text=linked_df['Linkage'],
            # mode='lines+text+markers',
            name='Linkage rate',
            textposition='top right',
            textfont=dict(color='#E58606'),
            mode='lines+markers+text',
            marker=dict(color='#5D69B1', size=10),
            texttemplate='%{text:.1f}%'
        ),
        secondary_y=True,

    )

    fig_link.add_trace(
        go.Bar(
            x=linked_df["Timestamp"], y=linked_df['total_pos'], text=linked_df['total_pos'],
            name='HTS_POS',

        ),
        secondary_y=False,

    )

    fig_link.add_trace(
        go.Bar(
            x=linked_df["Timestamp"], y=linked_df['Yes'], text=linked_df['Yes'],
            name='TX_NEW',

        ),
        secondary_y=False,

    )
    fig_link.update_yaxes(
        title_text="<b>HTS_POS / TX_NEW</b>", secondary_y=False,)
    fig_link.update_yaxes(
        title_text="<b>%Yield</b>", secondary_y=True,
        zeroline=False)
    fig_link.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis=dict(showgrid=False),

                           font=dict(size=15)

                           )
    fig_link['layout']['yaxis1']['showgrid'] = False
    fig_link['layout']['yaxis2']['showgrid'] = False
    st.plotly_chart(fig_link, use_container_width=True)

# --------------------------------third TABS ------------------------------------------------------------------------------------

spacer(3)

sex, marital_status, education_level, age_group, income_level = st.tabs(
    ["Sex", "Marital Status", "Education Level", "Age Group", "Income Level"])


def cardinality(one, two, three):
    yield_df = filtered_df.pivot_table(
        index=one, columns=[two], values=three, aggfunc='sum').reset_index()
    yield_df['total'] = yield_df['Negative'] + yield_df['Positive']
    return yield_df


def show_chart(df, label, values, title):

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(
        data=[go.Pie(labels=df[label], values=df[values], hole=.3)])
    fig.update_traces(textinfo='label+percent+value',
                      hoverinfo='label+percent+value', textfont_size=15)
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(size=15),
                      showlegend=False,
                      title=title
                      )
    st.plotly_chart(fig, use_container_width=True)


with sex:
    tested_sex, pos_sex = st.columns(2)
    with tested_sex:  # column 1

        show_chart(cardinality('sex', 'test_result', 'tested'),
                   'sex', 'total', 'HTS_TST | Sex')

    with pos_sex:  # column 2
        show_chart(cardinality('sex', 'test_result', 'tested'),
                   'sex', 'Positive', 'HTS_POS | Sex')

with marital_status:
    marital_test, marital_pos = st.columns(2)

    with marital_test:
        show_chart(cardinality('marital_status', 'test_result', 'tested'),
                   'marital_status', 'total', 'HTS_TST | Marital Status')

    with marital_pos:  # column 2
        show_chart(cardinality('marital_status', 'test_result', 'tested'),
                   'marital_status', 'Positive', 'HTS_POS | Marital Status')

with education_level:
    test_edu, pos_edu = st.columns(2)
    with test_edu:  # column 2
        show_chart(cardinality('education_level', 'test_result', 'tested'),
                   'education_level', 'total', 'HTS_TST | Education Level')
    with pos_edu:  # column 2
        show_chart(cardinality('education_level', 'test_result', 'tested'),
                   'education_level', 'Positive', 'HTS_POS | Education Level')
with age_group:
    age_test, age_pos = st.columns(2)
    with age_test:  # column 2
        show_chart(cardinality('age_group', 'test_result', 'tested'),
                   'age_group', 'total', 'HTS_TST | Age Group')
    with age_pos:  # column 2
        show_chart(cardinality('age_group', 'test_result', 'tested'),
                   'age_group', 'Positive', 'HTS_POS | Age Group')


with income_level:
    income_test, income_pos = st.columns(2)
    with income_test:  # column 2
        show_chart(cardinality('income_level', 'test_result', 'tested'),
                   'income_level', 'total', 'HTS_TST | Income Level')
    with income_pos:  # column 2
        show_chart(cardinality('income_level', 'test_result', 'tested'),
                   'income_level', 'Positive', 'HTS_POS | Income Level')

# --------------------------------fourth TABS ------------------------------------------------------------------------------------

spacer(3)

geolocation, recency = st.tabs(["Geolocation", "Recency Test"])

with geolocation:
    geo_df = filtered_df.pivot_table(index=['lat', 'lon'], columns=[
        'test_result'], values='tested', aggfunc='sum').reset_index()
    st.map(data=geo_df)

spacer(3)
with recency:
    recency_df = filtered_df.groupby(['cam_teams', 'recency_status']).size(
    ).reset_index().rename(columns={0: 'total'})
    recency_fig = px.bar(recency_df, x='cam_teams', y='total',
                         hover_data=['cam_teams', 'total', 'recency_status'], color='recency_status',
                         labels={'rec': 'recency_status'}, text='total', height=500)
    recency_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(size=15),
                              yaxis=dict(showgrid=False)
                              )

    st.plotly_chart(recency_fig, use_container_width=True)
