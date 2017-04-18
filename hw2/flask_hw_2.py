import datetime
import collections as cl
from flask import Flask
from flask import url_for, render_template, request, redirect
import re
from pymystem3 import Mystem
m = Mystem()
app = Flask(__name__)

def parse(text):
    lemmas = m.lemmatize(text)
    verbs = []
    out = {'pfv':0, 'ipfv':0, 'trans':0, 'intrans':0}
    for l in m.analyze(text):
        try:
        #print (l)
            if 'analysis' in l:
                pr = l['analysis'][0]
                if pr['gr'].split(',')[0] == 'V':
                    verbs.append(pr['lex'])
                    #print (pr.split(',')[1])
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
    freqlist = sorted(cl.Counter(verbs),  key = cl.Counter(verbs).get, reverse = True)
    out['freqlist'] = freqlist
    out['verbnumber'] = str(len(verbs))
    out['verbpercent'] = str(len(verbs)/len(lemmas))
    return out



@app.route('/')
def index():
    if request.args:
        text = request.args['text']
        out = parse(text)
        #return redirect(url_for('result'))
        return render_template('main_hw2.html', out = out, text = text, verbnumber = out['verbnumber'], verbpercent = out['verbpercent'], trans = out['trans'], intrans = out['intrans'], pfv = out['pfv'], ipfv = out['ipfv'], freqlist = out['freqlist'])
    return render_template('main_hw2.html')
'''
@app.route('/result')
def result():
    file  = open ('data.txt', 'r', encoding = 'utf-8')
    text = file.read()
    cat_sum = len(re.findall('cat=да', text, flags=re.DOTALL))
    dog_sum = len(re.findall('dog=да', text, flags=re.DOTALL))
    out = 'коты: ' + str(cat_sum) + '<br> собаки:' + str(dog_sum) +'<br>'
    people = {}
    for line in text.split('\n'):
        try:
            if line.split()[0] in people:
                people[line.split()[0]] += 1
            else:
                people[line.split()[0]] = 1
        except:
            continue
    for person in people:
        out = out + '<br>' + person + ' ' + str(people[person])
    print(out)
    return render_template('result.html', data = out.split('<br>'))

@app.route('/hi')
@app.route('/hi/<user>')
def hi(user=None):
    if user is None:
        user = 'friend'
    return '<html><body><p>Привет, ' + user + '!</p></body></html>'




'''
if __name__ == '__main__':
    app.run(debug=True)
