# Core Minibank Backend

Layanan backend untuk sistem Core Minibank, dibangun menggunakan FastAPI. Layanan ini menangani operasi perbankan inti termasuk manajemen rekening, mutasi saldo, dan pemrosesan transaksi.

## Fitur

*   **Manajemen Portofolio**:
    *   Membuat rekening portofolio baru.
    *   Setor tunai (Deposit).
    *   Tarik tunai (Withdraw).
*   **Transaksi**:
    *   Pemindahbukuan (Transfer Internal / Overbooking).
    *   Transfer Online (Eksternal / Antar Bank).
    *   Pembalikan Transaksi (Reversal / Refunds).
    *   Riwayat Mutasi (Rekening Koran).
*   **Keamanan**:
    *   Otentikasi API Key untuk komunikasi aman dengan Middleware/Klien.

## Tech Stack

*   **Bahasa Pemrograman**: Python 3.11+
*   **Framework**: FastAPI
*   **Database**: MySQL
*   **ORM**: SQLAlchemy (Async)
*   **Migrasi**: Alembic
*   **Server**: Uvicorn

## Instalasi

1.  **Clone repositori**
    ```bash
    git clone <url_repositori>
    cd Core_minibank
    ```

2.  **Buat dan aktifkan virtual environment**
    ```bash
    python -m venv venv
    
    # Linux/MacOS
    source venv/bin/activate
    
    # Windows
    venv\Scripts\activate
    ```

3.  **Install dependensi**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Environment**
    Buat file `.env` di direktori root dengan konfigurasi berikut:

    ```env
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=username_db_anda
    DB_PASSWORD=password_db_anda
    DB_NAME=core_bank
    
    # Kunci Keamanan
    API_KEY=api_key_untuk_klien
    API_KEY_MID=api_key_middleware
    
    # Layanan Eksternal
    ENDPOINT_API_MIDDLEWARE=http://localhost:8001/
    ```

5.  **Migrasi Database**
    Terapkan skema database menggunakan Alembic:
    ```bash
    alembic upgrade head
    ```

## Menjalankan Aplikasi

Jalankan server pengembangan:

```bash
python run_server.py
```

Atau menggunakan uvicorn secara langsung:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

Server akan berjalan di `http://localhost:8002`.

## Deployment dengan Docker

Anda juga dapat menjalankan aplikasi menggunakan Docker untuk lingkungan yang terisolasi dan mudah direuplikasi.

1.  **Prasyarat**
    Pastikan **Docker** dan **Docker Compose** sudah terinstall di sistem Anda.

2.  **Running**
    Jalankan perintah berikut di terminal:
    ```bash
    docker network create minibank-network
    docker compose up -d --build
    ```
    Perintah ini akan membangun image, menjalankan container database dan aplikasi, serta melakukan migrasi database secara otomatis.

3.  **Monitoring**
    Untuk melihat logs aplikasi:
    ```bash
    docker compose logs -f app-core
    ```

4.  **Stopping**
    Untuk menghentikan aplikasi:
    ```bash
    docker compose down
    ```
    *(Tambahkan flag `-v` jika ingin menghapus volume database)*

## Dokumentasi API

Dokumentasi API interaktif (Swagger UI) tersedia di:
*   **Swagger UI**: `http://localhost:8002/docs`
*   **ReDoc**: `http://localhost:8002/redoc`

## Struktur Proyek

```
Core_minibank/
├── alembic/                # Migrasi database
├── app/
│   ├── core/               # Konfigurasi aplikasi & keamanan
│   ├── db/                 # Model database & koneksi
│   ├── repositories/       # Data access layer (Akses data)
│   ├── routes/             # API Endpoints
│   ├── schemas/            # Model Pydantic (Request/Response)
│   ├── services/           # Logika bisnis
│   ├── utils/              # Fungsi utilitas
│   └── main.py             # Entry point aplikasi
├── .env                    # Variabel environment
├── alembic.ini             # Konfigurasi Alembic
├── requirements.txt        # Dependensi Python
└── run_server.py           # Skrip untuk menjalankan server
```

## Penulis
*   **Choco_Mette**

