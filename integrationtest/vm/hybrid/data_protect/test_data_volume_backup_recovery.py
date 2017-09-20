'''

New Integration Test for data protect under hybrid.

@author: Glody 
'''

import zstackwoodpecker.operations.hybrid_operations as hyb_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import zstackwoodpecker.operations.backupstorage_operations as bs_ops
import zstackwoodpecker.operations.image_operations as img_ops
import zstackwoodpecker.operations.volume_operations as vol_ops
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib

test_stub = test_lib.lib_get_test_stub()
dpbs_uuid = None
data_volume_uuid = None
image_uuid = None

def test():
    global dpbs_uuid
    global data_volume_uuid
    global image_uuid
    vm_res = hyb_ops.get_data_protect_image_store_vm_ip(test_lib.all_scenario_config, test_lib.scenario_file, test_lib.deploy_config)
    hostname = vm_res[0]
    url = vm_res[1]
    username = vm_res[2]
    password = vm_res[3]
    sshport = vm_res[4]
    name = "BS-public"
    data_protect_backup_storage = hyb_ops.add_disaster_image_store_bs(url, hostname, username, password, sshport, name)
    dpbs_uuid = data_protect_backup_storage.uuid 
    cond = res_ops.gen_query_conditions('resourceUuid', '=', dpbs_uuid)
    system_tag = res_ops.query_resource(res_ops.SYSTEM_TAG, cond)[0]
    if system_tag.tag != "remote":
        test_util.test_fail("Here isn't 'remote' system tag for data protect bs")
    zone = res_ops.query_resource(res_ops.ZONE)[0]
    bs_ops.attach_backup_storage(dpbs_uuid, zone.uuid)

    primary_storage_uuid = res_ops.query_resource(res_ops.PRIMARY_STORAGE)[0].uuid
    disk_offering_uuid = res_ops.query_resource(res_ops.DISK_OFFERING)[0].uuid
    cond = res_ops.gen_query_conditions('name', '=', 'image_store_bs')
    local_bs_uuid = res_ops.query_resource(res_ops.BACKUP_STORAGE, cond)[0].uuid

    volume_option = test_util.VolumeOption()
    volume_option.set_disk_offering_uuid(disk_offering_uuid)
    volume_option.set_name('data_volume_for_data_protect_test')
    volume_option.set_primary_storage_uuid(primary_storage_uuid)
    data_volume = vol_ops.create_volume_from_offering(volume_option)

    data_volume_uuid = data_volume.uuid 
    image_option = test_util.ImageOption()
    image_option.set_data_volume_uuid(data_volume_uuid)
    image_option.set_name('create_data_iso_to_image_store')
    image_option.set_backup_storage_uuid_list([dpbs_uuid])
    image = img_ops.create_data_volume_template(image_option)
    dpbs_image_uuid = image.uuid

    cond = res_ops.gen_query_conditions('uuid', '=', dpbs_image_uuid)
    media_type = res_ops.query_resource(res_ops.IMAGE, cond)[0].mediaType
    if media_type != 'DataVolumeTemplate':
        test_util.test_fail('Wrong image media type, the expect is "DataVolumeTemplate", the real is "%s"' %media_type) 

    cond = res_ops.gen_query_conditions('resourceUuid', '=', dpbs_image_uuid)
    system_tag = res_ops.query_resource(res_ops.SYSTEM_TAG, cond)[0]
    if system_tag.tag != "remote":
        test_util.test_fail("Here isn't 'remote' system tag for image in data protect bs")

    recovery_image = img_ops.recovery_image_from_image_store_backup_storage(local_bs_uuid, dpbs_uuid, dpbs_image_uuid) 
    if recovery_image.backupStorageRefs[0].backupStorageUuid != local_bs_uuid:
        test_util.test_fail('Recovery image failed, image uuid is %s' %recovery_image.uuid)
    if recovery_image.mediaType != 'DataVolumeTemplate':
        test_util.test_fail('Wrong image media type after recovery, the expect is "DataVolumeTemplate", the real is "%s"' %media_type)
    image_uuid = recovery_image.uuid

    try:
        #Try to recovery the same image again
        recovery_image = img_ops.recovery_image_from_image_store_backup_storage(local_bs_uuid, dpbs_uuid, dpbs_image_uuid)

    except Exception,e:
        if str(e).find('already contains it') != -1:
            test_util.test_pass('Try to recovery the same image again and get the error info expectly: %s' %str(e))
    finally: 
        vol_ops.delete_volume(data_volume_uuid)
        img_ops.delete_image(image_uuid)
        bs_ops.delete_backup_storage(dpbs_uuid) 
        pass
    test_util.test_fail('Try to recovery the same image second time success unexpectly')

#Will be called only if exception happens in test().
def error_cleanup():
    global dpbs_uuid
    global data_volume_uuid
    global image_uuid
    vol_ops.delete_volume(data_volume_uuid)
    img_ops.delete_image(image_uuid)
    if dpbs_uuid != None:
        bs_ops.delete_backup_storage(dpbs_uuid)
    
