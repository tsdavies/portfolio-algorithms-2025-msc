##############################
# BACK END
##############################

import sys
from pathlib import Path
import importlib
import os

from multiprocessing import Process, Manager
import time

'''
    An automated testing script for CMT120
     2022/23 using multiprocessing and not SIGALRM,
      ....so, this should work on Windows machines....
'''


class TimeoutException(Exception):
    pass


def a_test(running_complete_dict, out, fun, *param):
    '''
        Function to be used in mutliprocessing Process.
        This updates the dictionary values if
        The test completes within the Process time limit
    '''
    out = fun(*param)
    running_complete_dict["running_complete"] = True
    running_complete_dict["response"] = out
    return out  # dont really need this


def main():
    # Importing functions
    def importModule(module_name):
        # get a handle on the module
        mdl = importlib.import_module(module_name)

        # is there an __all__?  if so respect it
        if "__all__" in mdl.__dict__:
            names = mdl.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in mdl.__dict__ if not x.startswith("_")]

        # now drag them in
        globals().update({k: getattr(mdl, k) for k in names})

    try:
        mod = sys.argv[1].split('.')[0]
        importModule(mod)
    except IndexError as ie:
        sys.exit('Please, provide the name of the file to test.')


    # Testing function
    def runTest(call, output ,isSoft = False):
        if type(call) != type(output):
            return False

        if isinstance(call,list):
            if len(call) != len(output):
                return False
            for ind in range(len(call)):
                if isSoft:
                    res = call[ind] in output
                else:
                    res = runTest(call[ind],output[ind])
                if not res:
                    return False
        elif call != output:
            return False

        return True

    ##############################
    # TESTCASES
    ##############################

    # Lists of tests for each function
    # Each element of the list is a (input,solution) tuple
    # - 'input' is a tuple containing the input parameters.
    # - 'solution' must be provided in format expected.
        
    exercise1_list = [(([('Earth',100,10), ('Earth',100,10)], [('Mercury',80,10), ('Venus',80,10)]), False),
					  (([('Earth',100,10)], [('Mercury',80,10), ('Mars',80,10)]), True)]


    exercise2_list = [(('sehuoh',),1),
				  (('caarto',),5)]

    green_1 = {1:'i',3:'c'}
    yellow_1 = {'e':{3}}
    gray_1 = {'r','a','s','d','f'}
    green_2 = {2:'a'}
    yellow_2 = {'a':{3},'i':{2},'l':{3,4},'r':{1}}
    gray_2={'e','t','u','o','p','g','h','c','m','s'}
    exercise3_list = [((green_1,yellow_1,gray_1),5),
				  ((green_2,yellow_2,gray_2),3)]

    exercise4_list = [(([['A','X','R','R','R'],['O','O','O','X','B'],['O','O','O','O','R']],),(7,3)),
					  (([['A','X','R','R','R'],['O','O','O','X','R'],['O','O','O','B','R']],),(5,0))]

    network1 = [[0,1,1,0,0,0,0],
            [1,0,1,1,0,0,0],
            [1,1,0,0,0,0,0],
            [0,1,0,0,1,1,1],
            [0,0,0,1,0,1,0],
            [0,0,0,1,1,0,1],
            [0,0,0,1,0,1,0]]

    network2 = [[0,1,0,0,0,0,1],
            [1,0,0,0,0,0,1],
            [0,0,0,1,0,0,1],
            [0,0,1,0,0,0,1],
            [0,0,0,0,0,1,1],
            [0,0,0,0,1,0,1],
            [1,1,1,1,1,1,0]]

    exercise5_list = [((network1,),[1, 2, 1, 3, 1, 2, 1]),
    				  ((network2,),[1, 1, 1, 1, 1, 1, 3])]


    ##############################
    # FRONT END
    ##############################

    # Dictionary of functions to test
    test_dict = {exercise1: exercise1_list,
    			 exercise2: exercise2_list,
    			 exercise3: exercise3_list,
    			 exercise4: exercise4_list,
    			 exercise5: exercise5_list
                }
    
    soft_equal = () # Used for checking if two lists have the same elements instead of being fully identical

    res_list = []
    # Loop on every function to test
    manager = Manager()

    for fun,test_list in test_dict.items():
        # show the name of the exercise to be tested
        sys.stdout.write(f'\n#### FUNCTION {fun.__name__}:\n\n')
        res = 0
        # Loop on every test to run
        for index, t in enumerate(test_list, start=1):
            test_time_limit = 3 # per test time limit (seconds)
            param = t[0]
            sol = t[1]
            out = None

            try:
                # establish a dict to be passed to multiprocess Process.
                running_complete_dict = manager.dict()
                running_complete_dict["running_complete"] = False
                running_complete_dict["response"] = None
                new_test_process = Process(target=a_test, args=(running_complete_dict, out, fun ,*param,))
                # show test underway....else the 2-second pause can be frustrating
                sys.stdout.write(f'Test: {index}\n')
                sys.stdout.flush()

                new_test_process.start()
                # Process starts and we wait for the length of time indicated
                # 2-seconds per test is more generous than in the first testing
                #  framework.
                time.sleep(test_time_limit)
                new_test_process.terminate()

                out = running_complete_dict["response"]

                if not running_complete_dict["running_complete"] == False:
                    # the test has completed within the timelimit set,
                    #  test for correctness
                    isSoft = fun in soft_equal
                    if not runTest(out,sol,isSoft):
                        # the submission, does not return the correct value
                        err_str = f'ERROR IN {fun.__name__}{param}: *** EXPECTED: {sol} *** OBTAINED: {out}\n\n'
                        sys.stdout.write(err_str)
                        sys.stdout.flush()
                    else:
                        # the submission returns the correct value
                        res += 1
                        sys.stdout.write(f'{fun.__name__}{param}: PASSED\n\n')
                        sys.stdout.flush()
                else:
                    # the test did not complete within the time limit set...
                    raise TimeoutException
            except Exception as e:
                if type(e) == TimeoutException:
                    e = f"TimeoutException > {test_time_limit} seconds"
                err_str = f'ERROR IN {fun.__name__}{param}: {str(e)} \n\n'
                sys.stdout.write(err_str)
                sys.stdout.flush()
            # END for t in test_list:

        res_list.append(res)
        err_str = f'#### FUNCTION {fun.__name__} SCORE: {res} / {len(test_list)}\n\n'
        sys.stdout.write(err_str)
        sys.stdout.flush()
        # END for fun_name,test_list in test_dict.items():

    # print res_list as a CSV
    out_str = f'{sys.argv[1]}, {", ".join(str(x) for x in res_list)}\n'

    sys.stderr.write(out_str)
    sys.stderr.flush()


if __name__ == '__main__':
    main()
