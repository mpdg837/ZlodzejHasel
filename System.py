import psutil
import platform
import subprocess
import re
import uuid
import os
import socket

# Check public ip using CLI
# (Invoke-WebRequest ifconfig.me/ip).Content.Trim()
# nslookup myip.opendns.com resolver1.opendns.com

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def info():
    begining = dict()
    set = []
    if 1 == 1:
        # general details
        uname = platform.uname()
        # traverse the info
        Id = subprocess.Popen(['systeminfo'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
        line = []
        new = []

        ip = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[1][4][0]
        begining = dict(type="user_data", ipv6=ip, system = uname.system, name = uname.node,
                          relase = uname.release, version = uname.version, machine = uname.machine,
                          processor = uname.processor,data = set)

        cpufreq = psutil.cpu_freq()
        # let's f.write CPU information
        dictionary = dict(type="cpu", phy_cores=psutil.cpu_count(logical=False), tot_cores=psutil.cpu_count(logical=True),
                          mhz_max_freq=cpufreq.max, mhz_min_freq=cpufreq.min, mhz_current_freq=cpufreq.current)

        set.append(dictionary)


        # Memory Information
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        dictionary = dict(type="mem", total=get_size(svmem.total),
                          total_swap=get_size(swap.total))

        set.append(dictionary)

        # Disk Information
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue

            dictionary = dict(type="disk", mountpoint=partition.mountpoint,
                              file_system=partition.fstype, size =get_size(partition_usage.total), size_used = get_size(partition_usage.used))

            set.append(dictionary)


        # Network information
        # get all network interfaces (virtual and physical)
        dictionary = dict(type="mac_addr", mac_addr=re.findall('..', '%012x' % uuid.getnode()))
        set.append(dictionary)

        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    dictionary = dict(type="ip_interface", ip = address.address, netmask = address.netmask,
                                      broadcast = address.broadcast)
                    set.append(dictionary)
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    dictionary = dict(type="interface", mac=address.address, netmask=address.netmask,
                                      broadcast=address.broadcast)
                    set.append(dictionary)


    return begining