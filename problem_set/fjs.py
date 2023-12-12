from typing import List, Any


class FlexibleJobSchedulingProblem(object):
    number_of_machines: int
    number_of_ops: int
    number_of_jobs: int
    ops_per_job: list[int]
    time_required_for_job_op: list[list[list[int]]]

    def __init__(self, input_file_path):
        self.__read_input(input_file_path)

    def __read_input(self, input_file_path):
        self.number_of_jobs = 0
        self.number_of_ops = 0
        self.number_of_machines = 0
        self.ops_per_job = []
        self.time_required_for_job_op = []

        with open(input_file_path, "r") as fin:
            lines = [line.strip() for line in fin.readlines() if line]

            line_0_words = lines[0].split()
            self.number_of_jobs = int(line_0_words[0].strip())
            self.number_of_machines = int(line_0_words[1].strip())

            line_index = 0

            for i in range(self.number_of_jobs):
                line_index += 1
                current_line = lines[line_index]
                number_of_ops_for_this_job = int(current_line[0].strip())
                self.ops_per_job.append(number_of_ops_for_this_job)
                self.time_required_for_job_op.append([])
                for j in range(number_of_ops_for_this_job):
                    line_index += 1
                    current_line = lines[line_index]
                    times_for_this_op = current_line.split()
                    self.time_required_for_job_op[i].append([])
                    for k in range(self.number_of_machines):
                        time_required_by_next_machine = int(times_for_this_op[k].strip())
                        self.time_required_for_job_op[i][j].append(time_required_by_next_machine)

    def __str__(self):
        return str(self.time_required_for_job_op)

    def get_default_solution(self):
        string = ''
        next_time = 0
        for job_id in range(self.number_of_jobs):
            for op_id in range(self.ops_per_job[job_id]):
                time_for_this_job_op = self.time_required_for_job_op[job_id][op_id][0]
                string += f'j{job_id}o{op_id}m{0}t{next_time} '
                next_time += time_for_this_job_op
        return string
                