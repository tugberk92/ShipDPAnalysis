import ROOT as r
from array import array
import os,sys,getopt
 
try:
    opts, args = getopt.getopt(sys.argv[1:], "a:p:d:")

except getopt.GetoptError:
    print 'no file'
    sys.exit()

for o,a in opts:
    if o in ('-a',): analysis = a
    if o in ('-p',): prod = a
    if o in ('-d',): date = a
    if o in ('-l',): leptophilic = a

pathR = "../data/"+date+"/"

f=open(pathR+prod+"_"+analysis+'_fra.txt','r')

#f=open(prod+"_"+analysis+'_fra.txt','r')
a=f.readlines()
#leg=r.TLegend(0.9 , 0.8, 1., 1.)
c1  = r.TCanvas('c1', '',1920,1080)

br  = r.TMultiGraph()
gen = r.TMultiGraph()
vtx = r.TMultiGraph()
e_mass, mu_mass,    tau_mass,   pi_mass,    ka_mass,    pi4_mass,   pi3_mass,   pi0_mass,  oth_mass,   mix_mass,   single_mass = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
e_br,   mu_br,      tau_br,     pi_br,      ka_br,      pi4_br,     pi3_br,     pi0_br,    oth_br,     mix_br,     single_br   = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
e_vtx,  mu_vtx,     tau_vtx,    pi_vtx,     ka_vtx,     pi4_vtx,    pi3_vtx,    pi0_vtx,   oth_vtx,    mix_vtx = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
e_gen,  mu_gen,     tau_gen,    pi_gen,     ka_gen,     pi4_gen,    pi3_gen,    pi0_gen,   oth_gen,    mix_gen = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
for i in a:
    j=i.split(' ')
    if j[0]=='e': 
       # print float(j[1]) 
        e_mass.append(float(j[1]))
        e_br.append(float(j[2]))
        e_gen.append(float(j[3]))
        e_vtx.append(float(j[4]))
    elif j[0]=='mu':
        mu_mass.append(float(j[1]))
        mu_br.append(float(j[2]))
        mu_gen.append(float(j[3]))
        mu_vtx.append(float(j[4]))
    elif j[0]=='tau':
        tau_mass.append(float(j[1]))
        tau_br.append(float(j[2]))
        tau_gen.append(float(j[3]))
        tau_vtx.append(float(j[4]))
    elif j[0]=='pi':
        pi_mass.append(float(j[1]))
        pi_br.append(float(j[2]))
        pi_gen.append(float(j[3]))
        pi_vtx.append(float(j[4]))
    elif j[0]=='ka':
        ka_mass.append(float(j[1]))
        ka_br.append(float(j[2]))
        ka_gen.append(float(j[3]))
        ka_vtx.append(float(j[4]))
    elif j[0]=='4pi':
        pi4_mass.append(float(j[1]))
        pi4_br.append(float(j[2]))
        pi4_gen.append(float(j[3]))
        pi4_vtx.append(float(j[4]))
    elif j[0]=='3pi':
        pi3_mass.append(float(j[1]))
        pi3_br.append(float(j[2]))
        pi3_gen.append(float(j[3]))
        pi3_vtx.append(float(j[4]))
    elif j[0]=='2pi0':
        pi0_mass.append(float(j[1]))
        pi0_br.append(float(j[2]))
        pi0_gen.append(float(j[3]))
        pi0_vtx.append(float(j[4]))
    elif j[0]=='oth':
        oth_mass.append(float(j[1]))
        oth_br.append(float(j[2]))
        oth_gen.append(float(j[3]))
        oth_vtx.append(float(j[4]))
    elif j[0]=='single':
        single_mass.append(float(j[1]))
        single_br.append(float(j[2]))

