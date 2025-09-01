import pytest
from unittest.mock import patch, MagicMock
from app.email import (
    send_activation_email,
    send_welcome_email,
    send_email_via_sendgrid,
    send_email_via_smtp,
    generate_activation_token,
    get_activation_email_html,
    get_welcome_email_html
)
from app.models import User, UserRole


@pytest.fixture
def test_user():
    return User(
        id=1,
        email="test@example.com",
        display_name="Test User",
        contact_email="test@example.com",
        role=UserRole.ADVERTISER,
        hashed_password="hashed",
        is_active=False
    )


def test_generate_activation_token():
    token = generate_activation_token()
    assert len(token) > 20
    assert isinstance(token, str)

    # Test uniqueness
    token2 = generate_activation_token()
    assert token != token2


def test_get_activation_email_html(test_user):
    token = "test-token-123"
    html = get_activation_email_html(test_user, token)

    assert "FastFluence" in html
    assert test_user.display_name in html
    assert token in html
    assert "Aktywuj konto" in html
    assert "http://localhost:5173/activate/" in html


def test_get_welcome_email_html(test_user):
    html = get_welcome_email_html(test_user)

    assert "FastFluence" in html
    assert test_user.display_name in html
    assert "pomyślnie aktywowane" in html
    assert "dashboard" in html


@patch('app.email.httpx.Client')
def test_send_email_via_sendgrid_success(mock_client):
    # Mock successful SendGrid API response
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_client.return_value.__enter__.return_value.post.return_value = mock_response

    result = send_email_via_sendgrid(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<h1>Test</h1>"
    )

    assert result is True
    mock_client.return_value.__enter__.return_value.post.assert_called_once()


@patch('app.email.httpx.Client')
def test_send_email_via_sendgrid_failure(mock_client):
    # Mock failed SendGrid API response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_client.return_value.__enter__.return_value.post.return_value = mock_response

    result = send_email_via_sendgrid(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<h1>Test</h1>"
    )

    assert result is False


@patch('app.email.smtplib.SMTP')
def test_send_email_via_smtp_success(mock_smtp):
    # Mock successful SMTP
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = send_email_via_smtp(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<h1>Test</h1>"
    )

    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()


@patch('app.email.smtplib.SMTP')
def test_send_email_via_smtp_failure(mock_smtp):
    # Mock SMTP exception
    mock_smtp.side_effect = Exception("SMTP Error")

    result = send_email_via_smtp(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<h1>Test</h1>"
    )

    assert result is False


@patch('app.email.settings')
@patch('app.email.send_email_via_sendgrid')
def test_send_activation_email_with_sendgrid(mock_sendgrid, mock_settings, test_user):
    mock_settings.USE_SENDGRID_API = True
    mock_settings.SENDGRID_API_KEY = "test-key"
    mock_sendgrid.return_value = True

    result = send_activation_email(test_user, "test-token")

    assert result is True
    mock_sendgrid.assert_called_once()


@patch('app.email.settings')
@patch('app.email.send_email_via_smtp')
def test_send_activation_email_with_smtp(mock_smtp, mock_settings, test_user):
    mock_settings.USE_SENDGRID_API = False
    mock_settings.SENDGRID_API_KEY = ""
    mock_smtp.return_value = True

    result = send_activation_email(test_user, "test-token")

    assert result is True
    mock_smtp.assert_called_once()


@patch('app.email.settings')
@patch('app.email.send_email_via_sendgrid')
def test_send_welcome_email_with_sendgrid(mock_sendgrid, mock_settings, test_user):
    mock_settings.USE_SENDGRID_API = True
    mock_settings.SENDGRID_API_KEY = "test-key"
    mock_sendgrid.return_value = True

    test_user.is_active = True
    result = send_welcome_email(test_user)

    assert result is True
    mock_sendgrid.assert_called_once()


def test_email_content_creator_vs_advertiser():
    advertiser = User(
        email="advertiser@example.com",
        display_name="Advertiser User",
        contact_email="advertiser@example.com",
        role=UserRole.ADVERTISER,
        hashed_password="hashed",
        is_active=True
    )

    creator = User(
        email="creator@example.com",
        display_name="Creator User",
        contact_email="creator@example.com",
        role=UserRole.CREATOR,
        hashed_password="hashed",
        is_active=True
    )

    advertiser_html = get_welcome_email_html(advertiser)
    creator_html = get_welcome_email_html(creator)

    # Check role-specific content
    assert "reklamodawcy" in advertiser_html
    assert "Panel reklamodawcy" in advertiser_html
    assert "Tworzyć kampanie marketingowe" in advertiser_html

    assert "twórcy" in creator_html
    assert "Znajdź zlecenia" in creator_html
    assert "Przeglądać dostępne kampanie" in creator_html


@patch('app.email.settings')
def test_sendgrid_api_payload_structure(mock_settings):
    mock_settings.SMTP_FROM_EMAIL = "noreply@fastfluence.pl"
    mock_settings.SENDGRID_API_KEY = "SG.test-key"

    with patch('app.email.httpx.Client') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        send_email_via_sendgrid(
            to_email="test@example.com",
            subject="Test Subject",
            html_content="<h1>Test Content</h1>"
        )

        # Verify API call structure
        call_args = mock_client.return_value.__enter__.return_value.post.call_args

        # Check URL
        assert call_args[0][0] == "https://api.sendgrid.com/v3/mail/send"

        # Check payload structure
        payload = call_args[1]['json']
        assert 'personalizations' in payload
        assert 'from' in payload
        assert 'content' in payload

        assert payload['personalizations'][0]['to'][0]['email'] == "test@example.com"
        assert payload['personalizations'][0]['subject'] == "Test Subject"
        assert payload['from']['email'] == "noreply@fastfluence.pl"
        assert payload['content'][0]['type'] == "text/html"
        assert payload['content'][0]['value'] == "<h1>Test Content</h1>"

        # Check headers
        headers = call_args[1]['headers']
        assert 'Authorization' in headers
        assert headers['Authorization'] == "Bearer SG.test-key"
        assert headers['Content-Type'] == "application/json"


@patch('app.email.settings')
def test_email_fallback_mechanism(mock_settings, test_user):
    # Test fallback from SendGrid to SMTP when SendGrid fails
    mock_settings.USE_SENDGRID_API = True
    mock_settings.SENDGRID_API_KEY = "test-key"

    with patch('app.email.send_email_via_sendgrid') as mock_sendgrid:
        mock_sendgrid.return_value = False  # SendGrid fails

        with patch('app.email.send_email_via_smtp') as mock_smtp:
            mock_smtp.return_value = True  # SMTP succeeds

            # This would need to be implemented in the actual email functions
            # For now, just test that SendGrid was called and failed
            result = send_activation_email(test_user, "test-token")
            mock_sendgrid.assert_called_once()


def test_activation_token_security():
    # Test that tokens are cryptographically secure
    tokens = [generate_activation_token() for _ in range(100)]

    # All tokens should be unique
    assert len(set(tokens)) == 100

    # Tokens should be long enough
    for token in tokens:
        assert len(token) >= 32

    # Tokens should be URL-safe
    import string
    allowed_chars = string.ascii_letters + string.digits + '-_'
    for token in tokens:
        assert all(c in allowed_chars for c in token)