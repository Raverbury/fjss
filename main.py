from problems.fjs import FlexibleJobSchedulingProblem
from metaheuristics.tabu_search import TabuSearch


def __main__():
    flexible_job_scheduling_problem = FlexibleJobSchedulingProblem('input.txt')
    # print(flexible_job_scheduling_problem, flexible_job_scheduling_problem.number_of_jobs)
    solution = flexible_job_scheduling_problem.get_random_solution()
    valid_solution = 'valid' if flexible_job_scheduling_problem.solution_is_valid(solution) else 'invalid'
    solution_makespan = flexible_job_scheduling_problem.evaluate_solution(solution)
    print(f'{solution}: {valid_solution} with makespan of {solution_makespan}')
    solution_set = set()
    print('Generating neighbors')
    NUM_OF_NEIGHBORS = 200
    for i in range(NUM_OF_NEIGHBORS):
        neighbor_solution = flexible_job_scheduling_problem.get_random_neighbor_solution(solution)
        solution_set.add(neighbor_solution)
        solution_makespan = flexible_job_scheduling_problem.evaluate_solution(neighbor_solution)
        valid_solution = 'valid' if flexible_job_scheduling_problem.solution_is_valid(neighbor_solution) else 'invalid'
        print(f'{neighbor_solution}: {valid_solution} with makespan of {solution_makespan}')
    print(f'{len(solution_set)} unique solutions out of {NUM_OF_NEIGHBORS}')


if __name__ == '__main__':
    __main__()
