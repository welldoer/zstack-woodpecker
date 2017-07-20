package org.zstack.header.volume

import org.zstack.header.errorcode.ErrorCode

doc {

	title "云盘清单"

	ref {
		name "error"
		path "org.zstack.header.volume.APICreateDataVolumeFromVolumeTemplateEvent.error"
		desc "错误码，若不为null，则表示操作失败, 操作成功时该字段为null",false
		type "ErrorCode"
		since "0.6"
		clz ErrorCode.class
	}
	ref {
		name "inventory"
		path "org.zstack.header.volume.APICreateDataVolumeFromVolumeTemplateEvent.inventory"
		desc "创建出的云盘清单"
		type "VolumeInventory"
		since "0.6"
		clz VolumeInventory.class
	}
}