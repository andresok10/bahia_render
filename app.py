from imports import *
from modelo5 import *
#load_dotenv()
# Solo cargar .env si existe (local)
#if os.path.exists(".env"):
#    load_dotenv()
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#app.secret_key = os.getenv("A0Zr98j/3yX R~XHH!jmN]LWX/,?RT")

#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/render1"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://deybi10x:bahia@deybix.mysql.pythonanywhere-services.com/deybix$bahia'
##db=pymysql.connect(host="deybi10x.mysql.pythonanywhere-services.com",user="deybi10x",password="zzzzxxxx",database="deybi10x$contactos")
#SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("postgres://bahia_user:lzfll0pWQF2Gm2l2DbiOXzgeCZ4y0sp6@dpg-d5uoqcfpm1nc73c1kg4g-a:5432/bahia")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
    if Cat.query.count() == 0:
        init_db()
    else:
        print("Base de datos ya inicializada")
    #init_db()
    total = Articulos.query.count()
    print("Registros en la BD:", total)

app.register_blueprint(app0)
app.register_blueprint(app1)
app.register_blueprint(app2)
#lista = [app0,app1,app2]
#for x in lista:
#    app.register_blueprint(x)

# Inicializar carrito antes de cada request
'''@app.before_request
def before_request_func():
    if "id" not in session:
        session.clear()
    if "admin" not in session:
        session.clear()
    #if "carrito" not in session:
    #    session['carrito'] = []
    #if "contador" not in session:
    #    session['contador'] = 0
    if "total" not in session:
        session['total'] = 0'''

#✔ No borra sesión ✔ Mantiene carrito ✔ Seguro
'''@app.before_request
def before_request_func():
    session.setdefault('carrito', [])
    session.setdefault('contador', 0)
    session.setdefault('total', 0)'''

'''@app.context_processor
def inject_cart():
    return dict(
        cart_count=session.get('contador', 0),
        cart_total=session.get('total', 0)
    )'''

'''@app.before_request
def before_request_func():
    session.setdefault('carrito', [])
    session.setdefault('contador', 0)
    session.setdefault('total', 0)'''

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return redirect(url_for('fun_ini.iniciox'))

#if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=5008, debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    #port = int(os.getenv("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=False)