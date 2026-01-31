from imports import *
from modelo5 import *

app0 = Blueprint('fun_user', __name__)

#@app.route('/', methods=['get', 'post'])
@app0.route('/login', methods=['get', 'post'])
def loginx():
    msg=""
    if request.method == 'POST':       #if flask.request.method == 'GET':
        userx = request.form['user']
        passsx = request.form['passs']
        #remember = True if request.form.get('remember') else False
        #user = usuarios.query.filter_by(usuario=usuariox, password=passwordx).first()
        #if user is not None:
        #    #session['activo'] = True
        #session['id'] = user.id
        #session['nombre'] = user.nombre
        #session['admin'] = user.admin
            #return redirect(url_for('iniciox'))
        #    return redirect('/')
        user = Usuario.query.filter_by(user=userx,passs=passsx).first()
        #if user is not None and user.passs==passwordx: # and user.admin==0:
        if user:# and Usuario.query.filter_by(passs=passsx).first():
        #if user and db.execute(select(usuarios).filter_by(password=passwordx)).first():
            session['id'] = user.id
            session['nombre'] = user.name
            session['admin'] = user.admin
            #session['admin'] = 1
            return redirect('/')
            #return redirect(url_for('iniciox'))
        else:
            msg="credenciales invalidas"
    return render_template('usuarios/user.html',msg=msg, accion='login')

@app0.route("/registro", methods=["GET", "POST"])
def registrox():
    msg = ""
    if request.method == "POST":
        ced_ruc = request.form.get("ced_ruc", "")
        namex = request.form.get("name", "")
        userx = request.form.get("user", "")
        passs = request.form.get("passs", "")
        email = request.form.get("email", "")
        # Determinar si será admin
        adminx = 1 if session.get("admin") == 1 and request.form.get("admin") else 0
        # Verificar si ya existe el user
        user_existe = Usuario.query.filter_by(user=userx).first()
        if user_existe:
            if user_existe.admin == 1:
                msg = "El admin ya existe"
            else:
                msg = "El user ya existe"
        else:
            user_add = Usuario(ced_ruc=ced_ruc,name=namex,user=userx,passs=passs,email=email,admin=adminx)
            db.session.add(user_add)
            db.session.commit()
            msg = "Se registró con éxito un admin" if adminx == 1 else "Se registró con éxito un user"
    return render_template("usuarios/user.html", msg=msg, accion='registro')

@app0.route('/perfil', methods=["GET", "POST"])
def perfilx():
    if 'id' not in session:
        return redirect('/login')
    cuenta = Usuario.query.filter_by(id=session['id']).first()
    if not cuenta:
        return redirect('/inicio')

    # Por defecto estamos viendo el perfil
    accion = request.args.get('accion', 'perfil')
    msg = ""
    # Si estamos cambiando la contraseña
    if accion == "cambiar_pass" and request.method == 'POST':
        nueva_pass = request.form.get('passs', '').strip()
        if nueva_pass:
            cuenta.passs = nueva_pass
            db.session.commit()
            msg = "✅ Contraseña actualizada con éxito"
    return render_template("usuarios/user.html",accion=accion,cuenta=cuenta,msg=msg)

@app0.route('/cerrar')
def cerrarx():
    #if "id" in session:
    #    session.clear()
    #session.pop('activo', None)
    #session.pop('loggedin', None)
    #session.pop('id', None)
    #session.pop('nombre', None)
    session.clear()
    return redirect(url_for('fun_ini.iniciox'))