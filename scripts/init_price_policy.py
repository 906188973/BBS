import base
from web import models


def run():
    obj = models.Power()
    obj.user = models.UserInfo.objects.get(id = 1)
    obj.power = 4
    obj.save()
    print('True')


if __name__ == '__main__':
    run()
