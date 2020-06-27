from django.urls import path
from django.contrib.auth import views as user_view
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
    path('order-success/',views.order_success,name='order-success'),
    path('payment/',views.PaymentView.as_view(),name='payment'),
    path('payment-history/',views.order_history,name='payment-history'),
    path('comments/<slug>/', views.comments, name='comments'),
    path('like/<int:my_int>/', views.like, name='like'),
    path('dislike/<int:my_int>/', views.dislike, name='dislike'),
    path('reply/<int:sno>/', views.reply, name='reply'),

    path('password-reset/',user_view.PasswordResetView.as_view(template_name="password-reset.html"),name='password_reset'),
    path('password-reset-done/',user_view.PasswordResetDoneView.as_view(template_name="password-reset-done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',user_view.PasswordResetConfirmView.as_view(template_name="new-password-set.html"),name='password_reset_confirm'),
    path('password-reset-complete/',user_view.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"),name='password_reset_complete'),



]