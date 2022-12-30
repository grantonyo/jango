from datetime import datetime
from django.db import models  # импорт


class Order(models.Model):  # наследуемся от класса Model
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product", through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now() - self.time_in).total_seconds() // 60


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")

class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]

class ProductOrder(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1)

    def product_sum(self):
        product_price = self.product.price
        return product_price * self._amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


# class AbstractBaseUser(models.Model):
#     password = models.CharField(_('password'), max_length=128)
#     last_login = models.DateTimeField(_('last login'), blank=True, null=True)
#
#     is_active = True
#
# class AbstractUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.
#
#     Username and password are required. Other fields are optional.
#     """
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     first_name = models.CharField(_('first name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     email = models.EmailField(_('email address'), blank=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)