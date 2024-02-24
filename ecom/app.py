#from flask import Flask,render_template,request,redirect

#from flask_pymongo import PyMongo

#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
#mongo = PyMongo(app)


from flask import Flask, render_template, request, url_for, redirect 
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
# Instantiate the Flask class by creating a flask application
app = Flask(__name__)
# Create the mongodb client
client = MongoClient('localhost', 27017)
# Get and Post Route
@app.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == "POST":   # if the request method is post, then insert the todo document in vender collection
        content = request.form['content']
        degree = request.form['degree']
        uname =request.form['uname']
        number=request.form['number']
        vender.insert_one({'content': content, 'degree': degree, 'uname': uname,'number':number})
        return redirect(url_for('add')) # redirect the user to home page
    all_vender = vender.find()    # display all todo documents
    return render_template('add.html', vender = all_vender) # render home page template with all vender




def add():
      return render_template( 'add.html' )




@app.route('/')
def index():
    return  render_template('index.html')
@app.route('/contact')
def contact():
    return render_template( 'contact.html' )


  
@app.route('/add',methods=['POST'])

 
@app.route('/home')
def landingPage():
    return render_template('index.html')


@app.route('/about')
def about():
    return  render_template('about.html')


@app.post("/<id>/delete/")
def delete(id): #delete function by targeting a todo document by its own id
    vender.delete_one({"_id":ObjectId(id)}) #deleting the selected todo document by its converted id
    return redirect(url_for('add')) # again, redirecting you to the home page 
db = client.StyleIT # creating your flask database using your mongo client 
vender = db.vender # creating a collection called "vender"



if __name__ == "__main__":
    app.run(debug=True, port=8000)
