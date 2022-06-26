import sqlite3

from flask import Flask, render_template, redirect, request, g, session

app = Flask(__name__)
app.secret_key="hXDm8NXqqJATH&7XHW6AtM.XEqM4cEMn"

def get_db():
  if 'db' not in g:
    #データベースをオープンしてFlaskのグローバル変数の保存
    g.db = sqlite3.connect("UserDB.db")
  return g.db


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
  #データベースを開く
  con = get_db()
  #テーブル「ユーザー情報」の有無を確認
  cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='ユーザー情報'")

  for row in cur:
    if row[0] == 0:
      #テーブル「ユーザー情報」がなければ作成する
      cur.execute("CREATE TABLE ユーザー情報(ID VARCHAR(10) PRIMARY KEY, name VARCHAR(40), password VARCHAR(20))")
      #レコードを作る
      cur.execute(
        """INSERT INTO ユーザー情報(ID, name, password)
        values('1', '田中太郎', '1234'),
        ('2', '大阪花子', '12345')"""
      )
      con.commit()
  
  #ユーザー情報を読み込み
  cur = con.execute("select * from ユーザー情報 order by ID")
  data = cur.fetchall()
  session['data'] = data
  con.close()
  return render_template('index.html')


@app.route('/index', methods=['POST'])
def result_post():
  #テンプレートからログインするIDとpassを取得
  id = str(request.form["id"])
  pwd = str(request.form["pwd"])
  
  #セッションからデータを取得
  data = session['data']

  for user in data:
    if user[0] == id:
      if user[2] == pwd:
        session['user'] = user
        return render_template("main.html", name=user[1])
      else:
        return render_template("index.html", errMsg2 = "パスワードが正しくありません")
  return render_template("index.html", errMsg1 = "IDが正しくありません")


@app.route('/register', methods=['POST'])
def register():
  #テンプレートから新規登録するIDと名前とpassを取得
  id = str(request.form["id"])
  name = str(request.form["name"])
  pwd = str(request.form["pwd"])

  data = session['data']
  for user in data:
    if user[0] == id:
      return render_template("register.html", errMsg = "そのIDはすでに使用されています")

  #データベースを開く
  con = get_db()
 
  #登録処理
  sql = "INSERT INTO ユーザー情報(ID, name, password) values('{}', '{}', '{}')".format(id, name, pwd)
  con.execute(sql)
  con.commit()

  return render_template("result.html", id=id, name=name, pwd=pwd)


@app.route('/register', methods=['GET'])
def move():
  return render_template("register.html")

@app.route('/main', methods=['GET'])
def update():


  if "user" not in session:
    return redirect("/")
  user = session["user"]

  #
  #ここに更新時の処理を記述
  #
  return render_template("main.html", name=user[1])


@app.route('/main', methods=['POST'])
def tweet():
  #
  #つぶやき時の処理を記述
  #
  return render_template("main.html")

@app.route('/logout', methods=['GET'])
def logout():
  #セッションの削除
  session.pop('user', None)
  return redirect('/')

if __name__ == '__main__':
  app.debug = True
  app.run(host='localhost')