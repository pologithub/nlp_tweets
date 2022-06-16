from dash import Dash, dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
import os
import pandas as pd
import plotly.express as px
from utils import *
from model import *
from bertopic import BERTopic
from graph import wordcloud_plot
import glob
import dash_bootstrap_components as dbc
from dash import html



# path_to_pics = os.path.abspath(os.path.join(os.getcwd(), 'data', 'photo'))

image_directory = os.path.abspath(os.path.join(os.getcwd(), 'data', 'photo'))
list_of_images = []
for file in os.listdir(image_directory):
    if file[-3:] == 'png':
        list_of_images.append(file)
static_image_route = '/static/'

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# PLOTLY_LOGO = "https://raw.githubusercontent.com/lewagon/fullstack-images/master/uikit/logo.png"



# df with tweets and labels
path_to_df_tweet_with_labels = os.path.abspath(os.path.join(os.getcwd(), 'data', 'tweets_with_labels.csv'))
df_tweet_with_labels = pd.read_csv(path_to_df_tweet_with_labels)

# df tweets by candidats and labels
df_candidat_count_labels = df_tweet_with_labels[['name_autor', 'label_topic', 'label_tweet']]\
    .groupby(['name_autor', 'label_topic']).count().reset_index().rename(columns={'label_tweet': 'count'})


def tweets_by_candidat_day():

    df_tweet_date = df_tweet_with_labels[
        df_tweet_with_labels['date_tweet'] > '2021-10-01']

    df_tweet_date["date_tweet"] = df_tweet_date["date_tweet"].apply(
        pd.to_datetime)

    df_original_tweet_by_candidate = df_tweet_date.groupby([
        pd.Grouper(key='date_tweet', freq='d'), 'name_autor'
    ]).size().reset_index().rename(columns={0: "Numbers of Tweets"})

    import plotly.express as px

    fig = px.bar(df_original_tweet_by_candidate,
                 x="date_tweet",
                 y="Numbers of Tweets",
                 color="name_autor")

    fig.update_layout(xaxis_title="Date",
                      yaxis_title="Numbers of Tweets",
                      legend_title="Candidates",
                      font=dict(size=14, color="black"))

    return fig


TITLE = 'Mr(s) President'




NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row([
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Plotly", className="ml-2")),
                ],
                align="center",
                # no_gutters=True,
            ),
            href="https://plot.ly",

        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)




TITLEE = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(className="col-md-1", ),
                dbc.Col(
                    dbc.CardImg(
                        src=
                        "https://raw.githubusercontent.com/lewagon/fullstack-images/master/uikit/logo.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-2",
                ),
                dbc.Col(
                    dbc.CardBody([
                        html.H2("Le Wagon Nantes | Data Science | Batch #789",
                                className="card-title"),
                        html.H4("Mr(s) President", className="card-title"),
                        html.P(
                            "Extraction with twiter API and Analysis presidential candidate tweets with unsupervised techniques (Topic Modeling) to extract tweets topics.",
                            className="card-text",
                        ),
                        html.Small(
                            "11/03/2022",
                            className="card-text text-muted",
                        ),
                    ]),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-12",
    style={"maxWidth": "1200px"},
)




"""

TITLEE = dbc.Row([
    dbc.Col(first_card, width=24),
])


"""



'''

NAVBAR = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        # dbc.NavItem(dbc.NavLink("Page 2", href="#")),
        # dbc.NavItem(dbc.NavLink("Page 3", href="#")),
        # dbc.NavItem(dbc.NavLink("Page 4", href="#")),
    ],

    brand="Mr(s)President",
    brand_href="#",
    color="primary",
    dark=True,
    fluid=True

)
'''


table_header = [
    html.Thead(html.Tr([
    html.Th("First Name", id='cand_1'),\
    html.Th("Last Name", id='cand_2'),\
    html.Th("Last Name", id='cand_3')]))]

row1 = html.Tr([
       html.Td("Contenu", id='content_1'),\
       html.Td("Contenu", id='content_2'),\
       html.Td("Contenu", id='content_3')])

row2 = html.Tr([
       html.Td("Prediction", id='pred_1'),\
       html.Td("Prediction", id='pred_2'),\
       html.Td("Prediction", id='pred_3')])

table_body = [html.Tbody([row1, row2])]

table = dbc.Table(table_header + table_body, bordered=True)


IMAGE_HEADER = [
    dbc.CardHeader(html.H5("Word Cloud for each candidate")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-images-comps",
                children=[
                    dbc.Row([
                        dbc.Col(html.P("Choose a candidate"),
                                md=12),
                        dbc.Col(
                            [
                                dcc.Dropdown(id='image-dropdown',
                                             options=[{
                                                 'label': i.split('.')[0].replace('_', ' '),
                                                 'value': i
                                             } for i in list_of_images],
                                             value=list_of_images[0]),
                            ],
                            md=6,
                        ),
                    ]),
                    dbc.Row([dbc.Col(html.Img(id='image'))],
                            className='align-self-center'),

                ],
                type="default",
            )
        ],
        style={
            "marginTop": 0,
            "marginBottom": 0
        },
    ),
]







