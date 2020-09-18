# Generated by Django 3.1 on 2020-09-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='testtable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=70)),
                ('description', models.CharField(default='', max_length=200)),
                ('published', models.BooleanField(default=False)),
                ('SKU', models.IntegerField(default='0')),
                ('EAN', models.IntegerField(default='0')),
                ('Name', models.JSONField(default=dict)),
                ('Stock_quantity', models.IntegerField(default='0')),
                ('price', models.IntegerField(default='-1')),
                ('active', models.BooleanField(default='false')),
            ],
        ),
    ]