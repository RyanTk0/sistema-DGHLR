import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from banco_dados.connection import conectando


@pytest.fixture(scope="session")
def db_conn():
    """
    Conexão criada uma vez por sessão de testes.
    """
    conn = conectando()
    assert conn.is_connected(), "Não foi possível conectar ao MySQL."
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_conn):
    """
    Cursor por teste, com ROLLBACK automático.
    Nada fica salvo no banco após os testes.
    """
    cursor = db_conn.cursor(dictionary=True, buffered=True)
    db_conn.start_transaction()

    try:
        yield cursor
    finally:
        db_conn.rollback()
        cursor.close()