# Generated by Django 2.2.2 on 2019-07-26 19:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('electives', '0003_auto_20190725_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursedetail',
            old_name='proffesor',
            new_name='professor',
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='from_date_vote',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='until_date_vote',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name='enrrollment',
            unique_together={('student', 'course')},
        ),
    ]