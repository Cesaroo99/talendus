# Intégrations API Talendus

Toutes les clés restent **côté serveur** (variables d’environnement). Le navigateur n’appelle jamais LinkedIn, Indeed, Stripe, WhatsApp, OpenAI, etc. directement.

```
Utilisateur → Front Talendus → API Talendus → module integrations/ → API externe
```

## États d’un fournisseur

| État | Signification |
| --- | --- |
| `prepared` | Code prêt, **aucun identifiant**. Aucun appel externe. |
| `configured` | Identifiants présents, mais désactivé **ou** API partenaire pas encore branchée. |
| `active` | Activé **et** identifiants présents **et** implémentation officielle disponible. |

`GET /api/integrations` (staff) renvoie le catalogue **sans secrets**.

## Fournisseurs

| Nom | Catégorie | Réellement connecté ? | Activation |
| --- | --- | --- | --- |
| `email` | messaging | Oui (SMTP si `EMAIL_ENABLED=true`, sinon journal local) | `EMAIL_ENABLED` |
| `s3` | storage | Oui si `STORAGE_BACKEND=s3` + `S3_BUCKET` | `STORAGE_BACKEND` |
| `stripe` | payments | Oui si `STRIPE_SECRET_KEY` | `STRIPE_ENABLED` + clé |
| `paypal` | payments | Appel Orders API **seulement** avec client id/secret + `PAYPAL_ENABLED=true` | sinon 503 |
| `linkedin` | jobs | Partage d’URL : oui. Import d’offres : **non** (partenaire requis, pas de scraping) | `LINKEDIN_*` |
| `indeed` | jobs | **Non** (API partenaire, pas de scraping) | `INDEED_*` |
| `whatsapp` | messaging | Cloud API **seulement** si token + phone id + `WHATSAPP_ENABLED=true` | sinon 503 |
| `google_maps` | maps | Geocoding **seulement** si `GOOGLE_MAPS_API_KEY` + enabled | sinon 503 |
| `openai` | ai | Chat completions **seulement** si clé + enabled, via endpoint staff | jamais auto |
| `esignature` | esignature | Interface seulement (DocuSign à brancher) | 503 / 501 |

## Variables

Voir [`backend/.env.example`](.env.example). Copier vers `.env`. Ne jamais committer de secrets.

Activer un fournisseur :

1. Renseigner les identifiants (portail du fournisseur).
2. Passer `*_ENABLED=true`.
3. Redémarrer l’API.
4. Vérifier `GET /api/integrations/status/{name}` : `state=active`.

Sans identifiants, l’API répond **503** `INTEGRATION_NOT_CONFIGURED` et **n’invente pas** de succès.

## Hooks métier (déjà branchés)

Ces accroches n’appellent un fournisseur **que** s’il est `active`. Sinon : no-op (candidature, entretien, entreprise restent valides).

| Événement | Canal |
| --- | --- |
| Candidature créée | WhatsApp `application_confirm` + `employer_notice` |
| Statut de candidature | WhatsApp `application_status` ou `interview_invite` |
| Entretien créé / reporté | WhatsApp `interview_invite` |
| Entretien confirmé / annulé | WhatsApp `candidate_notice` |
| `POST /api/interviews/reminders` | e-mail + WhatsApp `interview_reminder` (fenêtre 24 h) |
| Création / MAJ entreprise ou offre | géocodage Google Maps → `lat` / `lng` |
| Recherche d’offres `radius_km` | bounding box si coordonnées (géocode `location` si Maps actif) |
| Facture | Stripe refund + webhook `charge.refunded` ; PayPal order/capture/refund |
| `POST /api/candidates/{id}/ai` | OpenAI **explicite** (jamais à l’upload CV) |
| `POST /api/contracts/{id}/esign` | e-sign tierce (503/501) — signature interne SHA-256 inchangée |

## Endpoints internes

Préfixe `/api`. Réponse succès : `{ "success": true, "data": … }`.

