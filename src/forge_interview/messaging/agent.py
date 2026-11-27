"""Agente de envíos corregido.

El original con los bugs está en reference/shipping_agent_original.py.
Bugs corregidos documentados en docs/part2/bugs.md.
"""

import datetime as dt
import random
import time

LIMITE_DIARIO = 25


class Numero:
    def __init__(self, telefono):
        self.telefono = telefono
        self.enviados_hoy = 0
        self.bloqueado = False
        self.ultimo_dia = dt.date.today()


def normalizar(tel):
    tel = tel.replace(" ", "").replace("-", "")
    if tel.startswith("+51"):
        return tel
    if tel.startswith("51"):
        return "+" + tel
    if tel.startswith("9"):
        return "+51" + tel
    return tel


def elegir_numero(numeros):
    disponibles = [n for n in numeros if not n.bloqueado and n.enviados_hoy < LIMITE_DIARIO]
    if not disponibles:
        return None
    return random.choice(disponibles)


def enviar(numero, destino, texto, api):
    hoy = dt.date.today()
    if numero.ultimo_dia != hoy:
        numero.enviados_hoy = 0
        numero.ultimo_dia = hoy
    try:
        api.send_text(numero.telefono, destino, texto)
    except Exception as e:
        if "blocked" in str(e):
            numero.bloqueado = True
        return False
    numero.enviados_hoy += 1
    return True


def campana(contactos, numeros, texto, api):
    enviados = 0
    vistos = set()
    for c in contactos:
        tel_norm = normalizar(c["telefono"])
        if tel_norm in vistos:
            continue
        vistos.add(tel_norm)
        n = elegir_numero(numeros)
        if n is None:
            break
        if enviar(n, tel_norm, texto.format(**c), api):
            enviados += 1
        time.sleep(random.uniform(20, 60))
    return enviados
