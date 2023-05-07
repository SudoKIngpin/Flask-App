from time import sleep 
import webbrowser as w 
import requests as r 


try :
        con=r.get("https://siet-exams.onrender.com")

        t=con.text
        # print(t)
except: 
        pass 
w.open_new("https://google.com",autoraise=False)
w.open_new_tab("https://siet.in")
sleep(3)
w.open_new("https://siet-exams.onrender.com")
sleep(5)
sleep(10)
w.open_new("https://siet-exams.onrender.com")
sleep(100)
w.open_new("https://siet-exams.onrender.com")

