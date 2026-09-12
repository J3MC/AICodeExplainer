# AI Code Explainer

AI Code Explainer is a Django web app that turns code and plain text into clear, beginner-friendly explanations using Groq AI.

## Features

- User signup, login, logout, and permanent account deletion
- Code and text explanations for Text, Python, JavaScript, HTML, CSS, C, C++, and Java
- Per-user explanation history with individual and bulk deletion
- Markdown-safe AI responses with formatted code blocks and tables
- Responsive dark/light interface with mobile-friendly layouts
- Django admin dashboard for managing users and explanations

## Local setup

1. Create and activate a virtual environment.
2. Install the dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Create `.env` from `.env.example` and add your Groq API key.
4. Apply migrations:

   ```powershell
   py manage.py migrate
   ```

5. Start the development server:

   ```powershell
   py manage.py runserver
   ```

Open `http://127.0.0.1:8000/` in your browser.

## Tests

```powershell
py manage.py test
```

## Security note

Never commit `.env`, API keys, `db.sqlite3`, or the virtual environment. These files are excluded by `.gitignore`.
