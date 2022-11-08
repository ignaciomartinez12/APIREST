'''
    Interfaces para el acceso a la API rest del servicio de autenticacion
'''
# nombres de la interfaz que no se pueden cambiar pylint: disable=C0103
import json
import requests
import hashlib

class Administrator:
    '''Cliente de autenticacion como administrador'''

    def __init__(self, uri, token, head_admin):
        self.uri = uri
        self.__token__ = token
        self.headAdmin = head_admin

    @property
    def token(self):
        '''Retorna el token del administrador'''
        return self.__token__

    def new_user(self, username, password):
        '''Crea un nuevo usuario'''
        if username is None or password is None:
            return "Faltan parametros."
        password_sha = hashlib.new("sha3_256", password.encode()).hexdigest()
        jso = {}
        jso.update({"hash-pass":password_sha})#Encriptar
        result = requests.put(
            f'{self.uri}v1/user/{username}',
            headers=self.headAdmin,
            data=json.dumps(jso),
            timeout=120
        )
        res = str(result.content.decode('utf-8'))
        if result.status_code != 200:
            return f"Error con codigo {result.status_code} y mensaje {res}"
        return res

    def remove_user(self, username):
        '''Elimina un usuario'''
        if username is None:
            return "Faltan parametros."
        jso = {}
        jso.update({"user":username})
        result = requests.delete(
            f'{self.uri}v1/user/{username}',
            headers=self.headAdmin,
            data=json.dumps(jso),
            timeout=120
        )
        res = str(result.content.decode('utf-8'))
        if result.status_code != 204:
            return f"Error con codigo {result.status_code} y mensaje {res}"
        return "Usuario eliminado"


class User:
    '''Cliente de autenticacion como usuario'''

    def __init__(self, uri, username, token):
        self.username = username
        self.__token__ = token
        self.uri = uri
        self.headUser = {"content-type": "application/json", "user-token":token}

    def set_new_password(self, new_password):
        '''Cambia la contraseña del usuario'''

        if new_password is None:
            return "Faltan parametros."
        password_sha = hashlib.new("sha3_256", new_password.encode()).hexdigest()
        jso = {}
        jso.update({"hash-pass": password_sha})#Encriptar
        result = requests.post(
            f'{self.uri}v1/user/{self.username}',
            headers=self.headUser,
            data = json.dumps(jso),
            timeout=120
        )
        res = str(result.content.decode('utf-8'))
        if result.status_code != 200:
            return f"Error con codigo {result.status_code} y mensaje {res}"
        return res

    @property
    def token(self):
        '''Retorna el token del usuario'''
        return self.__token__


class AuthService:
    '''Cliente de acceso al servicio de autenticacion'''

    def __init__(self, uri):
        self.uri = uri
        self.head = {"content-type": "application/json"}

    def user_of_token(self, token):
        '''Return username of the given token or error'''
        if token is None:
            return "Faltan parametros."
        result = requests.get(
            f'{self.uri}v1/token/{token}',
            headers=self.head,
            timeout=120
        )
        res = str(result.content.decode('utf-8'))
        if result.status_code != 200:
            return f"Error con codigo {result.status_code} y mensaje {res}"
        return res

    def exists_user(self, username):
        '''Return if given user exists or not'''
        if username is None:
            return "Faltan parametros."
        if username != "admin":
            result = requests.get(
                f'{self.uri}v1/user/{username}',
                headers=self.head,
                timeout=120
            )
            res = str(result.content.decode('utf-8'))
            if result.status_code != 204:
                return f"Error con codigo {result.status_code} y mensaje {res}"
        return "Existe"

    def administrator_login(self, token):
        '''Return Adminitrator() object or error'''
        headAdmin = {"content-type": "application/json"}
        headAdmin.update({"admin-token":token})
        result = requests.get(
            f'{self.uri}v1/user/admin',
            headers=headAdmin,
            data = {},
            timeout=120
        )
        if result.status_code != 204:
            return f"Error con codigo {result.status_code}: token de administrador incorrecto"
        adminn = Administrator(self.uri, token, headAdmin)
        return adminn

    def user_login(self, username, password):
        ''''Manda la request de login'''
        if username is None or password is None:
            return "Faltan parametros."
        password_sha = hashlib.new("sha3_256", password.encode()).hexdigest()
        jso = {}
        jso.update({"user":username})
        jso.update({"hash-pass":password_sha})#Encriptar
        result = requests.post(
            f'{self.uri}v1/user/login',
            headers=self.head,
            data=json.dumps(jso),
            timeout=120
        )
        res = str(result.content.decode('utf-8'))
        if result.status_code != 200:
            return f"Error con codigo {result.status_code} y mensaje {res}"
        return res
