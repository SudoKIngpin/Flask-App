from flask import Flask , render_template , redirect 
app=Flask(__name__)

@app.route('/')
def h():
    return render_template("index.html")

@app.route("/s1")
def s1():
        return redirect("https://drive.google.com/drive/folders/1Mn-p3Xtb0knsjWKU7n8h2pCqam3r_K3C?usp=sharing", code=302)

@app.route("/s2")
def s2():
<<<<<<< HEAD
    return redirect("https://drive.google.com/drive/folders/1ISC0C_-ub0rEknT9DcG0Rgu-keUPJPVh?usp=sharing",code=302)
app.run(host="0.0.0.0")
=======
    return render_template("s2.html")
app.run(host="0.0.0.0")
>>>>>>> 65b78f1ec3f60a59077169bfe20d9c9d430e01f8
