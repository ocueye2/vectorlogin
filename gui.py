from submod.fr import checkuser
import os
import time
os.chdir("/home/ocueye/Documents/workspace/docker/vector/vectorlogin")
from flask import Flask, render_template, request

app = Flask(__name__,"/static","static")

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/vector")
def vcheck():
    if checkuser():
        os.system("killall surf")
        os.system("hyprland &")
        time.sleep(1)
        exit()
        return render_template("suc.html")
    else:
        return render_template("fail.html")

@app.route("/submit",methods=['GET', 'POST'])
def submit():
    if request.form["Username"] == "admin":
        if request.form["password"] == "admin":
            os.system("/home/ocueye/Documents/workspace/docker/vector/load.sh")
            return render_template("suc.html")
        else:
            return render_template("fail.html")
    else:
        return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True,port=8060)