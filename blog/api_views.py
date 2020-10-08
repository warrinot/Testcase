from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post


class PostApiViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('blog__user').order_by('date_added')

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
