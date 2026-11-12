import random
from math import *
import time
from solver import SmartCube
import statistics
import numpy as np

draglista = ""
blandlista = ""

färger_upl = {
        'höger':'röd',
        'fram':'grön',
        'över':'vit',
        'vänster':'orange',
        'bak':'blå',
        'under':'gul',
        }

underfärg = färger_upl['under']
överfärg = färger_upl['över']

def skapa_sidouppställningar(färger_upl):
    färger = list(färger_upl.values())
    n = 3**2 # Antal rutor på en sida
    sidouppställningar = [[färg for _ in range(n)] for färg in färger]
    return sidouppställningar

def hitta_avstånd(punkt,mätpunkt):
    n = len(punkt)
    avstånd = sum([(punkt[i] - mätpunkt[i])**2 for i in range(n)])**0.5
    return avstånd

def indexera(lista):
    return [[lista[i],i] for i in range(len(lista))]
def störst(lista,näst_n =0):
    indexlista = indexera(lista)
    indexlista.sort()
    indexlista.reverse()
    störst_index = indexlista[näst_n][1]
    return störst_index

def skapa_färgpunkter(sidouppställningar): 
    n = range(-2,3)
    punkter = [[x,y,z] for x in n for y in n for z in n] # Skapar ett 5x5x5 punktnät

    mätpunkter = []
    n = 3
    for t in [+1,-1]:
        for i in range(n):
            set = [0 for i in range(n)]
            set[i] = t*3
            mätpunkter.append(set)

    returpunkter = []

    for sidouppställning,mätpunkt in zip(sidouppställningar,mätpunkter):
        avstånd = [hitta_avstånd(punkt,mätpunkt) for punkt in punkter]
        valda_punkter = [punkter[störst(avstånd,i)] for i in range(-1,-10,-1)]
        färgpunkter = [{'färg':sidouppställning[i],'punkt':valda_punkter[i]} for i in range(len(sidouppställning))]
        
        returpunkter += färgpunkter    
    
    return returpunkter

def skapa_uppslagslista(sökordsuppsättning,översättningar):
    return dict(zip(sökordsuppsättning,översättningar))

def skapa_kuber(kubpunkter,färgpunkter):
    kuber = []
    for kubpunkt in kubpunkter:
        avstånd = [hitta_avstånd(färgpunkt['punkt'],kubpunkt) for färgpunkt in färgpunkter]
        tilldelade_avstånd = zip(färgpunkter,avstånd)
        rätt_färgpunkter = []
        for tilldelat_avstånd in tilldelade_avstånd:
            if tilldelat_avstånd[1] == 1:
                rätt_färgpunkter.append(tilldelat_avstånd[0])
        kub = {'punkt':kubpunkt,'färgpunkter':rätt_färgpunkter}
        kuber.append(kub)
    return kuber

def skapa_kub(färger_upl):
    sidouppställningar = skapa_sidouppställningar(färger_upl)
    färgpunkter = skapa_färgpunkter(sidouppställningar)
    kubpunkter = [(x,y,z) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)]
    kub = skapa_kuber(kubpunkter,färgpunkter)
    return kub

def matris_vektor_multiplicera(matris,vektor): # Skräddarsydd för 3x3 matris, kan göra mångmatris!
    kolumn1 = matris[0]
    kolumn2 = matris[1]
    kolumn3 = matris[2]
    ny_vektor = (kolumn1[0] * vektor[0] + kolumn2[0] * vektor[1] + kolumn3[0] * vektor[2],
                 kolumn1[1] * vektor[0] + kolumn2[1] * vektor[1] + kolumn3[1] * vektor[2],
                 kolumn1[2] * vektor[0] + kolumn2[2] * vektor[1] + kolumn3[2] * vektor[2])
    return ny_vektor
def Ry(v):return [[cos(v),0,sin(v)],
                  [0,1,0],
                  [-sin(v),0,cos(v)]]
def Rx(v):return [[1,0,0],
                  [0,cos(v),sin(v)],
                  [0,-sin(v),cos(v)]]
def Rz(v):return [[cos(v),sin(v),0],
                  [-sin(v),cos(v),0],
                  [0,0,1]]

