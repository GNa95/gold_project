<<<<<<< Updated upstream
# Generated by Django 3.1.3 on 2022-11-26 12:20
=======
# Generated by Django 3.1.3 on 2022-11-25 05:44
>>>>>>> Stashed changes

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='secinquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquirys_name', models.CharField(max_length=20)),
                ('inquirys_email', models.CharField(max_length=30)),
                ('inquirys_text', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100, unique=True)),
                ('user_id', models.CharField(max_length=50)),
                ('user_phone', models.CharField(max_length=40, verbose_name='유저 전화번호')),
                ('user_addr', models.CharField(max_length=40, verbose_name='유저 주소')),
                ('user_level', models.CharField(max_length=8, verbose_name='등급')),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저',
                'db_table': 'TB_USER',
            },
        ),
    ]
