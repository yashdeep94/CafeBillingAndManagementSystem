from django.db import models

class Category(models.Model):
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.category
class Maincategory(models.Model):
    category=models.CharField(max_length=100,primary_key=True)
    
    def __str__(self):
        return self.category

class PaymentType(models.Model):
    payment_mode=models.CharField(max_length=50)

    def __str__(self):
        return self.payment_mode

class Size(models.Model):
    item_size=models.CharField(max_length=50)

    def __str__(self):
        return self.item_size

class Item(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    category=models.ForeignKey('Category', on_delete=models.CASCADE)
    size=models.ForeignKey('Size',on_delete=models.CASCADE)
    main_category=models.ForeignKey('Maincategory', on_delete=models.CASCADE, default='Veg - Pizzas')

    def __str__(self):
        return f"{self.name}, {self.price}, {self.category}, {self.size}"

class Order(models.Model):
    name=models.CharField(max_length=100)
    quantity_items=models.CharField(max_length=5000)
    total=models.IntegerField()
    payment_type=models.ForeignKey('PaymentType', on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    name=models.CharField(max_length=2000)
    price=models.IntegerField()
    date=models.DateField()
    
    def __str__(self):
        return self.name