def rotera_kring_axel(punkt,axel,v):
    p0 = punkt
    u0 = axel
    alfa = atan2(u0[0],u0[1])
    u1 = matris_vektor_multiplicera(Rz(alfa),u0)
    beta = -atan2(u1[2],u1[1])
    p1 = matris_vektor_multiplicera(Rz(alfa),p0)
    p2 = matris_vektor_multiplicera(Rx(beta),p1)
    p3 = matris_vektor_multiplicera(Ry(v),p2)
    p4 = matris_vektor_multiplicera(Rx(-beta),p3)
    p5 = matris_vektor_multiplicera(Rz(-alfa),p4)
    return p5

def rotera_kub(kub,axel,vinkel):
    for delkub in kub:
        delkub['punkt'] = rotera_kring_axel(delkub['punkt'],axel,vinkel)
        delkub['punkt'] = [int(round(koordinat,0)) for koordinat in delkub['punkt']]
        for färgpunkt in delkub['färgpunkter']:
            färgpunkt['punkt'] = rotera_kring_axel(färgpunkt['punkt'],axel,vinkel)
            färgpunkt['punkt'] = [int(round(koordinat,0)) for koordinat in färgpunkt['punkt']]

def omvänd_upl(upl):
    return {list(upl.values())[i]:list(upl.keys())[i] for i in range(len(upl))}

def vrid(kub,sida,*,vinkel = pi/2,visa =True, ämnad = 'drag'):
    for index in range(len(sida)):
        if sida[index] != 0:
            i = index
            break
    for delkub in kub:
        if delkub['punkt'][i] == sida[i]:
            delkub['punkt'] = rotera_kring_axel(delkub['punkt'],sida,vinkel)
            delkub['punkt'] = [int(round(koordinat,0)) for koordinat in delkub['punkt']]
            for färgpunkt in delkub['färgpunkter']:
                färgpunkt['punkt'] = rotera_kring_axel(färgpunkt['punkt'],sida,vinkel)
                färgpunkt['punkt'] = [int(round(koordinat,0)) for koordinat in färgpunkt['punkt']]

    färg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if tärning['punkt'] == sida]

    if visa:
        print('\n'*3)
        # print(färg)
        synliggör_kub(kub)

    motsatt_färgupl = omvänd_upl(färger_upl)

    # print(motsatt_färgupl)

    riktsida = motsatt_färgupl[färg[0]]

    dragbeteckningar = {
        'fram':"F",
        'bak':"B",
        'höger':"R",
        'vänster':"L",
        'över':"U",
        'under':"D"
    }

    beteckning = dragbeteckningar[riktsida]

    if ämnad == 'drag':
        prim = '' if vinkel < 0 else "'"
        global draglista
        draglista += beteckning + prim + " "
    
    if ämnad == 'blanda':
        prim = '' if vinkel < 0 else "'"
        global blandlista
        blandlista += beteckning + prim + " "
    
    return kub

def blanda_kub(kub,n):
    for _ in range(n):
        sida = [0,0,0]
        sida[random.choice(range(0,3))] = random.choice(range(-1,2,2))
        kub = vrid(kub,sida,visa=False,ämnad = 'blanda')

    return kub

def sortera_upllista(upllista,efter):
    sorteralista = [upl[efter] for upl in upllista]
    return [upllista[störst(sorteralista,i)] for i in range(len(upllista))]

