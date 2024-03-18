import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

print("initialisation starting...")

from use_fonction.screen_capture.screen_initialisation import screen_initialisation

# Créer système de capture video
windows_capture = screen_initialisation()
img = windows_capture.get_screen()

# img = cv2.imread('test0.png')
_,w_img,h_img = img.shape[::-1]
w_work,h_work=445,800   #dimension de la fenêtre sur laquelle les vignettes ont été créées
# print(w_img,h_img)
# print(w_work,h_work)
facteur_estimé = w_img/w_work  # on estime la taille des vignettes dans la nouvelle dimension
print("estimation du facteur d'échelle : ",facteur_estimé)

data = {
    "ROI_cartes":[[106,673,63,80],
            [190,673,63,80],
            [275,673,63,80],
            [359,673,63,80]],
    "ROI_elixir":[119,785,311,1],
    "ROI_tower":[[315,125,52,70],
           [80,125,52,70],
           [78,456,54,65],
           [313,456,54,65]]
}

def find_correspondant_size(temp,img):
    _,w_temp,h_temp = temp.shape[::-1]
    max_correspondance=0

    for w in range(int(facteur_estimé*w_temp*0.8),int(facteur_estimé*w_temp*1.2),1):
        h=int(h_temp * w/w_temp)
        resized = cv2.resize(temp, (w, h), interpolation=cv2.INTER_AREA)
        resultat = cv2.matchTemplate(img, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultat)
        if max_val>max_correspondance:
            max_correspondance=max_val
            x, y = max_loc
            w_m,h_m=w,h
    return [x,y,w_m,h_m],max_correspondance

def find_cartes(chemin_dossier,img):
    liste_roi=[]
    liste_max=[]
    print("esssaye de trouver une correspondance pour les cartes")
    for fichier in tqdm(os.listdir(chemin_dossier)):
        chemin_complet = os.path.join(chemin_dossier, fichier)
        vignette=cv2.cvtColor(cv2.imread(chemin_complet),cv2.COLOR_BGR2RGB)
        roi,max_correspondance = find_correspondant_size(vignette,img)
        liste_roi.append(roi)
        liste_max.append(max_correspondance)
    rois_et_valeurs = list(zip(liste_roi, liste_max))
    rois_et_valeurs_tries = sorted(rois_et_valeurs, key=lambda x: x[1], reverse=True)
    meilleurs_rois = rois_et_valeurs_tries[:4]
    meilleurs_rois_carte = [roi[0] for roi in meilleurs_rois]
    for i in meilleurs_rois_carte:
        x,y,w_m,h_m=i
        print(i)
        cv2.rectangle(img, (x, y), (x + w_m, y + h_m), (0, 255, 0), 2)
    return meilleurs_rois_carte

meilleurs_rois_carte = find_cartes("use_fonction/vignettes/",img)
data["ROI_cartes"] = meilleurs_rois_carte

gauche_img = img[:,0:w_img//2,:]
droite_img = img[:,w_img//2:,:]

ROI_tower=[0,0,0,0]
template=cv2.cvtColor(cv2.imread("use_fonction/towers/tower_red.jpg"),cv2.COLOR_BGR2RGB)

print("ROI_tower:")
ROI_tower[0],_=find_correspondant_size(template,droite_img)
ROI_tower[1],_=find_correspondant_size(template,gauche_img)
template=cv2.cvtColor(cv2.imread("use_fonction/towers/tower_blue.jpg"),cv2.COLOR_BGR2RGB)
ROI_tower[2],_=find_correspondant_size(template,gauche_img)
ROI_tower[3],_=find_correspondant_size(template,droite_img)

ROI_tower[0][0] = ROI_tower[0][0]+w_img//2
ROI_tower[3][0] = ROI_tower[3][0]+w_img//2

for i in ROI_tower:
    x,y,w_m,h_m=i
    print(i)
    cv2.rectangle(img, (x, y), (x + w_m, y + h_m), (0, 255, 0), 2)

data["ROI_tower"] = ROI_tower

def detecter_barre_violette(image):
    # Convertir l'image en espace HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # cv2.imshow("Resultat", hsv)

    # Définir les seuils pour la couleur violette dans l'espace HSV
    # Ces valeurs peuvent nécessiter un ajustement pour votre application spécifique
    violet_bas = np.array([130, 50, 50])
    violet_haut = np.array([160, 255, 255])

    # Masque pour extraire la couleur violette
    masque = cv2.inRange(hsv, violet_bas, violet_haut)
    # plt.imshow(cv2.cvtColor(masque, cv2.COLOR_BGR2RGB))
    # plt.show()

    # Opérations morphologiques pour améliorer la continuité
    noyau = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1))
    masque = cv2.morphologyEx(masque, cv2.MORPH_CLOSE, noyau)

    # Initialiser les variables pour trouver la plus longue barre horizontale
    max_longueur = 0
    roi_max = (0, 0, 0, 0)  # x, y, largeur, hauteur

    # Analyser chaque ligne du masque pour trouver la plus longue séquence continue de pixels violets
    for y in range(masque.shape[0]):
        x_start = None
        for x in range(masque.shape[1]):
            if masque[y, x] == 255:  # Pixel violet
                if x_start is None:
                    x_start = x  # Début d'une séquence violette
            else:
                if x_start is not None:
                    longueur = x - x_start
                    if longueur > max_longueur:
                        max_longueur = longueur
                        roi_max = (x_start, y, longueur, 1)  # Hauteur fixée à 1 pour une ligne
                    x_start = None  # Réinitialiser pour la prochaine séquence
        # Vérifier la dernière séquence de la ligne
        if x_start is not None:
            longueur = masque.shape[1] - x_start
            if longueur > max_longueur:
                max_longueur = longueur
                roi_max = (x_start, y, longueur, 1)

    # Retourner la ROI de la plus grande barre horizontale
    return roi_max

# Détecter la barre violette
x, y, w, h = detecter_barre_violette(img)

# Ajuster x et w pour retirer le premier onzième de la barre
decalage = w // 11  # Calculer un onzième de la largeur de la barre
x_ajuste = x + decalage  # Décaler le début de la barre vers la droite
w_ajuste = w - decalage  # Réduire la largeur de la barre pour exclure le premier onzième

cv2.rectangle(img, (x_ajuste, y), (x_ajuste+w_ajuste, y+h), (0, 255, 0), 2)

data["ROI_elixir"] = [x_ajuste,y,w_ajuste,1]
print("ROI elixir :",data["ROI_elixir"])

# Afficher l'image avec le rectangle
plt.imshow(img)
plt.title('Correspondance trouvée')
plt.show()

with open('use_fonction/configuration/roi_data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)