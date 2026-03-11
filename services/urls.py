from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('canteens/', views.canteen_list, name='canteen_list'),
    path('canteens/<int:canteen_id>/', views.canteen_detail, name='canteen_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('xerox/', views.xerox_list, name='xerox_list'),
    path('xerox/<int:center_id>/', views.xerox_detail, name='xerox_detail'),
    path('api/order_status/', views.api_order_status, name='api_order_status'),
    
    # Management URLs
    path('canteen/edit/', views.edit_canteen, name='edit_canteen'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('xerox/edit/', views.edit_xerox_center, name='edit_xerox_center'),
    path('admin-dashboard/', views.site_admin_dashboard, name='site_admin_dashboard'),
    path('payment/', views.payment_gateway, name='payment_gateway'),
    path('food-order/<int:order_id>/track/', views.track_food_order, name='track_food_order'),
]
