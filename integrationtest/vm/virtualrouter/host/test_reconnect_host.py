'''
This case can not execute parallelly
@author: Youyk
'''
import os
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.host_operations as host_ops
import zstackwoodpecker.operations.resource_operations as res_ops

_config_ = {
        'timeout' : 1000,
        'noparallel' : True
        }

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()

#custom function
#compare availableCpu/totalCpu/availableMemory/totalMemory 
def compare_capacity(res1, res2, cpu_free = 0, memory_free = 0):
    if res1.availableCpu != res2.availableCpu - cpu_free:
        test_util.test_logger('available CPU are different. res1: %s, res2: %s\
                ' % (res1.availableCpu, res2.availableCpu))
        return False

    if res1.totalCpu != res2.totalCpu:
        test_util.test_logger('total CPU are different. res1: %s, res2: %s\
                ' % (res1.totalCpu, res2.totalCpu))
        return False

    if res1.availableMemory != res2.availableMemory - memory_free:
        test_util.test_logger('available Memory are different. res1: %s, res2: %s\
                ' % (res1.availableMemory, res2.availableMemory))
        return False

    if res1.totalMemory != res2.totalMemory:
        test_util.test_logger('available Memory are different. res1: %s, res2: %s\
                ' % (res1.totalMemory, res2.totalMemory))
        return False

    return True

def test():
    #print test description and write this message to action log
    test_util.test_dsc('Test Host Reconnect function and check if the available CPU and memory number are aligned between before and after reconnect action')
    #get the value of the environment variable(l3VlanNetworkName1), use this value as a parameter to create a vm and add it to dict
    vm = test_stub.create_vlan_vm(os.environ.get('l3VlanNetworkName1'))
    test_obj_dict.add_vm(vm)

    #get vm's zoneUuid
    zone_uuid = vm.get_vm().zoneUuid
    #get vm's host inventory
    host = test_lib.lib_get_vm_host(vm.get_vm())
    #get hostUuid
    host_uuid = host.uuid

    #get the number of cpu and memory capacity in the zone
    tot_res1 = test_lib.lib_get_cpu_memory_capacity([zone_uuid])
    
    #reconnect host
    host_ops.reconnect_host(host_uuid)

    #after host reconnected, get the number of cpu and memory capacity in the zone
    tot_res2 = test_lib.lib_get_cpu_memory_capacity([zone_uuid])
    
    #call the custom function -- compare_capacity
    #to compare the cpu and memory consumption before and after the host reconnected
    #same: print msg, record test log; 
    #otherwise: record test log and test result, throw exception
    if compare_capacity( tot_res1, tot_res2):
        test_util.test_logger("the resource consumption are same after reconnect host")
    else:
        test_util.test_fail("the resource consumption are different after reconnect host: %s " % host_uuid)
    
    #get vm's instanceOfferingUuid
    vm_offering_uuid = vm.get_vm().instanceOfferingUuid
    #generate query conditions:uuid = vm_offering_uuid
    cond = res_ops.gen_query_conditions('uuid', '=', vm_offering_uuid)
    #QueryInstanceOffering with conditions, return instanceoffering inventory
    vm_offering = res_ops.query_resource(res_ops.INSTANCE_OFFERING, cond)[0]
    #get cpuNum,memorySize which defined by the instanceoffering
    vm_cpu = vm_offering.cpuNum
    vm_memory = vm_offering.memorySize
    
    #destroy vm
    vm.destroy()
    #remove vm from vm_dict[Running] and add it to vm_dict[Destroyed]
    test_obj_dict.rm_vm(vm)

    #after vm destroyed, get the number of cpu and memory capacity in the zone
    tot_res3 = test_lib.lib_get_cpu_memory_capacity([zone_uuid])
    
    #call the custom function -- compare_capacity
    #to compare the cpu and memory consumption before and after the vm destroyed
    #same: print msg, record test log; 
    #otherwise: record test log and test result, throw exception
    if compare_capacity(tot_res1, tot_res3, vm_cpu, vm_memory):
        test_util.test_logger("the resource consumption are aligned after destroy a vm")
    else:
        test_util.test_fail("the resource consumption are not aligned after destroy vm: %s on host: %s" % (vm.get_vm().uuid, host_uuid))

    #re-create vm and add it to dict
    vm = test_stub.create_vlan_vm(os.environ.get('l3VlanNetworkName1'))
    test_obj_dict.add_vm(vm)

    #after vm re-created, get the number of cpu and memory capacity in the zone
    tot_res4 = test_lib.lib_get_cpu_memory_capacity([zone_uuid])

    #call the custom function -- compare_capacity
    #to compare the cpu and memory consumption before and after the vm re-created
    #same: print msg, record test log; 
    #otherwise: record test log and test result, throw exception
    if compare_capacity(tot_res1, tot_res4):
        test_util.test_logger("the resource consumption are aligned after create a new vm")
    else:
        test_util.test_fail("the resource consumption are not aligned after create a new vm: %s " % vm.get_vm().uuid)

    #destroy vm
    vm.destroy()

    #test pass:print msg,record test log and test result
    test_util.test_pass('Reconnect Host and Test CPU/Memory Capacity Pass')

#Will be called only if exception happens in test().
def error_cleanup():
    #clean up the environment when error occurred
    test_lib.lib_error_cleanup(test_obj_dict)
