'''
test iam2 image operations by platform admin/operator/member

# 1 create project
# 2 create virtual id (project admin/operator/member)
# 3 Add image with virtual id
# 4 delete

@author: quarkonics
'''
import os
import time
import zstackwoodpecker.test_util as test_util
import apibinding.inventory as inventory
import zstackwoodpecker.operations.account_operations as acc_ops
import zstackwoodpecker.operations.iam2_operations as iam2_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import zstackwoodpecker.operations.image_operations as img_ops
import zstackwoodpecker.operations.volume_operations as vol_ops
import zstackwoodpecker.operations.account_operations as acc_ops
from zstackwoodpecker.operations import vm_operations as vm_ops
import zstackwoodpecker.operations.net_operations as net_ops
import zstackwoodpecker.operations.vxlan_operations as vxlan_ops
import zstackwoodpecker.operations.scheduler_operations as schd_ops
import zstackwoodpecker.operations.zwatch_operations as zwt_ops
import zstackwoodpecker.test_lib as test_lib

project_uuid = None
virtual_id_uuid = None
project_admin_uuid = None
project_operator_uuid = None
plain_user_uuid = None
test_stub = test_lib.lib_get_test_stub()

case_flavor = dict(project_admin=                   dict(target_role='project_admin'),
                   project_operator=                dict(target_role='project_operator'),
                   project_member=                  dict(target_role='project_member'),
                   )

