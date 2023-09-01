import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

class BenchmarkResult(object):

    def __init__(self):
        self.cores_per_node = 96
        self.ns_per_day = -1
        self.hours_per_ns = -1
        self.time_core = -1
        self.time_wall = -1
        self.mflops = -1
        self.ranks = 0
        self.ntomp = 0
    
    def __str__(self):
        s = str(self.ns_per_day) + "\n"
        s += str(self.hours_per_ns)+ "\n"
        s += str(self.time_core)+ "\n"
        s += str(self.time_wall)+ "\n"
        s += str(self.mflops)+ "\n"
        s += str(self.ranks)+ "\n"
        s += str(self.ntomp)+ "\n"
        
        return s                                      
        
    
    @property
    def tflops(self):
        return self.mflops*10**(-6)    

    @property
    def gflops(self):
        return self.mflops*10**(-3)  
        
    @property
    def nodes(self):
        return self.ranks*self.ntomp/self.cores_per_node        
        
        
def get_floats_from_line(line):

    nums = []
    for char in line.split(" "):
        try:
            nums.append(float(char))
        except:
            continue
    return nums            
            
          
        
def parse_benchmark(file_path):

    
    try:
        ranks = float(file_path.split("_")[1])
        ntomp =  float(file_path.split("_")[2])
    except:
        print(file_path)
        exit()        

    with open(file_path) as f:
        
        lines = f.readlines()
        bench = BenchmarkResult()
        bench.ntomp = ntomp
        bench.ranks = ranks
        
        flops_section = False
        
        for l in lines:
        
            if "Performance:" in l:
                nums=get_floats_from_line(l)
                bench.ns_per_day = nums[0]
                bench.hours_per_ns = nums[1]
                
            if "Time:" in l:
                nums=get_floats_from_line(l)
                bench.time_core = nums[0]
                bench.time_wall = nums[1]
                
            if "Total" in l and flops_section and bench.mflops == -1:
                nums=get_floats_from_line(l)
                bench.mflops == nums[0]
            
            if "M E G A - F L O P S   A C C O U N T I N G" in l:
                flops_section = True              
                
    return bench                
                
                                           
        
        
                            


# list all current log files
files = os.listdir("benchmark/")
files = [x for x in files if ".log" in x and not x[0] == '#']
print(files[:5])

print("... parsing benchmarks ... ")
benchs = [parse_benchmark("benchmark/" + f) for f in files]
print("... done ... ")

ranks = np.array([b.ranks for b in benchs])
nodes = np.array([b.nodes for b in benchs])
ns_per_day = np.array([b.ns_per_day for b in benchs])
ntomp = np.array([b.ntomp for b in benchs])
tflops = np.array([b.tflops for b in benchs])



inds_2 = np.where(ntomp == 2)[0]
inds_4 = np.where(ntomp == 4)[0]
inds_6 = np.where(ntomp == 6)[0]
inds_8 = np.where(ntomp == 8)[0]


ns_per_day_6 = ns_per_day[inds_6]
inds_6_sort = np.argsort(ns_per_day_6)

print(" ntomp 6 :: ")
print(ns_per_day_6[inds_6_sort])
print(ranks[inds_6][inds_6_sort])
print(nodes[inds_6][inds_6_sort])
print("")
print("")


plt.scatter(nodes[inds_2], ns_per_day[inds_2], label="NTOMP=2")
plt.scatter(nodes[inds_4], ns_per_day[inds_4], label="NTOMP=4")
plt.scatter(nodes[inds_6], ns_per_day[inds_6], label="NTOMP=6")
plt.scatter(nodes[inds_8], ns_per_day[inds_8], label="NTOMP=8")
plt.legend(loc="best")
plt.xlabel("LB2 nodes")
plt.ylabel("ns_per_day")
plt.tight_layout()
plt.grid()
plt.savefig("ns_per_day.png", dpi=600)
plt.clf()

plt.scatter(nodes[inds_2], ns_per_day[inds_2], label="NTOMP=2")
plt.scatter(nodes[inds_4], ns_per_day[inds_4], label="NTOMP=4")
plt.scatter(nodes[inds_6], ns_per_day[inds_6], label="NTOMP=6")
plt.scatter(nodes[inds_8], ns_per_day[inds_8], label="NTOMP=8")
plt.legend(loc="best")
plt.xlabel("LB2 nodes")
plt.ylabel("ns_per_day")
plt.xlim(0,100)
plt.tight_layout()
plt.grid()
plt.savefig("ns_per_day_subset.png", dpi=600)
plt.clf()


plt.scatter(nodes[inds_2], ns_per_day[inds_2], label="NTOMP=2")
plt.scatter(nodes[inds_4], ns_per_day[inds_4], label="NTOMP=4")
plt.scatter(nodes[inds_6], ns_per_day[inds_6], label="NTOMP=6")
plt.scatter(nodes[inds_8], ns_per_day[inds_8], label="NTOMP=8")
plt.legend(loc="best")
plt.xlabel("LB2 nodes")
plt.ylabel("ns_per_day")
plt.tight_layout()
plt.xscale('log')
plt.savefig("ns_per_day_log.png", dpi=600)
plt.clf()

plt.scatter(nodes, ns_per_day)
plt.xlabel("LB2 nodes")
plt.ylabel("ns_per_day")
plt.tight_layout()
plt.savefig("ns_per_day_scatter.png", dpi=600)
plt.clf()

plt.scatter(nodes, tflops)
plt.xlabel("LB2 nodes")
plt.ylabel("TFlop/s")
plt.tight_layout()
plt.savefig("tflops.png", dpi=600)
plt.clf()

plt.scatter(nodes, ntomp, c=ns_per_day)
plt.colorbar()
plt.xlabel("LB2 nodes")
plt.ylabel("ntomp")
plt.tight_layout()
plt.savefig("nodes_ntomp.png", dpi=600)
plt.clf()



