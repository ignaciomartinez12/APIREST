#!/usr/bin/env python3

'''
    Implementacion del servicio RESTLIST
'''
# nombres de la interfaz que no se pueden cambiar pylint: disable=C0103
import sqlite3

class User:
    '''Implementa todas las operaciones sobre un objeto tipo User()'''

    def __init__(self, ruta):
        self.ruta = ruta
        con = sqlite3.connect(ruta)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (nombre, password)''')
        con.commit()
        con.close()

    def createUser(self, nombre, hashh):
        '''Añade un usuario'''
        if nombre == 'admin':
            return "admin"
        if self.exists(nombre) is False:
            con = sqlite3.connect(self.ruta)
            cursor = con.cursor()
            cursor.execute(f"INSERT INTO user VALUES ('{nombre}', '{hashh}')")
            con.commit()
            con.close()
            return "perfe"
        return "existe"

    def borrarUsuario(self, nombre):
        '''Borra un usuario'''
        if self.exists(nombre) is True:
            con = sqlite3.connect(self.ruta)
            cursor = con.cursor()
            cursor.execute(f"DELETE FROM user WHERE nombre = '{nombre}'")
            con.commit()
            con.close()
            return "perfe"
        return "noexiste"

    def nuevoHash(self, nombre, hashh):
        '''Cambia el hash de un usuario'''
        if self.exists(nombre) is True:
            con = sqlite3.connect(self.ruta)
            cursor = con.cursor()
            cursor.execute(f"UPDATE user SET password = '{hashh}' WHERE nombre = '{nombre}'")
            con.commit()
            con.close()
            return "perfe"
        return "noexiste"

    def exists(self, nombre):
        '''Comprueba si un usuario existe'''
        con = sqlite3.connect(self.ruta)
        cursor = con.cursor()
        user = cursor.execute(f"SELECT nombre FROM user WHERE nombre='{nombre}'").fetchall()
        con.close()
        if user == []:
            return False
        return True

    def correctHash(self, nombre, hashh):
        '''Comprueba si un hash es correcto'''
        con = sqlite3.connect(self.ruta)
        cursor = con.cursor()
        if self.exists(nombre) is True:
            user_hash = cursor.execute(f"SELECT password FROM user WHERE nombre='{nombre}'").fetchone()
            con.close()
            if user_hash[0] == hashh:
                return "perfe"
            return "incorrecto"
        return "noexiste"
