from typing import Dict
import requests as req
from flask import Flask, jsonify, redirect, url_for, request    
import uuid
#import json
from pprint import pprint

app = Flask(__name__)



header = {'User-Agent': 'RedTek',}


headers_g = {"":{}}


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
        return redirect('<id>/<r>/""')


@app.route('/api/<id>/<r>/<last>', methods=['GET'])
def get_r_content(last, id, r):
        ret = []
        if (r == "best") or (r == "hot") or (r == "new") or (r == "top") :
                buff = req.get('https://oauth.reddit.com/' + r, headers=headers_g[id], params={"limit":"200","after":last})
        else: 
                buff = req.get('https://oauth.reddit.com/r/' + r, headers=headers_g[id], params={"limit":"200","after":last})
        for post in buff.json()['data']['children']:
                if not (".imgur" in post['data']['url']):
                        if (post['data']['is_video'] == True):
                                ret.append({
                                "type":"video",
                                'url':str(post['data']['media']['reddit_video']['fallback_url']).split("?", -1)[0],
                                'author':post['data']['author'],
                                'permalink':str(post['data']['permalink']).split("/r/")[1].split("/")[0],
                                'title':post['data']['title'],
                                'id':last,
                                'selftext':post['data']['selftext'],
                                })
                        elif (".jpg" in post['data']['url']) or  (".png" in post['data']['url']) or (".gif" in  post['data']['url']):
                                ret.append({
                                "type":"image",
                                'url':post['data']['url'],
                                'author':post['data']['author'],
                                'permalink':str(post['data']['permalink']).split("/r/")[1].split("/")[0],
                                'title':post['data']['title'],
                                'id':last,
                                'selftext':post['data']['selftext'],
                                })
                        #elif ("redd" in post['data']['url']):
                        else:
                                ret.append({
                                "type":"Unspecified",
                                'url':post['data']['url'],
                                'author':post['data']['author'],
                                'permalink':str(post['data']['permalink']).split("/r/")[1].split("/")[0],
                                'title':post['data']['title'],
                                'id':last,
                                'selftext':post['data']['selftext'],
                                })        
                        last = post['kind'] + '_' + post['data']['id']
        return jsonify(ret)


if __name__ == "__main__":
        app.run("0.0.0.0", 8081, debug=True)
        #app.run("127.0.0.1", 8081, debug=True)