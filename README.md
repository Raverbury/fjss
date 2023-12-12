## Input explanation
```text
num_of_jobs num_of_machines // line 0
num_of_ops_in_job_0         // line 1
time_of_op_0_0_in_machine_0 time_of_op_0_0_in_machine_1 ...
time_of_op_0_1_in_machine_0 time_of_op_0_1_in_machine_1 ...
...
... // repeat of line 1 until enough jobs have been filled
```
- Example:
```text
2 3       // 2 jobs, 3 machines
3         // job 0 has 3 ops
3 2 6
4 1 4
2 3 4
1         // job 1 has 1 op
4 7 8
```
