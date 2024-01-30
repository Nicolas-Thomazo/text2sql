# Text2SQL: dockerfiles

Ce répertoire contient les dockerfiles et les docker-composes utilisés pour les micro-services.

Les images et docker-composes doivent etre lancés depuis la racine du projet avec l'option `-f` pour spécifier le fichier dockerfile/docker-compose à utiliser.

## Dockerfiles

Les dockerfiles sont dans le répertoire `dockerfiles`. Ils sont nommés selon la convention suivante : `Dockerfile.<nom_du_service>`.

## Docker-compose

Les docker-compose sont dans le répertoire `docker-compose`. Ils sont nommés selon la convention suivante : `docker-compose.<nom_du_service>.yml`.

## Construction des images

Pour construire une image, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker build -f dockerfiles/Dockerfile.<nom_du_service> -t <nom_du_service> .
```

## Lancement des services

Pour lancer un service, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml up -d <--force-recreate>
```

## Arrêt des services

Pour arrêter un service, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down
```

## Arrêt et suppression des services

Pour arrêter et supprimer un service, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down --rmi all
```

## Arrêt et suppression des services et des volumes

Pour arrêter et supprimer un service et les volumes associés, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down --rmi all -v
```

## Arrêt et suppression des services et des volumes et des images

Pour arrêter et supprimer un service et les volumes associés et les images, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down --rmi all -v --remove-orphans
```

## Arrêt et suppression des services et des volumes et des images et des réseaux

Pour arrêter et supprimer un service et les volumes associés et les images et les réseaux, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down --rmi all -v --remove-orphans --remove-networks
```

## Arrêt et suppression des services et des volumes et des images et des réseaux et des images non utilisées

Pour arrêter et supprimer un service et les volumes associés et les images et les réseaux et les images non utilisées, il faut se rendre à la racine du projet et lancer la commande suivante :

```bash
docker-compose -f docker-compose/docker-compose.<nom_du_service>.yml down --rmi all -v --remove-orphans --remove-networks --prune-images
```
