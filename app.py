import requests as req
from flask import Flask, jsonify, redirect, url_for, request
#import json
from pprint import pprint

app = Flask(__name__)



header = {'User-Agent': 'RedTek'}

global headers


#buff = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
#print(buff.json()) 



#buff = req.get('https://oauth.reddit.com/best', headers=headers, params={"limit":"100","after":after})
#for post in buff.json()['data']['children']:
#        #if (".jpg" in post['data']['url'] ):
#        pprint(post, indent=4, sort_dicts=True)
#        #print(post['data']['url'])
#        #print(post['data']['author'])
#        #print(post['data']['permalink'])
#        #print(post['data']['title'])
#        #print("\n\n\n")
#        after = post['kind'] + '_' + post['data']['id']
#
#buff = req.get('https://oauth.reddit.com/best', headers=headers, params={"limit":"100", "after":after})
#for post in buff.json()['data']['children']:
#        if (".jpg" in post['data']['url'] ):
#                #pprint(post, indent=4, sort_dicts=True)
#                pprint(post['data']['url'], indent=4, sort_dicts=True)
#res = req.get("https://oauth.reddit.com/r/python/hot",
#                   headers=headers)
#
#print(res.json()) 
#after = ""


@app.route('/myapi/oath/<tok>', methods=['GET'])
def get_oath(tok):
        global headers
        headers = {**header, **{'Authorization': f"bearer {tok}"}}
        buff = req.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        pprint(buff.json())
        return jsonify( buff.json()['name'])


@app.route('/myapi/best', methods=['GET'])
def get_bestt():
        return redirect('best/""')

@app.route('/myapi/best/<last>', methods=['GET'])
def get_best(last):
        global headers
        ret = []
        while len(ret) < 35 :
                buff = req.get('https://oauth.reddit.com/best', headers=headers, params={"limit":"100","after":last})
                for post in buff.json()['data']['children']:
                        if (".jpg" in post['data']['url'] ):
                                ret.append({
                                'url':post['data']['url'],
                                'author':post['data']['author'],
                                'permalink':post['data']['permalink'],
                                'title':post['data']['title'],
                                'id':last
                                })
                                last = post['kind'] + '_' + post['data']['id']
        return jsonify(ret)

if __name__ == "__main__":
        app.run("0.0.0.0", 8081, debug=True)