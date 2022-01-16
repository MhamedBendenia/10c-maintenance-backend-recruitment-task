from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.businesslogic.errors import CannotInvestIntoProjectException
from core.businesslogic.investing import invest_into_project
from core.models import Project, Investor
from core.serializers import *


class ProjectsView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailsSerializer

    def update(self, request, *args, **kwargs):
        project_to_update = self.get_object()
        if project_to_update.funded:
            return Response(data={"details": "Cannot edit funded project."}, status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(project_to_update, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class InvestorsView(generics.ListCreateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvestorDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorDetailsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        investor_to_update = self.get_object()
        serializer = self.get_serializer(investor_to_update, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class InvestIntoProject(APIView):
    def post(self, request, pk, project_id):
        investor = get_object_or_404(Investor, pk=pk)
        project_to_invest_into = get_object_or_404(Project, pk=project_id)

        try:
            invest_into_project(investor, project_to_invest_into)
        except CannotInvestIntoProjectException as e:
            return Response(data={"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        investor.refresh_from_db()
        project_to_invest_into.refresh_from_db()
        return Response(
            data={
                "funded_project": ProjectSerializer(instance=project_to_invest_into).data,
                "remaining_amount": investor.remaining_amount
            }
        )


class ProjectMatches(generics.ListAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorsListSerializer
    
    # Display only matching investors
    def get_queryset(self):
        queryset = Investor.objects.all()
        
        project_id = self.kwargs["project_id"]
        investors_ids = Project.objects.get(id = project_id).matching_investors_ids
        
        queryset = queryset.filter(id__in = investors_ids)
        return queryset


class InvestorMatches(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer

    # Display only matching projects
    def get_queryset(self):
        queryset = Project.objects.all()
        
        investor_id = self.kwargs["pk"]
        projects_ids = Investor.objects.get(id = investor_id).matching_projects_ids
        
        queryset = queryset.filter(id__in = projects_ids)
        return queryset