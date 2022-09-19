from django.db.models.signals import post_save, m2m_changed
from django.db import models
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    session_id = models.CharField(max_length=32)
    items = models.ManyToManyField('Item')
    total = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, editable=False)


@receiver(m2m_changed, sender=Order.items.through)
def update_order(sender, instance, **kwargs):
    total = 0.0
    for item in instance.items.all():
        total += float(item.price)
    instance.total = total
    instance.save(update_fields=['total'])
