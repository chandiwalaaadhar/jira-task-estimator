from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response, session, flash
import sqlite3

app=Flask(__name__)
app.secret_key = b'enter your key' 

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        conn = sqlite3.connect('main.db')
        conn.execute("DROP TABLE IF EXISTS TASK_MASTER")
        conn.execute('''CREATE TABLE IF NOT EXISTS TASK_MASTER
        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME           TEXT     NOT NULL,
        POINTS          INT     NOT NULL);''')
    
        query="INSERT INTO TASK_MASTER (ID,NAME,POINTS) VALUES (?,?,?);"
        data=('0',task_name,0)
        conn.execute(query,data)
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    if request.method == 'GET':
        conn = sqlite3.connect('main.db')   
        query="SELECT NAME FROM TASK_MASTER WHERE POINTS IS 0;"
        query1="SELECT * FROM TASK_MASTER WHERE POINTS IS NOT 0;"
        query2="SELECT AVG(POINTS) FROM TASK_MASTER WHERE POINTS IS NOT 0"
        result=conn.execute(query).fetchall()
        result1=conn.execute(query1).fetchall()
        result2=conn.execute(query2).fetchall()
        conn.close()
        return render_template('admin.html', result=[result1,result2, result])
        

    
 

        
@app.route('/user', methods=['GET','POST'])
def user():
    if request.method == 'GET':
        conn = sqlite3.connect('main.db')
        task_name=conn.execute("SELECT NAME FROM TASK_MASTER WHERE ID = '0';").fetchall()
        conn.close()
        return render_template('user.html', result=task_name[0])


    if request.method == 'POST':
        try:
            points = float(request.form.get('points'))
            name = request.form.get('name')
            conn = sqlite3.connect('main.db')
            query="INSERT INTO TASK_MASTER (NAME, POINTS) VALUES (?,?);"
            data=(name,points)
            conn.execute(query,data)
            conn.commit()
            conn.close()
            message="Vote Added Succesfully"
        except:
            message="Can't process the Vote. Enter a Numeric Value!!"
            
        flash(message)
        return redirect(url_for('user'))
    


if __name__ == "__main__":
    app.run()
