from imports import *
#from modelo5 import *

#app2 = Blueprint('fun_art', __name__, url_prefix="")
app2 = Blueprint('fun_art', __name__)

def cargar_vista(cat_id=None,subcat_id=None,art_id=None,edit_cat=None,edit_subcat=None,edit_articulo=None):
    categorias = Cat.query.options(joinedload(Cat.subcats).joinedload(Subcat.articulosx)).all()

    categoria = categorias[0] if categorias else None
    subcategoria = None
    articulos = []

    if categoria and cat_id:
        categoria = next((c for c in categorias if c.id == cat_id), categoria)

    if categoria and categoria.subcats:
        subcategoria = categoria.subcats[0]

        if subcat_id:
            subcategoria = next((s for s in categoria.subcats if s.id == subcat_id),subcategoria)

        articulos = subcategoria.articulosx

    return render_template('index/crud_admin.html',
        categorias=categorias,
        categoria=categoria,
        subcategoria=subcategoria,
        articulos=articulos,
        art_id=art_id,
        edit_cat=edit_cat,
        edit_subcat=edit_subcat,
        edit_articulo=edit_articulo
    )

#@app2.route('/', methods=['GET', 'POST'])
@app2.route('/categoria', methods=['GET', 'POST'])
def categoriax():
    if request.method == 'POST':
        db.session.add(Cat(name=request.form.get('name')))
        #name = request.form.get('name')  # <- usa get() para evitar KeyError
        db.session.commit()
        return redirect(url_for('fun_art.categoriax'))

    return cargar_vista(cat_id=request.args.get('cat_id', type=int))

@app2.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    cat = Cat.query.get_or_404(id)
    if request.method == 'POST':
        cat.name = request.form['name']
        db.session.commit()
        return redirect(url_for('fun_art.categoriax'))
    return cargar_vista(cat_id=id, edit_cat=cat)

@app2.route('/subcat/<int:cat_id>', methods=['GET', 'POST'])
def subcatx(cat_id):
    if request.method == 'POST':
        db.session.add(Subcat(
            name=request.form['name'],
            img_subcat=request.form['img_subcat'],
            catid=cat_id
        ))
        db.session.commit()
        return redirect(url_for('fun_art.subcatx', cat_id=cat_id))

    return cargar_vista(
        cat_id=cat_id,
        subcat_id=request.args.get('subcat_id', type=int)
    )

@app2.route('/subcat/editar/<int:id>', methods=['GET', 'POST'])
def editar_subcategoria(id):
    sub = Subcat.query.get_or_404(id)

    if request.method == 'POST':
        sub.name = request.form['name']
        sub.img_subcat = request.form['img_subcat']
        db.session.commit()
        return redirect(url_for('fun_art.subcatx', cat_id=sub.catid))

    return cargar_vista(
        cat_id=sub.catid,
        subcat_id=sub.id,
        edit_subcat=sub
    )

@app2.route('/articulo/<int:subcat_id>')
def articulox(subcat_id):
    return cargar_vista(subcat_id=subcat_id)

@app2.route('/articulo/editar/<int:id>', methods=['GET', 'POST'])
def editar_articulo(id):
    art = Articulos.query.get_or_404(id)

    if request.method == 'POST':
        art.name = request.form['name']
        art.precio = request.form['precio']
        art.img1 = request.form['img1']
        art.img2 = request.form['img2']
        art.img3 = request.form['img3']
        db.session.commit()
        return redirect(url_for('fun_art.articulox', subcat_id=art.subcatid))

    return cargar_vista(
        cat_id=art.subcat.catid,
        subcat_id=art.subcatid,
        edit_articulo=art
    )

@app2.route('/categoria/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):
    db.session.delete(Cat.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('fun_art.categoriax'))


@app2.route('/subcategoria/eliminar/<int:id>', methods=['POST'])
def eliminar_subcategoria(id):
    sub = Subcat.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    return redirect(url_for('fun_art.subcatx', cat_id=sub.catid))


@app2.route('/articulo/eliminar/<int:id>', methods=['POST'])
def eliminar_articulo(id):
    art = Articulos.query.get_or_404(id)
    db.session.delete(art)
    db.session.commit()
    return redirect(url_for('fun_art.articulox', subcat_id=art.subcatid))