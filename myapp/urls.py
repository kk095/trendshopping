from django.urls import path
from . import views
urlpatterns = [
    path('', views.Courses, name='home-page'),
    path('signup' ,views.handlesign,name='sign'),
    path('login',views.handlelog,name='log'),
    path('logout',views.handlelogout, name='logout'),
    path('checkout/<slug:slug_field>',views.checkout, name='checkout'),
    path('about/',views.about, name='about'),
    path('about/history/', views.history,name='history'),
    path('contact/',views.contactus, name='contact'),
    path('search/', views.search, name='search'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', views.remove_from_card, name='remove_from_cart'),
    path('order-summary/', views.order_summary,name='order-summary'),
    path('register/',views.register,name='register'),
    path('plus/<slug>/',views.plus,name='plus'),
    path('minus/<slug>/',views.minus,name='minus'),
    path('order-place/',views.order_place,name='order-place'),



]