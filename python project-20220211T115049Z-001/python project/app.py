from flask import Flask, render_template, redirect, request, url_for
import sqlite3 
from cs50 import SQL

app = Flask(__name__)


#db = SQL("sqlite:///store.db")

db = SQL("sqlite:///store.db")


Q1 = {'Red', 'Green', 'Blue', 'Orange'}
@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template('sample.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    #conn = sqlite3.connect('store.db')
    #cur = conn.cursor()
    #error = None
    if request.method =='POST':
        global user
        user = request.form.get('username').strip()
        passw = request.form.get('password').strip()
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        #fuser = db.execute("SELECT username FROM login WHERE username = (?)", [user])
        c.execute("SELECT username FROM login WHERE username =?", (user,))
        c.execute("INSERT INTO quest (username) VALUES (?)", (user,))
        c.execute("INSERT INTO quest1 (username) VALUES (?)", (user,))
        c.execute("INSERT INTO quest2 (username) VALUES (?)", (user,))
        c.execute("INSERT INTO quest3 (username) VALUES (?)", (user,))
        work = c.fetchone() 
        conn.commit()
        conn.close()
        if (user == "" and passw == "") or (user == "" or passw == ""):
            return redirect('/')
        else:
            users = [user]
            insert_q = "INSERT INTO login (username,password) VALUES (?,?)"
            for use in users:
                db.execute(insert_q, user, passw)  
            return redirect('/success')

    #db.execute()
    #cur.execute(''' INSERT INTO login ''' + user + ''' = ? WHERE password = ?''', (user, password))
    #cur.execute("INSERT INTO login (username) VALUES (?)", (user,))
    #cur.execute("INSERT INTO login (password) VALUES (?)", (passw,))

@app.route('/login',methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    error = None
    #global use = request.form.get('username')
    user = request.form.get('username')
    passw = request.form.get('password')
    #fuser = db.execute("SELECT username FROM login WHERE username = (?)", [user])
    c.execute("SELECT password FROM login WHERE username =?", (user,))
    work = c.fetchone() 
    c.execute("SELECT rowid FROM login WHERE username =?", (user,))
    num = c.fetchone() 
    conn.commit()
    conn.close()
    if (user == "" and passw == "") or (user == "" or passw == "") or user != work:
            return redirect('/')
    else:
        if request.method =='POST':
            if passw != work[0]:
                error = "Invalid username or password. Try again"
            else:
                return redirect('/success')
    return render_template('log.html', error=error)

@app.route('/success', methods=["GET", "POST"])
def success():
    i = 0
    quest = ["q1", "q2", "q3", "q4"]
    if request.method =='POST':
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        color = request.form.get('question1')
        col = [color, user]
        #query = "UPDATE login SET q1=? WHERE username=?"
        #for co in color:
        #cur.execute("UPDATE SEN_Table SET SenNumber = ? WHERE FormName = ?", (senNumStr, nameGroup))
        c.execute("UPDATE quest SET q1 = ? WHERE username = ?", (str(color), str(user),))
        print("UPDATE quest SET q1 = ? WHERE username = ?", (str(color), str(user),))
        i += 1
        conn.commit()
        conn.close()
        return redirect('/q2')
    return render_template('qpage.html')

@app.route('/q2', methods=["GET", "POST"])
def q2():
    if request.method =='POST':
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        color = request.form.get('question2')
        col = [color, user]
        #query = "UPDATE login SET q1=? WHERE username=?"
        #for co in color:
        #cur.execute("UPDATE SEN_Table SET SenNumber = ? WHERE FormName = ?", (senNumStr, nameGroup))
        c.execute("UPDATE quest1 SET q2 = ? WHERE username = ?", (str(color), str(user),))
        conn.commit()
        conn.close()
        return redirect('/q3')
    return render_template('qpage2.html')

@app.route('/q3', methods=["GET", "POST"])
def q3():
    if request.method =='POST':
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        color = request.form.get('question3')
        col = [color, user]
        #query = "UPDATE login SET q1=? WHERE username=?"
        #for co in color:
        #cur.execute("UPDATE SEN_Table SET SenNumber = ? WHERE FormName = ?", (senNumStr, nameGroup))
        c.execute("UPDATE quest2 SET q3 = ? WHERE username = ?", (str(color), str(user),))
        conn.commit()
        conn.close()
        return redirect('/q4')
    return render_template('qpage3.html')

@app.route('/q4', methods=["GET", "POST"])
def q4():
    if request.method =='POST':
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        color = request.form.get('question4')
        col = [color, user]
        #query = "UPDATE login SET q1=? WHERE username=?"
        #for co in color:
        #cur.execute("UPDATE SEN_Table SET SenNumber = ? WHERE FormName = ?", (senNumStr, nameGroup))
        c.execute("UPDATE quest3 SET q4 = ? WHERE username = ?", (str(color), str(user),))
        conn.commit()
        conn.close()
        return redirect('/admin')
    return render_template('qpage4.html')   

@app.route('/admin', methods=['GET','POST'])
def admin():
    #if request.method =='POST':
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    col = c.execute("SELECT COUNT(*) FROM quest WHERE q1='Relaxed'")
    num = col.fetchone()
    div = c.execute("SELECT COUNT(*) FROM quest")
    divid = div.fetchone()  
    col1 = c.execute("SELECT COUNT(*) FROM quest WHERE q1='Spend time in Gaming'")
    num1 = col1.fetchone()
    col2 = c.execute("SELECT COUNT(*) FROM quest WHERE q1='Read novels'")
    num2 = col2.fetchone()
    col3 = c.execute("SELECT COUNT(*) FROM quest WHERE q1='All of the above'")
    num3 = col3.fetchone()

    res = float(num[0]/divid[0])*100
    print(res)
    res = round(res)

    res1 = float(num1[0]/divid[0])*100
    print(res1)
    res1 = round(res1)

    res2 = float(num2[0]/divid[0])*100
    print(res2)
    res2 = round(res2)

    res3 = float(num3[0]/divid[0])*100
    print(res3)
    res3 = round(res3)
    
    div1 = c.execute("SELECT COUNT(*) FROM quest1")
    divid1 = div1.fetchone() 
    q = c.execute("SELECT COUNT(*) FROM quest1 WHERE q2='Relaxed'")
    work = q.fetchone()
    q1 = c.execute("SELECT COUNT(*) FROM quest1 WHERE q2='Less excited'")
    work1 = q1.fetchone()
    q2 = c.execute("SELECT COUNT(*) FROM quest1 WHERE q2='More excited'")
    work2 = q2.fetchone()
    q3 = c.execute("SELECT COUNT(*) FROM quest1 WHERE q2='Same'")
    work3 = q3.fetchone()

    resp = float(work[0]/divid1[0])*100
    print(resp)
    resp = round(resp)

    resp1 = float(work1[0]/divid1[0])*100
    print(resp1)
    resp1 = round(resp1)

    resp2 = float(work2[0]/divid1[0])*100
    print(resp2)
    resp2 = round(resp2)

    resp3 = float(work3[0]/divid1[0])*100
    print(resp3)
    resp3 = round(resp3)

    div2 = c.execute("SELECT COUNT(*) FROM quest2")
    divid2 = div2.fetchone() 
    que = c.execute("SELECT COUNT(*) FROM quest2 WHERE q3='Want to Socialize again'")
    work = que.fetchone()
    que1 = c.execute("SELECT COUNT(*) FROM quest2 WHERE q3='I like living like this'")
    work1 = que1.fetchone()
    que2 = c.execute("SELECT COUNT(*) FROM quest2 WHERE q3='Maybe, not sure'")
    work2 = que2.fetchone()
    que3 = c.execute("SELECT COUNT(*) FROM quest2 WHERE q3='Other'")
    work3 = que3.fetchone()

    iss = float(work[0]/divid2[0])*100
    print(iss)
    iss = round(iss)

    iss1 = float(work1[0]/divid2[0])*100
    print(iss1)
    iss1 = round(iss1)

    iss2 = float(work2[0]/divid2[0])*100
    print(iss2)
    iss2 = round(iss2)

    iss3 = float(work3[0]/divid2[0])*100
    print(iss3)
    iss3 = round(iss3)
    
    div3 = c.execute("SELECT COUNT(*) FROM quest3")
    divid3 = div3.fetchone() 
    query = c.execute("SELECT COUNT(*) FROM quest3 WHERE q4='Peace'")
    done = query.fetchone()
    query1 = c.execute("SELECT COUNT(*) FROM quest3 WHERE q4='Achievement'")
    done1 = query1.fetchone()
    query2 = c.execute("SELECT COUNT(*) FROM quest3 WHERE q4='Work'")
    done2 = query2.fetchone()
    query3 = c.execute("SELECT COUNT(*) FROM quest3 WHERE q4='Happiness'")
    done3 = query3.fetchone()

    response = float(done[0]/divid3[0])*100
    print(response)
    response = round(response)

    response1 = float(done1[0]/divid3[0])*100
    print(response1)
    response1 = round(response1)

    response2 = float(done2[0]/divid3[0])*100
    print(response2)
    response2 = round(response2)

    response3 = float(done3[0]/divid3[0])*100
    print(response3)
    response3 = round(response3)
    conn.commit()
    conn.close()
    return render_template('pbl.html', num1 = res, num2 = res1, num3 = res2, num4 = res3, num5 = resp, num6 = resp1, num7 = resp2, num8 = resp3, num9 = iss, num10 = iss1, num11 = iss2, num12 = iss3, num13 = response, num14= response1, num15 = response2, num16 = response3)
    
    




    
        
