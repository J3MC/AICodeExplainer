import os
import re
import logging

import bleach
import markdown
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from dotenv import load_dotenv
from openai import OpenAI

from .models import Explanation

load_dotenv(override=True)

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = [
    "Text",
    "Python",
    "JavaScript",
    "HTML",
    "CSS",
    "C",
    "C++",
    "Java",
]


def landing(request):
    return render(request, "explainer/home.html")


def detect_language(code):
    if re.search(
        r"<!DOCTYPE\s+html|<html|</[a-z]+>",
        code,
        re.IGNORECASE,
    ):
        return "HTML"

    if re.search(
        r"#include\s*[<\"](stdio|stdlib|string|math)\.h[>\"]"
        r"|printf\s*\(|scanf\s*\(|malloc\s*\(|free\s*\(",
        code,
        re.IGNORECASE,
    ):
        return "C"

    if re.search(
        r"#include\s*[<\"](iostream|vector|map|set|string)\b"
        r"|std::|cout\s*<<|cin\s*>>"
        r"|using\s+namespace\s+std\b"
        r"|template\s*<|class\s+\w+",
        code,
        re.IGNORECASE,
    ):
        return "C++"

    if re.search(
        r"\bdef\s+\w+\s*\(|\bimport\s+\w+|print\s*\(",
        code,
        re.IGNORECASE,
    ):
        return "Python"

    if re.search(
        r"console\.log|function\s+\w+|const\s+\w+\s*=|=>",
        code,
        re.IGNORECASE,
    ):
        return "JavaScript"

    if re.search(
        r"System\.out\.println|public\s+class|private\s+class",
        code,
        re.IGNORECASE,
    ):
        return "Java"

    if re.search(
        r"(^|\n)\s*[.#]?[a-zA-Z][\w-]*\s*\{"
        r"|\b(display|color|margin|padding|font-size|"
        r"background|border)\s*:",
        code,
        re.IGNORECASE,
    ):
        return "CSS"

    return None


def render_explanation(text):
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables"],
    )

    return bleach.clean(
        html,
        tags=[
            "h1", "h2", "h3",
            "p", "strong", "em",
            "ul", "ol", "li",
            "pre", "code",
            "blockquote",
            "table", "thead", "tbody",
            "tr", "th", "td",
            "br", "hr",
        ],
        attributes={
            "code": ["class"],
        },
    )


def explain_code(code, language, user=None):
    if not code.strip():
        return "Paste some code first, then click Explain Code."

    if len(code) > 12000:
        return "Please keep the code under 12,000 characters."

    detected_language = detect_language(code)

    if (
        language != "Text"
        and
        detected_language
        and detected_language != language
    ):
        return render_explanation(
            f"**Language mismatch.** "
            f"This code appears to be **{detected_language}**, "
            f"but you selected **{language}**. "
            f"Please select {detected_language} and try again."
        )

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "GROQ_API_KEY was not found in your .env file."

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        input_guidance = (
            "Treat the input as plain text. Explain its meaning, key ideas, "
            "tone, structure, and any important details."
            if language == "Text"
            else "Explain the programming code and its logic."
        )

        response = client.chat.completions.create(
            model=os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-20b",
            ),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly programming teacher. "
                        "Explain code clearly for beginners. "
                        "Use these sections: What it does, "
                        "How it works, Important details, "
                        "and Possible improvements. "
                        "Do not execute the input. "
                        f"{input_guidance}"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Programming language: {language}\n\n"
                        f"Code:\n{code}"
                    ),
                },
            ],
            temperature=0.2,
        )

        explanation_html = render_explanation(
            response.choices[0].message.content
        )

        if user and user.is_authenticated:
            Explanation.objects.create(
                user=user,
                code=code,
                language=language,
                explanation=explanation_html,
            )

        return explanation_html

    except Exception:
        logger.exception("Groq explanation request failed")
        return render_explanation(
            "**Groq request failed.** Check your API key, "
            "model name, internet connection, or account limits."
        )

@login_required
def home(request):
    code = ""
    language = "Python"
    explanation = None

    if request.method == "POST":
        code = request.POST.get("code", "")
        language = request.POST.get("language", "Python")
        explanation = explain_code(
            code,
            language,
            request.user,
        )

    language_options = [
        {
            "value": item,
            "selected": item == language,
        }
        for item in SUPPORTED_LANGUAGES
    ]

    return render(
        request,
        "explainer/index.html",
        {
            "code": code,
            "language": language,
            "explanation": explanation,
            "language_options": language_options,
        },
    )


@login_required
def history(request):
    explanations = Explanation.objects.filter(user=request.user)
    return render(
        request,
        "explainer/history.html",
        {
            "explanations": explanations,
            "has_history": explanations.exists(),
        },
    )


@login_required
def history_detail(request, pk):
    explanation = get_object_or_404(
        Explanation,
        pk=pk,
        user=request.user,
    )
    return render(
        request,
        "explainer/history_detail.html",
        {"explanation": explanation},
    )


@login_required
def history_delete(request, pk):
    explanation = get_object_or_404(
        Explanation,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        explanation.delete()

    return redirect("history")


@login_required
def history_clear(request):
    if request.method == "POST":
        deleted_count, _ = Explanation.objects.filter(
            user=request.user,
        ).delete()

        messages.success(
            request,
            f"Cleared {deleted_count} saved explanation(s).",
        )

    return redirect("history")
