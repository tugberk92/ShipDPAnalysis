import ROOT as r

#f0=open('s.txt','r')

#f1=open('cs.txt','r')

f0=open('pbrem.txt','r')

f1=open('pa.txt','r')

l_f0=f0.readlines() 

l_f1=f1.readlines()

def find(x_i,l_i):
    for i in l_i:
        i=i.replace('\n','')
        #print i
        if x_i==i:
            #print i
            return True
    return False

for i in l_f0:
    i=i.replace('\n','')
    i=i.split(' ')
    if i[0]=='meson': x1=i[0]+'_'+i[1]+'_mass'+i[2]+'_eps'+i[3]+'_Ana.root'
    if not i[0]=='meson': x1=i[0]+'_mass'+i[1]+'_eps'+i[2]+'_Ana.root'
    #x1 = i+'_Ana.root'
    t1=find(x1,l_f1)
    if not t1: print i[0], i[1], i[2]
    #if not t1: print x1
