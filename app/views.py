from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from sqlalchemy import and_
from app import models, db, app, forms, mail
from flask.ext.mail import Message, Mail
from config import ADMINS, HOST_BASE, MSG_TEXT
import json
import datetime

@app.route("/", methods=['POST', 'GET'])
def index():
    form = forms.CredentialsForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        surname = form.surname.data.strip()
        email = form.email.data.strip()

        u = models.Aasi(name=name, surname=surname, email=email)
        print u
        db.session.add(u)
        db.session.commit()

        _send_verification_mail(u)

        return redirect(url_for('form_success'))

    return render_template('index.html', form=form)

@app.route("/verify/<verification_str>")
def verify_email(verification_str):
    u = models.Aasi.query.filter_by(verification_string=verification_str).first()
    if u:
        u.verified = True
        db.session.commit()
        return render_template('success.html')

    return "your email is not yet verified!"

@app.route("/success", methods=['GET'])
def form_success():
    return render_template('wait_for_verification.html')
    #return redirect(url_for('debug'))

@app.route("/pdf/<version>")
@app.route("/pdf")
def generate_pdf(version=None):
    import StringIO
    from flask_weasyprint import HTML, render_pdf

    now = datetime.datetime.now().strftime('%d.%m.%Y');

    #users = models.Aasi.query.all()

    # fetch the latest print_version from the database
    latest = db.session.query(db.func.max(models.Aasi.print_version)).one()[0]

    if version == None or version == 0:
        # if no version parameter given, print all
        users = models.Aasi.query.filter_by(verified=True)
    elif int(version) <= latest:
        # otherwise fetch older print versions and create the pdf
        users = models.Aasi.query.filter_by(verified=True, print_version=int(version))
    else:
        # else, get all the unprinted ones and append their version
        users = models.Aasi.query.filter_by(verified=True, print_version=0)

        for user in users:
            user.print_version = latest+1
            db.session.add(user)
        db.session.commit()

        # TODO: find a way to refresh the session?
        users = models.Aasi.query.filter_by(verified=True, print_version=latest+1)

    html = render_template('piikki.html', users=users, now=now)

    return render_pdf(HTML(string=html))
    #return html

    # TODO: send the pdf to all the admins
    # TODO: update revision

@app.route("/debug")
def debug():
    users = models.Aasi.query.all()

    res = request.args.get('reset')
    print res
    if res == 'True':
        for user in users:
            user.print_version = 0
            db.session.add(user)
        db.session.commit()


    return jsonify(json_list = [u.as_dict() for u in users])

def _send_verification_mail(aasi):
    # TODO: modify the layout of the email
    msg = Message('Askipiikin verifiointi', sender=ADMINS[0])
    msg.add_recipient(aasi.email)

    verify_link = "<a href='" + HOST_BASE + url_for('verify_email', verification_str=aasi.verification_string) + "'>verifioi</a>"

    msg.html = MSG_TEXT.format(link=verify_link)

    mail.send(msg)
