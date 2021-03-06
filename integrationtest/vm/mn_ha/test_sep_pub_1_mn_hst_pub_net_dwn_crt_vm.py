'''

Integration Test for down public network when public network is separated. 

@author: SyZhao
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.operations.node_operations as node_ops
import zstackwoodpecker.zstack_test.zstack_test_vm as test_vm_header
import zstackwoodpecker.operations.resource_operations as res_ops
import test_stub
import time
import os

vm = None
mn_host = None
pub_mn_ip = None
mag_mn_ip = None

def test():
    global vm
    global mn_host
    global pub_mn_ip
    global mag_mn_ip

    test_stub.skip_if_scenario_not_multiple_networks()

    mn_host = test_stub.get_host_by_mn_vm(test_lib.all_scenario_config, test_lib.scenario_file)
    if len(mn_host) != 1:
        test_util.test_fail('MN VM is running on %d host(s)' % len(mn_host))

    pub_mn_ip = os.environ['ZSTACK_BUILT_IN_HTTP_SERVER_IP']
    mag_mn_ip = res_ops.query_resource(res_ops.MANAGEMENT_NODE)[0].hostName
    os.environ['ZSTACK_BUILT_IN_HTTP_SERVER_IP'] = mag_mn_ip

    test_util.test_logger("shutdown host's network [%s] that mn vm is running on" % (mn_host[0].ip_))
    test_stub.shutdown_host_network(mn_host[0], test_lib.all_scenario_config, downMagt=False)
    test_util.test_logger("wait for 20 seconds to see if management node VM starts on another host")
    time.sleep(20)

    new_mn_host_ip = test_stub.get_host_by_consul_leader(test_lib.all_scenario_config, test_lib.scenario_file)
    if new_mn_host_ip == "" or (new_mn_host_ip != mn_host[0].ip_ and new_mn_host_ip != mn_host[0].managementIp_):
        test_util.test_fail("mn host should not changed if public network is down when public network is separated. Except [%s], while new host is [%s]" % (mn_host[0].ip_, new_mn_host_ip))

    count = 120
    while count > 0:
        new_mn_host = test_stub.get_host_by_mn_vm(test_lib.all_scenario_config, test_lib.scenario_file)
        if len(new_mn_host) == 1:
            test_util.test_logger("management node VM run after its former host down for 120s")
            break
        elif len(new_mn_host) > 1:
            test_util.test_fail("management node VM runs on more than one host after its former host down")
        time.sleep(5)
        count -= 1

    if len(new_mn_host) == 0:
        test_util.test_fail("management node VM does not run after its former host down for 120s")
    elif len(new_mn_host) > 1:
        test_util.test_fail("management node VM runs on more than one host after its former host down")

    #node_ops.wait_for_management_server_start()
    test_stub.wrapper_of_wait_for_management_server_start(600)

    test_stub.ensure_hosts_connected()
    test_stub.ensure_pss_connected()
    test_stub.ensure_bss_host_connected_from_sep_net_down(test_lib.scenario_file, test_lib.all_scenario_config, downMagt=False)
    test_stub.ensure_bss_connected()

    test_stub.return_pass_ahead_if_3sites("TEST PASS")
    vm = test_stub.create_basic_vm()
    vm.check()
    vm.destroy()

    test_util.test_pass('Create VM Test Success')

#Will be called what ever test result is
def env_recover():
    global pub_mn_ip
    global mag_mn_ip
    test_stub.reopen_host_network(mn_host[0], test_lib.all_scenario_config)
    test_stub.wait_for_mn_ha_ready(test_lib.all_scenario_config, test_lib.scenario_file)
    #test_stub.recover_host(mn_host[0], test_lib.all_scenario_config, test_lib.deploy_config)
    os.environ['ZSTACK_BUILT_IN_HTTP_SERVER_IP'] = pub_mn_ip

#Will be called only if exception happens in test().
def error_cleanup():
    global vm
    if vm:
        try:
            vm.destroy()
        except:
            pass
