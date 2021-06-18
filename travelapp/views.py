from django_filters import rest_framework as filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from user.models import CustomUser
from . import serializers
from .models import Comment, Category, Product, Tour, Rating, Like
from .permissions import IsOwnerOrReadOnly
from django.db import connection


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.select_related('owner', 'category')
    serializer_class = serializers.TourSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'category')
    pagination_class = StandardResultsSetPagination

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print(f'queries counted: {len(connection.queries)}')
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(id__icontains=search))
        return queryset


class PostCreateView(generics.CreateAPIView):
    """Endpoint for create post: only authenticated user can post"""
    serializer_class = serializers.TourSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveAPIView):
    """Endpoint for retrieve all posts"""
    queryset = Tour.objects.all()
    serializer_class = serializers.TourSerializer


class PostDeleteView(generics.DestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = serializers.TourSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class PostUpdateView(generics.UpdateAPIView):
    queryset = Tour.objects.all()
    serializer_class = serializers.TourSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    pagination_class = StandardResultsSetPagination


class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = serializers.RatingSerializer


class LikeListView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer


class LikeCreateView(generics.CreateAPIView):
    serializer_class = serializers.LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingCreateView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

