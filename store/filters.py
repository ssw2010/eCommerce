import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_ordered", lookup_expr='gte')
	end_date = DateFilter(field_name="date_ordered", lookup_expr='lte')
	#note = CharFilter(field_name='note', lookup_expr='icontains')

	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created', 'Status', 'Complete']

class ProductFilter(django_filters.FilterSet):
	#note = CharFilter(field_name='note', lookup_expr='icontains')
	name= CharFilter(field_name='name', lookup_expr='icontains', label = 'Common Name  ')
	sname= CharFilter(field_name='sname', lookup_expr='icontains', label = 'Scientific Name  ')
	#sname= CharFilter(field_name='Form', lookup_expr='icontains', label = 'Size  ')

	class Meta:
		model = Product
		fields = '__all__'
		exclude = ['image','price', 'Form', 'Soil_Conditions','Aspect', 'Sconditions', 'Description', 'Family', 'Sconditions', 'Natural_Habitat', 'Special_Feature', 'QuantityOfStock', 'digital']


