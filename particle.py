#!/usr/bin/python
import random
import math
random.seed(0)
class particle:
    def get_current(self):
        return self.__current
    def get_pbest(self):
        return self.__pbest
    def __init__(self,current,currentb):
        self.__current=current
        self.__pbest=current
        self.__speed=0
        self.__currentb=currentb
        self.__pbestb=currentb
        self.__speedb=0
    def set_current(self,current,currentb):
        self.__current=current
        self.__currentb=currentb
    def set_pbest(self,pbest,pbestb):
        self.__pbset=pbest
        self.__pbestb=pbestb
    def adjust_v(self,C1,C2,gbest,gbestb,Vmax):
        self.__speed=self.__speed+C1*self.rand01()*(self.__pbest-self.__current)+C2*self.rand01()*(gbest-self.__current)
        self.__speedb=self.__speedb+C1*self.rand01()*(self.__pbestb-self.__currentb)+C2*self.rand01()*(gbestb-self.__currentb)
        if self.__speed>Vmax:
            self.__speed=Vmax
        if self.__speedb>Vmax:
            self.__speedb=Vmax
    def get_speed(self):
        return self.__speed
    def rand01(self):
        r=random.random()
        print str(r)
        return r
    def get_currentb(self):
        return self.__currentb
    def get_pbestb(self):
        return self.__pbestb
    def get_speedb(self):
        return self.__speedb
