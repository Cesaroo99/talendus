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
| `STORAGE_DIR` | Répertoire local des CV |
| `STORAGE_BACKEND` | `local` (défaut) ou `s3` — la base stocke les métadonnées, pas le binaire |
| `S3_BUCKET` / `S3_REGION` / `S3_ENDPOINT_URL` / `S3_ACCESS_KEY` / `S3_SECRET_KEY` | Stockage objet optionnel |
| `MAX_RESUME_MB` | Taille max d’un CV |
| `SEED_PASSWORD` | Mot de passe des comptes de démonstration (jamais en production réelle) |
| `DEFAULT_CURRENCY` | Devise par défaut (`CAD`) |
| `DEFAULT_TAX_RATE_BP` | Taxes en points de base (14975 ≈ TPS+TVQ) |
| `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` | Optionnel — publication LinkedIn (le partage d’URL fonctionne sans) |

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

Au démarrage, l’application crée les tables (`create_all`) puis insère un jeu de **données de démonstration** s’il n’existe aucun utilisateur. Ce seed ne s’exécute pas en production déjà peuplée.

ORM : **SQLAlchemy 2**. Moteur : **SQLite** en développement / tests, **PostgreSQL** recommandé en production via `DATABASE_URL`.

### Lancer la base

```bash
cd backend
cp .env.example .env   # puis éditer DATABASE_URL, JWT_SECRET, SECRET_KEY
alembic upgrade head
python -m app.seed     # no-op si des utilisateurs existent déjà
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

PostgreSQL local :

```bash
createdb talendus
# DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/talendus
cd backend
alembic upgrade head
python -m app.seed
```

Migrations versionnées :

- `0001_initial` — schéma de base
- `0002_ops` — messages, entretiens, factures, signatures
- `0003_platform` — memberships, conversations, lignes de facture, préférences, paramètres, index, nouveaux rôles / statuts

### Tables principales

`users` → `candidates` (profils) → `resumes` → `applications` → `application_status_history`

`users` → `company_memberships` → `companies` → `recruitment_missions` / `contracts` → `job_offers` → `applications`

`users` → `conversations` → `messages` (+ `message_attachments`)

`companies` → `invoices` → `invoice_lines` / `payments`

`users` → `notifications` · `user_preferences`

`system_settings` · `audit_logs`

Autres : `recruiters`, `refresh_tokens`, `email_tokens`, `candidate_experiences`, `candidate_education`, `candidate_certifications`, `interviews`, `internal_notes`, `email_logs`, `roles`, `permissions`, `mission_jobs`, `contract_signatures`.

Les CV ne sont **pas** stockés en binaire dans PostgreSQL : métadonnées + `storage_url` / chemin fichier (`STORAGE_DIR` ou S3 plus tard).

Comptes de démonstration (mot de passe `talendus` sauf si `SEED_PASSWORD` est modifié) :

- `lea.super@talendus.ca` — SUPER_ADMIN
- `sophie.admin@talendus.ca` — ADMIN
- `marc.recruiter@talendus.ca` — RECRUITER
- `camille.recruiter@talendus.ca` — RECRUITER
- `nathalie.finance@talendus.ca` — FINANCE
- `alex.editeur@talendus.ca` — EDITOR
- `karine.lavoie@email.ca` — CANDIDATE
- employeurs liés aux entreprises seed (`j.rivest@metalco.ca`, etc.)

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
| CANDIDATE | profil, CV, offres publiques, candidatures personnelles (sans notes internes) |
| EMPLOYER | entreprise(s) via membership, offres, candidatures reçues |
| RECRUITER | missions, candidats, notes internes, statuts |
| ADMIN | vue globale, utilisateurs, logs, e-mails, paramètres |
| SUPER_ADMIN | mêmes droits admin, rôle maximal (évolutif) |
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
| GET/PATCH | `/users/me` `/users/me/preferences` | oui |
| GET/PATCH | `/candidates/me` + expériences, formation, certifications, CV | candidat |
| GET | `/jobs` `/jobs/{slug}` `/jobs/board` `/job-board` | public |
| POST | `/jobs` + publish/pause/close/archive | employeur / recruteur / admin |
| POST | `/applications` `/applications/public` | candidat / public |
| GET | `/applications/me` | candidat |
| POST | `/applications/{id}/status` | staff |
| GET | `/matching/jobs` | candidat |
| GET | `/matching/jobs/{id}/candidates` | staff / employeur |
| GET/POST | `/messages` `/messages/directory` `/messages/{user_id}` | oui |
| GET/POST | `/interviews` + `/interviews/{id}/status` | mixte |
| GET/POST | `/invoices` + send + payments | finance / admin (lecture recruteur / employeur) |
| GET/POST | `/contracts` `/contracts/{id}/sign` | mixte |
| GET | `/integrations/linkedin` | public |
| GET | `/notifications` `/notifications/unread` | oui |
| GET | `/admin/bootstrap` `/admin/users` `/admin/audit` `/admin/stats` `/admin/settings` `/emails` | staff / admin |
| POST | `/admin/candidates` | recruteur / admin |
| POST | `/contact` | public |

La documentation interactive liste tous les schémas.

## Notifications et e-mails

Les événements (compte créé, candidature, changement de statut, CV, entretien, message) créent une notification en base. Les templates texte sont dans `app/emails/templates/`. Chaque envoi est d’abord journalisé (`QUEUED`, corps persisté) puis traité par un worker qui relit la file en base lorsque SMTP est activé. Un échec d’envoi n’annule pas la candidature. Redis / Celery restent optionnels plus tard.

Espace candidat public : `/espace.html` (EN : `/en/account.html`) — profil, CV, correspondances, candidatures, entretiens, messages, notifications. Le back-office `/admin/` hydrate aussi factures, paiements et entretiens depuis `GET /api/admin/bootstrap`.

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

Couvrent inscription, connexion, permissions, publication d’offre, candidature, doublon, statut, notifications, matching, messagerie, entretiens, factures, signature interne et accès interdit.

## Modules opérationnels

- **Matching** : score déterministe 0–100 (compétences, ville, secteur, expérience, salaire). Pas d’IA générative. Le score est aussi stocké sur la candidature.
- **Messagerie** : fils REST candidat ↔ recruteur / employeur, avec contrôle d’accès. Pas de WebSocket.
- **Entretiens** : CRUD lié à une candidature, confirmation candidat, notification + e-mail.
- **Signature interne** : nom, date, IP, empreinte SHA-256 du mandat. Ce n’est pas DocuSign ni une valeur légale tierce.
- **Facturation** : factures et paiements en base (finance / admin). Pas de Stripe sans clés.
- **Job board** : `GET /api/job-board` (JSON). Partage LinkedIn via URL officielle. Publication automatique seulement si `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` sont définis (`posting_enabled`).

## Déploiement

1. Python 3.11+
2. `DATABASE_URL` PostgreSQL recommandé
3. Secrets forts, `APP_ENV=production`, `DEBUG=false`, `EMAIL_ENABLED=true`
4. Reverse proxy (HTTPS) vers `uvicorn` / `gunicorn`
5. Volume persistant pour `STORAGE_DIR`
6. Le front existant appelle `/api` ; en production, servir l’API et le site sous le même domaine ou ajuster `CORS_ORIGINS`

## Non livré volontairement

Matching LLM, WebSockets, visioconférence Zoom, DocuSign, encaissement Stripe, Redis/Celery obligatoire, publication LinkedIn sans identifiants OAuth.
