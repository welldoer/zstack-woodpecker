import apibinding.api_actions as api_actions
import account_operations
import apibinding.inventory as inventory
import zstackwoodpecker.operations.resource_operations as res_ops
import net_operations as net_ops
import vm_operations as vm_ops


def create_vpc_vrouter(name, virtualrouter_offering_uuid, resource_uuid=None, system_tags=None, use_tags=None, session_uuid=None):
    action = api_actions.CreateVpcVRouterAction()
    action.timeout = 300000
    action.name = name
    action.virtualRouterOfferingUuid = virtualrouter_offering_uuid
    action.resourceUuid = resource_uuid
    action.systemTags = system_tags
    action.userTags = use_tags
    evt = account_operations.execute_action_with_session(action, session_uuid)
    return evt.inventory


def remove_all_vpc_vrouter():
    cond = res_ops.gen_query_conditions('applianceVmType', '=', 'vpcvrouter')
    vr_vm_list = res_ops.query_resource(res_ops.APPLIANCE_VM, cond)
    if vr_vm_list:
        for vr_vm in vr_vm_list:
            nic_uuid_list = [nic.uuid for nic in vr_vm.vmNics if nic.metaData == '4']
            for nic_uuid in nic_uuid_list:
                net_ops.detach_l3(nic_uuid)
            vm_ops.destroy_vm(vr_vm.uuid)
