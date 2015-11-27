#coding:utf-8
import os
#import argparse
import math
import random
import string
import sys
import pdb
import learnParameters
print sys.getdefaultencoding()
random.seed(0)

def rand(a, b):
    return (b-a)*random.random() + a
def writeTrainWeights(filename):
    f_train=open(filename,'w')
    for i in xrange(10):
        f_train.write(str(1000)+':'+str(rand(0,0.9))+':'+str(rand(0,0.7)))
        f_train.write('\n')
    f_train.close()
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
        alllist[0]=feature
        newlist=[]
        if str(line[length-1])=='hotspot':
            newlist.append(1)
        else:
            newlist.append(0)
        alllist[1]=newlist
       # pdb.set_trace()
        pat.append(alllist)
        num=length-2
    return (num,pat)  
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

def sigmoid(x):
    return math.tanh(x-2.0)
    #return 1.0/(1.0+math.exp(-x)) 

def dsigmoid(y):
    #print('y=%f' %y)
    #pdb.set_trace()
    return 1.0-y**2 
    #return y
class NN:
    def __init__(self, ni, nh, no):
        self.ni = ni + 1 
        self.nh = nh
        self.no = no

        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            print('len(inputs):%d,%d' %(len(inputs),self.ni-1))
            raise ValueError('error for inputs number')

        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('error of input number')

        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print(N*change, M*self.co[j][k])

        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error

    def test(self, patterns):
        for p in patterns:
            print(p[0], '->', self.update(p[0]))

    def weights(self):
        for i in range(self.ni):
            print(self.wi[i])
        print('next is ')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=1000, N=0.05, M=0.08):
        sum=0.0
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print('error of 100= %-.5f' % error)
            sum=sum+error
        print('aravege error is %-.5f'%(sum/iterations))
        return (sum/iterations)
def psolearn(trainfile,N_value,M_value):
    pointNum,pat=readfile(trainfile)
    print('file read over ,the train has began please wait for a momment')
    n=NN(pointNum,pointNum,1)
    #for i in xrange(100):
    iterations=1000
    value=n.train(pat,iterations,N_value,M_value)
    #n.weights()
    return value
def demo():
   
    parser=argparse.ArgumentParser()
    parser.add_argument('-f', action='store', required=True, dest='trainfile',
                    help='file for train')
    parser.add_argument('-w', action='store', required=True, dest='weightfile',
                    help='weight file for train')
    inputs=parser.parse_args()
    writeTrainWeights(inputs.weightfile)
    pointNum,pat=readfile(learnParameters.expandfeature(inputs.trainfile))
    print pat
    print('file read over ,the train has began please wait for a momment')
    n=NN(pointNum,pointNum,1)
    #for i in xrange(100):
    f_wfile=open(inputs.weightfile,'r')
    for line in f_wfile:
        line=line.strip('\n')
        line=line.split(':')
        iterations=int(line[0])
        N_value=float(line[1])
        M_value=float(line[2])
        print('iterations=%d,N=%f,M=%f'%(iterations,N_value,M_value))
        n.train(pat,iterations,N_value,M_value)
        n.weights()
        print('Next paratermeters........')
    f_wfile.close()
if __name__ == '__main__':
    demo()