def synliggör_kub(kub):

    färgkoder = { # ANSI-färgkoder för terminalen
    'svart': '\033[40m',
    'röd': '\033[41m',
    'grön': '\033[42m',
    'gul': '\033[43m',
    'blå': '\033[44m',
    'lila': '\033[45m',
    'cyan': '\033[46m',
    'vit': '\033[47m',
    'orange': '\033[48;5;208m'}

    rutnät = [['svart' for x in range(3*3*3 + 2)] for y in range(3*3*2 + 1)]

    färgpunkter = [färgpunkt for delkub in kub for färgpunkt in delkub['färgpunkter']]
    färgpunkter = sortera_upllista(färgpunkter,'punkt')
    ordnade_färgpunkter = [[färgpunkt for färgpunkt in färgpunkter if färgpunkt['punkt'][i] == t] for i in range(0,3) for t in [2,-2]]
    ordnade_färgpunkter = [ordnade_färgpunkter[i] for i in [4,2,0,3,1,5]]
    for X,Y,i in zip([0,0,0,3,3,3,6,6,6],[0,3,6,0,3,6,0,3,6],[-1,-2,-3,-4,-5,-6,-7,-8,-9]):
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[0][i]['färg']
    for X,Y,i in zip([15,15,15,12,12,12,9,9,9],[0,3,6,0,3,6,0,3,6],range(9)):
        X = X + 1
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[1][i]['färg']
    for X,Y,i in zip([18,18,18,21,21,21,24,24,24],[0,3,6,0,3,6,0,3,6],range(9)):
        X = X + 2
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[2][i]['färg']
    for X,Y,i in zip([0,0,0,3,3,3,6,6,6],[9,12,15,9,12,15,9,12,15],range(9)):
        Y = Y + 1
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[3][i]['färg']
    for X,Y,i in zip([15,15,15,12,12,12,9,9,9],[9,12,15,9,12,15,9,12,15],range(9)):
        X = X + 1
        Y = Y + 1
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[4][i]['färg']
    for X,Y,i in zip([18,18,18,21,21,21,24,24,24],[15,12,9,15,12,9,15,12,9],range(9)):
        X = X + 2
        Y = Y + 1
        for y,x in [(y,x) for y in range(Y,Y+3) for x in range(X,X+3)]:rutnät[y][x] = ordnade_färgpunkter[5][i]['färg']

    for y in rutnät:
        for x in y:
            print(f'{färgkoder[x]}  \033[0m',end='')
        print()

def hitta_kuber(kub,tärnart,färg):
    tärnartsuppslag = {'inner':0,'mitt':1,'kant':2,'hörn':3}
    sidantal = tärnartsuppslag[tärnart]
    passande_sidantal = [delkub for delkub in kub if len(delkub['färgpunkter']) == sidantal]
    passande_tärningar = []
    for deltärning in passande_sidantal:
        färger = [färgpunkt['färg'] for färgpunkt in deltärning['färgpunkter']]
        if färg in färger:passande_tärningar.append(deltärning)
    return passande_tärningar

def blockerande_vit(kub,tärning,sida):
    möjligt_blockerande_tärningspunkt = sida[0:2] + [1]
    for tärning in kub:
        if list(tärning['punkt']) == möjligt_blockerande_tärningspunkt:rätt_tärning = tärning
    for färgpunkt in rätt_tärning['färgpunkter']:
        if färgpunkt['färg'] == underfärg and färgpunkt['punkt'][2] == 2:return True
    return False

def vit_ej_uppe(tärning):
    for färgpunkt in tärning['färgpunkter']:
        if färgpunkt['färg'] == underfärg and färgpunkt['punkt'][2] == 2:
            return False
    return True

def nedre_punktfärg(kub,nedre_punkt):
    färgpunkter = [färgpunkt for tärning in kub for färgpunkt in tärning['färgpunkter'] ]
    for färgpunkt in färgpunkter:
        if färgpunkt['punkt'] == nedre_punkt:return färgpunkt['färg']  

