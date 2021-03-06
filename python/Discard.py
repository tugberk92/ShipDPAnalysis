from array import array
import os,sys,getopt
from decimal import Decimal

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:", ["date="]) 
except getopt.GetoptError:
    sys.exit()

for o,a in opts:
    if o in ('-d','--date',): date = a

#prods=['meson_pi0','meson_omega','meson_eta','meson_eta1']
#prods=['meson_pi0','meson_omega','meson_eta','meson_eta1','pbrem','pbrem1','qcd']
#prods=['meson','meson_pi0','meson_omega','meson_eta','meson_eta1','qcd']
#prods=['meson','meson_pi0','meson_omega','meson_eta','meson_eta1','pbrem','pbrem1','qcd']
#prods=['meson_pi0','meson_omega','meson_eta','meson_eta1','meson_eta11','pbrem','pbrem1','qcd']
#prods = ['meson','pbrem','pbrem1','comb','comb1','meson','qcd']
#prods = ['meson','pbrem','pbrem1','meson','qcd']
#prods = ['pbrem','pbrem1']
#prods = ['ALPACA']
prods=['meson']
#for i in {'Rate1','ErrorRateP','ErrorRateM'}:
#prods = ['meson']
for prod in prods:
    #inp="../data/"+date+"/"+prod+"_"+i+".dat"
    inp="../data/"+date+"/"+prod+"_rate1.dat"
    outp=inp.replace("rate1","Rate1")
    f=open(inp,'r')
    k=f.readlines()
    l=open(outp,'w')
    for x in k:
        x=x.replace("\n","")
        x=x.split(" ")
        if prod=='meson_eta11' and Decimal(x[3]):
            l.write('%.5E %.9E %.9E' %(Decimal(x[0]),Decimal(x[1]),Decimal(float(x[3]))))
            l.write('\n')
        if prod!='meson_eta11' and Decimal(x[2]):
            l.write('%.5E %.9E %.9E' %(Decimal(x[0]),Decimal(x[1]),Decimal(float(x[2]))))
            l.write('\n')
f.close()
l.close()
