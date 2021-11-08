from logging import fatal
from os import pardir
import re
from sys import meta_path
from types import MethodDescriptorType
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from datetime import date, datetime

import json
from werkzeug.datastructures import ContentRange

from werkzeug.wrappers import response


usuarios = list()
publicaciones = list()
sesionOn = False
userActive = ""
password1 = ""
userView = ""
userEdit = ""
postEdit = ""
idPublicacion = 0
simbolosEspeciales = ['!', '#', '$', '%', '&', '/', '@']


class UsuarioIngresa:
    user = ""
    password = ""


class datosUsuario:
    name = ""
    gender = ""
    username = ""
    email = ""
    password = ""


class publicacion:
    id = 0
    type = ""
    url = ""
    category = ""
    date = ""
    owner = ""
    like = 0


class likes:
    username = ""
    noLikes = 0


admin = datosUsuario()
admin.name = "Wiliam Cabrera"
admin.gender = "M"
admin.username = "admin"
admin.email = "admin@ipc1.com"
admin.password = "admin@ipc1"

# user = datosUsuario()
# user.name = "Erick Hernandez"
# user.gender = "M"
# user.username = "Erick"
# user.email = "zeroeh"
# user.password = "123"

# user2 = datosUsuario()
# user2.name = "Fernando Hernandez"
# user2.gender = "M"
# user2.username = "hh"
# user2.email = "zeroeh"
# user2.password = "123"

# usuarios.append(user)
# usuarios.append(user2)

# publi = publicacion()
# publi.id = 10
# publi.type = "imagen"
# publi.url = "https://i.pinimg.com/550x/0c/17/ae/0c17ae80425d53c2dbd359864166e5f9.jpg"
# publi.category = "anime"
# publi.date = "05/11/2021"
# publi.owner = "Erick"
# publi.like = 30

# publi2 = publicacion()
# publi2.id = 11
# publi2.type = "imagen"
# publi2.url = "https://i.pinimg.com/550x/0c/17/ae/0c17ae80425d53c2dbd359864166e5f9.jpg"
# publi2.category = "anime"
# publi2.date = "05/11/2021"
# publi2.owner = "hh"
# publi2.like = 5

# publi3 = publicacion()
# publi3.id = 12
# publi3.type = "imagen"
# publi3.url = "https://i.pinimg.com/550x/0c/17/ae/0c17ae80425d53c2dbd359864166e5f9.jpg"
# publi3.category = "anime"
# publi3.date = "05/11/2021"
# publi3.owner = "hh"
# publi3.like = 100

# publicaciones.append(publi)
# publicaciones.append(publi2)
# publicaciones.append(publi3)

usuarios.append(admin)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Estaesmillavesecreta'
CORS(app)

# CORS(app, resources={r"/*/*": {"orgigins": "*"}})


@app.route('/ObetenerUsuarios', methods=['GET'])
def principal():
    response = []
    for a in usuarios:
        user = {
            "name": a.name,
            "gender": a.gender,
            "username": a.username,
            "email": a.email,
            "password": a.password
        }
        response.append(user)
    return{"status": 200, "data": response}

# Este metodo Obtiene la informacion del cliente
# y busca en la lista usuarios si existen los datos con
# los que se quieren iniciar sesion


@app.route('/inicio', methods=['POST'])
def iniciarSesion():
    if request.method == 'POST':
        content = request.get_json()
        # print(type(content))
        nuevoInicio = UsuarioIngresa()
        nuevoInicio.user = content['usuario']
        nuevoInicio.password = content['password']

        # print(nuevoInicio.user)
        # print(nuevoInicio.password)
        # var= 0

        for a in usuarios:
            # var= var +1
            # print (var)
            if a.username == nuevoInicio.user and a.password == nuevoInicio.password:
                if a.username == "admin" and a.password == "admin@ipc1":
                    globals()['sesionOn'] = True
                    globals()['userActive'] = a.username
                    print(userActive)
                    return {"message": "ok"}
                else:
                    # print (a.username + " " + a.password)
                    globals()['sesionOn'] = True
                    globals()['userActive'] = a.username
                    return {"message": "ok1"}

        return {"message": "Usuario o contraseña incorrectos"}


