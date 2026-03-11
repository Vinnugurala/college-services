from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('canteen_owner', 'Canteen Owner'),
        ('xerox_owner', 'Xerox Shop Owner'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    hostel_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.hostel_name} {self.room_number}"

class Canteen(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canteens')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='canteen_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.canteen.name}"

class FoodOrder(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_orders')
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.student.username}"

class FoodOrderItem(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Store price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order {self.order.id}"

class XeroxCenter(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xerox_centers')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class XeroxOrder(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Printing', 'Printing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    COLOR_CHOICES = (('BW', 'Black & White'), ('Color', 'Color'))
    PRINT_CHOICES = (('Single', 'Single Sided'), ('Double', 'Double Sided'))

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xerox_orders')
    center = models.ForeignKey(XeroxCenter, on_delete=models.CASCADE, related_name='orders')
    document = models.FileField(upload_to='xerox_documents/')
    copies = models.PositiveIntegerField(default=1)
    color_type = models.CharField(max_length=10, choices=COLOR_CHOICES, default='BW')
    print_type = models.CharField(max_length=10, choices=PRINT_CHOICES, default='Single')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Xerox Order {self.id} - {self.student.username}"
