import os
import sys
import math



 
def dealTextfile(filename,rate,rate1):
    sum=0.0
    file_result=open(filename,'r')
    loop=0
    result=0.0
    for line in file_result:
        line=line.strip('\n')
        line=line.split(':')
        #sum=sum+math.pow(((float(line[1])/0.58)*rate-float(line[2])+rate1),2)
        #sum=sum+math.pow(math.log10(math.fabs((float(line[1])/0.58)))*rate+rate1-float(line[2]),2)
        #sum=sum+math.pow(rate*math.sqrt(math.fabs(float(line[1])/0.58))+rate1-float(line[2]),2)
        sum=sum+math.pow(math.exp((rate*float(line[1])/0.58)**2)+rate1-float(line[2]),2)
        loop+=1
    result=math.sqrt(sum)/loop
    print "count sum is %s,the power is %s "%(str(loop),str(result))
    return result


def expandfeature(filename):
    f_original=open(filename,'r')
    f_result=open(filename+'_feature','w')
    for line in f_original:
        line=line.strip('\n')
        line=line.split(':')
        newvalue=float(line[1])/0.58
        f_result.write(line[0]+':'+str(newvalue)+':'+str((0.05*newvalue+1.09)**2)+':'+str((newvalue+1.06)**5)+':'+str((1.0/newvalue)**-5)+':'+str(math.log10(math.fabs(newvalue)))+':'+str(math.sqrt(math.fabs(newvalue)))+':'+str(float(line[2])))
        f_result.write('\n')
    f_original.close()
    f_result.close()
    return filename+'_feature'
