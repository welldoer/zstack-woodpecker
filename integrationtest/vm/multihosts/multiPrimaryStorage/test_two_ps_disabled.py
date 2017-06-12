'''
@author: FangSun
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.primarystorage_operations as ps_ops
import random

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()
VM_COUNT = 5
VOLUME_NUMBER = 0
new_ps_list = []


def test():
    env = test_stub.TwoPrimaryStorageEnv(test_object_dict=test_obj_dict,
                                         first_ps_vm_number=VM_COUNT,
                                         second_ps_vm_number=VM_COUNT,
                                         first_ps_volume_number=VOLUME_NUMBER,
                                         second_ps_volume_number=VOLUME_NUMBER)
    env.check_env()
    env.deploy_env()
    first_ps_vm_list = env.first_ps_vm_list
    first_ps_volume_list = env.first_ps_volume_list
    second_ps_vm_list = env.second_ps_vm_list
    second_ps_volume_list = env.second_ps_volume_list
    if env.new_ps:
        new_ps_list.append(env.second_ps)
    tbj_list = first_ps_vm_list + second_ps_vm_list + first_ps_volume_list + second_ps_volume_list

    test_util.test_dsc('Disable All Primary Storage')
    for ps in [env.first, env.second_ps]:
        ps_ops.change_primary_storage_state(ps.uuid, state='disable')

    test_util.test_dsc('make sure all VM and Volumes still OK and running')
    for test_object in tbj_list:
        test_object.check()

    test_util.test_dsc("Try to Create one vm")
    try:
        vm = test_stub.create_multi_vms(name_prefix='test-vm', count=1)[0]
    except Exception as e:
        test_util.test_logger('EXPECTED: Catch exception {}\nCreate vm in disabled ps will fail'.format(e))
    else:
        test_obj_dict.add_vm(vm)
        test_util.test_fail("CRITICAL ERROR: Can create VM in disabled ps")

    test_util.test_dsc("Try to Create one volume")
    try:
        volume = test_stub.create_multi_volume(count=1)
    except Exception as e:
        test_util.test_logger('EXPECTED: Catch exception {}\nCreate vm in disabled ps will fail'.format(e))
    else:
        test_obj_dict.add_volume(volume)
        test_util.test_fail("CRITICAL ERROR: Can create volume in disabled ps")


    test_util.test_pass('Multi PrimaryStorage Test Pass')

def env_recover():
    test_lib.lib_error_cleanup(test_obj_dict)
    if new_ps_list:
        for new_ps in new_ps_list:
            ps_ops.detach_primary_storage(new_ps.uuid, new_ps.attachedClusterUuids[0])
            ps_ops.delete_primary_storage(new_ps.uuid)
