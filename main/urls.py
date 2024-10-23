from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
        path('login/', views.login_index, name='LoginUrl'),
        path('logout/', views.logout_index, name='LogoutUrl'),
        path('join/', views.join_index, name='JoinUrl'),
        path('update/', views.update_index, name='UpdateUrl'),
         path('mypage/', views.mypage_view, name='MyPageUrl'),
        path('delete/', views.delete_index, name='DeleteUrl'),
        path('search', views.search_index, name="SearchUrl"),
]