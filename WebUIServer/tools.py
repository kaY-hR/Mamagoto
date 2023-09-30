from markdown import markdown
from flask import Markup

def read_md(name:str) -> str:
    with open(f'./WebUIServer/static/{name}.md', mode='r',encoding='utf-8') as mdfile:
        mdcontent = mdfile.read()
    return Markup(markdown(mdcontent))