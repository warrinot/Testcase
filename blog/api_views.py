from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post


class PostApiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
