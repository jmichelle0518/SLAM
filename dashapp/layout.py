from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

switches = dbc.Checklist(
    label_style={'color':'#CCC'},
    #options=list(badwords.keys()),
    value=[],
    id="switches-input",
    switch=True,
)

old_checklist = dcc.Checklist(
    className="form-check mb-2",
    inputClassName="form-check-input",
    labelClassName="form-check-label1",
    #options=list(badwords.keys()),
    value=[],
    id='language_picker',
    inline=False
)

logo = html.Span(
    [
        html.Img(id="logo", className='mr-1',src='',width='60',draggable='false'),
        dbc.Tooltip(
            children=[
                html.P('This is my logo.')
            ],
            target="logo"
        )
    ]
)

input_panel = html.Div(id="auth-left",
    children=[
        html.Div(
            className="",
            children=[html.A(
                html.Img(
                    className="logo",
                    #src=app.get_asset_url("dash-logo-new.png"),
                ),
                href="https://plotly.com/dash/",
            ),]
        ),
        html.H1(className="auth-title",children=["SLAM Tool"]),
        html.P(className="auth-subtitle",
            children=["""Select the applicable language types, upload a document,
            then click ready to have it analyzed for inappropriate language."""]
        ),
        html.Div(className="my-4",
            children=[
                html.H2(className="card-title",children=["SLAM Language Types:"],),
                html.P(className="auth-subtitle",
                    children=["Which appropriation categories apply to this SOW?"]),
                html.Div(style={'margin-top':'1em','padding-left':'12px'},
                    children=[
                        #switches,
                        old_checklist
                    ]

                )
            ]
        ), #language picker
        html.Div(
            className="my-4",
            children=[
                html.H2("Upload SOW"),
                dcc.Upload(
                    id="upload-data",
                    children=[
                        html.Div(style={'font-size':'1.1em','color':'#777'},
                            children=["Drag and drop or click to select a file to upload."]
                        )
                    ],
                    style={
                        "padding":"0.75rem 1.5rem",
                        "lineHeight": "1.5rem",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "0.5rem",
                        "textAlign": "center",
                        "margin": "1rem",
                    },
                    multiple=True,
                ),
            ]
        ), #upload button
        html.Div(className="mb-4",
            children=[
                html.P(id="file-list")
            ]),
        html.Div(className="mb-4",
            children=[
                dbc.ButtonGroup(
                    className="gap-4 col-md-5",
                    style={
                        'height':'5rem',
                        'width':'100%',
                        'padding-right':'12px'
                    },
                    children=[
                        dbc.Button(className="align-self-center p-1",id='ready',color="primary",children=["Ready"],style={'width':'49%','font-size':'1.3rem'}),
                        dbc.Button(className="align-self-center p-1",id="restart",color="secondary",children=["Start Over"],style={'width':'49%','font-size':'1.3rem'})
                    ]
                )
            ]
        )])

chart_card = dbc.Col(className="col-md-12", style={'margin-top':'2em','align':'center'},
    children=[
        html.Div(className="card", style={'margin-left':'auto','margin-right':'auto'},
            children=[
                html.Div(className="card-header",
                    children=[
                        html.H4(className="card-title",style={'text-align':'center'},
                            children=["Keywords Found"])
                    ]
                ),
                html.Div(className="card-body",
                    children=[
                        dcc.Graph(
                            #className="ratio ratio-16x9",
                            id="bar"
                        )
                    ]
                )
            ]
        )
    ]
)

preview_pane = dbc.Col(className="col-md-12", style={'margin-top':'2em','align':'center'},
    children=[
        html.Div(className="card",
            children=[
                html.Div(className="card-body",
                    children=[
                        html.H3(className="card-title",id="preview-title",style={'text-align':'center'},
                            children=["Document Preview"]),
                        #html.H4(className="card-subtitle mb-3", id="doc-title",children=["Hi"]),
                        html.P(className="card-text", id="text-preview",
                            children=[
                                "This is a bunch of text to check and see how the wrapping looks and whether I like this text class."
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

def create_header_layout():
    header_layout = html.Div(id="header",
        children=[
        html.H3(
            id="header-title", style={"vertical-align":"middle","-ms-transform": "translateY(20%)","transform": "translateY(20%)"},
            children=[
                html.Img(src="", width="30", style={'marginRight':'8px', 'color':'white'}),
                dcc.Link('IMAGINARY COMPANY',href='/',refresh=True, id='app_title')
            ]),
        html.Div(id='logos',children=[
            logo
        ]),
        ],
        className='d-flex px-5',
        style={'margin':'0','background-color':'#16244e','height':'100%'}
    )
    return header_layout

main_layout = html.Div(id="auth",
    #className="h-90",
    children=[
        dbc.Row(className="",
            children=[
                html.Div(className="col-lg-5 col-12", # Column for user controls
                    children=input_panel,
                ),
                html.Div(className="col-lg-7 d-none d-lg-block", # Column for app graphs and plots
                    id="auth-right",
                    children=[
                        html.Div(#id="auth-right",
                            className="p-5 div-for-charts",
                            #style={'padding':'2rem'},
                            children=[
                                #dbc.Row( # chart row className="", children=[chart_card]), # chart
                                dbc.Row( # preview pane row
                                    className="",
                                    children=[
                                        preview_pane
                                    ]
                                ), # preview pane
                            ],
                        )
                    ],
                ),
            ]
        ),
    ],
)

def serve_layout():
    page_layout = html.Div(id='page-container',
        style={'margin':'0px','padding':'0px'},
        children=[
            dcc.Location(id='url',refresh=False),
            html.Div([
                create_header_layout(),
            ], id='header-container', className='header h-5'
            ),
            main_layout
        ],
        className='container-fluid page-wrap')
    return page_layout
