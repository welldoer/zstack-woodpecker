'''

All ldap operations for test.

@author: quarkonics
'''

from apibinding.api import ApiError
import apibinding.inventory as inventory
import apibinding.api_actions as api_actions
import zstackwoodpecker.test_util as test_util
import account_operations
import config_operations

import os
import inspect

def add_aliyun_key_secret(name, description, key, secret, session_uuid=None):
    action = api_actions.AddAliyunKeySecretAction()
    action.name = name
    action.description = description
    action.key = key
    action.secret = secret
    test_util.action_logger('Add [aliyun key secret:] %s' % key)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[aliyun key secret:] %s is added.' % key)
    return evt.inventory

def del_aliyun_key_secret(uuid, session_uuid=None):
    action = api_actions.DeleteAliyunKeySecretAction()
    action.uuid = uuid
    test_util.action_logger('Delete [aliyun key secret:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[aliyun key secret:] %s is deleted.' % uuid)
    return evt

def attach_aliyun_key(uuid, session_uuid=None):
    action = api_actions.AttachAliyunKeyAction()
    action.uuid = uuid
    test_util.action_logger('Attach [aliyun key:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[aliyun key:] %s is attached.' % uuid)
    return evt

def detach_aliyun_key(uuid, session_uuid=None):
    action = api_actions.DetachAliyunKeyAction()
    action.uuid = uuid
    test_util.action_logger('Detach [aliyun key:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[aliyun key:] %s is detached.' % uuid)
    return evt

def get_oss_bucket_name_from_remote(uuid, session_uuid=None):
    action = api_actions.GetOssBucketNameFromRemoteAction()
    test_util.action_logger('get Oss Bucket Name from Remote')
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt.inventories

def add_oss_bucket_from_remote(region_id, oss_bucket_name, session_uuid=None):
    action = api_actions.AddOssBucketFromRemoteAction()
    action.regionid = region_id
    action.bucketName = oss_bucket_name
    test_util.action_logger('Add [Oss Bucket From Remote:] %s %s' % (region_id, oss_bucket_name))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss Bucket:] %s %s is added.' % (region_id, oss_bucket_name))
    return evt.inventory

def del_oss_bucket_name_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteOssBucketNameLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Oss File Bucket Name in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss File Bucket Name in local:] %s is deleted.' % (uuid))
    return evt

def create_oss_bucket_remote(region_id, bucket_name, description, session_uuid=None):
    action = api_actions.CreateOssBucketRemoteAction()
    action.regionId = region_id
    action.bucketName = bucket_name
    action.description = description
    test_util.action_logger('Create [Oss Bucket Name Remote:] %s %s' % (region_id, bucket_name))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss Bucket Name Remote:] %s %s is created.' % (region_id, bucket_name))
    return evt.inventory

def del_oss_bucket_remote(uuid, session_uuid=None):
    action = api_actions.DeleteOssBucketRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Oss Bucket Name Remote:] %s' % uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss Bucket Name Remote:] %s is deleted.' % uuid)
    return evt

def del_oss_bucket_file_remote(bucket_uuid, file_name, session_uuid=None):
    action = api_actions.DeleteOssBucketFileRemoteAction()
    action.bucketUuid = bucket_uuid
    action.fileName = file_name
    test_util.action_logger('Delete [Oss Bucket File Remote:] %s %s' % (bucket_uuid, file_name))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss Bucket File Remote:] %s %s is deleted.' % (bucket_uuid, file_name))
    return evt