def vitt_kryss(kub):
    vita_kanttärningar = hitta_kuber(kub,'kant',underfärg)
    for tärning in vita_kanttärningar:
        if tärning['punkt'][2] == 0: # Tärning är i mitten, här ska tärningens andra färgs sida vridas, dock om det är vit i toppen ska denna vridas först
            for färgpunkt in tärning['färgpunkter']:
                if färgpunkt['färg'] != underfärg:sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
            while blockerande_vit(kub,tärning,sida):kub = vrid(kub,[0,0,1],visa=0)
            while vit_ej_uppe(tärning):kub = vrid(kub,sida,visa=0)
        elif tärning['punkt'][2] == 1:
            for färgpunkt in tärning['färgpunkter']:
                if färgpunkt['färg'] == underfärg and färgpunkt['punkt'][2] != 2:
                    sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
                    kub = vrid(kub,sida,visa=0)
                    for färgpunkt in tärning['färgpunkter']: # Samma kod som ovan då det blir samma scenario
                        if färgpunkt['färg'] != underfärg:sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
                    while blockerande_vit(kub,tärning,sida):kub = vrid(kub,[0,0,1],visa=0)
                    while vit_ej_uppe(tärning):kub = vrid(kub,sida,visa=0)
        elif tärning['punkt'][2] == -1:
            for färgpunkt in tärning['färgpunkter']:
                if färgpunkt['färg'] == underfärg:
                    if färgpunkt['punkt'][2] == -1:
                        sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
                        while blockerande_vit(kub,tärning,sida):kub = vrid(kub,[0,0,1],visa=0)
                        kub = vrid(kub,sida,visa=0)
                        for färgpunkt in tärning['färgpunkter']: # Samma kod som ovan då det blir samma scenario
                            if färgpunkt['färg'] != underfärg:sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
                        while blockerande_vit(kub,tärning,sida):kub = vrid(kub,[0,0,1],visa=0)
                        while vit_ej_uppe(tärning):kub = vrid(kub,sida,visa=0)
                    else:
                        for färgpunkt in tärning['färgpunkter']:
                            if färgpunkt['färg'] != underfärg:sida = [int(färgpunkt['punkt'][i]/2) if abs(färgpunkt['punkt'][i]) == 2 else 0 for i in range(3)]
                        while blockerande_vit(kub,tärning,sida):kub = vrid(kub,[0,0,1],visa=0)
                        while vit_ej_uppe(tärning):kub = vrid(kub,sida,visa=0)
    for tärning in vita_kanttärningar:
        for färgpunkt in tärning['färgpunkter']:
            if färgpunkt['färg'] != underfärg:
                färg = färgpunkt['färg']
                nedre_punkt = färgpunkt['punkt'][0:2] + [0]
        while nedre_punktfärg(kub,nedre_punkt) != färg:
            kub = vrid(kub,[0,0,1],visa=0)
            nedre_punkt = rotera_kring_axel(nedre_punkt,[0,0,1],pi/2)
            nedre_punkt = [int(a) for a in nedre_punkt]
        sida = [int(nedre_punkt[i]/2) if abs(färgpunkt['punkt'][i]) == 1 else 0 for i in range(3)]
        kub = vrid(kub,sida,visa=0)
        kub = vrid(kub,sida,visa=0)

    return kub

def matchande_färgsidor(kub,tärning):
    två_färger = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] != underfärg]
    punkt = tärning['punkt']
    sidor = []
    for sida in [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]]:
        for i in [0,1]:
            if punkt[i] == sida[i]:sidor.append(sida)
    färger = []
    for delkub in kub:
        if delkub['punkt'] in sidor:färger.append(delkub['färgpunkter'][0]['färg'])
    två_färger.sort()
    färger.sort()
    if två_färger == färger:return True
    return False

def är_vit_på_botten(tärning):
    färgpunkt = [färgpunkt for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] == underfärg][0]
    if färgpunkt['punkt'][-1] == -2:
        return True
    return False

def löst_botten(kub):
    vita_hörntärningar = hitta_kuber(kub,'hörn',underfärg)
    for tärning in vita_hörntärningar:
        z = tärning['punkt'][2]
        if z == -1:
            y = tärning['punkt'][1]
            sida = [0,y,0]
            x = tärning['punkt'][0]
            if x == -1:v = -pi/2
            if x == 1:v = pi/2
            if y == -1:v = -v
            vrid(kub,sida,visa = False,vinkel = v)
            vrid(kub,[0,0,1],visa = False)
            vrid(kub,sida,visa = False,vinkel = -v)
        while not matchande_färgsidor(kub,tärning):vrid(kub,[0,0,1],visa=0)
        while not är_vit_på_botten(tärning):draglopp(kub,'höger draglopp',tärning)

def tag_upp_kanttärning(kub,tärning):
    draglopp(kub,'höger draglopp',tärning)
    rotera_kub(kub,[0,0,1],-pi/2)
    draglopp(kub,'oberoende vänster draglopp')

def matchande_färg_nedanför(kub,tärning):
    nedre_punktfärg = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'][2] == 1]
    färg_nedanför = [färgpunkt['färg'] for delkub in kub for färgpunkt in delkub['färgpunkter'] if delkub['punkt'] == [tärning['punkt'][0],tärning['punkt'][1],0]]
    return färg_nedanför == nedre_punktfärg

