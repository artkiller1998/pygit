import requests
import json 
import re
import openxmllib

#on the web page in the future these variables will be filled in by the teacher
#repos = 'kr-4k/2019-2020'
#token = 'JyNyFq8oJP7FsqKVcUXR'


def get_info(repos, token):
    #search for all nested repositories of a given repository

    response_repos = requests.get(
    'http://gitwork.ru/api/v4/projects/?statistics=true&search_namespaces=false&access_token=' + token + '&per_page=100&simple=true&search=' + repos).text
    respJson_repos = json.loads(response_repos)

    glob_list = [] #list where all data about repositories is stored: id, name, path_with_namespace
    
    if 'message' in respJson_repos:
        print('BAD token error!\n')
        print(respJson_repos['message'])
        glob_list.append('error')
        glob_list.append('Bad token! No access to site')
        return glob_list
    
    for r in respJson_repos:
        list_ = []
        if(re.match(r'.*-.*-.*-.*', r["name"])): #only Listener's (students') repositories are needed for example ../2016-3-1-qwe
            if(r["path_with_namespace"].count(repos + '/' + r["name"]) != 0):
                list_.append(r["id"].__str__())
                list_.append(r["name"])
                list_.append(r["path_with_namespace"])
            if list_ != []:
                glob_list.append(list_) #only student repositories are included in the list
        
    if(glob_list == []):
        print("WrongRepoErr")
        glob_list.append('error')
        glob_list.append('Bad repository name! There are no repo like "2016-03-16-caa" found')
        return glob_list


    #below is a query to find out the size of the repository
    for g in glob_list:
        resp_sizes = requests.get('http://gitwork.ru/api/v4/projects/' + g[0] + '?statistics=true&access_token=' + token).text
        json_ = json.loads(resp_sizes)
        g.append(json_["statistics"]["repository_size"])
        
 
    #a list containing information about the availability of necessary files in the repository (Result.docx, text.docx etc.)
    table_availiblity = []
    
    names_of_text_and_result = []
     
    for g in glob_list:
        readme_available = False
        result_doc_available = False
        result_ppt_available = False
        project_available = False
        text_doc_available = False
        
        list_ = []
        names_ = []
        
        #request that outputs information about the repository (the number of files in it, their name, and other service information)
        resp_available = requests.get('http://gitwork.ru/api/v4/projects/' + g[0] + '/repository/tree?access_token=' + token).text
        
        json_ = json.loads(resp_available)
        
        if(resp_available.count('README.md') != 0 or resp_available.count('Readme.md') != 0 or resp_available.count('readme.md') != 0):
            readme_available = True
            
        if(resp_available.count('Result.docx') != 0 or resp_available.count('result.docx') != 0 or resp_available.count('RESULT.docx') != 0 or resp_available.count('Result.doc') != 0 or resp_available.count('result.doc') != 0 or resp_available.count('RESULT.doc') != 0):
            result_doc_available = True
            
        if(resp_available.count('Result.pptx') != 0 or resp_available.count('result.pptx') != 0 or resp_available.count('RESULT.pptx') != 0 or resp_available.count('Result.ppt') != 0 or resp_available.count('result.ppt') != 0 or resp_available.count('RESULT.ppt') != 0):
            result_ppt_available = True
            
            for j in json_:
                if(j['name'] == 'Result.pptx' or j['name'] == 'result.pptx' or j['name'] == 'RESULT.pptx' or j['name'] == 'Result.ppt' or j['name'] == 'result.ppt' or j['name'] == 'RESULT.ppt'):
                    names_.append(j['name'])
        
        if(resp_available.count('text.docx') != 0 or resp_available.count('Text.docx') != 0 or resp_available.count('TEXT.docx') != 0 or resp_available.count('text.doc') != 0 or resp_available.count('Text.doc') != 0 or resp_available.count('TEXT.doc') != 0):
            text_doc_available = True
        
            for j in json_:
                if(j['name'] == 'Text.docx' or j['name'] == 'text.docx' or j['name'] == 'TEXT.docx' or j['name'] == 'Text.doc' or j['name'] == 'text.doc' or j['name'] == 'TEXT.doc'):
                    names_.append(j['name'])
        
        
        if(resp_available.count('Project') != 0 or resp_available.count('project') != 0 or resp_available.count('PROJECT') != 0):
            project_available = True
            
        list_.append(readme_available)
        list_.append(result_doc_available)
        list_.append(result_ppt_available)
        list_.append(text_doc_available)
        list_.append(project_available)
        
        table_availiblity.append(list_)
        
        names_of_text_and_result.append(names_)
    
 
    f = open('./tmp/output.csv', 'w')
    f.write(';readme.md;result.docx;result.pptx;text.docx;project;size;\n')
    
    
    result_list = []
    

    for t, g, n in zip(table_availiblity, glob_list, names_of_text_and_result):
        f.write(g[1] + ';')
        list_ = []
        list_.append(g[1] )
        for a in t:
            list_.append('+' if  a==True else '-')
            if(a == True):
                f.write('+'+ ";")
            else:
                f.write('-' + ';')
        f.write(round((g[3]/1024.0),2).__str__() + ';')
        f.write('\n')
        list_.append(round((g[3]/1024.0),2).__str__())
        list_.append(g[0])
        list_.append(n)
        result_list.append(list_)
        
    # sorting by group, then by number
    new_result_list = sorted(result_list, key=lambda x:(int(x[0][5:6]), int(x[0][7:9])))
    
    return new_result_list
    
def count_of_pages(token, glob_list):
    count_of_pages_and_slides = []
    
    for g in glob_list:
        count_ = []
        if (g[4] == '+'):
            with requests.get('http://gitwork.ru/api/v4/projects/' + g[7] + '/repository/files/' + g[8][1]+ '/raw?ref=master&access_token=' + token) as rq:
                with open('./tmp/text.docx', 'wb') as file:
                    file.write(rq.content)
                    
            text = openxmllib.openXmlDocument(path='./tmp/text.docx')

            g[4] = text.extendedProperties['Pages']
        
         
        if (g[3] == '+'):
            with requests.get('http://gitwork.ru/api/v4/projects/' + g[7] + '/repository/files/' + g[8][0]+ '/raw?ref=master&access_token=' + token) as rq:
                with open('./tmp/result.pptx', 'wb') as file:
                    file.write(rq.content)    
        
            presentation = openxmllib.openXmlDocument(path='./tmp/result.pptx')
            g[3] = presentation.extendedProperties['Slides']
       
    f = open('./tmp/output.csv', 'w')
    f.write(';readme.md;result.docx;result.pptx;text.docx;project;size;\n')
    for g in glob_list:
        f.write(g[0] + ';')
        f.write(g[1].__str__() + ';')
        f.write(g[2].__str__() + ';')
        f.write(g[3].__str__() + ';')
        f.write(g[4].__str__() + ';')
        f.write(g[5].__str__() + ';')
        f.write(g[6] + ';')
        f.write('\n')
            
        
        
    return glob_list
    
    
