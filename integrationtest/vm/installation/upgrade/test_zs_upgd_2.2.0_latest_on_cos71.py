'''
@author: YeTian  2017-12-23
Test on centos71 mini iso installed zstack 2.2.2 release 381, upgrade the latest zstack
'''
import os
import tempfile
import uuid
import time

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstacklib.utils.ssh as ssh
import zstackwoodpecker.operations.scenario_operations as scen_ops

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()
tmp_file = '/tmp/%s' % uuid.uuid1().get_hex()
vm_inv = None


def test():
    global vm_inv
    global zone_inv
    global cluster_inv
    global host_inv

    test_util.test_dsc('Create test vm to test zstack upgrade on centos71 mini iso with zstack 2.2.2 by -u.')

    image_name = os.environ.get('imageNameBase_c71_222_mn')
    iso_path = os.environ.get('iso_path')
    zstack_latest_version = os.environ.get('zstackLatestVersion')
    zstack_latest_path = os.environ.get('zstackLatestInstaller')
    vm_name = os.environ.get('vmName')
    upgrade_script_path = os.environ.get('upgradeScript')

    vm_inv = test_stub.create_vm_scenario(image_name, vm_name)
    vm_ip = vm_inv.vmNics[0].ip
    test_lib.lib_wait_target_up(vm_ip, 22)

    test_stub.make_ssh_no_password(vm_ip, tmp_file)

    test_util.test_logger('Update MN IP')
    test_stub.update_mn_hostname(vm_ip, tmp_file)
    test_stub.update_mn_ip(vm_ip, tmp_file)
    test_stub.start_mn(vm_ip, tmp_file)
    test_stub.check_installation(vm_ip, tmp_file)

    test_util.test_logger('Upgrade zstack to latest') 
    test_stub.update_iso(vm_ip, tmp_file, iso_path, upgrade_script_path)
    test_stub.upgrade_zstack(vm_ip, zstack_latest_path, tmp_file) 
    test_stub.check_zstack_version(vm_ip, tmp_file, zstack_latest_version)
    test_stub.start_mn(vm_ip, tmp_file)
    test_stub.check_installation(vm_ip, tmp_file)

    test_util.test_dsc('Create zone of name is zone1')
    zone_inv = test_stub.create_zone1(vm_ip, tmp_file)
    zone_uuid = zone_inv.uuid

    test_util.test_dsc('Create cluster of name is cluster1')
    cluster_inv = test_stub.create_cluster1(vm_ip, zone_uuid, tmp_file)
    cluster_uuid = cluster_inv.uuid

    test_util.test_dsc('Add host of name is host1')
    host_inv = test_stub.add_kvm_host1(vm_ip, cluster_uuid, tmp_file)
    host_uuid = host_inv.uuid

    os.system('rm -f %s' % tmp_file)
    test_stub.destroy_vm_scenario(vm_inv.uuid)
    test_util.test_pass('ZStack upgrade from centos71 mini iso 2.2.2 to the latest master zstack Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global vm_inv
    global zone_inv
    global cluster_inv
    global host_inv

    os.system('rm -f %s' % tmp_file)
    if vm_inv:
        test_stub.destroy_vm_scenario(vm_inv.uuid)
    test_lib.lib_error_cleanup(test_obj_dict)