if len(e_mass)!=0.:
    n=len(e_mass)
    #print e_br
    e_Br=r.TGraph(n,e_mass,e_br)
    e_Gen=r.TGraph(len(e_mass),e_mass,e_gen)
    e_Vtx=r.TGraph(len(e_mass),e_mass,e_vtx)
    e_Br.SetName("e_Br")
    e_Gen.SetName("e_Gen")
    e_Vtx.SetName("e_Vtx")
    e_Br.SetMarkerColor(2)
    e_Gen.SetMarkerColor(2)
    e_Vtx.SetMarkerColor(2)
    e_Br.SetMarkerStyle(39)
    e_Gen.SetMarkerStyle(43)
    e_Vtx.SetMarkerStyle(43)
    e_Br.SetLineColor(2)
    e_Gen.SetLineColor(2)
    e_Vtx.SetLineColor(2)
    e_Br.SetLineWidth(3)
    e_Gen.SetLineWidth(3)
    e_Vtx.SetLineWidth(3)
    e_Br.SetTitle("e^{+} + e^{-}") 
    e_Gen.SetTitle("e^{+} + e^{-}")
    e_Vtx.SetTitle("e^{+} + e^{-}")
    e_Br.SetFillStyle(0) 
    e_Gen.SetFillStyle(0)
    e_Vtx.SetFillStyle(0)
    e_Br.SetDrawOption("ALP")
    e_Gen.SetDrawOption("AP")
    e_Vtx.SetDrawOption("AP")
    br.Add(e_Br)
    gen.Add(e_Gen)
    vtx.Add(e_Vtx)
if len(mu_mass)!=0.:
    mu_Br=r.TGraph(len(mu_mass),mu_mass,mu_br)
    mu_Gen=r.TGraph(len(mu_mass),mu_mass,mu_gen)
    mu_Vtx=r.TGraph(len(mu_mass),mu_mass,mu_vtx)
    mu_Br.SetName("mu_Br")
    mu_Gen.SetName("mu_Gen")
    mu_Vtx.SetName("mu_Vtx")
    mu_Br.SetMarkerColor(3)
    mu_Gen.SetMarkerColor(3)
    mu_Vtx.SetMarkerColor(3)
    mu_Br.SetMarkerStyle(20)
    mu_Gen.SetMarkerStyle(20)
    mu_Vtx.SetMarkerStyle(20)
    mu_Br.SetLineColor(3)
    mu_Gen.SetLineColor(3)
    mu_Vtx.SetLineColor(3)
    mu_Br.SetLineWidth(3)
    mu_Gen.SetLineWidth(3)
    mu_Vtx.SetLineWidth(3)
    mu_Br.SetTitle("#mu^{+} + #mu^{-}") 
    mu_Gen.SetTitle("#mu^{+} + #mu^{-}")
    mu_Vtx.SetTitle("#mu^{+} + #mu^{-}")
    mu_Br.SetFillStyle(0) 
    mu_Gen.SetFillStyle(0)
    mu_Vtx.SetFillStyle(0)
    mu_Br.SetDrawOption("ALP")
    mu_Gen.SetDrawOption("AP")
    mu_Vtx.SetDrawOption("AP")
    br.Add(mu_Br)
    gen.Add(mu_Gen)
    vtx.Add(mu_Vtx)
if len(tau_mass)!=0.:
    tau_Br=r.TGraph(len(tau_mass),tau_mass,tau_br)
    tau_Gen=r.TGraph(len(tau_mass),tau_mass,tau_gen)
    tau_Vtx=r.TGraph(len(tau_mass),tau_mass,tau_vtx)
    tau_Br.SetName("tau_Br")
    tau_Gen.SetName("tau_Gen")
    tau_Vtx.SetName("tau_Vtx")
    tau_Br.SetMarkerColor(93)
    tau_Gen.SetMarkerColor(93)
    tau_Vtx.SetMarkerColor(93)
    tau_Br.SetMarkerStyle(21)
    tau_Gen.SetMarkerStyle(21)
    tau_Vtx.SetMarkerStyle(21)
    tau_Br.SetLineColor(93)
    tau_Gen.SetLineColor(93)
    tau_Vtx.SetLineColor(93)
    tau_Br.SetLineWidth(3)
    tau_Gen.SetLineWidth(3)
    tau_Vtx.SetLineWidth(3)
    tau_Br.SetTitle("#tau^{+} + #tau^{-}") 
    tau_Gen.SetTitle("#tau^{+} + #tau^{-}")
    tau_Vtx.SetTitle("#tau^{+} + #tau^{-}")
    tau_Br.SetFillStyle(0) 
    tau_Gen.SetFillStyle(0)
    tau_Vtx.SetFillStyle(0)
    tau_Br.SetDrawOption("ALP")
    tau_Gen.SetDrawOption("AP")
    tau_Vtx.SetDrawOption("AP")
    br.Add(tau_Br)
    gen.Add(tau_Gen)
    vtx.Add(tau_Vtx)