def get_oss_bucket_file_from_remote(bucket_uuid, session_uuid=None):
    action = api_actions.GetOssBucketFileFromRemoteAction()
    action.uuid = bucket_uuid
    test_util.action_logger('Get [Oss Bucket File From Remote:] %s' % bucket_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def get_datacenter_from_remote(datacenter_type, session_uuid=None):
    action = api_actions.GetDataCenterFromRemoteAction()
    action.type = datacenter_type
    test_util.action_logger('Get [Datacenter From Remote:] %s' % datacenter_type)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt.inventories

def add_datacenter_from_remote(datacenter_type, region_id, description, session_uuid=None):
    action = api_actions.AddDataCenterFromRemoteAction()
    action.type = datacenter_type
    action.regionId = region_id
    action.description = description
    test_util.action_logger('Add [datacenter from remote:] %s %s' % (datacenter_type, region_id))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[datacenter from remote:] %s %s is added.' % (datacenter_type, region_id))
    return evt.inventory

def del_datacenter_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteDataCenterInLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [datacenter in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[datacenter in local:] %s is deleted.' % uuid)
    return evt

def attach_oss_bucket_to_ecs_datacenter(oss_bucket_uuid, datacenter_uuid, session_uuid=None):
    action = api_actions.AttachOssBucketToEcsDataCenterAction()
    action.ossBucketUuid = oss_bucket_uuid
    action.dataCenterUuid = datacenter_uuid 
    test_util.action_logger('Attach [Oss bucket:] %s to [Datacenter:] %s' % (oss_bucket_uuid, datacenter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss bucket:] %s is attached to [Datacenter:] %s.' % (oss_bucket_uuid, datacenter_uuid))
    return evt

def detach_oss_bucket_to_ecs_datacenter(oss_bucket_uuid, datacenter_uuid, session_uuid=None):
    action = api_actions.DetachOssBucketFromEcsDataCenterAction()
    action.ossBucketUuid = oss_bucket_uuid
    action.dataCenterUuid = datacenter_uuid 
    test_util.action_logger('Detach [Oss bucket:] %s from [Datacenter:] %s' % (oss_bucket_uuid, datacenter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Oss bucket:] %s is detached to [Datacenter:] %s.' % (oss_bucket_uuid, datacenter_uuid))
    return evt

def get_identity_zone_from_remote(datacenter_type, region_id, session_uuid=None):
    action = api_actions.GetIdentityZoneFromRemoteAction()
    action.type = datacenter_type
    action.regionId = region_id
    test_util.action_logger('Get [Identity zone From Remote:] %s %s' % (datacenter_type, region_id))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt.inventories

def add_identity_zone_from_remote(datacenter_type, datacenter_uuid, zone_id, session_uuid=None):
    action = api_actions.AddIdentityZoneFromRemoteAction()
    action.type = datacenter_type
    action.dataCenterUuid = datacenter_uuid
    action.zoneId = zone_id
    test_util.action_logger('Add [identity zone from remote:] %s %s' % (datacenter_uuid, zone_id))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[identity zone from remote:] %s %s is added.' % (datacenter_uuid, zone_id))
    return evt.inventory

def del_identity_zone_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteIdentityZoneInLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [identity zone in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[identity zone in local:] %s is deleted.' % uuid)
    return evt

def create_ecs_vpc_remote(datacenter_uuid, name, cidr_block, session_uuid=None):
    action = api_actions.CreateEcsVpcRemoteAction()
    action.dataCenterUuid = datacenter_uuid
    action.name = name
    action.cidrBlock = cidr_block
    test_util.action_logger('Create [Ecs VPC Remote:] %s %s %s' % (datacenter_uuid, name, cidr_block))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VPC Remote:] %s %s %s is created.' % (datacenter_uuid, name, cidr_block))
    return evt.inventory

def sync_ecs_vpc_from_remote(datacenter_uuid, session_uuid=None):
    action = api_actions.SyncEcsVpcFromRemoteAction()
    action.dataCenterUuid = datacenter_uuid
    test_util.action_logger('Sync [Ecs VPC From Remote:] %s' % (datacenter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def del_ecs_vpc_local(uuid, session_uuid=None):
    action = api_actions.DeleteEcsVpcInLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs VPC Local:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VPC Local:] %s is deleted.' % (uuid))
    return evt

def del_ecs_vpc_remote(uuid, session_uuid=None):
    action = api_actions.DeleteEcsVpcRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs VPC Remote:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VPC Remote:] %s is deleted.' % (uuid))
    return evt

def create_ecs_vswtich_remote(vpc_uuid, identity_zone_uuid, name, cidr_block, session_uuid=None):
    action = api_actions.CreateEcsVSwitchRemoteAction()
    action.vpcUuid = vpc_uuid
    action.identityZoneUuid = identity_zone_uuid
    action.name = name
    action.cidrBlock = cidr_block
    test_util.action_logger('Create [Ecs VSwitch Remote:] %s %s %s %s' % (vpc_uuid, identity_zone_uuid, name, cidr_block))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VSwitch Remote:] %s %s %s %s is created.' % (vpc_uuid, identity_zone_uuid, name, cidr_block))
    return evt.inventory

def create_hybrid_eip(data_center_uuid, name, band_width, charge_type='PayByTraffic', eip_type='aliyun', session_uuid=None):
    action = api_actions.CreateHybridEipAction()
    action.dataCenterUuid = data_center_uuid
    action.name = name
    action.bandWidthMb = band_width
    action.chargeType = charge_type
    action.type = eip_type
    test_util.action_logger('Create [Hybrid Eip:] %s %s %s %s' % (data_center_uuid, name, charge_type, eip_type))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Hybrid Eip:] %s %s %s %s is created.' % (data_center_uuid, name, charge_type, eip_type))
    return evt.inventory

def del_hybrid_eip_remote(uuid, eip_type='aliyun', session_uuid=None):
    action = api_actions.DeleteHybridEipRemoteAction()
    action.uuid = uuid
    action.type = eip_type
    test_util.action_logger('Delete [Hybrid Eip Remote:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Hybrid Eip Remote:] %s is deleted.' % uuid)
    return evt

def attach_hybrid_eip_to_ecs(eip_uuid, ecs_uuid, eip_type='aliyun', session_uuid=None):
    action = api_actions.AttachHybridEipToEcsAction()
    action.eipUuid = eip_uuid
    action.ecsUuid = ecs_uuid
    action.type = eip_type
    test_util.action_logger('Attach [Hybrid Eip :] %s to ECS %s' % (eip_uuid, ecs_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Hybrid Eip :] %s is attached to Ecs %s.' % (eip_uuid, ecs_uuid))
    return evt

def detach_hybrid_eip_from_ecs(eip_uuid, eip_type='aliyun', session_uuid=None):
    action = api_actions.DetachHybridEipFromEcsAction()
    action.eipUuid = eip_uuid
    action.type = eip_type
    test_util.action_logger('Detach [Hybrid Eip :] %s from ECS' % eip_uuid)
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Hybrid Eip :] %s is detached from Ecs.' % eip_uuid)
    return evt

def sync_hybrid_eip_from_remote(data_center_uuid, eip_type='aliyun', session_uuid=None):
    action = api_actions.SyncHybridEipFromRemoteAction()
    action.dataCenterUuid = data_center_uuid
    action.type = eip_type
    test_util.action_logger('Sync [Hybrid Eip From Remote:] %s' % (data_center_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt.inventories

def sync_ecs_vswitch_from_remote(data_center_uuid, session_uuid=None):
    action = api_actions.SyncEcsVSwitchFromRemoteAction()
    action.dataCenterUuid = data_center_uuid
    test_util.action_logger('Sync [Ecs VSwitch From Remote:] %s' % (data_center_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt.inventories

def del_ecs_vswitch_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteEcsVSwitchInLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs VSwitch: %s] in Local' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VSwitch: %s] in Local is deleted.' % uuid)
    return evt

def del_ecs_vswitch_remote(uuid, session_uuid=None):
    action = api_actions.DeleteEcsVSwitchRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs VSwitch Remote:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs VSwitch Remote:] %s is deleted.' % (uuid))
    return evt

def del_ecs_instance_local(uuid, session_uuid=None):
    action = api_actions.DeleteEcsInstanceLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs Instance in Local:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs Instance in Local:] %s is deleted.' % (uuid))
    return evt

def sync_aliyun_virtual_router_from_remote(vpc_uuid, session_uuid=None):
    action = api_actions.SyncAliyunVirtualRouterFromRemoteAction()
    action.vpcUuid = vpc_uuid
    test_util.action_logger('Sync [Aliyun VirtualRouter From Remote:] %s' % (vpc_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def sync_router_entry_from_remote(vrouter_uuid, vrouter_type, session_uuid=None):
    action = api_actions.SyncAliyunRouteEntryFromRemoteAction()
    action.uuid = vrouter_uuid
    action.vRouterType = vrouter_type
    test_util.action_logger('Sync [Router Entry From Remote:] %s' % (vrouter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def create_vpc_virtualrouter_entry_remote(dest_cidr_block, vrouter_uuid, vrouter_type, next_hop_type, next_hop_uuid, session_uuid=None):
    action = api_actions.CreateAliyunVpcVirtualRouterEntryRemoteAction()
    action.destinationCidrBlock = dest_cidr_block
    action.uuid = vrouter_uuid
    action.vRouterType = vrouter_type
    action.nextHopType = next_hop_type
    action.nextHopUuid = next_hop_uuid
    test_util.action_logger('Create [VPC VirtualRouter Entry Remote:] %s %s %s %s %s' % (dest_cidr_block, vrouter_uuid, vrouter_type, next_hop_type, next_hop_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[VPC VirtualRouter Entry Remote:] %s %s %s %s %s is created.' % (dest_cidr_block, vrouter_uuid, vrouter_type, next_hop_type, next_hop_uuid))
    return evt.inventory

def del_router_entry_remote(uuid, session_uuid=None):
    action = api_actions.DeleteAliyunRouteEntryRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Router Entry Remote:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Router Entry Remote:] %s is deleted.' % (uuid))
    return evt

def create_ecs_security_group_remote(name, vpc_uuid, session_uuid=None):
    action = api_actions.CreateEcsSecurityGroupRemoteAction()
    action.name = name
    action.vpcUuid = vpc_uuid
    test_util.action_logger('Create [Ecs Security Group Remote:] %s %s' % (name, vpc_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('Ecs Security Group Remote:] %s %s is created.' % (name, vpc_uuid))
    return evt.inventory

def create_ecs_security_group_rule_remote(group_uuid, direction, protocol, port_range, cidr, policy, nic_type, priority, session_uuid=None):
    action = api_actions.CreateEcsSecurityGroupRuleRemoteAction()
    action.groupUuid = group_uuid
    action.direction = direction
    action.protocol = protocol
    action.portRange = port_range
    action.cidr = cidr
    action.policy = policy
    action.nictype = nic_type
    action.priority = priority
    test_util.action_logger('Create [Ecs Security Group Rule Remote:] %s %s %s %s %s %s %s %s' % (group_uuid, direction, protocol, port_range, cidr, policy, nic_type, priority))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs Security Group Rule Remote:] %s %s %s %s %s %s %s %s is created.' % (group_uuid, direction, protocol, port_range, cidr, policy, nic_type, priority))
    return evt.inventory

def sync_security_group_from_remote(ecs_vpc_uuid, session_uuid=None):
    action = api_actions.SyncEcsSecurityGroupFromRemoteAction()
    action.ecsVpcUuid = ecs_vpc_uuid
    test_util.action_logger('Sync [Security Group From Remote:] %s' % (ecs_vpc_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def del_ecs_security_group_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteEcsSecurityGroupInLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [ecs security group in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs security group in local:] %s is deleted.' % uuid)
    return evt

def del_ecs_security_group_rule_remote(uuid, session_uuid=None):
    action = api_actions.DeleteEcsSecurityGroupRuleRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs Security Group Rule Remote:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs Security Group Rule Remote:] %s is deleted.' % (uuid))
    return evt

def del_ecs_security_group_remote(uuid, session_uuid=None):
    action = api_actions.DeleteEcsSecurityGroupRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [Ecs Security Group Remote:] %s ' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Ecs Security Group Remote:] %s is deleted.' % (uuid))
    return evt

def create_ecs_image_from_local_image(bs_uuid, datacenter_uuid, image_uuid, session_uuid=None):
    action = api_actions.CreateEcsImageFromLocalImageAction()
    action.backupStorageUuid = bs_uuid
    action.dataCenterUuid = datacenter_uuid
    action.imageUuid = image_uuid
    test_util.action_logger('Create Ecs Image from [Local image:] %s %s %s' % (bs_uuid, datacenter_uuid, image_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('Ecs Image is created from [Local image:] %s %s %s.' % (bs_uuid, datacenter_uuid, image_uuid))
    return evt.inventory

def del_ecs_image_remote(uuid, session_uuid=None):
    action = api_actions.DeleteEcsImageRemoteAction()
    action.uuid = uuid
    test_util.action_logger('Delete [ecs image remote:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs image remote:] %s is deleted.' % uuid)
    return evt

def del_ecs_image_in_local(uuid, session_uuid=None):
    action = api_actions.DeleteEcsImageLocalAction()
    action.uuid = uuid
    test_util.action_logger('Delete [ecs image in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs image in local:] %s is deleted.' % uuid)
    return evt

def del_hybrid_eip_local(uuid, eip_type='aliyun', session_uuid=None):
    action = api_actions.DeleteHybridEipFromLocalAction()
    action.type = eip_type
    action.uuid = uuid
    test_util.action_logger('Delete [Hybrid Eip in local:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[Hybrid Eip in local:] %s is deleted.' % uuid)
    return evt

def sync_ecs_image_from_remote(datacenter_uuid, session_uuid=None):
    action = api_actions.SyncEcsImageFromRemoteAction()
    action.dataCenterUuid = datacenter_uuid
    test_util.action_logger('Sync [Ecs Image From Remote:] %s' % (datacenter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def create_ecs_instance_from_local_image(ecs_root_password, bs_uuid, image_uuid, ecs_vswitch_uuid, identity_zone_uuid, instance_offering_uuid, ecs_bandwidth, ecs_security_group_uuid, private_ip_address=None, allocate_public_ip='false', ecs_instance_name=None, ecs_console_password=None, session_uuid=None):
    action = api_actions.CreateEcsInstanceFromLocalImageAction()
    action.ecsRootPassword = ecs_root_password
    action.backupStorageUuid = bs_uuid
    action.imageUuid = image_uuid
    action.ecsVSwitchUuid = ecs_vswitch_uuid
    action.identityZoneUuid = identity_zone_uuid
    action.instanceOfferingUuid = instance_offering_uuid
    action.ecsBandWidth = ecs_bandwidth
    action.ecsSecurityGroupUuid = ecs_security_group_uuid
    action.privateIpAddress = private_ip_address
    action.allocatePublicIp = allocate_public_ip
    action.ecsInstanceName = ecs_instance_name
    action.ecsConsolePassword = ecs_console_password
    test_util.action_logger('Create Ecs Instance from [Local image:] %s %s' % (bs_uuid, image_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('Ecs Instance is created from [Local image:] %s %s.' % (bs_uuid, image_uuid))
    return evt.inventory

def del_ecs_instance(uuid, session_uuid=None):
    action = api_actions.DeleteEcsInstanceAction()
    action.uuid = uuid
    test_util.action_logger('Delete [ecs instance:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs instance:] %s is deleted.' % uuid)
    return evt

def sync_ecs_instance_from_remote(datacenter_uuid, session_uuid=None):
    action = api_actions.SyncEcsInstanceFromRemoteAction()
    action.dataCenterUuid = datacenter_uuid
    test_util.action_logger('Sync [Ecs Instance From Remote:] %s' % (datacenter_uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    return evt

def stop_ecs_instance(uuid, session_uuid=None):
    action = api_actions.StopEcsInstanceAction()
    action.uuid = uuid
    test_util.action_logger('Stop [ecs instance:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs instance:] %s is stopped.' % uuid)
    return evt

def start_ecs_instance(uuid, session_uuid=None):
    action = api_actions.StartEcsInstanceAction()
    action.uuid = uuid
    test_util.action_logger('Start [ecs instance:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs instance:] %s is started.' % uuid)
    return evt

def reboot_ecs_instance(uuid, session_uuid=None):
    action = api_actions.RebootEcsInstanceAction()
    action.uuid = uuid
    test_util.action_logger('Reboot [ecs instance:] %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs instance:] %s is rebooted.' % uuid)
    return evt

def update_ecs_instance_vnc_password(uuid, password, session_uuid=None):
    action = api_actions.UpdateEcsInstanceVncPasswordAction()
    action.uuid = uuid
    action.password = password
    test_util.action_logger('Update [ecs instance:] vnc password %s' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid) 
    test_util.test_logger('[ecs instance:] %s vnc password is updated.' % uuid)
    return evt

def update_image_guestOsType(uuid, guest_os_type, session_uuid=None):
    action = api_actions.UpdateImageAction()
    action.uuid = uuid
    action.guestOsType = guest_os_type
    test_util.action_logger('Update [image %s] guestOsType' % (uuid))
    evt = account_operations.execute_action_with_session(action, session_uuid)
    test_util.action_logger('[image %s] guestOsType is updated to [%s]' % (uuid, guest_os_type))
    return evt

def query_ecs_image_local(session_uuid=None):
    action = api_actions.QueryEcsImageFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Ecs image from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_ecs_vpc_local(session_uuid=None):
    action = api_actions.QueryEcsVpcFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Ecs Vpc from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_ecs_vswitch_local(session_uuid=None):
    action = api_actions.QueryEcsVSwitchFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Ecs vSwitch from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_ecs_instance_local(session_uuid=None):
    action = api_actions.QueryEcsInstanceFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Ecs Instance from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_aliyun_key_secret(session_uuid=None):
    action = api_actions.QueryAliyunKeySecretAction()
    action.conditions = []
    test_util.action_logger('Query Aliyun Key Secret')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_datacenter_local(session_uuid=None):
    action = api_actions.QueryDataCenterFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query DataCenter from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_ecs_security_group_local(session_uuid=None):
    action = api_actions.QueryEcsSecurityGroupFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Ecs Security Group from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_hybrid_eip_local(session_uuid=None):
    action = api_actions.QueryHybridEipFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Hybrid Eip from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def query_aliyun_virtual_router_local(session_uuid=None):
    action = api_actions.QueryAliyunVirtualRouterFromLocalAction()
    action.conditions = []
    test_util.action_logger('Query Aliyun Virtual Router from local')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt

def get_ecs_instance_vnc_url(uuid, session_uuid=None):
    action = api_actions.GetEcsInstanceVncUrlAction()
    action.uuid = uuid
    test_util.action_logger('Get Ecs Instance Vpc Url')
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt