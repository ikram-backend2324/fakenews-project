# 🛡️ FakeNews AI Detection System

AI-powered fake news detector using Django + DeepSeek via OpenRouter.
Supports **English**, **Russian**, and **Uzbek**.

---

## 🚀 Quick Start (Local)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file (copy from .env.example)
cp .env.example .env
# → Fill in SECRET_KEY and OPENROUTER_API_KEY

# 4. Run setup
python manage.py migrate
python manage.py compilemessages
python manage.py seed
python manage.py collectstatic --noinput

# 5. Start development server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🌐 Deploy on Render (Free Tier)

### Environment Variables (set in Render dashboard)
| Variable | Value |
|---|---|
| `SECRET_KEY` | Generate a strong random key |
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `OPENROUTER_MODEL` | `deepseek/deepseek-chat` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |

### Build Command
```
pip install -r requirements.txt && python manage.py migrate && python manage.py compilemessages && python manage.py seed && python manage.py collectstatic --noinput
```

### Start Command
```
gunicorn fakenews_project.wsgi:application
```

---

## 👤 Demo Credentials (after seed)

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin1234!` |
| User | `alice` | `Alice1234!` |
| User | `bob` | `Bob12345!` |

Admin panel: `/admin/`

---

## 📁 Project Structure

```
fakenews_project/
├── fakenews_project/   # Django settings, urls, wsgi
├── accounts/           # Auth: login, register, profile
├── detector/           # AI analysis, history, results
├── core/               # Home, about pages
├── templates/          # All HTML templates
├── static/             # CSS, JS
├── locale/             # i18n: en, ru, uz
└── manage.py
```

## 🤖 AI Model
- Provider: [OpenRouter](https://openrouter.ai)
- Default model: `deepseek/deepseek-chat` (cheap & accurate)
- Change via `OPENROUTER_MODEL` env var
