# deep-learning-sign-language

lien de la base de donnée : https://www.kaggle.com/gti-upm/leapgestrecog/kernels
Il faut placer la base de donnée décompréssé dans un dossier datasets à la racine du projet.
IL y a deux parties : la partie matlab et partie deep learning.


Pour la partie matlab, il faut lancer reconnaissance.m. On doit décommenter des ligne suivant ce qu'on veut lancer. Tout est doccumenté dans le fichier.

Pour la partie deep learning :

- le fichier preprocess.py transforme les images de la base de données pour être lisible par le réseau de neurones.
- le fichier loadData charge les donnée pré-processé en mémoire.
- le fichier network.py entraine le réseau et stock son modèle dans model.h5

- le fichier loadData_realData charge les données de smartphone et effectue un prétraitement pour les rendre lisible pour le CNN.
- le fichier network_test_realdata.py applique le réseau de neurones aux images de smartphone