# Este metodo crea los usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registrarUsuario():

    if request.method == 'POST':
        content = request.get_json()
        nuevoUsuario = datosUsuario()
        nuevoUsuario.name = content['name']
        nuevoUsuario.gender = content['gender']
        nuevoUsuario.username = content['username']
        nuevoUsuario.email = content['email']
        nuevoUsuario.password = content['password']

        password1 = nuevoUsuario.password
        # Valida si los campos vienen vacios
        if (nuevoUsuario.name == "" or
           nuevoUsuario.gender == "" or
           nuevoUsuario.username == "" or
           nuevoUsuario.email == "" or
           nuevoUsuario.password == ""):
            return {"message": "errorVacio"}

        # Valida si ya existe el nombre de usuario
        for a in usuarios:
            if nuevoUsuario.username == a.username:
                return {"message": "errorNombre"}

        # Valida que la contraseña tenga mas de 8 caracteres
        if len(password1) <= 7:
            return {"message": "errorPasswordLength"}

        if not any(char.isdigit() for char in password1):
            return {"message": "errorPasswordNum"}

        if not any(char in simbolosEspeciales for char in password1):
            return {"message": "errorPasswordSymb"}

        usuarios.append(nuevoUsuario)

        return {"message": "datosOk"}
        # for a in usuarios:
        #  return jsonify({"nombre ": a.name,
        #                 "genero": a.gender,
        #                 "usuario": a.username,
        #                 "email": a.email,
        #                 "password": a.password})
    else:
        return "metodo no soportado"

# Pregunta si ya se inicio la sesion


@app.route('/usuario', methods=['GET'])
def mostrarPublicaciones():
    # print ("pasa aqui")
    if sesionOn:
        response = []
        response2 = []
        for b in publicaciones:
            if b.type == "imagen" or b.type == "Imagen":
                publi = {
                    "id": b.id,
                    "type": b.type,
                    "url": b.url,
                    "category": b.category,
                    "date": b.date,
                    "owner": b.owner,
                    "like": b.like
                }
                response.append(publi)

        for a in publicaciones:
            if a.type == "video" or a.type == "Video":
                publi2 = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response2.append(publi2)
        for c in usuarios:
            if userActive == c.username:
                return {"name": c.name,
                        "gender": c.gender,
                        "username": c.username,
                        "email": c.email,
                        "data": response,
                        "data2": response2}
        # return {"name": userActive, "data": response}

    else:
        return {"message": "NoainiciadoSesion"}


@app.route('/getPostUser', methods=['GET', 'POST'])
def obtenerPostUsuario():
    if request.method == 'POST':
        # print("llego")
        username = request.get_data()
        globals()['userView'] = str(username, 'UTF-8')
        return {"message": 1}

    if request.method == 'GET':
        response = []
        response2 = []
        noRanking = []
        totalLikes = 0
        rankingno = 0

        for b in publicaciones:
            if (b.type == "imagen" or b.type == "Imagen") and b.owner == userView:
                publi = {
                    "id": b.id,
                    "type": b.type,
                    "url": b.url,
                    "category": b.category,
                    "date": b.date,
                    "owner": b.owner,
                    "like": b.like
                }
                response.append(publi)

        for a in publicaciones:
            if (a.type == "video" or a.type == "Video") and a.owner == userView:
                publi2 = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response2.append(publi2)

        for c in usuarios:
            noLikes = 0
            for a in publicaciones:
                if c.username == a.owner:
                    noLikes = a.like + noLikes
            like = likes()
            like.username = c.username
            like.noLikes = noLikes

            noRanking.append(like)

            # print(noRanking[0].username)

        response3 = bubblesortLikes(noRanking)
        var = 0
        for b in response3:
            var = var + 1
            if (b.username == userView):
                #print ("siiii")
                rankingno = var
                totalLikes = b.noLikes
                break

        for c in usuarios:
            if userView == c.username:
                return {"name": c.name,
                        "gender": c.gender,
                        "username": c.username,
                        "email": c.email,
                        "ranking": rankingno,
                        "total": totalLikes,
                        "data": response,
                        "data2": response2}


@app.route('/misPost', methods=['GET'])
def mostrarMisPublicaciones():
    # print ("pasa aqui")
    if sesionOn:
        response = []
        response2 = []
        noRanking = []
        totalLikes = 0
        rankingno = 0

        for b in publicaciones:
            if (b.type == "imagen" or b.type == "Imagen") and b.owner == userActive:
                publi = {
                    "id": b.id,
                    "type": b.type,
                    "url": b.url,
                    "category": b.category,
                    "date": b.date,
                    "owner": b.owner,
                    "like": b.like
                }
                response.append(publi)

        for a in publicaciones:
            if (a.type == "video" or a.type == "Video") and a.owner == userActive:
                publi2 = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response2.append(publi2)

        for c in usuarios:
            noLikes = 0
            for a in publicaciones:
                if c.username == a.owner:
                    noLikes = a.like + noLikes
            like = likes()
            like.username = c.username
            like.noLikes = noLikes

            noRanking.append(like)

            # print(noRanking[0].username)

        response3 = bubblesortLikes(noRanking)
        var = 0
        for b in response3:
            var = var + 1
            if (b.username == userActive):
                print("siiii")
                rankingno = var
                totalLikes = b.noLikes
                break

        for c in usuarios:
            if userActive == c.username:
                return {"name": c.name,
                        "gender": c.gender,
                        "username": c.username,
                        "email": c.email,
                        "ranking": rankingno,
                        "total": totalLikes,
                        "data": response,
                        "data2": response2}
        # return {"name": userActive, "data": response}

    else:
        return {"message": "NoainiciadoSesion"}


