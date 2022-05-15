from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TimeField, TextAreaField
import sqlite3

app = Flask(__name__)
app.debug = True
app.secret_key = "woeuifhdfjvbaoehgv=qieurgvq"

class ZavodnikForm(FlaskForm):
    jmeno = StringField("Jméno")
    prijmeni = StringField("Příjmení")
    cislo = IntegerField("Číslo")
    cas = TimeField("Dosažený čas", format='%H:%M:%S')
    poznamka = TextAreaField("Poznámka")


@app.route('/')
def vysledky():
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM vysledky")
    vysledky = cur.fetchall()
    return render_template('vysledky.html', vysledky = vysledky)



@app.route('/pridat', methods=['GET', 'POST'])
def zavodnik():
    form = ZavodnikForm()
    zad_jmeno = form.jmeno.data
    zad_prijmeni = form.prijmeni.data
    zad_cislo = form.cislo.data
    zad_cas = str(form.cas.data)
    zad_poznamka = form.poznamka.data

    if form.validate_on_submit():
        con = sqlite3.connect('vysledky.db')
        cur = con.cursor()
        cur.execute("INSERT INTO vysledky(jmeno, prijmeni, cislo, cas, poznamka) VALUES(?, ?, ?, ?, ?)", (zad_jmeno, zad_prijmeni, zad_cislo, zad_cas, zad_poznamka))
        con.commit()
        con.close()
        return redirect('/')

    return render_template('zavodnik.html', form=form)

@app.route('/prijmeni')
def prijmeni():
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM vysledky ORDER BY prijmeni")
    vysledky = cur.fetchall()
    prp="Seřazení podle příjmení vzestupně"
    con.close()
    return render_template('prijmeni.html', vysledky = vysledky,prp=prp)

@app.route('/cas')
def cas():
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM vysledky ORDER BY cas")
    vysledky = cur.fetchall()
    prp="Seřazení podle času vzestupně"
    con.close()
    return render_template('cas.html', vysledky = vysledky,prp=prp)

@app.route('/prijmeniDesc')
def prijmeniDesc():
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM vysledky ORDER BY prijmeni DESC")
    prp="Seřazení podle příjmení sestupně"
    vysledky = cur.fetchall()
    con.close()
    return render_template('prijmeni.html', vysledky = vysledky,prp=prp)

@app.route('/casDesc')
def casDesc():
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM vysledky ORDER BY cas DESC")
    vysledky = cur.fetchall()
    prp="Seřazení podle času sestupně"
    con.close()
    return render_template('cas.html', vysledky = vysledky, prp=prp)

@app.route('/smazani/<int:id_zavodnika>')
def smazani(id_zavodnika):
    con = sqlite3.connect('vysledky.db')
    cur = con.cursor()
    cur.execute("DELETE FROM vysledky WHERE cislo=?", (id_zavodnika,))
    vysledky = cur.fetchall()
    con.commit()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    app.run()