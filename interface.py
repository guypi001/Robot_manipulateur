import winsound
from tkinter import *
import tkinter.messagebox
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import math as Math
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

interface = Tk()
interface.title("Interface de simulation")
interface.geometry("1200x720")
interface['bg'] = '#d5f5E3'
interface.resizable(width=False, height=False)


# DEFINITION DE VARIABLES GLOBALE
global L0, L1, L2, O1, O2, XB, YB, SO1, CO1, nbrePas, nbreMaxPas, txtNbrePas, X_Pi, Y_Pi, listbox
X_Pi = []
Y_Pi = []
etatBtnTrajectoire=False
etatBtnPas=False
etatBtnBip=True
etatBtnR0=False
etatBtnR1=False
etatBtnR2=False
I=0
# FONCTIONS D'INITIALISATION
def verifSaisieInt(valeur):
    try:
        f =int(valeur)
        return True
    except:
        return False

def verifSaisieFloat(valeur):
    try:
        f =float(valeur)
        return True
    except:
        return False

def recupValeurLien(case):
    if (verifSaisieFloat(case.get())==True):
        return float(case.get())
    else:
        tkinter.messagebox.showwarning(title="Erreur",message="Un des champs est vide")
        return

def recupValeurAngle(angle):
    if (verifSaisieFloat(angle.get())==True):
        return float(angle.get())
    else:
        tkinter.messagebox.showwarning(title="Erreur",message="Un des champs est vide")
        return

def recupValeur(txt):
    if (verifSaisieInt(txt.get())==True):
        return int(txt.get())
    else:
        tkinter.messagebox.showwarning(title="Erreur",message="Un des champs est vide")
        return

def calcul():

    L0 = recupValeurLien(txtL1)
    L1 = recupValeurLien(txtL2)
    L2 = recupValeurLien(txtL3)
    O1 = Math.radians(recupValeurAngle(txtTeta1))
    O2 = Math.radians(recupValeurAngle(txtTeta2))
    nbrePas = int(recupValeur(txtNbrePas))
    YB = recupValeurLien(txtYB)
    XB = recupValeurLien(txtXB)
    
    #LES MATRICES DE PASSAGE DIRECTE
    Mat0T1 = np.array([[Math.cos(O1),-Math.sin(O1),0,L0],[Math.sin(O1),Math.cos(O1),0,0],[0,0,1,0],[0,0,0,1]])
    Mat1T2 = np.array([[Math.cos(O2),-Math.sin(O2),0,L1],[Math.sin(O2),Math.cos(O2),0,0],[0,0,1,0],[0,0,0,1]])
    Mat0T2 = Mat0T1.dot(Mat1T2)
    A2=np.array([[L2],[0],[0],[1]])
    A21=np.array([[L1],[0],[0],[1]])
    A10=np.array([[L0],[0],[0],[1]]) 
    
    A0 = Mat0T2.dot(A2)

    A20 = Mat0T1.dot(A21)

    rotAngle = Math.degrees(Math.atan2(Mat0T2[[1],[0]], Mat0T2[[0],[0]]))

    Mat1T0 = np.array([[Math.cos(O1),Math.sin(O1),0,-L0*Math.cos(O1)],[-Math.sin(O1),Math.cos(O1),0,L0*Math.sin(O1)],[0,0,1,0],[0,0,0,1]])
    Mat2T1 = np.array([[Math.cos(O2),Math.sin(O2),0,-L0*Math.cos(O2)],[-Math.sin(O2),Math.cos(O2),0,L1*Math.sin(O2)],[0,0,1,0],[0,0,0,1]])
   # txtXA.insert(0,float(A0[1]))
    #txtYA.insert(0,float(A0[0]))
    return [nbrePas, L0, A20, A0, YB, XB, L1, L2]

