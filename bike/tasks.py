from celery import shared_task

@shared_task
def calculate_rental_cost(rental_minute, price):
    rental_cost = rental_minute * price
    return rental_cost