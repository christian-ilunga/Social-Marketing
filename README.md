# Social Media Marketer Website (Python + Flask)

This is a professional, single-page marketing site for a social media marketer with:

- **Modern, responsive landing page** (hero, services, process, projects, about, contact) similar to [`SmartSocial`](https://christian-ilunga.github.io/SmartSocial/).
- **Contact form** that sends enquiries to your email.
- **Floating chat widget** that opens a WhatsApp chat directly with your number so you can reply from your phone.

The backend is built with **Flask** and structured so you can easily extend it.

---

## 1. Project structure

- `app.py` – Flask application with:
  - `GET /` – serves the landing page.
  - `POST /api/contact` – handles contact form submissions and emails you.
  - `POST /api/chat` – handles chat widget messages and notifies you.
- `templates/index.html` – main landing page.
- `static/css/styles.css` – styling for a clean, modern dark UI.
- `static/js/main.js` – front-end logic for the contact form and chat widget.
- `requirements.txt` – Python dependencies.

---

## 2. Setup

### 2.1. Create and activate a virtual environment (recommended)

In PowerShell, from the project folder (`websites with backend`):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2.2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2.3. Configure environment variables

Create a file named `.env` in the project root (same folder as `app.py`) with your email settings:

```env
OWNER_EMAIL=christianilungamulumba@gmail.com

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=christianilungamulumba@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

- **OWNER_EMAIL**: where enquiries and chat notifications are sent (defaults to your Gmail if not set).
- **SMTP\_***: SMTP details from your email provider (e.g. Gmail app password, Outlook, custom domain).

> Email sending will fail if these values are missing or incorrect – the backend returns a user‑friendly error message.

---

## 3. Run the app

From the project directory (with the virtualenv activated):

```powershell
python app.py
```

By default the site runs on `http://127.0.0.1:8000/`.

Open that URL in your browser to view the site.

---

## 4. How contact & chat work

### 4.1. Contact form (`/api/contact`)

- Frontend (`index.html` + `static/js/main.js`) sends a `POST` request to `/api/contact` with:
  - `name`
  - `email`
  - `message`
- The backend validates the fields and, if everything is valid:
  - Sends an email to `OWNER_EMAIL` summarising the enquiry.
  - Returns `{"ok": true}` to the frontend.

If something goes wrong (missing fields, bad email config), the user sees a friendly error message on the form.

### 4.2. Chat widget (WhatsApp click‑to‑chat)

- The floating chat widget in the bottom-right collects an optional `name` and `message`.
- When the visitor clicks **Open WhatsApp Chat**:
  - The browser opens a new tab to `https://wa.me/27692894703` with their message prefilled.
  - This starts a WhatsApp chat directly with your number, so you see the message instantly on your phone and can reply there.

This matches the behaviour of the [`SmartSocial` chat widget](https://christian-ilunga.github.io/SmartSocial/) while keeping the backend simple.

---

## 5. Connecting to other platforms (optional)

If you later want automated SMS or advanced WhatsApp features (broadcasts, bots, etc.), you can still integrate:

- **WhatsApp Cloud API**
- **Twilio**, **Nexmo**, or other SMS providers

by calling them from `_send_chat_notification(...)` in `app.py`. For now, the default setup keeps things simple:

- Contact form → email to your Gmail.
- Chat widget → opens WhatsApp directly on your phone.

---

## 6. Customisation

- Update all placeholder text like **Your Name**, **YourBrand**, and `you@example.com` in:
  - `templates/index.html`
  - `.env`
- Adjust colours and layout in `static/css/styles.css`.
- Add case studies, testimonials, and additional sections to `index.html` as needed.

If you tell me your **brand name, colours, and positioning**, I can further tailor the copy and styling.  

