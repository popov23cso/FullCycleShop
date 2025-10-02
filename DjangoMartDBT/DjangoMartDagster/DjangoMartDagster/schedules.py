"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster_dbt import build_schedule_from_dbt_selection
from dagster import ScheduleDefinition

from .assets import DjangoMartDBT_dbt_assets
from .jobs import djnagomart_daily_job

schedules = [
#     build_schedule_from_dbt_selection(
#         [DjangoMartDBT_dbt_assets],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     ),
]

daily_djangomart_schedule = ScheduleDefinition(
    job=djnagomart_daily_job,
    cron_schedule="0 6 * * *",  # every day at 6am
)