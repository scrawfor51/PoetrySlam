import os


text_doc = ""
selected_text = ""


def set_text_doc(sel_text):
    global text_doc
    text_doc = sel_text


def read_text_doc():

    set_text_doc(selected_text)
    os.system("say -v Serena -r 140 '" + text_doc + "'")
