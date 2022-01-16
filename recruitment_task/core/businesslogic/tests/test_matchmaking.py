from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from core.models import Investor, Project

class MatchmakingTestCase(TestCase):
    @staticmethod
    def _get_url_for_projects_matches(project_id):
        return f'/projects/{project_id}/matches/'

    @staticmethod
    def _get_url_for_investors_matches(investor_id):
        return f'/investors/{investor_id}/matches/'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='project_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=20)
        )
        self.investor = Investor.objects.create(
            name='investor_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_matchmaking_for_project(self):
        url_get = self._get_url_for_projects_matches(self.project.id)
        response = self.client.get(url_get)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        investor_data = response.data[0]

        self.assertEqual(investor_data['id'], self.investor.id)

    def test_matchmaking_for_investor(self):
        url_get = self._get_url_for_investors_matches(self.investor.id)
        response = self.client.get(url_get)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_data = response.data[0]

        self.assertEqual(project_data['id'], self.project.id)
