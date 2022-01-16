from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone

from core.models import Investor, Project


class InvestorDetailsViewTestCase(TestCase):
    @staticmethod
    def _get_url(investor_id):
        return f'/investors/{investor_id}/'

    def setUp(self) -> None:
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self):
        url = self._get_url(self.investor.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        investor_data = response.data

        self.assertEqual(investor_data['id'], self.investor.id)
        self.assertEqual(investor_data['name'], self.investor.name)


class ProjectDetailsViewTestCase(TestCase):
    @staticmethod
    def _get_url(project_id):
        return f'/projects/{project_id}/'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self):
        url = self._get_url(self.project.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_data = response.data

        self.assertEqual(project_data['id'], self.project.id)
        self.assertEqual(project_data['name'], self.project.name)

class ProjectsViewTestCase(TestCase):
    @staticmethod
    def _get_url():
        return '/projects/'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_project', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self):
        url = self._get_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_data = response.data[0]

        self.assertEqual(project_data['id'], self.project.id)
        self.assertEqual(project_data['name'], self.project.name)

class InvestorsViewTestCase(TestCase):
    @staticmethod
    def _get_url():
        return '/investors/'

    def setUp(self) -> None:
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self):
        url = self._get_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        investor_data = response.data[0]

        self.assertEqual(investor_data['id'], self.investor.id)
        self.assertEqual(investor_data['name'], self.investor.name)

class InvestIntoProjectTestCase(TestCase):
    @staticmethod
    def _get_url(project_id):
        return f'/projects/{project_id}/'

    @staticmethod
    def _post_url(investor_id, project_id):
        return f'/investors/{investor_id}/invest/{project_id}/'

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

    def test_get(self):
        url_post = self._post_url(self.investor.id, self.project.id)
        self.client.post(url_post)

        url_get = self._get_url(self.project.id)
        response = self.client.get(url_get)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_data = response.data

        self.assertEqual(project_data['funded_by'], self.investor.id)
        self.assertEqual(project_data['funded'], True)
