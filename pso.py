#!/usr/bin/python


import neuralNetwork
import particle
#import learnParameters
#from learnParameters import dealTestfile
from particle import particle
import math
class pso:
    __numParticle=100
    __Vmax=2
    __Max_ITERATIONS=1000
    __C1=1
    __C2=2
    __gbest=0.0
    __gbestb=-1.0 
    def __init__(self,num,Vmax,iterations,C1,C2,filename):
        print "begin Initial parameters"
        self.__numParticle=num
        self.__Vmax=Vmax
        self.__Max_ITERATIONS=iterations
        self.__C1=C1
        self.__C2=C2
        self.__filename=filename
        self.__particleNum=[]
        self.__gbest=1.0
        self.__gbestb=-2.0
        for i in xrange(self.__numParticle):
            p=particle(0.05*i,0.01*i)
            self.__particleNum.append(p)
        print "have initial done the num:%s,iterations:%s" %(self.__numParticle,self.__Max_ITERATIONS)
    def psobegin(self):
        iterationsCount=0
        while iterationsCount<self.__Max_ITERATIONS:
             print('iterations=%d\n\n'%iterationsCount)
             for pnum in xrange(self.__numParticle):
                 if self.fitness(self.__particleNum[pnum].get_current(),self.__particleNum[pnum].get_currentb()) < self.fitness(self.__particleNum[pnum].get_pbest(),self.__particleNum[pnum].get_pbestb()):
                     self.__particleNum[pnum].set_current(self.__particleNum[pnum].get_pbest(),self.__particleNum[pnum].get_pbestb())
             self.find_gbest()
             for pnum in xrange(self.__numParticle):
                 self.__particleNum[pnum].adjust_v(self.__C1,self.__C2,self.__gbest,self.__gbestb,self.__Vmax) 
                 self.__particleNum[pnum].set_current(self.__particleNum[pnum].get_current()+self.__particleNum[pnum].get_speed(),self.__particleNum[pnum].get_currentb()+self.__particleNum[pnum].get_speedb())  
             iterationsCount+=1
        self.find_gbest()
        print "the best parameter is %s and %s,and the best result is %s" %(str(self.__gbest),str(self.__gbestb),str(self.fitness(self.__gbest,self.__gbestb)))
    def find_gbest(self):
        for pnum in xrange(self.__numParticle):
            if self.fitness(self.__gbest,self.__gbestb)>self.fitness(self.__particleNum[pnum].get_current(),self.__particleNum[pnum].get_currentb()):
                self.__gbest=self.__particleNum[pnum].get_current()
                self.__gbestb=self.__particleNum[pnum].get_currentb()
    def fitness(self,rate,rate1):
        #return learnParameters.dealTextfile(self.__filename,rate,rate1)
        return neuralNetwork.psolearn(self.__filename,rate,rate1)  
