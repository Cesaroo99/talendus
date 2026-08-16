# SEO, Search Console et mesure marketing — Talendus

Talendus n’est **pas** une application Next.js. Le site public est du **HTML statique généré** (`scripts/build_pages.py`, `scripts/parts.py`) servi par FastAPI (`StaticFiles`). Le SEO et le tracking sont donc centralisés dans le générateur + quelques routes API, pas via `NEXT_PUBLIC_*`.

## Architecture

```
Visiteur
  → HTML (title, canonical, robots, OG, Twitter, JSON-LD)
  → bandeau cookies (consent.js)
  → si consentement analyse/marketing
       → GET /api/tracking/config  (IDs publics seulement)
       → gtag / Meta Pixel (un seul chargeur : tracking.js)
```

| Couche | Fichier |
| --- | --- |
| Metadata HTML | `scripts/parts.py` (`head`, `wrap`) |
| Pages services / locales | `scripts/seo_pages.py` |
| Sitemap / robots dynamiques | `GET /sitemap.xml`, `GET /robots.txt` (`app/services/seo.py`) |
| Redirections 301 | `SeoRedirectMiddleware` |
| Blog CMS | `blog_posts` + `/api/admin/blog` + `/blog/{slug}` |
| JobPosting | JSON-LD sur `emploi-*.html` / `en/job-*.html` |
| Consentement | `assets/js/consent.js` |
| GA4 + Meta Pixel | `assets/js/tracking.js` (jamais dupliqué dans les pages) |

## Pages indexables vs noindex

**Indexables :** accueil, services, pages de service, pages locales utiles, secteurs, emplois publics, articles, blog, contact, à propos, légal.

**Non indexables :** `/admin/`, `/espace.html`, `/espace-employeur.html`, `/en/account.html`, `/en/account-employer.html`, API, 404, gabarits StaffX (`index1.html`…), redirections legacy.

`robots.txt` les bloque ; les espaces privés ont aussi `<meta name="robots" content="noindex,nofollow">` et l’en-tête `X-Robots-Tag`.

## Variables d’environnement

Copier `backend/.env.example` vers `backend/.env`.

```
TRACKING_ENABLED=false
GA_MEASUREMENT_ID=G-XXXXXXXX
META_PIXEL_ID=1234567890
SEO_CANONICAL_HOST=https://talendus.ca
GOOGLE_SITE_VERIFICATION=
```

- `TRACKING_ENABLED=false` : aucun script tiers, même si les IDs sont remplis.
- En `APP_ENV=test`, le tracking est toujours coupé.
- Ne jamais coller les IDs dans le HTML.

## Google Analytics 4

**Déjà en place dans le code :** Consent Mode v2 (refus par défaut), chargeur unique, événements nommés pour conversions, IP anonymisée, pas de Google Signals.

**Encore manuel (compte Google requis) :**

1. Créer une propriété GA4 (région Canada si possible).
2. Flux Web → URL `https://talendus.ca` → copier l’ID `G-…`.
3. Mettre `GA_MEASUREMENT_ID` et `TRACKING_ENABLED=true` **en production**.
4. Dans Admin GA4 → Événements, marquer comme conversions les noms déjà envoyés :
   - `generate_lead`
   - `contact`
   - `submit_application`
   - `search`
   - `view_content`
5. Ne pas ajouter un second extrait gtag.

`GET /api/tracking/config` liste ces conversions (`data.conversions`).

## Google Search Console

**Déjà en place :** sitemap, robots, canonicals, noindex des espaces privés, fichier de validation.

**Encore manuel (compte Google requis) :**

1. [Search Console](https://search.google.com/search-console) → propriété **Préfixe d’URL** `https://talendus.ca`.
2. Choisir la validation **fichier HTML**. Google affiche un nom du type `googleJETON.html`.
3. Copier le jeton dans `GOOGLE_SITE_VERIFICATION` (sans le préfixe `google` ni `.html`) puis redémarrer l’API.
   - Le fichier devient `https://talendus.ca/googleJETON.html`.
   - Pour la méthode **balise meta**, le même jeton est injecté au `python3 scripts/build_pages.py` si la variable est dans l’environnement.
4. Sitemaps → soumettre `https://talendus.ca/sitemap.xml`.
5. Inspection d’URL sur l’accueil et les pages piliers après mise en ligne HTTPS.

## Meta Pixel / Meta Business Manager

**Déjà en place :** chargeur unique, consentement marketing, `grant`/`revoke`, événements PageView / Lead / Contact / SubmitApplication / Search / ViewContent.

**Encore manuel (compte Meta requis) :**

1. Events Manager → créer un Pixel → `META_PIXEL_ID`.
2. `TRACKING_ENABLED=true` en production.
3. Ne pas recoller le Pixel ailleurs. Les campagnes Ads réutilisent le même ID.
5. Pour les campagnes Ads : utiliser le même Pixel ; les UTM suffisent côté site. Un catalogue d’offres Meta n’est pas branché (à faire plus tard sans toucher au chargeur).

## Blog / ressources (admin)

Rôle **Éditeur** ou **Admin** → `#/content` → onglet Blog :

- créer / modifier
- brouillon, publié, programmé (`scheduled_at`), archivé
- image, catégorie, tags, auteur, slug, title SEO, meta description
- JSON-LD `Article` sur `/blog/{slug}`

Les articles HTML historiques `article-*.html` restent en ligne. Les nouveaux contenus CMS passent par `/blog/{slug}`.

## Stratégie mots-clés (intention, pas de bourrage)

| Page | Intention | Mot-clé principal | Secondaires | H1 | CTA |
| --- | --- | --- | --- | --- | --- |
| Accueil | Marque + tous secteurs | plateforme de recrutement | recrutement entreprises, tous secteurs | Recrutez mieux, plus vite et plus intelligemment. | Parler à un recruteur |
| Recrutement industriel | Exemple de secteur | recrutement industriel au Québec | agence de placement, personnel industriel | Recrutement industriel : un exemple parmi d'autres | Parler à un recruteur |
| Manufacturier | Exemple de secteur | recrutement manufacturier | recrutement manufacturier Montréal | Recrutement manufacturier… | Mandat |
| Technique | Service | recrutement de talents techniques | travailleurs qualifiés | Recrutement technique… | Métier |
| Permanent / temporaire | Type de contrat | recrutement permanent / temporaire | — | Selon la page | Mandat |
| Chasse de têtes | Senior / passif | chasse de têtes | — | Chasse de têtes… | Mandat |
| Cadres | Leadership | recrutement de cadres | — | Recrutement de cadres… | Mandat |
| Montréal / Laval / Longueuil / Québec | Local | recrutement + ville | agence locale | Distinct par bassin | Mandat local |
| Emplois | Candidats | offres d'emploi | métiers, compétences | Découvrez les offres | Créer mon profil |
| Blog | Autorité | recrutement, RH, rétention | un sujet par article | Titre de l’article | Parler à un recruteur |

Maillage : Accueil → Services → page service → articles / offres → candidature ; Accueil → Entreprises → contact.

## Performance

- Scripts thème en `defer` (jQuery reste synchrone, requis par le thème).
- Images sous la ligne de flottaison : `loading="lazy"`.
- Hero principal : `fetchpriority="high"`.
- Tracking tiers **après consentement** seulement.
- Ne pas retirer le préchargeur ni le design : le LCP du hero reste l’image d’usine.

## Régénérer le HTML

```
python3 scripts/build_pages.py
```