def fncTrajectoire():
    global etatBtnTrajectoire
    if(etatBtnTrajectoire==False):
        etatBtnTrajectoire = True
        btnTrajec.configure(bg='green')
        result = calcul()
        XA0 = result[3][0]
        XB = result[5]
        YA0 = result[3][1]
        YB = result[4]
        a = (YA0-YB)/(XA0-XB)
        b = YB-a*XB
        x=range(-100,101)
        y = a*x + b
        #Trace la droite
        plot.plot(y,x,"k-",lw=3)
        plot.grid(True)
        graphique.draw()
    else:
        etatBtnTrajectoire = False
        btnTrajec.configure(bg='white')

def fncInitialisation():
    plot.cla()
    global I
    I=1
    result = calcul()
    L0 = result[1]
    A20 = result[2]
    A0 = result[3]
    YB = result[4]
    XB = result[5]
    nbreMaxPas = result[0]

    plot.set_xlabel('Axe Y0')
    plot.set_ylabel('Axe X0')
    plot.yaxis.set_ticks_position('right')
    plot.set_xticks(range(16))
    plot.set_yticks(range(16))
    plot.set_xlim((15,-1))
    plot.set_ylim((-1, 15))
    plot.grid(True)

    #tracer L0
    plot.plot([0.0,0.0],[0.0,L0],"b-",lw=7)
    #tracer L1
    plot.plot([0.0,A20[1]],[L0,A20[0]],"b-",lw=7)
    #tracer L2
    plot.plot([A20[1],A0[1]],[A20[0],A0[0]],"b-",lw=7)
    #Le point A
    plot.scatter([A0[1]], [A0[0]], s =500, color = 'red')
    #Le point B
    plot.scatter([YB], [XB], s =500, color = 'red')
    #Les Articulations
    plot.scatter([0.0], [L0], s =500, color = 'black')
    plot.scatter([A20[1]], [A20[0]], s =500, color = 'black')
    #La base et le sol
    plot.plot([-0.5,0.5],[0.0,0.0],"k-",lw=10)
    plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=3)

    if etatBtnTrajectoire==True:
        XA0 = result[3][0]
        XB = result[5]
        YA0 = result[3][1]
        YB = result[4]
        a = (YA0-YB)/(XA0-XB)
        b = YB-a*XB
        x=range(-100,101)
        y = a*x + b
        #Trace la droite
        plot.plot(y,x,"k-",lw=3)
    plot.grid(True)
    graphique.draw()
    L1 = recupValeurLien(txtL2)
    L2 = recupValeurLien(txtL3)
    O1 = recupValeurAngle(txtTeta1)
    O2 = recupValeurAngle(txtTeta2)
    listbox.insert(END, "Déssin du robot avec les paramêtres      L0= " + str(L0) + "     L1= "+ str(L1) + "    L2= " + str(L2) + "    O1= " + str(O1)+ "    O2= " + str(O2)+"             "+ str(time.ctime()) )

def demo():
    txtL1.delete(0,END)
    txtL1.insert(0,"3.5")
    txtL2.delete(0,END)
    txtL2.insert(0,"3")
    txtL3.delete(0,END)
    txtL3.insert(0,"3")
    txtTeta1.delete(0,END)
    txtTeta1.insert(0,"55")
    txtTeta2.delete(0,END)
    txtTeta2.insert(0,"75")
    txtNbrePas.delete(0,END)
    txtNbrePas.insert(0,"20")
    txtYB.delete(0,END)
    txtYB.insert(0,"1")
    txtXB.delete(0,END)
    txtXB.insert(0,"0")
    txtL9.delete(0,END)
    txtL9.insert(0,"20")
    listbox.insert(END, "Les plages sont remplies par défault               "+ str(time.ctime()) )

def nouveau():
    txtL1.delete(0,END)
    txtL2.delete(0,END)
    txtL3.delete(0,END)
    txtTeta1.delete(0,END)
    txtTeta1.delete(0,END)
    txtTeta2.delete(0,END)
    txtNbrePas.delete(0,END)
    txtYB.delete(0,END)
    txtXB.delete(0,END)
    txtL9.delete(0,END)
    listbox.insert(END, "Les valeurs des champs ont été reinitialisées            " + str(time.ctime()))


