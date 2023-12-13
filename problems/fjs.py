import random


class FlexibleJobSchedulingProblem(object):
    number_of_machines: int
    number_of_ops: int
    number_of_jobs: int
    ops_per_job: list[int]
    time_required_for_job_op: list[list[list[int]]]
    available_machines_for_job_op: list[list[list[int]]]

    SWITCH_MACHINE_CHANCE = 0.8

    def __init__(self, input_file_path: str):
        self.__read_input(input_file_path)

    def __read_input(self, input_file_path: str):
        self.number_of_jobs = 0
        self.number_of_ops = 0
        self.number_of_machines = 0
        self.ops_per_job = []
        self.time_required_for_job_op = []
        self.available_machines_for_job_op = []

        with open(input_file_path, "r") as fin:
            lines = [line.strip() for line in fin.readlines() if (line and not line.startswith(('#', '//')))]

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
                self.available_machines_for_job_op.append([])
                for j in range(number_of_ops_for_this_job):
                    line_index += 1
                    current_line = lines[line_index]
                    times_for_this_op = current_line.split()
                    self.time_required_for_job_op[i].append([])
                    self.available_machines_for_job_op[i].append([])
                    for k in range(self.number_of_machines):
                        time_required_by_machine = int(times_for_this_op[k].strip())
                        self.time_required_for_job_op[i][j].append(time_required_by_machine)
                        if time_required_by_machine >= 0:
                            self.available_machines_for_job_op[i][j].append(k)

    def __str__(self):
        return f'{str(self.time_required_for_job_op)}\n{str(self.available_machines_for_job_op)}'

    def get_random_solution(self) -> str:
        string = ''

        # fill random pool with op 0 from all jobs
        pool: dict[int, list] = {}
        for job_id in range(self.number_of_jobs):
            pool[job_id] = [0] if self.ops_per_job[job_id] > 0 else []

        while len(pool) > 0:
            # draw a random op and a random machine available for that op
            random_job_id = random.choice(list(pool.keys()))
            random_op_id = random.choice(pool[random_job_id])
            random_machine_id = random.choice(self.available_machines_for_job_op[random_job_id][random_op_id])

            string += f'{random_job_id}-{random_op_id}-{random_machine_id} '
            (pool[random_job_id]).remove(random_op_id)

            # if op is the last op (highest possible op id) in the job, remove job from pool
            if random_op_id == self.ops_per_job[random_job_id] - 1:
                pool.pop(random_job_id)
            # else add the next available op
            else:
                pool[random_job_id].append(random_op_id + 1)

        return string

    def get_random_neighbor_solution(self, current_solution: str):
        struct_solution = FlexibleJobSchedulingProblem.parse_solution(current_solution)
        number_of_ops = len(struct_solution)
        lower_index = 0
        upper_index = 0
        random_op_index = 0

        # honestly idk why, prolly to catch some edge cases i can't think of atm
        while lower_index >= upper_index:
            random_op_index = random.randint(0, number_of_ops - 1)
            chosen_op = struct_solution[random_op_index]
            job_id = chosen_op[0]
            op_id = chosen_op[1]

            # explore backward until start of array
            lower_index = random_op_index - 1
            while lower_index >= 0:
                target_op = struct_solution[lower_index]
                target_job_id = target_op[0]
                target_op_id = target_op[1]

                # if we encounter a prereq op on the way (aka same job_id but target_op_id < by 1) then stop
                if target_job_id == job_id and target_op_id == op_id - 1:
                    break
                lower_index -= 1

            # lower index should have stopped at an op that can't be relocated to
            # either at -1 or at a prereq op, in any case, add 1 to re-enter valid range
            lower_index = lower_index + 1

            # explore forward until end of array
            upper_index = random_op_index + 1
            while upper_index <= number_of_ops - 1:
                target_op = struct_solution[upper_index]
                target_job_id = target_op[0]
                target_op_id = target_op[1]
                # if we encounter a postreq op on the way (aka same job_id but target_op_id > by 1) then stop
                if target_job_id == job_id and target_op_id == op_id + 1:
                    break
                upper_index += 1

            # upper index should have stopped at an op that can't be relocated to
            # either at max len or at a postreq op, in any case, subtract 1 to re-enter valid range
            upper_index = upper_index - 1

        index_to_insert_at = random_op_index
        # roll gacha until we get an index that's different from our starting random index
        while index_to_insert_at == random_op_index:
            index_to_insert_at = random.randint(lower_index, upper_index)

        # temp remove op from solution
        chosen_op = struct_solution[random_op_index]
        struct_solution.pop(random_op_index)

        # x% chance to randomly switch op to a new machine
        roll = random.random()
        # only if there are more than 1 machine available tho
        if len(self.available_machines_for_job_op[chosen_op[0]][chosen_op[1]]) > 1:
            if roll < FlexibleJobSchedulingProblem.SWITCH_MACHINE_CHANCE:
                current_machine_index = chosen_op[2]
                new_machine_index = current_machine_index
                # roll until we get a different machine index
                while new_machine_index == current_machine_index:
                    new_machine_index = random.choice(
                        self.available_machines_for_job_op[chosen_op[0]][chosen_op[1]])
                chosen_op[2] = new_machine_index

        # re-insert at new index
        struct_solution.insert(index_to_insert_at, chosen_op)

        return FlexibleJobSchedulingProblem.stringify_solution(struct_solution)

    @staticmethod
    def parse_solution(string_solution: str) -> list[list[int]]:
        result = []
        words: list[str] = [word.strip() for word in string_solution.split()]
        for word in words:
            numbers: list[int] = [int(num.strip()) for num in word.split('-')]
            result.append(numbers)
        return result

    @staticmethod
    def stringify_solution(struct_solution: list[list[int]]) -> str:
        """

        :param struct_solution: Solution in "struct"/list[list[int]] format.
        :return: Solution in string format.
        """
        result = ''
        for op in struct_solution:
            result += '-'.join([str(num) for num in op]) + ' '
        return result

    def solution_is_valid(self, string_solution: str) -> bool:
        struct_sol = FlexibleJobSchedulingProblem.parse_solution(string_solution)
        finished_ops = {job_id: -1 for job_id in range(self.number_of_jobs)}

        for op in struct_sol:
            job_id = op[0]
            op_id = op[1]
            if finished_ops[job_id] != op_id - 1:
                return False
            finished_ops[job_id] += 1
        return True

    def evaluate_solution(self, string_solution: str) -> int:
        struct_solution = FlexibleJobSchedulingProblem.parse_solution(string_solution)
        machine_time_table = {machine_id: [-1, 0] for machine_id in range(self.number_of_machines)}
        earliest_start_time_for_ops = [[-1] * self.ops_per_job[job_id] for job_id in range(self.number_of_jobs)]
        for job_id in range(self.number_of_jobs):
            if self.ops_per_job[job_id] > 0:
                earliest_start_time_for_ops[job_id][0] = 0

        for op in struct_solution:
            job_id = op[0]
            op_id = op[1]
            machine_id = op[2]
            time_required = self.time_required_for_job_op[job_id][op_id][machine_id]
            earliest_possible_start_time = max(machine_time_table[machine_id][1],
                                               earliest_start_time_for_ops[job_id][op_id])
            
            if machine_time_table[machine_id][0] == -1:
                machine_time_table[machine_id][0] = earliest_possible_start_time
            machine_time_table[machine_id][1] += time_required
            
            next_op_id = op_id + 1
            if next_op_id <= len(earliest_start_time_for_ops[job_id]) - 1:
                earliest_start_time_for_ops[job_id][next_op_id] = machine_time_table[machine_id][1]

        start_times = [machine_time[0] for machine_time in machine_time_table.values()]
        end_times = [machine_time[1] for machine_time in machine_time_table.values()]
        earliest_machine_start_time = 0 if min(start_times) == -1 else min(start_times)
        latest_machine_end_time = max(end_times)

        return latest_machine_end_time - earliest_machine_start_time