TWEETS_BY_CANDIDAT = [
    dbc.CardHeader(html.H5("Tweets by candidate")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-word-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-word_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(figure=tweets_by_candidat_day()),
                ],
                type="default",
            )
        ],
        style={
            "marginTop": 0,
            "marginBottom": 0
        },
    ),
]





RECUP_TWEET = [
    dbc.CardHeader(html.H5("Labeled tweets with Bertopic")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="recup_tweet_loading",
                children=[
                    # dbc.Alert(
                    #     "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                    #     id="no-data-alert-bigrams_comp",
                    #     color="warning",
                    #     style={"display": "none"},
                    # ),
                    dbc.Row([
                        dbc.Col(html.Button('Get labeled tweets!', id='submit-val', n_clicks=0),md=12),
                        dbc.Col([table],md=12),
                    ]),
                ],
                type="default",
            )
        ],
        style={
            "marginTop": 0,
            "marginBottom": 0
        },
    ),

]












COMPAIR_TWO_CANDIDATE = [
    dbc.CardHeader(html.H5("Compair topics of two candidates")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row([
                        dbc.Col(html.P("Choose two candidates to compare:"),
                                md=12),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="bigrams-comp_1",
                                    options=[{
                                        "label": i,
                                        "value": i
                                    } for i in df_candidat_count_labels.
                                             name_autor.unique()],
                                    value="Valérie Pécresse",
                                )
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="bigrams-comp_2",
                                    options=[{
                                        "label": i,
                                        "value": i
                                    } for i in df_candidat_count_labels.
                                             name_autor.unique()],
                                    value="Yannick Jadot",
                                )
                            ],
                            md=6,
                        ),
                    ]),
                    dcc.Graph(id="bigrams-comps"),
                ],
                type="default",
            )
        ],
        style={
            "marginTop": 0,
            "marginBottom": 0
        },
    ),
]





BODY = dbc.Container(
    [
        dbc.Row([
            dbc.Col(dbc.Card(TITLEE)),
        ],
                style={"marginTop": 30}),
        dbc.Row([
            dbc.Col(dbc.Card(TWEETS_BY_CANDIDAT)),
        ],
                style={"marginTop": 30}),
        dbc.Row([
            dbc.Col(dbc.Card(IMAGE_HEADER)),
        ], style={"marginTop": 30}),
        dbc.Row([
            dbc.Col(dbc.Card(COMPAIR_TWO_CANDIDATE)),
        ],
                style={"marginTop": 30}),
        dbc.Row([
            dbc.Col(dbc.Card(RECUP_TWEET)),
        ], style={"marginTop": 30}),
    ],
    className="mt-12",
)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(children=[NAVBAR, BODY])