| Méthode | Chemin | Auth | Effet |
| --- | --- | --- | --- |
| GET | `/integrations` | staff | Catalogue |
| GET | `/integrations/linkedin` | public | Partage / posting (existant) |
| GET | `/integrations/status/{name}` | staff | Détail d’un fournisseur |
| GET | `/integrations/jobs/external` | staff | Offres importées |
| POST | `/integrations/jobs/import` | staff | Upsert + déduplication |
| POST | `/integrations/jobs/sync` | admin | Fetch fournisseur (501/503 si non branché) |
| POST | `/integrations/whatsapp/send` | staff | Template WhatsApp |
| POST | `/integrations/maps/geocode` | staff | Géocodage |
| POST | `/integrations/maps/distance` | staff | Distance |
| POST | `/integrations/ai/complete` | admin | OpenAI (explicite) |
| POST | `/integrations/esignature/envelopes` | staff | 501/503 |
| POST | `/integrations/paypal/checkout` | staff | Order PayPal |
| POST | `/invoices/{id}/checkout` | employeur | Stripe (existant) |
| POST | `/invoices/{id}/paypal` | employeur | Order PayPal (503 si non actif) |
| POST | `/invoices/{id}/paypal/capture` | employeur | Capture PayPal |
| POST | `/invoices/{id}/refund` | finance | Stripe (défaut) ou PayPal |
| POST | `/interviews/reminders` | staff | Rappels d’entretien |
| POST | `/candidates/{id}/ai` | staff | Analyse IA explicite |
| POST | `/contracts/{id}/esign` | staff | Enveloppe e-sign (501/503) |
| POST | `/webhooks/stripe` | signature Stripe | Paiement + remboursement |
| POST | `/webhooks/paypal` | secret | Idempotent |
| GET/POST | `/webhooks/whatsapp` | verify token / HMAC | Meta |
| POST | `/webhooks/esignature` | HMAC | Signature |

### Exemples

Catalogue (staff) :

```http
GET /api/integrations
Authorization: Bearer <access>
```

```json
{
  "success": true,
  "data": [
    {
      "name": "stripe",
      "state": "prepared",
      "configured": false,
      "enabled": true,
      "implemented": true,
      "env_vars": ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET", "STRIPE_PUBLISHABLE_KEY"]
    }
  ]
}
```

Import d’offres (données déjà obtenues via un canal officiel) :

```http
POST /api/integrations/jobs/import
```

```json
{
  "source": "linkedin",
  "jobs": [
    {
      "external_id": "urn:li:job:123",
      "title": "Soudeur-monteur",
      "company": "Métalco",
      "location": "Drummondville",
      "original_url": "https://www.linkedin.com/jobs/view/123"
    }
  ]
}
```

WhatsApp sans clés → 503 :

```json
{ "success": false, "code": "INTEGRATION_NOT_CONFIGURED", "message": "WhatsApp Business n'est pas configuré (identifiants manquants)." }
```

Géocodage (mock / clé réelle) :

```http
POST /api/integrations/maps/geocode
{ "address": "Montréal, QC" }
```

OpenAI (admin seulement, jamais depuis le front avec la clé) :

```http
POST /api/integrations/ai/complete
{ "purpose": "skill_extraction", "prompt": "CV : cariste WMS Laval…" }
```

## Erreurs

| Code | HTTP | Cas |
| --- | --- | --- |
| `INTEGRATION_NOT_CONFIGURED` | 503 | Pas d’identifiants |
| `INTEGRATION_DISABLED` | 503 | `*_ENABLED=false` alors que des clés existent |
| `INTEGRATION_NOT_IMPLEMENTED` | 501 | API partenaire pas branchée (LinkedIn Jobs, Indeed, e-sign) |
| `INTEGRATION_AUTH` | 502 | 401 fournisseur |
| `INTEGRATION_FORBIDDEN` | 403 | Permission fournisseur / webhook |
| `INTEGRATION_INVALID_REQUEST` | 400 | Payload local invalide |
| `INTEGRATION_NOT_FOUND` | 404 | Ressource absente |
| `INTEGRATION_RATE_LIMITED` | 429 | Quota fournisseur |
| `INTEGRATION_TIMEOUT` | 504 | Timeout |
| `INTEGRATION_UNAVAILABLE` | 503 | 5xx / réseau |
| `INTEGRATION_SIGNATURE_INVALID` | 400 | Webhook rejeté |

Les messages n’incluent jamais de clé, jeton ou corps de carte.

## Ajouter un fournisseur

1. Variables dans `app/config.py` + `.env.example`.
2. Entrée dans `app/integrations/registry.py`.
3. Module `app/integrations/<categorie>/<nom>.py` isolé.
4. `require_active("nom")` avant tout HTTP.
5. Utiliser `app.integrations.http.request` (timeout, retries, logs redactés).
6. Endpoint interne dans `app/api/integrations.py` (jamais de secret au client).
7. Tests avec `httpx.MockTransport` — **sans** vraie API.

## Tests

```bash
cd backend && pytest -q tests/test_integrations.py tests/test_api.py
```

Les tests mockent succès, 503, timeout, 429, payload invalide et fournisseur non configuré.
