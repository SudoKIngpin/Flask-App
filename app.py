from flask import Flask, render_template, request

app = Flask(__name__)

# Data for each year
YEAR_DATA = {

    "1st":
     {
        "title": "First Year Papers",
        "description": "Discover the foundation of engineering with introductory courses.",
        "image": "images/1.png",
        "subjects": [
            {"name": "Maths1", "sessional1_link": "/static/papers/1/1st/maths11.pdf", "sessional2_link": "/static/papers/2/1st/maths12.pdf"},
            {"name": "Physics", "sessional1_link": "/static//papers/1/1st/physics1.pdf", "sessional2_link": "/static/papers/2/1st/physics2.pdf"},
            {"name": "Soft Skills", "sessional1_link": "/static/papers/1/1st/soft1.pdf", "sessional2_link": "/static/papers/2/1st/soft2.pdf"},
            {"name": "PPS", "sessional1_link": "/static//papers/1/1st/pps1.pdf", "sessional2_link": "/static/papers/2/1st/pps2.pdf"},
            {"name": "Chemistry", "sessional1_link": "/static/papers/1/1st/chemistry1.pdf", "sessional2_link": "/static/papers/1/1st/chemistry1.pdf"},
            {"name": "Environment", "sessional1_link": "/static/papers/1/1st/env1.pdf", "sessional2_link": "/static/papers/1/1st/env1.pdf"},
            {"name": "Maths2", "sessional1_link": "/static/papers/1/1st/maths21.pdf", "sessional2_link": "/static/papers/2/1st/maths22.pdf"},
            {"name": "Mechanical Engineering", "sessional1_link": "/static/papers/1/1st/mech1.pdf", "sessional2_link": "/static/papers/1/1st/mech1.pdf"},
            {"name": "Electrical Engineering", "sessional1_link": "/static/papers/1/1st/electrical1.pdf", "sessional2_link": "/static/papers/2/1st/electrical2.pdf"},
            {"name": "Electronics Engineering", "sessional1_link": "/static/papers/1/1st/electronics1.pdf", "sessional2_link": "/static/papers/1/1st/electronics1.pdf"},
        ]
    },


    "2nd":
     {
        "title": "Second Year Papers",
        "description": "Dive deeper into your core subjects and practical learning and clear your basics.",
        "image": "images/2.png",
        "subjects": [

             {"name": "Data Structures", "sessional1_link": "/static/papers/1/2nd/dsa.jpg", "sessional2_link": "/static/papers/2/2nd/dsa.jpg"},
             {"name": "Digital Electronics", "sessional1_link": "/static/papers/1/2nd/de.jpg", "sessional2_link": "/static/papers/2/2nd/de.jpg"},
             {"name": "Computer Org. & Arch.", "sessional1_link": "/static/papers/1/2nd/coa.jpg", "sessional2_link": "/static/papers/2/2nd/coa.jpg"},
             {"name": "Discrete Maths", "sessional1_link": "/static/papers/1/2nd/dm.jpeg", "sessional2_link": "/static/papers/2/2nd/dm.jpg"},
             {"name": "Human Values", "sessional1_link": "/static/papers/1/2nd/uhv.jpg", "sessional2_link": "/static/papers/2/2nd/uhv.jpg"},




        ]
    },


    "3rd": {
        "title": "Third Year Papers",
        "description": "Master advanced topics and prepare for internships and projects",
        "image": "images/3.png",
        "subjects": ["Operating Systems.pdf", "Algorithms.pdf", "Computer Networks.pdf"]
    },


    "4th": {
        "title": "Final Year Papers",
        "description": "Finalize your journey with specializations and your major projects.",
        "image": "images/4.png",
        "subjects": ["Machine Learning.pdf", "Cloud Computing.pdf", "AI.pdf"]
    }


}

@app.route('/')
def home():
    return render_template('home.html', year=None)

@app.route('/<year>')
def papers(year):
    data = YEAR_DATA.get(year)
    if not data:
        return "Year not found", 404
    return render_template('papers.html', year=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


