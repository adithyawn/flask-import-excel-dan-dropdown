from flask import Flask, render_template, request, jsonify, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField
from flask_wtf import FlaskForm

from flask_migrate import Migrate
import xlrd
import MySQLdb

# Establish a MySQL connection
database = MySQLdb.connect(
    user='root', password='root', host='localhost', database='sqlalchemy')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kygcdjkddsfiusdlinsdiuodlnkvsbaf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/sqlalchemy'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class KategoriWbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_kategori_wbs = db.Column(db.String(50), unique=True, nullable=False)
    kategori_wbs = db.Column(db.String(50))

    link_kategori_wbs = db.relationship(
        'InputWbs', backref='kategori_wbs', lazy='dynamic')


class WbsSpesifik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wbs_spesifik = db.Column(db.String(50), unique=True, nullable=False)
    wbs_spesifik = db.Column(db.String(50))
    id_kategori_wbs = db.Column(db.String(50))

    link_wbs_spesifik = db.relationship(
        'InputWbs', backref='wbs_spesifik', lazy='dynamic')


class WbsLevel2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wbs_level2 = db.Column(db.String(50), unique=True, nullable=False)
    wbs_level2 = db.Column(db.String(50))
    id_wbs_spesifik = db.Column(db.String(50))

    link_wbs_level2 = db.relationship(
        'InputWbs', backref='wbs_level2', lazy='dynamic')


class WbsLevel3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wbs_level3 = db.Column(db.String(50), unique=True, nullable=False)
    wbs_level3 = db.Column(db.String(50))
    id_wbs_level2 = db.Column(db.String(50))

    # Penulisan WbsLevel3 di backref jadi wbs_level3
    link_wbs_level3 = db.relationship(
        'InputWbs', backref='wbs_level3', lazy='dynamic')


class InputWbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_id_kategori_wbs = db.Column(
        db.String(300), db.ForeignKey('kategori_wbs.id_kategori_wbs'))
    input_id_wbs_spesifik = db.Column(
        db.String(300), db.ForeignKey('wbs_spesifik.id_wbs_spesifik'))
    input_id_wbs_level2 = db.Column(
        db.String(300), db.ForeignKey('wbs_level2.id_wbs_level2'))

    # Penulisan WbsLevel3 di backref jadi wbs_level3, disini terkait pada penulisan ForeignKey
    input_id_wbs_level3 = db.Column(
        db.String(300), db.ForeignKey('wbs_level3.id_wbs_level3'))


class Form(FlaskForm):
    select_kategori_wbs = SelectField('select_kategori_wbs', choices=[])
    select_wbs_spesifik = SelectField('select_wbs_spesifik', choices=[])
    select_wbs_level2 = SelectField('select_wbs_level2', choices=[])
    select_wbs_level3 = SelectField('select_wbs_level3', choices=[])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = Form()
    form.select_kategori_wbs.choices = [
        ("", "---")]+[(i.id_kategori_wbs, i.kategori_wbs) for i in KategoriWbs.query.all()]

    results = db.session.query(InputWbs, WbsLevel3, WbsLevel2, WbsSpesifik, KategoriWbs).select_from(
        InputWbs).join(WbsLevel3).join(WbsLevel2).join(WbsSpesifik).join(KategoriWbs).all()

    return render_template('index.html', form=form, results=results)


@app.route('/submitwbs', methods=['POST'])
def submitwbs():

    form = Form()

    if request.method == 'POST':

        summarywbs = InputWbs(input_id_kategori_wbs=form.select_kategori_wbs.data, input_id_wbs_spesifik=form.select_wbs_spesifik.data,
                              input_id_wbs_level2=form.select_wbs_level2.data, input_id_wbs_level3=form.select_wbs_level3.data)
        db.session.add(summarywbs)
        db.session.commit()

    return redirect(url_for('index'))

######################## JSON #####################


