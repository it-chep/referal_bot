# Generated by Django 4.2.1 on 2023-05-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0002_usersbase_father_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referalbase',
            name='count_referals',
            field=models.IntegerField(null=True, verbose_name='Количество рефералов'),
        ),
        migrations.AlterField(
            model_name='referalbase',
            name='father_username',
            field=models.CharField(max_length=255, null=True, verbose_name='User_name БАТИ'),
        ),
        migrations.AlterField(
            model_name='referalbase',
            name='last_tg_id',
            field=models.BigIntegerField(null=True, verbose_name='Tg_id последнего'),
        ),
        migrations.AlterField(
            model_name='referalbase',
            name='last_username',
            field=models.CharField(max_length=255, null=True, verbose_name='User_name последнего'),
        ),
        migrations.AlterField(
            model_name='referalbase',
            name='pred_invite_link',
            field=models.CharField(max_length=200, null=True, verbose_name='Ссылка по которой пришел '),
        ),
        migrations.AlterField(
            model_name='usersbase',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='usersbase',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время'),
        ),
    ]
