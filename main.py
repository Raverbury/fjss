from problem_set.fjs import FlexibleJobSchedulingProblem


def __main__():
    flexible_job_scheduling_problem = FlexibleJobSchedulingProblem('input.txt')
    print(flexible_job_scheduling_problem, flexible_job_scheduling_problem.number_of_jobs)
    print(flexible_job_scheduling_problem.get_default_solution())


if __name__ == '__main__':
    __main__()
