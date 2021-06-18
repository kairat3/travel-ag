from django.urls import path
from . import views


urlpatterns = [
    path('tours/create/', views.PostCreateView.as_view()),
    path('tours/', views.TourListView.as_view()),
    path('tours/<int:pk>/', views.PostDetailView.as_view()),
    path('tours/<int:pk>/update/', views.PostUpdateView.as_view()),
    path('tours/<int:pk>/delete/', views.PostDeleteView.as_view()),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('travelshop/', views.ProductListView.as_view()),
    path('travelshop/create/', views.ProductCreateView.as_view()),
    path('like/', views.LikeListView.as_view()),
    path('like/create/', views.LikeCreateView.as_view()),
    path('rating/', views.RatingListView.as_view()),
    path('rating/create/', views.RatingCreateView.as_view()),
]
