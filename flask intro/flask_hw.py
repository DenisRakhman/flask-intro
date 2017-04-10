import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect
import re

app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        name = request.args['name']
        dog = 'да' if 'dog' in request.args else 'нет'
        cat = 'да' if 'cat' in request.args else 'нет'
        file = open('data.txt', 'a', encoding='utf-8')
        file.write(name + ' dog=' + dog + ' cat=' + cat + '\n')
        file.close()
        return redirect(url_for('result'))
    return render_template('main_hw.html')

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





if __name__ == '__main__':
    app.run(debug=True)
