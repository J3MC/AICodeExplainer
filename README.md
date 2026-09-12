# AI Code Explainer

[![Django checks](https://github.com/J3MC/AICodeExplainer/actions/workflows/django.yml/badge.svg)](https://github.com/J3MC/AICodeExplainer/actions/workflows/django.yml)

AI Code Explainer is a Django web app that turns code and plain text into clear, beginner-friendly explanations using Groq AI.

## What it does

Paste a code snippet or plain text, choose the matching language, and receive a structured explanation. Signed-in users can revisit their explanations in a private history area, while administrators can manage users and saved explanations through Django Admin.

## Features

- User signup, login, logout, and permanent account deletion
- Code and text explanations for Text, Python, JavaScript, HTML, CSS, C, C++, and Java
- Per-user explanation history with individual and bulk deletion
- Markdown-safe AI responses with formatted code blocks and tables
- Responsive dark/light interface with mobile-friendly layouts
- Django admin dashboard for managing users and explanations

## Supported input

The explainer accepts plain text plus Python, JavaScript, HTML, CSS, C, C++, and Java. It does not execute submitted code; it only sends the input to the configured AI provider for explanation.

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

GitHub Actions runs `manage.py check` and the full test suite automatically on every push to `main` and on pull requests.

## Project structure

- `config/` — Django settings and project URLs
- `accounts/` — signup and account management
- `explainer/` — workspace, history, AI explanation logic, templates, and static files
- `.github/workflows/` — automated checks for GitHub

## Security note

Never commit `.env`, API keys, `db.sqlite3`, or the virtual environment. These files are excluded by `.gitignore`.
