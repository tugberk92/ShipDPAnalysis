import ROOT as r
import os,sys,getopt
import rootUtils as ut
import shipunit as u
import darkphoton
from ShipGeoConfig import ConfigRegistry 
from decorators import *
from rootpyPickler import Unpickler
from array import array
import shipRoot_conf
import dpProductionRates as dputil
import math as m
import numpy as np
shipRoot_conf.configure()
dpMom = '' 

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:p:m:e:A:g:f:", ["date=","production=","mass=","epsilon=","motherID=","geoFile=","final_dest="])
except getopt.GetoptError:
    print 'no file'
    sys.exit()
for o,a in opts:
    if o in ('-d',): date = a
    if o in ('-p',): pro = a
    if o in ('-m',): mass_mc = a
    if o in ('-e',): eps = a
    if o in ('-A',): dpMom = a
    if o in ('-g', '--geoFile',): geoFile = a
    if o in ('-f',): dest = a

if dpMom!='': tmp1 = "/eos/experiment/ship/data/DarkPhoton/PBC-June-3/"+date+"/reco/"+pro+"_"+dpMom+"_mass"+mass_mc+"_eps"+eps
if dpMom=='': tmp1 = "/eos/experiment/ship/data/DarkPhoton/PBC-June-3/"+date+"/reco/"+pro+"_mass"+mass_mc+"_eps"+eps
if pro=="pbrem1": tmp1 = "/eos/experiment/ship/data/DarkPhoton/PBC-June-3/"+date+"/reco/pbrem_mass"+mass_mc+"_eps"+eps
inputFile = tmp1+"_rec.root"
print inputFile
mass_mc=float(mass_mc)
eps=float(eps)
 

eosship =  r.gSystem.Getenv("EOSSHIP")
eospath = eosship+inputFile
f = r.TFile.Open(eospath)
sTree=f.cbmsim
eospath = eosship+geoFile
fgeo = r.TFile.Open(eospath)
sGeo = r.gGeoManager

upkl    = Unpickler(fgeo)
ShipGeo = upkl.load('ShipGeo')
ecalGeoFile = ShipGeo.ecal.File
hcalGeoFile = ShipGeo.hcal.File 
dy = ShipGeo.Yheight/u.m
MeasCut=25

# -----Create geometry----------------------------------------------
import shipDet_conf
run = r.FairRunSim()
run.SetName("TGeant4")  # Transport engine
run.SetOutputFile(ROOT.TMemFile('output', 'recreate'))  # Output file
run.SetUserConfig("g4Config_basic.C") # geant4 transport not used, only needed for the mag field

# -----Create geometry----------------------------------------------
modules = shipDet_conf.configure(run,ShipGeo)

import geomGeant4
if hasattr(ShipGeo.Bfield,"fieldMap"):
  fieldMaker = geomGeant4.addVMCFields(ShipGeo, '', True, withVirtualMC = False)
else:
  print "no fieldmap given, geofile too old, not anymore support"
  exit(-1)
sGeo   = fgeo.FAIRGeom
geoMat =  r.genfit.TGeoMaterialInterface()
ROOT.genfit.MaterialEffects.getInstance().init(geoMat)
bfield = r.genfit.FairShipFields()
bfield.setField(fieldMaker.getGlobalField())
fM = r.genfit.FieldManager.getInstance()
fM.init(bfield)

volDict = {}
i=0
for x in ROOT.gGeoManager.GetListOfVolumes():
 volDict[i]=x.GetName()
 i+=1

# prepare veto decisions
import shipVeto
veto = shipVeto.Task(sTree)
vetoDets={}

PDG = r.TDatabasePDG.Instance()

import TrackExtrapolateTool 
targ=r.TVector3(0,0,ShipGeo.target.z0)

h={}
hs={}

ut.bookHist(hs,'DPmom_xf','',40,0.,1.)
ut.bookHist(hs,'DPmom_rapidity','',100,-3.,9)
ut.bookHist(hs,'DPmom_pt2','',400,0.,400.)
ut.bookHist(hs,'DPmom_pz','',100,0.,400.)
ut.bookHist(hs,'DPmom_p','',100,0.,400.)
 
ut.bookHist(hs,'DP_xf','',40,0.,1.)
ut.bookHist(hs,'DP_rapidity','',100,-3.,9)
ut.bookHist(hs,'DP_pt2','',400,0.,400.)
ut.bookHist(hs,'DP_pz','',100,0.,400.)
ut.bookHist(hs,'DP_p','',40,0.,400.)
 
ut.bookHist(hs,'DPmomR_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPmomR_pt2','',400,0.,400.)
ut.bookHist(hs,'DPmomR_pz','',100,0.,400.)
ut.bookHist(hs,'DPmomR_p','',100,0.,400.)
 
ut.bookHist(hs,'DPr_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPr_pt2','',400,0.,400.)
ut.bookHist(hs,'DPr_pz','',100,0.,400.)
ut.bookHist(hs,'DPr_p','',100,0.,400.)

ut.bookHist(hs,'DPmomC3_xf','',40,0.,1.)
ut.bookHist(hs,'DPmomC3_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPmomC3_pz','',100,0.,400.)
ut.bookHist(hs,'DPmomC3_p','',100,0.,400.)
 
ut.bookHist(hs,'DPc3_xf','',40,0.,1.)
ut.bookHist(hs,'DPc3_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPc3_pz','',100,0.,400.)
ut.bookHist(hs,'DPc3_p','',100,0.,400.)
 
