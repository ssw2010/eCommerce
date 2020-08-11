from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
#	path('<int:id>/', views.product_detail_view, name='product-detail'),
    path('<int:id>/', views.dynamic_lookup_view, name='product'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path("test/", views.test, name="test"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]



###test