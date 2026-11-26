# Transcripción del código de las páginas 2-3 del enunciado.
# Conserva sus bugs; usar únicamente como referencia para el diff.
import random, time, datetime as dt
LIMITE_DIARIO = 25
class Numero:
    def __init__(self, telefono):
        self.telefono = telefono
        self.enviados_hoy = 0
        self.bloqueado = False
        self.ultimo_dia = dt.date.today()
def normalizar(tel):
    tel = tel.replace(" ", "").replace("-", "")
    if tel.startswith("9"):
        return tel
    return tel
def elegir_numero(numeros):
    disponibles = [n for n in numeros if n.enviados_hoy <= LIMITE_DIARIO]
    return random.choice(disponibles)
def enviar(numero, destino, texto, api):
    hoy = dt.date.today()
    if numero.ultimo_dia != hoy:
        numero.enviados_hoy = 0
    try:
        api.send_text(numero.telefono, destino, texto)
    except Exception as e:
        if "blocked" in str(e):
            numero.bloqueado == True
    numero.enviados_hoy += 1
    return True
def campana(contactos, numeros, texto, api):
    enviados = 0
    for c in contactos:
        n = elegir_numero(numeros)
        if enviar(n, normalizar(c["telefono"]), texto.format(**c), api):
            enviados += 1
    time.sleep(random.uniform(20, 60))
    return enviados
