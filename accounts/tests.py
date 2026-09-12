from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from explainer.models import Explanation


class AccountBackendTests(TestCase):
    def test_signup_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        self.assertRedirects(response, reverse("explainer"))
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_user_can_permanently_delete_account(self):
        user = User.objects.create_user(
            username="delete-me",
            password="StrongPassword123!",
        )
        Explanation.objects.create(
            user=user,
            code="print('private')",
            language="Python",
            explanation="Private explanation",
        )

        self.client.force_login(user)
        response = self.client.post(reverse("delete_account"))

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
        self.assertFalse(
            Explanation.objects.filter(user_id=user.pk).exists()
        )