ut.bookHist(hs,'DPmomC2_xf','',40,0.,1.)
ut.bookHist(hs,'DPmomC2_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPmomC2_pz','',100,0.,400.)
ut.bookHist(hs,'DPmomC2_p','',100,0.,400.)
 
ut.bookHist(hs,'DPc2_xf','',40,0.,1.)
ut.bookHist(hs,'DPc2_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPc2_pz','',100,0.,400.)
ut.bookHist(hs,'DPc2_p','',100,0.,400.)

ut.bookHist(hs,'DPmomC1_xf','',40,0.,1.)
ut.bookHist(hs,'DPmomC1_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPmomC1_pz','',100,0.,400.)
ut.bookHist(hs,'DPmomC1_p','',100,0.,400.)
 
ut.bookHist(hs,'DPc1_xf','',40,0.,1.)
ut.bookHist(hs,'DPc1_rapidity','',100,-3.,9.)
ut.bookHist(hs,'DPc1_pz','',100,0.,400.)
ut.bookHist(hs,'DPc1_p','',100,0.,400.)
 
tmp1=tmp1.replace(date,dest)
 
tmp2=tmp1.replace("reco","ana")
tmp1=tmp1.replace("reco","ana/dat")

if pro=='pbrem1':
    tmp1=tmp1.replace("pbrem","pbrem1")
    tmp2=tmp2.replace("pbrem","pbrem1")

 
TreeFile=r.TFile(tmp2+"_ProdAna.root",'recreate')
ProdAna=r.TTree("ProdAna","results of the productions")


DP_Pt          =r.std.vector(float)()
DPmom_Pt       =r.std.vector(float)() 
DP_Pz          =r.std.vector(float)()
DPmom_Pz       =r.std.vector(float)()
DP_P          =r.std.vector(float)()
DPmom_P       =r.std.vector(float)()
DP_Rapidity     =r.std.vector(float)()
DPmom_Rapidity  =r.std.vector(float)()
DP_Xf          =r.std.vector(float)()
DPmom_Xf       =r.std.vector(float)()
 
ProdAna.Branch('DP_Xf',DP_Xf) 
ProdAna.Branch('DPmom_Xf',DPmom_Xf) 
ProdAna.Branch('DP_Pt',DP_Pt) 
ProdAna.Branch('DPmom_Pt',DPmom_Pt) 
ProdAna.Branch('DP_P',DP_P) 
ProdAna.Branch('DPmom_P',DPmom_P) 
ProdAna.Branch('DP_Pz',DP_Pz) 
ProdAna.Branch('DPmom_Pz',DPmom_Pz) 
ProdAna.Branch('DP_Rapidity',DP_Rapidity) 
ProdAna.Branch('DPmom_Rapidity',DPmom_Rapidity) 

ut.bookHist(h,'DauPDG','PDG OF Primaries')
ut.bookHist(h,'DPang1','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang1_e','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang1_mu','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang1_tau','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang1_charg','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang1_neut','invariant Mass (GeV)',100,0.,mass_mc+5.)


ut.bookHist(h,'DPang1_oth','invariant Mass (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPW','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpurW','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangWe','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_e','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_e','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_e','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_e','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_e','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_e','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_mu','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_mu','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_mu','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_mu','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_mu','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_mu','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_tau','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_tau','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_tau','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_tau','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_tau','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_tau','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_neut','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_neut','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_neut','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_neut','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_neut','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_neut','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_charg','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_charg','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_charg','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_charg','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_charg','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_charg','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DP_oth','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DP_noth','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPpur_oth','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPves_oth','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPvesW_oth','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPang_oth','invariant Mass (GeV)',100,0.,mass_mc+5.)
ut.bookHist(h,'DPangW_oth','invariant Mass with Weights (GeV)',100,0.,mass_mc+5.)

ut.bookHist(h,'DOCA','Doca between two tracks',100,0.,100)
ut.bookHist(h,'IP','Impact Parameter',100,0.,10.)

def dist2InnerWall(X,Y,Z):
    dist = 0
    node = sGeo.FindNode(X,Y,Z)
    #print node.GetName()
    if ShipGeo.tankDesign < 5:
        if not 'cave' in node.GetName(): return dist  # TP 
    else:
        if not 'decayVol' in node.GetName(): return dist
    start = array('d',[X,Y,Z])
    nsteps = 8
    dalpha = 2*r.TMath.Pi()/nsteps
    rsq = X**2+Y**2
    minDistance = 100 *u.m
    for n in range(nsteps):
        alpha = n * dalpha
        sdir  = array('d',[r.TMath.Sin(alpha),r.TMath.Cos(alpha),0.])
        node = sGeo.InitTrack(start, sdir)
        nxt = sGeo.FindNextBoundary()
        if ShipGeo.tankDesign < 5 and nxt.GetName().find('I')<0: return 0    
        distance = sGeo.GetStep()
        if distance < minDistance  : minDistance = distance
    #print minDistance
    return minDistance

def checkFiducialVolume(sTree,tkey,dy):
# extrapolate track to middle of magnet and check if in decay volume
   inside = True
   #if not fiducialCut: return True
   fT = sTree.FitTracks[tkey]
   rc,pos,mom = TrackExtrapolateTool.extrapolateToPlane(fT,ShipGeo.Bfield.z)
   #print pos.X(), pos.Y(), pos.Z()
   if not rc: 
       #print "rc"
       return False
   if not dist2InnerWall(pos.X(),pos.Y(),pos.Z())>0:
       node = sGeo.FindNode(pos.X(),pos.Y(),pos.Z())
       #print "dist",node.GetName()
       return False
   return inside
