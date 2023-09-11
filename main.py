from app import app
from app import render_template 

if __name__ == "__main__":
    app.run(port = 3000, debug = True)

@app.route('/')
def inicio():
    return render_template('menu.html')