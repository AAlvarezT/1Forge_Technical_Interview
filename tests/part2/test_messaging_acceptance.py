"""Tres contratos de la Parte 2 — todos deben pasar con el agente corregido."""

import pytest

from forge_interview.messaging import agent
from forge_interview.messaging.mock_api import MockAPI


@pytest.fixture(autouse=True)
def deterministic_execution(monkeypatch):
    monkeypatch.setattr(agent.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(agent.random, "choice", lambda values: values[0])


def test_sender_cannot_exceed_25_successful_messages():
    number = agent.Numero("+51900000999")
    api = MockAPI()
    contacts = [{"telefono": f"9{index:08d}"} for index in range(26)]
    successful = agent.campana(contacts, [number], "Hola", api)
    assert successful == 25
    assert len(api.log) == 25
    assert number.enviados_hoy == 25


def test_blocked_sender_is_removed_from_rotation():
    blocked = agent.Numero("+51900000001")
    available = agent.Numero("+51900000002")
    api = MockAPI(bloquear=[blocked.telefono])
    result = agent.enviar(blocked, "+51900000003", "Hola", api)
    assert result is False
    assert blocked.bloqueado is True
    assert blocked.enviados_hoy == 0
    assert agent.elegir_numero([blocked, available]) is available


def test_repeated_contact_receives_one_message():
    api = MockAPI()
    contacts = [{"telefono": "900000001"}, {"telefono": "+51 900-000-001"}]
    successful = agent.campana(contacts, [agent.Numero("+51900000999")], "Hola", api)
    assert successful == 1
    assert len(api.log) == 1
