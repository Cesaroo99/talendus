# Talendus API

Back-end FastAPI de la plateforme de recrutement industriel **Talendus**.
Le site public (HTML/CSS/JS) continue de vivre à la racine du dépôt ; cette API en est le cerveau.

## Installation

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Éditez `.env` : changez `SECRET_KEY`, `JWT_SECRET` et, en production, `DATABASE_URL`.

## Configuration

Toutes les valeurs sensibles sont lues depuis l’environnement (fichier `.env` local).

| Variable | Rôle |
| --- | --- |
| `DATABASE_URL` | SQLite par défaut, PostgreSQL en production (`postgresql+psycopg://…`) |
| `JWT_SECRET` | Signature des jetons d’accès |
| `SECRET_KEY` | Secret applicatif |
| `FRONTEND_URL` | Liens dans les courriels |
| `CORS_ORIGINS` | Origines autorisées |
| `EMAIL_SERVER` / `EMAIL_USERNAME` / `EMAIL_PASSWORD` | SMTP |
| `EMAIL_ENABLED` | `false` = log sans envoi réel |
| `STORAGE_DIR` | Répertoire des CV |
| `MAX_RESUME_MB` | Taille max d’un CV |
| `SEED_PASSWORD` | Mot de passe des comptes de démonstration |

Voir `.env.example`.

## Lancement local

Depuis `backend/` :

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L’API est préfixée par `/api`. Le site statique du dépôt est aussi servi à la racine.

- Santé : `GET /api/health`
- OpenAPI / Swagger : [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc : [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## Base de données et seed

Au démarrage, l’application crée les tables (`create_all`) puis insère un jeu de données s’il n’existe aucun utilisateur.

```bash
python -m app.seed
```

Comptes de démonstration (mot de passe `talendus` sauf si `SEED_PASSWORD` est modifié) :

- `sophie.admin@talendus.ca` — ADMIN
- `marc.recruiter@talendus.ca` — RECRUITER
- `camille.recruiter@talendus.ca` — RECRUITER
- `nathalie.finance@talendus.ca` — FINANCE
- `alex.editeur@talendus.ca` — EDITOR
- `karine.lavoie@email.ca` — CANDIDATE

Les slugs d’offres (`cariste`, `soudeur`, …) correspondent aux pages HTML publiques.

Pour PostgreSQL, créez la base puis pointez `DATABASE_URL`. Alembic pourra être ajouté plus tard ; le schéma actuel est porté par les modèles SQLAlchemy.

## Architecture

```
backend/app/
  api/           # routes REST
  models/        # entités SQLAlchemy
  services/      # logique métier
  emails/templates/
  middleware.py  # rate limit + en-têtes
  security.py    # JWT / bcrypt
  rbac.py        # permissions
  errors.py      # format d’erreur unique
  seed.py
```

Couches : routes → services → modèles. Les e-mails et notifications sont découplés de la requête métier (un échec SMTP n’empêche pas une candidature).

## Authentification

- Inscription publique : rôles `CANDIDATE` et `EMPLOYER` uniquement
- Connexion / refresh / déconnexion
- Vérification d’e-mail, mot de passe oublié / réinitialisé / changé
- Jetons JWT (accès) + refresh stocké hashé en base
- Mots de passe hashés avec bcrypt (jamais en clair)

Header : `Authorization: Bearer <access_token>`

## Rôles et permissions

| Rôle | Accès principal |
| --- | --- |
| CANDIDATE | profil, CV, offres publiques, candidatures personnelles |
| EMPLOYER | entreprise, offres, candidatures reçues |
| RECRUITER | missions, candidats, notes internes, statuts |
| ADMIN | tout le système, utilisateurs, logs, e-mails |
| FINANCE / EDITOR | modules back-office (finance / contenu) |

Un candidat ne peut pas lire le dossier d’un autre candidat ni une candidature qui n’est pas la sienne (contrôle IDOR dans les services).

## Endpoints

Préfixe `/api`. Réponse succès :

```json
{ "success": true, "data": {}, "message": "…", "meta": {} }
```

Erreur :

```json
{ "success": false, "message": "Une candidature existe déjà pour cette offre.", "code": "APPLICATION_ALREADY_EXISTS", "details": [] }
```

| Méthode | Chemin | Auth |
| --- | --- | --- |
| POST | `/auth/register` `/auth/login` `/auth/refresh` `/auth/logout` | mixte |
| POST | `/auth/forgot-password` `/auth/reset-password` `/auth/change-password` `/auth/verify-email` | mixte |
| GET/PATCH | `/users/me` | oui |
| GET/PATCH | `/candidates/me` + expériences, formation, certifications, CV | candidat |
| GET | `/jobs` `/jobs/{slug}` | public |
| POST | `/jobs` + publish/pause/close/archive | employeur / recruteur / admin |
| POST | `/applications` `/applications/public` | candidat / public |
| GET | `/applications/me` | candidat |
| POST | `/applications/{id}/status` | staff |
| GET | `/notifications` `/notifications/unread` | oui |
| GET | `/admin/users` `/admin/audit` `/admin/stats` `/emails` | admin |
| POST | `/contact` | public |

La documentation interactive liste tous les schémas.

## Notifications et e-mails

Les événements (compte créé, candidature, changement de statut, CV, entretien) créent une notification en base. Les templates texte sont dans `app/emails/templates/`. Chaque envoi est journalisé (`email_logs`) : destinataire, type, statut, erreur.

## Sécurité

- Validation Pydantic côté serveur
- RBAC + vérifications d’appartenance (anti-IDOR)
- CORS configurable, en-têtes de sécurité, rate limiting
- Upload CV : PDF/DOC/DOCX, taille max, MIME magique, nom sanitizé, téléchargement authentifié
- Logs d’audit sans mot de passe ni jeton

## Tests

```bash
cd backend
pytest -q
```

Couvrent inscription, connexion, permissions, publication d’offre, candidature, doublon, statut, notifications et accès interdit.

## Déploiement

1. Python 3.11+
2. `DATABASE_URL` PostgreSQL recommandé
3. Secrets forts, `APP_ENV=production`, `DEBUG=false`, `EMAIL_ENABLED=true`
4. Reverse proxy (HTTPS) vers `uvicorn` / `gunicorn`
5. Volume persistant pour `STORAGE_DIR`
6. Le front existant appelle `/api` ; en production, servir l’API et le site sous le même domaine ou ajuster `CORS_ORIGINS`

## Évolutions prévues (non implémentées)

Matching / scoring, messagerie, calendrier d’entretiens, signature, facturation CRM, intégrations job boards. Les modèles (`RecruitmentMission`, `Contract`, `InternalNote`, `Role` / `Permission`) sont déjà en place pour le back-office.
