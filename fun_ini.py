from imports import *
from modelo5 import *
from decimal import Decimal, ROUND_HALF_UP # 4242424242424242  02/29 895

app1 = Blueprint('fun_ini', __name__)    #<b>{{ session.carrito|length }}</b>

'''Q = Decimal("0.00")
IVA_ACTUAL = Decimal("0.12")

def procesar_totales_carrito_stripe(carrito):
    """
    Función central para calcular subtotal (incluyendo IVA), total y productos_detalle.
    Retorna:
        productos_detalle: lista de productos con subtotal, iva, total
        subtotal, iva_total, total: Decimales
    """
    productos_detalle = []
    subtotalx = Decimal("0.00")
    iva_totalx = Decimal("0.00")
    total_a_pagarx = Decimal("0.00")

    for item in carrito:
        producto = Articulos.query.get(item["id"])
        if not producto:
            raise ValueError(f"Producto {item['id']} no encontrado")
        if int(item["cantidad"]) > producto.stock:
            raise ValueError(f"Stock insuficiente para {producto.name}")

        cantidad = int(item["cantidad"])
        precio_unit = Decimal(str(producto.precio)).quantize(Q, ROUND_HALF_UP)

        # Calcular subtotal base y IVA
        sub_base = (precio_unit * cantidad).quantize(Q, ROUND_HALF_UP)
        iva = (sub_base * IVA_ACTUAL).quantize(Q, ROUND_HALF_UP)
        # Subtotal ahora incluye el IVA
        subtotal_item = (sub_base + iva).quantize(Q, ROUND_HALF_UP)

        productos_detalle.append({
            "id": producto.id,
            "name": producto.name,
            "img1": producto.img1,
            "cantidad": cantidad,
            "precio_unitario": float(precio_unit),
            "subtotal": float(subtotal_item),  # subtotal ahora incluye IVA
            "iva": float(iva),
            "total": float(subtotal_item)      # total = subtotal con IVA
        })

        subtotalx += subtotal_item
        iva_totalx += iva
        total_a_pagarx += subtotal_item

    # 🔹 Totales finales (Decimal)
    subtotal = subtotalx.quantize(Q, ROUND_HALF_UP)
    iva_total = iva_totalx.quantize(Q, ROUND_HALF_UP)
    total_a_pagar = total_a_pagarx.quantize(Q, ROUND_HALF_UP)
    return productos_detalle, subtotal, iva_total, total_a_pagar'''

DECIMALS_2 = Decimal("0.00")
IVA_ACTUAL = Decimal("0.12")

def procesar_totales_carrito_stripe(carrito):
    """
    Función central para calcular subtotal (incluyendo IVA), IVA total, total y productos_detalle.
    
    Retorna:
        productos_detalle: lista de productos con subtotal, iva, total
        subtotal, iva_total, total: Decimales
    """
    productos_detalle = []
    subtotal_total = DECIMALS_2   # Inicializamos con Q para mantener consistencia
    iva_total = DECIMALS_2        # Igual para IVA

    for item in carrito:
        producto = Articulos.query.get(item["id"])
        if not producto:
            raise ValueError(f"Producto {item['id']} no encontrado")
        
        cantidad = int(item["cantidad"])
        if cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente para {producto.name}")

        # Precio unitario
        precio_unit = Decimal(str(producto.precio)).quantize(DECIMALS_2, ROUND_HALF_UP)

        # Subtotal base y IVA
        sub_base = (precio_unit * cantidad).quantize(DECIMALS_2, ROUND_HALF_UP)
        iva_item = (sub_base * IVA_ACTUAL).quantize(DECIMALS_2, ROUND_HALF_UP)

        # Subtotal incluyendo IVA
        subtotal_item = (sub_base + iva_item).quantize(DECIMALS_2, ROUND_HALF_UP)

        # Agregar detalle del producto
        productos_detalle.append({
            "id": producto.id,
            "name": producto.name,
            "img1": producto.img1,
            "cantidad": cantidad,
            "precio_unitario": float(precio_unit),
            "subtotal": float(subtotal_item),  # subtotal incluye IVA
            "iva": float(iva_item),
            "total": float(subtotal_item)      # total = subtotal con IVA
        })

        # Acumular totales
        subtotal_total += subtotal_item
        iva_total += iva_item

    # Totales finales (Decimal)
    subtotal_total = subtotal_total.quantize(DECIMALS_2, ROUND_HALF_UP)
    iva_total = iva_total.quantize(DECIMALS_2, ROUND_HALF_UP)
    total_a_pagar = subtotal_total  # total = subtotal incluyendo IVA
    return productos_detalle, subtotal_total, iva_total, total_a_pagar

