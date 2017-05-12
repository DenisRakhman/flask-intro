from flask import Flask
import collections as cl
from flask import url_for, render_template, request, redirect
app = Flask(__name__)
from pymystem3 import Mystem
m = Mystem()
import json
import requests

def parse(text):
    lemmas = m.lemmatize(text)
    verbs = []
    out = {'pfv': 0, 'ipfv': 0, 'trans': 0, 'intrans': 0}
    for l in m.analyze(text):
        try:
            # print (l)
            if 'analysis' in l:
                pr = l['analysis'][0]
                if pr['gr'].split(',')[0] == 'V':
                    verbs.append(pr['lex'])
                    # print (pr.split(',')[1])
                    if 'нп=' in pr['gr']:
                        out['intrans'] += 1
                    else:
                        out['trans'] += 1
                    if 'сов' in pr['gr'].split(','):
                        out['pfv'] += 1
                    else:
                        out['ipfv'] += 1
        except:
            continue
    freqlist = sorted(cl.Counter(verbs), key=cl.Counter(verbs).get, reverse=True)
    out['freqlist'] = freqlist
    out['verbnumber'] = str(len(verbs))
    out['verbpercent'] = str(len(verbs) / len(lemmas))
    return out

def verbs():
    import datetime
    import collections as cl
    from flask import Flask
    from flask import url_for, render_template, request, redirect
    import re
    from pymystem3 import Mystem
    m = Mystem()
    app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/verbs')
def index():
    if request.args:
        text = request.args['text']
        out = parse(text)
        # return redirect(url_for('result'))
        return render_template('main_hw2.html', out=out, text=text, verbnumber=out['verbnumber'],
                               verbpercent=out['verbpercent'], trans=out['trans'], intrans=out['intrans'],
                               pfv=out['pfv'], ipfv=out['ipfv'], freqlist=out['freqlist'])
    return render_template('main_hw2.html')

@app.route('/vk')
def vk():
    if request.args:
        domain = request.args['id']
        def get_page(domain, number = 100):
            response = requests.get('http://api.vk.com/method/wall.get?domain='+domain+'&count='+str(number))
            if 'error' in response.text:
                if json.loads(response.text)['error']['error_code'] == 100:
                    response = requests.get('http://api.vk.com/method/wall.get?owner_id=-'+(domain[4:])+'&count='+str(number))
            if 'error' in response.text:
                if json.loads(response.text)['error']['error_code'] == 15:
                    return 'forbidden'
            return response

        response = get_page(domain)
        if response == 'forbidden':
            return render_template('vk_comments.html', allowed = 0)
        print (response.text)
        data = json.loads(response.text)
        print (data)
        print(type(data))
        posts = [post for post in data['response'] if type(post) != "<class 'int'>"]
        posts = data['response']
        print(posts)
        commentators_scores = {}
        print (len(posts))

        for post in posts:
            if type(post) != int:
                #print (post['id'])
                curpost = json.loads(requests.get('http://api.vk.com/method/wall.getComments?owner_id=' + str(post['from_id']) + '&post_id=' + str(post['id'])).text)
                #print (curresp)
                for com in curpost['response']:
                    if type(com) != int:
                        #commentators.append(str(com['from_id']))
                        if str(com['from_id']) in commentators_scores:
                            commentators_scores[str(com['from_id'])] += 1
                        else:
                            commentators_scores[str(com['from_id'])] = 1


        def get_names(ids):
            response = json.loads(requests.get('http://api.vk.com/method/users.get?user_ids=' + ','.join(ids)).text)
            return {user['uid'] : user['first_name'] + ' ' + user['last_name']  for user in response['response']}

        commentators_names = get_names([uid for uid in commentators_scores])

        uids = sorted(cl.OrderedDict(commentators_scores), key = cl.Counter(commentators_scores).get, reverse = 1)
        new = cl.OrderedDict({})
        for u in uids:
            new[u] = commentators_scores[u]
        commentators_scores = new
        print(commentators_scores)
        com_names_scores = [commentators_names[int(uid)] + ' - '  + str(commentators_scores[str(uid)]) for uid in commentators_scores if int(uid) in commentators_names]
        for i in com_names_scores:
            print(i)

        return render_template('vk_comments.html', allowed = 1, com_names_scores = com_names_scores)

    else:
        return render_template('vk_comments.html')

if __name__ == '__main__':
    app.run(debug=True)