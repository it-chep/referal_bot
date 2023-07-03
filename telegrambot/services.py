from datetime import datetime

import requests
from django.core.exceptions import ObjectDoesNotExist

from .models import Repository


class Service:
    """
    Класс имеет несколько методов по работе с БЛ

    1. Новый участник. Принимает id пользователя, его username, пригласительную ссылку по котороый пришел.
    Происходит проверка есть ли пользователь вступивший вновь в канал в базе участников реф.системы.
    Если пользователь найдет, возвращает значение True, если этот пользователь новый член канала, то создается
     запись в БД и возвращается FALSE

    2.Найти отца. Принимает id пользователя, его username, пригласительную ссылку по котороый пришел и флаг,
    который показывает, какой уровень реф.системы проверяется 0 или 1. Происходит проверка пришласительной ссылки.
    То есть берется ссылка нового пользователя и ищется в бд. Если находится, то тому, кому принадлежит
    эта ссылка добавляется один реферал, если нет такой, то возвращается пустое значение. Также если ссылка найдена,
    отправляется запрос на платформу, чтобы выдать бонус. После этого запускатеся поиск Дедушки, то есть 1 уровень
    реф.системы если считать от 0

    3. Отправить бонус. Прирнимает Id клиента, которому нужно отправить бонус, количество рефералов. Отправляет пост
    запрос на платформу, ничего не возвращает.

    4. Посчитать всех пользователей. Ничего не принимает, возвращает число всех пользователей
    """

    def __init__(self):
        self.repo = Repository()

    def new_member(self, user_id, user_name, invite_link):
        try:
            self.repo.users.objects.get(tg_id=user_id)
            return False  # User already exists
        except ObjectDoesNotExist:
            # User does not exist, so create it
            self.repo.users.objects.create(
                tg_id=user_id,
                username=user_name,
                invite_link=invite_link,
                father_id='243807051'
            )
            return True
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    @staticmethod
    def find_father(user_id, user_name, invite_link, flag):
        ind_chuvaka = False
        try:
            user = Service().repo.referals.objects.filter(invite_link__contains=invite_link).get()
        except ObjectDoesNotExist:
            print(f"No user found with invite link {invite_link}")
            return False

        if user:
            ind_chuvaka = user.pk
            try:
                new_user = Service().repo.users.objects.filter(invite_link__contains=invite_link).get()
                new_user.father_id = user.tg_id
                new_user.save()
            except Exception:
                print(Exception, "EXCEPTION ON IND.CHUVAKA = pk")

        if ind_chuvaka is not False:
            referals = user.count_referals + 1
            user.count_referals = referals
            user.save()
            print(referals, user.count_referals)
            Service().referal_bonus(user.sb_id, referals)

        if flag == 0:
            try:
                if user.pred_invite_link != 'был':
                    Service().find_father(user_id, user_name, user.pred_invite_link[:22], 1)
                else:
                    # Handle the case where pred_invite_link is 'был' and flag is 0
                    print(f"User {user_id} has 'был' pred_invite_link and flag is 0")
            except Exception:
                print('not_link')
            return
        return

    @staticmethod
    def referal_bonus(client_id, count_referal):
        url = 'https://chatter.salebot.pro/api/eefd5e0165aad466aa446254b5016f85/callback'
        params = {
            "message": "referal_bonus",
            "client_id": f"{client_id}",
            "ref_clients": f"{count_referal}"
        }
        response = requests.post(url, json=params)

    def get_all_users(self):
        return self.repo.users.objects.all().count()


