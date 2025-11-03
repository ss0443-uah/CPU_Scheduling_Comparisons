# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 15:02:33 2025

@author: check
"""
from collections import deque
import heapq
class Process:
    def __init__(self, pid, priority, burst_time):
        self.pid = pid
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.nice = self.priority - 120
        self.weight = 1024 / (1.25 ** self.nice)
        self.vruntime =  (1024 / self.weight)
        self.start_time = None
        self.end_time = None
        
    def reset(self):
        self.remaining_time = self.burst_time
        self.vruntime = 0
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        return self.vruntime < other.vruntime



def run_cfs(process_list):
    current_time = 0
    gantt_chart = []
    ready_queue = []
    completed = []

    num_process = len(process_list)
    heapq.heapify(process_list)
    ready_queue = process_list
    print("\nInitial Ready Queue Order:")
    #for p in ready_queue:
        #print(f"PID {p.pid} | Nice {p.nice} | Weight {round(p.weight, 2)} | vruntime {p.vruntime}")
    #ready_queue = sorted(process_list, key=lambda p: calculate_weight(calculate_nice(p.priority)), reverse=True)
    #ready_queue = heapq.heapify(process_list)
    print("\n\nstarting CFS...")
    while ready_queue:
        time_slice=max(round(10/len(ready_queue)),1)
        process = heapq.heappop(ready_queue)
        #nice_value = calculate_nice(process.priority)
        #weight = calculate_weight(nice_value)
        #print(f"\n[Time {current_time}] Selected PID {process.pid} with vruntime {round(process.vruntime, 6)}")
        exec_time = min(time_slice, process.remaining_time)
        process.remaining_time -= exec_time
        process.vruntime += exec_time * (1024 / process.weight)

            # Track start and finish time
        if process.start_time is None:
            process.start_time = current_time
        current_time += exec_time
        gantt_chart.append((str(current_time-exec_time)+'--'+str(current_time), process.pid))

        if process.remaining_time == 0:
            process.end_time = current_time
            completed.append(process)
        else:
            heapq.heappush(ready_queue, process)

    # Print Gantt Chart
    print("\nCFS Gantt Chart :")
    for time, pid in gantt_chart:
        print(f"  PID {pid:>2}  |  {time:>3} ms")

    # Metrics
    total_turnaround = 0;
    total_waiting = 0;
    print("\nPerformance Metrics of CFS:")
    print(f"{'PID':<5}{'Start':<8}{'End':<8}{'Burst':<8}{'Waiting':<10}{'Turnaround':<12}")
    for p in sorted(completed, key=lambda x: x.pid):
        turnaround = p.end_time
        waiting = turnaround - p.burst_time
        total_turnaround += turnaround;
        total_waiting += waiting;
        print(f"{p.pid:<5}{p.start_time:<8}{p.end_time:<8}{p.burst_time:<8}{waiting:<10}{turnaround:<12}")
    Average_TAT = total_turnaround/num_process
    Average_WT = total_waiting/num_process
    print(f"Average Turn Around Time: {round(Average_TAT,2)}")
    print(f"Average Wait Time: {round(Average_WT,2)}")
    print(f"Context Switches: {len(gantt_chart)-1}")

def run_round_robin(process_list, time_slice=10):
    current_time = 0
    gantt_chart = []
    queue = deque()
    completed = []

    ready_queue = sorted(process_list, key=lambda p: p.pid)
    queue = deque(ready_queue)
    
    print("\n\nstarting classical RR...")
    track=1
    while queue:
        track += 1
        process = queue.popleft()

        # Track first start time
        if process.start_time is None:
            process.start_time = current_time

        exec_time = min(time_slice, process.remaining_time)
        process.remaining_time -= exec_time
        current_time += exec_time
        gantt_chart.append((str(current_time-exec_time)+'--'+str(current_time), process.pid))
        if process.remaining_time == 0:
            process.end_time = current_time
            completed.append(process)
        else:
            queue.append(process)
            

    # Print Gantt Chart
    print("\n Classical RR Gantt Chart:")
    for time, pid in gantt_chart:
        print(f"  PID {pid:>2}  |  {time:>3} ms")

    # Metrics
    total_turnaround = 0;
    total_waiting = 0;
    print("\nPerformance Metrics of Classical RR:")
    print(f"{'PID':<5}{'Start':<8}{'End':<8}{'Burst':<8}{'Waiting':<10}{'Turnaround':<12}")
    for p in sorted(completed, key=lambda x: x.pid):
        turnaround = p.end_time
        waiting = turnaround - p.burst_time
        total_turnaround += turnaround;
        total_waiting += waiting;
        print(f"{p.pid:<5}{p.start_time:<8}{p.end_time:<8}{p.burst_time:<8}{waiting:<10}{turnaround:<12}")
    Average_TAT = total_turnaround/len(process_list)
    Average_WT = total_waiting/len(process_list)
    print(f"Average Turn Around Time: {round(Average_TAT,2)}")
    print(f"Average Wait Time: {round(Average_WT,2)}")
    print(f"Context Switches: {len(gantt_chart)-1}")
    
def run_modified_round_robin(process_list, time_slice=10):
    current_time = 0
    gantt_chart = []
    queue = deque()
    completed = []
    
    print("\n\nstarting modified RR...")
    track_loop = 0
    time_track = 1
    track=0
    ready_queue = sorted(process_list, key=lambda p: p.pid)
    queue = deque(ready_queue)
    #print(len(queue))
    n = len(ready_queue)
    while queue:
        #print("queue len:"+str(len(queue)))
        #print(track_loop)
        if (track_loop == n):
            updated_queue = sorted(queue, key=lambda p: p.remaining_time)
            queue = deque(updated_queue)
            n = len(queue)
            track_loop = 1
            time_track = 2
            track=1
        elif (track==1) & (track_loop == n):
            updated_queue = sorted(queue, key=lambda p: p.remaining_time)
            queue = deque(updated_queue)
            n = len(queue)
            track_loop = 1
            #print("i am here in 1")
        else:
            track_loop += 1
        process = queue.popleft()
        #print(process.pid, process.remaining_time, time_track)

        if process.start_time is None:
            process.start_time = current_time

        exec_time = min(time_track*time_slice, process.remaining_time)
        process.remaining_time -= exec_time
        current_time += exec_time
        gantt_chart.append((str(current_time-exec_time)+'--'+str(current_time), process.pid))
        if process.remaining_time == 0:
            process.end_time = current_time
            completed.append(process)
        else:
            queue.append(process)
            
        

    # Print Gantt Chart
    print("\n Modified RR Gantt Chart:")
    for time, pid in gantt_chart:
        print(f"  PID {pid:>2}  |  {time:>3} ms")

    # Metrics
    total_turnaround = 0;
    total_waiting = 0;
    print("\nPerformance Metrics of Modified RR:")
    print(f"{'PID':<5}{'Start':<8}{'End':<8}{'Burst':<8}{'Waiting':<10}{'Turnaround':<12}")
    for p in sorted(completed, key=lambda x: x.pid):
        turnaround = p.end_time
        waiting = turnaround - p.burst_time
        total_turnaround += turnaround;
        total_waiting += waiting;
        print(f"{p.pid:<5}{p.start_time:<8}{p.end_time:<8}{p.burst_time:<8}{waiting:<10}{turnaround:<12}")
    Average_TAT = total_turnaround/len(process_list)
    Average_WT = total_waiting/len(process_list)
    print(f"Average Turn Around Time: {round(Average_TAT,2)}")
    print(f"Average Wait Time: {round(Average_WT,2)}")
    print(f"Context Switches: {len(gantt_chart)-1}")

def reset_process(process_list):
    for item in process_list:
        item.reset()    



processes = [
    Process(1, 120, 8),
    Process(2, 115, 5),
    Process(3, 130, 30),
    Process(4, 100, 9),
    Process(5, 120, 27),
    Process(6, 108, 115),
    Process(7, 136, 7),
    Process(8, 100, 2),
    Process(9, 110, 18),
    Process(10, 125, 34),
]
"""
processes = [
    Process(1, 120, 8),
    Process(2, 115, 12),
    Process(3, 130, 18),
    Process(4, 100, 19),
    Process(5, 120, 27),
    Process(6, 108, 38),
    Process(7, 136, 50),
    Process(8, 100, 31),
    Process(9, 110, 18),
    Process(10, 125, 14),
]
"""
run_cfs(processes)
processes = [
    Process(1, 120, 8),
    Process(2, 115, 5),
    Process(3, 130, 30),
    Process(4, 100, 9),
    Process(5, 120, 27),
    Process(6, 108, 115),
    Process(7, 136, 7),
    Process(8, 100, 2),
    Process(9, 110, 18),
    Process(10, 125, 34),
]
"""
processes = [
    Process(1, 120, 8),
    Process(2, 115, 12),
    Process(3, 130, 18),
    Process(4, 100, 19),
    Process(5, 120, 27),
    Process(6, 108, 38),
    Process(7, 136, 50),
    Process(8, 100, 31),
    Process(9, 110, 18),
    Process(10, 125, 14),
]
"""
run_round_robin(processes)
reset_process(processes)
run_modified_round_robin(processes)