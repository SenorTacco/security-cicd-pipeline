"""DATABASE_PATH ortam degiskeni ile veritabani yolu yapilandirmasini test et."""
import os
import sys


def _clean_app_modules():
    """app, database, config modullerini cache'den temizle"""
    for mod_name in ('app', 'database', 'config'):
        sys.modules.pop(mod_name, None)


def test_database_path_env_is_respected(tmp_path, monkeypatch):
    """DATABASE_PATH verildiginde veritabani o yolda olusmali"""
    db_file = tmp_path / "data" / "app.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_file))
    secure_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'secure')
    )
    monkeypatch.syspath_prepend(secure_path)
    _clean_app_modules()
    try:
        import database
        database.init_db()
        # Dosya, olmayan alt dizinle birlikte belirtilen yolda olusmali
        assert db_file.exists()
        users = database.get_user_secure("admin")
        assert users and users[0][1] == "admin"
    finally:
        _clean_app_modules()


def test_database_path_defaults_to_local_file(tmp_path, monkeypatch):
    """DATABASE_PATH verilmezse calisma dizininde app.db olusmali"""
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    monkeypatch.chdir(tmp_path)
    secure_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'secure')
    )
    monkeypatch.syspath_prepend(secure_path)
    _clean_app_modules()
    try:
        import database
        database.init_db()
        assert (tmp_path / "app.db").exists()
    finally:
        _clean_app_modules()
