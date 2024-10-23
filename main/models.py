from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    class Meta:
        db_table = 'user'

class Stay(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    
    @classmethod
    def create(cls, id, lat, lng):
        stay = cls(user_id=id, lat=lat, lon=lng)
        stay.save()
    
    class Meta:
        db_table = 'stay'
    
class Category(models.Model):
    category = models.CharField(max_length=2, primary_key=True)
    
    class Meta:
        db_table = 'category'

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="명소", unique=False, db_column='category')
    name = models.CharField(max_length=50)
    location = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    
    class Meta:
        db_table = 'place'

class Search(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, db_column='user_id')
    pl_id = models.ForeignKey(Place, on_delete=models.CASCADE, unique=False, db_column='pl_id')
    
    @classmethod
    def create(cls, user_id, pl_id):
        search = cls(user_id=user_id, pl_id=pl_id)
        search.save()
        
    class Meta:
        db_table = 'search'