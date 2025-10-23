## Setup Backend

1. **Masuk ke folder backend**
```bash
cd backend

````
2. **Buat virtual environment**
```bash
python -m venv venv
```

3. **Aktifkan virtual environment**

* **Windows:**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Copy file environment**

```bash
cp .env.example .env
```

6. **Edit `.env` dan sesuaikan konfigurasi database**

```bash
# Contoh konfigurasi
DB_HOST=localhost
DB_PORT=5432
DB_NAME=task_tracker_db
DB_USER=postgres
DB_PASSWORD=your_password
```

7. **Jalankan server**

```bash
python run.py
```

Server akan berjalan di: [http://localhost:5000](http://localhost:5000)

```
