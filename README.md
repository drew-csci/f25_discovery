# Discovery Hub

## 🧰 Setup Instructions

### 1) Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing or needs updating:

```bash
pip freeze > requirements.txt
```

---

### 3) Configure environment variables -- THIS HAS BEEN DONE ALREADY

Create a `.env` file in the project root (same folder as `manage.py`) with the Postgres settings below. The host value mirrors the original project’s remote DB host.

```env
DJANGO_SECRET_KEY=dev-insecure-change-me
DJANGO_DEBUG=True
DB_NAME=discovery_db
DB_USER=disco_app
DB_PASSWORD=CSCI340Fall2025Disco
DB_HOST=34.16.174.60
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

> Notes  
> • The project uses a custom user model with **email login** and a `user_type` field. The three roles are **University**, **Company**, and **Investor**.  
> • Keep credentials out of version control in real deployments.

---

### 4) Apply migrations -- THIS HAS BEEN DONE ALREADY

```bash
python manage.py migrate
```

If you’re developing locally and using the remote DB, make sure your network allows connections to that host/port.

---

### 5) Create users

#### a) Create the admin (superuser) -- THIS HAS BEEN DONE ALREADY

Run:

```bash
python manage.py createsuperuser --email admin_disco@drew.edu --username admin
```

When prompted, enter the password of your choice, for example: **`Discovery1!`**

#### b) Seed the three role accounts -- THIS HAS BEEN DONE ALREADY

From the Django shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

spec = [
    ("university@drew.edu", "university"),
    ("company@drew.edu", "company"),
    ("investor@drew.edu", "investor"),
]

for email, role in spec:
    u, created = User.objects.get_or_create(
        email=email,
        defaults={"user_type": role, "username": email}
    )
    u.user_type = role
    u.username = email
    u.set_password("ChangeMe123!")
    u.save()
    print(("Created" if created else "Updated"), email, role)
```

> You’ll **sign in with email** on the app’s login form. The admin site also stores a `username` field for compatibility.

---

### 6) Start the development server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

---

## 👤 Demo Accounts

| Role       | Email                 | Password       |
| ---------- | --------------------- | -------------- |
| University | `university@drew.edu` | `ChangeMe123!` |
| Company    | `company1@drew.edu`   | `ChangeMe123!` |
| Investor   | `investor@drew.edu`   | `ChangeMe123!` |

> Change these passwords after first login if you keep them around.

---

## ⚙️ Admin Panel

Admin site: **http://127.0.0.1:8000/admin**

**Superuser (created in Step 5a)**

- **Email:** `admin_disco@drew.edu`
- **Username:** `admin`
- **Password:** `Discovery1!` _(you set this at the prompt)_

---

## 💡 Notes & Tips

- Always activate your virtual environment before running commands.
- Stop the dev server with **Ctrl+C**.
- If you add packages: `pip freeze > requirements.txt` to update.
- Email is the **primary login identifier** throughout the app.
- The database host value above mirrors the original project’s settings so your environment behaves the same.
