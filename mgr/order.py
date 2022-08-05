import json

from django.http import JsonResponse
from django.db import IntegrityError, transaction
from common.models import Order, OrderMedicine
from django.db.models import  F

def listorder(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录,这里是order表，该表里面关联了用户
    # 其中用户是通过order项里面的customer关联的，如果要得到关联的用户信息，直接用
    #customer + 双下划线 + 用户的属性 即可
    #
    qs = Order.objects \
        .annotate(
        customer_name=F('customer__name'),
        medicines_name=F('medicines__name')
    ) \
        .values(
        'id', 'name', 'create_date',
        'customer_name',
        'medicines_name'
    )
    retlist = list(qs)
    # 可能有 ID相同，药品不同的订单记录， 需要合并，即同一个订单里面会存在多个药品，
    #上面对order表（含有外键即多对一和多对多的一个外联表）获取，会得到订单的所有信息，即每一个订单
    #里面订单id对应的用户id对应的药品id，多对一 + 多对多
    newlist = []
    id2order = {}
    for one in retlist:
        orderid = one['id']
        if orderid not in id2order:
            newlist.append(one)
            id2order[orderid] = one
        else:
            id2order[orderid]['medicines_name'] += ' | ' + one['medicines_name']

    return JsonResponse({'ret': 0, 'retlist': newlist})


def addorder(request):
    info = request.params['data']
    #print(info)
    #创建事务的上下文，如果其中一个操作失败，所有的操作都会回滚
    with transaction.atomic():
        #创建一个新的订单，订单里面包含用户的信息，用户和订单是一对多，所以只需要一个订单关联一个用户即可，通过
        #外键关联即可
        new_order= Order.objects.create(name=info['name'] ,
                                    customer_id = info['customerid'])
        #将订单里面的订单号和药物号一一提取出来,多对多，通过另一个表来去表达多对多的关系
        batch = [OrderMedicine(order_id=new_order.id, medicine_id=mid, amount=1)
                 for mid in info['medicineids']]

        #  在多对多关系表中 添加了 多条关联记录
        #  使用 bulk_create， 参数是一个包含所有 该表的 Model 对象的 列表，更新多对多的关系
        OrderMedicine.objects.bulk_create(batch)

    return JsonResponse({'ret': 0, 'id': new_order.id})


# def modifyorder(request):
#     # 从请求消息中 获取修改药品的信息
#     # 找到该药品，并且进行修改操作
#
#     orderid = request.params['id']
#     newdata = request.params['newdata']
#
#     try:
#         # 根据 id 从数据库中找到相应的客户记录
#         order = Order.objects.get(id=orderid)
#     except order.DoesNotExist:
#         return {
#             'ret': 1,
#             'msg': f'id 为`{order}`的客户不存在'
#         }
#
#     if 'name' in newdata:
#         order.name = newdata['name']
#     if 'sn' in newdata:
#         order.phonenumber = newdata['sn']
#     if 'desc' in newdata:
#         order.address = newdata['desc']
#
#     # 注意，一定要执行save才能将修改信息保存到数据库
#     order.save()
#
#     return JsonResponse({'ret': 0})


def deleteorder(request):

    orderid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        order = Order.objects.get(id=orderid)
    except order.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{order}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    order.delete()

    return JsonResponse({'ret': 0})


def dispatcher(request):

    # 根据session判断用户是否是登录的管理员用户
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'},
            status=302)

    if request.session['usertype'] != 'mgr' :
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'} ,
            status=302)
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_order':
        return listorder(request)
    elif action == 'add_order':
        return addorder(request)
    elif action == 'del_order':
        return deleteorder(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})