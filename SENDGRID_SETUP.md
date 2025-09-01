# SendGrid Setup Guide dla FastFluence

## 1. Tworzenie konta SendGrid

1. Idź na https://sendgrid.com
2. Kliknij **Start for Free**
3. Wypełnij formularz rejestracyjny
4. Zweryfikuj email
5. Wypełnij onboarding (wybierz Web API)

## 2. Tworzenie API Key

1. Zaloguj się do SendGrid Dashboard
2. Idź do **Settings → API Keys**
3. Kliknij **Create API Key**
4. Wybierz **Full Access** lub **Restricted Access** z Mail Send permissions
5. Nazwij klucz np. "FastFluence Production"
6. Skopiuj klucz (zaczyna się od `SG.`)

## 3. Weryfikacja domeny nadawcy

### Opcja A: Single Sender Verification (szybka)
1. Idź do **Settings → Sender Authentication**
2. Kliknij **Verify a Single Sender**
3. Wprowadź:
   - From Name: "FastFluence"
   - From Email: "noreply@yourdomain.com"
   - Reply To: "support@yourdomain.com"
   - Address: Twój adres
4. Sprawdź email weryfikacyjny
5. Kliknij link w emailu

### Opcja B: Domain Authentication (zalecana dla produkcji)
1. Idź do **Settings → Sender Authentication**
2. Kliknij **Authenticate Your Domain**
3. Wprowadź swoją domenę (np. `fastfluence.pl`)
4. Wybierz **No** dla "Would you also like to brand the links for this domain?"
5. Skopiuj DNS records
6. Dodaj DNS records do swojego DNS provider:
   ```
   CNAME s1._domainkey.yourdomain.com → s1.domainkey.u123456.wl.sendgrid.net
   CNAME s2._domainkey.yourdomain.com → s2.domainkey.u123456.wl.sendgrid.net
   ```
7. Czekaj na weryfikację (może potrwać 24-48h)

## 4. Konfiguracja FastFluence

### .env configuration:
```bash
# SendGrid Web API (ZALECANA)
USE_SENDGRID_API=true
SENDGRID_API_KEY=SG.your-api-key-here
SMTP_FROM_EMAIL=noreply@yourdomain.com

# Alternative: SendGrid SMTP
# USE_SENDGRID_API=false
# SMTP_HOST=smtp.sendgrid.net
# SMTP_PORT=587
# SMTP_USERNAME=apikey
# SMTP_PASSWORD=SG.your-api-key-here
```

### docker-compose.yml:
```yaml
backend:
  environment:
    USE_SENDGRID_API: "true"
    SENDGRID_API_KEY: ${SENDGRID_API_KEY}
    SMTP_FROM_EMAIL: noreply@yourdomain.com
```

### Uruchomienie:
```bash
export SENDGRID_API_KEY=SG.your-api-key-here
docker-compose up --build
```

## 5. Test wysyłki

### Przez aplikację:
1. Zarejestruj nowe konto na http://localhost:5173
2. Sprawdź czy email aktywacyjny dotarł
3. Sprawdź Activity w SendGrid Dashboard

### Przez curl:
```bash
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

### Przez SendGrid API bezpośrednio:
```bash
curl -X "POST" "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer SG.your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [
      {
        "to": [{"email": "test@example.com"}],
        "subject": "Test Email"
      }
    ],
    "from": {"email": "noreply@yourdomain.com"},
    "content": [
      {
        "type": "text/html",
        "value": "<h1>Test email from FastFluence</h1>"
      }
    ]
  }'
```

## 6. Monitoring i Analytics

### SendGrid Dashboard:
1. **Activity** → Zobacz wysłane emaile, dostawy, bounces
2. **Statistics** → Ogólne statystyki wysyłki
3. **Suppressions** → Zablokowane adresy email
4. **Email Testing** → Inbox testing

### Logi aplikacji:
```bash
# Sprawdź logi backend
docker-compose logs backend | grep -i email

# Sprawdź błędy SendGrid
docker-compose logs backend | grep -i sendgrid
```

## 7. Troubleshooting

### Email nie docierają:
1. **Sprawdź Activity w SendGrid Dashboard**
   - Czy email został wysłany?
   - Czy był delivered czy bounced?

2. **Sprawdź SPAM folder**
   - Niezweryfikowane domeny często trafiają do SPAM

3. **Sprawdź DNS records**
   ```bash
   dig TXT yourdomain.com
   dig CNAME s1._domainkey.yourdomain.com
   ```

4. **Sprawdź konfigurację API Key**
   ```bash
   curl -H "Authorization: Bearer $SENDGRID_API_KEY" \
        https://api.sendgrid.com/v3/user/account
   ```

### Błędy API:
- **401 Unauthorized**: Nieprawidłowy API key
- **403 Forbidden**: Brak uprawnień Mail Send
- **400 Bad Request**: Nieprawidłowe dane (sprawdź email FROM)

### Częste problemy:
1. **From email nie jest zweryfikowany**
   - Zweryfikuj domenę lub single sender

2. **API Key bez uprawnień**
   - Utwórz nowy klucz z Full Access lub Mail Send

3. **DNS propagation**
   - Domain authentication może potrwać 48h

## 8. Limity i plany

### Free Plan:
- 100 emaili dziennie
- Tylko 30 dni historii
- SendGrid branding w emailach

### Essentials ($14.95/miesiąc):
- 40,000 emaili miesięcznie
- Email support
- 1 miesięczna historia

### Pro ($89.95/miesiąc):
- 100,000 emaili miesięcznie
- Phone support
- 1 miesięczna historia

## 9. Best Practices

### Email deliverability:
1. **Używaj zweryfikowanych domen**
2. **Dodaj SPF, DKIM, DMARC records**
3. **Utrzymuj niski bounce rate (<5%)**
4. **Dodaj unsubscribe link**

### Content guidelines:
1. **Unikaj spam słów** (FREE, URGENT, LIMITED TIME)
2. **Używaj odpowiedniego ratio text/HTML**
3. **Dodaj plain text version**
4. **Test na różnych klientach email**

### Monitoring:
1. **Sprawdzaj bounce rate**
2. **Monitoruj spam complaints**
3. **Sprawdzaj open rates**
4. **Używaj A/B testing**

## 10. Przydatne linki

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [API Reference](https://docs.sendgrid.com/api-reference)
- [Email Deliverability Guide](https://sendgrid.com/resource/the-email-deliverability-guide/)
- [DNS Records Checker](https://mxtoolbox.com/)
- [Email Testing Tools](https://www.mail-tester.com/)