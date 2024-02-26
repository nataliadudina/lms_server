# Generated by Django 4.2.7 on 2024-02-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_payment_session_id_payment_status_alter_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Payment link'),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
