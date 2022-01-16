from django.test import TestCase

from core.serializers import *

class ProjectDetailsSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "test",
            "description": "test",
            "amount": "500.00",
            "delivery_date": "2022-01-21"
        }

    def test_deserialize(self):
        serializer = ProjectDetailsSerializer(data=self.data)
        serializer.is_valid()
        instance = serializer.save()


class InvestorDetailsSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "Investor1",
            "remaining_amount": "400.00",
            "total_amount": "650.00",
            "individual_amount": "100.00",
            "project_delivery_deadline": "2022-01-31"
        }

    def test_deserialize(self):
        serializer = InvestorDetailsSerializer(data=self.data)
        serializer.is_valid()
        instance = serializer.save()

class InvestorSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
                "name": "Investor1",
                "remaining_amount": "400.00",
                "total_amount": "650.00",
                "individual_amount": "100.00",
                "project_delivery_deadline": "2022-01-31"
            }

    def test_deserialize(self):
        serializer = InvestorSerializer(data=self.data)
        result = serializer.is_valid()
        instance = serializer.save()

class ProjectsListSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "test",
            "description": "test",
            "amount": "500.00",
            "delivery_date": "2022-01-21"
        }

    def test_deserialize(self):
        serializer = ProjectsListSerializer(data=self.data)
        serializer.is_valid()
        instance = serializer.save()

class InvestorsListSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
                "name": "Investor1",
                "remaining_amount": "400.00",
                "total_amount": "650.00",
                "individual_amount": "100.00",
                "project_delivery_deadline": "2022-01-31"
            }

    def test_deserialize(self):
        serializer = InvestorsListSerializer(data=self.data)
        result = serializer.is_valid()
        instance = serializer.save()