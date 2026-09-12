from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("explainer")
    else:
        form = SignUpForm()

    return render(
        request,
        "explainer/signup.html",
        {"form": form},
    )


@login_required
def delete_account(request):
    if request.method != "POST":
        return redirect("explainer")

    user = request.user
    logout(request)
    user.delete()

    return redirect("home")
