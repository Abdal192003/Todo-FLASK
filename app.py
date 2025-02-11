from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///mydatabase.db"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"

@app.route('/', methods=['GET','POST'])
def Hello_World():
    if(request.method=='POST'):
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/product')
def product():
    alltodo=Todo.query.all()
    print(alltodo)
    return 'This is my product'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if (request.method=='POST'):
        title=request.form['title']    
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
        

@app.route('/delete/<int:sno>',methods=['GET','POST'])
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)