print ShipGeo.Bfield.z, ShipGeo.tankDesign
def isInFiducial(X,Y,Z):
    if Z > ShipGeo.TrackStation1.z : return False
    if Z < ShipGeo.vetoStation.z+100.*u.cm : return False
    if dist2InnerWall(X,Y,Z)<5*u.cm: return False
    return True 

def findmum():#this function finds the mother of DP with weight,xs,momentum etc. USED for finding DP event
    for dp_ind,dp_tr in enumerate(sTree.MCTrack):
        if dp_tr.GetPdgCode()==9900015 or dp_tr.GetPdgCode()==4900023:
            mum_id=dp_tr.GetMotherId()
            #print mum_id
            dp_id=dp_ind
            #print dp_id
            if pro=='qcd' and dp_id==0: continue
            #print mum_id 
            mum_pdg=sTree.MCTrack[mum_id].GetPdgCode()
            #print mum_pdg
            if pro=='meson':
                xsw = dputil.getDPprodRate(mass_mc,eps,'meson',mum_pdg)
                if 'eta1' in dpMom and xsw!=0:
                    xsw1=xsw[1]
                    xsw=xsw[0]
            else: xsw = dputil.getDPprodRate(mass_mc,eps,pro,0) 
            #print "bu da farkli", xsw
            wg = sTree.MCTrack[dp_id].GetWeight()
            #print wg
            #print dp_id 
            dp_mom=r.TVector3(sTree.MCTrack[dp_id].GetPx(),sTree.MCTrack[dp_id].GetPy(),sTree.MCTrack[dp_id].GetPz())
            dp_mag=sTree.MCTrack[dp_id].GetP()
            break
        else:
            if 'eta1' in dpMom: xsw,xsw1,wg,dp_id,dp_mom,dp_mag,mum_id=0,0,0,0,0,0,0
            if not 'eta1' in dpMom: xsw,wg,dp_id,dp_mom,dp_mag,mum_id=0,0,0,0,0,0
    if 'eta1' in dpMom: return xsw,xsw1,wg,dp_id,dp_mom,dp_mag,mum_id
    if not 'eta1' in dpMom: return xsw,wg,dp_id,dp_mom,dp_mag,mum_id

def find_signal(pdg):# this function finds the signal tracks. USED for finding signals in fittracks.. It is also looks for pi0 and gamma BUT no gamma or pi0 in FitTracks. So, signals are proton+-, pion+-, kaon+-, electron +- muon +-
    try:
        PRT=PDG.GetParticle(pdg)
        if abs(PRT.Charge())>0 and PRT.Stable(): return True
        else: return False
    except:
        return False

def checkTrue(sTree, dp_id):# this function gives the DP with its direct decay channel USED for finding the DP events with at least two e,mu,tau channel or any chargronic channel from MCTracks.
    #lepto=0
    PID=[]
    for mc,tr in enumerate(sTree.MCTrack):
        pid = tr.GetPdgCode()
        mom = tr.GetMotherId() 
        if mc>1:
            mom_pid=sTree.MCTrack[mom].GetPdgCode()
            if abs(pid)>9 and abs(pid)!=21:
                if mom==dp_id:#leptons in all process and/or chargrons in meson process
                    PID.append(mc)
                elif (abs(mom_pid)<9 or abs(mom_pid)==21):#chargrons in qcd and pbrem
                    PID.append(mc)#I NEED TO THINK OF SMT TO SPLIT NEUTRAL CHANNELS
    return PID

def find_charge(pdg):# this function finds the signal tracks. USED for finding signals in fittracks.. It is also looks for pi0 and gamma BUT no gamma or pi0 in FitTracks. So, signals are proton+-, pion+-, kaon+-, electron +- muon +-
    try:
        PRT=PDG.GetParticle(pdg)
        if abs(PRT.Charge())>0: return True
        else: return False
    except:
        return False

def totCharge(pdg):
    CC=0
    PRT=PDG.GetParticle(pdg)
    if PRT.Charge()>0.:
        CC=+1
        return CC
    elif PRT.Charge()<0.:
        CC=-1
        return CC
    else: return CC

def findStable(pdg):
    try:
        PRT=PDG.GetParticle(pdg)
        if PRT.Stable(): return True
        else: return False
    except:
        return False

def findLepton(pdg):
    if abs(pdg)==11 or abs(pdg)==13 or abs(pdg)==15: return True
    else: return False

def checkLepMode(sTree, dp_id):
    PID=[]
    for mc,tr in enumerate(sTree.MCTrack):
        pid = tr.GetPdgCode()
        mom = tr.GetMotherId() 
        if mc>1:
            mom_pid=sTree.MCTrack[mom].GetPdgCode()
            if abs(pid)>9 and abs(pid)!=21 and findLepton(pid):
                if mom==dp_id:#leptons in all process and/or chargrons in meson process
                    PID.append(mc)
                elif(abs(mom_pid)<9 or abs(mom_pid)==21):#chargrons in qcd and pbrem
                    PID.append(mc)
                #else:
                    #if tr.GetProcID()==0. and findStable(pid): PID.append(mc)
            if tr.GetProcID()!=0.: return PID
    return PID

