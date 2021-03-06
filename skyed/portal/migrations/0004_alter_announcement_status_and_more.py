# Generated by Django 4.0.4 on 2022-06-01 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_alter_announcement_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Active for students'), (3, 'Active for instructors'), (-1, 'Hidden')], default=1),
        ),
        migrations.AlterField(
            model_name='deptannouncement',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Active for students'), (3, 'Active for instructors'), (-1, 'Hidden')], default=1),
        ),
        migrations.AlterField(
            model_name='sectionannouncement',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (-1, 'Hidden')], default=1),
        ),
    ]
