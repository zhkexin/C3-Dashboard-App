# Generated by Django 4.1.7 on 2023-03-26 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0009_alter_claim_cheque_amt_alter_claim_cheque_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='claim_net_amt',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
