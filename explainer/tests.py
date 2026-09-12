from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Explanation
from .views import detect_language


class LanguageDetectionTests(TestCase):
    def test_detects_python(self):
        self.assertEqual(
            detect_language('print("Hello")'),
            "Python",
        )

    def test_detects_html(self):
        self.assertEqual(
            detect_language("<!DOCTYPE html><html></html>"),
            "HTML",
        )

    def test_detects_css(self):
        self.assertEqual(
            detect_language("body { color: red; }"),
            "CSS",
        )

    def test_detects_c(self):
        self.assertEqual(
            detect_language(
                '#include <stdio.h>\n'
                'int main() { printf("Hello"); return 0; }'
            ),
            "C",
        )

    def test_detects_cpp(self):
        self.assertEqual(
            detect_language(
                '#include <iostream>\n'
                'int main() { std::cout << "Hello"; }'
            ),
            "C++",
        )


class WorkspaceBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!",
        )

    def test_workspace_requires_login(self):
        response = self.client.get(reverse("explainer"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_logged_in_user_can_open_workspace(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("explainer"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your code")

    def test_history_only_contains_current_users_explanations(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPassword123!",
        )
        Explanation.objects.create(
            user=self.user,
            code="print('mine')",
            language="Python",
            explanation="My explanation",
        )
        Explanation.objects.create(
            user=other_user,
            code="print('theirs')",
            language="Python",
            explanation="Other explanation",
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse("history"))

        self.assertContains(response, "print(&#x27;mine&#x27;)")
        self.assertNotContains(response, "print(&#x27;theirs&#x27;)")

    def test_user_can_clear_only_their_history(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPassword123!",
        )
        Explanation.objects.create(
            user=self.user,
            code="print('mine')",
            language="Python",
            explanation="My explanation",
        )
        Explanation.objects.create(
            user=other_user,
            code="print('theirs')",
            language="Python",
            explanation="Other explanation",
        )

        self.client.force_login(self.user)
        response = self.client.post(reverse("history_clear"))

        self.assertRedirects(response, reverse("history"))
        self.assertFalse(
            Explanation.objects.filter(user=self.user).exists()
        )
        self.assertTrue(
            Explanation.objects.filter(user=other_user).exists()
        )
