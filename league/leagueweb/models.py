from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from PIL import Image

## Customer
class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        return total

    @property
    def Shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()

        for i in orderItems:
            if i.product.digital is False:
                shipping = True
        return shipping

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        totalitem = sum([item.quantity for item in orderitems])
        return totalitem



class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("user"),
        related_name='profile',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile')

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self) -> str:
        return str(self.user.username)

    # def get_absolute_url(self) -> str:
    #     return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 300 or pic.height > 300:
                new_size = (300, 300)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)
