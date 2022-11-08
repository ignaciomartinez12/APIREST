#!/usr/bin/env python3

import unittest
import restauth.user
import restauth.token

NAME_EXISTS = 'nacho'
ADMIN_NAME = 'admin'
PASSWORD = '12345'
NAME_FAKE = 'name_fake'
PASSWORD_FAKE = 'fake'
NAME = "prueba"

class TestUserImplementation(unittest.TestCase):

    def test_User(self):
        myUser = restauth.user.User('user.db')
        
        '''Test creation user'''
        self.assertEqual(myUser.createUser(ADMIN_NAME, PASSWORD), "admin")
        self.assertEqual(myUser.createUser(NAME, PASSWORD), "perfe")
        self.assertEqual(myUser.createUser(NAME, PASSWORD), "existe")

        '''Test comprobar hash'''
        self.assertEqual(myUser.correctHash(NAME, PASSWORD), "perfe")
        self.assertEqual(myUser.correctHash(NAME, PASSWORD_FAKE), "incorrecto")
        self.assertEqual(myUser.correctHash(NAME_FAKE, PASSWORD), "noexiste")

        '''Test cambiar hash'''
        self.assertEqual(myUser.nuevoHash(NAME, PASSWORD), "perfe")
        self.assertEqual(myUser.nuevoHash(NAME_FAKE, PASSWORD), "noexiste")

        '''Test delete user'''
        self.assertEqual(myUser.borrarUsuario(NAME), "perfe")
        self.assertEqual(myUser.borrarUsuario(NAME_FAKE), "noexiste")

class TestTokenImplementation(unittest.TestCase):

    def test_exists(self):
        '''Test cambiar hash'''
        myToken = restauth.token.Token()
        myToken.tokens.update({"nacho":"token_prueba"})
        self.assertEqual(myToken.exists(NAME_EXISTS), True)
        self.assertEqual(myToken.exists(NAME_FAKE), False)

