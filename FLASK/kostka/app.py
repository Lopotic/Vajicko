import random
from flask import Flask,render_template
 
app = Flask(__name__)
app.debug = True
 

 
@app.route('/')
def kostka():
    hod_kostkou = random.randint(1,6)
    n2w = {1: 'jedna', 2:'dva', 3:'tři',4:'čtyři',5:'pět',6:'šest'}
    return render_template("kostka.html",hod_kostkou=hod_kostkou)
    

 
if __name__ == '__main__':
    app.run()
