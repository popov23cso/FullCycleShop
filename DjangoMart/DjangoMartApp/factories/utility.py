import random
import calendar
from datetime import datetime, timezone

# define some generic trends for dates of generated records
# to have a more realistic record generation
# general idea is to have a bias towards weekends,
# holiday seasons and later years of project lifecycle
def get_weighted_date():

    year_weights_dict = {
        2023: 0.5, 2024: 0.8, 2025: 1.1
    }

    month_weights_dict = {
        1: 0.8,  2: 0.7,  3: 1.0,  4: 1.2,
        5: 1.5,  6: 1.8,  7: 1.6,  8: 1.2,
        9: 1.0, 10: 1.3, 11: 2.0, 12: 2.5
    }

    day_weights_dict = {
        1: 0.7,  2: 0.7,  3: 0.8,  4: 0.9,
        5: 1.2,  6: 1.2,  7: 1.1
    }

    year = pick_value_by_weight(year_weights_dict)
    month = pick_value_by_weight(month_weights_dict)
    day = pick_value_by_weight(day_weights_dict)

    day_of_picked_month = get_random_day_of_month(year, month, day)

    hour = random.randint(0, 23)

    return datetime(year, month, day_of_picked_month, hour, tzinfo=timezone.utc)


def get_random_day_of_month(year, month, day_num):

    number_of_days = calendar.monthrange(year, month)[1]

    matching_days = []

    for day in range(1, number_of_days + 1):
        if datetime(year, month, day).isoweekday() == day_num:
            matching_days.append(day)

    return random.choice(matching_days)

def pick_value_by_weight(weights_dict):
    items = list(weights_dict.keys())
    item_weights = list(weights_dict.values())

    value = random.choices(items, weights=item_weights, k=1)[0]

    return value

    





