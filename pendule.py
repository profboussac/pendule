import matplotlib.pyplot as plt  # permet de tracer un pgraphe
import numpy as np              # permet de faire des calculs sur des listes
from math import pi

#paramètres de l'expérience
m=0.163 # masse en kg
l=0.52 # longeur du pendule en m
g= 9.81 # intensité de pesanteur SI
periode_propre=2*pi*(l/g)**(1/2)
print("la valeur de la pseudo période propre est: ", periode_propre," s")

# lecture des mesures obtenues avec le gyroscope
# indiquer ci-dessous le chemin du fichier qui contient les mesures
t,omegax,omegay,omegaz,norme = np.genfromtxt('mesures.csv', delimiter=';',unpack=True)

# indiquer ci-dessous le nombre de lignes d'en-tete
lignes_intro=1
t=t[lignes_intro:]
omega=omegax[lignes_intro:]


# Recherche des annulations de vitesse angulaires
dates_omega_nulle=[]
omega_nulle=[]
index_omega_nulle=[]
for i in range(len(t)):
    if omega[i]==0 or omega[i]>0 and omega[i+1]<0:
        dates_omega_nulle.append(t[i])
        omega_nulle.append(omega[i])
        index_omega_nulle.append(i)
dates_omega_nulle=np.asarray(dates_omega_nulle)
index_omega_nulle=np.asarray(index_omega_nulle)
omega_nulle=np.asarray(omega_nulle)

# Tracés des valeurs expérimentales de la vitesse angulaire
plt.subplot(311)
plt.xlabel("temps (s)")
plt.plot(t,omega,label="vitesse angulaire (rad/s)")
plt.scatter(dates_omega_nulle,omega_nulle,marker="+",color="black")
for i in range(len(dates_omega_nulle)):
    plt.text(dates_omega_nulle[i],1,i)
plt.legend()

# calcul de la pseudo-période = valeur moyenne sur plusieurs pseudo périodes
premier_point=13
dernier_point=30
ti=dates_omega_nulle[premier_point]
tf=dates_omega_nulle[dernier_point]
dates_omega_nulle=dates_omega_nulle[premier_point:dernier_point]
omega_nulle=omega_nulle[premier_point:dernier_point]
index_omega_nulle=index_omega_nulle[premier_point:dernier_point]

pseudo_periode=(dates_omega_nulle[-1]-dates_omega_nulle[0])/(len(dates_omega_nulle)-1)

# affichage de la valeur expérimentale dela pseudo période
plt.plot([ti,ti],[-2,2],color="black", linestyle="--")
plt.plot([tf,tf],[-2,2],color="black",linestyle="--")
plt.text(ti,2,"la valeur expérimentale de la pseudo période est: {} s".format(round(pseudo_periode,2)))



# recherche du premier maximum local de vitesse anngulaire et décalage des dates
premier_max=np.max(omega[index_omega_nulle[0]:index_omega_nulle[1]])
for i in range(index_omega_nulle[0],index_omega_nulle[1]):
    if omega[i]==premier_max:
        i0=i
        t0=t[i]

t=t-t0
dates_omega_nulle=dates_omega_nulle-t0

ifinal=index_omega_nulle[-1]
omega=omega[i0:ifinal]
t=t[i0:ifinal]

# Calcul de theta
theta=[0]
for i in range(1,len(t)):
    thetai=theta[i-1]+omega[i]*(t[i]-t[i-1])
    theta.append(thetai)
theta_mediane=np.median(theta[index_omega_nulle[1]:]) # on apporte une correction de manière à ce que la valeur médiane de theta sur un nombre entier de période soit nulle
theta=theta-theta_mediane


#calcul de l'énergie cinétique
Ec= 0.5*m*(l*omega)**2

#calcul de l'énergie potentielle de pesanteur
Epp=m*g*l*(1-np.cos(theta))   # initialisation de la liste de l'énergie potentielle de pesanteur

#calcul de l'énergie mécanique
Em=Ec+Epp

# Tracés
plt.subplot(312)
plt.xlabel("temps (s)")
plt.plot(t,omega,label="vitesse angulaire (rad/s)")
plt.plot(t,theta,label="angle theta (rad)")
plt.legend()

plt.subplot(313)
plt.xlabel("temps (s)")
plt.ylabel("énergie (J)")
plt.plot(t,Ec,label="énergie cinétique")
plt.plot(t,Epp,label="énergie potentielle de pesanteur")
plt.plot(t,Em,label="énergie mécanique du pendule")
plt.legend()
plt.show()
plt.close()