@app.route('/wbs_spesifik/<input_kategori_wbs>')
def wbs_spesifik_by_kategori_wbs(input_kategori_wbs):
    all_wbs_spesifik = WbsSpesifik.query.filter_by(
        id_kategori_wbs=input_kategori_wbs).all()

    wbs_spesifikArray = []
    for wbs_spesifik in all_wbs_spesifik:
        wbs_spesifikObj = {}
        wbs_spesifikObj['id'] = wbs_spesifik.id_wbs_spesifik
        wbs_spesifikObj['name'] = wbs_spesifik.wbs_spesifik
        wbs_spesifikArray.append(wbs_spesifikObj)

    return jsonify({'wbs_spesifik_kategori_wbs': wbs_spesifikArray})
    # return "{}".format(all_wbs_spesifik)


@app.route('/wbs_level2/<input_wbs_spesifik>')
def wbs_level2_by_wbs_spesifik(input_wbs_spesifik):
    all_wbs_level2 = WbsLevel2.query.filter_by(
        id_wbs_spesifik=input_wbs_spesifik).all()

    wbs_level2Array = []
    for wbs_level2 in all_wbs_level2:
        wbs_level2Obj = {}
        wbs_level2Obj['id'] = wbs_level2.id_wbs_level2
        wbs_level2Obj['name'] = wbs_level2.wbs_level2
        wbs_level2Array.append(wbs_level2Obj)

    return jsonify({'wbs_level2_wbs_spesifik': wbs_level2Array})


@app.route('/wbs_level3/<input_wbs_level2>')
def wbs_level3_by_wbs_level2(input_wbs_level2):
    all_wbs_level3 = WbsLevel3.query.filter_by(
        id_wbs_level2=input_wbs_level2).all()

    wbs_level3Array = []
    for wbs_level3 in all_wbs_level3:
        wbs_level3Obj = {}
        wbs_level3Obj['id'] = wbs_level3.id_wbs_level3
        wbs_level3Obj['name'] = wbs_level3.wbs_level3
        wbs_level3Array.append(wbs_level3Obj)

    return jsonify({'wbs_level3_wbs_spesifik': wbs_level3Array})
###################### END JSON ###################

#################### FUNGSI IMPORT EXCEL ####################