def bubblesortLikes(likesd):
    intercambio = True
    response = likesd
    response2 = []
    while intercambio:
        intercambio = False
        for i in range(len(response)-1):
            if response[i].noLikes < response[i+1].noLikes:
                response[i], response[i+1] = response[i+1], response[i]
                intercambio = True
    for a in response:
        new = likes()
        new.username = a.username
        new.noLikes = a.noLikes

        response2.append(new)
    return response2

# Ordena las publicaciones por like


@app.route('/ranking', methods=['GET'])
def obtenerRanking():
    if request.method == 'GET':
        response2 = bubblesort()
        return {"message": response2}


def bubblesort():
    intercambio = True
    response = publicaciones
    response2 = []
    while intercambio:
        intercambio = False
        for i in range(len(response)-1):
            if response[i].like < response[i+1].like:
                response[i], response[i+1] = response[i+1], response[i]
                intercambio = True
    for a in response:
        publi2 = {
            "id": a.id,
            "type": a.type,
            "url": a.url,
            "category": a.category,
            "date": a.date,
            "owner": a.owner,
            "like": a.like
        }
        response2.append(publi2)
    return response2

    for a in response:
        print(a.id)
        print(a.type)
        print(a.url)
        print(a.category)

    return response


@app.route('/usuario', methods=['PUT'])
def nuevoLike():
    if request.method == 'PUT':
        response = []
        response2 = []
        content = request.get_json()
        id = content
        for a in publicaciones:
            if a.id == id:
                a.like = a.like + 1

        for a in publicaciones:
            if a.type == "imagen" or a.type == "Imagen":
                publi = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response.append(publi)

        for a in publicaciones:
            print("pasa por a")
            if a.type == "video" or a.type == "Video":
                print("pasa por b")
                publi2 = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }

                response2.append(publi2)
        for a in usuarios:
            if userActive == a.username:
                return {"name": a.name,
                        "data": response,
                        "data2": response2}


@app.route('/editUserByAdmin', methods=['GET', 'POST', 'PUT'])
def editarUser():
    if request.method == 'POST':
        content = request.get_data()
        globals()['userEdit'] = str(content, 'UTF-8')
        print(userEdit)
        return {"message": "okis"}

    if request.method == 'GET':
        for c in usuarios:
            if userEdit == c.username:
                return {"name": c.name,
                        "gender": c.gender,
                        "username": c.username,
                        "email": c.email,
                        }
    if request.method == 'PUT':
        content = request.get_json()
        nuevoUsuario = datosUsuario()
        nuevoUsuario.name = content['name']
        nuevoUsuario.gender = content['gender']
        nuevoUsuario.username = content['username']
        nuevoUsuario.email = content['email']
        nuevoUsuario.password = content['password']

        password1 = nuevoUsuario.password
        # Valida si los campos vienen vacios
        if (nuevoUsuario.name == "" or
           nuevoUsuario.gender == "" or
           nuevoUsuario.username == "" or
           nuevoUsuario.email == "" or
           nuevoUsuario.password == ""):
            return {"message": "errorVacio"}

        # Valida si ya existe el nombre de usuario
        for a in usuarios:
            if nuevoUsuario.username == a.username:
                return {"message": "errorNombre"}

        # Valida que la contraseña tenga mas de 8 caracteres
        if len(password1) <= 7:
            return {"message": "errorPasswordLength"}

        if not any(char.isdigit() for char in password1):
            return {"message": "errorPasswordNum"}

        if not any(char in simbolosEspeciales for char in password1):
            return {"message": "errorPasswordSymb"}

        for a in publicaciones:
            if userEdit == a.owner:
                a.owner = nuevoUsuario.username

        for a in usuarios:
            if userEdit == a.username:
                a.name = nuevoUsuario.name
                a.gender = nuevoUsuario.gender
                a.username = nuevoUsuario.username
                a.email = nuevoUsuario.email
                a.password = nuevoUsuario.password

                globals()['userEdit'] = nuevoUsuario.username
                print(userEdit)

                return {"message": "datosOk"}


