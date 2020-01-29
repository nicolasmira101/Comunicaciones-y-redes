# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 18:03:53 2018

@author: adrian
"""


class FileReader:

    # función para la lectura del archivo de texto
    def readRules(self, filename):
        # abrir archivo y leer línas
        fileRules = open(filename, "r")
        lines = fileRules.readlines()
        fileRules.close()

        print("\nFile with rules read")

        expression = None
        instruction = None

        # si solo hay 1 línea se revisa instrucción compleja
        if(len(lines) == 1):
            commands = lines[0].rstrip().split("\t")
            if(len(commands) == 2):
                instruction = commands[0]
                expression = commands[1]
        # si hay más líneas se concatenan las secciones del archivo de texto
        elif(len(lines) > 1):
            # inicializar variables
            type = ""
            expression = ""
            counterIPs = 0
            counterConditions = 0
            numberLine = 0

            for line in lines:

                numberLine = numberLine + 1
                # distinguir secciones del archivo
                if(line[0] == "#"):
                    if(line.rstrip() == "#Instruction"):
                        type = "Instruction"
                    elif(line.rstrip() == "#IPs"):
                        type = "IPs"
                    elif(line.rstrip() == "#Protocols"):
                        type = "Protocols"
                else:
                    # distinguir las 3 posibles instrucciones
                    if(type == "Instruction"):  # info de si es para aceptar o rechazar tráfico
                        if (line.rstrip() == "block all"):
                            expression = "true"
                            instruction = "block"
                            break
                        elif(line.rstrip() == "block"):
                            instruction = "block"
                        elif(line.rstrip() == "allow"):
                            instruction = "allow"
                    # concatenar IPs especificadas con su respectivo tipo (fuente/destino)
                    if(type == "IPs"):  # info de las IPs

                        counterIPs = counterIPs + 1
                        if(counterIPs == 1):
                            expression = expression + "("
                        IPs = line.rstrip().split("\t")

                        if(len(IPs) == 2):
                            if(counterIPs > 1):
                                expression = expression + " or "
                            expression = expression + "ip." + \
                                IPs[1] + " == " + IPs[0]
                        else:
                            print("Line "+str(numberLine) +
                                  " of the file is incorrect. It was ignored")

                        if(numberLine == len(lines)):
                            expression = expression + ")"
                    # concatenar protocolos especificados con condición opcional
                    elif(type == "Protocols"):  # info de los protocolos

                        counterConditions = counterConditions + 1
                        if(counterConditions == 1 and counterIPs > 0):
                            expression = expression + ") and ("

                        conditions = line.rstrip().split("\t")

                        if(len(conditions) == 1 or len(conditions) == 2):

                            expression = expression + conditions[0]

                            if(len(conditions) == 2):
                                expression = expression + "." + conditions[1]

                            if(numberLine < len(lines)):
                                expression = expression + " or "

                            if(numberLine == len(lines) and counterIPs > 0):
                                expression = expression + ")"

                        else:
                            print("Line "+str(numberLine) +
                                  " of the file is incorrect. It was ignored")

            if(expression == ""):
                expression = None
        # se retorna la expresión para el filtro y la instrucción a realizar
        return expression, instruction