def andra_lagret(kub):
    kanttärningar = hitta_kuber(kub,'kant','röd') + hitta_kuber(kub,'kant','orange')
    fel_kanttärningar = hitta_kuber(kub,'kant',underfärg) + hitta_kuber(kub,'kant',överfärg)

    # Sollar bort fel kanttärningar vilket lämnar endast mittenkanttärningarna
    for kanttärning in kanttärningar:
        if kanttärning in fel_kanttärningar:kanttärningar.remove(kanttärning)
    for kanttärning in kanttärningar:
        if kanttärning in fel_kanttärningar:kanttärningar.remove(kanttärning)

    for tärning in kanttärningar:
        färger = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter']]
        if tärning['punkt'][2] == 0:tag_upp_kanttärning(kub,tärning)
        while not matchande_färg_nedanför(kub,tärning):vrid(kub,[0,0,1],visa=0)
        while tärning['punkt'] != [0,1,1]:rotera_kub(kub,[0,0,1],pi/2)
        tärning_om_höger = [delkub for delkub in kub if delkub['punkt'] == [1,0,0]][0]
        if tärning_om_höger['färgpunkter'][0]['färg'] in färger:
            vrid(kub,[0,0,1],vinkel = -pi/2, visa = 0)
            draglopp(kub,'oberoende höger draglopp')
            rotera_kub(kub,[0,0,1],-pi/2)
            draglopp(kub,'oberoende vänster draglopp')
        else:
            vrid(kub,[0,0,1],vinkel = pi/2, visa = 0)
            draglopp(kub,'oberoende vänster draglopp')
            rotera_kub(kub,[0,0,1],pi/2)
            draglopp(kub,'oberoende höger draglopp')

def medelvärde(lista):
    summa = sum(lista)
    n = len(lista)
    medelvärde = summa/n
    return medelvärde

def hitta_mittpunkt(punkter):
    n = len(punkter[0])
    mittpunkt = [medelvärde([punkt[i] for punkt in punkter]) for i in range(n)]
    return mittpunkt

def upponervänt_L(punkter):
    if [0,1,2] in punkter and [1,0,2] in punkter:
        return True
    return False

def lodrätt_streck(punkter):
    if [1,0,2] in punkter and [-1,0,2] in punkter:
        return True
    return False

def gult_kors(kub):
    gula_kanttärningar = hitta_kuber(kub,'kant',överfärg)
    while len([färgpunkt for tärning in gula_kanttärningar for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] == överfärg and färgpunkt['punkt'][2] == 2]) != 4:
        gult_uppåt = [färgpunkt for tärning in gula_kanttärningar for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] == överfärg and färgpunkt['punkt'][2] == 2]
        punkter = [färgpunkt['punkt'] for färgpunkt in gult_uppåt]
        if len(gult_uppåt) != 0:
            mittpunkt = hitta_mittpunkt(punkter)
            if mittpunkt[0:2] != [0,0] and len(gult_uppåt) > 1:
                while not upponervänt_L(punkter):
                    rotera_kub(kub,[0,0,1],pi/2)
                    punkter = [färgpunkt['punkt'] for färgpunkt in gult_uppåt]
            elif len(gult_uppåt) == 2:
                while not lodrätt_streck(punkter):
                    rotera_kub(kub,[0,0,1],pi/2)
                    punkter = [färgpunkt['punkt'] for färgpunkt in gult_uppåt]
        vrid(kub,[0,-1,0],vinkel = -pi/2,visa = 0)
        rotera_kub(kub,(0,1,0),-pi/2)
        draglopp(kub,'oberoende höger draglopp')
        rotera_kub(kub,(0,1,0),pi/2)
        vrid(kub,[0,-1,0],vinkel = pi/2,visa = 0)
        
