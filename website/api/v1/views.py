from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from website.models import StatusDiscoverImage
from .serializers import StatusSerializer

class StatusModelViewSet(viewsets.ModelViewSet):

    queryset = StatusDiscoverImage.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]