def actualizar_carrito_sesion(carrito):
    """Actualiza los valores del carrito en session usando la función central."""
    productos_detalle, subtotal, iva_total, total_a_pagar = procesar_totales_carrito_stripe(carrito)
    session["carrito"] = productos_detalle
    session["subtotal"] = subtotal
    session["iva"] = iva_total
    session["total"] = total_a_pagar
    session.modified = True

@app1.get("/")
@app1.get('/inicio')
@app1.get('/inicio/<int:catidx>')
@app1.get('/inicio/<int:catidx>/<int:subcatidx>')
def iniciox(catidx=None, subcatidx=None):
    cat_all = Cat.query.options(joinedload(Cat.subcats).joinedload(Subcat.articulosx)).all()
    #cat_id = next((x for x in cat_all if x.id == catidx), cat_all[0]) if catidx else cat_all[0] # categoria actual
    cat_id = next((c for c in cat_all if c.id == catidx), cat_all[0]) # categoria actual
    subcat_id = next((x for x in cat_id.subcats if x.id == subcatidx), cat_id.subcats[0] if cat_id.subcats else None)
    arts_id = subcat_id.articulosx if subcat_id else []
    # Petición HTMX: solo productos # Si es petición HTMX (solo se actualiza productos)
    if "HX-Request" in request.headers:
        return render_template("index/_productos.html", arts_id=arts_id, session=session)
    # Petición normal: toda la página
    return render_template("index/1mujer.html",cat_all=cat_all,cat_id=cat_id,subcategoria=subcat_id,arts_id=arts_id,session=session)

#@app1.route("/add", methods=["POST"])
@app1.post("/add")
def addx():
    prod_id = request.form.get("prod_id_form", type=int)
    cantidad = request.form.get("cantidad", type=int, default=1) #
    if not prod_id:
        abort(400)
    carrito = session.get("carrito", [])
    prod = Articulos.query.get_or_404(prod_id)
    # Agregar o actualizar cantidad
    for x in carrito:
        if x["id"] == prod_id:
            x["cantidad"] = min(x["cantidad"] + cantidad, prod.stock)
            break
    else:
        carrito.append({
            "id": prod.id,
            "name": prod.name,
            "precio": prod.precio,
            "img1": prod.img1,
            "stock": prod.stock,
            "cantidad": min(cantidad, prod.stock)
        })

    #calcular_carrito(carrito)
    actualizar_carrito_sesion(carrito)
    # Devuelve solo el número de productos para HTMX
    #return f"{sum(i['cantidad'] for i in carrito)}"
    #return f"{sum(i['id'] for i in carrito)}"
    return str(len(carrito))

