#coding:utf-8
import math
import random
import string
import os
import argparse

random.seed(0)
def rand(a, b):
    return (b-a)*random.random() + a
def readfile(filename):  # n is represent for number of feature 
    pat=[]
    num=0
    if not os.path.isfile(filename):
        raise TypeError('file is not a file or not exits')
    f_file=open(filename,'r')
    for line in f_file:
        alllist=[[] for i in range(2)]
        line=line.strip('\n')
        line=line.split(':')
        length=len(line)
        feature=[[]for i in range(length-2)]
        for i in range(length-2):
            feature[i]=float(line[i+1])
        alllist.append(feature)
        alllist.append(float(line[length-1]))
        pat.append(alllist)
        num=length-2
    return (num,pat)  

def makeMatrix(I,J,fill=0.0):
    m=[]
    for i in range(I):
        m.append(fill*J)
    return m
def sigmoid(x):
    return 0.05*x+1.09

def dsigmoid(y):
    return 1-y**2


class NN:
    '''tree level for BP'''
    def __init__(self,ni,nh,no):
        '''ni represents points of input level'''
        '''nh represent points of hidden level'''
        '''no represents points of output level'''
        self.ni=ni+1     
        self.nh=nh      
        self.no=no       
      
        '''activate all points (vector)'''
        self.ai=[1.0]*self.ni
        self.ah=[1.0]*self.nh
        self.ao=[1.0]*self.no


       # establish weight (matrix)
        self.wi=makeMatrix(self.ni,self.nh)
        self.wo=makeMatrix(self.nh,self.no)
       
      # establish the random number for weights
        for i in range(self.ni):
            for j in range(self.nh):
                one=-0.2
                two=0.2
                self.wi[i][j] = rand(one, two)
                #self.wi[i][j]=randNum(-0.2, 0.2)
        for i in range(self.nh):
            for j in range(self.no):
                self.wo[i][j]=rand(-2.0, 2.0)
       #establish momentum facor(matrix)
        self.ci=makeMatrix(self.ni,self.nh)
        self.co=makeMatrix(self.nh,self.no)
    def update(self,inputs):
        if len(inputs)!=self.ni-1:
            raise ValueError('don\'t not tally with the number of input nodes')
        for i in range(self.ni-i):  #activate input level
            self.ai[i]=inputs[i]



        for j  in range(self.nh):#activate hidden level
            sum=0.0
            for i in range(self.ni):
                sum=sum+self.ai[i]*self.wi[i][j]
            self.ah[j]=sigmod(sum) 
        for k in range(self.no):   #activate output level
            sum=0.0
            for j in range(self.nh):
                sum=sum+self.ah[j]*self.wo[j][k]
            self.ao[k]=sigmod(sum)
        return self.ao[:]
    def backPropagate(self,targets,N,M):
        '''back for change weights'''
        if len(targets)!=self.no:
            raise ValueError('don\'t not tally with the number of output nodes') 
        #deltas output
        output_deltas=[0.0]*self.no
        for k in range(self.no):
            error=target[k]-self.ao[k]
            output_deltas[k]=dsigmoid(self.ao[k])*error
        #deltas hidden
        hidden_deltas=[0.0]*self.nh
        for j in range(self.nh):
            error=0.0
            for k in range(self.no):
                error=error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j]=dsigmoid(self.ah[j])*error
        #update output weight
        for j in range(self.nh):
            for k in range(self.no):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k]=self.wo[j][k]+N*change+M*self.co[j][k]
                self.co[j][k]=change
                print(N*change,M*self.co[j][k])
        #update input weight
        for i in range(self.ni):
            for j in range(self.nh):
                change=hidden_deltas[j]*self.ai[i]
                self.wi[i][j]=self.wi[i][j]+N*change+M*self.ci[i][j]
                self.ci[i][j]=change
        
        #caculate error
        error=0.0
        for k in range(len(targets)):
            error=error+0.5(targets[k]-self.ao[k])**2
        return error
    def test(self,patterns):
        for p in patterns:
            print (p[0],'->',self.update(p[0]))
    

    def weights(self):
        print(' weights of inputs:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('weights of outputs:')
        for j  in range(self.nh):
            print(self.wo[j])
    def train(self,patterns,iteractions=1000,N=0.5,M=0.1):
        #N->(learining rate)
        #M->(momentum factor)
        for i in range(iterations):
            error=0.0
            for p in patterns:
                inputs=p[0]
                targets=p[1]
                self.update(inputs)
                error=error+self.backPropagate(targets,N,M)

            if i%100==0:
                print('error %-.5f' %error)

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('-f', action='store', required=True, dest='trainfile',
                    help='file for train')
    inputs=parser.parse_args()
    pointNum,pat=readfile(inputs.trainfile)
    print('file read over ,the train has began please wait for a momment')
    n=NN(pointNum,pointNum,1)
    n.train(pat)
    n.weights()


if __name__=="__main__":
    main()
