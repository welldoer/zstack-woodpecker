'''

@author: Frank
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()

def test():
    global test_obj_dict
    #print test description and write this message to action log
    test_util.test_dsc('Create test vm and check')
    #create user_vlan_vm
    vm = test_stub.create_user_vlan_vm()
    #add vm to vm_dict[Running]
    test_obj_dict.add_vm(vm)
    #check vm state
    #check_vm_db,check_kvm_vm_running,check_kvm_vm_snat,check_kvm_vm_dhcp,check_kvm_vm_network,check_kvm_vm_set_host_vlan_ip,check_kvm_vm_dns
    vm.check()
    
    #destroy vm
    vm.destroy()
    #test pass:print msg, record test log and test result
    test_util.test_pass('Create VirtualRouter VM Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    #clean up the environment when error occurred
    test_lib.lib_error_cleanup(test_obj_dict)
