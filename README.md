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

## Solution format
- String solution: the most common format used by the program, preferred for ease of use and high flexibility,
incomplete as it only contains information about job, operation and machine
    - Example: 
      ```text
      0-0-1 0-1-3 2-0-2 0-2-1
      ```
    - *"This isn't even my final form."*
- Struct solution: solution in the form of builtin data types, namely in the form of list\[list\[int\]\], incomplete for
the same reason
  - No example here because it's the same thing as string solution, except in code form 
- Visualized solution: processed string solution by adding time information, final form as it is what people actually
expect to see
  - Example (render might look weird depending on font since characters may not have equal width, just check raw if
  that's the case):
  ```text
               t=0       t=1       t=2       t=3       t=4       t=5       t=6    
   m=0    {____________1-0_____________}{__1-1___}{____________1-2_____________}
   m=1    {__2-0___}                              {_______2-2________}          
   m=2    {__0-0___}{___________________________0-1____________________________}
   m=3              {____________2-1_____________}                    {__2-3___}
  ```

## Setting up
- Clone this repo
- Inside the local repo, open a terminal there
- Use conda (either miniconda or the full-blown anaconda) to create a 3.10 pythonenv:
```shell
conda create -n <your_env_name> python==3.10.13
```
- Activate the conda environment:
```shell
conda activate <your_env_name>
```
- Install python packages:
```shell
pip install -r requirements.txt
```
- Modify inputs as needed in main.py or whatever
- Run the program (assuming you didn't drastically change it):
```shell
python main.py
```
- "Yes I could have made it more user-friendly by setting up batch run, pytest and all that good stuff. But the client
didn't request such features... and I'm not getting paid anyway."

## Extra
- Logs for each tabu search run is stored in logs/
- Input data should be placed in data/ but not mandatory