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
| `STORAGE_BACKEND` | `local` (défaut) ou `s3` |
| `S3_BUCKET` / `S3_REGION` / `S3_ENDPOINT_URL` / `S3_ACCESS_KEY` / `S3_SECRET_KEY` / `S3_PREFIX` | Stockage objet optionnel (`STORAGE_BACKEND=s3`) |
| `MAX_RESUME_MB` | Taille max d’un CV |
| `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` / `STRIPE_PUBLISHABLE_KEY` | Checkout Stripe (503 `STRIPE_NOT_CONFIGURED` si absent) |
| `JOB_MATCH_MIN_SCORE` | Seuil de notification `JOB_MATCH` à la publication (défaut 50) |
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

Les CV ne sont **pas** stockés en binaire dans PostgreSQL : métadonnées + `storage_url`. Avec `STORAGE_BACKEND=s3`, l’upload va vers le seau configuré ; sinon fichiers locaux sous `STORAGE_DIR`. Un parse déterministe (PDF/DOCX, sans LLM) remplit `resumes.parse_json` / `parse_status`.

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
| POST | `/applications/{id}/status` | staff (Talendus orchestre le suivi) |
| POST | `/invoices/{id}/checkout` | employeur / finance |
| POST | `/invoices/{id}/paypal` `/invoices/{id}/paypal/capture` `/invoices/{id}/refund` | mixte / finance |
| POST | `/interviews/reminders` | staff |
| POST | `/candidates/{id}/ai` | staff |
| POST | `/contracts/{id}/esign` | staff |
| POST | `/webhooks/stripe` | Stripe (signature, sans JWT) |
| GET | `/matching/jobs` | candidat |
| GET | `/matching/jobs/{id}/candidates` | staff |
| GET/POST | `/messages` `/messages/directory` `/messages/{user_id}` | oui |
| GET/POST | `/interviews` + `/interviews/{id}/status` | mixte |
| GET/POST | `/invoices` + send + payments | finance / admin (lecture recruteur / employeur) |
| GET/POST | `/contracts` `/contracts/{id}/sign` | mixte |
| GET | `/integrations` `/integrations/status/{name}` | staff |
| GET | `/integrations/linkedin` | public |
| POST | `/integrations/jobs/import` `/integrations/jobs/sync` | staff / admin |
| POST | `/webhooks/stripe` `/webhooks/paypal` `/webhooks/whatsapp` `/webhooks/esignature` | signatures fournisseurs |
| GET | `/notifications` `/notifications/unread` | oui |
| GET | `/admin/bootstrap` `/admin/users` `/admin/audit` `/admin/stats` `/admin/settings` `/emails` | staff / admin |
| POST | `/admin/candidates` | recruteur / admin |
| POST | `/contact` | public |

La documentation interactive liste tous les schémas.

## Notifications et e-mails

Les événements (compte créé, candidature, changement de statut, CV, entretien, message) créent une notification en base. Les templates texte sont dans `app/emails/templates/`. Chaque envoi est d’abord journalisé (`QUEUED`, corps persisté) puis traité par un worker qui relit la file en base lorsque SMTP est activé. Un échec d’envoi n’annule pas la candidature. Redis / Celery restent optionnels plus tard.

Espace candidat public : `/espace.html` (EN : `/en/account.html`) — profil, CV, correspondances, candidatures, entretiens, messages, notifications.

Espace employeur : `/espace-employeur.html` (EN : `/en/account-employer.html`) — entreprise, offres, inbox (dossiers présentés par Talendus, lecture seule), pipeline, factures (Checkout Stripe si configuré). Aucun contact direct employeur–candidat : messagerie, entretiens et changements de statut passent par le staff. Le kanban admin `/admin/` enregistre les déplacements via `POST /api/applications/{id}/status` ; `GET /api/admin/bootstrap` fournit `stageMap` et `pipeline`.

À la publication d’une offre, les candidats actifs au-dessus de `JOB_MATCH_MIN_SCORE` reçoivent une notification `JOB_MATCH` (respect des préférences `notify_match` / `notify_in_app`).

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

Couvrent inscription, connexion, permissions, publication d’offre, candidature, doublon, statut, notifications, matching `JOB_MATCH`, messagerie, entretiens, factures, Checkout Stripe (503 sans clé), parse CV et accès interdit.

## Modules opérationnels

- **Matching** : score déterministe 0–100 (compétences, ville, secteur, expérience, salaire). Pas d’IA générative. Le score est aussi stocké sur la candidature.
- **Messagerie** : fils REST uniquement via Talendus (candidat ↔ conseiller, employeur ↔ conseiller). Pas de fil employeur–candidat, pas de WebSocket.
- **Entretiens** : planifiés par le staff uniquement. L’employeur ne voit que les entretiens client ; le candidat confirme/annule ses rendez-vous avec Talendus. Notification + e-mail.
- **Signature interne** : nom, date, IP, empreinte SHA-256 du mandat. Ce n’est pas DocuSign ni une valeur légale tierce.
- **Facturation** : factures et paiements en base (finance / admin). Checkout Stripe (`POST /api/invoices/{id}/checkout`) si `STRIPE_SECRET_KEY` est défini ; webhook `POST /api/webhooks/stripe` pose `stripe_payment_intent_id` et marque la facture payée. Remboursement `POST /api/invoices/{id}/refund` (finance) + événement `charge.refunded`. PayPal : order / capture / refund si configuré. Sans clé : 503.
- **Job board** : `GET /api/job-board` (JSON). Partage LinkedIn via URL officielle. Publication automatique seulement si `LINKEDIN_CLIENT_ID` / `LINKEDIN_CLIENT_SECRET` sont définis (`posting_enabled`).
- **Stockage CV** : local ou S3 (`STORAGE_BACKEND=s3`). Téléchargement authentifié (URL présignée S3 ou fichier local).
- **Intégrations** : couche `app/integrations/` (un module par fournisseur). Catalogue `GET /api/integrations`. Sans identifiants : 503 `INTEGRATION_NOT_CONFIGURED`, aucun appel simulé. Hooks métier (WhatsApp, Maps) en no-op si le fournisseur n’est pas `active`. Détail : [`INTEGRATIONS.md`](INTEGRATIONS.md).

## Déploiement

La production est définie par `Dockerfile` + `render.yaml` à la racine du dépôt. GitHub Actions (`CI`) lance pytest et construit l’image ; Render ne déploie `main` que si ces contrôles passent (`autoDeployTrigger: checksPass`).

Gardes-fous applicatifs (`APP_ENV=production`) : `DEBUG=false`, secrets ≥ 32 caractères, PostgreSQL obligatoire, seed limité au super-admin (pas d’employeurs / candidats fictifs), `/api/docs` désactivé.

En local, un double de la prod : `docker compose up --build` puis http://localhost:8000.

## Non livré volontairement

Matching LLM automatique, WebSockets, visioconférence Zoom, DocuSign branché, Redis/Celery obligatoire, publication LinkedIn / import Indeed sans accès partenaire officiel.
