'''
@author: FangSun
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.vm_operations as vm_ops
import time
import random

_config_ = {
        'timeout' : 1000,
        'noparallel' : True
        }

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()


def test():

    test_util.test_dsc("STEP1: Ceate vm instance offering")
    vm_instance_offering = test_lib.lib_create_instance_offering(cpuNum = 1,
                                                                memorySize = 1024 * 1024 * 1024)
    test_obj_dict.add_instance_offering(vm_instance_offering)

    test_util.test_dsc("STEP2: Ceate vm and wait until it up for testing")
    vm = test_stub.create_vm(vm_name = 'ckvmoffering-c7-64', image_name = "imageName_i_c7",
                             instance_offering_uuid=vm_instance_offering.uuid)
    test_obj_dict.add_vm(vm)
    vm.check()

    test_util.test_dsc("STEP3: Ceate Snapshot of root volume")
    vm_root_volume_inv = test_lib.lib_get_root_volume(vm.get_vm())
    snapshots = test_obj_dict.get_volume_snapshot(vm_root_volume_inv.uuid)
    snapshots.set_utility_vm(vm)
    snapshots.create_snapshot('create_root_snapshot1')
    snapshot1 = snapshots.get_current_snapshot()

    test_util.test_dsc("STEP4: Hot Plugin CPU and Memory and check capacity")
    cpu_change = random.randint(1,5)
    mem_change = random.randint(1,500)*1024*1024

    with test_stub.CapacityCheckerContext(vm, cpu_change, mem_change):
        vm_ops.update_vm(vm.get_vm().uuid, vm_instance_offering.cpuNum+cpu_change,
                         vm_instance_offering.memorySize+mem_change)
        vm.update()
        test_stub.online_hotplug_cpu_memory(vm)
        time.sleep(10)

    test_util.test_dsc("STEP5: Recover from snapshot make sure CPU memory no change")
    with test_stub.CapacityCheckerContext(vm, 0, 0) as cc:
        vm.stop()
        vm.check()
        snapshots.check()
        snapshots.use_snapshot(snapshot1)
        vm.start()
        vm.check()
        cc.disable_internal_check = True

    test_util.test_dsc("STEP6: Destroy test object")
    test_lib.lib_error_cleanup(test_obj_dict)
    test_util.test_pass('VM online change instance offering Test Pass')


def error_cleanup():
    test_lib.lib_error_cleanup(test_obj_dict)
