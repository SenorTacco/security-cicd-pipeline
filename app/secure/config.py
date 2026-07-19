import os
from dotenv import load_dotenv

# .env dosyasindan degiskenleri yukle
load_dotenv()

# DUZELTILDI: Tum hassas degerler ortam degiskenlerinden okunuyor
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

API_SECRET_KEY = os.environ.get("API_SECRET_KEY", "fallback-only-for-dev")

# Veritabani dosya yolu ortam degiskeninden yapilandirilir.
# Docker'da kalici depolama icin volume'e bagli bir dizin verilmelidir
# (or. /app/data/app.db). Varsayilan deger lokal gelistirme icindir.
DATABASE_PATH = os.environ.get("DATABASE_PATH", "app.db")

# DUZELTILDI: Uretimde debug kapali
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"
