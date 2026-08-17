# Talendus

Site et espace de **Talendus**, agence de placement intelligente.

Devise : *Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.*

Talendus n'est pas un job board ni un logiciel ATS en libre-service. L'entreprise confie un besoin ; Talendus recherche, présélectionne et présente une shortlist. L'entreprise garde la décision finale. L'intelligence artificielle est déjà utilisée dans les outils internes de Talendus ; elle n'est pas un produit que le client opère lui-même.

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

Le site sera d’abord disponible en `https://talendus-web.onrender.com`. Pour que `https://talendus.ca` s’ouvre (et reste ouvert) :

1. Dans Render → service **talendus-web** → **Custom Domains** : ajouter `talendus.ca` et `www.talendus.ca`.
2. Chez Namespro, **désactiver** le transfert de site / parking / « Website Forwarding ». C’est ce qui envoie aujourd’hui le domaine vers `51.222.143.2` avec un certificat SSL Namespro expiré — le navigateur refuse alors la page.
3. Enregistrements DNS Namespro (serveurs de noms `htns1/2/3.namespro.ca` inchangés) :

| Type | Hôte | Valeur |
| --- | --- | --- |
| A | `@` | `216.24.57.1` |
| CNAME | `www` | `talendus-web.onrender.com` |

Supprimer l’ancien A vers `51.222.143.2`, le CNAME `www` → `talendus.ca`, tout transfert URL, et tout enregistrement **AAAA**.
4. Dans Render, cliquer **Verify**. Le certificat HTTPS est émis par Render (Let’s Encrypt), pas par Namespro.
5. Variable d’environnement `FRONTEND_URL=https://talendus.ca` (déjà dans `render.yaml`).

Tant que le DNS n’est pas corrigé, le site reste joignable sur `https://talendus-web.onrender.com`.

## Technique

- Front : pages HTML générées par `scripts/build_pages.py`
- API : [`backend/README.md`](backend/README.md)
- Production : `Dockerfile`, `render.yaml`, `.github/workflows/ci.yml`
