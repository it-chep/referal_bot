from django.db import models


class UsersBase(models.Model):
    """
    Таблица с пользователями, сюда попадают все, кто попал в канал по пригласительной ссылке
    """

    tg_id = models.BigIntegerField('ID Новичка')
    father_id = models.BigIntegerField('ID Бати')
    date = models.DateField('Дата', auto_now_add=True, null=True)
    time = models.DateTimeField('Время', auto_now_add=True, null=True)
    username = models.CharField('username', max_length=255)
    invite_link = models.CharField('По какой ссылке пришел', max_length=200)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'


class ReferalBase(models.Model):
    """
    Таблица с рефералами, сюда попадают все, кто получил реферальную ссылку
    """

    father_name = models.CharField('Имя БАТИ', max_length=255)
    father_username = models.CharField('User_name БАТИ', max_length=255, null=True)
    tg_id = models.BigIntegerField('Tg_id')
    sb_id = models.BigIntegerField('Sb_id')
    last_tg_id = models.BigIntegerField('Tg_id последнего', null=True)
    count_referals = models.IntegerField('Количество рефералов', null=True)
    last_username = models.CharField('User_name последнего', max_length=255, null=True)
    invite_link = models.CharField('Пригласительная ссылка', max_length=200)
    pred_invite_link = models.CharField('Ссылка по которой пришел ', max_length=200, null=True)

    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Рефералы'


class Repository:
    users = UsersBase
    referals = ReferalBase
