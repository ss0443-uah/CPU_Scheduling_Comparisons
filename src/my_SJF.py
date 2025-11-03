# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 16:39:54 2025

@author: check
"""
from collections import deque
class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.predicted_burst = 0  # For burst prediction
        self.vruntime = 0
        self.start_time = None
        self.end_time = None

    def reset(self):
        self.remaining_time = self.burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        return self.predicted_burst < other.predicted_burst
    
def sjf_with_prediction(process_list, alpha):
    time = 0
    completed = []
    gantt_chart = []
    ready_queue = deque(process_list)
    track=0
    for process in ready_queue:
        if track == 0:
            process.predicted_burst = 5
        else:
            process.predicted_burst = round(alpha * ready_queue[track-1].burst_time + (1 - alpha) * ready_queue[track-1].predicted_burst)
        track += 1
    updated_queue = deque(sorted(ready_queue, key=lambda p: p.predicted_burst))
    while updated_queue:
        current = updated_queue.popleft()

        current.start_time = time
        current.end_time = time + current.burst_time
        gantt_chart.append((current.pid, str(current.start_time)+'--'+str(current.end_time)))

        time += current.burst_time
        completed.append(current)

    print("\nSJF Gantt Chart :")
    for pid, time in gantt_chart:
        print(f"  PID {pid:>2}  |  {time:>3} ms")
    
    # Metrics
    total_turnaround = 0;
    total_waiting = 0;
    print("\nPerformance Metrics of CFS:")
    print(f"{'PID':<5}{'Start':<8}{'End':<8}{'Burst':<8}{'Predicted_Burst':<18}{'Waiting':<10}{'Turnaround':<12}")
    for p in sorted(completed, key=lambda x: x.pid):
        turnaround = p.end_time
        waiting = turnaround - p.burst_time
        total_turnaround += turnaround;
        total_waiting += waiting;
        print(f"{p.pid:<5}{p.start_time:<8}{p.end_time:<8}{p.burst_time:<8}{p.predicted_burst:<18}{waiting:<10}{turnaround:<12}")
    Average_TAT = total_turnaround/len(process_list)
    Average_WT = total_waiting/len(process_list)
    print(f"Average Turn Around Time: {round(Average_TAT,2)}")
    print(f"Average Wait Time: {round(Average_WT,2)}")
    print(f"Context Switches: {len(gantt_chart)-1}")
        

"""   
processes = [
    Process(1, 8),
    Process(2, 5),
    Process(3, 30),
    Process(4, 9),
    Process(5, 27),
    Process(6, 115),
    Process(7, 7),
    Process(8, 2),
    Process(9, 18),
    Process(10, 34),
]
"""
processes = [
    Process(1, 8),
    Process(2, 12),
    Process(3, 18),
    Process(4, 19),
    Process(5, 27),
    Process(6, 38),
    Process(7, 50),
    Process(8, 31),
    Process(9, 18),
    Process(10, 14),
]
sjf_with_prediction(processes, alpha=0.8)


