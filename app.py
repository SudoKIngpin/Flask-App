from flask import Flask , render_template
app=Flask(__name__)

@app.route('/')
def h():
    return render_template("index.html")

@app.route("/s1")
def s1():
    return render_template("s1.html")

@app.route("/s2")
def s2():
    return render_template("s2.html")
app.run(debug=True)