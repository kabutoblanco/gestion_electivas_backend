# Generated by Django 2.2.4 on 2019-08-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electives', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]