from problems.fjs import FlexibleJobSchedulingProblem
from metaheuristics.tabu_search import TabuSearch
import datetime
import os
import argparse


def __main__():
    arg_parser = argparse.ArgumentParser(
        description='Use tabu search to optimize the solutions to a flexible job shop scheduling problem',
        epilog='Example: python main.py data/input_0.txt 5000 '
    )

    arg_parser.add_argument('path_to_input_file',
                            help='Path to the input file, refer to README.md for input format')
    arg_parser.add_argument('number_of_iterations',
                            type=int,
                            help='Number of iterations the tabu search should run for')
    arg_parser.add_argument('--number_of_neighbors', '-n',
                            default=100,
                            type=int,
                            help='The number of neighbors to generate each iteration. ' +
                            'Defaults to 100. If -1 the program will infer from the given input, result ' +
                            '= (!num_of_ops * (num_of_ops ** num_of_machines)) / 100, clamped between 50 and 500')
    arg_parser.add_argument('--tabu_size', '-t',
                            default=20,
                            type=int,
                            help='The size of the tabu list, automatically removing older entries if exceeding. ' +
                            'Defaults to 20')
    arg_parser.add_argument('--stuck_reset_threshold', '-s',
                            default=10,
                            type=int,
                            help='If the search cannot find a better solution after this many iterations, ' +
                            'backtrack to an earlier solution. Defaults to 10')
    arg_parser.add_argument('--timeout_duration', '-o',
                            default=15.0,
                            type=float,
                            help='The search will automatically stop after this much time has passed. ' +
                            'Defaults to 15.0 seconds')

    args = vars(arg_parser.parse_args())

    flexible_job_scheduling_problem = FlexibleJobSchedulingProblem(args['path_to_input_file'])

    best_makespan, best_visualized_solutions, log = (
        TabuSearch.run_fjs(flexible_job_scheduling_problem,
                           args['number_of_iterations'],
                           args['tabu_size'],
                           args['stuck_reset_threshold'],
                           args['number_of_neighbors'],
                           args['timeout_duration']))

    print(f'Tabu search returned {len(best_visualized_solutions)} best solution(s) with makespan of {best_makespan}')

    for best_visualized_solution in best_visualized_solutions:
        print(best_visualized_solution)

    filename = ('log_' +
                str(datetime.datetime.now()).replace(':', '_').replace(' ', '_') + '.txt')
    logs_path = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_path, exist_ok=True)
    final_filepath = os.path.join(logs_path, filename)
    with open(f'{final_filepath}', 'wt+') as f:
        f.write(log)
    print(f'Log saved to {final_filepath}')


if __name__ == '__main__':
    __main__()
