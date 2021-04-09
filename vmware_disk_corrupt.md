vmware虚拟机 

“磁盘xxx.vmdk”出现一个或多个无法修复的内部错误。请通过该磁盘的备份副本进行恢复。
指定的虚拟磁盘需要进行修复

方法一：
    打开命令提示符cmd，进入到VMware安装路径
    如：cd C:\Program Files (x86)\VMware\VMware Workstation

    找到你需要修复的虚拟磁盘路径即虚拟机安装路径
    如：D:\虚拟机\04Windows Server 2003 Standard Edition\04Windows Server 2003 Standard Edition.vmdk

    执行修复命令
    vmware-vdiskmanager -R “虚拟磁盘路径”
    如：vmware-vdiskmanager -R “D:\虚拟机\04Windows Server 2003 Standard Edition\04Windows Server 2003 Standard Edition.vmdk”

但我执行失败：

    The vitual disk,'xxx.vmdk'，is corrupted and cannot be repaired.

此时已经有点绝望了。但也不能放弃，遂又搜了第二种办法

https://serverfault.com/questions/993860/how-to-repaire-a-vmdk-that-is-is-corrupted-and-cannot-be-repaired

    Try using vmware-vdiskmanager to repair the image.

    Since VMware already likely tried running this command on its own, this probably will not help, but it's the easiest thing to try.

    On macOS with VMware Fusion open terminal and change directory to /Applications/VMware Fusion.app/Contents/Library

    ./vmware-vdiskmanager -R /path/to/your_corrupted_disk.vmdk

    If you get a message saying that The virtual disk, '/path/to/your_corrupted_disk.vmdk', is corrupted and cannot be repaired. Try using StarWind V2V Converter on Windows to repair the disk.

    Download StarWind V2V Converter from https://www.starwindsoftware.com/starwind-v2v-converter, and install it on a Windows PC.
    Make a copy of your_corrupted_disk.vmdk along with all related .vmdks. (your_corrupted_disk-s001.vmdk, your_corrupted_disk-s002.vmdk, ...). Best to copy the whole parent directory.
    Use StarWind to convert it from a local vmdk to a local vmdk. It will flatten all your "*.vmdk" files into a single file
    Create a new virtual machine and select to "use an existing virtual disk" and point it to the fixed version.

下载工具StarWind V2V Converter

    