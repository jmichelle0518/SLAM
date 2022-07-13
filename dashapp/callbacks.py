from dash import Dash, dcc, html, Input, Output, State
#import os
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
import copy
#from flask import Flask#, send_from_directory
# from functions.xml_parser import xml_parser
from app.functions.upload_files import file_download_link, save_file, uploaded_files

#server = Flask(__name__)

badwords = {
    "type1":["neat","cool"],
    "type2":["and","or","but"],
    "type3":["word","them"]
    }

def run_style(run):
    style = {}
    if run.bold:
        style["font-weight"] = "bold"
    if run.italic:
        style["font-style"] = "italic"
    if run.underline:
        style["text-decoration"] = "underline" # https://www.w3schools.com/cssref/pr_text_text-decoration.asp
    if run.font.all_caps:
        style["font-variant"] = "small-caps"
#    if not run.font.color.ColorFormat.type == "None":
#        style[color] = run.font.color.ColorFormat.rgb # https://python-docx.readthedocs.io/en/latest/api/shared.html#docx.shared.RGBColor
    if not run.font.highlight_color is None:
        #print(run.font.highlight_color)
        match run.font.highlight_color:
            case WD_COLOR_INDEX.AUTO:
                #print(run.text + ": AUTO")
                style["background-color"]=""
            case WD_COLOR_INDEX.BLACK:
                #print(run.text + ": BLACK")
                style["background-color"]="black"
            case WD_COLOR_INDEX.BLUE:
                #print(run.text + ": BLUE")
                style["background-color"]="blue"
            case WD_COLOR_INDEX.BRIGHT_GREEN:
                #print(run.text + ": BRIGHT_GREEN")
                style["background-color"]="#00FF00"
            case WD_COLOR_INDEX.DARK_BLUE:
                #print(run.text + ": DARK_BLUE")
                style["background-color"]="#000080"
            case WD_COLOR_INDEX.DARK_RED:
                #print(run.text + ": DARK_RED")
                style["background-color"]="#800000"
            case WD_COLOR_INDEX.DARK_YELLOW:
                #print(run.text + ": DARK_YELLOW")
                style["background-color"]="#808000"
            case WD_COLOR_INDEX.GRAY_25:
                #print(run.text + ": GRAY_25")
                style["background-color"]="#C0C0C0"
            case WD_COLOR_INDEX.GRAY_50:
                #print(run.text + ": GRAY_50")
                style["background-color"]="#808080"
            case WD_COLOR_INDEX.GREEN:
                #print(run.text + ": GREEN")
                style["background-color"]="#008000"
            case WD_COLOR_INDEX.PINK:
                #print(run.text + ": PINK")
                style["background-color"]="#FF00FF"
            case WD_COLOR_INDEX.RED:
                #print(run.text + ": RED")
                style["background-color"]="#FF0000"
            case WD_COLOR_INDEX.TEAL:
                #print(run.text + ": TEAL")
                style["background-color"]="#008080"
            case WD_COLOR_INDEX.TURQUOISE:
                #print(run.text + ": TURQUOISE")
                style["background-color"]="#00FFFF"
            case WD_COLOR_INDEX.VIOLET:
                #print(run.text + ": VIOLET")
                style["background-color"]="#800080"
            case WD_COLOR_INDEX.WHITE:
                #print(run.text + ": WHITE")
                style["background-color"]="#FFFFFF"
            case WD_COLOR_INDEX.YELLOW:
                #print(run.text + ": YELLOW")
                style["background-color"]="#FFFF00"
    if not run.font.size is None:
        style["font-size"] = str(run.font.size.pt) + "pt"
    if run.font.small_caps:
        style["font-variant"] = "small-caps"
    return style

def para_style(para):
    document_body=""
    match para.style.name:
        case "Heading 1":
            #para_contents=html.H1(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])
            return html.H1(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])
        case "Heading 2":
            return html.H2(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])
        case "Normal":
            return html.P(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])
        case _:
            return html.P(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])

def register_callbacks(app, flask=True):
    @app.callback(                          # callback on upload file chosen
        [Output("file-list", "children"), Output("doc-title","children")],
        [Input("upload-data", "filename"), Input("upload-data", "contents")],
    )
    def update_active_files(uploaded_filenames, uploaded_file_contents):
        """Save uploaded files and regenerate the file list."""
        names = []
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data)

        files = uploaded_files()
        if len(files) == 0:
            return [html.Li("No files yet!")],''
        else:
            return [html.Li(file_download_link(filename)) for filename in files], [name.split('.')[0] for name in uploaded_filenames]

    @app.callback(
        Output("text-preview","children"),
        [Input("language_picker","value"),Input("ready","n_clicks")]
    )
    def newfunc(values,n):
        import os
        """This function needs to take the language category and uploaded file to start returning data"""
        files = uploaded_files()

        runs=""
        targetwords={}
        for key, values in badwords.items():
            targetwords[key]={}
            for value in values:
                targetwords[key][value]=0

        for file in files:
            doc=Document(files[file]) # need to figure out how to reference the path for a specific doc
            #print("Filename: " + file)
            docstring = ""
            for paragraph in doc.paragraphs:
                #print("Paragraph: " + paragraph.text)
                docstring+=paragraph.text+"<br>"
                for key, values in badwords.items():
                    if(isinstance(values,list)):
                        for value in values:
                            if value in paragraph.text:
                                currRuns = copy.copy(paragraph.runs)
                                paragraph.runs.clear()
                                targetwords[key][value]+=paragraph.text.count(value)

                    else:
                        if values in paragraph.text:
                            currRuns = copy.copy(paragraph.runs)
                            paragraph.runs.clear()

                            for run in currRuns:
                                if values in run.text:
                                    #print("Run: " + run.text + "_____End Run_____")
                                    targetwords[key]+=1
            #print(file + " has " + str(targetwords) + " mismatched words.")
            os.remove(files[file])         #will need to move once we get the download function up and running
            items = []
            keyword_outline = []
            for key in targetwords:
                keyword_outline.append(html.P(key + ": "))
                keyword_outline.append(html.Ul(
                    children=[html.Li(str(targetwords[key][key1])+ " " + key1 + " keywords.") for key1 in targetwords[key]]
                ))

            for paragraph in doc.paragraphs:
                items.append(
                    para_style(paragraph)
                )
            return items
