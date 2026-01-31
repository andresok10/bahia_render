from imports import *
from sqlalchemy.dialects.postgresql import JSON
#from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class Usuario(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    ced_ruc = Column(String(20), nullable=True)  # Cedula o RUC
    name = Column(String(30), nullable=False)       # Nombre o Razón Social
    user = Column(String(30), nullable=False, unique=True)
    passs = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    #admin = Column(Boolean, default=False)
    admin = Column(Integer, default=False)
    #fecha = Column(DateTime, default=datetime.now)
    #fecha = Column(DateTime, default=datetime.today)
    def __repr__(self):
        return '<Usuario id=%r, name=%r>' % (self.id, self.name)


class Cat(db.Model): 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subcats = db.relationship("Subcat", backref="cat", cascade="all, delete-orphan", lazy="select")
    def __repr__(self):
        return f"<Cat {self.id} {self.name}>"

class Subcat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    catid = Column(Integer, ForeignKey('cat.id'), nullable=False)

    name = Column(String(50), nullable=False)
    img_subcat = Column(String(50), nullable=False)
    articulosx = db.relationship("Articulos", backref="subcat", cascade="all, delete-orphan", lazy="select")
    def __repr__(self):
        return f"<Subcat {self.id} {self.name}>"

class Articulos(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    subcatid = Column(Integer, ForeignKey('subcat.id'), nullable=False)

    name = Column(String(30), nullable=False)
    #precio = Column(Float, default=0)
    precio = Column(Numeric(10, 2), nullable=False)   # ✅
    info = Column(String(50))
    img1 = Column(String(200))
    img2 = Column(String(200))
    img3 = Column(String(200))
    stock = Column(Integer, default=1)
    def __repr__(self):
        return f"<Articulo {self.id} {self.name}>"

class Pedido(db.Model):
    id = Column(Integer, primary_key=True)
    subtotal = Column(Numeric(10, 2))
    iva = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    estado = Column(String(20), default="PENDIENTE")
    productos = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    usuario = relationship("Usuario", backref=db.backref("pedidos", lazy=True))
    def __repr__(self):
        return f"<Pedido {self.id} Usuario {self.user_id} Total {self.total}>"

lista_subcat_icons = [
        # subcat mujer icon
        ["Blusas","1blusa.png",1], ["faldas","2.webp",1], ["Pantalon","3.webp",1], 
        ["Chaquetas/Abrigos","9.jpg",1],["Vestidos Elegantes","6.jpg",1], 
        ["Trajes de Baño","4.webp",1], ["Shorts","5.jpg",1], 
        ["Conjuntos/Enterizos","7.jpg",1],["Trajes para Trabajo","8.webp",1], 
        ["Zapatos","10.jpg",1], 
        ["Joyas y carteras","11.jpg",1], 
        ["Maquillajes","12.jpg",1],
        
        # subcat hombre icon
        ["camisas/camisetas","1.jpg",2], ["Pantalones","2.png",2], 
        ["Sudaderas y Abrigos","3.jpg",2],["Chaquetas","4.jpg",2], 
        ["Conjuntos","iconblusa1.webp",2], ["Trajes Elegantes","6.webp",2],
        ["playeras","7.jpg",2], ["Gorras y Bolsos","77.jpg",2], ["Zapatos","8.png",2], 
        ["Joyeria y mas","9.jpg",2]
    ]

#lista_subcat_hombre = [
#        ["Blusas y Camisetas","1blusa.png",1], ["faldas","1.webp",1], ["Pantalon","3.webp",1], ["Chaquetas/Abrigos","9.jpg",1],
#        ["Vestidos Elegantes","6.jpg",1], ["Trajes de Baño","4.webp",1], ["Shorts","5.jpg",1], ["Conjuntos/Enterizos","7.jpg",1],
#        ["Trajes para Trabajo","8.webp",1], ["Zapatos","10.jpg",1], ["Joyeria y Accesorios","11.jpg",1], ["Maquillajes","12.jpg",1]
#  

arts = [
    # blusas # articulos(nombre,img1,img2,img3,precio,info,stock,subcatid),
    ["ok1", "blusa1.1.webp", "blusa1.2.webp", "blusa3.jpg", 10.22, "xxx", 2, 1], 
    ["ok1", "blusa1.2.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 2, 1],
    ["ok1", "blusa3.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 2, 1], 
    ["ok1", "blusa7.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 2, 1],
    # faldas
    ["ok2", "falda1.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 2], 
    ["ok2", "falda2.jpg", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 2],
    ["ok2", "falda3.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 2, 2], 
    ["ok2", "falda4.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 2, 2],
    # pantalon
    ["ok3", "p1.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 3],  
    ["ok3", "p2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 6, 3],
    ["ok3", "p3.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 3],  
    ["ok3", "p4.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 6, 3],
    # chaquetas y abrigos
    ["ok4", "abrigo1.webp", "1blusa.png", "1blusa.png", 30.22, "xxx", 5, 4], 
    ["ok4", "abrigo2.webp", "1blusa.png", "1blusa.png", 40.22, "xxx", 5, 4],
    ["ok4", "abrigo3.jpg", "1blusa.png", "1blusa.png", 30.22, "xxx", 5, 4], 
    ["ok4", "abrigo4.png", "1blusa.png", "1blusa.png", 40.22, "xxx", 5, 4],
    # vesitdps
    ["ok5", "v1.webp", "1blusa.png", "1blusa.png", 30.22, "xxx", 5, 5], 
    ["ok5", "v2.webp", "1blusa.png", "1blusa.png", 40.22, "xxx", 5, 5],
    ["ok5", "v3.webp", "1blusa.png", "1blusa.png", 30.22, "xxx", 5, 5], 
    ["ok5", "v4.webp", "1blusa.png", "1blusa.png", 40.22, "xxx", 5, 5],
    # trajes de baño
    ["ok6", "tb1.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 6],
    ["ok6", "tb2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 6],
    #["ok6",  img1="tb3.webp",img2="1blusa.png",img3="1blusa.png",      precio=10.22, info="xxx",stock=2,subcatid=6)],
    #["ok6",  img1="tb4.webp",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=6)],
    # shorts
    ["ok7", "1.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 7],
    ["ok7", "2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 7],
    #["ok7",  img1="3.webp",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=7)],
    #["ok7",  img1="4.jpg",img2="1blusa.png",img3="1blusa.png",      precio=10.22, info="xxx",stock=2,subcatid=7)],
    # conjuntos y enterizos
    ["ok8", "1.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 8],
    ["ok8", "2.jpg", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 8],
    #["ok8",  img1="3.webp",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=8)],
    #["ok8",  img1="5.webp",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=8)],
    # trajes para trabajo
    ["ok9",  "t1.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 9],
    ["ok9",  "t2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 9],
    #["ok9",  img1="t3.webp",img2="1blusa.png",img3="1blusa.png",      precio=10.22, info="xxx",stock=2,subcatid=9)],
    #["ok9",  img1="t4.webp",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=9)],
    # zapatos
    ["ok9", "1.webp",  "1blusa.png", "1blusa.png", 10.22, "xxx", 9, 10],
    ["ok10", "2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 10, 10],
    #["ok11",  img1="3.webp",img2="1blusa.png",img3="1blusa.png",     precio=30.22, info="xxx",stock=11,subcatid=10)],
    #["ok12",  img1="4.webp",img2="1blusa.png",img3="1blusa.png",     precio=40.22, info="xxx",stock=12,subcatid=10)],
    # accesorios
    ["ok10", "1.webp", "1blusa.png", "1blusa.png", 10.22, "xxx", 13, 11],
    ["ok10", "2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 14, 11],
    #["ok10",  img1="3.webp",img2="1blusa.png",img3="1blusa.png",       precio=30.22, info="xxx",stock=15,subcatid=11)],
    #["ok10",  img1="4.webp",img2="1blusa.png",img3="1blusa.png",       precio=40.22, info="xxx",stock=16,subcatid=11)],
    # maquillajes
    ["ok11", "m1.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 5, 12],
    ["ok11", "m2.jpg", "1blusa.png", "1blusa.png", 20.22, "xxx", 5, 12],
    #["ok11",  img1="m3.jpg",img2="1blusa.png",img3="1blusa.png",       precio=10.22, info="xxx",stock=2,subcatid=12)],
    #["ok11",  img1="m4.jpg",img2="1blusa.png",img3="1blusa.png",      precio=10.22, info="xxx",stock=2,subcatid=12)],
    ###########################################################################
    # hombre camisas
    ["ok12", "1.jpg", "1blusa.png", "1blusa.png", 10.22, "xxx", 1, 13],
    ["ok13", "2.webp", "1blusa.png", "1blusa.png", 20.22, "xxx", 2, 13]
    #["ok1",  img1="camisa3.webp",img2="1blusa.png",img3="1blusa.png",     precio=30.22, info="xxx",stock=3,subcatid=19)],
    #["ok1",  img1="camisa4.webp",img2="1blusa.png",img3="1blusa.png",     precio=40.22, info="xxx",stock=4,subcatid=20)], 
    
]
#print(len(arts))

def init_db():
    os.system('mysql -u root -e "DROP DATABASE IF EXISTS render1;"')
    os.system('mysql -u root -e "CREATE DATABASE IF NOT EXISTS render1;"')
    db.create_all()

    [db.session.add(Cat(name=x)) for x in ["mujer", "hombre", "niño", "niña"] if not Cat.query.filter_by(name=x).first()]
    #for x in ["mujer", "hombre", "niño", "niña"]:
    #    if not cat.query.filter_by(nombre=x).first():
    #        db.session.add(cat(nombre=x))
    ####################################################
    lista_usuarios =[
        ["09991" ,"dave1x","dave1","qqww","ok1@gmail.com",1],
        ["09992" ,"dave2x","dave2","aass","ok2@gmail.com",0],
    ]
    for xx in lista_usuarios:
        if not Usuario.query.filter_by(ced_ruc=xx[0]).first():
            db.session.add(Usuario(ced_ruc=xx[0], name=xx[1], user=xx[2], passs=xx[3], email=xx[4], admin=xx[5]))

    ##########################################################
    for nombre, icono, catid in lista_subcat_icons:
        # ruta base por categoría
        if catid == 1:
            ruta = f"subcat_mujer_icon/{icono}"
        elif catid == 2:
            ruta = f"subcat_hombre_icon/{icono}"
        else:
            continue

        if not Subcat.query.filter_by(name=nombre, catid=catid).first():
            db.session.add(Subcat(name=nombre,img_subcat=ruta,catid=catid))

    ###################################################################
    lista_mujer = ["1blusas","2faldas","3pantalon","4chaquetas_abrigos","5vestidos","6tbaño","7short","8conjuntos","9trabajo","10zapatos","11accesorios","12maquillaje"]
    lista_hombre = ["1camisas","2pantalon","3abrigos","4chaquetas","5trajes","6tbaño","7gorras","8zapatos","9accesorios"]

    for art in arts:
        #print(len(art)) # 8campos
        subcatid = art[7]

        if 1 <= subcatid <= 12: # MUJER (subcatid 1 a 12)
            ruta = f"1mujer/{lista_mujer[subcatid - 1]}/" #subcatid - 1 = 0

        elif 13 <= subcatid <= 21: # HOMBRE (subcatid 13 a 21)
            ruta = f"2hombre/{lista_hombre[subcatid - 13]}/"

        else:
            continue

        img1, img2, img3 = (ruta + art[1],ruta + art[2],ruta + art[3])

        if not Articulos.query.filter_by(img1=img1).first():
            db.session.add(Articulos(name=art[0],img1=img1,img2=img2,img3=img3,
                    precio=art[4],
                    info=art[5],
                    stock=art[6],
                    subcatid=subcatid
                )
            )
    db.session.commit()
    db.session.close()

"""
Cuando el usuario finaliza su compra, puedes usar este método para agregar los productos al pedido y guardarlos:
@app1.route('/finalizar_compra', methods=["POST"])
def finalizar_compra():
    if 'carrito' in session and 'id' in session:
        carrito = session['carrito']
        usuario_id = session['id']
        pedido = Pedido(usuario_id=usuario_id, productos=[], total=0)
        pedido.add_productos(carrito)
        db.session.add(pedido)
        db.session.commit()

        # Limpiar el carrito después de la compra
        session['carrito'] = []
        session['total'] = 0

        return redirect(url_for('fun1.ver_pedido', pedido_id=pedido.id))
    return redirect(url_for('fun1.iniciox'))
"""

#def create_tables_and_seed():
#    with app.app_context():
#        db.drop_all()  # Elimina tablas existentes (opcional, solo para pruebas)
#        db.create_all()  # Crea las tablas en el orden correcto
#        seed_data()  # Llama a la función para poblar datos iniciales
# Ejecutar la creación de tablas y datos iniciales
#create_tables_and_seed()