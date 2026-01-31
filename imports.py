from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, current_app ,render_template, redirect, url_for, request, \
session, make_response, abort, json, Blueprint, flash, send_file, Response

from flask_sqlalchemy import SQLAlchemy

#JSON,
from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, Numeric, Float, Boolean, \
DECIMAL, DateTime, Text, select, text, create_engine

from sqlalchemy.orm import backref, joinedload, join, relationship

import os
from dotenv import load_dotenv

from werkzeug.utils import secure_filename

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

import stripe

from flask_wtf.csrf import CSRFProtect, CSRFError   #from flask_wtf import FlaskForm,CSRFProtect ## pip install Flask-WTF
#from flask_wtf.csrf import CSRFError

from modelo5 import db, init_db, Usuario, Cat, Subcat, Articulos, Pedido
#from modelo5 import *
# Esto es para usar JSON en la base de datos (requiere PostgreSQL o base de datos compatible)
#from sqlalchemy.dialects.postgresql import JSON

from fun_user import app0
from fun_ini import app1
from fun_art import app2

# No debes crear la app en este archivo
# app = Flask(__name__, static_folder="static", template_folder="templates")
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' 
# db.init_app(app)

"""
{% if not htmx_only %}
<div id="productos" style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px;">
    {% endif %}
    {% for a in arts_id %}
    <div style="display:block;text-align:center;">
        <a href="{{ url_for('fun_ini.detallesx', id=a.id) }}">
            <img class="img_galeria" src="{{ url_for('static', filename=a.img1) }}">
        </a>
        <div style="display:flex;gap:20px;justify-content:center;">
            <p>{{ a.name }}</p>
            <p>${{ a.precio }} USD</p>
            <p>stock {{ a.stock }}</p>
        </div>

        {% if session.get("admin") %}
        <!--<form method="post" action="{{ url_for('fun_ini.addx') }}">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <input type="hidden" name="prod_id_form" value="{{ a.id }}">
            <input type="hidden" name="cantidad" value="1">
            <input type="hidden" name="accion" value="add">
        <button class="boton1" type="submit">
                        <img style="width:25px;height:20px"
                             src="{{ url_for('static', filename='iconos/carrito.png') }}">
                        Agregar
                    </button>
        </form>-->
        <form hx-post="{{ url_for('fun_ini.addx') }}" hx-target="#cart-counter" hx-swap="innerHTML" method="post">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <input type="hidden" name="prod_id_form" value="{{ a.id }}">
            <input type="hidden" name="cantidad" value="1">
            <button class="boton1" type="submit">
                <img style="width:25px;height:20px" src="{{ url_for('static', filename='iconos/carrito.png') }}">
                Agregar
            </button>
        </form>

        {% else %}
        <a href="{{ url_for('fun_user.loginx') }}">
            <button class="boton1">
                <img style="width:25px;height:20px" src="{{ url_for('static', filename='iconos/carrito.png') }}">
                Agregar
            </button>
        </a>
        {% endif %}
    </div>
    {% endfor %}
    {% if not htmx_only %}
</div>
{% endif %}
"""