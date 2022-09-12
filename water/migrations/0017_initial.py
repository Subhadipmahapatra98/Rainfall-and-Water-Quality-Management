# Generated by Django 4.0 on 2022-07-24 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('water', '0016_remove_neworder_user_remove_neworder_water_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.CharField(max_length=20)),
                ('available', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('cost', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Querry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=12)),
                ('messages', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='User_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='NewOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10)),
                ('fullname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('pnum', models.CharField(max_length=12)),
                ('pin', models.CharField(max_length=6)),
                ('state', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=25)),
                ('houseno', models.CharField(max_length=20)),
                ('landmark', models.CharField(max_length=50)),
                ('dated', models.DateTimeField(auto_now_add=True)),
                ('expected_date', models.CharField(max_length=50)),
                ('totalcost', models.CharField(max_length=50)),
                ('confirmation', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='water.user_details')),
                ('water', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='water.product')),
            ],
        ),
    ]
