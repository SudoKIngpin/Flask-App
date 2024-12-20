from flask import Flask, render_template, request, Response

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
             {"name": "Operating System", "sessional1_link": "/static/papers/1/2nd/OS.pdf", "sessional2_link": "/static/papers/2/2nd/OS.pdf"},
             {"name": "Human Values", "sessional1_link": "/static/papers/1/2nd/uhv.jpg", "sessional2_link": "/static/papers/2/2nd/uhv.jpg"},
             {"name": "Python", "sessional1_link": "/static/papers/1/2nd/python1.pdf", "sessional2_link": "/static/papers/2/2nd/python2.pdf"},
             {"name": "Java", "sessional1_link": "/static/papers/1/2nd/", "sessional2_link": "/static/papers/2/2nd/"},
             {"name": "Maths - IV", "sessional1_link": "/static/papers/1/2nd/M4.pdf", "sessional2_link": "/static/papers/2/2nd/M4.pdf"}




        ]
    },


    "3rd": 
    {
        "title": "Third Year Papers",
        "description": "Master advanced topics and prepare for internships and projects",
        "image": "images/3.png",
        "subjects":  [
             
             {"name": "Web  Technology", "sessional1_link": "/static/papers/1/3rd/Web.pdf", "sessional2_link": "/static/papers/2/3rd/Web.pdf"},
             {"name": "Machine Learning", "sessional1_link": "/static/papers/1/3rd/Ml.jpg", "sessional2_link": "/static/papers/2/3rd/ML.pdf"},
             {"name": "Data Analytics", "sessional1_link": "/static/papers/1/3rd/DA.jpg", "sessional2_link": "/static/papers/2/3rd/DA.pdf"},
             {"name": "Algorithms", "sessional1_link": "/static/papers/1/3rd/DAA.pdf", "sessional2_link": "/static/papers/2/3rd/DAA.pdf"},
             {"name": "Constitution", "sessional1_link": "/static/papers/1/3rd/Const.jpg", "sessional2_link": "/static/papers/2/3rd/Const.jpg"},
             {"name": "DBMS", "sessional1_link": "/static/papers/1/3rd/DBMS.pdf", "sessional2_link": "/static/papers/2/3rd/DBMS.pdf"}         
  ]
  
    },


    "4th": {
        "title": "Final Year Papers",
        "description": "Finalize your journey with specializations and your major projects.",
        "image": "images/4.png",
        "subjects": ["Machine Learning.pdf", "Cloud Computing.pdf", "AI.pdf"]
    }


}



@app.route('/robots.txt')
def robots_txt():
    response = Response("User-agent: Googlebot\nDisallow:\nSitemap: https://siet-exams.onrender.com/sitemap.xml", mimetype='text/plain')
    return response



@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

<url>
  <loc>https://siet-exams.onrender.com/</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>1.00</priority>
</url>
<url>
  <loc>https://siet-exams.onrender.com/feedback</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>0.80</priority>
</url>
<url>
  <loc>https://siet-exams.onrender.com/1st</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>0.80</priority>
</url>
<url>
  <loc>https://siet-exams.onrender.com/2nd</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>0.80</priority>
</url>
<url>
  <loc>https://siet-exams.onrender.com/3rd</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>0.80</priority>
</url>
<url>
  <loc>https://siet-exams.onrender.com/4th</loc>
  <lastmod>2024-12-11T14:52:24+00:00</lastmod>
  <priority>0.80</priority>
</url>
</urlset>'''
    response = Response(sitemap_xml, mimetype='application/xml')
    return response

@app.route('/')
def home():
    return render_template('home.html', year=None)

@app.route('/<year>')
def papers(year):
    data = YEAR_DATA.get(year)
    if not data:
        return "Year not found", 404
    return render_template('papers.html', year=data)


@app.route("/feedback")
def feedback():
    return render_template("/feedback.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')


