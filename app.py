from flask import Flask, render_template, request, redirect
from passlib.hash import sha256_crypt
from data import Articles
import pymysql

app = Flask(__name__)

app.debug = True # 오류를 웹페이지 상에 보여주는 세팅 (베포할떈 False)

db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)

cursor = db.cursor()

# 클라이언트가 http://localhost:5000/data 으로 get방식으로 요청들어왔을떄 hello world 문구를 리턴해 본다

@app.route('/', methods = ['Get']) #데코레이터 /data 는 요청들어왔을때 저경로로 중계준다는 말
def index():#이름 아무거나 해도됨
    # return "hello world"
    return render_template("index.html", data='kim') # template 파일아래를 찾아 클라이언트에게 파일이 아닌 문서로 해석한다음 보낸다.
    # render_template 첫번쨰 인짜 ; 파일, 두번쨰 인자 : data 값
    # render_template 가 하는일 html 안에 파이썬문법 해석해줌 그리고 클라이언트에게 결과값을 보내줌 이능력을 엔진이라하고 그엔진명은 진자2라고 함 플라스크안에 내장되어있음

@app.route('/about')
def about():
    return render_template('about.html',hello = "Gary Kim")

@app.route('/articles')
def articles():
    cursor = db.cursor()
    sql = 'SELECT * FROM topic;'
    cursor.execute(sql)
    # 여러줄 사용할 것이니 fetchAll()사용
    topics = cursor.fetchall()
    print(topics)
    # articles = Articles()
    # print(articles[0]['body'])
    return render_template('articles.html', articles = topics)

@app.route('/article/<int:id>') #/<id> 는 params 임 이걸 써먹을것임 (int만)
def article(id): # params 에 있던 id값임 python 이 알아서 넣어줌
    cursor = db.cursor()
    sql = f'SELECT * FROM topic WHERE id = {id};'
    cursor.execute(sql)
    # 한줄만출력하니 fetchone() 함수 사용
    topic = cursor.fetchone()
    print(topic)
    # articles = Articles()
    # article = articles[id-1]
    # print(articles[id-1])
    return render_template("article.html", article = topic)

@app.route('/add_articles', methods=["GET","POST"])
def add_articles():
    cursor = db.cursor()
    if request.method == 'POST':
        sql_3 = "INSERT INTO `topic` (`title`, `body`, `author`) VALUES (%s, %s, %s);"
        
        desc = request.form['desc']
        title = request.form['title']
        author = request.form['author']
        input_data = [title,desc,author ]

        print(request.form)
        cursor.execute(sql_3,input_data)
        db.commit()
        print("몇번째 줄일까?",cursor.rowcount)
        # db.close() 오류나서걍 주석처리함
        return redirect("/articles")
    else:
        return render_template("add_articles.html")

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor = db.cursor()
    sql = f'DELETE FROM topic WHERE id = {id};'
    print("sql")
    cursor.execute(sql)
    db.commit()
    return redirect("/articles")

@app.route('/<int:id>/edit', methods=['POST','GET'])
def edit(id):
    cursor = db.cursor()
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        sql = f"UPDATE topic SET title = '{title}', body = '{desc}' WHERE (id = {id});"
        cursor.execute(sql)
        db.commit()
        return redirect("/articles")
    else:   
        sql = f'SELECT * FROM topic WHERE id={id};'
        # print("sql")
        cursor.execute(sql)
        topic = cursor.fetchone()
        # print(topic)
        # db.commit()
        return render_template("article_edit.html",article = topic)

@app.route('/register', methods=['POST','GET'])
def register():
    cursor = db.cursor()
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = sha256_crypt.encrypt(request.form['password'])
        value_lsit = [name, email, username, password]
        sql =f"INSERT INTO users (`name`, `email`, `username`, `password`) VALUES ('{name}', '{email}', '{username}', '{password}');"
        print(sql)
        cursor.execute(sql)
        db.commit()
        return redirect("/user_list")

@app.route('/user_list', methods=['POST','GET'])
def user_list():
    cursor = db.cursor()
    if request.method == "POST":
        return "/user_list -> post"
    else:   
        sql = 'SELECT * FROM users;'
        cursor.execute(sql)
        users = cursor.fetchall()
        print(users)
        return render_template("user_list.html",users = users)



@app.route('/login', methods=['POST','GET'])
def login():
    cursor = db.cursor()
    if request.method == "POST":
        # name = request.form['name']
        email = request.form['email']
        # username = request.form['username']
        get_password = request.form['password']
        print(email, get_password)
        sql = f"SELECT * FROM users WHERE email = '{email}';"        
        cursor.execute(sql)
        user = cursor.fetchone()
        print(user)
        if user == None :
            print(user)
            return redirect("/register")
        else:
            if sha256_crypt.verify(get_password, user[4]):
                return redirect("/articles")
            return render_template("login.html")
    else:   
        return render_template("login.html")
        
# app.py 파일을 가장 먼저 실행하겠다라는 내용 (그중 이줄부터 실행할것이란 소리)
if __name__ == '__main__':
    app.run() # 애가 서버 실행시켜줌

# 서버 키려먼 이프로그램 실행하고 
# 서버 끄려면 이 프로그램 끄면 된다. -> citr + c




