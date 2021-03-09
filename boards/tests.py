from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Board, Job


class BoardTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.board = Board.objects.create(title="Jobs", user=self.user)

    def test_create_board(self):
        self.assertEqual(f"{self.board.title}", "Jobs")

    def test_board_detail_view_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("board_detail", kwargs={"board_slug": self.board.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jobs")
        self.assertTemplateUsed(response, "boards/board_detail.html")

    def test_board_update_ajax_required(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("board_update", kwargs={"board_slug": self.board.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_board_detail_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("board_detail", kwargs={"board_slug": self.board.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/boards/%s/" % (reverse("login"), self.board.slug)
        )


class JobTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.board = Board.objects.create(title="Jobs", user=self.user)
        self.job = Job.objects.create(
            board=self.board,
            company="Company",
            title="Job",
            deadline=date(2020, 10, 26),
            progress="Applied",
            description="This is a test.",
        )

    def test_job_create(self):
        self.assertEqual(f"{self.job.company}", "Company")
        self.assertEqual(f"{self.job.title}", "Job")
        self.assertEqual(
            f"{self.job.deadline}", "2020-10-26"
        )  # str since value is not saved as python obj
        self.assertEqual(f"{self.job.progress}", "Applied")
        self.assertEqual(f"{self.job.description}", "This is a test.")

    def test_job_update_ajax_required(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse(
                "job_update",
                kwargs={"board_slug": self.job.board.slug, "job_slug": self.job.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_job_update_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            reverse(
                "job_update",
                kwargs={"board_slug": self.job.board.slug, "job_slug": self.job.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=/boards/%s/jobs/%s/edit/"
            % (reverse("login"), self.job.board.slug, self.job.slug),
        )