@app.route('/editPostByAdmin', methods=['GET', 'POST', 'PUT'])
def editarPost():
    if request.method == 'POST':
        content = request.get_data()
        globals()['postEdit'] = str(content, 'UTF-8')
        print(postEdit)
        return {"message": "okis"}

    if request.method == 'GET':
        response = []
        for a in publicaciones:
            publi2 = {
                "id": a.id,
                "type": a.type,
                "url": a.url,
                "category": a.category,
                "date": a.date,
                "owner": a.owner,
                "like": a.like
            }
            response.append(publi2)
        return {"message": response}
    if request.method == 'PUT':
        response = []
        for a in publicaciones:
            if postEdit == str(a.id):
                publi2 = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response.append(publi2)
            return {"message": response}


@app.route('/obtenerPost', methods=['GET'])
def obtenerpost():
    if request.method == 'GET':
        response = []
        for a in publicaciones:
            if postEdit == str(a.id):
                publi = {
                    "id": a.id,
                    "type": a.type,
                    "url": a.url,
                    "category": a.category,
                    "date": a.date,
                    "owner": a.owner,
                    "like": a.like
                }
                response.append(publi)
                print(response)
                return {"response": response}


@app.route('/configuracion', methods=['PUT'])
def actualizarUsuario():
    if request.method == 'PUT':
        content = request.get_json()
        nuevoUsuario = datosUsuario()
        nuevoUsuario.name = content['name']
        nuevoUsuario.gender = content['gender']
        nuevoUsuario.username = content['username']
        nuevoUsuario.email = content['email']
        nuevoUsuario.password = content['password']

        password1 = nuevoUsuario.password
        # Valida si los campos vienen vacios
        if (nuevoUsuario.name == "" or
           nuevoUsuario.gender == "" or
           nuevoUsuario.username == "" or
           nuevoUsuario.email == "" or
           nuevoUsuario.password == ""):
            return {"message": "errorVacio"}

        # Valida si ya existe el nombre de usuario
        for a in usuarios:
            if nuevoUsuario.username == a.username:
                return {"message": "errorNombre"}

        # Valida que la contraseña tenga mas de 8 caracteres
        if len(password1) <= 7:
            return {"message": "errorPasswordLength"}

        if not any(char.isdigit() for char in password1):
            return {"message": "errorPasswordNum"}

        if not any(char in simbolosEspeciales for char in password1):
            return {"message": "errorPasswordSymb"}

        for a in publicaciones:
            if userActive == a.owner:
                a.owner = nuevoUsuario.username

        for a in usuarios:
            if userActive == a.username:
                a.name = nuevoUsuario.name
                a.gender = nuevoUsuario.gender
                a.username = nuevoUsuario.username
                a.email = nuevoUsuario.email
                a.password = nuevoUsuario.password

                globals()['userActive'] = nuevoUsuario.username
                print(userActive)

                return {"message": "datosOk"}
            else:
                return {"message": "wtf"}


