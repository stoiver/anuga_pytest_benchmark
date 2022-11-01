# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.


#--------------------------------------------------------------------------
# Setup procedures
#--------------------------------------------------------------------------
class Set_Stage:
    """Set an initial condition with constant water height, for x0<x<x1
    """

    def __init__(self, x0=0.25, x1=0.5, h=1.0):
        self.x0 = x0
        self.x1 = x1
        self.h  = h

    def __call__(self, x, y):
        return self.h*((x>self.x0)&(x<self.x1))+1.0


class Set_Elevation:
    """Set an elevation
    """

    def __init__(self, h=1.0):
        self.x0 = x0
        self.x1 = x1
        self.h  = h

    def __call__(self, x, y):
        return x/self.h
    


import time
import pytest

@pytest.mark.benchmark(
    group="anuga benchmarks",
    min_time=0.5,
    max_time=3.5,
    min_rounds=1,
    timer=time.perf_counter,
    disable_gc=True,
    warmup=False
)
def test_anuga_evolve(benchmark):

    benchmark(run_anuga_evolve)


def run_anuga_evolve():

    import anuga

    import os
    print(os.path.abspath(__file__))
    file_dir = os.path.dirname(os.path.abspath(__file__))

    print(file_dir)

    mesh_filename = file_dir+"/merimbula_10785_1.tsh"

    x0 = 756000.0 ; x1 = 756500.0; yieldstep = 10.0; finaltime = 50.0

    domain = anuga.create_domain_from_file(mesh_filename)
    domain.set_quantity('stage', Set_Stage(x0, x1, 1.0))

    domain.set_name()
    domain.set_store(False)
    domain.set_flow_algorithm('DE0')

    Br = anuga.Reflective_boundary(domain)      # Solid reflective wall
    from math import sin
    Bts = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(domain, lambda t: 10*sin(t/200))

    domain.set_boundary({'exterior' :Br, 'open' :Bts})
    
    for t in domain.evolve(yieldstep= yieldstep, finaltime=finaltime):
        domain.print_timestepping_statistics()
        pass


if __name__ == "__main__":
    run_anuga_evolve()
    


        


