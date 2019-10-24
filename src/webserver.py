from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Index!"

@app.route("/submit")
def submitPage():
    return "Submit!"
    
@app.route("/submit/<string:name>/")
def submitURL(name):
    return "Submitted: " + name

@app.route("/view")
def viewPage():
    return "View"

@app.route("/view/<string:name>/")
def viewResults(name):
    return "Viewed: " + name

if __name__ == "__main__":
    app.run(port="5000")