# Generated by Django 4.0 on 2022-07-21 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0012_alter_product_quality'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10)),
                ('fullname', models.CharField(max_length=50)),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='water.user_details')),
                ('water', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='water.product')),
            ],
        ),
    ]