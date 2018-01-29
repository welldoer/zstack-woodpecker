'''

Create a VM with vlan L3 network and a data volume offering.

Test step:
    1. Select Data VolumeOffering, select l3Network that makes its VR only has DNS and DHCP services to create a VM and record the vm and its state in vm_dict
    2. Check:
        1). Assign an IP address for host vlan device:
            config an IP address(next_avail_ip) to vm's host L2 bridge dev with IP: next_avail_ip
            (Test netmask is assume to be 255.255.0.0/255.255.255.0. 
            The reason is test case will use 
             x.y.0.1~x.y.127.255/x.y.z.2~x.y.z.232 for VM IP assignment; 
             x.y.128.1~x.y.255.254/x.y.z.233~x.y.z.254 for hosts L2 bridge dev IP assignment.)
            so next_avail_ip:
              net_address = pri_l3_ip_ranges.startIp
              if netmask == "255.255.0.0":
                the last two digits of net_address == the last two digits of host.ip
                and the 3rd digit should >=128, if not, this digit plus 128
              if netmask == "255.255.255.0":
                modify the last digit of net_address to digit in range(233, 254), after modified, the net_address should not in pri_l3_ip_ranges
        2). Check kvm vm running status:
            post http request(get vm_status) to back-end
        3). Check kvm vm network connection status -- whether VM's network is reachable:
            ssh host to ping vm ip(ping -c 5 -W 5 vm.ip), we expect it to be successful
        4). Check kvm vm dhcp status -- whether VM's dhcp is set correctly:
            check vm DHCP binding setting in VR: ssh vr, execute the command(/bin/cli-shell-api showCfg), vm nic.mac should in the command result
            check VM DHCP in VM: ssh vm, execute the command(/sbin/ip a), vm ip should in the command result
        5). Check kvm vm dns status -- whether VM's dns is set correctly:
            ssh vm, execute the command(cat /etc/resolv.conf), vr's private ip should in the command result
        6). QueryVmInstance to get vm state in database and check the synchronizationstate of vm state in vm_dict and database
    3. the vm should have two volumes, check it
    4. Destroy VM

@author: Youyk
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import os

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()

def test():
    global test_obj_dict
    test_util.test_dsc('Create test vm and check. VR only has DNS and DHCP services')
    vm = test_stub.create_vlan_vm_with_volume(os.environ.get('l3VlanNetworkName1'))
    test_obj_dict.add_vm(vm)
    vm.check()
    volumes_number = len(test_lib.lib_get_all_volumes(vm.vm))
    if volumes_number != 2:
        test_util.test_fail('Did not find 2 volumes for [vm:] %s. But we assigned 1 data volume when create the vm. We only catch %s volumes' % (vm.vm.uuid, volumes_number))
    else:
        test_util.test_logger('Find 2 volumes for [vm:] %s.' % vm.vm.uuid)

    vm.destroy()
    test_util.test_pass('Create VirtualRouter VM DNS DHCP Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    test_lib.lib_error_cleanup(test_obj_dict)
