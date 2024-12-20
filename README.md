
## **Description du Projet**

Ce projet vise à mettre en place une solution **MLOps** complète, intégrant les principes **DevOps** pour le déploiement et la surveillance d'un modèle de Machine Learning. L’infrastructure repose sur des outils modernes pour automatiser les processus, assurer le suivi des versions et monitorer les performances. Les éléments clés sont les suivants :

1. **Infrastructure automatisée** avec **Terraform** pour configurer les ressources cloud (AWS EC2).
2. **Gestion des serveurs** avec **Ansible** pour installer les outils requis (Docker, Grafana, Prometheus).
3. **Containerisation** via **Docker** pour faciliter les déploiements.
4. **CI/CD** utilisant **GitHub Actions** pour tester, construire et déployer les applications.
5. **Monitoring** à l'aide de **Prometheus** pour collecter les métriques et **Grafana** pour les visualiser.

L'application propose une **API Flask** pour effectuer des prédictions grâce à un modèle ML entraîné avec **LGBM**.

---

## **1. Infrastructure**

### **1.1. Configuration de la clé SSH**

Avant de commencer, une clé SSH est nécessaire pour accéder à l’instance EC2 :

1. Créez une paire de clés avec `ssh-keygen` :
   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/myKey.pem
   ```
2. Rendez la clé privée utilisable :
   ```bash
   chmod 600 ~/.ssh/myKey.pem
   ```
3. Ajoutez la clé publique dans la configuration Terraform.
4. Connectez-vous à l’instance EC2 :
   ```bash
   ssh -i ~/.ssh/myKey.pem ec2-user@<PUBLIC_IP>
   ```

---

### **1.2. Outils Utilisés**

- **Terraform** : Permet de décrire et provisionner les ressources cloud.
- **Ansible** : Configure automatiquement les serveurs pour installer les outils nécessaires.

---

### **1.3. Déploiement avec Terraform**

1. Initialisez Terraform :
   ```bash
   cd terraform
   terraform init
   ```
2. Vérifiez les changements à appliquer :
   ```bash
   terraform plan
   ```
3. Appliquez la configuration :
   ```bash
   terraform apply
   ```

---

### **1.4. Configuration des Serveurs avec Ansible**

1. Configurez le fichier `hosts.ini` :
   ```ini
   [docker_host]
   <PUBLIC_IP> ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/myKey.pem
   ```
2. Exécutez le playbook pour installer Docker :
   ```bash
   cd ansible
   ansible-playbook -i hosts.ini playbooks/setup_docker.yml
   ```
3. Vérifiez l’installation :
   ```bash
   docker --version
   ```

---

## **2. Application ML**

### **2.1. Entraînement du Modèle**

1. **LGBM** est utilisé pour entraîner un modèle à partir d’un jeu de données.
2. **MLflow** assure le suivi des expériences et des versions des modèles.
3. Lancez l’entraînement :
   ```bash
   cd ml/model
   python train_model.py
   ```
4. Visualisez les résultats avec MLflow :
   ```bash
   mlflow ui
   ```
   Accédez à l’interface via `http://127.0.0.1:5000`.

---

### **2.2. Déploiement de l’API Flask**

1. Lancez l’API en local :
   ```bash
   cd ml/api
   python app.py
   ```
2. Testez les prédictions :
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"features": [[8.3252, 41, 6.9841, 1.023810, 322, 2.5556, 37.88, -122.23]]}' \
   http://127.0.0.1:5001/predict
   ```

---

## **3. Monitoring**

### **3.1. Mise en Place**

1. Copiez les fichiers nécessaires sur l’instance :
   ```bash
   rsync -av -e "ssh -i ~/.ssh/myKey.pem" monitoring ec2-user@<PUBLIC_IP>:/home/ec2-user/
   ```
2. Configurez Prometheus (`prometheus.yml`) :
   ```yaml
   scrape_configs:
     - job_name: 'api'
       static_configs:
         - targets: ['api:5001']
   ```
3. Configurez Grafana pour utiliser Prometheus comme source de données.

---

### **3.2. Lancement des Services**

1. Démarrez les services avec Docker :
   ```bash
   cd docker
   docker-compose up -d
   ```
2. Accédez aux interfaces :
   - **Prometheus** : `http://<PUBLIC_IP>:9090`
   - **Grafana** : `http://<PUBLIC_IP>:3000`

---
