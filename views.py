from django.db import connection, transaction
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework import mixins
# Create your views here.
from rest_framework.views import APIView

from log.views import log_create
from .schemas import *


def dictfetchall(cursor):
    desc = cursor.description  # 得到列明
    print('desc', desc)
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()  # ((1,'zs',5),(),())
    ]
class PermissionListView(APIView):
    """
    查看角色权限用户列表
    """
    filter_backends = (DjangoFilterBackend,SearchFilter)
    search_fields = ('user_id', 'log_content')
    module_perms = ['users.permission_view']
    def post(self,request):
        sql = """SELECT new_gp.*,GROUP_CONCAT(users_userprofile_groups.userprofile_id) as user_ids,GROUP_CONCAT(users_userprofile.username) as user_names
FROM(
SELECT auth_group.id,auth_group.`name` as group_name,GROUP_CONCAT(auth_permission.`name`) as permission_names
FROM auth_group LEFT JOIN auth_group_permissions
ON auth_group.id = auth_group_permissions.group_id
LEFT JOIN auth_permission ON auth_permission.id = auth_group_permissions.permission_id
group by auth_group.id) as new_gp 
LEFT JOIN users_userprofile_groups
ON new_gp.id = users_userprofile_groups.group_id
LEFT JOIN users_userprofile ON users_userprofile.id = users_userprofile_groups.userprofile_id
GROUP BY new_gp.id
        """
        cursor = connection.cursor()
        cursor.execute(sql)
        res=dictfetchall(cursor)
        user = self.request.user
        log_create(log_content='查看角色权限用户列表', log_module='权限管理', user=user)
        return Response(data={'res':res})


# 获取所有权限
class PermissionList(APIView):
    """获取所有权限"""
    module_perms = ['users.permission_view']

    def post(self, request):
        sql = """select id,name from auth_permission
            where name not like 'C%' """
        cursor = connection.cursor()
        cursor.execute(sql)
        res = dictfetchall(cursor)
        cursor.close()
        user = self.request.user
        log_create(log_content='获取所有权限', log_module='权限管理', user=user)
        return Response(res)


# 获取所有用户
class UserListView(APIView):
    """
    获取所有用户
    """
    module_perms = ['users.permission_view']

    def post(self, request):
        sql = """select id,username from users_userprofile
            where is_superuser = 0"""
        cursor = connection.cursor()
        cursor.execute(sql)
        res = dictfetchall(cursor)
        cursor.close()
        user = self.request.user
        log_create(log_content='获取所有用户', log_module='权限管理', user=user)
        return Response(res)


# 新增角色
class RoleCreateView(APIView):
    """
    新增角色
    """
    module_perms = ['users.permission_control']
    schema = RoleCreateSchema

    def post(self, request):
        role_name = self.request.data['role']['role_name']
        role_permission = self.request.data['role']['role_permission']
        role_user = self.request.data['role']['role_user']
        role = Group()
        with transaction.atomic():
            try:
                role.name = role_name
                role.save()
            except:
                return Response(data={'code': 400, 'message': '创建失败'})
            role = Group.objects.get(name=role_name)
            if role_permission:
                for permission in role_permission:
                    try:
                        sql = """insert into auth_group_permissions(group_id, permission_id) values({},{})
                        """.format(role.id, permission)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        # role.delete()
                        return Response(data={'code': 400, 'message': '创建失败' + str(e)})
            if role_name:
                for user in role_user:
                    try:
                        sql = """insert into users_userprofile_groups(group_id, userprofile_id) values ({},{})
                        """.format(role.id, user)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        # role.delete()
                        return Response(data={'code': 400, 'message': '创建失败' + str(e)})
        user = self.request.user
        log_create(log_content='新增角色', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '新增成功'})


# 修改权限
class PermissionUpdateView(APIView):
    """
    修改权限
    """
    module_perms = ['users.permission_control']
    schema = PermissionUpdateSchema

    def post(self, request):
        role_id = self.request.data['permission']['group_id']
        permission_id = self.request.data['permission']['permission_id']
        with transaction.atomic():
            sql = """delete from auth_group_permissions where group_id = {}
            """.format(role_id)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.close()
            if permission_id:
                for permission_id in permission_id:
                    try:
                        sql = """insert into auth_group_permissions(group_id, permission_id) values({},{})
                        """.format(role_id, permission_id)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        return Response(data={'code': 400, 'message': '更新失败' + str(e)})
        user = self.request.user
        log_create(log_content='修改权限', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '更新成功'})


# 修改用户
class UserUpdateView(APIView):
    """
    修改用户
    """
    module_perms = ['users.permission_control']
    schema = UserUpdateSchema

    def post(self, request):
        role_id = self.request.data['user']['group_id']
        userprofile_id = self.request.data['user']['userprofile_id']
        with transaction.atomic():
            sql = """delete from users_userprofile_groups where group_id = {}
            """.format(role_id)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.close()
            if userprofile_id:
                for userprofile_id in userprofile_id:
                    try:
                        sql = """insert into users_userprofile_groups(group_id, userprofile_id) values({},{})
                        """.format(role_id, userprofile_id)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        return Response(data={'code': 400, 'message': '更新失败' + str(e)})
        user = self.request.user
        log_create(log_content='修改用户', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '更新成功'})


# 删除角色
class RoleDeleteView(APIView):
    """
    删除角色
    """
    module_perms = ['users.permission_control']
    schema = RoleDeleteSchema

    def post(self, request):
        role_id = self.request.query_params.get('role_id')
        with transaction.atomic():
            try:
                sql = """delete from auth_group_permissions where group_id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
                sql = """delete from users_userprofile_groups where group_id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
                sql = """delete from auth_group where id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
            except Exception as e:
                return Response(data={'code': 400, 'message': '删除失败' + str(e)})
        user = self.request.user
        log_create(log_content='删除角色', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '删除成功'})