@app1.route('/ver_carrito', methods=["GET", "POST"])
def ver_carritox():
    carrito = session.get('carrito', [])
    if request.method == "POST":
        prod_id_form = int(request.form['prod_id_form'])
        cantidad = int(request.form['cantidad'])
        #prod = Articulos.query.get_or_404(prod_id_form)
        prod_id = Articulos.query.get_or_404(prod_id_form) #Evita errores si alguien manipula el product_id.
        for x in carrito:
            if x["id"] == prod_id_form:
                x["cantidad"] = min(max(cantidad, 1),prod_id.stock) #la cantidad nunca va hacer menor que 1 ni mayor a stock
                if cantidad > prod_id.stock: # mensajes solamente
                    flash(f"Stock máximo: {prod_id.stock}")
                #else: flash("Cantidad actualizada correctamente")
                break  # MUY IMPORTANTE
        #calcular_carritox(carrito) # 🔥 CALCULAR TAMBIÉN EN POST
        #return redirect(url_for('fun_ini.ver_carritox'))
    #calcular_carrito(carrito) # 🔥 CALCULAR TAMBIÉN EN GET
    actualizar_carrito_sesion(carrito)
    return render_template("index/carrito.html",cart=carrito,subtotal=session["subtotal"],iva=session["iva"],
        total_a_pagar=session["total"])
    #return render_template("index/carrito.html",cart=carrito,subtotal=session.get("subtotal", 0),
    #                    iva=session.get("iva", 0),total=session.get("total", 0))

@app1.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    carrito = [x for x in session.get('carrito', []) if x['id'] != product_id]
    session['carrito'] = carrito
    #calcular_carrito(carrito)
    actualizar_carrito_sesion(carrito)
    return redirect(url_for('fun_ini.ver_carritox'))

#@app1.route('/detalles/<int:id>')
@app1.get('/detalles/<int:id>')
def detallesx(id):
    producto = Articulos.query.get_or_404(id)
    return render_template("index/detalles.html", product=producto)

############################ PAGAR ############################)
#@app1.route('/pagar', methods=["POST"])
@app1.post('/pagar')
def pagarx():
    pedido = Pedido(user_id=session["id"])
    try:
        productos_detalle, subtotal, iva, total = procesar_totales_carrito_stripe(session["carrito"])
        pedido.productos = productos_detalle
        pedido.subtotal = subtotal
        pedido.iva = iva
        pedido.total = total

        db.session.add(pedido)
        db.session.commit()
        session["pedido_id"] = pedido.id  # para usar luego en la página de gracias
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('fun_ini.ver_carritox'))

    line_items = []
    for p in pedido.productos: # o como guardes imagen
        #img_url = url_for("static",filename=f"img/{p['prod_id']}.jpg", _external=True)
        #img_url = url_for("static", filename=f"img/{p['img']}", _external=True)
        #img_url = url_for('static',filename='img/' + p['img'],_external=True)
        img_url = url_for('static',filename=p['img1'],_external=True)
        print(f"Imagen URL: {img_url}")  # Verifica que la URL es correcta
        # unit_amount = subtotal + iva POR UNIDAD
        #unit_amount = int(Decimal(p["subtotal"]) + Decimal(p["iva"]))  # en dólares
        #unit_amount_cents = int(unit_amount * 100)  # convertir a centavos
        #unit_amountx = int(Decimal(p["total"]) * 100),
        unit_amountx = int(float(p["total"]) * 100)  # ✅ convertir a float antes de *100
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    #"name": p["name"],
                    "name": " va a pagar: " + p['name'],
                    #"images": [img_url], # URL de la imagen del producto
                    #"images": p["img"], # URL de la imagen del producto
                },
                # Stripe exige INT en centavos
                #"unit_amount": unit_amount_cents,
                "unit_amount" : unit_amountx,

            },
            "quantity": p["cantidad"],
        })

    stripe.api_key = os.getenv("STRIPE_KEY")
    checkout_sessionx = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items, # Aquí pasamos todos los productos
        mode="payment",
        success_url=url_for('fun_ini.graciasx', _external=True),
        cancel_url=url_for('fun_ini.ver_carritox', _external=True)
        #success_url="https://app1-ey6x.onrender.com/gracias",  # Página de éxito
        #cancel_url="https://app1-ey6x.onrender.com/carrito"  # Página de cancelación
    )
    return redirect(checkout_sessionx.url, code=303)
    #return redirect(url_for('fun_ini.ver_carritox'))

