import json
from random import randint

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *


class MainPage(APIView):
    """Класс имеет возможность гет запроса и возвращает список всех участников
    канала, приглашенных по реферальной ссылке"""

    template_name = 'site/main.html'

    def get(self, request):
        return render(request, self.template_name, )


class Referals(APIView):
    """Класс имеет возможность гет запроса и возвращает список всех рефералов"""

    template_name = 'site/referals.html'

    def get(self, request):
        referals = ReferalBase.objects.all()
        return render(request, self.template_name, {'data': referals})


class Users(APIView):
    template_name = 'site/users.html'

    def get(self, request):
        users = UsersBase.objects.all()

        return render(request, self.template_name, {'data': users})


class NewReferal(APIView):
    """Класс имеет возможность пост запроса. Этот запрос приходит с сервиса Salebot и просит создать
    нового пользователя в базе рефералов и вернуть номер его строки в базе"""

    def post(self, request):
        data = request.body.decode()
        parsed_data = json.loads(data)

        name = parsed_data['name']
        tg_id = parsed_data['tg_id']
        sb_id = parsed_data['sb_id']
        count_referals = parsed_data['count_referals']
        invite_link = parsed_data['invite_link']
        username = parsed_data['username']
        pred_invite_link = parsed_data['pred_invite_link']

        try:
            new_user = ReferalBase.objects.create(
                father_name=name,
                father_username=username,
                tg_id=tg_id,
                sb_id=sb_id,
                count_referals=count_referals,
                pred_invite_link=pred_invite_link,
                invite_link=invite_link,
            )
            new_data = {"status": 200, "message": 'all good', 'number_row': new_user.pk}
            return HttpResponse(json.dumps(new_data), content_type='application/json')

        except Exception:
            new_data = {"status": 500, "message": "Что-то пошло не так"}
            return HttpResponse(json.dumps(new_data), content_type='application/json')


class MyStatistic(APIView):
    """Класс имеет возможность пост запроса. Этот запрос приходит с сервиса Salebot и просит
     вернуть ему статистику по его рефералам(сколько он потгласил)"""

    def get(self, request):
        return HttpResponse(status=200)

    def post(self, request):

        data = request.body.decode()
        parsed_data = json.loads(data)
        sb_id = json.loads(parsed_data['sb_id'])

        try:
            ref_clients = ReferalBase.objects.filter(sb_id=sb_id).get().count_referals
        except:
            ref_clients = 0

        new_data = {
            'status': 200,
            'ref_clients': ref_clients,
        }

        return HttpResponse(json.dumps(new_data), content_type='application/json')


class GetData(APIView):
    """Класс имеет возможность пост запроса. Этот запрос приходит с сервиса Salebot и просит
     вернуть ему количество его гостей, которых он пригласил, id последнего прирглашенного гостя,
      username последнего приглашенного гостя"""

    def get(self, request):
        return HttpResponse(status=200)

    def post(self, request):
        data = request.body.decode()
        parsed_data = json.loads(data)
        sb_id = json.loads(parsed_data['sb_id'])

        try:
            ref_clients = ReferalBase.objects.filter(sb_id=sb_id).get()
            data = {
                'status': 200,
                'message': 'Держи',
                'ref_clients': ref_clients.count_referals,
                'last_ref': ref_clients.last_tg_id,
                'last_ref_name': ref_clients.last_username
            }

        except Exception:
            data = {
                'status': 404,
                'message': 'Пользователь не найден',
                'ref_clients': 0,
                'last_ref': None,
                'last_ref_name': None
            }

        return HttpResponse(json.dumps(data), content_type='application/json')


class GetDed(APIView):
    """Класс имеет возможность пост запроса. Этот запрос приходит с сервиса Salebot и просит
     вернуть ему id пользователя от которого пришла пригласительная ссылка"""

    def post(self, request):
        data = request.body.decode()
        parsed_data = json.loads(data)
        tg_id = json.loads(parsed_data['tg_id'])

        try:
            row_ded = UsersBase.objects.filter(tg_id=tg_id).get().father_id
        except Exception:
            row_ded = 0

        data = {
            'status': 200,
            'row_ded': row_ded,
        }

        return HttpResponse(json.dumps(data), content_type='application/json')


class GetDedLink(APIView):
    """Класс имеет возможность пост запроса. Этот запрос приходит с сервиса Salebot и просит
     вернуть ему пригласительную ссылку, по которой в канал пришел юзер"""

    def post(self, request):
        data = request.body.decode()
        parsed_data = json.loads(data)
        father_id = json.loads(parsed_data['row_ded'])

        try:
            father = UsersBase.objects.filter(father_id=father_id).get().invite_link
            data = {
                'status': 200,
                'row_ded': father,
            }
        except:
            data = {
                'status': 404,
                'row_ded': 'null',
            }

        return HttpResponse(json.dumps(data), content_type='application/json')
