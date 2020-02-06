date='200205'

mothers=['pi0','eta','omega','eta1']
for mother in mothers:
    exec('f1_%s = open("../data/"+date+"/meson_%s"+"_rate1.dat","r")'%(mother,mother))
    exec('l1_%s = f1_%s.readlines() '%(mother,mother))

f0 = open("mr.txt","r")#dosya lazim
l0 = f0.readlines()

f1 = open("../data/"+date+"/meson_rate1.dat","w")

def find(mother,l0,l_i):
    for i in l_i:
        i=i.replace('\n','')
        i = i.split(' ')
        if float(l0[0])==float(i[0]) and float(l0[1])==float(i[1]):
            if mother == "eta1" and (float(i[2]) or float(i[3])): return float(i[2])+float(i[3])
            if mother != "eta1" and float(i[2]): return float(i[2])
    return 0.


for i in l0:
    s1,s2 = 0.,0.
    i=i.replace('\n','')
    i=i.split(' ')
    for mother in mothers:
        exec('s1 += find("%s",i,l1_%s)'%(mother,mother))
    if s1:
        f1.write('%s %s %s'%(i[0],i[1],s1))
        f1.write('\n')

