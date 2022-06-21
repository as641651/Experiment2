import sys
import os
import shutil

from linnea.algebra.expression import Matrix, Vector, Equal, Times, Inverse, Transpose, Plus
from linnea.algebra.equations import Equations
from linnea.algebra.properties import Property

import pathlib
this_dir = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(this_dir,"../../utils"))

#from ...utils import generate_linnea_experiment_code
import generate_linnea_experiment_code

import argparse


def random1(m,n,k):

    M1 = Matrix("M1", (m, n))
    M1.set_property(Property.FULL_RANK)

    M2 = Matrix("M2", (m, n))
    M2.set_property(Property.FULL_RANK)

    M3 = Matrix("M3", (m, k))
    M3.set_property(Property.FULL_RANK)

    M4 = Matrix("M4", (m, m))
    M4.set_property(Property.UPPER_TRIANGULAR)

    M5 = Matrix("M5", (m, m))
    M5.set_property(Property.UPPER_TRIANGULAR)

    Y = Matrix("Y", (m, m))

    # Y = ABCD
    equations = Equations(Equal(Y, Plus(
                                        Times(M1, Transpose(M2)),
                                        Times(M3, Transpose(M3)),
                                        Transpose(M4),
                                        Transpose(M5))))

    return equations



if __name__ == "__main__":

    import linnea.config

    linnea.config.set_output_code_path(".")
    linnea.config.experiment_configuration["repetitions"] = 10
    linnea.config.init()

    from linnea.algorithm_generation.graph.search_graph import SearchGraph

    parser = argparse.ArgumentParser(description='Input: [m,n,k]')
    parser.add_argument('dims', metavar='N', type=int, nargs='+',
                        help=' Enter atleast 3 integers. ')
    parser.add_argument('--threads', type=int, default=4,
                        help= 'Num threads')

    dims = parser.parse_args()._get_kwargs()[0][1]
    threads = parser.parse_args()._get_kwargs()[1][1]
    if len(dims) != 3:
        raise Exception("Need 3 dimensions")
    m,n,k = dims
    linnea.config.experiment_configuration["threads"] = str(threads)

    expression_dir = os.path.join(this_dir,'experiments','{}_{}_{}/'.format(m,n,k))
    if os.path.exists(expression_dir):
        shutil.rmtree(expression_dir)
    os.makedirs(expression_dir)
    linnea.config.set_output_code_path(expression_dir)


    #from input1 import equations

    # import linnea.examples.examples
    # equations = linnea.examples.examples.Example001().eqns

    equations = random1(m,n,k)
    graph = SearchGraph(equations)
    graph.generate(time_limit=60,
                   merging=True,
                   dead_ends=True,
                   pruning_factor=100.0)

    graph.write_output(code=True,
                       generation_steps=True,
                       output_name="variants",
                       experiment_code=True,
                       algorithms_limit=100,
                       graph=True,
                       no_duplicates=True)


    ## Generate Experiment Code
    generate_linnea_experiment_code.generate_experiment_code(expression_dir)
    generate_linnea_experiment_code.generate_runner_code(expression_dir,
                                                         threads=threads,
                                                         backend_template='slrum_submit.sh')

    ##generate min flops runner code. read case table and find alg with min flops

    print("Generated Variants.")