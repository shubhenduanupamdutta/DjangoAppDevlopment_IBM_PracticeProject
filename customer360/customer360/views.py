from datetime import date, timedelta
from typing import TypeAlias

from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Customer, Interaction

Choices: TypeAlias = list[tuple[str, str]]


def index(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "index.html", context=context)


def create_customer(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST["social_media"]
        customer = Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            social_media=social_media,
        )
        customer.save()
        msg = "Successfully Saved a Customer"
        return render(request, "add.html", context={"msg": msg})
    return render(request, "add.html")


def summary(request: HttpRequest) -> HttpResponse:
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)

    count = len(interactions)
    interactions = interactions.values("channel", "direction").annotate(count=Count("channel"))
    context = {
        "interactions": interactions,
        "count": count,
    }

    return render(request, "summary.html", context=context)


def interact(request: HttpRequest, cid: int) -> HttpResponse:
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context: dict[str, str | Choices] = {
        "channels": channels,
        "directions": directions,
    }

    if request.method == "POST":
        customer = Customer.objects.get(id=cid)
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        interaction = Interaction.objects.create(
            customer=customer,
            channel=channel,
            direction=direction,
            summary=summary,
        )
        interaction.save()
        context["msg"] = "Interaction Success"
        return render(request, "interact.html", context=context)

    return render(request, "interact.html", context=context)
