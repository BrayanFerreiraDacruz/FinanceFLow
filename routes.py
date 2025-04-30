from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Transacao
from . import db

routes = Blueprint('routes', __name__)

def calcular_totais(transacoes):
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'receita')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'despesa')
    saldo = total_entradas - total_saidas
    return total_entradas, total_saidas, saldo

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = current_user.id
    usuario = User.query.get(user_id)

    if request.method == "POST":
        try:
            saldo_informado = float(request.form.get("saldo_informado", 0))
            despesas_informadas = float(request.form.get("despesas_informadas", 0))

            usuario.saldo_informado = saldo_informado
            usuario.despesas_informadas = despesas_informadas
            db.session.commit()
        except:
            flash("Erro ao atualizar saldo/despesas", "danger")

    transacoes = Transacao.query.filter_by(user_id=user_id).order_by(Transacao.data.desc()).all()
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'receita')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'despesa')
    saldo = total_entradas - total_saidas

    return render_template(
        "dashboard.html",
        transacoes=transacoes,
        total_entradas=total_entradas,
        total_saidas=total_saidas,
        saldo=saldo,
        saldo_total=saldo,
        saldo_informado=usuario.saldo_informado or 0,
        despesas_informadas=usuario.despesas_informadas or 0
    )

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user_existente = User.query.filter_by(email=email).first()
        if user_existente:
            flash('Email já cadastrado.', 'warning')
            return redirect(url_for('routes.register'))

        senha_hash = generate_password_hash(senha)
        novo_usuario = User(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login agora.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@routes.route('/logout')
def logout():
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('routes.login'))
