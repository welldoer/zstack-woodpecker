'''

All IAM2 operations for test.

@author: ronghaoZhou
'''
import apibinding.api_actions as api_actions
import zstackwoodpecker.test_util as test_util
import account_operations


def add_attributes_to_iam2_project(uuid, attributes, session_uuid=None):
    action = api_actions.AddAttributesToIAM2ProjectAction()
    action.timeout = 30000
    action.uuid = uuid
    action.attributes = attributes
    test_util.action_logger('Add attributes: %s to iam2 project :%s' % (attributes, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_attributes_to_iam2_virtual_id_group(uuid, attributes, session_uuid=None):
    action = api_actions.AddAttributesToIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.uuid = uuid
    action.attributes = attributes
    test_util.action_logger('Add attributes: %s to iam2 virtual ID group :%s' % (attributes, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_attributes_to_iam2_virtual_id(uuid, attributes, session_uuid=None):
    action = api_actions.AddAttributesToIAM2VirtualIDAction()
    action.timeout = 30000
    action.uuid = uuid
    action.attributes = attributes
    test_util.action_logger('Add attributes: %s to iam2 virtual ID :%s' % (attributes, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_attributes_to_organization(uuid, attributes, session_uuid=None):
    action = api_actions.AddAttributesToOrganizationAction()
    action.timeout = 30000
    action.uuid = uuid
    action.attributes = attributes
    test_util.action_logger('Add attributes: %s to Organization :%s' % (attributes, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_iam2_virtual_ids_to_group(virtual_id_uuids, group_uuid, session_uuid=None):
    action = api_actions.AddIAM2VirtualIDsToGroupAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.groupUuid = group_uuid
    test_util.action_logger('Add iam2 virtual ids: %s to group :%s' % (virtual_id_uuids, group_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_iam2_virtual_ids_to_organization(virtual_id_uuids, organization_uuid, session_uuid=None):
    action = api_actions.AddIAM2VirtualIDsToOrganizationAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.organizationUuid = organization_uuid
    test_util.action_logger('Add iam2 virtual ids: %s to organization:%s' % (virtual_id_uuids, organization_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_iam2_virtual_ids_to_project(virtual_id_uuids, project_uuid, session_uuid=None):
    action = api_actions.AddIAM2VirtualIDsToProjectAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.projectUuid = project_uuid
    test_util.action_logger('Add iam2 virtual ids: %s to project:%s' % (virtual_id_uuids, project_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_roles_to_iam2_virtual_id_group(role_uuids, group_uuid, session_uuid=None):
    action = api_actions.AddRolesToIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.roleUuids = role_uuids
    action.groupUuid = group_uuid
    test_util.action_logger('Add roles : %s to iam2 virtual id group:%s' % (role_uuids, group_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def add_roles_to_iam2_virtual_id(role_uuids, virtual_id_uuid, session_uuid=None):
    action = api_actions.AddRolesToIAM2VirtualIDAction()
    action.timeout = 30000
    action.roleUuids = role_uuids
    action.virtualIDUuid = virtual_id_uuid
    test_util.action_logger('Add roles : %s to iam2 virtual id:%s' % (role_uuids, virtual_id_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def change_iam2_organization_parent(parent_uuid, children_uuids, session_uuid=None):
    action = api_actions.ChangeIAM2OrganizationParentAction()
    action.timeout = 30000
    action.childrenUuids = children_uuids
    action.parentUuid = parent_uuid
    test_util.action_logger('Change iam2 organization children : %s  parent:%s' % (children_uuids, parent_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def change_iam2_organization_state(uuid, state_event, session_uuid=None):
    action = api_actions.ChangeIAM2OrganizationStateAction()
    action.timeout = 30000
    action.uuid = uuid
    action.stateEvent = state_event
    test_util.action_logger('change iam2 organization : %s to state :%s' % (uuid, state_event))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def change_iam2_project_state(uuid, state_event, session_uuid=None):
    action = api_actions.ChangeIAM2ProjectStateAction()
    action.timeout = 30000
    action.uuid = uuid
    action.stateEvent = state_event
    test_util.action_logger('change iam2 project : %s to state :%s' % (uuid, state_event))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def change_iam2_virtual_id_group_state(uuid, state_event, session_uuid=None):
    action = api_actions.ChangeIAM2VirtualIDGroupStateAction()
    action.timeout = 30000
    action.uuid = uuid
    action.stateEvent = state_event
    test_util.action_logger('change iam2 virtual id group : %s to state :%s' % (uuid, state_event))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def change_iam2_virtual_id_state(uuid, state_event, session_uuid=None):
    action = api_actions.ChangeIAM2VirtualIDStateAction()
    action.timeout = 30000
    action.uuid = uuid
    action.stateEvent = state_event
    test_util.action_logger('change iam2 virtual id : %s to state :%s' % (uuid, state_event))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def create_iam2_organization(name, type, description=None, parent_uuid=None, attributes=None, session_uuid=None):
    action = api_actions.CreateIAM2OrganizationAction()
    action.timeout = 30000
    action.name = name
    action.type = type
    if description:
        action.description = description
    if parent_uuid:
        action.parentUuid = parent_uuid
    if attributes:
        action.attributes = attributes
    test_util.action_logger('create iam2 organization : %s ' % name)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def create_iam2_project(name, description=None, attributes=None, session_uuid=None):
    action = api_actions.CreateIAM2ProjectAction()
    action.timeout = 30000
    action.name = name
    if description:
        action.description = description
    if attributes:
        action.attributes = attributes
    test_util.action_logger('create iam2 project : %s ' % name)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def create_iam2_virtual_id_group(project_uuid, name, description=None, attributes=None, session_uuid=None):
    action = api_actions.CreateIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.name = name
    action.projectUuid = project_uuid
    if description:
        action.description = description
    if attributes:
        action.attributes = attributes
    test_util.action_logger('create iam2 virtual id group : %s  in project : %s' % (name, project_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def create_iam2_virtual_id(name, password, description=None, attributes=None, project_uuid=None, organization_uuid=None,
                           session_uuid=None):
    action = api_actions.CreateIAM2VirtualIDAction()
    action.timeout = 30000
    action.name = name
    action.password = password
    if description:
        action.description = description
    if project_uuid:
        action.parentUuid = project_uuid
    if attributes:
        action.attributes = attributes
    if organization_uuid:
        action.organizationUuid = organization_uuid
    test_util.action_logger('create iam2 virtual id : %s ' % name)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def delete_iam2_organization(uuid, session_uuid=None):
    action = api_actions.DeleteIAM2OrganizationAction()
    action.timeout = 30000
    action.uuid = uuid
    test_util.action_logger('delete IAM2 organization : %s ' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def delete_iam2_project(uuid, session_uuid=None):
    action = api_actions.DeleteIAM2ProjectAction()
    action.timeout = 30000
    action.uuid = uuid
    test_util.action_logger('delete IAM2 project : %s ' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def delete_iam2_virtual_id_group(uuid, session_uuid=None):
    action = api_actions.DeleteIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.uuid = uuid
    test_util.action_logger('delete IAM2 virtual id group : %s ' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def delete_iam2_virtual_id(uuid, session_uuid=None):
    action = api_actions.DeleteIAM2VirtualIDAction()
    action.timeout = 30000
    action.uuid = uuid
    test_util.action_logger('delete IAM2 virtual id  : %s ' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def get_iam2_system_attributes(session_uuid=None):
    action = api_actions.GetIAM2SystemAttributesAction()
    action.timeout = 30000
    test_util.action_logger('get iam2 system attributes')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventories


def get_iam2_virtual_id_api_permission(apis_to_check=None, session_uuid=None):
    action = api_actions.GetIAM2VirtualIDAPIPermissionAction()
    action.timeout = 30000
    if apis_to_check:
        action.apisToCheck = apis_to_check
    test_util.action_logger('get iam2 virtual id api permission')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.permissions


def login_iam2_virtual_id(name, password, timeout=160000):
    login = api_actions.LoginIAM2VirtualIDAction()
    login.name = name
    login.password = password
    login.timeout = timeout
    test_util.action_logger('login by iam2 virtual id :%s' % name)
    session_uuid = login.run().inventory.uuid
    return session_uuid


def login_iam2_project(project_name, session_uuid=None):
    action = api_actions.LoginIAM2ProjectAction()
    action.timeout = 30000
    action.projectName = project_name
    test_util.action_logger('login iam2 project : %s' % project_name)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def remove_attributes_from_iam2_organization(uuid, attribute_uuids, session_uuid=None):
    action = api_actions.RemoveAttributesFromIAM2OrganizationAction()
    action.timeout = 30000
    action.attributeUuids = attribute_uuids
    action.uuid = uuid
    test_util.action_logger('remove attributes :%s from organization : %s' % (attribute_uuids, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_attributes_from_iam2_project(uuid, attribute_uuids, session_uuid=None):
    action = api_actions.RemoveAttributesFromIAM2ProjectAction()
    action.timeout = 30000
    action.attributeUuids = attribute_uuids
    action.uuid = uuid
    test_util.action_logger('remove attributes :%s from project : %s' % (attribute_uuids, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_attributes_from_iam2_virtual_id_group(uuid, attribute_uuids, session_uuid=None):
    action = api_actions.RemoveAttributesFromIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.attributeUuids = attribute_uuids
    action.uuid = uuid
    test_util.action_logger('remove attributes :%s from iam2 virtual id group : %s' % (attribute_uuids, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_attributes_from_iam2_virtual_id(uuid, attribute_uuids, session_uuid=None):
    action = api_actions.RemoveAttributesFromIAM2VirtualIDAction()
    action.timeout = 30000
    action.attributeUuids = attribute_uuids
    action.uuid = uuid
    test_util.action_logger('remove attributes :%s from virtual id : %s' % (attribute_uuids, uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_iam2_virtual_ids_from_group(virtual_id_uuids, group_uuid, session_uuid=None):
    action = api_actions.RemoveIAM2VirtualIDsFromGroupAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.groupUuid = group_uuid
    test_util.action_logger('remove virtual id : %s from group :%s' % (virtual_id_uuids, group_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_iam2_virtual_ids_from_organization(virtual_id_uuids, organization_uuid, session_uuid=None):
    action = api_actions.RemoveIAM2VirtualIDsFromOrganizationAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.organizationUuid = organization_uuid
    test_util.action_logger('remove virtual id : %s from organization :%s' % (virtual_id_uuids, organization_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_iam2_virtual_ids_from_project(virtual_id_uuids, project_uuid, session_uuid=None):
    action = api_actions.RemoveIAM2VirtualIDsFromProjectAction()
    action.timeout = 30000
    action.virtualIDUuids = virtual_id_uuids
    action.projectUuid = project_uuid
    test_util.action_logger('remove virtual id : %s from project :%s' % (virtual_id_uuids, project_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_roles_from_iam2_virtual_idgroup(role_uuids, group_uuid, session_uuid=None):
    action = api_actions.RemoveRolesFromIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.roleUuids = role_uuids
    action.groupUuid = group_uuid
    test_util.action_logger('remove roles : %s from group :%s' % (role_uuids, group_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def remove_roles_from_iam2_virtual_id(role_uuids, virtual_id_uuid, session_uuid=None):
    action = api_actions.RemoveRolesFromIAM2VirtualIDAction()
    action.timeout = 30000
    action.roleUuids = role_uuids
    action.virtualIDUuid = virtual_id_uuid
    test_util.action_logger('remove roles : %s from virtual id :%s' % (role_uuids, virtual_id_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt


def update_iam2_organization(uuid, name=None, description=None, parent_uuid=None, type=None, session_uuid=None):
    action = api_actions.UpdateIAM2OrganizationAction()
    action.timeout = 30000
    action.uuid = uuid
    if name:
        action.name = name
    if description:
        action.description = description
    if parent_uuid:
        action.parentUuid = parent_uuid
    if type:
        action.type = type
    test_util.action_logger('update iam2 organization : %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def update_iam2_project(uuid, name=None, description=None, session_uuid=None):
    action = api_actions.UpdateIAM2ProjectAction()
    action.timeout = 30000
    action.uuid = uuid
    if name:
        action.name = name
    if description:
        action.description = description
    test_util.action_logger('update iam2 project : %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def update_iam2_virtual_id_group(uuid, name=None, description=None, session_uuid=None):
    action = api_actions.UpdateIAM2VirtualIDGroupAction()
    action.timeout = 30000
    action.uuid = uuid
    if name:
        action.name = name
    if description:
        action.description = description
    test_util.action_logger('update iam2 virtual id group : %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def update_iam2_virtual_id(uuid, name=None, description=None, password=None, session_uuid=None):
    action = api_actions.UpdateIAM2VirtualIDAction()
    action.timeout = 30000
    action.uuid = uuid
    if name:
        action.name = name
    if description:
        action.description = description
    if password:
        action.password = description
    test_util.action_logger('update iam2 virtual id : %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory
