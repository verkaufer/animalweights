# Generated by Django 2.0.6 on 2018-06-23 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_weight', models.FloatField()),
                ('recorded_at', models.DateTimeField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weights', to='animals.Animal')),
            ],
        ),
    ]
