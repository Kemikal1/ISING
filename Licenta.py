#florentina.suter@g.unibuc.ro
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand
from celluloid import Camera
from copy import deepcopy

c = 2
a = c
b = c
c = 1
print(b)

"""
Functie ce returneaza o matrice in starea initiala randomizata
"""
def stare_initiala(r,c):
    mat = 2 * np.random.randint(2, size=(r, c)) - 1
    return mat

"""
Functie ce afiseaza starea matricei curente
"""
def afisare( f, stare, i, N, n_):
        x,y = np.meshgrid(range(N), range(N))
        splt = f.add_subplot(3, 3, n_)
        plt.setp(splt.get_yticklabels(), visible=False)
        plt.setp(splt.get_xticklabels(), visible=False)
        plt.pcolormesh(x,y, stare, cmap=plt.cm.Spectral)
        plt.title('Timp=%d' % i)
        plt.axis('tight')


"""
Functie ce afiseaza animatie pentru simulare
"""
def afis_animatie(fig,stare,cam,N):
    x, y = np.meshgrid(range(N), range(N))
    fig.pcolormesh(x,y, stare, cmap=plt.cm.Spectral)
    cam.snap()
    return cam

"""
Functie ce reprezinta un singur pas pentru algoritmul de simulare
"""
def miscare_monte_carlo (stare,N,beta):
    for i in range(N):
        for j in range(N):
            ii=np.random.randint(0,N)
            jj=np.random.randint(0,N)
            spin_select=stare[ii][jj]
            hamiltonian=stare[(ii+1)%N][jj] + stare[ii][(jj+1)%N] + stare[(ii-1)%N][jj] + stare[ii][(jj-1)%N]
            cost_eng=2*spin_select*hamiltonian
            spin_nou=spin_select
            if cost_eng<0:
                spin_nou = spin_select*-1
            else:
                if rand()<np.exp(-cost_eng*beta):
                    spin_nou = spin_select*-1

            stare[ii][jj]=spin_nou
    return stare

"""
Functie ce ruleaza metoda ISING in intregime
"""
def ising():
    n=200
    matrice=stare_initiala(n,n)
    kb=13e-24
    t=400
    factor=8*np.log(2)*10e18
    beta=(1/kb/t)/factor

    iteratii=300
    print(beta)

    an, sub = plt.subplots(1)
    x, y = np.meshgrid(range(n), range(n))
    plt.pcolormesh(x, y, matrice, cmap=plt.cm.Spectral)
    plt.title('Simulare')
    camera = Camera(an)
    fig=plt.figure()
    afisare(fig, matrice, 0, n,1)

    for i in range(iteratii):
        camera = afis_animatie(sub,matrice,camera,n)
        matrice=miscare_monte_carlo(matrice,n,beta)
        if i == 1:       afisare(fig, matrice, i, n, 2)
        if i == 4:       afisare(fig, matrice, i, n, 3)
        if i == 32:      afisare(fig, matrice, i, n, 4)
        if i == 100:     afisare(fig, matrice, i, n, 5)
        if i == 200:     afisare(fig, matrice, i, n, 6)
        if i == iteratii-1:    afisare(fig, matrice, i, n, 7)
    animatie= camera.animate(interval=30, blit=True)
    plt.show()


ising()



"""
Clasa Muchiei ce determina valoarea unei muchi dintre 2 noduri
"""

class Muchie:
    def __init__(self , start = None , capat = None, cost = None):
        self.pozitieStart = start
        self.pozitieCapat = capat
        self.cost = cost
'''
Clasa matricei de cost.Marimea matricei este setata predefinit la 30.Marimea ei fiind defapt de 30*30x30*30
'''

class MatriceDeCost:
    def __init__(self ,marime = 30):
        self.marime = marime * marime
        self.valori = []
        for ii in range(marime):
            for jj in range(marime):
                lista = []
                for i in range(marime):
                    for j in range(marime):
                        lista.append(Muchie((ii,jj),(i,j),0))
                self.valori.append(lista)

    def afisare(self):
        print(np.shape(self.valori))
        for i in range(self.marime):
            string = ""
            for j in range(self.marime):
                string +=" " + str(self.valori[i][j].cost)
            print(string)
    def element(self,i , j):
        marime = np.sqrt(self.marime)
        return int(marime*i+j);

def afisareHop(f, stare, N, n_):
    x, y = np.meshgrid(range(N), range(N))
    splt = f.add_subplot(1, 3, n_)
    plt.setp(splt.get_yticklabels(), visible=False)
    plt.setp(splt.get_xticklabels(), visible=False)
    plt.pcolormesh(x, y, stare, cmap=plt.cm.Spectral)
    plt.axis('tight')

marime = 30

#Initializam matrice de memorat
MatriceDeMemorat = np.zeros((marime,marime))
f = open("in.txt", "r")
for i in range(marime):
    linie = f.readline()
    linie = linie.strip()
    for  j in range (marime):
        MatriceDeMemorat[i][j] = int(linie[2*j])
MatriceDeMemorat = np.flip(MatriceDeMemorat)

#Initializam matrice de intrare care este defapt imaginea memorata + zgomot
MatriceDeIntrare = deepcopy(MatriceDeMemorat)
for k in range (int(marime*marime/5)):
    ii = np.random.randint(0, marime)
    jj = np.random.randint(0, marime)
    MatriceDeIntrare[ii][jj] = np.random.randint(0,2)


#Initializam matrice de cost
matriceCost = MatriceDeCost()

fig = plt.figure()
afisareHop(fig ,MatriceDeMemorat,marime,1)
afisareHop(fig ,MatriceDeIntrare,marime,2)

"""
Calculam matricei costului in functie de imaginea ce dorim s ao memoram
"""

def initializareMatriceCost():
    for ii in range(marime):
        for jj in range(marime):
            for i in range(marime):
                for j in range(marime):
                    if ii != i or jj != j:
                        pozCapat = matriceCost.element(i,j)
                        pozStart = matriceCost.element(ii,jj)
                        matriceCost.valori[pozStart][pozCapat].cost = (2*MatriceDeMemorat[ii][jj]-1)*(2*MatriceDeMemorat[i][j]-1)
                        matriceCost.valori[pozCapat][pozStart].cost = (2*MatriceDeMemorat[ii][jj]-1)*(2*MatriceDeMemorat[i][j]-1)


"""
Calculam imaginea memorata din imaginea cu zgomot adaugat
"""
def calculeazaImaginea():
    actualizeaza = 1
    while (actualizeaza):
        actualizeaza = 0
        for k in range(marime*marime):
            ii = np.random.randint(0, marime)
            jj = np.random.randint(0, marime)
            pozStart = matriceCost.element(ii, jj)
            valNoua = 0
            for i in range(marime):
                for j in range(marime):
                    if ii != i or jj != j:
                        pozCapat = matriceCost.element(i, j)
                        valNoua += MatriceDeIntrare[i][j]*matriceCost.valori[pozStart][pozCapat].cost
            if valNoua > 0 :
                valNoua = 1
            else:
                valNoua = 0
            if valNoua != MatriceDeIntrare[ii][jj]:
                actualizeaza = 1
            MatriceDeIntrare[ii][jj] = valNoua

initializareMatriceCost()
calculeazaImaginea()

afisareHop(fig ,MatriceDeIntrare,marime,3)
plt.show()





