from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, StudentProfileForm, XeroxOrderForm, MenuItemForm, CanteenForm, XeroxCenterForm
from .models import User, Canteen, MenuItem, FoodOrder, FoodOrderItem, XeroxCenter, XeroxOrder

def home(request):
    return render(request, 'services/home.html')

def custom_csrf_failure(request, reason=""):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'services/csrf_failure.html', {'reason': reason}, status=403)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            if role == 'student':
                if profile_form.is_valid():
                    user = form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    login(request, user)
                    return redirect('dashboard')
            else:
                user = form.save()
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
        profile_form = StudentProfileForm()
    return render(request, 'services/register.html', {'form': form, 'profile_form': profile_form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'services/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        if request.method == 'POST' and 'cancel_order' in request.POST:
            order_type = request.POST.get('order_type')
            order_id = request.POST.get('order_id')
            if order_type == 'food':
                order = get_object_or_404(FoodOrder, id=order_id, student=user)
                if order.status == 'Pending':
                    order.status = 'Cancelled'
                    order.save()
            elif order_type == 'xerox':
                order = get_object_or_404(XeroxOrder, id=order_id, student=user)
                if order.status == 'Pending':
                    order.status = 'Cancelled'
                    order.save()
            return redirect('dashboard')
            
        food_orders = FoodOrder.objects.filter(student=user).exclude(status='Cancelled').order_by('-created_at')[:5]
        xerox_orders = XeroxOrder.objects.filter(student=user).exclude(status='Cancelled').order_by('-created_at')[:5]
        return render(request, 'services/student_dashboard.html', {
            'food_orders': food_orders,
            'xerox_orders': xerox_orders
        })
    elif user.role == 'canteen_owner':
        canteen = getattr(user, 'canteens', None)
        canteen_obj = canteen.first() if canteen else None
        if not canteen_obj:
            return render(request, 'services/canteen_dashboard.html', {'setup_required': True})
            
        if request.method == 'POST' and 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('status')
            order = get_object_or_404(FoodOrder, id=order_id, canteen=canteen_obj)
            order.status = new_status
            order.save()
            return redirect('dashboard')
            
        orders = FoodOrder.objects.filter(canteen=canteen_obj).exclude(status='Cancelled').order_by('-created_at')
        menu_items = MenuItem.objects.filter(canteen=canteen_obj)
        
        return render(request, 'services/canteen_dashboard.html', {
            'canteen': canteen_obj,
            'orders': orders,
            'menu_items': menu_items,
            'status_choices': FoodOrder.STATUS_CHOICES
        })
    elif user.role == 'xerox_owner':
        center = getattr(user, 'xerox_centers', None)
        center_obj = center.first() if center else None
        if not center_obj:
            return render(request, 'services/xerox_dashboard.html', {'setup_required': True})
            
        if request.method == 'POST' and 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('status')
            order = get_object_or_404(XeroxOrder, id=order_id, center=center_obj)
            order.status = new_status
            order.save()
            return redirect('dashboard')
            
        orders = XeroxOrder.objects.filter(center=center_obj).exclude(status='Cancelled').order_by('-created_at')
        
        return render(request, 'services/xerox_dashboard.html', {
            'center': center_obj,
            'orders': orders,
            'status_choices': XeroxOrder.STATUS_CHOICES
        })
    elif user.role == 'admin':
        return redirect('site_admin_dashboard')
    else:
        return redirect('admin:index')

@login_required
def add_menu_item(request):
    if request.user.role != 'canteen_owner':
        return redirect('dashboard')
    
    canteen = request.user.canteens.first()
    if not canteen:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.canteen = canteen
            item.save()
            return redirect('dashboard')
    else:
        form = MenuItemForm()
    
    return render(request, 'services/menu_item_form.html', {'form': form, 'title': 'Add Menu Item'})

@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.user.role != 'canteen_owner' or item.canteen.owner != request.user:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MenuItemForm(instance=item)
    
    return render(request, 'services/menu_item_form.html', {'form': form, 'title': 'Edit Menu Item'})

@login_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.user.role != 'canteen_owner' or item.canteen.owner != request.user:
        return redirect('dashboard')
        
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard')
    
    return render(request, 'services/item_confirm_delete.html', {'item': item})

@login_required
def edit_canteen(request):
    if request.user.role != 'canteen_owner':
        return redirect('dashboard')
    
    canteen = request.user.canteens.first()
    if not canteen:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CanteenForm(request.POST, request.FILES, instance=canteen)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CanteenForm(instance=canteen)
    
    return render(request, 'services/canteen_form.html', {'form': form})

@login_required
def edit_xerox_center(request):
    if request.user.role != 'xerox_owner':
        return redirect('dashboard')
    
    center = request.user.xerox_centers.first()
    if not center:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = XeroxCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = XeroxCenterForm(instance=center)
    
    return render(request, 'services/xerox_center_form.html', {'form': form})

@login_required
def site_admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    
    total_users = User.objects.count()
    total_canteens = Canteen.objects.count()
    total_xerox_centers = XeroxCenter.objects.count()
    total_food_orders = FoodOrder.objects.count()
    total_xerox_orders = XeroxOrder.objects.count()
    
    recent_food_orders = FoodOrder.objects.order_by('-created_at')[:10]
    recent_xerox_orders = XeroxOrder.objects.order_by('-created_at')[:10]
    
    return render(request, 'services/site_admin_dashboard.html', {
        'total_users': total_users,
        'total_canteens': total_canteens,
        'total_xerox_centers': total_xerox_centers,
        'total_food_orders': total_food_orders,
        'total_xerox_orders': total_xerox_orders,
        'recent_food_orders': recent_food_orders,
        'recent_xerox_orders': recent_xerox_orders,
    })

@login_required
def canteen_list(request):
    canteens = Canteen.objects.all()
    return render(request, 'services/canteen_list.html', {'canteens': canteens})

@login_required
def canteen_detail(request, canteen_id):
    canteen = get_object_or_404(Canteen, id=canteen_id)
    menu_items = canteen.menu_items.filter(is_available=True)
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = request.session.get('cart', {})
        # Save as string key (JSON formatting requirement)
        cart[str(item_id)] = cart.get(str(item_id), 0) + quantity
        request.session['cart'] = cart
        
        return redirect('canteen_detail', canteen_id=canteen.id)
        
    return render(request, 'services/canteen_detail.html', {'canteen': canteen, 'menu_items': menu_items})

@login_required
def cart(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id_str, quantity in cart_session.items():
        try:
            item_id = int(item_id_str)
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total_price += item_total
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'item_total': item_total
            })
        except MenuItem.DoesNotExist:
            continue
            
    return render(request, 'services/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    cart_session = request.session.get('cart', {})
    if not cart_session:
        return redirect('canteen_list')
    
    # Calculate total for display on payment page
    total_price = 0
    for item_id_str, quantity in cart_session.items():
        try:
            item = MenuItem.objects.get(id=int(item_id_str))
            total_price += item.price * quantity
        except MenuItem.DoesNotExist:
            continue
            
    if request.method == 'POST':
        # Redirect to payment page instead of creating order directly
        return redirect('payment_gateway')
        
    return redirect('cart')

@login_required
def payment_gateway(request):
    cart_session = request.session.get('cart', {})
    if not cart_session:
        return redirect('canteen_list')
    
    total_price = 0
    cart_items = []
    for item_id_str, quantity in cart_session.items():
        try:
            item = MenuItem.objects.get(id=int(item_id_str))
            item_total = item.price * quantity
            total_price += item_total
            cart_items.append({'item': item, 'quantity': quantity, 'total': item_total})
        except MenuItem.DoesNotExist:
            continue
            
    if request.method == 'POST':
        # Simulate payment processing and create orders
        items_by_canteen = {}
        for item_data in cart_items:
            item = item_data['item']
            qty = item_data['quantity']
            if item.canteen not in items_by_canteen:
                items_by_canteen[item.canteen] = []
            items_by_canteen[item.canteen].append((item, qty))
            
        for canteen, items in items_by_canteen.items():
            order_total = sum((item.price * qty) for item, qty in items)
            order = FoodOrder.objects.create(
                student=request.user,
                canteen=canteen,
                total_price=order_total,
                status='Pending'
            )
            for item, qty in items:
                FoodOrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.price
                )
                
        request.session['cart'] = {}
        return render(request, 'services/payment_success.html')
        
    return render(request, 'services/payment.html', {
        'total_price': total_price,
        'cart_items': cart_items
    })

@login_required
def xerox_list(request):
    centers = XeroxCenter.objects.all()
    return render(request, 'services/xerox_list.html', {'centers': centers})

@login_required
def xerox_detail(request, center_id):
    center = get_object_or_404(XeroxCenter, id=center_id)
    if request.method == 'POST':
        form = XeroxOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.student = request.user
            order.center = center
            order.save()
            return redirect('dashboard')
    else:
        form = XeroxOrderForm()
        
    return render(request, 'services/xerox_detail.html', {'center': center, 'form': form})

@login_required
def track_food_order(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id, student=request.user)
    
    # Define steps for the progress bar
    steps = [
        ('Pending', 'Order Placed'),
        ('Preparing', 'Food is being prepared'),
        ('Out for Delivery', 'On the way'),
        ('Delivered', 'Enjoy your meal!')
    ]
    
    current_step_index = 0
    for i, (status, label) in enumerate(steps):
        if order.status == status:
            current_step_index = i
            break
        if order.status == 'Cancelled':
            current_step_index = -1 # Special case for cancelled
            
    progress_percentage = 0
    if current_step_index >= 0:
        progress_percentage = (current_step_index) * 33.33
            
    return render(request, 'services/track_order.html', {
        'order': order,
        'steps': steps,
        'current_step_index': current_step_index,
        'progress_percentage': progress_percentage
    })

@login_required
def api_order_status(request):
    user = request.user
    data = {}
    if user.role == 'student':
        food_orders = FoodOrder.objects.filter(student=user).exclude(status='Cancelled').order_by('-created_at')[:5]
        xerox_orders = XeroxOrder.objects.filter(student=user).exclude(status='Cancelled').order_by('-created_at')[:5]
        data['food_orders'] = [{'id': o.id, 'status': o.status} for o in food_orders]
        data['xerox_orders'] = [{'id': o.id, 'status': o.status} for o in xerox_orders]
    elif user.role == 'canteen_owner':
        canteen = getattr(user, 'canteens', None)
        canteen_obj = canteen.first() if canteen else None
        if canteen_obj:
            orders = FoodOrder.objects.filter(canteen=canteen_obj).exclude(status='Cancelled').order_by('-created_at')
            data['orders'] = [{'id': o.id, 'status': o.status} for o in orders]
    elif user.role == 'xerox_owner':
        center = getattr(user, 'xerox_centers', None)
        center_obj = center.first() if center else None
        if center_obj:
            orders = XeroxOrder.objects.filter(center=center_obj).exclude(status='Cancelled').order_by('-created_at')
            data['orders'] = [{'id': o.id, 'status': o.status} for o in orders]
    return JsonResponse(data)