if len(pi_mass)!=0.:
    pi_Br=r.TGraph(len(pi_mass),pi_mass,pi_br)
    pi_Gen=r.TGraph(len(pi_mass),pi_mass,pi_gen)
    pi_Vtx=r.TGraph(len(pi_mass),pi_mass,pi_vtx)
    pi_Br.SetName("pi_Br")
    pi_Gen.SetName("pi_Gen")
    pi_Vtx.SetName("pi_Vtx")
    pi_Br.SetMarkerColor(5)
    pi_Gen.SetMarkerColor(5)
    pi_Vtx.SetMarkerColor(5)
    pi_Br.SetMarkerStyle(22)
    pi_Gen.SetMarkerStyle(22) 
    pi_Vtx.SetMarkerStyle(22)
    pi_Br.SetLineColor(5)
    pi_Gen.SetLineColor(5)
    pi_Vtx.SetLineColor(5)
    pi_Br.SetLineWidth(3)
    pi_Gen.SetLineWidth(3)
    pi_Vtx.SetLineWidth(3)
    pi_Br.SetTitle("#pi^{+} + #pi^{-}") 
    pi_Gen.SetTitle("#pi^{+} + #pi^{-}")
    pi_Vtx.SetTitle("#pi^{+} + #pi^{-}")
    pi_Br.SetFillStyle(0) 
    pi_Gen.SetFillStyle(0)
    pi_Vtx.SetFillStyle(0)
    pi_Br.SetDrawOption("ALP")
    pi_Gen.SetDrawOption("AP")
    pi_Vtx.SetDrawOption("AP")
    br.Add(pi_Br)
    gen.Add(pi_Gen)
    vtx.Add(pi_Vtx)
if len(ka_mass)!=0.:
    ka_Br=r.TGraph(len(ka_mass),ka_mass,ka_br)
    ka_Gen=r.TGraph(len(ka_mass),ka_mass,ka_gen)
    ka_Vtx=r.TGraph(len(ka_mass),ka_mass,ka_vtx)
    ka_Br.SetName("ka_Br")
    ka_Gen.SetName("ka_Gen")
    ka_Vtx.SetName("ka_Vtx")
    ka_Br.SetMarkerColor(7)
    ka_Gen.SetMarkerColor(7)
    ka_Vtx.SetMarkerColor(7)
    ka_Br.SetMarkerStyle(23)
    ka_Gen.SetMarkerStyle(23) 
    ka_Vtx.SetMarkerStyle(23)
    ka_Br.SetLineColor(7)
    ka_Gen.SetLineColor(7)
    ka_Vtx.SetLineColor(7)
    ka_Br.SetLineWidth(3)
    ka_Gen.SetLineWidth(3)
    ka_Vtx.SetLineWidth(3)
    ka_Br.SetTitle("K^{+} + K^{-}") 
    ka_Gen.SetTitle("K^{+} + K^{-}")
    ka_Vtx.SetTitle("K^{+} + K^{-}")
    ka_Br.SetFillStyle(0) 
    ka_Gen.SetFillStyle(0)
    ka_Vtx.SetFillStyle(0)
    ka_Br.SetDrawOption("ALP")
    ka_Gen.SetDrawOption("AP")
    ka_Vtx.SetDrawOption("AP")
    br.Add(ka_Br)
    gen.Add(ka_Gen)
    vtx.Add(ka_Vtx)
