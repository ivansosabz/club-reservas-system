from datetime import datetime, time

from django.db import migrations, models


def backfill_datetimes(apps, schema_editor):
    Reservation = apps.get_model("reservations", "Reservation")
    for r in Reservation.objects.all():
        r.start_datetime = datetime.combine(r.date, r.start_time)
        r.end_datetime = datetime.combine(r.end_date or r.date, r.end_time)
        r.save(update_fields=["start_datetime", "end_datetime"])


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0002_reservation_end_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation",
            options={
                "ordering": ["start_datetime"],
                "verbose_name": "Reserva",
                "verbose_name_plural": "Reservas",
            },
        ),
        migrations.AddField(
            model_name="reservation",
            name="start_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="reservation",
            name="end_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(backfill_datetimes, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="reservation",
            name="date",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="end_time",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="start_time",
        ),
        migrations.AlterField(
            model_name="reservation",
            name="start_datetime",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="end_datetime",
            field=models.DateTimeField(),
        ),
    ]
