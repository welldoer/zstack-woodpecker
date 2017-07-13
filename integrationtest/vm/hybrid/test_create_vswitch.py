'''

New Integration Test for hybrid.

@author: Quarkonics
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.hybrid_operations as hyb_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import time
import os

test_obj_dict = test_state.TestStateDict()
ks_inv = None
datacenter_inv = None
vpc_inv = None
iz_inv = None
vswitch_inv = None

def test():
    global ks_inv
    global datacenter_inv
    global vpc_inv
    global iz_inv
    global vswitch_inv
    datacenter_type = os.getenv('datacenterType')
    try:
        ks_inv = hyb_ops.add_aliyun_key_secret('test_hybrid', 'test for hybrid', os.getenv('aliyunKey'), os.getenv('aliyunSecret'))
    except:
        pass
    datacenter_list = hyb_ops.get_datacenter_from_remote(datacenter_type)
    regions = [ i.regionId for i in datacenter_list]
    err_list = []
    for region_id in regions:
        try:
            datacenter_inv = hyb_ops.add_datacenter_from_remote(datacenter_type, region_id, 'datacenter for test')
        except hyb_ops.ApiError, e:
            err_list.append(e)
            pass
        if datacenter_inv:
            break
    if len(err_list) == len(regions):
        raise hyb_ops.ApiError("Failed to add DataCenter: %s" % err_list)
    vpc_inv = hyb_ops.create_ecs_vpc_remote(datacenter_inv.uuid, 'vpc_for_test', '192.168.0.0/16')
    time.sleep(5)
    iz_list = hyb_ops.get_identity_zone_from_remote(datacenter_type, region_id)
    zone_id = iz_list[0].zoneId
    iz_inv = hyb_ops.add_identity_zone_from_remote(datacenter_type, datacenter_inv.uuid, zone_id)
    vswitch_inv = hyb_ops.create_ecs_vswtich_remote(vpc_inv.uuid, iz_inv.uuid, 'zstack-test-vswitch', '192.168.0.0/16')
    test_util.test_pass('Create ECS VSwitch Test Success')


def env_recover():
    global vswitch_inv
    if vswitch_inv:
        time.sleep(10)
        hyb_ops.del_ecs_vswitch_remote(vswitch_inv.uuid)
    global vpc_inv
    if vpc_inv:
        time.sleep(10)
        hyb_ops.del_ecs_vpc_remote(vpc_inv.uuid)
    global iz_inv
    if iz_inv:
        hyb_ops.del_identity_zone_in_local(iz_inv.uuid)
    global datacenter_inv
    if datacenter_inv:
        hyb_ops.del_datacenter_in_local(datacenter_inv.uuid)
    global ks_inv
    if ks_inv:
        hyb_ops.del_aliyun_key_secret(ks_inv.uuid)

#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    test_lib.lib_error_cleanup(test_obj_dict)