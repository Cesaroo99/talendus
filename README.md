# Talendus

Site et plateforme de **Talendus**, plateforme de recrutement pour toutes les entreprises.

Devise : *Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.*

## Comment le site se met à jour

Vous n’avez rien à installer. Les changements se font ici, dans Cursor :

1. On modifie le site dans Cursor.
2. Les **tests** tournent tout seuls (rien n’est publié s’ils échouent).
3. Quand les tests sont verts, le code est fusionné dans `main`.
4. Render **rebuild** le site et ne bascule le trafic que si `/api/health` répond.

Résultat : une modification validée ici se retrouve sur le site en production, sans manipulation technique de votre part.

**Gardes-fous :** pas de contact direct employeur–candidat, secrets forts obligatoires, PostgreSQL uniquement en production, pas de fausses données de démo en ligne, documentation API fermée au public, déploiement seulement si la CI est verte.

## Première mise en ligne (une seule fois)

Le code est prêt. Il reste deux actions que seul le propriétaire du compte peut cliquer :

1. Fusionner / laisser GitHub Actions fusionner la pull request vers `main`.
2. Sur [Render](https://dashboard.render.com) : **New → Blueprint** → dépôt `Cesaroo99/talendus`, branche `main`. Render crée le site, la base PostgreSQL et le disque des CV.

Le mot de passe initial du compte `lea.super@talendus.ca` est dans Render → le service `talendus-web` → **Environment** → `ADMIN_PASSWORD`. Changez-le à la première connexion (`/admin/`).

Le site sera d’abord disponible en `https://talendus-web-….onrender.com`. Le nom `talendus.ca` s’ajoute ensuite dans Render → **Custom Domain** (DNS chez le registrar).

## Technique

- Front : pages HTML générées par `scripts/build_pages.py`
- API : [`backend/README.md`](backend/README.md)
- Production : `Dockerfile`, `render.yaml`, `.github/workflows/ci.yml`
