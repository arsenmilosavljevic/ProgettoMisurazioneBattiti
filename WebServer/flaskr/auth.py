from flask import Blueprint, g, redirect, render_template, request ,session as br_sesion, url_for
from sqlalchemy import SQLAlchemy
import hashlib
import db.models as models

bp=Blueprint("auth", __name__, url_prefix="/auth")

# region LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('homepage'))

    error = None

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        utente = Utente.query.filter_by(username=username).first()

        if utente and check_password_hash(utente.password, password):
            session['username'] = username
            return redirect(url_for('homepage'))
        else:
            error = 'Username o password non corretti.'

    return render_template('auth/login.html', error=error)

#region REGISTER
@bp.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if 'username' in session:
        return redirect(url_for('homepage'))

    error = None
    success = None

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm  = request.form['confirm']
        nome     = request.form['nome'].strip()
        cognome  = request.form['cognome'].strip()
        eta      = request.form['eta'].strip()

        if not username or not password or not nome or not cognome or not eta:
            error = 'Tutti i campi sono obbligatori.'

        elif len(username) < 3:
            error = 'Username troppo corto.'

        elif len(password) < 6:
            error = 'Password troppo corta.'

        elif password != confirm:
            error = 'Password non coincidono.'

        elif not eta.isdigit() or not (1 <= int(eta) <= 120):
            error = "Età non valida."

        elif Utente.query.filter_by(username=username).first():
            error = 'Username già in uso.'

        else:
            nuovo = Utente(
                username=username,
                password=generate_password_hash(password),
                nome=nome,
                cognome=cognome,
                eta=int(eta),
                created_at=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            )

            db.session.add(nuovo)
            db.session.commit()

            success = "Registrazione completata!"

    return render_template('auth/registrazione.html', error=error, success=success)

# region LOGOUT
@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
