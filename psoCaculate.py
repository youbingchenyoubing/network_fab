#!/usr/bin/python/env
import os
import sys
import pso
import argparse
#from pso import psobegin
#usage python psoCaculate.py -f result -C1 2 -C2 4 -v 2 -p 100 -i 1000
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-f', action='store', required=True, dest='filename',
                    help='filename is the result file of asa')
    parser.add_argument('-C1', action='store', required=True, dest='speedstep1',
                    help='float for C1')
    parser.add_argument('-C2', action='store', required=True, dest='speedstep2',
                    help='float for C2')
    parser.add_argument('-v', action='store', required=True, dest='Vmax',
                    help='float for v')
    parser.add_argument('-p', action='store', required=True, dest='particleCount',
                    help='the number of particle, it\'s a Integer')
    parser.add_argument('-i', action='store', required=True, dest='iterations',
                    help='the number of iteration, it\'s a Integer')
    inputs=parser.parse_args()
    filename=os.getcwd()+'/'+inputs.filename
    print "the pso program is begin caculate,please waiting for a moment"
    psocaculate=pso.pso(int(inputs.particleCount),float(inputs.Vmax),int(inputs.iterations),float(inputs.speedstep1),float(inputs.speedstep2),filename) 
    psocaculate.psobegin()
  



if __name__=="__main__":
    print "in main functions"
    main()