def test():
    global project_uuid, project_admin_uuid, virtual_id_uuid, project_operator_uuid, plain_user_uuid

    flavor = case_flavor[os.environ.get('CASE_FLAVOR')]
    # 1 create project
    project_name = 'test_project'
    project = iam2_ops.create_iam2_project(project_name)
    project_uuid = project.uuid
    project_linked_account_uuid = project.linkedAccountUuid

    if flavor['target_role'] == 'project_admin':
        # 2 create virtual id
        project_admin_name = 'username'
        project_admin_password = 'password'
        project_admin_uuid = iam2_ops.create_iam2_virtual_id(project_admin_name, project_admin_password).uuid
        virtual_id_uuid = iam2_ops.create_iam2_virtual_id('usernametwo', 'password').uuid
    
        # 3 create project admin
        iam2_ops.add_iam2_virtual_ids_to_project([project_admin_uuid],project_uuid)
        attributes = [{"name": "__ProjectAdmin__", "value": project_uuid}]
        iam2_ops.add_attributes_to_iam2_virtual_id(project_admin_uuid, attributes)

        # login in project by project admin
        project_admin_session_uuid = iam2_ops.login_iam2_virtual_id(project_admin_name, project_admin_password)
        project_login_uuid = iam2_ops.login_iam2_project(project_name, session_uuid=project_admin_session_uuid).uuid
        # iam2_ops.remove_attributes_from_iam2_virtual_id(virtual_id_uuid, attributes)
    elif flavor['target_role'] == 'project_operator':
        project_operator_name = 'username2'
        project_operator_password = 'password'
        attributes = [{"name": "__ProjectOperator__", "value": project_uuid}]
        project_operator_uuid = iam2_ops.create_iam2_virtual_id(project_operator_name,project_operator_password,attributes=attributes).uuid
        virtual_id_uuid = iam2_ops.create_iam2_virtual_id('usernamethree','password').uuid

        # login in project by project operator
        iam2_ops.add_iam2_virtual_ids_to_project([project_operator_uuid],project_uuid)
        project_operator_session_uuid = iam2_ops.login_iam2_virtual_id(project_operator_name,project_operator_password)
        project_login_uuid = iam2_ops.login_iam2_project(project_name,session_uuid=project_operator_session_uuid).uuid
    elif flavor['target_role'] == 'project_member':
	plain_user_name = 'username'
	plain_user_password = 'password'
	plain_user_uuid = iam2_ops.create_iam2_virtual_id(plain_user_name, plain_user_password,
	                                                  project_uuid=project_uuid).uuid
	# 3 add virtual id to project
	iam2_ops.add_iam2_virtual_ids_to_project([plain_user_uuid],project_uuid)

	# 4 login in project by plain user
	plain_user_session_uuid = iam2_ops.login_iam2_virtual_id(plain_user_name, plain_user_password)

	# 4 login in project
	#project_inv=iam2_ops.get_iam2_projects_of_virtual_id(plain_user_session_uuid)
	project_login_uuid = iam2_ops.login_iam2_project(project_name, plain_user_session_uuid).uuid

    zone_uuid = res_ops.get_resource(res_ops.ZONE)[0].uuid

    try:
        l2 = net_ops.create_l2_novlan('l2_for_pm', 'eth0', zone_uuid, session_uuid=project_login_uuid)
        test_util.test_fail("Expect exception: project admin not allowed to create Novlan L2 except vxlan")
    except:
        pass

    try:
        l2 = net_ops.create_l2_vlan('l2_for_pm', 'eth0', zone_uuid, 1234, session_uuid=project_login_uuid)
        test_util.test_fail("Expect exception: project admin not allowed to create vlan L2 except vxlan")
    except:
        pass
    if flavor['target_role'] == 'project_member':
        statements = [{"effect": "Allow", "actions": ["org.zstack.network.l2.**"]}, {"effect": "Allow", "actions": ["org.zstack.header.network.l3.**"]}]
        role_uuid = iam2_ops.create_role('test_role', statements).uuid
        iam2_ops.add_roles_to_iam2_virtual_id([role_uuid], plain_user_uuid)

    vxlan_pool = res_ops.get_resource(res_ops.L2_VXLAN_NETWORK_POOL)
    if vxlan_pool == None or len(vxlan_pool) == 0:
        test_util.test_skip('Vxlan is required for testing')
    vxlan_pool_uuid = vxlan_pool[0].uuid
    acc_ops.share_resources([project_linked_account_uuid], [vxlan_pool_uuid])
    vxlan_pool_uuid = res_ops.get_resource(res_ops.L2_VXLAN_NETWORK_POOL, session_uuid=project_login_uuid)[0].uuid
    vxlan_l2_uuid = vxlan_ops.create_l2_vxlan_network('vxlan_for_pm', vxlan_pool_uuid, zone_uuid, session_uuid=project_login_uuid).uuid
    l3_uuid = net_ops.create_l3('l3_for_pm', vxlan_l2_uuid, session_uuid=project_login_uuid).uuid
    net_ops.delete_l3(l3_uuid, session_uuid=project_login_uuid)
    net_ops.delete_l2(vxlan_l2_uuid, session_uuid=project_login_uuid)

    # 11 delete
    acc_ops.logout(project_login_uuid)
    if virtual_id_uuid != None:
        iam2_ops.delete_iam2_virtual_id(virtual_id_uuid)
    if project_admin_uuid != None:
        iam2_ops.delete_iam2_virtual_id(project_admin_uuid)
    if project_operator_uuid != None:
        iam2_ops.delete_iam2_virtual_id(project_operator_uuid)
    if plain_user_uuid != None:
        iam2_ops.delete_iam2_virtual_id(plain_user_uuid)

    iam2_ops.delete_iam2_project(project_uuid)
    iam2_ops.expunge_iam2_project(project_uuid)

    test_util.test_pass('success test iam2 login in by project admin!')


def error_cleanup():
    global project_uuid, project_admin_uuid, virtual_id_uuid
    if virtual_id_uuid:
        iam2_ops.delete_iam2_virtual_id(virtual_id_uuid)
    if project_admin_uuid:
        iam2_ops.delete_iam2_virtual_id(project_admin_uuid)
    if project_uuid:
        iam2_ops.delete_iam2_project(project_uuid)
        iam2_ops.expunge_iam2_project(project_uuid)
    if plain_user_uuid != None:
        iam2_ops.delete_iam2_virtual_id(plain_user_uuid)

