# Generated by Django 2.2.2 on 2019-07-18 23:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('electives', '0005_auto_20190717_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliablehour',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570544, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='avaliablehour',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570523, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='classroom_id',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 569659, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 569640, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 567700, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 567682, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='coursedetail',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 568577, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='coursedetail',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 568559, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 571070, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 571047, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='enrrollment',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 569096, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='enrrollment',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 569072, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 566826, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 566803, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='professorvote',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 572100, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='professorvote',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 572076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='program',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 567264, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='program',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 567245, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570166, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570150, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_from',
            field=models.TimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570096, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_to',
            field=models.TimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 570119, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 568161, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 568144, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='studentvote',
            name='date_mod',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 571553, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='studentvote',
            name='date_reg',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 18, 23, 46, 8, 571530, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='classroom',
            unique_together={('id', 'faculty')},
        ),
    ]