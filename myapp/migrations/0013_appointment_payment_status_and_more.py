# Generated by Django 4.0.5 on 2022-07-28 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_appointment_precription'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='payment_status',
            field=models.CharField(default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='precription',
            field=models.TextField(default=''),
        ),
    ]