def matcha_hörnbitar(kub):
    while True:
        matchande_hörnbitar = []
        gula_hörnbitar = hitta_kuber(kub,'hörn',överfärg)
        for tärning in gula_hörnbitar:
            färger = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] != överfärg]
            motsvarande_mittbitspunkter = [hitta_kuber(kub,'mitt',färg)[0]['punkt'] for färg in färger]
            faktiska_mittbitspunkter = [[tärning['punkt'][0],0,0],[0,tärning['punkt'][1],0]]
            if faktiska_mittbitspunkter[0] in motsvarande_mittbitspunkter and faktiska_mittbitspunkter[1] in motsvarande_mittbitspunkter:
                matchande_hörnbitar.append(tärning)
        if len(matchande_hörnbitar) >= 2:break
        vrid(kub,[0,0,1],visa=0)
    if len(matchande_hörnbitar) != 4:
        punkter = [tärning['punkt'] for tärning in matchande_hörnbitar]
        mittpunkt = hitta_mittpunkt(punkter)
        if mittpunkt[0:2] == [0,0]:
            if [1,1,0] in punkter:
                vrid(kub,[0,0,1],vinkel =-pi/2,visa=0)
            draglopp(kub,'oberoende höger draglopp')
            draglopp(kub,'oberoende höger draglopp')
            draglopp(kub,'oberoende höger draglopp')
            rotera_kub(kub,[0,0,1],-pi/2)
            draglopp(kub,'oberoende vänster draglopp')
            draglopp(kub,'oberoende vänster draglopp')
            draglopp(kub,'oberoende vänster draglopp')

        while True:
            matchande_hörnbitar = []
            gula_hörnbitar = hitta_kuber(kub,'hörn',överfärg)
            for tärning in gula_hörnbitar:
                färger = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] != överfärg]
                motsvarande_mittbitspunkter = [hitta_kuber(kub,'mitt',färg)[0]['punkt'] for färg in färger]
                faktiska_mittbitspunkter = [[tärning['punkt'][0],0,0],[0,tärning['punkt'][1],0]]
                if faktiska_mittbitspunkter[0] in motsvarande_mittbitspunkter and faktiska_mittbitspunkter[1] in motsvarande_mittbitspunkter:
                    matchande_hörnbitar.append(tärning)
            if len(matchande_hörnbitar) >= 2:break
            vrid(kub,[0,0,1],visa=0)
        punkter = [tärning['punkt'] for tärning in matchande_hörnbitar]
        mittpunkt = hitta_mittpunkt(punkter)
        if mittpunkt[0:2] == [0,1]:rotera_kub(kub,[0,0,1],-pi/2)
        elif mittpunkt[0:2] == [1,0]:rotera_kub(kub,[0,0,1],pi)
        elif mittpunkt[0:2] == [0,-1]:rotera_kub(kub,[0,0,1],pi/2)
        draglopp(kub,'oberoende höger draglopp')
        draglopp(kub,'oberoende höger draglopp')
        draglopp(kub,'oberoende höger draglopp')
        rotera_kub(kub,[0,0,1],-pi/2)
        draglopp(kub,'oberoende vänster draglopp')
        draglopp(kub,'oberoende vänster draglopp')
        draglopp(kub,'oberoende vänster draglopp')
        while True:
            matchande_hörnbitar = []
            gula_hörnbitar = hitta_kuber(kub,'hörn',överfärg)
            for tärning in gula_hörnbitar:
                färger = [färgpunkt['färg'] for färgpunkt in tärning['färgpunkter'] if färgpunkt['färg'] != överfärg]
                motsvarande_mittbitspunkter = [hitta_kuber(kub,'mitt',färg)[0]['punkt'] for färg in färger]
                faktiska_mittbitspunkter = [[tärning['punkt'][0],0,0],[0,tärning['punkt'][1],0]]
                if faktiska_mittbitspunkter[0] in motsvarande_mittbitspunkter and faktiska_mittbitspunkter[1] in motsvarande_mittbitspunkter:
                    matchande_hörnbitar.append(tärning)
            if len(matchande_hörnbitar) == 4:break
            vrid(kub,[0,0,1],visa=0)

def vänd_gula_uppåt(kub):
    rotera_kub(kub,[1,0,0],pi)
    for i in range(4):
        while True:
            if överfärg in [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [1,1,-2]]:break
            draglopp(kub,'oberoende höger draglopp')
        vrid(kub,[0,0,-1],visa=0)
    rotera_kub(kub,[1,0,0],pi)

def sista_algoritm(kub):
    draglopp(kub,'oberoende höger draglopp')
    draglopp(kub,'oberoende vänster draglopp')

    draglopp(kub,'oberoende höger draglopp')
    draglopp(kub,'oberoende höger draglopp')
    draglopp(kub,'oberoende höger draglopp')
    draglopp(kub,'oberoende höger draglopp')
    draglopp(kub,'oberoende höger draglopp')

    draglopp(kub,'oberoende vänster draglopp')
    draglopp(kub,'oberoende vänster draglopp')
    draglopp(kub,'oberoende vänster draglopp')
    draglopp(kub,'oberoende vänster draglopp')
    draglopp(kub,'oberoende vänster draglopp')

