import json
from dbs.dbs import *
from imgCv2 import takePhoto
from flask import Flask, flash, render_template as render, redirect, url_for, request

with open("dbs/config.json") as config_file:
    keys_config = json.load(config_file)

app = Flask(__name__, static_url_path='/static')
app.secret_key = keys_config['SECRET_KEY']


@app.route("/")
def home():
    try:
        getUserInfo = personalData()
    except:
        return redirect(url_for('loadFile'))

    LocalAll = "SELECT * FROM Location"
    locations = askAll(LocalAll)
    shelfAll = "SELECT * FROM Shelf"
    shelfs = askAll(shelfAll)
    containerAll = "SELECT * FROM Container"
    containers = askAll(containerAll)

    return render("home.html", title="Home", getUserInfo=getUserInfo, locations=locations, shelfs=shelfs, containers=containers)


@app.route("/createLocation", methods=['POST', 'GET']) 
def createLocation():
    Locals = "SELECT * FROM Location"
    locations = askAll(Locals)
    
    if request.method == "POST":
        location = {'espacio':request.form['espacio'], 'nivel':request.form['nivel'], 'lugar':request.form['lugar'], 'direccion':request.form['direccion'], 'ciudad':request.form['ciudad'], 'depto':request.form['depto']}
        dbCreateLocation(location)
        return redirect('/createShelf')

    return render("containLog/createLocation.html", title="Crear Localidad", locations=locations)


@app.route("/createShelf", methods=['POST', 'GET']) 
def createShelf():
    LocalAll = "SELECT * FROM Location"
    locations = askAll(LocalAll)
    shelfAll = "SELECT * FROM Shelf"
    shelfs = askAll(shelfAll)

    if request.method == "POST":
        shelf = {'estante':request.form['estante'], 'entrepano':request.form['entrepano'], 'id_location':request.form['location']}
        dbCreateShelf(shelf)
        return redirect('/createContainer')

    return render("containLog/createShelf.html", title="Create Container", locations=locations, shelfs=shelfs)


@app.route("/createContainer", methods=['POST', 'GET'])
def createContainer():
    LocalAll = "SELECT * FROM Location"
    locations = askAll(LocalAll)
    shelfAll = "SELECT * FROM Shelf"
    shelfs = askAll(shelfAll)
    containerAll = "SELECT * FROM Container"
    containers = askAll(containerAll)

    if request.method == "POST":
        container = {'indice':request.form['indice'], 'numero':request.form['numero'], 'contenedor':request.form['contenedor'], 'id_shelf':request.form['shelf'], 'id_location':request.form['location']}
        dbCreateContainer(container)
        return redirect('/')

    return render("containLog/createContainer.html", title="Create Container", locations=locations, shelfs=shelfs, containers=containers)


@app.route("/createArticle", methods=['POST', 'GET'])
def createArticle():
    LocalAll = "SELECT * FROM Location"
    locations = askAll(LocalAll)
    shelfAll = "SELECT * FROM Shelf"
    shelfs = askAll(shelfAll)
    containerAll = "SELECT * FROM Container"
    containers = askAll(containerAll)
    articleAll = "SELECT * FROM Article"
    articles = askAll(articleAll)

    if request.method == "POST":
        name = request.form['name']
        id = request.form['contenedor']
        sqlquery = "SELECT * FROM Container WHERE id = ?"
        container = askOne(sqlquery, int(id))

        objectName = container[3] + "_" + container[1] + container[2] + "_" + name
        img_name = takePhoto(objectName)
        
        article = {'photo':img_name,'type':request.form['type'], 'name':request.form['name'], 'description':request.form['description'], 'id_container':request.form['contenedor'], 'id_shelf':request.form['shelf'], 'id_location':request.form['location']}

        dbCreateArticle(article)
        return redirect('/')

    return render("containLog/createArticle.html", title="Create Articulo", locations=locations, shelfs=shelfs, containers=containers, articles=articles)


# ************** USER *************
@app.route('/enter', methods=['POST', 'GET']) 
def enter():
    getUserInfo = personalData()
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        try:
            conn = db_conn()
            getUser = conn.execute("SELECT * FROM users WHERE email =?", (email,)).fetchone()
            conn.commit()
            conn.close()
            
            if getUser[1] == passwordHash:
                session['user'] = getUser[0]
                session['loged'] = "Yes"
                return redirect(url_for('dashboard'))
            else:
                flash('Something went wrong, try again!')
                return render("userLog/enter.html", title="Volunteer", getUserInfo=getUserInfo)
        except:
            session['user'] = ""
            session['loged'] = "No"
            flash('Record not found, Register or try again!')
            return render("userLog/add_user.html", title="Volunteer", getUserInfo=getUserInfo)

    return render("userLog/enter.html", title="Login", getUserInfo=getUserInfo)


@app.route('/loadFile', methods=["POST", "GET"]) 
def loadFile():
    getUserInfo = personalData()
    if request.method == "POST":
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            try:
                email = request.form['email']
                passwordHash = hashlib.sha256(password.encode()).hexdigest()
                conn = db_conn()
                conn.execute("CREATE TABLE users (email, passwordHash)")
                conn.commit()
                conn.execute("INSERT INTO users (email, passwordHash) VALUES (?, ?)", (email, passwordHash))
                conn.commit()
                conn.close()
            except:
                pass

            fileinn = request.files.get("fileinn")
            dfSheets = pd.ExcelFile(fileinn).sheet_names
            for sheet in dfSheets:
                if sheet != "keys":
                    df = pd.read_excel(fileinn, sheet)
                    df.to_sql(name=sheet, con=conn, if_exists="append", index=False)

            session['user'] = email
            session['loged'] = "Yes"
            flash('The register was successful and you are login to!')
            return redirect(url_for('dashboard'))
        else:
            flash('The passwords are not the same, try again!')
            return redirect(url_for('loadFile'))

    return render("userLog/loadFile.html")


@app.route("/logout") 
def logout():
    flash("You have been logged out", "info")
    session['user'] = ""
    session['loged'] = "No"
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
