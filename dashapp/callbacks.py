from dash import Dash, dcc, html, Input, Output, State
#import os
from docx import Document
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_COLOR_INDEX
import copy
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re
#from flask import Flask#, send_from_directory
# from functions.xml_parser import xml_parser
from app.functions.upload_files import file_download_link, save_file, uploaded_files

#server = Flask(__name__)

badwords = {
    "type1":[["neat","cool"],'cat1'],
    "type2":[["and","or","but"],'cat2'],
    "type3":[["word","them"],'cat3']
    }

def run_style(runs, c):
    para = {}
    index = 0
    for r in runs:
        print("line 26 == run_style: " + r.text + ".  para is " + str(len(para)) + " runs long")
        styles = {}
        if r.bold:
            styles["font-weight"] = "bold"
        if r.italic:
            styles["font-style"] = "italic"
        if r.underline:
            styles["text-decoration"] = "underline" # https://www.w3schools.com/cssref/pr_text_text-decoration.asp
        if r.font.all_caps:
            styles["font-variant"] = "small-caps"
        if not r.font.highlight_color is None:
            #print(run.font.highlight_color)
            if run.font.highlight_color is WD_COLOR_INDEX.AUTO:
                    #print(run.text + ": AUTO")
                style["background-color"]=""
            if run.font.highlight_color is WD_COLOR_INDEX.BLACK:
                    #print(run.text + ": BLACK")
                style["background-color"]="black"
            if run.font.highlight_color is WD_COLOR_INDEX.BLUE:
                    #print(run.text + ": BLUE")
                style["background-color"]="blue"
            if run.font.highlight_color is WD_COLOR_INDEX.BRIGHT_GREEN:
                    #print(run.text + ": BRIGHT_GREEN")
                style["background-color"]="#00FF00"
            if run.font.highlight_color is WD_COLOR_INDEX.DARK_BLUE:
                    #print(run.text + ": DARK_BLUE")
                style["background-color"]="#000080"
            if run.font.highlight_color is WD_COLOR_INDEX.DARK_RED:
                    #print(run.text + ": DARK_RED")
                style["background-color"]="#800000"
            if run.font.highlight_color is WD_COLOR_INDEX.DARK_YELLOW:
                    #print(run.text + ": DARK_YELLOW")
                style["background-color"]="#808000"
            if run.font.highlight_color is WD_COLOR_INDEX.GRAY_25:
                    #print(run.text + ": GRAY_25")
                style["background-color"]="#C0C0C0"
            if run.font.highlight_color is WD_COLOR_INDEX.GRAY_50:
                    #print(run.text + ": GRAY_50")
                style["background-color"]="#808080"
            if run.font.highlight_color is WD_COLOR_INDEX.GREEN:
                    #print(run.text + ": GREEN")
                style["background-color"]="#008000"
            if run.font.highlight_color is WD_COLOR_INDEX.PINK:
                    #print(run.text + ": PINK")
                style["background-color"]="#FF00FF"
            if run.font.highlight_color is WD_COLOR_INDEX.RED:
                    #print(run.text + ": RED")
                style["background-color"]="#FF0000"
            if run.font.highlight_color is WD_COLOR_INDEX.TEAL:
                    #print(run.text + ": TEAL")
                style["background-color"]="#008080"
            if run.font.highlight_color is WD_COLOR_INDEX.TURQUOISE:
                    #print(run.text + ": TURQUOISE")
                style["background-color"]="#00FFFF"
            if run.font.highlight_color is WD_COLOR_INDEX.VIOLET:
                    #print(run.text + ": VIOLET")
                style["background-color"]="#800080"
            if run.font.highlight_color is WD_COLOR_INDEX.WHITE:
                    #print(run.text + ": WHITE")
                style["background-color"]="#FFFFFF"
            if run.font.highlight_color is WD_COLOR_INDEX.YELLOW:
                    #print(run.text + ": YELLOW")
                style["background-color"]="#FFFF00"
        if not r.font.size is None:
            styles["font-size"] = str(r.font.size.pt) + "pt"
        if r.font.small_caps:
            styles["font-variant"] = "small-caps"

        for cat in c: # for each category selected
            for word in badwords[cat][0]: # for each keyword
                pattern = re.compile(word)
                print("line 98 == " + cat + ": " + word)
                if pattern.search(r.text): # if the current keyword is in this run
                    tempr = r.text.strip().split(" ")   #split the run into individual words
                    print(tempr)
                    for w in tempr: # for word in run
                        print("line 103 == w="+w)
                        if pattern.search(w): #if the word is a keyword, give it specific style
                            para[cat+w]={
                                "text":w + " ",
                                "style":{},
                                "isKeyword":True,
                                "category":cat,
                                "kw":word,
                                "className": badwords[cat][1] + " category"
                            }
                            print("line 114 == Run had keyword and word was keyword")
                        else:
                            para[cat+w]={
                                "text":w + " ",
                                "style":styles,
                                "isKeyword":False,
                                "category":'',
                                "kw":'',
                                "className":''
                            }
                            print("line 127 == Run had keyword, word was not keyword")
                        print("line 130 == ")
                        print(para[cat+w])
                        print(len(para))
                    break
                else:
                    para[cat+r.text]={
                        "text":r.text,
                        "style":styles,
                        "isKeyword":False,
                        "category":'',
                        "kw":'',
                        "className":''
                    }
                    print("line 137 == No Key Word")
                    print(para[cat+r.text])
                    print(len(para))
        #para.append(html.Span(children=[html.Span(r.text)], style = styles))
        print("line 140 == Line Appended, end of cat checks")
        #run = html.Span(children=[html.Span(r.text)], style = styles, className = classes)
    print("line 142 == End of runs in para")
    print(para)
    return [html.Span(children=v["text"],style=v["style"],className=v["className"]) for k,v in para.items()]

