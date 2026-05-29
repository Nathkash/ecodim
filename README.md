# 📚 Écodim — Système de Gestion de l'École du Dimanche

Application web Django pour la gestion des enfants, leçons et présences de l'École du Dimanche.

## Fonctionnalités
- Gestion des enfants (2 classes selon l'âge)
- Planning des leçons avec assignation aux moniteurs
- Feuilles de présence par séance
- Tableau de bord Président et Moniteur
- Interface responsive mobile

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/TON_USERNAME/ecodim.git
cd ecodim
```

### 2. Créer l'environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Migrations
```bash
python manage.py migrate
```

### 5. Créer les classes A et B
```bash
python manage.py init_classes
```

### 6. Créer le compte Président
```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

## Technologies
- Python / Django
- HTML5 / CSS3
- Font Awesome
- Google Fonts (Inter)