def fncAvanceePas():
    global etatBtnPas, Y_Pi, X_Pi
    result = calcul()
    nbrePas = result[0]
    L0 = result[1]
    L1 = result[6]
    L2 = result[7]
    YB = result[4]
    A0 = result[3]
    XB = result[5]
    A20 = result[2]
    LT = L2+L1
    
    global I
    i=I
    plot.cla()
    #Definir les proprietes du nouveau graphe
    plot.set_xlabel('Axe Y0')
    plot.set_ylabel('Axe X0')
    plot.yaxis.set_ticks_position('right')
    plot.set_xticks(range(16))
    plot.set_yticks(range(16))
    plot.set_xlim((15,-1))
    plot.set_ylim((-1, 15))
    plot.grid(True)
    #Distance X entre deux pas
    disXPas = (XB-A0[0])/nbrePas
    if disXPas<0:
        disXPas = -disXPas
        #Distance Y entre deux pas
    disYPas = (YB-A0[1])/nbrePas
    if disYPas<0:
        disYPas = -disYPas
    if XB>=A0[0] :
        Xi = A0[0]+i*disXPas
    else:
        Xi = A0[0]-i*disXPas

    if YB>A0[1]:
        Yi = A0[1]+i*disYPas
    else:
        Yi = A0[1]-i*disYPas

    #LES CALCULS ------------------------------------->
    B1 = -2*Yi*L1
    B2 = 2*L1*(L0-Xi)
    B3 = L2**2-Yi**2-(L0-Xi)**2-L1**2
    teta_1=0
    teta_2=0
    SO1 = 0
    CO1 = 0
    epsi = 1
    #conf.configure(bg="green")
    if B3==0 :
        teta_1 = Math.degrees(Math.atan2(-B2,B1))
    else:
        if ((B1**2+B2**2-B3**2)>=0) :
            SO1 = (B3*B1+epsi*B2*Math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            CO1 = (B3*B2-epsi*B1*Math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
            teta_1 = Math.degrees(Math.atan2(SO1,CO1))
        else:
            pass
     #conf.configure(bg="red")
    Yn1 = L2*SO1
    Yn2 = L2*CO1
    if L2!=0 :
        teta_2 = Math.degrees(Math.atan2(Yn1/L2,Yn2/L2))
    else:
        pass
        #conf.configure(bg="red")
    XA1i =L1*Math.cos(Math.radians(teta_1))+L0
    YA1i =L1*Math.sin(Math.radians(teta_1))

    #Position des Pi
    '''txtTeta1Pi.delete(0,END)
    txtTeta1Pi.insert(0,float((int(teta_1*1000))/1000))
    txtTeta2Pi.delete(0,END)
    txtTeta2Pi.insert(0,float((int(teta_2*1000))/1000))
    txtXPi.delete(0,END)
    txtXPi.insert(0,float((int(Xi*1000))/1000))
    txtYPi.delete(0,END)
    txtYPi.insert(0,float((int(Yi*1000))/1000))'''

    if(i==nbrePas):
        I=0
    else:
        I=I+1
    #Trajectoire
    if etatBtnTrajectoire==True:
        XA0 = result[3][0]
        XB = result[5]
        YA0 = result[3][1]
        YB = result[4]
        a = (YA0-YB)/(XA0-XB)
        b = YB-a*XB
        x=range(-100,101)
        y = a*x + b
        #Trace la droite
        plot.plot(y,x,"k-",lw=3)
        #Droite entre A et Pi
        plot.plot([A0[1],Yi],[A0[0],Xi],"y-",lw=5)

    if etatBtnPas==True:
        for j in range(0,len(X_Pi)) :
            plot.scatter([Y_Pi[j]], [X_Pi[j]], s =200, color = '#FF00CC')

    #Le repere R0
    if etatBtnR0==True:
        plot.plot([0.0,0.0],[0.0,15.0],"r-",lw=2)
        plot.plot([0.0,15.0],[0.0,0.0],"r-",lw=2)
    #Le repere R1
    if etatBtnR1==True:
        m=(YA1i-0)/(XA1i-L0)
        c=YA1i-m*XA1i
        u = m*(16)+c
        plot.plot([0.0,u],[L0,16.0],"y--",lw=2)
        l = (-1/m)*(16)+YA1i+(1/m)*XA1i
        plot.plot([0.0,l],[L0,16.0],"y--",lw=2)
    #Le repere R2
    if etatBtnR2==True:
        m=(YA1i-Yi)/(XA1i-Xi)
        c=YA1i-m*XA1i
        u = m*16+c
        plot.plot([YA1i,u],[XA1i,16.0],"m--",lw=2)
        l = (-1/m)*(-16)+YA1i+(1/m)*XA1i
        plot.plot([YA1i,l],[XA1i,-16.0],"m--",lw=2)

    #tracer L0
    plot.plot([0.0,0.0],[0.0,L0],"b-",lw=7)
    #tracer L1
    plot.plot([0.0,YA1i],[L0,XA1i],"b-",lw=7)
    #tracer L2
    plot.plot([YA1i,Yi],[XA1i,Xi],"b-",lw=7)
    #Point Pi
    plot.scatter([Yi], [Xi], s =500, color = '#FF0000')
    #Point A0
    plot.scatter([0], [L0], s =500, color = 'black')
    #Point A2
    plot.scatter([YA1i], [XA1i], s =500, color = 'black')
    if i!=0:
        #Le point A
        plot.scatter([A0[1]], [A0[0]], s =300, color = '#006633')
    else:
        #Le point A
        plot.scatter([A0[1]], [A0[0]], s =500, color = '#FF0000')
    if i==nbrePas:
        #Le point B
        plot.scatter([YB], [XB], s =500, color = '#FF0000')
    else:
        #Le point B
        plot.scatter([YB], [XB], s =300, color = '#00FF33')
    #La base et le sol
    plot.plot([-0.5,0.5],[0.0,0.0],"k-",lw=10)
    plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=3)
    plot.grid(True)
    graphique.draw()
    if etatBtnBip==True:
        #Le Bip
        winsound.Beep(20, 10)
    listbox.insert(END, "Déplacement du robot vers le point ( "+ str(Yi)+"  ; "+ str(Xi)+" )            " + str(time.ctime()))



def avance():
    
    global X_Pi, Y_Pi, etatBtnPas, etatBtnBip, etatBtnR0, graphique, plot
    X_Pi = []
    Y_Pi = []
    result = calcul()
    nbrePas = result[0]
    L0 = result[1]
    L1 = result[6]
    L2 = result[7]
    YB = result[4]
    A0 = result[3]
    XB = result[5]
    A20 = result[2]
    tps = recupValeur(txtL9)
    vitesse= tps/nbrePas

    LT = L2+L1
    if(LT<YB or LT<XB):
        listbox.insert(END, "Impossible d'ateindre le point B ( "+ str(YB)+"  ; "+ str(XB)+" )            " + str(time.ctime()))
        tkinter.messagebox.showwarning(title="Erreur",message="Inmpossible d'atteindre le point")
        return
    #vitesse = float(1/(int(txtL9.get())))
    #fig = plt.figure(figsize=(12, 10), dpi=50)

    ims = []

    for i in range(1,nbrePas+1):
        #plt.cla()
        plot.clear()
        #Definir les proprietes du nouveau graph
        plot.set_xlabel('Axe Y0')
        plot.set_ylabel('Axe X0')
        plot.yaxis.set_ticks_position('right')
        plot.set_xticks(range(16))
        plot.set_yticks(range(16))
        plot.set_xlim((15,-1))
        plot.set_ylim((-1, 15))
        plot.grid(True)
        #plt.xlim(15, -1)
        #plt.ylim(-1, 15)
        #Distance X entre deux pas
        disXPas = (XB-A0[0])/nbrePas
        if disXPas<0:
            disXPas = -disXPas
        #Distance Y entre deux pas
        disYPas = (YB-A0[1])/nbrePas
        if disYPas<0:
            disYPas = -disYPas
        if XB>=A0[0] :
            Xi = A0[0]+i*disXPas
        else:
            Xi = A0[0]-i*disXPas

        if YB>A0[1]:
            Yi = A0[1]+i*disYPas
        else:
            Yi = A0[1]-i*disYPas

        #LES CALCULS ------------------------------------->
        B1 = -2*Yi*L1
        B2 = 2*L1*(L0-Xi)
        B3 = L2**2-Yi**2-(L0-Xi)**2-L1**2
        teta_1=0
        teta_2=0
        SO1 = 0
        CO1 = 0
        epsi = 1
        if B3==0 :
            teta_1 = Math.degrees(Math.atan2(-B2,B1))
        else:
            if ((B1**2+B2**2-B3**2)>=0) :
                SO1 = (B3*B1+epsi*B2*Math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
                CO1 = (B3*B2-epsi*B1*Math.sqrt(B1**2+B2**2-B3**2))/(B1**2+B2**2)
                teta_1 = Math.degrees(Math.atan2(SO1,CO1))
            else:
                #conf.configure(bg="red")
                break
        Yn1 = L2*SO1
        Yn2 = L2*CO1
        if L2!=0 :
            teta_2 = Math.degrees(Math.atan2(Yn1/L2,Yn2/L2))
        else:
            #conf.configure(bg="red")
            break
        #conf.configure(bg="green")
        XA1i =L1*Math.cos(Math.radians(teta_1))+L0
        YA1i =L1*Math.sin(Math.radians(teta_1))
        #Position des Pi
        '''txtTeta1Pi.delete(0,END)
        txtTeta1Pi.insert(0,float((int(teta_1*1000))/1000))
        txtTeta2Pi.delete(0,END)
        txtTeta2Pi.insert(0,float((int(teta_2*1000))/1000))
        txtXPi.delete(0,END)
        txtXPi.insert(0,float((int(Xi*1000))/1000))
        txtYPi.delete(0,END)
        txtYPi.insert(0,float((int(Yi*1000))/1000))'''
        #Trajectoire
        if etatBtnTrajectoire==True:
            XA0 = result[3][0]
            XB = result[5]
            YA0 = result[3][1]
            YB = result[4]
            a = (YA0-YB)/(XA0-XB)
            b = YB-a*XB
            x=range(-100,101)
            y = a*x + b
            #Trace la droite
            plot.plot(y,x,"k-",lw=3)
            #Droite entre A et Pi
            plot.plot([A0[1],Yi],[A0[0],Xi],"y-",lw=5)
        #sauvegarde les coordonnees des Pi
        X_Pi.append(Xi)
        Y_Pi.append(Yi)
        #Les Pas
        if etatBtnPas==True:
            for j in range(0,len(X_Pi)) :
                plot.scatter([Y_Pi[j]], [X_Pi[j]], s =200, color = '#FF00CC')
        #for j in range(0,X_Pi.len()):
         #   print(X_Pi, Y_Pi)
        #tracer L0
        plot.plot([0.0,0.0],[0.0,L0],"b-",lw=7)
        #tracer L1
        plot.plot([0.0,YA1i],[L0,XA1i],"b-",lw=7)
        #tracer L2
        plot.plot([YA1i,Yi],[XA1i,Xi],"b-",lw=7)
        #Point Pi
        plot.scatter([Yi], [Xi], s =500, color = '#FF0000')
        #Point A0
        plot.scatter([0], [L0], s =500, color = 'black')
        #Point A2
        plot.scatter([YA1i], [XA1i], s =500, color = 'black')
        if i!=0:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =300, color = '#006633')
        else:
            #Le point A
            plot.scatter([A0[1]], [A0[0]], s =500, color = '#FF0000')
        if i==nbrePas:
            #Le point B
            plot.scatter([YB], [XB], s =300, color = '#FF0000')
        else:
            #Le point B
            plot.scatter([YB], [XB], s =300, color = '#00FF33')
        #Le repere R0
        if etatBtnR0==True:
            plot.plot([0.0,0.0],[0.0,15.0],"r-",lw=2)
            plot.plot([0.0,15.0],[0.0,0.0],"r-",lw=2)
        #Le repere R1
        if etatBtnR1==True:
            m=(YA1i-0)/(XA1i-L0)
            c=YA1i-m*XA1i
            u = m*(16)+c
            plt.plot([0.0,u],[L0,16.0],"y--",lw=2)
            l = (-1/m)*(16)+YA1i+(1/m)*XA1i
            plot.plot([0.0,l],[L0,16.0],"y--",lw=2)
        #Le repere R2
        if etatBtnR2==True:
            m=(YA1i-Yi)/(XA1i-Xi)
            c=YA1i-m*XA1i
            u = m*16+c
            plot.plot([YA1i,u],[XA1i,16.0],"m--",lw=2)
            l = (-1/m)*(-16)+YA1i+(1/m)*XA1i
            plot.plot([YA1i,l],[XA1i,-16.0],"m--",lw=2)
        #Le sol
        plot.plot([-0.5,0.5],[0.0,0.0],"k-",lw=10)
        plot.plot([0.0,15.0],[0.0,0.0],"k--",lw=3)
        plot.grid(True)
        graphique.draw()
        graphique.get_tk_widget().pack()
        schema.canvas.draw()
        schema.canvas.flush_events()
        listbox.insert(END, "Déplacement du robot vers le point ( "+ str(Yi)+"  ; "+ str(Xi)+" )            " + str(time.ctime()))
        if etatBtnBip==True:
            #Le Bip
            winsound.Beep(440, 250)
        time.sleep(vitesse)
       
    
        
    
    







interface1= Frame(interface)
interface1.place(x=900, y=520)

label = Label(interface, text="ROBOT MANIPULATEUR 2D", font='Helvetica 18 bold',bg = "#d5f5E3")
label.pack()

lbl1 = Label(interface, text="LES PARAMETRES", width=23, font="Helvetica 16 bold", bg="#d5f5E3", underline=TRUE)
lbl1.place(x=0, y=40)

lbl2 = Label(interface, text="Variables géométrique", width=30, font="Helvetica 12 bold", bg="gray")
lbl2.place(x=0, y=80)

lbl3 = Label(interface, text="Longueur du lien L0", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl3.place(x=0, y=120)

txtL1 = Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtL1.insert(0,"3")
txtL1.place(x=200, y=120)

lbl4 = Label(interface, text="Longueur du lien L1", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl4.place(x=0, y=160)

txtL2 = Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtL2.insert(0,"3")
txtL2.place(x=200, y=160)

lbl5 = Label(interface, text="Longueur du lien L2", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl5.place(x=0, y=200)

txtL3 = Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtL3.insert(0,"3")
txtL3.place(x=200, y=200)

lbl6 = Label(interface, text="Variables articulaire", width=30, font="Helvetica 12 bold", bg="gray")
lbl6.place(x=0, y=240)

lbl7 = Label(interface, text="Mésure l'angle 01", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl7.place(x=0, y=280)

txtTeta1 = Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtTeta1.insert(0,"3")
txtTeta1.place(x=200, y=280)

lbl8 = Label(interface, text="Mésure l'angle 02", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl8.place(x=0, y=320)

txtTeta2= Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtTeta2.insert(0,"3")
txtTeta2.place(x=200, y=320)

lbl9 = Label(interface, text="Point B à atteindre", width=30, font="Helvetica 12 bold", bg="gray")
lbl9.place(x=0, y=360)

lbl10 = Label(interface, text="Abscisse du point B", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl10.place(x=0, y=400)

txtXB= Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtXB.insert(0,"3")
txtXB.place(x=200, y=400)

lbl11 = Label(interface, text="Ordonnée point B", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl11.place(x=0, y=440)

txtYB= Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtYB.insert(0,"3")
txtYB.place(x=200, y=440)

lbl12 = Label(interface, text="Paramètres du mouvement", width=30, font="Helvetica 12 bold", bg="gray")
lbl12.place(x=0, y=480)

lbl13 = Label(interface, text="Nombre de pas", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl13.place(x=0, y=520)

txtNbrePas= Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtNbrePas.insert(0,"3")
txtNbrePas.place(x=200, y=520)

lbl14 = Label(interface, text="Durée du trajet A-B", width=23, font="Helvetica 12 bold", bg="#d5f5E3")
lbl14.place(x=0, y=560)

txtL9= Entry(interface, bd=0, width=8, font="Helvetica 12 bold")
#txtL9.insert(0,"3")
txtL9.place(x=200, y=560)




lbl15 = Label(interface, text="Boutons du simulateur", width=30, font="Helvetica 12 bold", bg="gray")
lbl15.place(x=900, y=40)














btn1 = Button(interface, text="Demo", bd=0, width=20, bg='orange',fg='white', height=2, activeforeground="black", activebackground="green", font="Helvetica 12 bold", command=demo)
btn1.place(x=940, y=80)

btnTrajec = Button(interface, text="Dessiner", bd=0, width=20, height=2,bg='green',fg='white', activeforeground="black", activebackground="green", font="Helvetica 12 bold", command=fncInitialisation)
btnTrajec.place(x=940, y=160)

btn1 = Button(interface, text="Simuler", bd=0, width=20, height=2, bg='green',fg='white', activeforeground="black", activebackground="green", font="Helvetica 12 bold", command=avance)
btn1.place(x=940, y=240)

btn1 = Button(interface, text="Nouveau", bd=0, width=20, height=2,bg='gray',fg='white', activeforeground="black", activebackground="green", font="Helvetica 12 bold", command=nouveau)
btn1.place(x=940, y=320)

btn1 = Button(interface, text="Quitter", bd=0, width=20, height=2,bg='red',fg='white', activeforeground="black", activebackground="green", font="Helvetica 12 bold", command=interface.quit)
btn1.place(x=940, y=400)

lbl12 = Label(interface, text="Auteur de l'interface", width=30, font="Helvetica 12 bold", bg="gray")
lbl12.place(x=900, y=480)

lbl12 = Label(interface, text="Paramètres du mouvement", width=60, font="Helvetica 12 bold", bg="gray")
lbl12.place(x=290, y=540)

'''img = ImageTk.PhotoImage(Image.open("guypi.png"))
panel = Label(interface, image = img,width=200, height=150)
panel.place(x=920, y=520)
'''
scrollbar = Scrollbar(interface)
scrollbar.place(x=890, y=570)
#scrollbar.pack(fill="y")

listbox = Listbox(interface, width=100,yscrollcommand=scrollbar.set)
listbox.place(x=290, y=570)
#listbox.pack(fill="both")
#for line in range(100):
 #      listbox.insert(END, "le nombre de ligne" + str(line))
listbox.insert(END, "Démarrage du programe "+ str(time.ctime()))
scrollbar.config(command=listbox.yview)

graph = Canvas(interface, width=610, height=460)
graph.place(x=280,y=40)
schema = plt.figure(figsize=(12, 10), dpi=50)
plot = schema.add_subplot(1, 1, 1)
plot.set_xlabel('Axe Y0')
plot.set_ylabel('Axe X0')
plot.yaxis.set_ticks_position('right')
plot.set_xticks(range(16))
plot.set_yticks(range(16))
plot.set_xlim((15,-1))
plot.set_ylim((-1, 15))
plot.grid(True)

graphique = FigureCanvasTkAgg(schema, graph)
graphique.draw()
graphique.get_tk_widget().pack()

interface.mainloop()