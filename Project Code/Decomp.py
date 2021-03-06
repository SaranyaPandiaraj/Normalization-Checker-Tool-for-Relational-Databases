from Normalization import *

N = Normalization()


class Decomposition:
    def __init__(self):
        self.List_Relation=list()
    #def combineSingleTonFD(self,MinFDs):

    def proposal3NF(self,R,MinFDs,Fds):
        #FDs=self.combineSingleTonFD(MinFDs)
        FDs=Fds
        for fd in MinFDs:
            R1=self.createNewRelation(fd)
            #self.List_Relation.append(R1)
            F0=self.projectFDs(R,R1,MinFDs)
            self.addRelation(R1,F0)


        if not self.candidateKeyChecking(R,MinFDs,FDs):
            KRs = self.createKeyRelation(R,MinFDs,FDs)

            Fkey = self.projectFDs(R,KRs[0],MinFDs)
            self.List_Relation.append((KRs[0],Fkey))

        return self.List_Relation

    #testing Phase
    def proposalBCNF(self,R0,F0):
        accum=list()
        L=self.decomposeBCNF(R0,F0,accum)
        return L

    def decomposeBCNF(self,R0,F0,accum):
        norm=Normalization()
        candKeys=norm.findCandKeys(R0,F0,F0)
        #print(candKeys)
        for f in F0:
            lh=set(f.lh)
            rh=set(f.rh)
            if norm.checkBCNF(f,lh,rh,candKeys):
            #print(norm.FDListBCNF)
                break
        #print(norm.FDListBCNF)

        if not norm.FDListBCNF==[]:
            fd=norm.FDListBCNF[0]
            #print(fd)
            X=fd.lh
            #print(X)
            xclosure=F0.attribute_closure(X)
            #print(xclosure)
            R01=set(xclosure)
            #print(R01)
            R02=R0.copy()
            R02=R02.difference(R01)
            #print(R02)
            R02=R02.union(set(X))
            #print(R02)
            F01=self.projectFDs(R0,R01,F0)
            #print("FD:",F01)
            F02=self.projectFDs(R0,R02,F0)
            self.decomposeBCNF(R01,F01,accum)
            #accum.append((R01,F01))
            self.decomposeBCNF(R02,F02,accum)
        else:
            accum.append((R0,F0))
        return accum

    def projectFDs(self,ParentRelation,DecompRelation,ParentFDs):
        T=FDependencyList()
        properset=N.findNonEmptySubsets(DecompRelation)
        #print('PROPERSET = ',properset)
        for X in properset:
            xclosure=ParentFDs.attribute_closure(X)
            #print('Xclosure',xclosure)

            for a in xclosure:
                #print("a:",a)
                if DecompRelation.__contains__(a):
                    T.append(FDependency(list(X),[a]))

        G=T.MinimalCover()
        #print("FD=",G)
        return G



    def addRelation(self,R1,F):

        """ This method will check if any of the currently
            added relation is a subset of New Relation """
        #check=False;
        T=self.List_Relation.copy()
        if self.List_Relation==[]:
            self.List_Relation.append((R1,F))
        else:
            for g in T:
                if(g[0].issubset(R1)):
                    self.List_Relation.remove(g)
                #self.List_Relation.append(R1)
                else:
                    if R1.issubset(g[0]):
                #self.List_Relation.remove(R1)
                        return 0
            self.List_Relation.append((R1,F))

        return 0

    def createNewRelation(self,nfd):

        g=list()
        g.extend(nfd.lh)
        g.extend(nfd.rh)

        return set(g)
    #N=Normalization ()
    def createKeyRelation(self,R,MinFDs,FDs):
        #KeyRelations=list()
        KeyRelations=N.findCandKeys(R,MinFDs,FDs)
        return KeyRelations

    def candidateKeyChecking(self,R,MinFDs,FDs):
        flag=False
        keys=N.findCandKeys(R,MinFDs,FDs)
        for R2 in self.List_Relation:
            for key in keys:
                if key.issubset(R2[0]):
                    flag=True
                    return True
                else:
                    flag=False
        return flag
