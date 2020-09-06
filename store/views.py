from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter,ProductFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse





from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required


#from django.shortcuts import render, get_object_or_404

###for testing only
def test(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "store/test.html", context)

##Show dashboard of transactions

#@unauthenticated_user

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'staff'])

def dashboard(request):
	orders = Order.objects.all().order_by('-transaction_id')
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'store/dashboard.html', context)

##Show detailed view per customers

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
   #address = Customer.order_set.all()
	#customer = Customer.objects.all()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, "store/customer.html", context)




@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'store/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'store/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def user(request):
    #customer = Customer.objects.get.all()
	orders = request.user.customer.order_set.all()
#	order_details = request.order.OrderItem_set.all()
	order_count = orders.count()
   # orders = customer.order_set.all()
   # order_count =  orders.count()
    #ordrorder_count = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	#Test = OrderItem.objects.filter(order__
	#Orrders = Order__Customer.name

	print('ORDERS:', orders)

	context = {'orders':orders, 'delivered':delivered,'pending':pending,  'orders':orders, 'order_count':order_count}
	return render(request, 'store/customers.html',  context)




##main page


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()

	myFilter2 = ProductFilter(request.GET, queryset=products)
	products = myFilter2.qs

#   orders = customer.order_set.all()
#	order_count = orders.count()

#	myFilter = OrderFilter(request.GET, queryset=orders)
#	orders = myFilter.qs

#	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
#	'myFilter':myFilter}

	context = {'products':products, 'cartItems':cartItems,'myFilter2':myFilter2}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

###https://docs.djangoproject.com/en/3.0/intro/tutorial03/


def dynamic_lookup_view(request, id):
    product = Product.objects.get(id=id)
    products = get_object_or_404(Product, id=id)


    context = {'products':products, 'product':product}

    return render(request, "store/product_details.html", context)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'store/order_form.html', context)


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')


	context = {'form':form}
	return render(request, 'store/register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('store')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', { 'question': question })

# Get question and display results
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    print(votedata)
    return JsonResponse(votedata, safe=False)



#from itertools import chain
#def get_all_cars():
#    bmws = Bmw.objects.filter()
#    teslas = Tesla.objects.filter()
#    cars_list = sorted(
#        chain(bmws, teslas),
#        key=lambda car: car.created, reverse=True)
#    return cars_list