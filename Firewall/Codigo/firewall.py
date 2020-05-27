# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 20:09:38 2018

@author: adrian
"""

# importar librería pydivert
import pydivert


class Firewall:

    # constructor de la clase
    def __init__(self, expression):
        self.expression = expression

    # validar si la expresión para filtrar paquetes es correcta
    def validateExpression(self):
        # crear instancia de WinDivert usando expresión
        w = pydivert.WinDivert(self.expression)
        # chequear si la expresión es correcta
        # se devuelven 3 variables
        x, y, z = w.check_filter(self.expression)
        # se retorna únicamente la última variable
        return z

    # función para permitir solo tráfico específicado
    def allowTraffic(self):
        # se filtra todo el tráfico
        with pydivert.WinDivert("true", 1) as w:
            for packet in w:
                # si el tráfico coincide con la expresión se reenvía
                if (packet.matches(self.expression, 1) == True):
                    w.send(packet, True)

    # función para bloquear solo tráfico específicado
    def blockTraffic(self):
        # se filtra todo el tráfico
        with pydivert.WinDivert("true", 1) as w:
            for packet in w:
                # si el tráfico no coincide con la expresión se reenvía
                if (packet.matches(self.expression, 1) == False):
                    w.send(packet, True)
