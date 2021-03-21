# Generated by Django 3.1.7 on 2021-03-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210319_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionitem',
            name='title',
            field=models.CharField(default='Action Item 2021-03-19 15:55:14', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='title',
            field=models.CharField(default='Attachment 2021-03-19 15:55:14', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='title',
            field=models.CharField(default='Meeting 2021-03-19 15:55:14', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(default='Note 2021-03-19 15:55:14', max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='person',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_self',
            field=models.BooleanField(default=False, verbose_name='This is Me'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(default='Project 2021-03-19 15:55:14', max_length=100, verbose_name='Title'),
        ),
    ]
