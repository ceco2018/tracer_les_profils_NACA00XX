import numpy as np
import matplotlib.pyplot as plt

print("------------------------------------------------- MGA802 --------------------------------------------------")
print("-------- CE PROGRAMME PERMET DE TRACER TOUT TYPE DE PROFILS NACA 00XX A PARTIR DE SES COORDONNEES ---------")

# -------------- Constantes de la fonction de paramétrage du NACA 00XX
coeff_naca = [0.2969, -0.1260, -0.3516, 0.2843, -0.1036]
pow_naca = [0.5, 1, 2, 3, 4]

# -------------- PARAMETRES DU PROFIL NACA 00XX
# ---- Fournir la référence du profil
reference_du_profil = []
count_ref_profil = 0
while (reference_du_profil[0:7] != "NACA 00") or (len(reference_du_profil) != len("NACA 00XX")):
    if count_ref_profil == 0:
        reference_du_profil = str(input("\nEntrer la reference du profil au format - NACA 00XX - : "))
    else:
        print("\nAttention ! La reference du profil doit respecter le format - NACA 00XX - ")
        reference_du_profil = str(input("\nEntrer de nouveau la reference du profil format - NACA 00XX - : "))
    count_ref_profil += 1

# ---- Fournir la longueur de corde du profil
corde_en_metre = float(input("\nEntrer la longueur de la corde en mètre : "))       # [m] corde en mètre
corde_adim = corde_en_metre/corde_en_metre                                          # [-] corde adimensionnelle

# ---- Fournir le nombre de points de long de la courbe pour le tracé
nbre_de_points = int(input("\nEntrer le nombre de points de discrétisation : "))

# ---- Fournir le type de distribution de points le long de la corde (linéaire ou non-uniforme)
type_de_distribution = int(input("\nChoisir le type de distribution de discrétisation. "
                                 "\n  -1- pour distribution linéaire \n  -2- pour distribution non-uniforme "
                                 "\n  Entrer votre choix : "))

# -------------- épaisseur maximale relative du profil
tmax_relative = int(reference_du_profil[7:10])/100

# -------------- Coordonnées adimensionnelles xc sur la corde
if type_de_distribution == 1:
    distribution = "uniforme"
    # ---- coordonnées adimensionnelles xc sur la corde, avec la distribution linéaire
    xc = np.linspace(0, corde_adim, nbre_de_points + 1)

elif type_de_distribution == 2:
    distribution = "non-uniforme"
    # ---- coordonnées adimensionnelles xc sur la corde, avec la transformation de Glauert
    xi = np.linspace(0, np.pi, nbre_de_points + 1)
    xc = 0.5 * (1 - np.cos(xi))

# -------------- Coordonnées adimensionnelles yt de la demi-épaisseur, avec la fonction de paramétrage
# initialisation
yt = np.zeros_like(xc)  # initialisation
# remplissage du vecteur de coordonné
for i in range(len(xc)):
    for j in range(len(coeff_naca)):
        yt[i] += coeff_naca[j] * xc[i] ** pow_naca[j]
    yt[i] *= (5 * tmax_relative)

# -------------- Construire les tableaux de coordonnées (xup, yup) et (xdown, ydown) selon le nombre de points requis
# ---- sur l'extrados (xup, yup)
xup = xc * corde_adim
yup = yt * corde_adim

# ---- sur l'intrados (xdown, ydown)
xdown = xc * corde_adim
ydown = -yt * corde_adim

# -------------- Calculer l’épaisseur maximale et la position de ce maximum le long de la corde
# ---- variation de l'épaisseur le long de la corde
thickness = yup - ydown

# ---- déduire l'épaisseur maximale
tmax = np.max(thickness)*corde_en_metre  #[m]

# ---- position de l'épaisseur maximale le long de la corde
index = np.argmax(thickness)
xc_tmax = xc[index]  # abscisse du maximum d'épaisseur

# ---- Affichage des résultats pour l'utilisateur
print(f'Épaisseur maximale                                   = {tmax} [m]')
print(f'Épaisseur maximale relative "tmax/corde"             = {100 * tmax / corde_en_metre} [%]')
print(f"Position de l'épaisseur maximale le long de la corde : {xc_tmax * 100} [%]")


# -------------- Affichage du profil
plt.figure(1)
plt.plot(xup, yup, '-o', xdown, ydown, '-s')
plt.legend(['extrados', 'intrados', 'reference'])
plt.title(f'NACA 00{int(reference_du_profil[7:10])} - {nbre_de_points} points - {distribution}')
plt.xlim([0, 1.2 * corde_adim])
plt.ylim([-0.05, 0.05])
plt.grid()
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()

print("_________________________________________________________________________________________________________")
print("*----**----**----**----**----**----**----** Fin du programme ! **----**----**----**----**----**----**----*")
