from math import exp 
from parse import read_input_file, write_output_file
import os
from tqdm import tqdm

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    dp = [[[0 for _ in range(1441)] for _ in range(len(tasks) + 1)] for _ in range(len(tasks) + 1)]

    for s in tqdm(range(1, len(tasks) + 1)):
        for i in range(1, len(tasks) + 2 - s):
            for t in range(1, 1441):
                for k in range(i, i + s - 1):
                    current_task = tasks[k - 1]
                    current_duration = current_task.duration
                    time_before_task = t - current_task.duration
                    if time_before_task >= 0 and t <= current_task.deadline:
                        dp[i][i + s - 1][t] = max(dp[i][i + s - 1][t], 
                                              max(dp[i][k][t - current_duration], dp[k + 1][i + s - 1][t - current_duration]) + current_task.perfect_benefit)
                    else:
                        dp[i][i + s - 1][t] = dp[i][i + s - 1][t - 1]
    return dp
    # dp = [[[0 for _ in range(1441)] for _ in range(len(tasks) + 1)] for _ in range(len(tasks) + 1)]

    # for s in tqdm(range(1, len(tasks) + 1)):
    #     for i in range(1, len(tasks) + 2 - s):
    #         for t in range(1, 1441):
    #             for k in range(i, i + s - 1):
    #                 current_task = tasks[k - 1]
    #                 current_duration = current_task.duration
    #                 time_before_task = t - current_task.duration
    #                 if time_before_task >= 0 and t <= current_task.deadline:
    #                     dp[i][i + s - 1][t] = max(dp[i][i + s - 1][t], 
    #                                           max(dp[i][k][t - current_duration], dp[k + 1][i + s - 1][t - current_duration]) + current_task.perfect_benefit)
    #                 else:
    #                     dp[i][i + s - 1][t] = dp[i][i + s - 1][t - 1]
    


def ratio(tasks):
    # sort by profit/time ratio, decreasing
    tasks.sort(key=lambda t: -t.perfect_benefit / t.duration)
    # print(*tasks, sep="\n")

    sol = []
    time = 0
    while tasks and time + tasks[0].duration <= 1440:
        sol.append(tasks[0].task_id)
        time += tasks[0].duration
        del tasks[0]
    
    return sol

def calculate_profit(output, tasks):
    time = 0
    profit = 0
    for id in output:
        task = tasks[id - 1]
        finish = time + task.duration
        if finish <= task.deadline:
            profit += task.perfect_benefit
        else:
            profit += task.perfect_benefit * exp(-0.017 * (finish - task.deadline))
        time += task.duration

        if time > 1440:
            raise Exception("Output Exceeds 1440 Time") 
    return profit

# Here's an example of how to run your solver.
if __name__ == '__main__':
    total_profit = 0

    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if size not in input_file:
                continue
            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            print(input_path, output_path)
            tasks = read_input_file(input_path)
            output = solve(tasks)
            print(output)
            total_profit += calculate_profit(output, tasks)
            write_output_file(output_path, output)
            exit()

    print("Total Profit: ", total_profit)