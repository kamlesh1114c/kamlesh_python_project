# Generated by Django 4.0.5 on 2022-07-19 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_appointment_precription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='precription',
            field=models.TextField(default='Not Given Yet'),
        ),
    ]
