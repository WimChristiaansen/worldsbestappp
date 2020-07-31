from flask import Flask, render_template, flash,redirect
from Flask.Form.form import PlotForm #import the form we made in another py-file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '1DEDA5F2D1C57ABCB34AC024CB21FFFE4C96F2D4' #SHA1
app.config['SQLALCHEMY_DATABASE_URI'] = "sqllite:///site.db" # is a relative path

db = SQLAlchemy(app)

class User(db.Model):
    date = db.Column(db.DateTime,primary_key = 0, default = datetime.utcnow)
    #username = db.Column(db.String(20),unique=True,nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False,default="default.jpeg")
    street =db.Column(db.String(50),nullable=False)
    streetNumber = db.Column(db.Integer(4), nullable=False)
    postCode = db.Column(db.Integer(4), nullable=False)
    city = db.Column(db.String(50),nullable=False)

    def __repr__(self): #how are object is printed
        return f"User('{self.date}','{self.street}','{self.streetNumber}','{self.postCode}'," \
               f"'{self.city}')"


@app.route("/")
def hello():
    return  render_template('home.html')

@app.route("/about") #http://localhost:5000/about
def about():
    return render_template("about.html")

@app.route('/form',methods=['GET','POST'])
def form():
    form = PlotForm()
    #if form.validate_on_submit():
     #   flash(f'House Plotted {form.Street.data}!','success') #flash-message
     #   return redirect(url_for('home'))
    return render_template('form.html',title="Plotting a House in 3D",form=form)


app.run(debug=True) # run app localy

