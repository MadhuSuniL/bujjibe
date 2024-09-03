from django.urls import path
from .views import QueryMetaInfoView, SpaceTopicsView, SourceTypesView

urlpatterns = [
    path('query/meta-info/', QueryMetaInfoView.as_view(), name='query_meta_info'),
    path('space-topics/', SpaceTopicsView.as_view(), name='space_topics'),
    path('sources/', SourceTypesView.as_view(), name='sources'),
]
