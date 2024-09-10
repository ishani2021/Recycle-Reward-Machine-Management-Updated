"""
URL configuration for wasteproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from wasteapp.views import place_order_view, cancel_order_view, company_dashboard, \
user_dashboard, enter_waste_view, update_profile, login_view, company_check, view_orders_view, initial, select_user, \
view_dashboard, user_dashboard_home, company_dashboard_home, login_base, user_login

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    path('selectuser/',select_user),
    path('',initial),
    path('dash/', view_dashboard),
    path('user_home/',user_dashboard_home),
    path('company_home', company_dashboard_home),
    path('login/',login_base),
    path('userlogin/', user_login),

    # User URLs
    path('login/', login_view, name='login'),
    path('credits/', user_dashboard, name='credits'),
    path('update/', update_profile, name='update'),
    path('enter_waste/', enter_waste_view, name='enter_waste'),

    # Company URLs
    path('company/dashboard/', company_dashboard, name='company_dashboard'),
    path('company/order/place/', place_order_view, name='place_order'),
    path('company/order/cancel/<int:order_id>/', cancel_order_view, name='cancel_order'),
    path('company/orders/', view_orders_view, name='view_orders'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