# Crea un post nuevo
@app.route('/nuevopost', methods=['POST', 'PUT'])
def nuevaPublicacion():
    if request.method == 'POST':
        tiempo = datetime.now()
        año = tiempo.year
        mes = tiempo.month
        dia = tiempo.day
        fecha = str(dia) + "/" + str(mes)+"/"+str(año)

        content = request.get_json()
        nuevaPubli = publicacion()
        nuevaPubli.type = str(content['type'])
        nuevaPubli.url = content['url']
        nuevaPubli.category = content['category']
        nuevaPubli.date = fecha
        nuevaPubli.owner = userActive
        nuevaPubli.like = 0
        globals()['idPublicacion'] = idPublicacion + 1
        nuevaPubli.id = idPublicacion
        print(nuevaPubli.id)

        # print(nuevaPubli.type)
        # print(nuevaPubli.url)
        # print(nuevaPubli.category)
        # print(nuevaPubli.date)
        # print(nuevaPubli.owner)

        if (not nuevaPubli.type or
            not nuevaPubli.url or
                not nuevaPubli.category):
            return{"message": "errorVacio"}

        if(nuevaPubli.type == "imagen" or
           nuevaPubli.type == "Imagen" or
           nuevaPubli.type == "video" or
           nuevaPubli.type == "Video"):
            print("ok")
        else:
            return{"message": "errorType"}

        publicaciones.append(nuevaPubli)
        return {"message": "ok"}

    if request.method == 'PUT':
        tiempo = datetime.now()
        año = tiempo.year
        mes = tiempo.month
        dia = tiempo.day
        fecha = str(dia) + "/" + str(mes)+"/"+str(año)

        content = request.get_json()
        nuevaPubli = publicacion()
        nuevaPubli.type = content['type']
        nuevaPubli.url = content['url']
        nuevaPubli.category = content['category']
        nuevaPubli.date = fecha
        #nuevaPubli.owner = content['owner']
        #nuevaPubli.like = content['like']
        nuevaPubli.id = globals()['postEdit'] 
        
        #nuevaPubli.id = idPublicacion
        #print(nuevaPubli.id)

        #print(nuevaPubli.type)
        #print(nuevaPubli.url)
        #print(nuevaPubli.category)
        #print(nuevaPubli.date)
        #print(nuevaPubli.owner)

        if (not nuevaPubli.type or
            not nuevaPubli.url or
                not nuevaPubli.category):
            return{"message": "errorVacio"}

        if(nuevaPubli.type == "imagen" or
           nuevaPubli.type == "Imagen" or
           nuevaPubli.type == "video" or
           nuevaPubli.type == "Video"):
            print("ok")
        else:
            return{"message": "errorType"}

        #publicaciones.append(nuevaPubli)
        for a in publicaciones:
            if str(a.id) == str(postEdit):
                a.id = nuevaPubli.id
                a.type = nuevaPubli.type
                a.url = nuevaPubli.url
                a.category = nuevaPubli.category
                a.date = nuevaPubli.date
                a.owner = a.owner
                a.like = a.like
                return {"message": "ok"}


@app.route('/cerrar', methods=['GET'])
def cerrarSesion():
    if request.method == 'GET':
        globals()['userActive'] = ""
        globals()['sesionOn'] = False
        return {"message": "sesionCerrada"}


@app.route('/deleUserAdmin<id>', methods=['DELETE'])
def eliminarUsuario(id):
    var = 0
    for a in usuarios:
        print(var)
        if a.username == id:

            usuarios.pop(var)

            return {"message": "ok"}
        var = var + 1

@app.route('/delePostAdmin<id>', methods=['DELETE'])
def eliminarPost(id):
    var = 0
    print("leegogo", id)
    
    for a in publicaciones:
        print(var)
        if str(a.id) == id:
            print("paso")
            publicaciones.pop(var)

            return {"message": "ok"}
        var = var + 1

@app.route('/cargaMasivaUsuarios', methods=['POST'])
def cargaMasivaUsuarios():
    if request.method == 'POST':
        # print("llego")
        content = request.get_json()

        for a in content:
            nuevoUsuario = datosUsuario()
            nuevoUsuario.name = a['name']
            nuevoUsuario.gender = a['gender']
            nuevoUsuario.username = a['username']
            nuevoUsuario.email = a['email']
            nuevoUsuario.password = a['password']

            # print(nuevoUsuario.name)
            usuarios.append(nuevoUsuario)

        for a in usuarios:
            print(a.name)
        #mensaje = str(content,'UTF-8')
        #jsonUsers = json.loads(content)

        # print(jsonUsers[0]['codigo'])

        return {"message": "siiiii"}

@app.route('/cargaMasivaPost', methods=['POST'])
def cargaMasivaPost():
    if request.method == 'POST':
        # print("llego")
        content = request.get_json()
        imagenes = []
        videos = []
        imagenes = content['images']
        videos = content['videos']

        for a in imagenes:
            nuevo = publicacion()
            nuevo.type = "imagen"
            nuevo.url = a['url']
            nuevo.category = a['category']
            nuevo.date = a['date']
            nuevo.owner = "admin"
            nuevo.like = 0
            globals()['idPublicacion'] = idPublicacion + 1
            nuevo.id = idPublicacion

            publicaciones.append(nuevo)

        for a in videos:
            nuevo = publicacion()
            nuevo.type = "video"
            nuevo.url = a['url']
            nuevo.category = a['category']
            nuevo.date = a['date']
            nuevo.owner = "admin"
            nuevo.like = 0
            globals()['idPublicacion'] = idPublicacion + 1
            nuevo.id = idPublicacion

            publicaciones.append(nuevo)

        
        
        #mensaje = str(content,'UTF-8')
        #jsonUsers = json.loads(content)

        # print(jsonUsers[0]['codigo'])

        return {"message": "sii"}


if __name__ == '__main__':
    app.run(debug=True)
