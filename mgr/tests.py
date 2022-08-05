from django.test import TestCase

# Create your tests here.
import  requests,pprint


def customerTest(sessionid):
    '''
    管理员app里面顾客模块测试
    '''
    #测试管理员模块里面查询顾客信息的是否正常
    response = requests.get('http://localhost/api/mgr/customers?action=list_customer', \
                            cookies={'sessionid': sessionid})#客户端提供给服务端一样的sessionid表面自己刚刚已经登陆过
    pprint.pprint(response.json())

    info = {'action': 'add_customer',
            'data':
                {
                    'name':'wyy',
                    'phonenumber':'1215323',
                    'address':'sdsda'
                }}
    # response = requests.post('http://localhost/api/mgr/customers',
    #                          json=info,
    #                          cookies={'sessionid': sessionid})
    # pprint.pprint(response.json())
def medicineTest(sessionid):
    '''
    管理员app里面药品模块测试
    '''
    #测试查询、增加和删除药品是否正常
    info = {
            'data': {
            'name': '999感冒灵颗粒',
            'sn': '102225',
            'desc': '专门治疗感冒发烧'
            },
            'action': 'add_medicine',
            }

    # response = requests.post('http://localhost/api/mgr/medicines', \
    #                         cookies={'sessionid': sessionid},\
    #               json= info)#客户端提供给服务端一样的sessionid表面自己刚刚已经登陆过
    # pprint.pprint(response.json())
    response = requests.get('http://localhost/api/mgr/medicines?action=list_medicine', \
                            cookies={'sessionid': sessionid})#客户端提供给服务端一样的sessionid表面自己刚刚已经登陆过
    pprint.pprint(response.json())
def orderTest(sessionid):

    '''
    管理员app里面订单模块的测试
    '''
    # order_info = {
    #     'data': {
    #         'name':'第一个订单',
    #         'customerid': 1,
    #         'medicineids': [2, 3],
    #             },
    #     'action': 'add_order',
    # }
    # response = requests.post('http://localhost/api/mgr/orders', \
    #                          cookies={'sessionid': sessionid},\
    #                          json = order_info)
    # pprint.pprint(response.json())

    response = requests.get('http://localhost/api/mgr/orders?action=list_order', \
                             cookies = {'sessionid': sessionid})
    pprint.pprint(response.json())
def testAll():
    # 测试管理员模块里面的登陆是否正常
    person_Info = {'username': 'piao', 'password': '123456'}
    response = requests.post('http://localhost/api/mgr/signin', data=person_Info)
    pprint.pprint(response.json())

    # 获取用户的session，即跟踪刚刚登陆完成的管理员，不需要再次登陆
    sessionid = response.cookies['sessionid']  # 服务器端给客户端用户提供的session号
    print(sessionid)
    orderTest(sessionid)