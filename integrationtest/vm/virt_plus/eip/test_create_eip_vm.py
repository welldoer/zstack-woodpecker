'''

Test create EIP for a VM. 

Test step:
    1. Create a VM
    2. Create a EIP with VM's nic
    3. Check the EIP connectibility
    4. Destroy VM

@author: quarkonics
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import os

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()

def test():
    #print test description and write this message to action log
    test_util.test_dsc('Create test vm with EIP and check.')
    #get the value of the environment variable,use this value as a parameter to create a vm
    vm = test_stub.create_vlan_vm(os.environ.get('l3VlanNetworkName1'))
    #add vm to dict
    test_obj_dict.add_vm(vm)
    
    #get the value of environment variable(l3VlanNetworkName1) and its uuid
    pri_l3_name = os.environ.get('l3VlanNetworkName1')
    pri_l3_uuid = test_lib.lib_get_l3_by_name(pri_l3_name).uuid

    #get the value of environment variable(l3PublicNetworkName) and its uuid
    pub_l3_name = os.environ.get('l3PublicNetworkName')
    pub_l3_uuid = test_lib.lib_get_l3_by_name(pub_l3_name).uuid

    #get vmNics inventory and vmNics uuid 
    vm_nic = vm.vm.vmNics[0]
    vm_nic_uuid = vm_nic.uuid
    #specify network to create vip and add it to dict
    vip = test_stub.create_vip('create_eip_test', pub_l3_uuid)
    test_obj_dict.add_vip(vip)
    #create eip:specify network and attach eip to vm
    eip = test_stub.create_eip('create eip test', vip_uuid=vip.get_vip().uuid, vnic_uuid=vm_nic_uuid, vm_obj=vm)
    
    #after eip is create, set vip state and network service
    vip.attach_eip(eip)
    
    #check vm state
    vm.check()
    #test vm ping vip.ip
    #if ping failed, record test log and test result, throw exception
    if not test_lib.lib_check_directly_ping(vip.get_vip().ip):
        test_util.test_fail('expected to be able to ping vip while it fail')
    #ping successed, destroy vm
    vm.destroy()
    test_obj_dict.rm_vm(vm)
    #ping vip.ip
    #if ping successed, record test log and test result, throw exception
    if test_lib.lib_check_directly_ping(vip.get_vip().ip):
        test_util.test_fail('not expected to be able to ping vip while it succeed')

    #cleanup
    eip.delete()
    vip.delete()

    test_obj_dict.rm_vip(vip)
    #test pass:print msg, record test log and test result
    test_util.test_pass('Create EIP for VM Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    #clean up the environment when error occurred
    test_lib.lib_error_cleanup(test_obj_dict)
