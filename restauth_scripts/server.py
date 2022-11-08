#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''
import argparse
import time
from flask import Flask

from restauth.server import routeApp
from restauth.user import User
from restauth.token import Token

def main():
    '''Entry point'''
    jso = comprobarArgs()
    portt = jso['port']
    hostt = jso['host']
    adtok = jso['adt']
    ruta = jso['ruta']
    app = Flask("restauth")
    insToken = Token()
    routeApp(app, User(ruta), insToken, adtok)
    app.run(debug=True, host = hostt, port = portt)
    borrarHilos(insToken)

def comprobarArgs():
    '''Funcion para comprobar argumentos'''
    parser = argparse.ArgumentParser(description='Process some options.')
    jso = {}
    parser.add_argument('-p')
    parser.add_argument('--port')
    parser.add_argument('-a')
    parser.add_argument('--admin')
    parser.add_argument('-l')
    parser.add_argument('--listening')
    parser.add_argument('-d')
    parser.add_argument('--db')
    args = parser.parse_args()

    if args.p is None and args.port is None:
        jso.update({"port":3001})
    else:
        try:
            if args.p is not None:
                jso.update({"port":int(args.p)})
            else:
                jso.update({"port":int(args.port)})
        except ValueError:
            print("Introduce un puerto valido. Por ejemplo, 3001")

    if args.a is None and args.admin is None:
        jso.update({"adt":"1234"})
    else:
        if args.a is not None:
            jso.update({"adt":args.a})
        else:
            jso.update({"adt":args.admin})

    if args.l is None and args.listening is None:
        jso.update({"host":"0.0.0.0"})
    else:
        if args.l is not None:
            jso.update({"host":args.l})
        else:
            jso.update({"host":args.listening})

    if args.d is None and args.db is None:
        jso.update({"ruta":"user.db"})
    else:
        if args.d is not None:
            jso.update({"ruta":args.d})
        else:
            jso.update({"ruta":args.db})
    return jso

def borrarHilos(insToken):
    '''Borrar todos los timer'''
    if len(insToken.timers) > 0:
        for i in insToken.timers:
            print("Timer borrado")
            i.cancel()
    time.sleep(3)

if __name__ == '__main__':
    main()
