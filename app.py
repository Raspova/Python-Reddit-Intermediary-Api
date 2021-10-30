from typing import Dict
import requests as req
from flask import Flask, jsonify, redirect, url_for, request    
import uuid
#import json
from pprint import pprint

app = Flask(__name__)



header = {'User-Agent': 'RedTek',}


headers_g = {"":{}}


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


@app.route('/api/oath/<tok>', methods=['GET'])
def get_oath(tok):
        global headers_g
        header_buff = {**header, **{'Authorization': f"bearer {tok}"}}
        buff = req.get('https://oauth.reddit.com/api/v1/me', headers=header_buff)
        pprint(buff.json())
        header_buff = {str(buff.json()['name']):header_buff}
        headers_g = header_buff
        print(headers_g)
        banner =  str(buff.json()['subreddit']['banner_img'])
        icon =  str(buff.json()['subreddit']['icon_img'])
        return jsonify( {"name":buff.json()['name'],
                        "description":buff.json()['subreddit']['public_description'],
                        "icon":icon.split("?", -1)[0],
                        "banner":banner.split("?", -1)[0]})


@app.route('/api/<id>/<r>', methods=['GET'])
def get_bestt():
        return redirect('<id>/best/""')


@app.route('/api/<id>/<r>/<last>', methods=['GET'])
def get_r_content(last, id, r):
        ret = []
        while len(ret) < 35 :
                buff = req.get('https://oauth.reddit.com/r/' + r, headers=headers_g[id], params={"limit":"100","after":last})
                for post in buff.json()['data']['children']:
                        if ((".jpg" in post['data']['url'] )
                        and not (".imgur" in post['data']['url'] )):
                                ret.append({
                                'url':post['data']['url'],
                                'author':post['data']['author'],
                                'permalink':post['data']['permalink'],
                                'title':post['data']['title'],
                                'id':last
                                })
                                last = post['kind'] + '_' + post['data']['id']
        return jsonify(ret)

@app.route('/api/<id>/best/<last>', methods=['GET'])
def get_best(last, id):
        ret = []
        while len(ret) < 35 :
                buff = req.get('https://oauth.reddit.com/best', headers=headers_g[id], params={"limit":"100","after":last})
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
        #app.run("127.0.0.1", 8081, debug=True)