#!/usr/bin/env python3

'''
    REST access library + client example
'''

import json
from restauth.auth import AuthService
from restauth.auth import User

def main():
    '''Entry point'''
    uri = 'http://127.0.0.1:3001/'
    client = AuthService(uri)
    admin = client.administrator_login("1234")
    if type(admin) != str :
        token_admin = admin.headAdmin['admin-token']
        print(token_admin)
        print("######## Login admin correcto ########")
        res = admin.new_user("user1", "123456")
        if res[0] == '{':
            username = json.loads(res)['user']
            print(username)
            print("######## Crear usuario correcto ########")
            print(admin.remove_user(username))
        else:
            print(res)
            print("hhhhhh")

        ############# Crear usuario para login #############
        nombre = "userLogin"
        password = "HOLA"
        rest = admin.new_user(nombre, password)
    else :
        print(admin)

    print(client.exists_user("userLogin"))


    response = client.user_login("userLogin", "HOLA")
    token_user = " "
    if response[0] == "{":
        print("######## Login correcto ########")
        print(response)
        token_user = json.loads(response)['token']
        user = User(uri, "userLogin", token_user)
        resp = client.user_of_token(token_user)
        print(resp)
        print("######## Cambiando password ########")
        print(user.set_new_password("hola"))
        print(client.user_login("userLogin", "HOLA")) #Saldra hash incorrecto
    else:
        print(response)


if __name__ == '__main__':
    main()