def lös_mittenbitar(kub):
    hittat = False
    for _ in range(4):
        mittenfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [0,2,1]]
        högerfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [1,2,1]]
        if mittenfärg == högerfärg:
            hittat = True
            break
        rotera_kub(kub,[0,0,1],pi/2)

    if hittat == False:
        sista_algoritm(kub)

    while True:
        i = 0
        for _ in range(4):
            mittenfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [0,2,1]]
            högerfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [1,2,1]]
            if mittenfärg == högerfärg:
                i += 1
            rotera_kub(kub,[0,0,1],pi/2)
        if i == 4:break
    
        for _ in range(4):
            mittenfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [0,2,1]]
            högerfärg = [färgpunkt['färg'] for tärning in kub for färgpunkt in tärning['färgpunkter'] if färgpunkt['punkt'] == [1,2,1]]
            if mittenfärg == högerfärg:
                hittat = True
                break
            rotera_kub(kub,[0,0,1],pi/2)
        sista_algoritm(kub)

def tredje_lagret(kub):
    gult_kors(kub)
    matcha_hörnbitar(kub)
    vänd_gula_uppåt(kub)
    lös_mittenbitar(kub)

def Lös(kub):
    vitt_kryss(kub)
    global vitt_kryss_n
    vitt_kryss_n = len(gör_lista(compact_sequence(draglista)))
    löst_botten(kub)
    andra_lagret(kub)
    global andra_lagret_n
    andra_lagret_n = len(gör_lista(compact_sequence(draglista)))
    tredje_lagret(kub)
    global tredje_lagret_n
    tredje_lagret_n = len(gör_lista(compact_sequence(draglista)))

def draglopp(kub,slag,tärning =0):
    if slag == 'höger draglopp':
        while tärning['punkt'][0:2] != [1,1]:rotera_kub(kub,[0,0,1],pi/2)
        sidlista = [[1,0,0,-pi/2],[0,0,1,-pi/2],[1,0,0,pi/2],[0,0,1,pi/2]]
        for sida in sidlista:vrid(kub,sida[0:3],vinkel = sida[-1],visa=0)
    elif slag == 'vänster draglopp':
        while tärning['punkt'][0:2] != [-1,1]:
            rotera_kub(kub,[0,0,1],pi/2)
        sidlista = [[-1,0,0,pi/2],[0,0,1,pi/2],[-1,0,0,-pi/2],[0,0,1,-pi/2]]
        for sida in sidlista:vrid(kub,sida[0:3],vinkel = sida[-1],visa=0)
    elif slag == 'oberoende vänster draglopp':
        sidlista = [[-1,0,0,pi/2],[0,0,1,pi/2],[-1,0,0,-pi/2],[0,0,1,-pi/2]]
        for sida in sidlista:vrid(kub,sida[0:3],vinkel = sida[-1],visa=0)
    elif slag == 'oberoende höger draglopp':
        sidlista = [[1,0,0,-pi/2],[0,0,1,-pi/2],[1,0,0,pi/2],[0,0,1,pi/2]]
        for sida in sidlista:vrid(kub,sida[0:3],vinkel = sida[-1],visa=0)
    return kub

def stränga(lista):
    sträng = ''
    for tecken in lista:sträng += tecken + ' '
    return sträng

def gör_lista(str):
    lista = []
    temp_str = ""
    for i in str:
        if i != " ":
            temp_str += i
        else:
            lista.append(temp_str)
            temp_str = ""
    lista.append(temp_str)
    return lista

def defdefdef(draglista):
    ny_draglista = []
    for drag in draglista:
        if drag[-1] == '2':
            a = drag[0] + "'"
            ny_draglista.append(a)
            ny_draglista.append(a)
        elif drag[-1] != "'":
            a = drag[0] + "'"
            ny_draglista.append(a)
            ny_draglista.append(a)
            ny_draglista.append(a)
        else:
            ny_draglista.append(drag)
    
    return ny_draglista

def vrid_enligt_lista(draglista,kub):

    draglista = gör_lista(draglista)
    # print(draglista)
    draglista = defdefdef(draglista)
    # print(draglista)
    str = ""
    for i in draglista:
        str += i + " "
    # print(str)

    beteckningsdrag = [("R",[1,0,0]),("L",[-1,0,0]),
                       ("F",[0,1,0]),("B",[0,-1,0]),
                       ("U",[0,0,1]),("D",[0,0,-1]),]
    
    for drag in draglista:
        for sida in beteckningsdrag:
            if sida[0] == drag[0]:
                # print(drag)
                # print(sida[1])
                vrid(kub,sida[1],visa=False,vinkel=pi/2,ämnad = 'blanda')
                # synliggör_kub(kub)

