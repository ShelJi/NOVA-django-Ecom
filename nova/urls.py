from django.urls import path
from nova import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('register/', views.SignupView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('product/<str:ptype>/<str:pid>/', views.ProductView.as_view(), name='product'),
    path('category/<str:ptype>/', views.CategoryView.as_view(), name='category'),
    path('cart/', views.CartView.as_view(), name='cartview'),
    path('delcart/', views.CartdelView.as_view(), name='delcart'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('reviews/', views.ReviewView.as_view(), name='review'),
]
