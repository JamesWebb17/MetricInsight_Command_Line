""" @package Memory
Documentation for GPU module.

More details.
Function for calculating the GPU charge.
"""

import time

import shared.flags
from Read_File.PID.gpu import GPU
from shared import Result, flags


def utilisation_gpu(frequency, interval, result):
    """
    Find the Memory usage of a process in files /proc/[pid]/statm and /proc/uptime.
    :param frequency: frequency of the points
    :param interval: interval of time wanted
    :param result: array for sending the result to the main thread
    :return: status of the function
    """

    start = time.clock_gettime(time.CLOCK_REALTIME)
    now = 0

    process_info = GPU()

    list_gpu = []
    list_temps = []

    while process_info.read() != -1 and now - start < interval and shared.flags.THREAD_CPU_END_FLAG is False and shared.flags.THREAD_MEM_END_FLAG is False:
        now = time.clock_gettime(time.CLOCK_REALTIME)

        list_gpu.append(process_info.load/10)
        list_temps.append(now - start)

        time.sleep(1 / frequency)

    result.append(Result("GPU", "Utilisation GPU (%)", [list_temps, list_gpu]))
    flags.THREAD_GPU_END_FLAG = True
    return 0
