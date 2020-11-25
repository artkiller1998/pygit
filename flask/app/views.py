# coding: utf-8
from app import app,redirect
from flask import render_template, request,send_file
from app import pygit as pg

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    glob_list=[]  
    if  request.method == 'POST' :
        repos = request.form['repos']
        token = request.form['token']
        if request.form['submit_button'] == 'Run':
            try :
                glob_list = pg.get_info(repos, token)
                if glob_list[0] == "error":
                    return render_template("index.html", glob_list = glob_list, token = token, repos = repos, error = glob_list[1])
            except :
                if glob_list[0] == "error":
                    return render_template("index.html", glob_list = glob_list, token = token, repos = repos, error = glob_list[1])
                return render_template("index.html", glob_list = glob_list, token = token, repos = repos)
            return render_template("index.html", glob_list = glob_list, token = token, repos = repos)
        elif request.form['submit_button'] == 'More':
            if glob_list == []:
                glob_list = pg.get_info(repos, token)
            glob_list = pg.count_of_pages(token, glob_list)

            return render_template("index.html", glob_list = glob_list, token = token, repos = repos, array = [glob_list, 'output' , 'csv'])
        
    return render_template("index.html", glob_list = glob_list)
        
        
@app.route('/uploads/send_file')
def download():
    path = "../tmp/output.csv"
    return send_file(path, as_attachment=True)
        
@app.route('/about')
def about():
    print(app.root_path)
    return render_template("about.html")
    
