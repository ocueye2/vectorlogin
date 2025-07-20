from submod.fr import checkuser

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/vector")
def vcheck():
    if checkuser():
         return render_template("suc.html")
    else:
        return render_template("fail.html")

if __name__ == "__main__":
    app.run()