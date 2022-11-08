#!/usr/bin/env python3

''' servidor que recibe peticiones del cliente'''
# nombres de la interfaz que no se pueden cambiar pylint: disable=C0103

from flask import make_response, request

def routeApp(app, USER, TOKEN, adminToken):
    '''Enruta la API REST a la webapp'''

    @app.route('/v1/user/login', methods=['POST'])
    def login():
        '''Devuelve el usuario y su token si el login es correcto'''
        if hayJson(request) is True:
            reqjso = request.get_json()
            nombre = reqjso['user']
            hash_pass = reqjso['hash-pass']
            response = USER.correctHash(nombre, hash_pass)
            if response == "perfe":
                jso = {}
                token = TOKEN.crearToken(nombre)
                jso.update({"user":nombre})
                jso.update({"token":token})
                return make_response(jso, 200)
            elif response == "incorrecto":
                return make_response("Hash incorrecto", 400)
            else:
                return make_response("El usuario no existe", 404)
        return make_response("Missing JSON", 400)

    @app.route('/v1/user/admin', methods=['GET'])
    def getAdt():
        if headerAdmin(request.headers) is False:
            return make_response("Cabecera admin incorrecta", 401)
        return make_response("", 204)

    @app.route('/v1/user/<nombre_usuario>', methods=['PUT'])
    def crearUsuario(nombre_usuario):
        '''Crea al usuario mediante un nombre y hash dado'''
        mensaje = headerAdmin(request.headers)
        if mensaje is False:
            return make_response(mensaje, 401)
        if hayJson(request) is True:
            hash_pass = request.get_json()['hash-pass']
            response = USER.createUser(nombre_usuario, hash_pass)
            if response == "admin":
                return make_response("No se puede añadir admin", 400)
            elif response == "existe":
                return make_response("Ya existe ese usuario", 400)
            else:
                jso = {}
                jso.update({"user":nombre_usuario})
                return make_response(jso, 200)
        return make_response("Missing JSON", 400)

    @app.route('/v1/user/<nombre_usuario>', methods=['POST'])
    def cambiarHash(nombre_usuario):
        '''Cambia el hash de un usuario dado'''

        if headerUser(request.headers) is False:
            return make_response("Error cabecera user", 401)
        else:
            if hayJson(request) is True:
                hash_pass = request.get_json()['hash-pass']
                response = USER.nuevoHash(nombre_usuario, hash_pass)
                if response == "noexiste":
                    return make_response("No existe ese usuario", 404)
                else:
                    jso = {}
                    jso.update({"user":nombre_usuario})
                    return make_response(jso, 200)
            return make_response("Missing JSON", 400)

    @app.route('/v1/user/<nombre_usuario>', methods=['GET'])
    def existeUsuario(nombre_usuario):
        '''Comprueba si el usuario existe o no'''
        if USER.exists(nombre_usuario) is True:
            return make_response("Existe usuario", 204)
        return make_response("No existe el usuario", 404)

    @app.route('/v1/user/<nombre_usuario>', methods=['DELETE'])
    def borrarUsuario(nombre_usuario):
        '''Borra el usuario si existe'''
        response = USER.borrarUsuario(nombre_usuario)
        if response == "perfe":
            return make_response("Usuario borrado", 204)
        return make_response("No existe el usuario", 404)

    @app.route('/v1/token/<token>', methods=['GET'])
    def obtenerToken(token):
        '''Obtiene el usuario dado el token'''
        response = TOKEN.existsToken(token)
        if response != "error":
            jso = {}
            jso.update({"user":response})
            return make_response(jso, 200)
        return make_response("Token erroneo", 400)

    def hayJson(requestt):
        if not requestt.is_json:
            return False
        return True

    def headerAdmin(headers):
        adt = headers.get('admin-token')
        if adt is not None:
            if adt == adminToken:
                return True
        return False

    def headerUser(headers):
        tok = headers.get('user-token')
        if tok is not None:
            if TOKEN.existsToken(tok) != "error":
                return True
        return False
