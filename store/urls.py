from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('dashboard/', views.dashboard, name="dashboard"),
#	path('<int:id>/', views.product_detail_view, name='product-detail'),
    path('<int:id>/', views.dynamic_lookup_view, name='product'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
 #   path('customers/', views.customers, name="customers"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path("test/", views.test, name="test"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
	path('create_order/', views.createOrder, name="create_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('user/', views.user, name="user"),


	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
        name="password_reset_complete"),
    path('index', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('resultsdata/<str:obj>/', views.resultsData, name="resultsdata"),

]



###test