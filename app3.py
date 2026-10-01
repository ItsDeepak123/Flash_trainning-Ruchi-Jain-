from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
# database connectivity configuration code
# Define Database URI: mysql+pymysql://username:password@host/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("Deepak")
# Initialize SQLAlchemy
db = SQLAlchemy(app)


class Employee(db.Model):
    Eno=db.Column(db.Integer,primary_key=True)
    Ename=db.Column(db.String(80),nullable=True)
    Email=db.Column(db.String(80),nullable=True)    
    phone=db.Column(db.String(80),nullable=True)
    msg=db.Column(db.String(80),nullable=True)
with app.app_context():
    db.create_all()
if __name__=='__main__':
    app.run(debug=True)