@app.route('/submitexcel', methods=['POST'])
def submitexcel():

    if request.method == 'POST':
        fileuploaded = request.form['excelfile']

        # Open the workbook and define the worksheet
        book = xlrd.open_workbook(fileuploaded)
        sheet_infra = book.sheet_by_name("infra")
        sheet_gedung = book.sheet_by_name("gedung")

        # Get the cursor, which is used to traverse the database, line by line
        cursor = database.cursor()

        ####### INFRA ###########

        # KATEGORI WBS INFRA
        query_infra_kategori_wbs = """ REPLACE INTO kategori_wbs (id_kategori_wbs,kategori_wbs) VALUES (%s, %s)"""

        for i in range(1, sheet_infra.nrows):
            id_kategori_wbs = sheet_infra.cell(i, 0).value
            kategori_wbs = sheet_infra.cell(i, 1).value

            # Assign values from each row
            values_infra_kategori_wbs = (id_kategori_wbs, kategori_wbs)

            # Execute sql Query
            cursor.execute(query_infra_kategori_wbs, values_infra_kategori_wbs)

        # WBS SPESIFIK INFRA
        query_infra_wbs_spesifik = """ REPLACE INTO wbs_spesifik (id_wbs_spesifik,wbs_spesifik,id_kategori_wbs) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_infra.nrows):
            id_wbs_spesifik = sheet_infra.cell(i, 2).value
            wbs_spesifik = sheet_infra.cell(i, 3).value
            id_kategori_wbs = sheet_infra.cell(i, 0).value

            # Assign values from each row
            values_infra_wbs_spesifik = (
                id_wbs_spesifik, wbs_spesifik, id_kategori_wbs)

            # Execute sql Query
            cursor.execute(query_infra_wbs_spesifik, values_infra_wbs_spesifik)

        # WBS LEVEL 2 INFRA
        query_infra_wbs_level2 = """ REPLACE INTO wbs_level2 (id_wbs_level2,wbs_level2,id_wbs_spesifik) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_infra.nrows):
            id_wbs_level2 = sheet_infra.cell(i, 4).value
            wbs_level2 = sheet_infra.cell(i, 5).value
            id_wbs_spesifik = sheet_infra.cell(i, 2).value

            # Assign values from each row
            values_infra_wbs_level2 = (
                id_wbs_level2, wbs_level2, id_wbs_spesifik)

            # Execute sql Query
            cursor.execute(query_infra_wbs_level2, values_infra_wbs_level2)

        # WBS LEVEL 3 INFRA
        query_infra_wbs_level3 = """ REPLACE INTO wbs_level3 (id_wbs_level3,wbs_level3,id_wbs_level2) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_infra.nrows):
            id_wbs_level3 = sheet_infra.cell(i, 6).value
            wbs_level3 = sheet_infra.cell(i, 7).value
            id_wbs_level2 = sheet_infra.cell(i, 4).value

            # Assign values from each row
            values_infra_wbs_level3 = (
                id_wbs_level3, wbs_level3, id_wbs_level2)

            # Execute sql Query
            cursor.execute(query_infra_wbs_level3, values_infra_wbs_level3)

        ####### GEDUNG ###########

        # KATEGORI WBS GEDUNG
        query_gedung_kategori_wbs = """ REPLACE INTO kategori_wbs (id_kategori_wbs,kategori_wbs) VALUES (%s, %s)"""

        for i in range(1, sheet_gedung.nrows):
            id_kategori_wbs = sheet_gedung.cell(i, 0).value
            kategori_wbs = sheet_gedung.cell(i, 1).value

            # Assign values from each row
            values_gedung_kategori_wbs = (id_kategori_wbs, kategori_wbs)

            # Execute sql Query
            cursor.execute(query_gedung_kategori_wbs,
                           values_gedung_kategori_wbs)

        # WBS SPESIFIK GEDUNG
        query_gedung_wbs_spesifik = """ REPLACE INTO wbs_spesifik (id_wbs_spesifik,wbs_spesifik,id_kategori_wbs) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_gedung.nrows):
            id_wbs_spesifik = sheet_gedung.cell(i, 2).value
            wbs_spesifik = sheet_gedung.cell(i, 3).value
            id_kategori_wbs = sheet_gedung.cell(i, 0).value

            # Assign values from each row
            values_gedung_wbs_spesifik = (
                id_wbs_spesifik, wbs_spesifik, id_kategori_wbs)

            # Execute sql Query
            cursor.execute(query_gedung_wbs_spesifik,
                           values_gedung_wbs_spesifik)

        # WBS LEVEL 2 GEDUNG
        query_gedung_wbs_level2 = """ REPLACE INTO wbs_level2 (id_wbs_level2,wbs_level2,id_wbs_spesifik) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_gedung.nrows):
            id_wbs_level2 = sheet_gedung.cell(i, 4).value
            wbs_level2 = sheet_gedung.cell(i, 5).value
            id_wbs_spesifik = sheet_gedung.cell(i, 2).value

            # Assign values from each row
            values_gedung_wbs_level2 = (
                id_wbs_level2, wbs_level2, id_wbs_spesifik)

            # Execute sql Query
            cursor.execute(query_gedung_wbs_level2, values_gedung_wbs_level2)

        # WBS LEVEL 3 GEDUNG
        query_gedung_wbs_level3 = """ REPLACE INTO wbs_level3 (id_wbs_level3,wbs_level3,id_wbs_level2) VALUES (%s, %s, %s)"""

        for i in range(1, sheet_gedung.nrows):
            id_wbs_level3 = sheet_gedung.cell(i, 6).value
            wbs_level3 = sheet_gedung.cell(i, 7).value
            id_wbs_level2 = sheet_gedung.cell(i, 4).value

            # Assign values from each row
            values_gedung_wbs_level3 = (
                id_wbs_level3, wbs_level3, id_wbs_level2)

            # Execute sql Query
            cursor.execute(query_gedung_wbs_level3, values_gedung_wbs_level3)

        # Close the cursor
        cursor.close()

        # Commit the transaction
        database.commit()

        # Close the database connection
        # database.close()

    return redirect(url_for('index'))

##################	BATAS IMPORT ####################


if __name__ == '__main__':
    app.run(debug=True)
