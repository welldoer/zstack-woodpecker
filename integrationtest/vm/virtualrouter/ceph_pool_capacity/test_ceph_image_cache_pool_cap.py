'''

New Integration Test for Ceph Pool Capacity.

@author: Legion
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import time

test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()
pool_cap = test_stub.PoolCapacity()


def test():
    pool_cap.create_vm()
    pool_cap.add_image(name=test_stub.CEPHPOOLTESTISONAME, 
                       bs_type='ImageStoreBackupStorage', image_format='iso', 
                       media_type='ISO', image='testIsoUrl')
    test_obj_dict.add_vm(pool_cap.vm)
    pool_cap.attach_iso()
    time.sleep(200)
    pool_cap.get_ceph_pool('ImageCache')
    used1 = pool_cap.pool.usedCapacity
    avail1 = pool_cap.pool.availableCapacity
    pool_name = pool_cap.pool.poolName
    pool_cap.check_pool_cap([used1, avail1], pool_name=pool_name)
    test_util.test_pass('Ceph Image Pool Capacity Test Success')


#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    test_lib.lib_error_cleanup(test_obj_dict)
