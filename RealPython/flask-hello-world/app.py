# ---- Flask Hello World ---- #

# import the Flask class from the flask package
from flask import Flask

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route("/")
@app.route("/hello")
def hello_world():
    return "Hello, World!"

# dynamic route
@app.route("/test/<search_query>") # take a query parameter
def search(search_query):
    return search_query

# start the development server using the run() method
if __name__=="__main__":
    app.run()