if len(pi4_mass)!=0.:
    pi4_Br=r.TGraph(len(pi4_mass),pi4_mass,pi4_br)
    pi4_Gen=r.TGraph(len(pi4_mass),pi4_mass,pi4_gen)
    pi4_Vtx=r.TGraph(len(pi4_mass),pi4_mass,pi4_vtx)
    pi4_Br.SetName("pi4_Br")
    pi4_Gen.SetName("pi4_Gen")
    pi4_Vtx.SetName("pi4_Vtx")
    pi4_Br.SetMarkerColor(58)
    pi4_Gen.SetMarkerColor(58)
    pi4_Vtx.SetMarkerColor(58)
    pi4_Br.SetMarkerStyle(33) 
    pi4_Gen.SetMarkerStyle(33)
    pi4_Vtx.SetMarkerStyle(33)
    pi4_Br.SetLineColor(58)
    pi4_Gen.SetLineColor(58)
    pi4_Vtx.SetLineColor(58)
    pi4_Br.SetLineWidth(3)
    pi4_Gen.SetLineWidth(3)
    pi4_Vtx.SetLineWidth(3)
    pi4_Br.SetTitle("2x(#pi^{+} + #pi^{-})") 
    pi4_Gen.SetTitle("2x(#pi^{+} + #pi^{-})")
    pi4_Vtx.SetTitle("2x(#pi^{+} + #pi^{-})")
    pi4_Br.SetFillStyle(0) 
    pi4_Gen.SetFillStyle(0)
    pi4_Vtx.SetFillStyle(0)
    pi4_Br.SetDrawOption("ALP")
    pi4_Gen.SetDrawOption("AP")
    pi4_Vtx.SetDrawOption("AP")
    br.Add(pi4_Br)
    gen.Add(pi4_Gen)
    vtx.Add(pi4_Vtx)
if len(pi3_mass)!=0.:
    pi3_Br=r.TGraph(len(pi3_mass),pi3_mass,pi3_br)
    pi3_Gen=r.TGraph(len(pi3_mass),pi3_mass,pi3_gen)
    pi3_Vtx=r.TGraph(len(pi3_mass),pi3_mass,pi3_vtx)
    pi3_Br.SetName("pi3_Br")
    pi3_Gen.SetName("pi3_Gen")
    pi3_Vtx.SetName("pi3_Vtx")
    pi3_Br.SetMarkerColor(51)
    pi3_Gen.SetMarkerColor(51)
    pi3_Vtx.SetMarkerColor(51)
    pi3_Br.SetMarkerStyle(29) 
    pi3_Gen.SetMarkerStyle(29)
    pi3_Vtx.SetMarkerStyle(29)
    pi3_Br.SetLineColor(51)
    pi3_Gen.SetLineColor(51)
    pi3_Vtx.SetLineColor(51)
    pi3_Br.SetLineWidth(3)
    pi3_Gen.SetLineWidth(3)
    pi3_Vtx.SetLineWidth(3)
    pi3_Br.SetTitle("#pi^{+} + #pi^{-} + #pi^{0}") 
    pi3_Gen.SetTitle("#pi^{+} + #pi^{-} + #pi^{0}")
    pi3_Vtx.SetTitle("#pi^{+} + #pi^{-} + #pi^{0}")
    pi3_Br.SetFillStyle(0) 
    pi3_Gen.SetFillStyle(0)
    pi3_Vtx.SetFillStyle(0)
    pi3_Br.SetDrawOption("ALP")
    pi3_Gen.SetDrawOption("AP")
    pi3_Vtx.SetDrawOption("AP")
    br.Add(pi3_Br)
    gen.Add(pi3_Gen)
    vtx.Add(pi3_Vtx)