def compact_sequence(sequence: str) -> str:
       #compact duplicate moves
       #keep track of changes
       prev_seq = sequence
       while True:
           new_seq: list[str] = [" "]
           for i, x in enumerate(prev_seq):
               if not x.lower() in "udfblrxyz":
                   continue
               turn: str = x
               # replace 2 and ' with star counters
               if i < len(prev_seq) - 1:
                   if prev_seq[i+1] == "2":
                       turn += "*"
                   elif prev_seq[i+1] == "'":
                       turn += "**"
               if turn[0].lower() == new_seq[-1][0].lower():
                   # change previous and it's stars
                   new_seq[-1] = new_seq[-1][0] + "*" * ((len(turn) + len(new_seq[-1])-1) % 4)
               else:
                   new_seq.append(turn)
           #replace stars with 2 and '
           new_seq_styled: list[str] = [f"{i} ".replace("***", "4").replace("**", "'").replace("*", "2") for i in new_seq[1:]]
           new_seq_compact = ""
           for i in new_seq_styled:
               # remove full turns
               if "4" not in i:
                   new_seq_compact += i
           # return if nothing changed
           if new_seq_compact == prev_seq:
               return new_seq_compact
           else:
               prev_seq = new_seq_compact


def summera_sträng(list):
    str = ""
    for i in list:
        str += i + " "
    return str

def sära_på_antal_drag(tuple):
    a,b,c = tuple
    a -= 1
    b -= 1
    c -= 1
    d = c
    c -= b
    b -= a
    return (a,b,c,d)

def lössekvens(blandning=False):
    if not blandning:
        cube = SmartCube()
        blandning = cube.scramble()
    global draglista
    draglista = ""
    kub = skapa_kub(färger_upl)
    vrid_enligt_lista(blandning,kub)

    Lös(kub)

    dragantalstuple = (vitt_kryss_n,andra_lagret_n,tredje_lagret_n)
    dragantalstuple = sära_på_antal_drag(dragantalstuple)
    return dragantalstuple

def main():
    names = ["LBL", "CFOP", "CFOP-4LLL", "REVERSE"]
    steps = ["CROSS", "F2L", "LL", "FULL"]
    lst = [[[] for __ in range(4)] for _ in range(4)]
    i = 1
    try:
        while True:
            cube = SmartCube()
            scramble = cube.scramble()
            
            global draglista
            draglista = ""
            kub = skapa_kub(färger_upl)
            # synliggör_kub(kub)
            #wbca_blandning = "D2 L' F2 R2 U R2 F2 U B2 D' R2 F2 D' B' U2 B' F' D' R D U'"
            vrid_enligt_lista(scramble,kub)
            # synliggör_kub(kub)
            Lös(kub)
            # print(compact_sequence(blandlista))
            # print(compact_sequence(draglista))
            # i += 1
            # print(i)
            # vitt_kryss_n -= 1
            # andra_lagret_n -= 1
            # tredje_lagret_n -= 1
            dragantalstuple = (vitt_kryss_n,andra_lagret_n,tredje_lagret_n)
            dragantalstuple = sära_på_antal_drag(dragantalstuple)

            # print(dragantalstuple)
            # print("hej")
            for j in range(4):
                lst[0][j].append(dragantalstuple[j])
            res = cube.solve(verbose=False)
            if not res[0]:
                print("hej")
                exit()
            for j in range(4):
                lst[1][j].append(res[2][j])

            cube = SmartCube()
            cube.sequence(scramble)
            res = cube.solve(verbose=False, do_4lll=True)
            if not res[0]:
                exit()
            for j in range(4):
                lst[2][j].append(res[2][j])

            #rev scramble
            lst[3][3].append(cube.count_turns(scramble))


            print(i, end="\r")
            i += 1


    except KeyboardInterrupt:
        print(f"Solves: {i}")
        for j, stat in enumerate(lst):
            print(f"\n\n\n# {names[j]}")
            for k, s in enumerate(stat):
                try:
                    print(f"\n## {steps[k]}:\nMedian: {statistics.median(s)}\nMean: {statistics.mean(s)}\nQ1: {np.percentile(s, 25)}\nQ3: {np.percentile(s, 75)}\nMin: {min(s)}\nMax: {max(s)}")
                except statistics.StatisticsError:
                    continue

if __name__ == "__main__":
    main()