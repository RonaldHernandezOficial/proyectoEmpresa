from app import app
from app import render_template 

@app.route('/')
def inicio():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run()