def para_style(para,cats):
    print("line 143 == para_style: " + para.text)
    if para.style.name == "Heading 1":
        print("line 145 == H1 " + "".join(cats))
            #para_contents=html.H1(children=[html.Span(children = [run.text],style = run_style(run)) for run in para.runs])
        return html.H1(children=run_style(para.runs,cats))
    if para.style.name == "Heading 2":
        print("line 149 == H2 " + "".join(cats))
        return html.H2(children=run_style(para.runs,cats))
        #children=[html.Span(children = [run.text],style = run_style(run,cats)) for run in para.runs])
    if para.style.name == "Normal":
        print("line 153 == Normal " + "".join(cats))
        return html.P(children=run_style(para.runs,cats))
    else:
        print("line 156 == Other " + "".join(cats))
        return html.P(children=run_style(para.runs,cats))

def register_callbacks(app, flask=True):
    @app.callback(
        [#Output("switches-input",'options'),
        Output("language_picker",'options')],
        Input("auth-left","children")
    )
    def checklist(child):
        return [list(badwords.keys())]#,list(badwords.keys())

    @app.callback(                          # callback on upload file chosen
        [Output("file-list", "children"), Output("preview-title","children")],
        [Input("upload-data", "filename"), Input("upload-data", "contents")],
    )
    def update_active_files(uploaded_filenames, uploaded_file_contents):
        """Save uploaded files and regenerate the file list."""
        names = []
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data)

        files = uploaded_files()
        if len(files) == 0 or files is None:
            return [html.Li("No files yet!")],'Document Preview'
        else:
            return [html.Li(file_download_link(filename)) for filename in files], [name.split('.')[0] for name in uploaded_filenames]

    @app.callback(
        #[
        Output("text-preview","children"),#Output("bar","figure")],
        [Input("language_picker","value"),Input("ready","n_clicks")]
    )
    def newfunc(checks,n):
        print("New Run\n")
        import os
        """This function needs to take the language category and uploaded file to start returning data"""
        files = uploaded_files()

        runs=""
        targetwords={}
        for key, v in badwords.items():
            targetwords[key]={}
            for value in v[0]:
                targetwords[key][value]=0

        for file in files:
            doc=Document(files[file]) # need to figure out how to reference the path for a specific doc
            #print("Filename: " + file)
            docstring = ""
            for paragraph in doc.paragraphs:
                #print("Paragraph: " + paragraph.text)
                docstring+=paragraph.text+"<br>"
                for k, v in badwords.items():
                    if(isinstance(v,list)):
                        for value in v[0]:
                            if value in paragraph.text:
                                currRuns = copy.copy(paragraph.runs)
                                paragraph.runs.clear()
                                targetwords[k][value]+=paragraph.text.count(value)

                    else:
                        if v in paragraph.text:
                            currRuns = copy.copy(paragraph.runs)
                            paragraph.runs.clear()

                            for run in currRuns:
                                if v in run.text:
                                    #print("Run: " + run.text + "_____End Run_____")
                                    targetwords[key]+=1
            #print(file + " has " + str(targetwords) + " mismatched words.")
            os.remove(files[file])         #will need to move once we get the download function up and running
            items = []
            keyword_outline = []
            for k in targetwords:
                keyword_outline.append(html.P(k + ": "))
                keyword_outline.append(html.Ul(
                    children=[html.Li(str(targetwords[k][key1])+ " " + key1 + " keywords.") for key1 in targetwords[k]]
                ))

            for paragraph in doc.paragraphs:
                print("line 209 == " + paragraph.text)
                items.append(
                    para_style(paragraph,checks)
                )

            df = {key: pd.Series(val) for key, val in targetwords.items() }
            df2 = pd.DataFrame.from_dict(targetwords, orient="index")
            #print(df)
            #print(df2)

            df3 = pd.DataFrame([{'Category':{},'Keyword':{},'Value':{}}])
            # for each key in targetwords, concatenate a row
            #print(targetwords)
            return items#, go.Figure(px.bar(df))
