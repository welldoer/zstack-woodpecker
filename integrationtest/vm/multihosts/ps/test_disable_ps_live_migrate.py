'''
New Integration Test for delete vm under PS disable mode.

@author: SyZhao
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.primarystorage_operations as ps_ops
import zstackwoodpecker.operations.host_operations as host_ops
import zstackwoodpecker.operations.vm_operations as vm_ops
import zstackwoodpecker.header.vm as vm_header
import apibinding.inventory as inventory
import os

_config_ = {
        'timeout' : 1000,
        'noparallel' : True
        }

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()
ps_uuid = None
host_uuid = None
vr_uuid = None

def test():
    global test_obj_dict
    global ps_uuid
    global host_uuid
    global vr_uuid

    test_util.test_dsc('Create test vm and check')
    vm = test_stub.create_vr_vm('vm1', 'imageName_net', 'l3VlanNetwork3')
    test_obj_dict.add_vm(vm)

    backup_storage_list = test_lib.lib_get_backup_storage_list_by_vm(vm.vm)
    for bs in backup_storage_list:
        if bs.type == inventory.CEPH_BACKUP_STORAGE_TYPE:
            break
    else:
        vm.destroy()
        test_util.test_skip('Not find ceph type backup storage.')

    l3_1_name = os.environ.get('l3VlanNetwork3')
    l3_1 = test_lib.lib_get_l3_by_name(l3_1_name)
    vr = test_lib.lib_find_vr_by_l3_uuid(l3_1.uuid)[0]
    vr_uuid = vr.uuid
    
    host = test_lib.lib_get_vm_host(vm.get_vm())
    host_uuid = host.uuid
    test_obj_dict.add_vm(vm)
    vm.check()
    ps = test_lib.lib_get_primary_storage_by_vm(vm.get_vm())
    ps_uuid = ps.uuid
    ps_ops.change_primary_storage_state(ps_uuid, 'disable')
    if not test_lib.lib_wait_target_up(vm.get_vm().vmNics[0].ip, '22', 90):
        test_util.test_fail('VM is expected to running when PS change to disable state')

    #vm.set_state(vm_header.RUNNING)
    vm.check()
    test_stub.migrate_vm_to_random_host(vm)
    vm.check()

    ps_ops.change_primary_storage_state(ps_uuid, 'enable')
    host_ops.reconnect_host(host_uuid)
    vm_ops.reconnect_vr(vr_uuid)
    test_util.test_pass('PS disable mode Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global ps_uuid
    if ps_uuid != None:
        ps_ops.change_primary_storage_state(ps_uuid, 'Enabled')
    global host_uuid
    if host_uuid != None:
        host_ops.reconnect_host(host_uuid)
    global vr_uuid
    if vr_uuid != None:
        vm_ops.reconnect_vr(vr_uuid)
    global test_obj_dict
    test_lib.lib_error_cleanup(test_obj_dict)