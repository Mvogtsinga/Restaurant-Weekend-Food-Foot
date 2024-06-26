# Generated by Django 5.0.3 on 2024-03-24 03:54

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TableType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('COUPLE', 'Couple'), ('FAMILIAL', 'Familial'), ('INDIVIDUAL', 'Individuel'), ('VIP', 'VIP'), ('EXTRA_FAMILLE', 'Extra Famille')], max_length=50, unique=True)),
                ('seats', models.IntegerField(default=2)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image_path', models.CharField(default='path/to/default/image.jpg', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('table_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weekendfoodfoot.tabletype')),
            ],
            options={
                'unique_together': {('user', 'table_type', 'date')},
            },
        ),
    ]
