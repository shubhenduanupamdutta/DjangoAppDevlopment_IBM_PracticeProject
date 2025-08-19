from typing import ClassVar

from django.db import models


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.id)


class Interaction(models.Model):
    CHANNEL_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("phone", "Phone"),
        ("sms", "SMS"),
        ("email", "Email"),
        ("letter", "Letter"),
    ]

    DIRECTION_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("inbound", "Inbound"),
        ("outbound", "Outbound"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    channel = models.CharField(max_length=15, choices=CHANNEL_CHOICES)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    interaction_date = models.DateField(auto_now_add=True)
    summary = models.TextField()

    def __str__(self) -> str:
        return f"Interaction with {self.customer.name} on {self.interaction_date}"