RUTA_FACTURAS = "D:/dev/"
def generar_factura_pdf(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        cliente = pedido.usuario  # ✅ relación correcta
        archivo = os.path.join(RUTA_FACTURAS, f"factura_{pedido_id}.pdf")
        doc = SimpleDocTemplate(
            archivo,
            pagesize=letter,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=18
        )
        elements = []
        styles = getSampleStyleSheet()

        # ================= ENCABEZADO =================
        encabezado = [
            ["FACTURA", "", "", "", f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            [f"Cliente / Razón Social: {cliente.name}", "", "", "", f"Pedido ID: {pedido.id}"],
            [f"RUC / Cédula: {cliente.ced_ruc}", "", "", "", ""]
        ]

        table_encabezado = Table(encabezado, colWidths=[120, 100, 100, 80, 80])
        table_encabezado.setStyle(TableStyle([
            ('SPAN', (0,0), (3,0)),
            ('SPAN', (0,1), (3,1)),
            ('SPAN', (0,2), (3,2)),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))

        elements.append(table_encabezado)
        elements.append(Spacer(1, 12))

        # ================= PRODUCTOS =================
        data = [["Producto", "Precio Unit.", "Cantidad", "IVA", "Total"]]

        for prod in pedido.productos:
            data.append([
                prod["name"],
                f"${prod['precio_unitario']}",
                str(prod["cantidad"]),
                f"${prod['iva']}",
                f"${prod['total']}",
            ])

        # ================= TOTALES =================
        data.append(["", "", "", "SUBTOTAL:", f"${pedido.subtotal}"])
        data.append(["", "", "", "IVA:", f"${pedido.iva}"])
        data.append(["", "", "", "TOTAL:", f"${pedido.total}"])

        table = Table(data, colWidths=[180, 90, 60, 80, 80])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,-3), (-1,-1), 'Helvetica-Bold'),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        footer = Paragraph("¡Gracias por su compra!", styles["Normal"])
        elements.append(footer)

        doc.build(elements)
        return True

    except Exception as e:
        print("ERROR AL CREAR PDF:", e)
        return False

@app1.get('/gracias')
def graciasx():
    pedido_id = session.get("pedido_id")
    pedido = Pedido.query.get_or_404(pedido_id)

    # Descontar stock usando productos ya procesados
    for item in pedido.productos:
        producto = Articulos.query.get(item["id"])
        if producto:
            producto.stock -= int(item["cantidad"])
    db.session.commit()

    # Generamos factura y limpiamos sesión
    generar_factura_pdf(pedido_id)
    session.pop("carrito", None)
    session.pop("pedido_id", None)
    return render_template("index/gracias.html", pedido=pedido)

'''RUTA_FACTURAS = "D:/dev/"
def generar_factura_pdf():
    try:
        pedido_id = session.get('pedido_id')
        carrito = session.get('carrito', [])

        if not pedido_id or not carrito:
            raise ValueError("No hay datos para generar factura")

        # Datos del pedido y cliente
        pedido = Pedido.query.get(pedido_id)
        cliente = pedido.usuariox
        nombre_o_razon = cliente.name
        cedula_o_ruc = cliente.ced_ruc

        archivo = os.path.join(RUTA_FACTURAS, f"factura_{pedido_id}.pdf")
        doc = SimpleDocTemplate(archivo, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []

        # Encabezado
        encabezado = [
            [f"FACTURA", "", "", "", f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            [f"Cliente / Razón Social: {nombre_o_razon}", "", "", "", f"Pedido ID: {pedido_id}"],
            [f"RUC / Cédula: {cedula_o_ruc}", "", "", "", ""]
        ]
        table_encabezado = Table(encabezado, colWidths=[120, 100, 100, 80, 80])
        table_encabezado.setStyle(TableStyle([
            ('SPAN', (0,0), (3,0)),
            ('SPAN', (0,1), (3,1)),
            ('SPAN', (0,2), (3,2)),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12)
        ]))
        elements.append(table_encabezado)
        elements.append(Spacer(1,12))

        # Tabla de productos
        data = [["Nombre", "Precio Unitario", "Cantidad", "IVA", "Precio+IVA"]]
        total_iva = 0
        total_precio_iva = 0
        for prod in carrito:
            nombre = prod['name']
            precio_unit = round(prod['precio'], 2)
            cantidad = prod['cantidad']
            iva = round(precio_unit * 0.12 * cantidad, 2)
            total = round(precio_unit * cantidad + iva, 2)
            total_iva += iva
            total_precio_iva += total
            data.append([nombre, f"${precio_unit:.2f}", str(cantidad), f"${iva:.2f}", f"${total:.2f}"])

        # Totales al final
        data.append(["", "", "", "TOTAL IVA:", f"${total_iva:.2f}"])
        data.append(["", "", "", "TOTAL:", f"${total_precio_iva:.2f}"])

        table = Table(data, colWidths=[180, 100, 60, 80, 80])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,-2), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),
        ]))
        elements.append(table)
        # Footer
        styles = getSampleStyleSheet()
        footer = Paragraph("¡Gracias por su compra en nuestra tienda!", styles['Normal'])
        elements.append(Spacer(1,12))
        elements.append(footer)
        doc.build(elements)
        return True
    except Exception as e:
        print("ERROR AL CREAR PDF:", e)
        return False'''

'''@app1.route('/gracias')
def graciasx():
    carrito = session.get('checkout_carrito', [])
    total = session.get('checkout_total', 0)
    # 🔹 CREAR PEDIDO
    pedido = Pedido(usuario_id=session.get('id'))
    pedido.add_productos(carrito)
    db.session.add(pedido)
    db.session.commit()
    generar_factura_pdf()
    # limpiar carrito
    session.pop('carrito', None)
    session.pop('total', None)
    session.pop('checkout_carrito', None)
    session.pop('checkout_total', None)
    return render_template("index/gracias.html", pedido=pedido)'''

#############################################################

'''def calcular_carritox(carrito):
    subtotal = 0
    iva_total = 0
    total = 0

    for item in carrito:
        sub = item["precio"] * item["cantidad"]
        iva = sub * 0.12
        total_item = sub + iva

        item["subtotal"] = round(sub, 2)
        item["iva"] = round(iva, 2)
        item["total"] = round(total_item, 2)

        subtotal += sub
        iva_total += iva
        total += total_item

    session["carrito"] = carrito
    session["subtotal"] = round(subtotal, 2)
    session["iva"] = round(iva_total, 2)
    session["total"] = round(total, 2)
    session.modified = True'''

'''@app1.get("/")
@app1.get('/inicio')
@app1.get('/inicio/<int:catidx>')
@app1.get('/inicio/<int:catidx>/<int:subcatidx>')
def iniciox(catidx=None, subcatidx=None):
    cat_all = Cat.query.options(joinedload(Cat.subcats).joinedload(Subcat.articulosx)).all()
    cat_id = next((x for x in cat_all if x.id == catidx), cat_all[0]) if catidx else cat_all[0]
    subcat_id = next((x for x in cat_id.subcats if x.id == subcatidx), cat_id.subcats[0] if cat_id.subcats else None)
    arts_id = subcat_id.articulosx if subcat_id else []
    # Detecta si es petición HTMX
    htmx_request = "HX-Request" in request.headers
    return render_template("index/1mujer.html",cat_all=cat_all,cat_id=cat_id,subcategoria=subcat_id,arts_id=arts_id,
    session=session, htmx_only=htmx_request)'''
###################################################################

'''@app1.route("/", methods=["GET", "POST"])
@app1.route('/inicio', methods=["GET", "POST"])
@app1.route('/inicio/<int:catidx>', methods=["GET", "POST"])
@app1.route('/inicio/<int:catidx>/<int:subcatidx>', methods=["GET", "POST"])
def iniciox(catidx=None, subcatidx=None):
    cat_all = Cat.query.options(joinedload(Cat.subcats).joinedload(Subcat.articulosx)).all()
    
    cat_id = next((x for x in cat_all if x.id == catidx), cat_all[0]) if catidx else cat_all[0]
    subcat_id = next((x for x in cat_id.subcats if x.id == subcatidx), cat_id.subcats[0] if cat_id.subcats else None)

    arts_id = subcat_id.articulosx if subcat_id else []

    carrito = session.get('carrito', [])
    if request.method == "POST" and request.form.get('accion') == 'add':
        prod_id_form = int(request.form['prod_id_form'])
        cantidad = int(request.form['cantidad'])
        prod_id = Articulos.query.get_or_404(prod_id_form) # mala practica -> producto = Articulos.query.get(product_id)
        for x in carrito:
            if x["id"] == prod_id_form:
                # min() hace que la cantidad del carrito + la del formulario nunca se pasen del stock
                x["cantidad"] = min(x["cantidad"] + cantidad, prod_id.stock)
                break
        else: # El else se ejecuta solo si el for NO hizo break O sea: si no se encontró el producto
            carrito.append({
                'id': prod_id.id,
                'name': prod_id.name,
                'precio': prod_id.precio,
                'img1': prod_id.img1,
                'stock': prod_id.stock,
                'cantidad': min(cantidad, prod_id.stock) #'cantidad': cantidad
            })
        calcular_carrito(carrito)
        return redirect(url_for('fun_ini.iniciox', catidx=catidx,subcatidx=subcatidx))
    return render_template("index/1mujer.html",
                           cat_all=cat_all,
                           cat_id=cat_id,
                           subcategoria=subcat_id,
                           arts_id=arts_id,
                           cart=session.get('carrito', []),
                           total=session.get('total', 0)) #,msg=msg'''

#############################################
'''@app1.post("/add")
def addx():
    carrito = session.get('carrito', [])
    if request.method == "POST" and request.form.get('accion') == 'add':
        prod_id_form = int(request.form['prod_id_form'])
        cantidad = int(request.form['cantidad'])
        prod_id = Articulos.query.get_or_404(prod_id_form) # mala practica -> producto = Articulos.query.get(product_id)
        for x in carrito:
            if x["id"] == prod_id_form:
                # min() hace que la cantidad del carrito + la del formulario nunca se pasen del stock
                x["cantidad"] = min(x["cantidad"] + cantidad, prod_id.stock)
                break
        else: # El else se ejecuta solo si el for NO hizo break O sea: si no se encontró el producto
            carrito.append({
                'id': prod_id.id,
                'name': prod_id.name,
                'precio': prod_id.precio,
                'img1': prod_id.img1,
                'stock': prod_id.stock,
                'cantidad': min(cantidad, prod_id.stock) #'cantidad': cantidad
            })
        calcular_carrito(carrito)
        return redirect(url_for('fun_ini.iniciox'))
    return render_template("index/1mujer.html",cart=session.get('carrito', []),total=session.get('total', 0))'''

'''@app1.post("/add")
def addx():
    product_id = request.form.get("prod_id_form", type=int)
    cantidad = request.form.get("cantidad", type=int, default=1)

    carrito = session.get("carrito", [])
    prod = Articulos.query.get_or_404(product_id)

    for x in carrito:
        if x["id"] == product_id:
            x["cantidad"] = min(x["cantidad"] + cantidad, prod.stock)
            break
    else:
        carrito.append({
            "id": prod.id,
            "name": prod.name,
            "precio": prod.precio,
            "img1": prod.img1,
            "stock": prod.stock,
            "cantidad": min(cantidad, prod.stock)
        })

    calcular_carrito(carrito)

    return render_template(
        "index/1mujer.html",
        cart=carrito
    )'''