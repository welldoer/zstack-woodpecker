'''

Test about monitor trigger on one host cpu free ratio in five minutes

@author: Songtao,Haochen

'''

import os
import test_stub
import random
import time
import zstacklib.utils.ssh as ssh
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.operations.resource_operations as res_ops
import zstackwoodpecker.operations.monitor_operations as mon_ops

def test():
    global trigger
    global media
    global trigger_action

    test_item = "host.cpu.util"
    resource_type="HostVO"
    host_monitor_item = test_stub.get_monitor_item(resource_type)
    if test_item not in host_monitor_item:
        test_util.test_fail('%s is not available for monitor' % test_item)

    hosts = res_ops.get_resource(res_ops.HOST)
    host = hosts[0]
    duration = 300
    expression = "host.cpu.util{cpu=1,type=\"idle\"}<40.0"
    monitor_trigger = mon_ops.create_monitor_trigger(host.uuid, duration, expression)

    send_email = test_stub.create_email_media()
    media = send_email.uuid
    trigger_action_name = "trigger"+ ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(8)))
    trigger = monitor_trigger.uuid
    receive_email = os.environ.get('receive_email')
    monitor_trigger_action = mon_ops.create_email_monitor_trigger_action(trigger_action_name, send_email.uuid, trigger.split(), receive_email)
    trigger_action = monitor_trigger_action.uuid

    host.password = os.environ.get('hostPassword')
    ssh_cmd = test_stub.ssh_cmd_line(host.managementIp, host.username, host.password, port=int(host.sshPort))
    for i in range(4):test_stub.run_cpu_load(ssh_cmd, 1, 1)

    status_problem, status_ok = test_stub.query_trigger_in_loop(trigger,80)
    test_util.action_logger('Trigger old status: %s triggered. Trigger new status: %s recovered' % (status_problem, status_ok ))
    if status_problem != 1 or status_ok != 1:
        test_util.test_fail('%s Monitor Test failed, expected Problem or OK status not triggered' % test_item)

    mail_list = test_stub.receive_email()
    keywords = "fired"
    mail_flag = test_stub.check_email(mail_list, keywords, trigger, host.uuid)
    if mail_flag == 0:
        test_util.test_fail('Failed to Get Target: %s for: %s Trigger Mail' % (vm_uuid, test_item))

    mon_ops.delete_monitor_trigger_action(trigger_action)
    mon_ops.delete_monitor_trigger(trigger)
    mon_ops.delete_email_media(media)

def error_cleanup():
    global trigger
    global media
    global trigger_action
    mon_ops.delete_monitor_trigger_action(trigger_action)
    mon_ops.delete_monitor_trigger(trigger)
    mon_ops.delete_email_media(media)