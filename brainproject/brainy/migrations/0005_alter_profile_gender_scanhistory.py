# Generated by Django 5.0.6 on 2024-05-23 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brainy', '0004_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'M'), ('Female', 'F')], max_length=20),
        ),
        migrations.CreateModel(
            name='ScanHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mri', models.ImageField(blank=True, null=True, upload_to='scans/')),
                ('date', models.DateField()),
                ('Model1', models.TextField(blank=True)),
                ('Model2', models.TextField(blank=True)),
                ('Model3', models.TextField(blank=True)),
                ('Model4', models.TextField(blank=True)),
                ('Model5', models.TextField(blank=True)),
                ('Result', models.CharField(choices=[('G', 'glioma'), ('M', 'meningioma'), ('N', 'notumor'), ('P', 'pituitary')], max_length=30)),
                ('Profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brainy.profile')),
            ],
        ),
    ]
