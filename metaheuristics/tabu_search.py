import math
import time
import heapq
from tqdm.auto import tqdm
from problems.fjs import FlexibleJobSchedulingProblem


class TabuSearch(object):
    @staticmethod
    def run_fjs(fjs: FlexibleJobSchedulingProblem, number_of_iterations: int, tabu_size: int,
                reset_threshold: int, number_of_neighbors: int, timeout_duration: float = 15.0) -> list[str]:
        """
        Run Tabu Search against a Flexible Job Shop Scheduling problem

        :param fjs: An instance of Flexible Job Shop Scheduling problem
        :param number_of_iterations: The number of iterations to run for this tabu search
        :param tabu_size: The size of the tabu list, automatically removing older entries if exceeding this limit
        :param reset_threshold: Backtrack if algo can't find a better solution in this many iterations
        :param number_of_neighbors: Number of neighbors to generate for each iteration before tabu filtering
        :param timeout_duration: The algo will only run for this amount of time, set to -1 if endless is desired
        :returns: tuple (best visualized solutions: list, best makespan: int, log: str)
        """
        all_solutions_dict_with_makespan_as_key: dict[int, set[str]] = dict()
        all_solutions = []
        all_solutions_dict_with_sol_as_key: dict[str, int] = dict()
        best_solutions: list[str] = []
        best_makespan: int = -1
        tabu_list: UniqueQueue = UniqueQueue()
        initial_solution = fjs.get_random_solution()
        current_solution = initial_solution
        rollback_stack: set[str] = set()
        stuck_counter = 0
        start_time = time.time()
        log = ''
        current_iteration = 0
        timed_out = False
        tabu_block_counter = 0

        init_non = number_of_neighbors
        if number_of_neighbors == -1:
            number_of_neighbors = int(float(math.factorial(fjs.number_of_ops) *
                                            (fjs.number_of_machines ** fjs.number_of_ops)) / number_of_iterations)
        number_of_neighbors = min(500, max(50, number_of_neighbors))

        # add this iter's best sols to tabu, sort these sols and pick the first one as next iter's sol, could also
        # be last and reversed when inserting into tabu
        # if stuck counter pass the reset threshold, pop the most recent sol in tabu stack, use the next most recent
        # or init if empty sol as the next iter's sol

        for current_iteration in tqdm(range(number_of_iterations)):
            log += f'## Iteration {current_iteration}\n'
            current_makespan = fjs.evaluate_solution(current_solution)
            log += f'- Current solution: {current_solution} with makespan {current_makespan}\n'
            # if run time exceeds timeout duration, end prematurely
            elapsed = time.time() - start_time
            if elapsed >= timeout_duration:
                print('Timed out!')
                log += f'- !!! Timed out!\n'
                timed_out = True
                break

            # gen list of neighbors
            neighbors = []
            for i in range(number_of_neighbors):
                new_neighbor = fjs.get_random_neighbor_solution(current_solution)
                # remove neighbor who's in the tabu
                if new_neighbor not in tabu_list:  # maybe add a valid check here?
                    neighbors.append(new_neighbor)
                    tabu_block_counter += 1
            neighbor_solutions_with_makespan = dict()

            # eval make span for all neighbors
            # add every new sol to all sol list
            for neighbor_solution in neighbors:
                makespan = fjs.evaluate_solution(neighbor_solution)
                if makespan not in neighbor_solutions_with_makespan:
                    neighbor_solutions_with_makespan[makespan] = set()
                neighbor_solutions_with_makespan[makespan].add(neighbor_solution)
                if makespan not in all_solutions_dict_with_makespan_as_key:
                    lst = set()
                    all_solutions_dict_with_makespan_as_key[makespan] = lst
                all_solutions_dict_with_makespan_as_key[makespan].add(neighbor_solution)
                if neighbor_solution not in all_solutions_dict_with_sol_as_key:
                    all_solutions_dict_with_sol_as_key[neighbor_solution] = makespan
                    heapq.heappush(all_solutions, neighbor_solution)
            makespans = list(neighbor_solutions_with_makespan.keys())
            best_makespan_this_iter = min(makespans)
            log += f'- All-time best makespan: {best_makespan}\n'
            log += f'- This iteration\'s best makespan: {best_makespan_this_iter}\n'

            # best neighbors of this iter
            best_neighbors = sorted(neighbor_solutions_with_makespan[best_makespan_this_iter])

            # if there are better sols, update all-time best, else increase stuck counter
            if best_makespan_this_iter < best_makespan or best_makespan == -1:
                best_makespan = best_makespan_this_iter
                best_solutions = best_neighbors
                stuck_counter = 0
            else:
                stuck_counter += 1
                log += f'- Stuck counter: {stuck_counter}/{reset_threshold}\n'

            tabu_list.push(best_neighbors[-1])
            if len(tabu_list) > tabu_size:
                tabu_list.pop()
            current_solution = best_neighbors[-1]
            for best_neighbor in reversed(best_neighbors):
                rollback_stack.add(best_neighbor)

            # if stuck for too long, backtrack and remove the next backtrack target from tabu
            if stuck_counter >= reset_threshold:
                stuck_counter = 0
                rollback_solution = rollback_stack.pop() if len(rollback_stack) > 0 else initial_solution
                if rollback_solution in tabu_list:
                    tabu_list.remove(rollback_solution)
                current_solution = rollback_solution
                rollback_makespan = fjs.evaluate_solution(current_solution)
                log += f'- !!! Stuck for too long, backtracking to {current_solution} with makespan {rollback_makespan}!\n'

            log += '\n'

        # actually finish making the final solution
        # string results are only partially completed and may yield duplicate result
        visualized_best_solutions = set([fjs.get_evaluated_visualization(sol) for sol in best_solutions])

        header_log = '# Tabu search summary\n'
        header_log += f'- Input obtained from {fjs.input_file}:\n\n'
        with open(fjs.input_file, 'rt') as f:
            header_log += f.read() + '\n\n'
        num_of_completed_iterations = current_iteration if timed_out else current_iteration + 1
        header_log += f'- Completed {num_of_completed_iterations} out of {number_of_iterations} iterations\n'
        header_log += f'- number_of_iteration was {number_of_iterations}\n'
        header_log += f'- tabu_size was {tabu_size}\n'
        header_log += f'- reset_threshold was {reset_threshold}\n'
        header_log += f'- number_of_neighbors was {init_non} -> {number_of_neighbors}\n'
        header_log += f'- timeout_duration was {timeout_duration}\n'
        num_of_all_sols = sum([len(x) for x in all_solutions_dict_with_makespan_as_key.values()])
        header_log += (f'- Explored {num_of_all_sols} ' +
                       'unique string solutions, distribution is as follows:\n')
        for key in all_solutions_dict_with_makespan_as_key.keys():
            num_of_sols = len(all_solutions_dict_with_makespan_as_key[key])
            percentage = '{:.2f}'.format((float(num_of_sols) / float(num_of_all_sols) * 100))
            header_log += f'  + Makespan of {key}: {num_of_sols} unique string solutions ({percentage}%)\n'
        header_log += f'- Best makespan found was {min(all_solutions_dict_with_makespan_as_key.keys())}\n'
        header_log += f'- Tabu list prevented {tabu_block_counter} solutions from being revisited (before uniqueness)\n'

        log = header_log + '\n# Tabu search details\n' + log

        # Do not uncomment this unless you can plot this in a real plot with a real plotting lib
        # or if you like flooding your log file with a LOT of ########
        # sol_space_log = '\n# Solution space visualization, sorted by string solution\n'
        # while len(all_solutions) > 0:
        #     solution = heapq.heappop(all_solutions)
        #     makespan = all_solutions_dict_with_sol_as_key[solution]
        #     sol_space_log += ''.ljust(makespan, '#') + '\n'
        #
        # log = log + sol_space_log

        return best_makespan, list(visualized_best_solutions), log


class UniqueQueue(object):
    inner_set = set()
    inner_list = []

    def push(self, item):
        if item in self.inner_set:
            return
        self.inner_set.add(item)
        self.inner_list.append(item)

    def pop(self):
        item = self.inner_list.pop(0)
        self.inner_set.remove(item)
        return item

    def remove(self, item):
        if item not in self:
            return
        self.inner_set.remove(item)
        self.inner_list.remove(item)

    def __len__(self):
        return len(self.inner_list)

    def __contains__(self, item):
        return item in self.inner_set
