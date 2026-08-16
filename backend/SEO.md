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
```

- `TRACKING_ENABLED=false` : aucun script tiers, même si les IDs sont remplis.
- En `APP_ENV=test`, le tracking est toujours coupé.
- Ne jamais coller les IDs dans le HTML.

## Google Analytics 4 (actions manuelles)

1. Créer une propriété GA4 (région Canada si possible).
2. Flux Web → URL `https://talendus.ca` → copier l’ID `G-…`.
3. Mettre `GA_MEASUREMENT_ID` et `TRACKING_ENABLED=true` **après** validation du bandeau cookies en production.
4. Dans Admin GA4 → Événements, marquer comme conversions :
   - `generate_lead` (demande de recrutement / formulaires employeur)
   - `contact`
   - `submit_application` (candidature)
   - `search` (filtre d’offres, après saisie réelle)
   - `view_content` (fiche d’emploi)
5. Explorer → acquisition : organique, direct, social, campagnes (`utm_source`, `utm_medium`, `utm_campaign` déjà lus par GA4).
6. Ne pas ajouter un second extrait gtag (GTM + ce chargeur = double comptage). Si vous passez à GTM plus tard, désactiver `GA_MEASUREMENT_ID` ici.

## Google Search Console (actions manuelles)

1. [search.google.com/search-console](https://search.google.com/search-console) → Ajouter la propriété **Préfixe d’URL** `https://talendus.ca`.
2. Validation : fichier HTML, enregistrement DNS, ou balise meta. La balise meta se place dans `scripts/parts.py` (`head`) **une fois**, puis `python scripts/build_pages.py`.
3. Sitemaps → soumettre `https://talendus.ca/sitemap.xml`.
4. Vérifier que `https://talendus.ca/robots.txt` pointe vers ce sitemap.
5. Inspection d’URL sur l’accueil, `/recrutement-industriel.html`, une offre, un article.
6. Demander l’indexation des pages piliers après mise en ligne.

Le sitemap FastAPI est la source de vérité (pages statiques + articles CMS publiés + offres `PUBLISHED`). Un `sitemap.xml` de secours est aussi généré à la racine pour un hébergement statique.

## Meta Pixel / Meta Business Manager (actions manuelles)

1. Meta Events Manager → créer un Pixel → copier l’ID numérique.
2. `META_PIXEL_ID=…` + consentement marketing accepté.
3. Événements envoyés **après une action réelle** : `PageView`, `Lead`, `Contact`, `SubmitApplication`, `Search`, `ViewContent`.
4. Ne pas recoller le Pixel dans d’autres composants.
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
| Accueil | Marque + industrial QC | recrutement industriel au Québec | agence de recrutement industriel | Premiers candidats qualifiés… | Confier un recrutement |
| Recrutement industriel | Service | recrutement industriel au Québec | agence de placement industriel, personnel industriel | Recrutement industriel au Québec… | Consultation |
| Manufacturier | Service | recrutement manufacturier | recrutement manufacturier Montréal | Recrutement manufacturier… | Mandat |
| Technique | Service | recrutement de talents techniques | travailleurs qualifiés | Recrutement technique… | Métier |
| Permanent / temporaire | Type de contrat | recrutement permanent / temporaire | — | Selon la page | Mandat |
| Chasse de têtes | Senior / passif | chasse de têtes | — | Chasse de têtes… | Mandat |
| Cadres | Leadership | recrutement de cadres | — | Recrutement de cadres d'usine… | Mandat |
| Montréal / Laval / Longueuil / Québec | Local | recrutement industriel + ville | agence locale | Distinct par bassin | Mandat local |
| Emplois | Candidats | offres d'emploi usine | métiers | Postes industriels ouverts | Déposer un CV |
| Blog | Autorité | pénurie, salaires, CV, rétention | un sujet par article | Titre de l’article | Consultation |

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
