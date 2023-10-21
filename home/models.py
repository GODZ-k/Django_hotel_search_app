from django.contrib.auth.models import User
from django.db import models
import uuid

# from curses.ascii import US

# Create your models here.
class basemodel(models.Model):   # predefine features of the model it is not img before devlopment , we can add this in every model but this is suitable method to implement it before .
    uid=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Amenities(basemodel):   # amenities means features of the rooms or hotel ex . wifi , swiming pool , AC and more
    amenity_name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name


class hotel(basemodel):
    hotel_name=models.CharField(max_length=100)
    hotel_price=models.IntegerField()
    description=models.TextField()
    hotel_place=models.CharField(max_length=100,default="Unknown")
    amenities=models.ManyToManyField(Amenities)
    hotel_count=models.IntegerField(default=10)


    def __str__(self) -> str:
        return self.hotel_name


class hotel_images(basemodel):
    hotel=models.ForeignKey(hotel, related_name="images", on_delete=models.CASCADE)
    images=models.ImageField(upload_to="hotels")


class booking(basemodel):
    hotel=models.ForeignKey(hotel, related_name="hotel_bookings", on_delete=models.CASCADE)
    start_date=models.DateField()
    user=models.ForeignKey(User, related_name="user_booking", on_delete=models.CASCADE)
    end_date=models.DateField()
    booking_type=models.CharField(choices=(('prepaid','prepaid'),('postpaid','postpaid')) ,max_length=100)
