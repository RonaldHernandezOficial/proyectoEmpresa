from app import app
from app import render_template 
from flask_mysqldb import MySQL

# MYSQL Connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'post_sale'

# Settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/')
def inicio():
    return render_template('/menu.html')

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