@app.callback(
    Output("bigrams-comps", "figure"),
    [Input("bigrams-comp_1", "value"), Input("bigrams-comp_2", "value")],
)
def comp_bigram_comparisons(comp_first, comp_second):
    comp_list = [comp_first, comp_second]
    temp_df = df_candidat_count_labels[df_candidat_count_labels.name_autor.isin(comp_list)]
    temp_df = temp_df[temp_df['label_topic'] != 'no_label']
    temp_df.loc[temp_df.name_autor == comp_list[-1], "count"] = - temp_df[
        temp_df.name_autor == comp_list[-1]]['count'].values
    fig = px.bar(temp_df,
                 title="Comparison: " + comp_first + " | " + comp_second,
                 x="label_topic",
                 y="count",
                 color="name_autor",
                 template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.Bold,
                 labels={
                     "name_autor": "candidats:",
                     "count": "Nombres de tweet topics"
                 },
                 hover_data=""
                 )
    fig.update_layout(legend=dict(x=0.1, y=1.1), legend_orientation="h")
    fig.update_yaxes(
        title="number of tweet",
        showticklabels=True,
        title_font={"size": 18},
    )
    fig.update_xaxes(tickfont_size=14)
    fig.update_xaxes(
        title="Topics",
        showticklabels=True,
        title_font={"size": 18},
    )
    fig.update_xaxes(tickangle=45, title_font={"size": 20}, title_standoff=25)
    # fig.update_layout(tickvals=len(temp_df), ticktext=temp_df['label_topic'])
    fig.data[0]["hovertemplate"] = fig.data[0]["hovertemplate"][:-14]
    return fig





@app.callback(
    Output('cand_1', 'children'),
    Output('cand_2', 'children'),
    Output('cand_3', 'children'),
    Output('content_1', 'children'),
    Output('content_2', 'children'),
    Output('content_3', 'children'),
    Output('pred_1', 'children'),
    Output('pred_2', 'children'),
    Output('pred_3', 'children'),
    Input('submit-val', 'n_clicks'),)
# State('input-on-submit', 'value'))










def update_output(n_clicks):
    if n_clicks > -1:
        df_labeled = df_tweet_with_labels[
            df_tweet_with_labels['label_topic'] != 'no_label']
        df_sample_labeled_tweet = df_labeled.sample(n=3)


        df_sample_labeled_tweet_dict = df_sample_labeled_tweet.to_dict(
            'records')

        return (df_sample_labeled_tweet_dict[0]['name_autor'],
                df_sample_labeled_tweet_dict[1]['name_autor'],
                df_sample_labeled_tweet_dict[2]['name_autor'],
                df_sample_labeled_tweet_dict[0]['tweet'],
                df_sample_labeled_tweet_dict[1]['tweet'],
                df_sample_labeled_tweet_dict[2]['tweet'],
                df_sample_labeled_tweet_dict[0]['label_topic'],
                df_sample_labeled_tweet_dict[1]['label_topic'],
                df_sample_labeled_tweet_dict[2]['label_topic'])


@app.callback(Output('image', 'src'),
              [Input('image-dropdown', 'value')])



def update_image_src(value):
    return static_image_route + value

import flask
# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                image_path))
    return flask.send_from_directory(image_directory, image_name)





if __name__ == '__main__':
    app.run_server(debug=True)






"""


def update_output_old(n_clicks):
    if n_clicks > -1:

        # tweet to predict
        df_new_tweet = get_last_tweet_api()
        df_new_tweet['date_tweet'] = pd.to_datetime(df_new_tweet['date_tweet'])
        df_new_tweet = df_new_tweet.sort_values('date_tweet')
        df_new_tweet_dict = df_new_tweet.to_dict('records')
        # prediction
        model = get_model_from_local()
        list_prediction = get_topic_prediction(df_new_tweet[-3:], model)

        # last_3_tweets = df_new_tweet[-3:]
        return (df_new_tweet_dict[0]['name_autor'],
                df_new_tweet_dict[1]['name_autor'],
                df_new_tweet_dict[2]['name_autor'],
                df_new_tweet_dict[0]['tweet'], df_new_tweet_dict[1]['tweet'],
                df_new_tweet_dict[2]['tweet'], list_prediction[0],
                list_prediction[1], list_prediction[2])
"""
