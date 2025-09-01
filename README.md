# FastFluence Vue - Minimal Viable Product

Platforma łącząca reklamodawców z influencerami dla skutecznych kampanii marketingowych z funkcjonalnością aktywacji konta przez email (SendGrid + SMTP).

## Technologie

**Backend:**
- Python 3.12 + FastAPI + SQLModel
- JWT auth (python-jose)
- SQLite (dev) / PostgreSQL (prod)
- SendGrid Web API + SMTP fallback
- Poetry dla zarządzania zależności

**Frontend:**
- Vue 3 + Vite + Pinia
- Vue Router (history mode)
- Bootstrap 5 + HeadlessUI
- TypeScript + ESLint + Prettier

## Szybki start

### Wymagania
- Docker i Docker Compose
- Node.js 18+ (dla developmentu)
- Python 3.12+ (dla developmentu)
- Konto SendGrid (lub Gmail/Mailgun)

### 1. Klonowanie repozytorium
```bash
git clone <repository-url>
cd fastfluence-vue
```

### 2. Konfiguracja SendGrid
#### Opcja A: SendGrid Web API (ZALECANA)
```bash
# Utwórz .env
cp .env.example .env

# Edytuj .env
USE_SENDGRID_API=true
SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

#### Opcja B: SendGrid SMTP
```bash
USE_SENDGRID_API=false
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.your-sendgrid-api-key-here
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Konfiguracja SendGrid w dashboardzie
1. Załóż konto na https://sendgrid.com
2. Idź do Settings → API Keys
3. Utwórz nowy API Key z pełnymi uprawnieniami Mail Send
4. Skopiuj klucz do `.env` jako `SENDGRID_API_KEY`
5. Zweryfikuj domenę nadawcy w Sender Authentication

### 4. Uruchomienie z Docker Compose
```bash
# Eksportuj klucz SendGrid
export SENDGRID_API_KEY=SG.your-key-here

# Uruchom aplikację
docker-compose up --build
```

### 5. Sprawdzenie dostępności
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Caddy Proxy: http://localhost

### 6. Pierwsze kroki
1. Otwórz http://localhost:5173
2. Kliknij "Jestem reklamodawcą" lub "Jestem influencerem"
3. Wypełnij formularz rejestracji
4. Sprawdź email aktywacyjny w skrzynce (również w SPAM)
5. Kliknij link aktywacyjny
6. Zaloguj się do platformy

### 7. Development Setup

**Backend:**
```bash
cd backend
poetry install

# Ustaw zmienne środowiskowe
export SENDGRID_API_KEY=SG.your-key-here
export USE_SENDGRID_API=true
export SMTP_FROM_EMAIL=noreply@yourdomain.com

poetry run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 8. Testowanie wysyłki email
```bash
# Backend z testowaniem
cd backend
poetry run pytest -v

# Test email endpoint
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "role": "advertiser",
    "display_name": "Test User",
    "contact_email": "test@example.com"
  }'
```

### 9. Alternatywne dostawcy email

#### Gmail SMTP:
```bash
USE_SENDGRID_API=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

#### Mailgun SMTP:
```bash
USE_SENDGRID_API=false
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=your-mailgun-username
SMTP_PASSWORD=your-mailgun-password
```

### 10. Produkcja
```bash
# Ustaw zmienne środowiskowe
export SENDGRID_API_KEY=SG.your-production-key
export SECRET_KEY=your-super-secret-production-key
export FRONTEND_URL=https://yourdomain.com

docker-compose -f docker-compose.prod.yml up -d
```

### 11. Troubleshooting

**Email nie docierają:**
```bash
# Sprawdź logi backend
docker-compose logs backend

# Sprawdź konfigurację
echo $SENDGRID_API_KEY

# Test SendGrid API
curl -X "POST" "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json"
```

**SendGrid błędy:**
- Sprawdź czy API Key ma uprawnienia Mail Send
- Zweryfikuj domenę nadawcy w SendGrid
- Sprawdź czy email FROM jest zweryfikowany
- Sprawdź Activity w SendGrid Dashboard

**Błędy bazy danych:**
```bash
docker-compose down -v
docker-compose up --build
```

### 12. Monitorowanie SendGrid
- Dashboard: https://app.sendgrid.com
- Activity → Email Activity
- Statistics → Stats Overview
- Sprawdzanie deliverability i bounce rate

### 13. Konfiguracja domeny nadawcy
1. W SendGrid: Settings → Sender Authentication
2. Authenticate Your Domain
3. Dodaj DNS records do swojej domeny
4. Czekaj na weryfikację (może potrwać 24h)
5. Użyj zweryfikowanej domeny w `SMTP_FROM_EMAIL`

### 14. Limity SendGrid
- Free plan: 100 emaili/dzień
- Essentials: 40,000 emaili/miesiąc za $14.95
- Pro: 100,000 emaili/miesiąc za $89.95

### 15. API Endpoints z email
- `POST /api/v1/auth/register` - Rejestracja + email aktywacyjny
- `POST /api/v1/auth/activate/{token}` - Aktywacja konta + email powitalny
- `POST /api/v1/auth/resend-activation` - Ponowne wysłanie emaila
- `POST /api/v1/auth/token` - Logowanie (tylko aktywne konta)

## Następne kroki
- [ ] Template email z HTML/CSS
- [ ] Unsubscribe links
- [ ] Email templates w SendGrid
- [ ] A/B testing emaili
- [ ] Analytics email engagement
- [ ] Powiadomienia email o nowych kampaniach
- [ ] Newsletter system
- [ ] Password reset przez email