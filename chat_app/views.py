from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base_app.consonants import SourceTypes, SpaceTopics

class QueryMetaInfoView(APIView):
    def get(self, request, *args, **kwargs):
        space_topics = SpaceTopics().get_space_topics()
        filtered_sources = SourceTypes.get_sources()
        response_data = {
            "space_topics": space_topics,
            "sources": filtered_sources
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SpaceTopicsView(APIView):
    def get(self, request, *args, **kwargs):
        space_topics = SpaceTopics().get_space_topics()
        return Response({"space_topics": space_topics}, status=status.HTTP_200_OK)


class SourceTypesView(APIView):
    def get(self, request, *args, **kwargs):
        filtered_sources = SourceTypes.get_sources()
        return Response({"sources": filtered_sources}, status=status.HTTP_200_OK)
