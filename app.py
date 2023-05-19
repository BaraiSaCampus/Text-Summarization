from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from gene import generate
from bs4 import BeautifulSoup
import requests
import datetime
import csv
import os
from en_decode import encode,decode

app = Flask(__name__)
app.secret_key = 'mysecretkey'
logs = []


def get_users():
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        users = {row['username']: row['password'] for row in reader}
    return users


def add_user(username, password):
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])


users = get_users()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = encode(request.form['password'])
        if username in users and users[username] == password:
            logs.append((username, datetime.datetime.now()))
            with open('login_log.txt', 'a') as f:
                f.write('{} 登录于 {}\n'.format(username, datetime.datetime.now()))
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists')
        else:
            add_user(username, encode(password))
            users[username] = encode(password)
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            text1 = request.form['text']
            text2 = generate(text1)
            path = r'D:\\flaskProject\\history\\'
            filename = path + text2
            with open(filename, 'w') as f:
                f.write(text1)
            return render_template('index.html', text=text2)
        else:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/history')
def history():
    # files = [f for f in os.listdir('.') if f.endswith('.txt')]
    path = r'D:\\flaskProject\\history\\'
    dirs = os.listdir(path)
    files = [f for f in dirs]
    return render_template('history.html', files=files)


@app.route('/history/<filename>')
def view(filename):
    with open(r'D:\\flaskProject\\history\\' + filename, 'r') as f:
        text = f.read()
        return render_template('view.html', filename=filename, text=text)


@app.route('/news')
def news():
    url = 'https://news.sina.com.cn/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.select('div#syncad_1 a')
    news_list = []
    for n in news:
        title = n.string
        link = n['href']
        try:
            response = requests.get(link)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.select_one('div#article p').get_text()
            paragraphs = soup.select('div#article p')
            content1 = ''.join([p.get_text() for p in paragraphs])
            if len(content1) < 40:
                pass
            else:
                content = generate(content1)
                path = r'D:\\flaskProject\\history\\'
                filename = path+content
                with open(filename, 'w') as f:
                    f.write(content1)
                news_list.append((title, content, link))
        except:
            pass
        # news_list.append((title, content, link))
    return render_template('news.html', news_list=news_list)


@app.route('/admin', methods=['GET'])
def admin():
    if 'username' in session and session['username'] == 'tE9foq6YE7NCQq9ziXKOrg==':
        users = get_users()
        logs.append(('admin', datetime.datetime.now()))
        with open('login_log.txt', 'a') as f:
            f.write('{} 登录于 {}\n'.format('admin', datetime.datetime.now()))
        return render_template('admin.html', users=users)
    else:
        return render_template('index.html', error='No Permission!')
        # return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

####代码片段备份区
# def index():
#     url = 'https://news.sina.com.cn/'
#     response = requests.get(url)
#     response.encoding = 'utf-8'
#     soup = BeautifulSoup(response.text, 'html.parser')
#     news = soup.select('div#syncad_1 a')
#     news_list = []
#     for n in news:
#         title = n.string
#         link = n['href']
#         try:
#             response = requests.get(link)
#             response.encoding = 'utf-8'
#             soup = BeautifulSoup(response.text, 'html.parser')
#             content = soup.select_one('div#article p').get_text()
#             paragraphs = soup.select('div#article p')
#             content = ''.join([p.get_text() for p in paragraphs])
#         except:
#             pass
#         news_list.append((title, content, link))
#     return render_template('news.html', news_list=news_list)
