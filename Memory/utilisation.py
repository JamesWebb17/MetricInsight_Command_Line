import matplotlib.pyplot as plt
import time

from Read_File import Statm, Uptime
from shared import locking, Result


def calcul_utilisation_mem(statm, uptime, clock_ticks_per_second):
    process_size = statm.size
    process_resident = statm.resident
    process_share = statm.share
    process_start_sec = statm.starttime / clock_ticks_per_second

    system_uptime_sec = uptime.total_time

    process_elapsed_sec = system_uptime_sec - process_start_sec
    process_mem_usage = 100 * ((process_size + process_resident + process_share) / process_elapsed_sec)

    return process_mem_usage


def plot_mem_usage(mem_usage_list, time_list):
    with locking.lock:
        plt.figure()
        plt.plot(time_list, mem_usage_list)
        plt.xlabel("Temps (s)")
        plt.ylabel("Utilisation de la mémoire (%)")
        plt.show()


def store_mem_usage(mem_usage_list, time_list, pid):
    with locking.lock:
        plt.figure()
        plt.plot(time_list, mem_usage_list)
        plt.xlabel("Temps (s)")
        plt.ylabel("Utilisation de la mémoire (%)")
        plt.savefig(f"MEM_{pid}.png")
        plt.close()


def utilisation_mem(pid, frequence, nbre_points, result):
    process_info = Statm(pid)
    uptime_info = Uptime()

    list_mem = []
    list_temps = []
    compt = 0
    while compt < nbre_points:

        process_info.read_proc_statm()
        uptime_info.read_proc_uptime()

        list_mem.append(process_info.size)
        list_temps.append(compt*frequence)
        compt += 1

        time.sleep(frequence)

    result.append(Result("MEM",  "Utilisation mémoire (mB)", [list_temps, list_mem]))
    #store_mem_usage(list_mem, list_temps,pid)