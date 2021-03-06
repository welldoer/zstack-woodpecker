'''

New Test For set HA global config test

@author: Quarkonics
'''
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.operations.vm_operations as vm_ops
import zstackwoodpecker.operations.volume_operations as vol_ops 
import zstackwoodpecker.operations.image_operations as img_ops
import zstackwoodpecker.operations.host_operations as host_ops
import zstackwoodpecker.operations.net_operations as net_ops
import zstackwoodpecker.operations.ha_operations as ha_ops
import zstackwoodpecker.operations.console_operations as console_ops
import zstackwoodpecker.operations.scheduler_operations as schd_ops
import zstackwoodpecker.operations.config_operations as config_ops
import zstackwoodpecker.operations.account_operations as account_operations
import zstackwoodpecker.operations.resource_operations as res_ops
import zstackwoodpecker.operations.tag_operations as tag_ops
import zstackwoodpecker.zstack_test.zstack_test_image as zstack_image_header
import zstackwoodpecker.zstack_test.zstack_test_snapshot as zstack_snapshot_header
import zstackwoodpecker.zstack_test.zstack_test_vm as zstack_vm_header
import zstackwoodpecker.operations.deploy_operations as deploy_operations
import zstackwoodpecker.header.vm as vm_header
import apibinding.api_actions as api_actions
import apibinding.inventory as inventory
import threading
import uuid
import os
import time
import json
import simplejson
import zstackwoodpecker.operations.deploy_operations as dep_ops

_config_ = {
        'timeout' : 24*60*60+1200,
        'noparallel' : True,
        }


test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()
vm = None
origin_value = None


def test():
    global vm
    global origin_value
    imagestore = test_lib.lib_get_image_store_backup_storage()
    if imagestore == None:
        test_util.test_skip('Required imagestore to test')
    image_uuid = test_stub.get_image_by_bs(imagestore.uuid)
    cond = res_ops.gen_query_conditions('type', '=', 'SharedMountPoint')
    pss = res_ops.query_resource(res_ops.PRIMARY_STORAGE, cond)

    if len(pss) == 0:
        test_util.test_skip('Required %s ps to test' % (ps_type))
    ps_uuid = pss[0].uuid
    vm = test_stub.create_vm(image_uuid=image_uuid, ps_uuid=ps_uuid)

    vm.stop()
    ha_ops.set_vm_instance_ha_level(vm.get_vm().uuid,'NeverStop')
    cond = res_ops.gen_query_conditions('uuid', '=', vm.get_vm().uuid)
    for i in range(5):
        time.sleep(1)
        try:
            if res_ops.query_resource(res_ops.VM_INSTANCE, cond)[0].state == vm_header.RUNNING:
                break
        except:
            test_util.test_logger('Retry until VM change to running')

    if res_ops.query_resource(res_ops.VM_INSTANCE, cond)[0].state != vm_header.RUNNING:
        test_util.test_fail('set HA after stopped VM test fail')

    no_exception = True
    try:
        config_ops.change_global_config('ha','host.check.successRatio', -1)
        no_exception = True
    except:
        test_util.test_logger('Expected exception')
        no_exception = False
    if no_exception:
        test_util.test_fail('Expect exception while there is none') 
    
    origin_value = config_ops.change_global_config('ha','neverStopVm.scan.interval', '30')

    config_ops.change_global_config('ha','enable', 'false')
    vm.stop()
    cond = res_ops.gen_query_conditions('uuid', '=', vm.get_vm().uuid)
    for i in range(int(config_ops.get_global_config_value('ha','neverStopVm.scan.interval'))):
        time.sleep(1)
        try:
            if res_ops.query_resource(res_ops.VM_INSTANCE, cond)[0].state != vm_header.STOPPED:
                break
        except:
            test_util.test_logger('Retry until VM change to running')

    if res_ops.query_resource(res_ops.VM_INSTANCE, cond)[0].state == vm_header.RUNNING:
        test_util.test_fail('disable HA after stopped VM test fail')

    test_util.test_pass('set HA global config pass')

def env_recover():
    config_ops.change_global_config('ha','enable', 'true')
    global origin_value
    config_ops.change_global_config('ha','neverStopVm.scan.interval', origin_value)
    global vm
    if vm != None:
        vm.destroy()
        vm.expunge()
