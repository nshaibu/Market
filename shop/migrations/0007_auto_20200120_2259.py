# Generated by Django 3.0.2 on 2020-01-20 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200120_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-date_added']},
        ),
    ]
