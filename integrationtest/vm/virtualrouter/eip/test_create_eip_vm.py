'''

Test create EIP for a VM. 

Test step:
    1. Create a VM
    2. Create a EIP with VM's nic
    3. Check the EIP connectibility
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
    #print test description and write this message to action log
    test_util.test_dsc('Create test vm with EIP and check.')
    #get the value of the environment variable, use this value as a parameter to create a vm
    vm = test_stub.create_vlan_vm(os.environ.get('l3VlanNetworkName1'))
    #add vm to dict
    test_obj_dict.add_vm(vm)
    
    #get the value of environment variable(l3VlanNetworkName1)
    l3_name = os.environ.get('l3VlanNetworkName1')
    #get l3network uuid
    vr1_l3_uuid = test_lib.lib_get_l3_by_name(l3_name).uuid
    #get vrs, which has vnic belongs to vr1_l3_uuid
    vrs = test_lib.lib_find_vr_by_l3_uuid(vr1_l3_uuid)
    temp_vm1 = None
    #if vrs does not exist
    #create temp_vm1 for getting vlan1's vr
    #otherwise get a vr
    if not vrs:
        #create temp_vm1 for getting vlan1's vr for test pf_vm portforwarding
        temp_vm1 = test_stub.create_vlan_vm()
        test_obj_dict.add_vm(temp_vm1)
        vr1 = test_lib.lib_find_vr_by_vm(temp_vm1.vm)[0]
    else:
        vr1 = vrs[0]

    #get the value of environment variable(l3NoVlanNetworkName1)
    l3_name = os.environ.get('l3NoVlanNetworkName1')
    #get l3network uuid
    vr2_l3_uuid = test_lib.lib_get_l3_by_name(l3_name).uuid
    #get vrs, which has vnic belongs to vr2_l3_uuid
    vrs = test_lib.lib_find_vr_by_l3_uuid(vr2_l3_uuid)
    temp_vm2 = None
    #if vrs does not exist
    #create temp_vm2 for getting novlan's vr
    #otherwise get a vr
    if not vrs:
        #create temp_vm2 for getting novlan's vr for test pf_vm portforwarding
        temp_vm2 = test_stub.create_user_vlan_vm()
        test_obj_dict.add_vm(temp_vm2)
        vr2 = test_lib.lib_find_vr_by_vm(temp_vm2.vm)[0]
    else:
        vr2 = vrs[0]

    #we do not need temp_vm1 and temp_vm2, since we just use their VRs.
    #so destroy vm and deal with the corresponding dict
    if temp_vm1:
        temp_vm1.destroy()
        test_obj_dict.rm_vm(temp_vm1)
    if temp_vm2:
        temp_vm2.destroy()
        test_obj_dict.rm_vm(temp_vm2)

    #get vmNics inventory and vmNics uuid 
    vm_nic = vm.vm.vmNics[0]
    vm_nic_uuid = vm_nic.uuid
    #get vm's private l3NetworkUuid 
    pri_l3_uuid = vm_nic.l3NetworkUuid
    #get a vr, which has vnic belongs to vm's private l3NetworkUuid
    vr = test_lib.lib_find_vr_by_l3_uuid(pri_l3_uuid)[0]
    #get vr's public nic
    vr_pub_nic = test_lib.lib_find_vr_pub_nic(vr)
    #get vr's public l3NetworkUuid
    l3_uuid = vr_pub_nic.l3NetworkUuid
    #specify network to create vip and add it to dict
    vip = test_stub.create_vip('create_eip_test', l3_uuid)
    test_obj_dict.add_vip(vip)
    #create eip:specify network and attach eip to vm
    eip = test_stub.create_eip('create eip test', vip_uuid=vip.get_vip().uuid, vnic_uuid=vm_nic_uuid, vm_obj=vm)
    
    #after eip is create, set vip state and network service
    vip.attach_eip(eip)
    
    #cleanup
    vm.check()
    vip.check()
    vm.destroy()
    test_obj_dict.rm_vm(vm)
    vip.check()
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
