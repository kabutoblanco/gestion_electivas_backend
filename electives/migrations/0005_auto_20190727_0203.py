# Generated by Django 2.2.2 on 2019-07-27 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('electives', '0004_auto_20190726_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetail',
            name='from_date_vote',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='coursedetail',
            name='until_date_vote',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]