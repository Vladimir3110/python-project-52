from django.urls import path

from .views import (
                    UserCreateView,
                    UserDeleteView,
                    UserListView,
                    UserLoginView,
                    UserLogoutView,
                    UserUpdateView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
