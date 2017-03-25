# -*- coding:utf-8 -*-

import affinity

class BindingCpu(object):
    '''
               1 means cpu enable
    CPUID           mask(value)     binary number
    1               1               0000000000000001
    2               2               0000000000000010
    3               4               0000000000000100
    4               8               0000000000001000
    5               16              0000000000010000
    6               32              0000000000100000
    7               64              0000000001000000
    8               128             0000000010000000
    9               256             0000000100000000
    10              512             0000001000000000
    11              1024            0000010000000000
    12              2048            0000100000000000
    13              4096            0001000000000000
    14              8192            0010000000000000
    15              16384           0100000000000000
    16              32768           1000000000000000
    all cpu         65535           1111111111111111
    '''
    def __init__(self,started_process,cpuId):
        """
        :param started_process: process waiting to bing
        :type <class 'multiprocessing.process.Process'>
        :param cpuId: which cpu do you want to bind
        :type int
        """
        self.p = started_process
        self.p_name = self.p.name
        self.p_pid = self.p.pid
        self.cpuId = cpuId

    @classmethod
    def get_cpu_usage(cls, cpuId):
        '''
        I want to check cpu utilization before binding to it
        :param cpuId: which cpu do you want to bind
        :type int
        :return eg:
            cpu_usage={'cpu1':0.1,
                       'cpu2':0.2,
                       'cpu3':0.3}
        '''
        cpu_usage={}
        return cpu_usage

    @classmethod
    def affinity_cpu(cls, started_process, cpuId):
        if cpuId > 0:
            p_name = started_process.name
            p_pid = started_process.pid
#             cpuId_usage = cls.get_cpu_usage(cpuId)
#             if cpuId_usage(balabala) > 0.8:
#                 print "cpu utilization is %r, more than 80%, \
#                 better binding process %r (pid %r) to another cpu " %(cpuId_usage, p_pid, bin(cpuId))
            affinity.set_process_affinity_mask(p_pid, cpuId)
            print "process: %r (pid %r) is running on processor(after binding) : %r" %(p_name, p_pid, bin(cpuId))
        else:
            print "process: %r (pid %r) could not set CPU affinity(%r), continuing..." % (p_name, p_pid, bin(cpuId))


