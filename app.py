import pymysql as pymysql
from flask import Flask, render_template, request, redirect, session


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return render_template('templates/home.html')


@app.route('/about')
def about():
    return render_template('templates/about.html')


@app.route('/contact')
def contact():
    return render_template('templates/contact.html')


@app.route('/register_car', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # capture the form values
        car_type = request.form['CarType']
        make = request.form['Make']
        vregno = request.form['VehicleRegNo']
        drvname = request.form['DriverName']
        drvcntct = request.form['DriverContact']
        year = request.form['YearOfMake']
        drvlicense = request.form['DriverLicenseNo']

        # connect to the database
        # arguments(server, username-root, password-blank, dbName)
        con = pymysql.connect("localhost", "root", "", "blazecar")
        crs = con.cursor()
        sql = " INSERT INTO `cars` (`CarType`, `Make`, `VehicleRegNo`, `DriverName`, `DriverContact`, `YearOfMake`, `DriverLicenseNo`) VALUES (%s, %s, %s, %s, %s, %s, %s ) "

        # execute query using a tuple
        try:
            crs.execute(sql, (car_type, make, vregno,
                              drvname, drvcntct, year, drvlicense))
            # enforce the values
            con.commit()
            return render_template('templates/register_car.html', msg="Successfully saved")
        except:
            # revert to previous page in case of corrupt values
            con.rollback()
            return render_template('templates/register_car.html', msg="Failed")
    else:
        return render_template('templates/register_car.html')


@app.route('/search_car', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        vregno = request.form['VehicleRegNo']

        # connection to the db
        con = pymysql.connect("localhost", "root", "", "blazecar")

        # create a cursor to establish connection to the db and to actually process the query
        cur = con.cursor()
        # we use %s here coz this is where sql injection can occur
        searchquery = "SELECT * FROM cars where VehicleRegNo = %s"

        # execute query
        cur.execute(searchquery, vregno)

        if cur.rowcount == 0:  # rowcount-function that counts the records found but does not display the number
            return render_template('search_car.html', ms="No Records found")
        else:
            rows = cur.fetchall()  # gets actual array in a list format
            return render_template('search_car.html', rows=rows)
    else:
        return render_template('templates/search_car.html')


@app.route('/view_cars')
def view():
    # no post required, only pulling all records form the db

    # connect to db
    con = pymysql.connect("localhost", "root", "", "blazecar")
    curs = con.cursor()

    # sql query executed
    viewqry = "SELECT * FROM cars"
    curs.execute(viewqry)

    if curs.rowcount == 0:
        return render_template("templates/view_cars.html", ms="No records found")
    else:
        rows = curs.fetchall()
        return render_template('templates/view_cars.html', rows=rows)


@app.route('/earnings', methods=['GET', 'POST'])
def earnings():
    if request.method == 'POST':
        vreg = request.form['VehicleRegNo']
        amnt = request.form['Amount']
        '''date = request.form['Date']'''

        con = pymysql.connect("localhost", "root", "", "blazecar")
        crs = con.cursor()
        sql = "INSERT INTO `earnings` (`VehicleRegNo`, `Amount`) VALUES(%s, %s)"

        try:
            crs.execute(sql, (vreg, amnt))
            # enforce the values
            con.commit()
            return render_template('templates/earnings.html', msg="Successfully saved")
        except:
            # revert to previous page in case of corrupt values
            con.rollback()
            return render_template('templates/earnings.html', msg="Failed")
    else:
        return render_template('templates/earnings.html')


@app.route('/ttlearnings', methods=['POST', 'GET'])
def ttlearnings():
    if request.method == 'POST':

        vregno = request.form['VehicleRegNo']

        # connection to the db
        con = pymysql.connect("localhost", "root", "", "blazecar")

        # create a cursor to establish connection to the db and to actually process the query
        cur = con.cursor()
        # we use %s here coz this is where sql injection can occur
        searchquery = "SELECT * FROM earnings where VehicleRegNo = %s"

        # execute query
        cur.execute(searchquery, vregno)

        if cur.rowcount == 0:  # rowcount-function that counts the records found but does not display the number
            return render_template('ttlearnings.html', ms="No Records found")
        else:
            rows = cur.fetchall()  # gets actual array in a list format
            return render_template('templates/ttlearnings.html', rows=rows)
    else:
        return render_template('templates/ttlearnings.html')


if __name__ == '__main__':
    app.run()
