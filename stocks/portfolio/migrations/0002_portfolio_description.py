# Generated by Django 3.1.4 on 2021-04-11 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='description',
            field=models.TextField(default='123'),
            preserve_default=False,
        ),
    ]
