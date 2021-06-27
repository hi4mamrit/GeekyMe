"""
REST API to find links of recently unanswered python/java/unix questions in stackOverflow

###How to Call:-
python consume_rest_api.py --language=python --que
python consume_rest_api.py -l=unix -q
python consume_rest_api.py -l=java -q
python consume_rest_api.py --help

###Output:-
C:\Users\amrikuma>python consume_rest_api.py -l=python -q

Connecting:  http://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow
Established..
Parsing...

Searching for tag:  python

Python Un-answered links:-
https://stackoverflow.com/questions/68153275/why-is-there-no-difference-between-variables-in-python
https://stackoverflow.com/questions/68153211/allow-your-bot-to-read-multiple-values-of-a-variable-in-discord-py
"""

import requests,argparse,sys

g_language = ''
g_api_link = "http://api.stackexchange.com"
g_so_dict ={'que': '/2.2/questions?order=desc&sort=activity&site=stackoverflow'}


def parse_arguments():
    global g_language,g_api_link
   
    argparser = argparse.ArgumentParser(description='A tool to find links of recently unanswered python(default) questions in stackOverflow')    
    argparser.add_argument('--language' ,'-l' , default='python' ,\
                           help='e.g -l=python .Questions related to which language. Default is Python')
    argparser.add_argument('--que', '-q', dest='i_que', action='store_true' ,help='Option to support questions only....Mandatory')    
    v_args = argparser.parse_args()
    
    g_language=v_args.language
    if v_args.i_que:
        g_api_link = g_api_link + g_so_dict['que']
    else:
        print("Please select -q as well. Exiting ...\n")
        sys.exit(1)


def f_na_language(p_list,p_language):
    #Takes list as input , iterates over it filtering 'interested' tags and resturns the list of links as result
    
    v_list= list()
    v_language = p_language.lower()
    
    for item in p_list:
        if not bool(item['is_answered']) and (v_language in [x.lower() for x in item['tags']]):
            v_list.append(item['link'])
    
    return v_list


def main():
    #Main Program
    
    parse_arguments()    
    print ("Connecting: " ,g_api_link)    
    response = requests.get(g_api_link)
    i_list = response.json()['items']    

    print ("Established..\nParsing...\n")
    print("Searching for tag: ", g_language)    
    ans_list =f_na_language(i_list,g_language)

    print('\n'+g_language.capitalize() ,'Un-answered links:-')
    print(*ans_list,sep='\n')
    
    
if __name__ == '__main__':
    main()
