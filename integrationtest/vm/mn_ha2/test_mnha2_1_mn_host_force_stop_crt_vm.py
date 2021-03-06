'''
Test Steps:
    1. force stop host where vip located.
    2. check vip switch to another MN.
    3. create vm to validate everything goes on well. 

@author: SyZhao
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.operations.node_operations as node_ops
import zstackwoodpecker.zstack_test.zstack_test_vm as test_vm_header
import test_stub
import time
import os

vm = None
vip_s_vm_cfg_lst = None

def test():
    global vm
    global vip_s_vm_cfg_lst

    vip_s_vm_cfg_lst = test_stub.get_s_vm_cfg_lst_vip_bind(test_lib.all_scenario_config, test_lib.scenario_file)
    if len(vip_s_vm_cfg_lst) != 1:
        test_util.test_fail('vip has been running on %d host(s)' % len(vip_s_vm_cfg_lst))

    test_util.test_logger("force shutdown host [%s]" % (vip_s_vm_cfg_lst[0].ip_))
    test_stub.stop_host(vip_s_vm_cfg_lst[0], test_lib.all_scenario_config, 'cold')

    time.sleep(20)

    expected_vip_s_vm_cfg_lst_ip = test_stub.get_expected_vip_s_vm_cfg_lst_after_switch(test_lib.all_scenario_config, test_lib.scenario_file, vip_s_vm_cfg_lst[0].ip_)
    if not test_stub.check_if_vip_is_on_host(test_lib.all_scenario_config, test_lib.scenario_file, expected_vip_s_vm_cfg_lst_ip):
        test_util.test_fail("find vip should drift on ip %s, but is not on it." %(expected_vip_s_vm_cfg_lst_ip))

    vip_s_vm_cfg_lst = test_stub.get_s_vm_cfg_lst_vip_bind(test_lib.all_scenario_config, test_lib.scenario_file)
    if len(vip_s_vm_cfg_lst) != 1:
        test_util.test_fail('vip has been running on %d host(s)' % len(vip_s_vm_cfg_lst))

    test_stub.wrapper_of_wait_for_management_server_start(600)

    test_stub.ensure_bss_connected()
    test_stub.ensure_pss_connected()

    vm = test_stub.create_basic_vm()
    vm.check()
    vm.destroy()

    test_util.test_pass('Create VM Test Success')

#Will be called what ever test result is
def env_recover():
    test_util.test_logger("recover host: %s" % (vip_s_vm_cfg_lst[0].ip_))
    test_stub.recover_host(vip_s_vm_cfg_lst[0], test_lib.all_scenario_config, test_lib.deploy_config)
    test_stub.wait_for_mn_ha_ready(test_lib.all_scenario_config, test_lib.scenario_file)

#Will be called only if exception happens in test().
def error_cleanup():
    global vm
    if vm:
        try:
            vm.destroy()
        except:
            pass