def checkHadMode(sTree):
    PID=[]
    for mc,tr in enumerate(sTree.MCTrack):
        pid=tr.GetPdgCode()
        if abs(pid)>9 and abs(pid)!=21 and tr.GetProcID()==0. and findStable(pid): PID.append(mc)
        if tr.GetProcID()!=0.: return PID
    return PID

def myEventLoop(n):# Analysis is starting here
    DP_Xf.clear()
    DP_Pt.clear()
    DPmom_Pt.clear()
    DP_P.clear()
    DPmom_P.clear()
    DP_Pz.clear()
    DPmom_Pz.clear()
    DP_Rapidity.clear()
    DPmom_Xf.clear()
    DPmom_Rapidity.clear()

    #print n
    rc=sTree.GetEntry(n) 
    fm=findmum()
    if 'eta1' in dpMom:
        xsw=fm[0]
        xsw1=fm[1]
        wg=fm[2]
        dp_id=fm[3]
        dp_M=fm[4]
        dp_Mag=fm[5]
        mum=fm[6]
    if not 'eta1' in dpMom:
        xsw=fm[0]
        wg=fm[1]
        dp_id=fm[2]
        dp_M=fm[3]
        dp_Mag=fm[4]
        mum=fm[5]
    MA,MAS=[],[] 
    DPmom=r.TLorentzVector(0.,0.,0.,0.)
    DPma=r.TLorentzVector(0.,0.,0.,0.) 
    dau=0
    DOC=[]
    T1,T2=[],[]
    VES=0 
    r_track=0
    f_track=0
    RECO=0
    CE,CM,CT,CH=0,0,0,0
    CHARGE=0
    debug=0
    e, mu, tau, charg, neut, oth_v = 0, 0, 0, 0, 0, 0
    #print "mom find"
    if xsw==0 and wg==0 and dp_id==0: 
        #Dump(sTree.MCTrack)
        return 0
    DPmom_P.push_back(sTree.MCTrack[mum].GetP())
    DPmom_Pz.push_back(sTree.MCTrack[mum].GetPz())
    DPmom_Pt.push_back(sTree.MCTrack[mum].GetPt())
    DPmom_Rapidity.push_back(sTree.MCTrack[mum].GetRapidity())
    DPmom_Xf.push_back(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))

    hs['DPmom_pt2'].Fill(sTree.MCTrack[mum].GetPt()*sTree.MCTrack[mum].GetPt())
    hs['DPmom_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
    hs['DPmom_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
    hs['DPmom_pz'].Fill(sTree.MCTrack[mum].GetPz())
    hs['DPmom_p'].Fill(sTree.MCTrack[mum].GetP())
    if sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP()))<0.3 and sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP()))>0.025:
        #print sTree.MCTrack[mum].GetRapidity()
        hs['DPmomR_pz'].Fill(sTree.MCTrack[mum].GetPz())
        hs['DPmomR_p'].Fill(sTree.MCTrack[mum].GetP())
        hs['DPmomR_pt2'].Fill(sTree.MCTrack[mum].GetPt()*sTree.MCTrack[mum].GetPt())
        hs['DPmomR_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
    if sTree.MCTrack[mum].GetPt()>3.5:
        hs['DPmomC3_pz'].Fill(sTree.MCTrack[mum].GetPz())
        hs['DPmomC3_p'].Fill(sTree.MCTrack[mum].GetP())
        hs['DPmomC3_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
        hs['DPmomC3_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
    if sTree.MCTrack[mum].GetPt()>2.0:
        hs['DPmomC2_pz'].Fill(sTree.MCTrack[mum].GetPz())
        hs['DPmomC2_p'].Fill(sTree.MCTrack[mum].GetP())
        hs['DPmomC2_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
        hs['DPmomC2_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
    if sTree.MCTrack[mum].GetPt()>1.0:
        hs['DPmomC1_pz'].Fill(sTree.MCTrack[mum].GetPz())
        hs['DPmomC1_p'].Fill(sTree.MCTrack[mum].GetP())
        hs['DPmomC1_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
        hs['DPmomC1_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())


    h['DPW'].Fill(mass_mc) 
    dau=checkLepMode(sTree,dp_id) 
    for xxx in dau:
        pid = sTree.MCTrack[xxx].GetPdgCode()
        h['DauPDG'].Fill(pid)
        CHARGE+=abs(totCharge(pid))
        if abs(pid)==11:
            doca=sTree.MCTrack[xxx].GetStartT()
            e+=1
            CE+=totCharge(pid)
        if abs(pid)==13:
            doca=sTree.MCTrack[xxx].GetStartT()
            mu+=1
            CM+=totCharge(pid)
        if abs(pid)==15:
            doca=sTree.MCTrack[xxx].GetStartT()
            tau+=1
            CT+=totCharge(pid)
    if not dau:
        dau=checkHadMode(sTree)
        for xxx in dau:
            pid=sTree.MCTrack[xxx].GetPdgCode()
            doca=sTree.MCTrack[xxx].GetStartT() 
            CHARGE+=abs(totCharge(pid))
            h['DauPDG'].Fill(pid)
            if not find_charge(pid):
                neut+=1
            elif find_charge(pid):
                charg+=1
            else: print pid 
    try:
        tug = sTree.GetBranch("FitTracks")
        tug.GetEntries()
        #tug.IsEmpty()
    except:
        print "FiTracks fail",n,e,CE,mu,CM,tau,CT,charg,CH,neut
        return

    for F,FIT in enumerate(sTree.FitTracks):
        fitStatus = FIT.getFitStatus()
        if not fitStatus.isFitConverged(): continue
        xx = FIT.getFittedState()
        mc = sTree.MCTrack[sTree.fitTrack2MC[F]]
        vtx=r.TVector3(mc.GetStartX(), mc.GetStartY(), mc.GetStartZ())
        mom=r.TVector3(mc.GetPx(), mc.GetPy(), mc.GetPz())
        trackDir = xx.getDir()
        vx = ROOT.TVector3()
        trackPos = xx.getPos()
        mc.GetStartVertex(vx)
        TT = 0
        for k in range(3):   TT += trackDir(k)*(vx(k)-trackPos(k))
        Dist = 0
        for k in range(3):   Dist += (vx(k)-trackPos(k)-TT*trackDir(k))**2
        Dist = ROOT.TMath.Sqrt(Dist)
        h['IP'].Fill(Dist)
        #print "ftrack"
        if not find_signal(xx.getPDG()): continue#This is charge Cut
        if not isInFiducial(vtx.X(),vtx.Y(),vtx.Z()): continue #vessel cut
        f_track+=1
        if not checkFiducialVolume(sTree,F,dy): continue
        #print n
        nmeas = fitStatus.getNdf()
        chi2 = fitStatus.getChi2()
        if not nmeas>25.: continue
        if not chi2/nmeas<5.: continue 
        if not xx.getMomMag()>1.: continue
        h['DOCA'].Fill(mc.GetStartT()-doca)
        if not (mc.GetStartT()-doca)<=1.: continue
        #print "DOCA", xx.getPDG(), Dist, n
        if not Dist<10.: continue
        RECO+=1

    #print "Finl Analysis Failed",n,e,CE,mu,CM,tau,CT,charg,CH,neut
    if e>1 and CE==0.0:#at least two electrons decay channel FOR BR
        h['DP_e'].Fill(mass_mc)
    
    if mu>1 and CM==0.0:#at least two muons decay channel FOR BR
      h['DP_mu'].Fill(mass_mc)
    
    if tau>1 and CT==0.0:#at least two taus decay channel FOR BR
      h['DP_tau'].Fill(mass_mc)
    
    if charg>0:#any chargronic decay channel for BR
      h['DP_charg'].Fill(mass_mc)
      #if neut!=0:Dump(sTree.MCTrack)

    if neut>0 and charg==0:
      h['DP_neut'].Fill(mass_mc)   
      #print e,mu,tau,charg,neut, "neutral"

    #if charg==1:
        #print e,mu,tau,charg,neut, "charg=1"
        #Dump(sTree.MCTrack)

    #if neut==0 and charg==0: print e,mu,tau,charg,neut, "0had "

    if CHARGE>1:#at least two charged particle in the VESSEL
        #print e,CE,mu,CM,tau,CT,charg,CH,neut

        if e>1 and CE==0.0:#at least two electrons decay channel FOR VES_PROB
            h['DPpur_e'].Fill(mass_mc)  
        
        if mu>1 and CM==0.0:#at least two muons decay channel FOR pur_PROB
            h['DPpur_mu'].Fill(mass_mc) 
         
        if tau>1 and CT==0.0:#at least two taus decay channel FOR pur_PROB
            h['DPpur_tau'].Fill(mass_mc)
        
        if charg>0:#any chargronic decay channel for BR
            h['DPpur_charg'].Fill(mass_mc) 
       
        if neut>0 and charg==0.0:
            h['DPpur_neut'].Fill(mass_mc)
    
    if f_track>1:#at least two charged particle in the VESSEL
        if e>1 and CE==0.0:#at least two electrons decay channel FOR VES_PROB
            h['DPvesW_e'].Fill(mass_mc,wg)
            h['DPves_e'].Fill(mass_mc)
            
        if mu>1 and CM==0.0:#at least two muons decay channel FOR VES_PROB
            h['DPvesW_mu'].Fill(mass_mc,wg)
            h['DPves_mu'].Fill(mass_mc)
            
        if tau>1 and CT==0.0:#at least two taus decay channel FOR VES_PROB
            h['DPvesW_tau'].Fill(mass_mc,wg)
            h['DPves_tau'].Fill(mass_mc)
            
        if charg>0:#any charged chargronic decay channel for BR
            h['DPvesW_charg'].Fill(mass_mc,wg)
            h['DPves_charg'].Fill(mass_mc)

        if neut>0 and charg==0.0:
            h['DPvesW_neut'].Fill(mass_mc,wg)
            h['DPves_neut'].Fill(mass_mc)
            
    if f_track>1 and RECO>1:#at least two charged tracks in the FINAL CUT
        if e>1 and CE==0.0:#at least two electrons decay channel FOR RECO_EFF
            h['DPang_e'].Fill(mass_mc,wg*xsw)
            if 'eta1' in dpMom: h['DPang1_e'].Fill(mass_mc,wg*xsw1)
            h['DPangW_e'].Fill(mass_mc,wg)  

        if mu>1 and CM==0.0:#at least two muons decay channel FOR RECO_EFF
            h['DPang_mu'].Fill(mass_mc,wg*xsw)
            if 'eta1' in dpMom: h['DPang1_mu'].Fill(mass_mc,wg*xsw1)
            h['DPangW_mu'].Fill(mass_mc,wg) 

        if neut>0 and charg==0:#any chargronic decay channel for RECO_EFF
            h['DPang_neut'].Fill(mass_mc,wg*xsw)
            if 'eta1' in dpMom: h['DPang1_neut'].Fill(mass_mc,wg*xsw1)
            h['DPangW_neut'].Fill(mass_mc,wg)

        if charg>0:#any chargronic decay channel for RECO_EFF
            h['DPang_charg'].Fill(mass_mc,wg*xsw)
            if 'eta1' in dpMom: h['DPang1_charg'].Fill(mass_mc,wg*xsw1)
            h['DPangW_charg'].Fill(mass_mc,wg)

        if tau>1 and CT==0:#at least two taus decay channel FOR RECO_EFF
            h['DPang_tau'].Fill(mass_mc,wg*xsw)
            if 'eta1' in dpMom: h['DPang1_tau'].Fill(mass_mc,wg*xsw1)
            h['DPangW_tau'].Fill(mass_mc,wg)

    if (e>1 and CE==0) or (mu>1 and CM==0) or (tau>1 and CT==0) or (charg>0) or (neut>0 and charg==0):#at least two charged leptons decay channel and any chargronic decay channel FOR BR_TOT
        h['DP'].Fill(mass_mc)
        if CHARGE>1:
            h['DPpur'].Fill(mass_mc)
            if f_track>1:##at least two charged tracks in the VESL
                h['DPvesW'].Fill(mass_mc,wg)
                h['DPves'].Fill(mass_mc)
                if RECO>1:#at least two charged tracks in the FINAL CUT 
                    #print "reco"
                    DP_P.push_back(sTree.MCTrack[mum].GetP())
                    DP_Pz.push_back(sTree.MCTrack[mum].GetPz())
                    DP_Pt.push_back(sTree.MCTrack[mum].GetPt())
                    DP_Rapidity.push_back(sTree.MCTrack[mum].GetRapidity())
                    DP_Xf.push_back(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
                    hs['DP_pz'].Fill(sTree.MCTrack[mum].GetPz())
                    hs['DP_p'].Fill(sTree.MCTrack[mum].GetP())
                    hs['DP_pt2'].Fill(sTree.MCTrack[mum].GetPt()*sTree.MCTrack[mum].GetPt())
                    hs['DP_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
                    hs['DP_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
                    if sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP()))<0.3 and sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP()))>0.025:
                        #print sTree.MCTrack[mum].GetRapidity()
                        hs['DPr_pz'].Fill(sTree.MCTrack[mum].GetPz())
                        hs['DPr_p'].Fill(sTree.MCTrack[mum].GetP())
                        hs['DPr_pt2'].Fill(sTree.MCTrack[mum].GetPt()*sTree.MCTrack[mum].GetPt())
                        hs['DPr_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
                    if sTree.MCTrack[mum].GetPt()>3.5:
                        hs['DPc3_pz'].Fill(sTree.MCTrack[mum].GetPz())
                        hs['DPc3_p'].Fill(sTree.MCTrack[mum].GetP())
                        hs['DPc3_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
                        hs['DPc3_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
                    if sTree.MCTrack[mum].GetPt()>2.0:
                        hs['DPc2_pz'].Fill(sTree.MCTrack[mum].GetPz())
                        hs['DPc2_p'].Fill(sTree.MCTrack[mum].GetP())
                        hs['DPc2_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
                        hs['DPc2_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())
                    if sTree.MCTrack[mum].GetPt()>1.0:
                        hs['DPc1_pz'].Fill(sTree.MCTrack[mum].GetPz())
                        hs['DPc1_p'].Fill(sTree.MCTrack[mum].GetP())
                        hs['DPc1_xf'].Fill(sTree.MCTrack[mum].GetPz()/400*m.cos(m.asin(sTree.MCTrack[mum].GetPt()/sTree.MCTrack[mum].GetP())))
                        hs['DPc1_rapidity'].Fill(sTree.MCTrack[mum].GetRapidity())

                    h['DPangW'].Fill(mass_mc)
                    h['DPangWe'].Fill(mass_mc,wg)
                    h['DPang'].Fill(mass_mc,wg*xsw)#FOR THE RATE
                    if 'eta1' in dpMom: h['DPang1'].Fill(mass_mc,wg*xsw1)
                else:
                    h['DPangW_oth'].Fill(mass_mc,wg)
                    h['DPang_oth'].Fill(mass_mc,wg*xsw)
                    if 'eta1' in dpMom: h['DPang1_oth'].Fill(mass_mc,wg*xsw1)
            else: 
                h['DPves_oth'].Fill(mass_mc)
                h['DPvesW_oth'].Fill(mass_mc,wg) 
        if CHARGE<2: 
            #print "CHARGE",CHARGE,e,mu,tau,charg,neut
            """for xxx in dau:
            print sTree.MCTrack[xxx].GetPdgCode()
            print sTree.MCTrack[xxx].GetProcID()"""
            #if mu or charg: Dump(sTree.MCTrack)
            h['DP_noth'].Fill(mass_mc)
    else: 
        #Dump(sTree.MCTrack)
        h['DP_oth'].Fill(mass_mc)
    ProdAna.Fill()
nEvents =sTree.GetEntries()
for n in range(nEvents):
    myEventLoop(n)


o1  = tmp1+"_e.dat"
o2  = tmp1+"_mu.dat"
o3  = tmp1+"_tau.dat" 
o4n = tmp1+"_neutral.dat" 
o4c = tmp1+"_charged.dat"
o6  = tmp1+"_other.dat"
o7  = tmp1+"_all.dat"
o8  = tmp1+"_sum.dat"
o9  = tmp1+"_rate1.dat"

a=open(o1,'w+')
b=open(o2,'w+')
c=open(o3,'w+')
dn=open(o4n,'w+')
dc=open(o4c,'w+')
f=open(o6,'w+')
g=open(o7,'w+')
H=open(o8,'w+')
k=open(o9,'w+')


print h['DP'].Integral(), h['DPpur'].Integral(), h['DPvesW'].Integral(), h['DPang'].Integral(), h['DPangW'].Integral(), h['DPangWe'].Integral()
print h['DPvesW'].Integral(), h['DPvesW_e'].Integral(), h['DPvesW_mu'].Integral(),  h['DPvesW_tau'].Integral(), h['DPvesW_neut'].Integral(),h['DPvesW_charg'].Integral()
print h['DPangW'].Integral(), h['DPangW_e'].Integral(), h['DPangW_mu'].Integral(),  h['DPangW_tau'].Integral(), h['DPangW_neut'].Integral(),h['DPangW_charg'].Integral()
if float(h['DP'].Integral())!=0.0:
    Sum=0.0
    #print h['DP'].Integral(), h['DPpur'].Integral(), h['DPvesW'].Integral(), h['DPang'].Integral(), h['DPangWe'].Integral()
    H.write('%.4g %s %.8g %.8g %.8g %.8g %.8g %.8g' %(mass_mc, eps, nEvents, float(h['DPW'].Integral()), float(h['DP'].Integral()), float(h['DPpur'].Integral()),float(h['DPves'].Integral()), float(h['DPangW'].Integral())))
    H.write('\n')

    if float(h['DPpur'].Integral())!=0.0:
        if float(h['DPvesW'].Integral())!=0.0:
            f.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_oth'].Integral())/float(h['DPW'].Integral()), float(h['DP_noth'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_oth'].Integral())/float(h['DPpur'].Integral()), float(h['DPangW_oth'].Integral())/float(h['DPvesW'].Integral())))
            f.write('\n')#mass, epsilon, how much we lose from 2 track selection, how much we lose in vessel, how much we lose in final selection
        if float(h['DPvesW'].Integral())==0.0:
            f.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_oth'].Integral())/float(h['DPW'].Integral()), float(h['DP_noth'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_oth'].Integral())/float(h['DPpur'].Integral())))
            f.write('\n')
    if float(h['DPpur'].Integral())==0.0:
        f.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_oth'].Integral())/float(h['DPW'].Integral()), float(h['DP_noth'].Integral())/float(h['DP'].Integral())))
        f.write('\n')

    if float(h['DP_e'].Integral())!=0.0:
        Sum+=float(h['DP_e'].Integral())
        if float(h['DPpur_e'].Integral())!=0.0:
            if float(h['DPvesW_e'].Integral())!=0.0:
                a.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_e'].Integral())/float(h['DP'].Integral()), float(h['DPpur_e'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_e'].Integral())/float(h['DPpur_e'].Integral()), float(h['DPangW_e'].Integral())/float(h['DPvesW_e'].Integral())))
                a.write('\n')
            if float(h['DPvesW_e'].Integral())==0.0:
                a.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_e'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_e'].Integral())/float(h['DP'].Integral()),float(h['DPvesW_e'].Integral())/float(h['DPpur_e'].Integral())))
                a.write('\n')
        if float(h['DPpur_e'].Integral())==0.0:
            a.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_e'].Integral())/float(h['DP'].Integral()), float(h['DPpur_e'].Integral())/float(h['DP'].Integral())))
            a.write('\n')

    if float(h['DP_mu'].Integral())!=0.0:
        Sum+=float(h['DP_mu'].Integral())
        if float(h['DPpur_mu'].Integral())!=0.0:
            if float(h['DPvesW_mu'].Integral())!=0.0:
                b.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_mu'].Integral())/float(h['DP'].Integral()), float(h['DPpur_mu'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_mu'].Integral())/float(h['DPpur_mu'].Integral()), float(h['DPangW_mu'].Integral())/float(h['DPvesW_mu'].Integral())))
                b.write('\n')
            if float(h['DPvesW_mu'].Integral())==0.0:
                b.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_mu'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_mu'].Integral())/float(h['DP'].Integral()),float(h['DPvesW_mu'].Integral())/float(h['DPpur_mu'].Integral())))
                b.write('\n')
        if float(h['DPpur_mu'].Integral())==0.0:
            b.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_mu'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_mu'].Integral())/float(h['DP'].Integral())))
            b.write('\n')
    
    if float(h['DP_tau'].Integral())!=0.0:
        Sum+=float(h['DP_tau'].Integral())
        if float(h['DPpur_tau'].Integral())!=0.0:
            if float(h['DPvesW_tau'].Integral())!=0.0:
                c.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_tau'].Integral())/float(h['DP'].Integral()), float(h['DPpur_tau'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_tau'].Integral())/float(h['DPpur_tau'].Integral()), float(h['DPangW_tau'].Integral())/float(h['DPvesW_tau'].Integral())))
                c.write('\n')
            if float(h['DPvesW_tau'].Integral())==0.0:
                c.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_tau'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_tau'].Integral())/float(h['DP'].Integral()),float(h['DPvesW_tau'].Integral())/float(h['DPpur_tau'].Integral())))
                c.write('\n')
        if float(h['DPpur_tau'].Integral())==0.0:
            c.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_tau'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_tau'].Integral())/float(h['DP'].Integral())))
            c.write('\n')

    if float(h['DP_neut'].Integral())!=0.0:
        Sum+=float(h['DP_neut'].Integral())
        if float(h['DPpur_neut'].Integral())!=0.0:
            if float(h['DPvesW_neut'].Integral())!=0.0:
                dn.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_neut'].Integral())/float(h['DP'].Integral()), float(h['DPpur_neut'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_neut'].Integral())/float(h['DPpur_neut'].Integral()), float(h['DPangW_neut'].Integral())/float(h['DPvesW_neut'].Integral())))
                dn.write('\n')
            if float(h['DPvesW_neut'].Integral())==0.0:
                dn.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_neut'].Integral())/float(h['DP'].Integral()), float(h['DPpur_neut'].Integral())/float(h['DP'].Integral()),float(h['DPvesW_neut'].Integral())/float(h['DPpur_neut'].Integral())))
                dn.write('\n')
        if float(h['DPpur_neut'].Integral())==0.0:
            dn.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_neut'].Integral())/float(h['DP'].Integral()), float(h['DPpur_neut'].Integral())/float(h['DP'].Integral())))
            dn.write('\n')

    if float(h['DP_charg'].Integral())!=0.0:
            Sum+=float(h['DP_charg'].Integral())
            if float(h['DPpur_charg'].Integral())!=0.0:
                if float(h['DPvesW_charg'].Integral())!=0.0:
                    dc.write('%.4g %s %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP_charg'].Integral())/float(h['DP'].Integral()), float(h['DPpur_charg'].Integral())/float(h['DP'].Integral()), float(h['DPvesW_charg'].Integral())/float(h['DPpur_charg'].Integral()), float(h['DPangW_charg'].Integral())/float(h['DPvesW_charg'].Integral())))
                    dc.write('\n')
                if float(h['DPvesW_charg'].Integral())==0.0:
                    dc.write('%.4g %s %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP_charg'].Integral())/float(h['DP'].Integral()),  float(h['DPpur_charg'].Integral())/float(h['DP'].Integral()),float(h['DPvesW_charg'].Integral())/float(h['DPpur_charg'].Integral())))
                    dc.write('\n')
            if float(h['DPpur_charg'].Integral())==0.0:
                dc.write('%.4g %s %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP_charg'].Integral())/float(h['DP'].Integral()),    float(h['DPpur_charg'].Integral())/float(h['DP'].Integral())))
                dc.write('\n')

    if float(Sum)!=0.0:
        if float(h['DPpur'].Integral())!=0.0:
            if float(h['DPvesW'].Integral())!=0.0:
                g.write('%.4g %s %.8g %.8g %.8g %.8g %.8g' %(mass_mc, eps, float(h['DP'].Integral()/h['DPW'].Integral()), float(h['DPpur'].Integral()/h['DP'].Integral()), float(Sum/h['DP'].Integral()), float(h['DPvesW'].Integral())/float(h['DPpur'].Integral()), float(h['DPangWe'].Integral())/float(h['DPvesW'].Integral())))
                g.write('\n')
            if float(h['DPvesW'].Integral())==0.0:
                g.write('%.4g %s %.8g %.8g %.8g %.8g 0.0' %(mass_mc, eps, float(h['DP'].Integral()/h['DPW'].Integral()), float(h['DPpur'].Integral()/h['DP'].Integral()), float(Sum/h['DP'].Integral()), float(h['DPvesW'].Integral())/float(h['DPpur'].Integral())))
                g.write('\n')
        if float(h['DPpur'].Integral())==0.0:
                g.write('%.4g %s %.8g %.8g %.8g 0.0 0.0' %(mass_mc, eps, float(h['DP'].Integral()/h['DPW'].Integral()), float(h['DPpur'].Integral()/h['DP'].Integral()), float(Sum/h['DP'].Integral())))
                g.write('\n')

    if 'eta1' in dpMom:
        RecW=h['DPang'].Integral()/h['DP'].Integral()*2.0e+20#weighted Selected/weighted Vessel
        RecW1=h['DPang1'].Integral()/h['DP'].Integral()*2.0e+20
        k.write('%.4g %s %.8g %.8g' %(mass_mc, eps, RecW1, RecW)) 
        k.write('\n')

    if not 'eta1' in dpMom:
        RecW=h['DPang'].Integral()/h['DP'].Integral()*2.0e+20#weighted Selected/weighted Vessel
        k.write('%.4g %s %.8g' %(mass_mc, eps, RecW)) 
        k.write('\n')

    if not 'eta1' in dpMom: print mass_mc, eps, RecW
    if 'eta1' in dpMom: print mass_mc, eps, RecW, RecW1

a.close()
b.close()
c.close()
dc.close()
dn.close()
f.close()
g.close()
H.close()
k.close()

hfile =tmp2+"_ana.root" 
hsfile = tmp2+"_xs.root" 
 
TreeFile.Write()
TreeFile.Close()

r.gROOT.cd()
ut.writeHists(h,hfile)
ut.writeHists(hs,hsfile)
