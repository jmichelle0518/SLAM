from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

badwords = {
    "type1":["neat","cool"],
    "type2":["and","or","but"],
    "type3":["word","them"]
    }

switches = dbc.Checklist(
    label_style={'color':'#CCC'},
    options=list(badwords.keys()),
    value=[],
    id="switches-input",
    switch=True,
)

old_checklist = dcc.Checklist(
    className="form-check mb-5",
    inputClassName="form-check-input",
    labelClassName="form-check-label1",
    options=list(badwords.keys()),
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

input_panel = [
    html.A(
        html.Img(
            className="logo",
            #src=app.get_asset_url("dash-logo-new.png"),
        ),
        href="https://plotly.com/dash/",
    ),
    html.H1(className="auth-title",children=["SLAM Tool"]),
    html.P(className="auth-subtitle mb-5",
        children=["""Select the applicable language types, upload a document, then click ready to have it analyzed for inappropriate language."""]
    ),
    html.Div(className="mb-5 mt-5",
        children=[
            html.H2(className="card-title",children=["SLAM Language Types:"],),
            html.P(className="auth-subtitle mb-5",
                children=["This component is inactive."],style={'font-style':'italic'}),
            html.Div(style={'margin-top':'1em','padding-left':'12px'},
                children=[
                    switches,
                    old_checklist
                ]

            )
        ]
    ), #language picker
    html.Div(
        className="mb-5 mt-5",
        children=[
            html.H2("Upload SOW"),
            dcc.Upload(
                id="upload-data",
                children=[
                    html.Div(style={"font-family":"Open Sans",'font-size':'1.1em','color':'#777'},
                        children=["Drag and drop or click to select a file to upload."]
                    )
                ],
                style={
                    #"width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "12px",
                },
                multiple=True,
            ),
        ]
    ), #upload button
    html.Div(className="mb-5 mt-6",
        children=[
            html.P(id="file-list")
        ]),
    html.Div(className="mb-5 mt-6",
        children=[
            dbc.ButtonGroup(
                className="vstack gap-4 col-md-5",
                style={
                    'height':'10rem',
                    'width':'100%',
                    'font-family':'Open Sans',
                    'padding-left':'12px',
                    'padding-right':'12px'
                },
                children=[
                    dbc.Button(className="align-self-center",id='ready',color="primary",children=["Ready"],style={'width':'50%','font-size':'1.5rem'}),
                    dbc.Button(className="align-self-center",id="restart",color="secondary",children=["Start Over"],style={'width':'50%','font-size':'1.5rem'})
                ]
            )
        ]
    )]

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
                            id="bar",
                            style={'max-height':'400px'},
                            figure={
                                'layout':{
                                    'height':'48%',
                                    'margin':'0'
                                }
                            }
                        )
                    ]
                )
            ]
        )
    ]
)

preview_pane = dbc.Col(className="col-md-12", style={'margin-top':'2em','align':'center','padding':'1rem'},
    children=[
        html.Div(className="card",
            children=[
                html.Div(className="card-body",
                    children=[
                        html.H3(className="card-title",style={'text-align':'center'},
                            children=["Document Preview"]),
                        html.H4(className="card-subtitle mb-3", id="doc-title",children=["Hi"]),
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
        html.H1([
            html.Img(src="", width="30", style={'marginRight':'8px', 'color':'white'}),
            dcc.Link('IMAGINARY COMPANY',href='/',refresh=True, id='app_title')
        ]),
        html.Div(id='logos',children=[
            logo
        ]),
        ],
        className='d-flex',
        style={'margin':'0','padding':'1rem','background-color':'#16244e','height':'100%'}
    )
    return header_layout

main_layout = html.Div(id="auth",
    children=[
        dbc.Row(className="h-100",
            children=[
                html.Div(className="col-lg-5 col-12", # Column for user controls
                    children=[
                        html.Div(id="auth-left",
                            children=input_panel,
                        ),
                    ],
                ),
                html.Div(className="col-lg-7 d-none d-lg-block", # Column for app graphs and plots
                    id="auth-right",
                    children=[
                        html.Div(#id="auth-right",
                            className="p-5",
                            #style={'padding':'2rem'},
                            children=[
                                dbc.Row( # chart row
                                    className="h-50",
                                    children=[
                                        #chart_card
                                    ]), # chart
                                dbc.Row( # preview pane row
                                    className="h-50",
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
            ], id='header-container', className='header h-10'
            ),
            main_layout
        ],
        className='container-fluid page-wrap')
    return page_layout
