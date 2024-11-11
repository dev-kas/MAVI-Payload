import platform
import psutil
import uuid
import os
import re

###################{ FORMAT }#################
# (
#     os: string,
#     arch: string,
#     name: string,
#     scrRes: string,
#     deviceType: "desktop" | "mobile" | "tablet" | "laptop",
#     deviceUUID: string,
#     ram: number, // bytes
#     isVM: boolean
# )
# 

def is_running_in_vm():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    vm_processes = ['vmware', 'virtualbox', 'qemu', 'kvm']
    for proc in psutil.process_iter(['name']):
        if any(vm in proc.info['name'].lower() for vm in vm_processes):
            return True

    if 'hyperv' in platform.uname().release.lower():
        return True

    if any('vda' in part.device for part in psutil.disk_partitions()):
        return True
    
    return False

def get_info():
    info = {}

    info["os"] = platform.system()
    info["arch"] = platform.architecture()[0]
    info["name"] = platform.node()
    info["scrRes"] = f"123x456" # TODO: Add screen resolution
    info["deviceType"] = "desktop" if re.search(r"desktop", platform.system().lower()) else "mobile" if re.search(r"mobile" , platform.system().lower()) else "tablet" if re.search(r"tablet", platform.system().lower()) else "laptop"
    info["deviceUUID"] = f"asjkdbkbasda aiusdh aysdga" # TODO: Add device UUID
    info["ram"] = psutil.virtual_memory().total
    info["isVM"] = is_running_in_vm()

    return info
