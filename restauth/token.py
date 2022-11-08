#!/usr/bin/env python3

'''
    Implementacion de la clase de negocio para la estion de tokens
'''

# nombres de la interfaz que no se pueden cambiar pylint: disable=C0103
import uuid
import threading
class Token():
    '''Clase de negocio que contiene tokens de acceso'''

    def __init__(self):
        self.ages = {}
        self.tokens = {}
        self.timers = []

    def crearToken(self, nombre):
        '''Crea un nuevo token para un usuario dado'''
        token = ""
        if self.exists(nombre) is True:
            token = self.tokens[''+nombre+'']
            self.reiniciarEdad(nombre)
        else:
            token = str(uuid.uuid4())
            self.tokens.update({nombre:token})
            self.ages.update({token:0})
        self.timerr = threading.Timer(5, self.incremento, args=(token,))
        self.timers.append(self.timerr)
        self.timerr.start()
        return token

    def reiniciarEdad(self, nombre):
        '''Reinicia la edad de un token de un usuario dado'''
        token = self.tokens[''+nombre+'']
        self.ages[''+token+''] = 0

    def exists(self, nombre):
        '''Comprueba si existe un token para un usuario dado'''
        keys = self.tokens.keys()
        if nombre in keys:
            return True
        return False

    def existsToken(self, token):
        '''retorna el usuario del token si existe'''
        keys = self.ages.keys()
        if token in keys:
            users = self.tokens.keys()
            for i in users:
                if self.tokens[i] == token:
                    return i
        return "error"

    def incremento(self, token):
        '''metodo para incrementar la edad'''
        try:
            if self.ages[token] >= 180:

                self.ages.pop(token)
                keys = self.tokens.keys()
                names = []
                for i in keys:
                    if token == self.tokens[i]:
                        names.append(i)
                for i in names:
                    self.tokens.pop(i)

            else:
                self.ages[token] += 1
                self.timer = threading.Timer(5, self.incremento, args=(token,))
                self.timers.append(self.timer)
                self.timer.start()
        except KeyError:
            print("Ya se ha eliminado")