if len(pi0_mass)!=0.:
    pi0_Br=r.TGraph(len(pi0_mass),pi0_mass,pi0_br)
    pi0_Gen=r.TGraph(len(pi0_mass),pi0_mass,pi0_gen)
    pi0_Vtx=r.TGraph(len(pi0_mass),pi0_mass,pi0_vtx)
    pi0_Br.SetName("pi0_Br")
    pi0_Gen.SetName("pi0_Gen")
    pi0_Vtx.SetName("pi0_Vtx")
    pi0_Br.SetMarkerColor(6)
    pi0_Gen.SetMarkerColor(6)
    pi0_Vtx.SetMarkerColor(6)
    pi0_Br.SetMarkerStyle(34) 
    pi0_Gen.SetMarkerStyle(34)
    pi0_Vtx.SetMarkerStyle(34)
    pi0_Br.SetLineColor(6)
    pi0_Gen.SetLineColor(6)
    pi0_Vtx.SetLineColor(6)
    pi0_Br.SetLineWidth(3)
    pi0_Gen.SetLineWidth(3)
    pi0_Vtx.SetLineWidth(3)
    pi0_Br.SetTitle("#pi^{+} + #pi^{-} + 2x #pi^{0}") 
    pi0_Gen.SetTitle("#pi^{+} + #pi^{-} + 2x #pi^{0}")
    pi0_Vtx.SetTitle("#pi^{+} + #pi^{-} + 2x #pi^{0}")
    pi0_Br.SetFillStyle(0) 
    pi0_Gen.SetFillStyle(0)
    pi0_Vtx.SetFillStyle(0)
    pi0_Br.SetDrawOption("ALP")
    pi0_Gen.SetDrawOption("AP")
    pi0_Vtx.SetDrawOption("AP")
    br.Add(pi0_Br)
    gen.Add(pi0_Gen)
    vtx.Add(pi0_Vtx)
if len(oth_mass)!=0.:
    oth_Br=r.TGraph(len(oth_mass),oth_mass,oth_br)
    oth_Br.SetName("oth_Br")
    oth_Br.SetMarkerColor(28)
    oth_Br.SetMarkerStyle(47)
    oth_Br.SetLineColor(28)
    oth_Br.SetLineWidth(3)
    oth_Br.SetTitle("Unstable Hadrons") 
    oth_Br.SetFillStyle(0) 
    oth_Br.SetDrawOption("ALP")
    br.Add(oth_Br)
if len(single_mass)!=0.:
    single_Br=r.TGraph(len(single_mass),single_mass,single_br)
    single_Br.SetName("single_Br")
    single_Br.SetMarkerColor(1)
    single_Br.SetMarkerStyle(41)
    single_Br.SetLineColor(1)
    single_Br.SetLineWidth(3)
    single_Br.SetTitle("Untagged Hadrons") 
    single_Br.SetFillStyle(0) 
    single_Br.SetDrawOption("ALP")
    br.Add(single_Br)

 
br.SetTitle(";Mass(GeV);Branching Ratios")
br.Draw("ALP")
c1.BuildLegend()
c1.Update()
c1.Print(pathR+prod+"_"+analysis+"_br.root")

if analysis=='Dau':gen.SetTitle(";Mass(GeV);Vessel Probability from Direct Decay Products")
else: gen.SetTitle(";Mass(GeV);Vessel Probability from Final-State Particles")
gen.Draw("AP")
c1.BuildLegend()
c1.Update()
c1.Print(pathR+prod+"_"+analysis+"_gen.root")

if analysis=='Dau': vtx.SetTitle(";Mass(GeV);Geometrical Acceptance from Direct Decay Products")
else: vtx.SetTitle(";Mass(GeV);Geometrical Acceptance from Final-State Particles")
vtx.Draw("AP")
c1.BuildLegend()
c1.Update()
c1.Print(pathR+prod+"_"+analysis+"_vtx.root")
