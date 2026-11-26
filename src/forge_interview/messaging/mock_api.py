"""Mock del enunciado. Solo registra llamadas en memoria; no tiene acceso a WhatsApp."""


class MockAPI:
    def __init__(self, bloquear=()):
        self.bloquear = set(bloquear)
        self.log = []

    def send_text(self, desde, hacia, texto):
        if desde in self.bloquear:
            raise RuntimeError("number blocked")
        self.log.append((desde, hacia, texto))
