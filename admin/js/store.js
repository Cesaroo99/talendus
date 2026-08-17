/* Talendus Admin — store démo (localStorage), prêt pour un vrai backend */
(function (global) {
  const KEY = "talendus-admin-v1";
  const SESSION = "talendus-admin-session";

  const users = [
    { id: "u-sophie", firstName: "Sophie", lastName: "Tremblay", email: "sophie.admin@talendus.ca", password: "talendus", role: "admin", title: "Directrice générale", initials: "ST" },
    { id: "u-marc", firstName: "Marc", lastName: "Gagnon", email: "marc.recruiter@talendus.ca", password: "talendus", role: "recruiter", title: "Recruteur senior", initials: "MG" },
    { id: "u-camille", firstName: "Camille", lastName: "Bouchard", email: "camille.recruiter@talendus.ca", password: "talendus", role: "recruiter", title: "Recruteuse industrielle", initials: "CB" },
    { id: "u-nathalie", firstName: "Nathalie", lastName: "Roy", email: "nathalie.finance@talendus.ca", password: "talendus", role: "finance", title: "Contrôleure financière", initials: "NR" },
    { id: "u-alex", firstName: "Alexandre", lastName: "Fortin", email: "alex.editeur@talendus.ca", password: "talendus", role: "editor", title: "Éditeur de contenu", initials: "AF" }
  ];

  const PERMS = {
    admin: ["dashboard", "candidates", "clients", "jobs", "missions", "content", "finance", "analytics", "notifications", "settings", "profile"],
    recruiter: ["dashboard", "candidates", "clients", "jobs", "missions", "notifications", "settings", "profile"],
    finance: ["dashboard", "finance", "analytics", "notifications", "settings", "profile"],
    editor: ["content", "notifications", "settings", "profile"]
  };

  function d(iso) { return iso; }

  const SEED = {
    users,
    candidates: [
      { id: "c-01", firstName: "Karine", lastName: "Lavoie", email: "karine.lavoie@email.ca", phone: "514 555-0142", city: "Laval", title: "Cariste", sector: "Entrepôt", experience: 6, level: "Intermédiaire", availability: "2 semaines", status: "qualifie", languages: ["Français", "Anglais"], recruiterId: "u-marc", createdAt: "2026-07-12", lastActivity: "2026-08-14", skills: ["Chariot élévateur classe I-IV", "WMS", "SST", "Préparation de commandes"], salaryMin: 22, salaryMax: 26, shift: "Jour", education: [{ school: "Formation interne LogiCentre", diploma: "Permis chariot", year: "2020" }], experiences: [{ company: "LogiCentre Laval", role: "Cariste", years: "2021 — 2026" }], bio: "Cariste expérimentée, quarts de jour, à l’aise WMS et cadence entrepôt.", jobId: "j-01", clientId: "cl-02" },
      { id: "c-02", firstName: "Hugo", lastName: "Bélanger", email: "hugo.belanger@email.ca", phone: "450 555-0188", city: "Longueuil", title: "Opérateur de production", sector: "Production", experience: 4, level: "Intermédiaire", availability: "Immédiat", status: "entretien", languages: ["Français"], recruiterId: "u-camille", createdAt: "2026-07-28", lastActivity: "2026-08-15", skills: ["Ligne d’assemblage", "Contrôle qualité", "5S"], salaryMin: 20, salaryMax: 24, shift: "Rotatif", education: [{ school: "DEP Production", diploma: "DEP", year: "2019" }], experiences: [{ company: "Alimor", role: "Préposé ligne", years: "2022 — 2026" }], bio: "Opérateur fiable, habitué aux quarts rotatifs en agroalimentaire.", jobId: "j-02", clientId: "cl-03" },
      { id: "c-03", firstName: "Nadia", lastName: "Côté", email: "nadia.cote@email.ca", phone: "819 555-0110", city: "Drummondville", title: "Soudeuse-monteuse", sector: "Métallurgie", experience: 8, level: "Senior", availability: "1 mois", status: "presente", languages: ["Français"], recruiterId: "u-marc", createdAt: "2026-06-04", lastActivity: "2026-08-13", skills: ["MIG", "TIG", "Lecture de plans", "Cartes de compétences"], salaryMin: 28, salaryMax: 34, shift: "Jour", education: [{ school: "CFP Drummond", diploma: "DEP Soudage", year: "2016" }], experiences: [{ company: "Métalco", role: "Soudeuse", years: "2018 — 2025" }], bio: "Soudeuse MIG/TIG, lecture de plans, prête pour un deuxième quart structuré.", jobId: "j-03", clientId: "cl-01" },
      { id: "c-04", firstName: "Éric", lastName: "Nguyen", email: "eric.nguyen@email.ca", phone: "450 555-0194", city: "Saint-Jérôme", title: "Machiniste CNC", sector: "Manufacturier", experience: 11, level: "Senior", availability: "3 semaines", status: "entretien-client", languages: ["Français", "Anglais"], recruiterId: "u-camille", createdAt: "2026-05-22", lastActivity: "2026-08-12", skills: ["Set-up", "Programmation", "Fanuc", "Tolérances serrées"], salaryMin: 30, salaryMax: 38, shift: "Jour", education: [{ school: "Cégep Saint-Jérôme", diploma: "Techniques de génie mécanique", year: "2013" }], experiences: [{ company: "Plastika", role: "Machiniste", years: "2015 — 2026" }], bio: "Machiniste CNC rare, set-up autonome, profil passif approché discrètement.", jobId: "j-04", clientId: "cl-04" },
      { id: "c-05", firstName: "Samuel", lastName: "Diallo", email: "samuel.diallo@email.ca", phone: "514 555-0166", city: "Montréal", title: "Électromécanicien", sector: "Maintenance", experience: 9, level: "Senior", availability: "2 semaines", status: "offre", languages: ["Français", "Anglais"], recruiterId: "u-marc", createdAt: "2026-04-18", lastActivity: "2026-08-15", skills: ["Hydraulique", "Pneumatique", "Dépannage 24/7", "Cadenassage"], salaryMin: 32, salaryMax: 40, shift: "Rotatif", education: [{ school: "École des métiers", diploma: "DEP Électromécanique", year: "2014" }], experiences: [{ company: "Usine Nordique", role: "Électromécanicien", years: "2017 — 2026" }], bio: "Dépannage de ligne, hydraulique et pneumatique, quarts rotatifs.", jobId: "j-05", clientId: "cl-06" },
      { id: "c-06", firstName: "Mélanie", lastName: "Gagné", email: "melanie.gagne@email.ca", phone: "819 555-0177", city: "Sherbrooke", title: "Mécanicienne industrielle", sector: "Maintenance", experience: 7, level: "Intermédiaire", availability: "Immédiat", status: "a-contacter", languages: ["Français"], recruiterId: "u-camille", createdAt: "2026-08-02", lastActivity: "2026-08-10", skills: ["Préventif", "Alignement", "Convoyeurs"], salaryMin: 30, salaryMax: 36, shift: "Jour", education: [{ school: "CFP Sherbrooke", diploma: "DEP Mécanique industrielle", year: "2018" }], experiences: [{ company: "Forge Mauricie", role: "Mécanicienne", years: "2019 — 2025" }], bio: "Maintenance préventive, fiabilité convoyeurs.", jobId: "j-06", clientId: "cl-07" },
      { id: "c-07", firstName: "Jordan", lastName: "Pelletier", email: "jordan.pelletier@email.ca", phone: "450 555-0121", city: "Boucherville", title: "Journalier d’usine", sector: "Production", experience: 2, level: "Junior", availability: "Immédiat", status: "nouveau", languages: ["Français"], recruiterId: "u-marc", createdAt: "2026-08-11", lastActivity: "2026-08-11", skills: ["Manutention", "Ponctualité", "Travail d’équipe"], salaryMin: 18, salaryMax: 21, shift: "Soir", education: [{ school: "Formation interne", diploma: "SST", year: "2025" }], experiences: [{ company: "Distro Plus", role: "Journalier", years: "2024 — 2026" }], bio: "Disponible quart de soir, bonne condition physique.", jobId: "j-07", clientId: "cl-08" },
      { id: "c-08", firstName: "Isabelle", lastName: "Morin", email: "isabelle.morin@email.ca", phone: "819 555-0133", city: "Trois-Rivières", title: "Superviseure de production", sector: "Supervision", experience: 12, level: "Senior", availability: "1 mois", status: "place", languages: ["Français", "Anglais"], recruiterId: "u-camille", createdAt: "2026-03-09", lastActivity: "2026-08-01", skills: ["KPI", "Lean", "Leadership de quart", "SST"], salaryMin: 70000, salaryMax: 85000, shift: "Jour", education: [{ school: "UQTR", diploma: "Certificat gestion", year: "2018" }], experiences: [{ company: "Alimor", role: "Contremaître", years: "2016 — 2026" }], bio: "Superviseure Lean, stabilise le quart et le climat.", jobId: "j-08", clientId: "cl-03" },
      { id: "c-09", firstName: "Antoine", lastName: "Ross", email: "antoine.ross@email.ca", phone: "514 555-0190", city: "Anjou", title: "Coordonnateur logistique", sector: "Logistique", experience: 5, level: "Intermédiaire", availability: "3 semaines", status: "qualifie", languages: ["Français", "Anglais"], recruiterId: "u-marc", createdAt: "2026-06-21", lastActivity: "2026-08-09", skills: ["WMS", "Planification", "Transport interne"], salaryMin: 55000, salaryMax: 68000, shift: "Jour", education: [{ school: "Cégep Marie-Victorin", diploma: "Logistique", year: "2019" }], experiences: [{ company: "TransQuébec", role: "Commis expédition", years: "2020 — 2026" }], bio: "Coordonnateur WMS, anglais opérationnel.", jobId: "j-09", clientId: "cl-05" },
      { id: "c-10", firstName: "Patricia", lastName: "Hamel", email: "patricia.hamel@email.ca", phone: "418 555-0144", city: "Québec", title: "Directrice d’usine", sector: "Cadres", experience: 16, level: "Cadre", availability: "2 mois", status: "presente", languages: ["Français", "Anglais"], recruiterId: "u-sophie", createdAt: "2026-02-14", lastActivity: "2026-08-08", skills: ["P&L", "Lean", "Gestion 100+ employés"], salaryMin: 120000, salaryMax: 150000, shift: "Jour", education: [{ school: "Université Laval", diploma: "MBA", year: "2012" }], experiences: [{ company: "Usine Nordique", role: "Directrice production", years: "2018 — 2026" }], bio: "Mandat confidentiel, chasse de têtes discrète.", jobId: "j-10", clientId: "cl-06" },
      { id: "c-11", firstName: "Yassine", lastName: "Benali", email: "yassine.benali@email.ca", phone: "514 555-0108", city: "Montréal", title: "Électromécanicien", sector: "Maintenance", experience: 3, level: "Junior", availability: "Immédiat", status: "refuse", languages: ["Français", "Arabe"], recruiterId: "u-marc", createdAt: "2026-07-01", lastActivity: "2026-07-22", skills: ["Électricité industrielle", "Dépannage"], salaryMin: 28, salaryMax: 32, shift: "Rotatif", education: [{ school: "Équivalence", diploma: "Technicien", year: "2022" }], experiences: [{ company: "PME Rive-Nord", role: "Aide-mécanicien", years: "2023 — 2026" }], bio: "Profil prometteur, écart de quart avec le client.", jobId: "j-05", clientId: "cl-06" },
      { id: "c-12", firstName: "Chloé", lastName: "Savard", email: "chloe.savard@email.ca", phone: "450 555-0155", city: "Laval", title: "Cariste", sector: "Entrepôt", experience: 1, level: "Junior", availability: "Immédiat", status: "inactif", languages: ["Français"], recruiterId: "u-camille", createdAt: "2026-01-20", lastActivity: "2026-04-02", skills: ["Chariot élévateur"], salaryMin: 20, salaryMax: 23, shift: "Soir", education: [], experiences: [], bio: "Plus joignable depuis avril.", jobId: "j-01", clientId: "cl-02" }
    ],
    clients: [
      { id: "cl-01", name: "Métalco", sector: "Métallurgie", city: "Drummondville", contact: "Jean Rivest", email: "j.rivest@metalco.ca", phone: "819 555-2001", status: "Actif", recruiterId: "u-marc", employees: 180, website: "metalco.example", since: "2023-04-01" },
      { id: "cl-02", name: "LogiCentre Laval", sector: "Entrepôt", city: "Laval", contact: "Amélie Fortin", email: "a.fortin@logicentre.ca", phone: "450 555-2002", status: "Actif", recruiterId: "u-marc", employees: 95, website: "logicentre.example", since: "2024-01-15" },
      { id: "cl-03", name: "Alimor", sector: "Transformation alimentaire", city: "Longueuil", contact: "Maude Lavoie", email: "m.lavoie@alimor.ca", phone: "450 555-2003", status: "Actif", recruiterId: "u-camille", employees: 240, website: "alimor.example", since: "2022-09-08" },
      { id: "cl-04", name: "Plastika", sector: "Plasturgie", city: "Saint-Jérôme", contact: "Benoit Gauthier", email: "b.gauthier@plastika.ca", phone: "450 555-2004", status: "Actif", recruiterId: "u-camille", employees: 70, website: "plastika.example", since: "2025-02-11" },
      { id: "cl-05", name: "TransQuébec", sector: "Transport", city: "Anjou", contact: "David Chen", email: "d.chen@transquebec.ca", phone: "514 555-2005", status: "Actif", recruiterId: "u-marc", employees: 130, website: "transquebec.example", since: "2024-06-20" },
      { id: "cl-06", name: "Usine Nordique", sector: "Manufacturier", city: "Québec", contact: "Sylvie Paquet", email: "s.paquet@nordique.ca", phone: "418 555-2006", status: "Actif", recruiterId: "u-sophie", employees: 310, website: "nordique.example", since: "2021-11-02" },
      { id: "cl-07", name: "Forge Mauricie", sector: "Métallurgie", city: "Trois-Rivières", contact: "Luc Tremblay", email: "l.tremblay@forgemauricie.ca", phone: "819 555-2007", status: "Prospect", recruiterId: "u-camille", employees: 55, website: "forge.example", since: "2026-07-01" },
      { id: "cl-08", name: "Distro Plus", sector: "Distribution", city: "Boucherville", contact: "Cathy Nguyen", email: "c.nguyen@distroplus.ca", phone: "450 555-2008", status: "Actif", recruiterId: "u-marc", employees: 88, website: "distroplus.example", since: "2025-08-18" }
    ],
    contracts: [
      { id: "ct-01", clientId: "cl-01", type: "Retainer + succès", start: "2026-01-01", end: "2026-12-31", commission: 18, terms: "18 % du salaire annuel, garantie 90 jours.", status: "Actif", document: "contrat-metalco-2026.pdf" },
      { id: "ct-02", clientId: "cl-02", type: "Succès", start: "2026-03-01", end: "2027-02-28", commission: 16, terms: "16 % au succès, remplacement 60 jours.", status: "Actif", document: "contrat-logicentre.pdf" },
      { id: "ct-03", clientId: "cl-03", type: "Entente-cadre", start: "2025-09-01", end: "2026-08-31", commission: 17, terms: "Volume 8+ mandats / an, 17 %.", status: "Expire bientôt", document: "entente-alimor.pdf" },
      { id: "ct-04", clientId: "cl-06", type: "Chasse de têtes", start: "2026-02-01", end: "2026-12-31", commission: 22, terms: "Cadres : 22 %, confidentiel.", status: "Actif", document: "chasse-nordique.pdf" }
    ],
    jobs: [
      { id: "j-01", title: "Cariste", clientId: "cl-02", city: "Laval", sector: "Entrepôt", type: "Permanent", salary: "22 à 26 $/h", shift: "Quart de jour", status: "publiee", publishedAt: "2026-07-20", expiresAt: "2026-09-20", applications: 14, experience: "1 an", skills: "Permis chariot, WMS", benefits: "Assurances, stationnement", description: "Manutention et préparation de commandes dans un centre de distribution.", responsibilities: "Conduire le chariot, charger/décharger, respecter la SST.", qualifications: "Permis valide, 1 an d’expérience." },
      { id: "j-02", title: "Opérateur de production", clientId: "cl-03", city: "Longueuil", sector: "Production", type: "Permanent", salary: "20 à 24 $/h", shift: "Quarts rotatifs", status: "publiee", publishedAt: "2026-07-22", expiresAt: "2026-09-22", applications: 11, experience: "Expérience d’usine", skills: "Procédures, équipe", benefits: "Prime de quart", description: "Opération de ligne en transformation alimentaire.", responsibilities: "Suivre le standard, qualité, hygiène.", qualifications: "Expérience usine, ponctualité." },
      { id: "j-03", title: "Soudeur-monteur", clientId: "cl-01", city: "Drummondville", sector: "Métallurgie", type: "Permanent", salary: "28 à 34 $/h", shift: "Quart de jour", status: "publiee", publishedAt: "2026-06-10", expiresAt: "2026-09-10", applications: 7, experience: "3 ans", skills: "MIG/TIG, plans", benefits: "REER, outils", description: "Soudure et montage pour un deuxième quart.", responsibilities: "Souder selon plans, contrôle visuel.", qualifications: "DEP soudage, cartes un atout." },
      { id: "j-04", title: "Machiniste CNC", clientId: "cl-04", city: "Saint-Jérôme", sector: "Manufacturier", type: "Permanent", salary: "30 à 38 $/h", shift: "Quart de jour", status: "publiee", publishedAt: "2026-05-28", expiresAt: "2026-09-28", applications: 4, experience: "3 ans", skills: "Set-up, dessins", benefits: "Horaire jour", description: "Usinage de précision, set-up autonome.", responsibilities: "Programmer ou set-up, qualité.", qualifications: "3 ans CNC." },
      { id: "j-05", title: "Électromécanicien", clientId: "cl-06", city: "Montréal", sector: "Maintenance", type: "Permanent", salary: "32 à 40 $/h", shift: "Quarts rotatifs", status: "publiee", publishedAt: "2026-04-12", expiresAt: "2026-10-12", applications: 9, experience: "5 ans", skills: "Hydraulique, électricité", benefits: "Prime de disponibilité", description: "Dépannage de ligne et fiabilité.", responsibilities: "Diagnostiquer, réparer, préventif.", qualifications: "DEP électromécanique." },
      { id: "j-06", title: "Mécanicien industriel", clientId: "cl-07", city: "Sherbrooke", sector: "Maintenance", type: "Permanent", salary: "30 à 36 $/h", shift: "Quart de jour", status: "brouillon", publishedAt: "", expiresAt: "2026-10-01", applications: 0, experience: "3 ans", skills: "Préventif, convoyeurs", benefits: "À confirmer", description: "Entretien préventif.", responsibilities: "Alignement, pièces d’usure.", qualifications: "DEP mécanique industrielle." },
      { id: "j-07", title: "Journalier d’usine", clientId: "cl-08", city: "Boucherville", sector: "Production", type: "Permanent", salary: "18 à 21 $/h", shift: "Quart de soir", status: "publiee", publishedAt: "2026-08-01", expiresAt: "2026-09-15", applications: 22, experience: "Aucune", skills: "Manutention", benefits: "Formation interne", description: "Renfort de quart de soir.", responsibilities: "Alimenter la ligne, emballage.", qualifications: "Bonne condition physique." },
      { id: "j-08", title: "Superviseur de production", clientId: "cl-03", city: "Trois-Rivières", sector: "Supervision", type: "Permanent", salary: "70 000 à 85 000 $", shift: "Quart de jour", status: "archivee", publishedAt: "2026-03-01", expiresAt: "2026-06-01", applications: 6, experience: "5 ans", skills: "Lean, KPI", benefits: "Bonus", description: "Supervision d’équipe de quart.", responsibilities: "KPI, SST, climat.", qualifications: "5 ans en usine." },
      { id: "j-09", title: "Coordonnateur logistique", clientId: "cl-05", city: "Anjou", sector: "Logistique", type: "Permanent", salary: "55 000 à 68 000 $", shift: "Quart de jour", status: "publiee", publishedAt: "2026-06-18", expiresAt: "2026-09-18", applications: 8, experience: "3 ans", skills: "WMS, anglais", benefits: "Télétravail partiel rare", description: "Planification des flux.", responsibilities: "WMS, transport interne.", qualifications: "Anglais un atout." },
      { id: "j-10", title: "Directeur d’usine", clientId: "cl-06", city: "Québec", sector: "Cadres", type: "Permanent", salary: "120 000 à 150 000 $", shift: "Quart de jour", status: "suspendue", publishedAt: "2026-02-20", expiresAt: "2026-08-20", applications: 3, experience: "10 ans", skills: "P&L, Lean", benefits: "Auto, bonus", description: "Mandat confidentiel.", responsibilities: "P&L, 100+ employés.", qualifications: "Expérience plant manager." }
    ],
    missions: [
      { id: "m-01", clientId: "cl-02", jobId: "j-01", title: "Caristes — pic saisonnier", seats: 8, recruiterId: "u-marc", start: "2026-07-15", due: "2026-09-01", status: "en-cours", value: 72000, commission: 11520, progress: 62, stageMap: { "c-01": "presentation", "c-12": "nouveaux" } },
      { id: "m-02", clientId: "cl-03", jobId: "j-02", title: "Opérateurs ligne 2", seats: 4, recruiterId: "u-camille", start: "2026-07-20", due: "2026-08-30", status: "en-cours", value: 48000, commission: 8160, progress: 45, stageMap: { "c-02": "entretien-talendus" } },
      { id: "m-03", clientId: "cl-01", jobId: "j-03", title: "Soudeurs deuxième quart", seats: 3, recruiterId: "u-marc", start: "2026-06-01", due: "2026-08-20", status: "en-cours", value: 96000, commission: 17280, progress: 70, stageMap: { "c-03": "entretien-client" } },
      { id: "m-04", clientId: "cl-04", jobId: "j-04", title: "Machiniste CNC", seats: 1, recruiterId: "u-camille", start: "2026-05-20", due: "2026-09-01", status: "en-cours", value: 68000, commission: 12240, progress: 80, stageMap: { "c-04": "entretien-client" } },
      { id: "m-05", clientId: "cl-06", jobId: "j-05", title: "Électromécanicien fiabilité", seats: 2, recruiterId: "u-marc", start: "2026-04-10", due: "2026-08-25", status: "en-cours", value: 110000, commission: 24200, progress: 88, stageMap: { "c-05": "offre", "c-11": "nouveaux" } },
      { id: "m-06", clientId: "cl-03", jobId: "j-08", title: "Superviseur de production", seats: 1, recruiterId: "u-camille", start: "2026-03-01", due: "2026-06-15", status: "pourvue", value: 78000, commission: 13260, progress: 100, stageMap: { "c-08": "placement" } },
      { id: "m-07", clientId: "cl-06", jobId: "j-10", title: "Directeur d’usine confidentiel", seats: 1, recruiterId: "u-sophie", start: "2026-02-10", due: "2026-09-15", status: "en-cours", value: 140000, commission: 30800, progress: 55, stageMap: { "c-10": "presentation" } },
      { id: "m-08", clientId: "cl-08", jobId: "j-07", title: "Journaliers quart de soir", seats: 6, recruiterId: "u-marc", start: "2026-08-01", due: "2026-08-28", status: "en-cours", value: 36000, commission: 5760, progress: 30, stageMap: { "c-07": "preselection" } }
    ],
    invoices: [
      { id: "F-2026-014", clientId: "cl-03", missionId: "m-06", amount: 13260, date: "2026-07-02", due: "2026-08-01", status: "payee" },
      { id: "F-2026-018", clientId: "cl-02", missionId: "m-01", amount: 8640, date: "2026-07-28", due: "2026-08-27", status: "en-attente" },
      { id: "F-2026-019", clientId: "cl-01", missionId: "m-03", amount: 5760, date: "2026-07-15", due: "2026-08-10", status: "en-retard" },
      { id: "F-2026-021", clientId: "cl-06", missionId: "m-05", amount: 12100, date: "2026-08-04", due: "2026-09-03", status: "envoyee" },
      { id: "F-2026-022", clientId: "cl-04", missionId: "m-04", amount: 0, date: "2026-08-12", due: "2026-09-12", status: "brouillon" },
      { id: "F-2026-011", clientId: "cl-05", missionId: "m-01", amount: 4200, date: "2026-05-12", due: "2026-06-11", status: "annulee" },
      { id: "F-2026-008", clientId: "cl-06", missionId: "m-07", amount: 15400, date: "2026-04-20", due: "2026-05-20", status: "payee" },
      { id: "F-2026-023", clientId: "cl-08", missionId: "m-08", amount: 2880, date: "2026-08-10", due: "2026-09-09", status: "en-attente" }
    ],
    payments: [
      { id: "p-01", invoiceId: "F-2026-014", amount: 13260, date: "2026-07-28", method: "Virement" },
      { id: "p-02", invoiceId: "F-2026-008", amount: 15400, date: "2026-05-18", method: "Virement" }
    ],
    pages: [
      { id: "pg-home", title: "Accueil", slug: "/", status: "publie", updatedAt: "2026-08-16", authorId: "u-alex" },
      { id: "pg-employers", title: "Entreprises", slug: "/entreprises.html", status: "publie", updatedAt: "2026-08-16", authorId: "u-alex" },
      { id: "pg-jobs", title: "Offres d’emploi", slug: "/emplois.html", status: "publie", updatedAt: "2026-08-16", authorId: "u-alex" },
      { id: "pg-contact", title: "Contact", slug: "/contact.html", status: "publie", updatedAt: "2026-08-16", authorId: "u-alex" },
      { id: "pg-about", title: "À propos", slug: "/a-propos.html", status: "publie", updatedAt: "2026-08-10", authorId: "u-alex" }
    ],
    posts: [
      { id: "po-01", title: "Combien coûte une mauvaise embauche en usine ?", status: "publie", updatedAt: "2026-07-08", authorId: "u-alex", seo: "recrutement industriel Québec" },
      { id: "po-02", title: "Recruter un machiniste CNC au Québec en 2026", status: "publie", updatedAt: "2026-07-18", authorId: "u-alex", seo: "recrutement manufacturier Québec" },
      { id: "po-03", title: "Pénurie de caristes : stratégies pour les entrepôts", status: "brouillon", updatedAt: "2026-08-12", authorId: "u-alex", seo: "recrutement cariste" }
    ],
    testimonials: [
      { id: "t-01", author: "M.L.", role: "Directrice des opérations · Alimor", quote: "Ils ont compris nos quarts rotatifs dès le premier appel.", status: "publie" },
      { id: "t-02", author: "J.R.", role: "Directeur maintenance · Métalco", quote: "Trois dossiers solides, un électromécanicien en poste.", status: "publie" },
      { id: "t-03", author: "A.D.", role: "Candidate placée · Laval", quote: "Entrevue claire, conditions nettes.", status: "archive" }
    ],
    faqs: [
      { id: "f-01", q: "Talendus est-il une agence généraliste ?", a: "Non. Partenaire des entreprises opérationnelles du Québec.", status: "publie" },
      { id: "f-02", q: "À partir de quand les premiers candidats ?", a: "Shortlist qualifiée à partir de 7 jours sur les métiers d’opération.", status: "publie" },
      { id: "f-03", q: "Comment se passe une consultation ?", a: "Sur rendez-vous uniquement. Réponse moyenne sous 30 minutes.", status: "publie" }
    ],
    notes: [
      { id: "n-01", entity: "candidate", entityId: "c-04", authorId: "u-camille", text: "Profil passif. Ne pas appeler sur le quart — SMS après 16 h.", at: "2026-08-12 09:14" },
      { id: "n-02", entity: "candidate", entityId: "c-05", authorId: "u-marc", text: "Offre verbale 36 $/h + prime. Relance écrite demain.", at: "2026-08-15 11:02" },
      { id: "n-03", entity: "client", entityId: "cl-01", authorId: "u-marc", text: "Contremaître exige test de soudure sur place.", at: "2026-08-13 16:40" }
    ],
    interviews: [
      { id: "i-01", candidateId: "c-02", clientId: "cl-03", type: "Talendus", at: "2026-08-18 09:30", location: "Visio", recruiterId: "u-camille" },
      { id: "i-02", candidateId: "c-04", clientId: "cl-04", type: "Client", at: "2026-08-19 14:00", location: "Saint-Jérôme", recruiterId: "u-camille" },
      { id: "i-03", candidateId: "c-05", clientId: "cl-06", type: "Offre", at: "2026-08-17 10:00", location: "Téléphone", recruiterId: "u-marc" }
    ],
    documents: [
      { id: "d-01", name: "CV_Karine_Lavoie.pdf", entity: "candidate", entityId: "c-01", size: "214 Ko" },
      { id: "d-02", name: "Cartes_competences_Cote.pdf", entity: "candidate", entityId: "c-03", size: "1,1 Mo" },
      { id: "d-03", name: "contrat-metalco-2026.pdf", entity: "client", entityId: "cl-01", size: "420 Ko" }
    ],
    notifications: [
      { id: "nt-01", type: "candidature", text: "Nouvelle candidature : Jordan Pelletier — journalier d’usine", at: "2026-08-16 08:12", read: false, href: "#/candidates/c-07" },
      { id: "nt-02", type: "entretien", text: "Entretien client Éric Nguyen demain 14 h (Plastika)", at: "2026-08-15 17:40", read: false, href: "#/candidates/c-04" },
      { id: "nt-03", type: "facture", text: "Facture F-2026-019 en retard — Métalco 5 760 $", at: "2026-08-15 09:00", read: false, href: "#/finance" },
      { id: "nt-04", type: "mission", text: "Mission soudeurs Métalco proche de l’échéance (20 août)", at: "2026-08-14 12:22", read: true, href: "#/missions/m-03" },
      { id: "nt-05", type: "client", text: "Nouveau prospect : Forge Mauricie", at: "2026-08-01 10:05", read: true, href: "#/clients/cl-07" },
      { id: "nt-06", type: "placement", text: "Placement confirmé : Isabelle Morin — Alimor", at: "2026-08-01 16:18", read: true, href: "#/candidates/c-08" }
    ],
    activities: [
      { id: "a-01", text: "Nouveau candidat inscrit — Jordan Pelletier", at: "2026-08-11 09:20" },
      { id: "a-02", text: "Nouvelle candidature — journalier Distro Plus", at: "2026-08-11 09:22" },
      { id: "a-03", text: "Nouveau client — Forge Mauricie (prospect)", at: "2026-07-01 14:00" },
      { id: "a-04", text: "Offre publiée — Journalier d’usine, Boucherville", at: "2026-08-01 08:40" },
      { id: "a-05", text: "Entretien planifié — Hugo Bélanger × Alimor", at: "2026-08-15 11:30" },
      { id: "a-06", text: "Placement effectué — Isabelle Morin, superviseure", at: "2026-08-01 16:18" },
      { id: "a-07", text: "Facture payée — F-2026-014 Alimor 13 260 $", at: "2026-07-28 10:02" },
      { id: "a-08", text: "Samuel Diallo : offre verbale 36 $/h", at: "2026-08-15 11:02" }
    ],
    monthly: {
      applications: [18, 22, 19, 28, 31, 26, 34, 29],
      placements: [1, 2, 1, 3, 2, 2, 4, 2],
      revenue: [18000, 24000, 15400, 28600, 22100, 19800, 31200, 8640],
      months: ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû"]
    }
  };

  let state = null;
  const listeners = [];

  function clone(v) {
    return JSON.parse(JSON.stringify(v));
  }

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state = Object.assign(clone(SEED), parsed);
        return;
      }
    } catch (e) {}
    state = clone(SEED);
  }

  function persist() {
    localStorage.setItem(KEY, JSON.stringify(state));
    listeners.forEach(function (fn) { fn(state); });
  }

  load();

  global.TLStore = {
    PERMS: PERMS,
    get: function () { return state; },
    user: function (id) { return state.users.find(function (u) { return u.id === id; }); },
    client: function (id) { return state.clients.find(function (c) { return c.id === id; }); },
    candidate: function (id) { return state.candidates.find(function (c) { return c.id === id; }); },
    job: function (id) { return state.jobs.find(function (j) { return j.id === id; }); },
    mission: function (id) { return state.missions.find(function (m) { return m.id === id; }); },
    name: function (userId) {
      var u = this.user(userId);
      return u ? u.firstName + " " + u.lastName : "—";
    },
    update: function (mutator) {
      mutator(state);
      persist();
    },
    reset: function () {
      state = clone(SEED);
      persist();
    },
    hydrateFromApi: async function () {
      if (!window.TalendusAPI || !window.TalendusAPI.bootstrap) return false;
      try {
        var json = await window.TalendusAPI.bootstrap();
        var d = json && json.data;
        if (!d) return false;
        ["candidates", "clients", "jobs", "missions", "contracts", "notes", "notifications", "activities", "interviews", "invoices", "payments", "jobMatches"].forEach(function (key) {
          if (Array.isArray(d[key])) state[key] = d[key];
        });
        if (Array.isArray(d.users) && d.users.length) {
          var mapped = d.users.filter(function (u) { return ["admin", "recruiter", "finance", "editor"].indexOf(u.role) !== -1; });
          if (mapped.length) {
            var byEmail = {};
            state.users.forEach(function (u) { byEmail[u.email] = u; });
            mapped.forEach(function (u) {
              if (byEmail[u.email]) {
                byEmail[u.email].id = u.id;
                byEmail[u.email].firstName = u.firstName;
                byEmail[u.email].lastName = u.lastName;
                byEmail[u.email].title = u.title;
              } else {
                state.users.push(u);
              }
            });
          }
        }
        persist();
        return true;
      } catch (e) {
        return false;
      }
    },
    subscribe: function (fn) { listeners.push(fn); },
    login: async function (email, password) {
      if (window.TalendusAPI) {
        try {
          var json = await window.TalendusAPI.login(email, password);
          var apiUser = json && json.data && json.data.user;
          if (apiUser) {
            var staffMap = { ADMIN: "admin", SUPER_ADMIN: "admin", RECRUITER: "recruiter", FINANCE: "finance", EDITOR: "editor" };
            var mapped = staffMap[apiUser.role];
            if (!mapped) throw new Error("not-staff");
            var local = state.users.find(function (x) { return x.email === email; });
            if (local) {
              sessionStorage.setItem(SESSION, JSON.stringify({ id: local.id, role: local.role, access_token: json.data.access_token }));
              await this.hydrateFromApi();
              var again = state.users.find(function (x) { return x.email === email; });
              if (again) {
                sessionStorage.setItem(SESSION, JSON.stringify({ id: again.id, role: again.role, access_token: json.data.access_token }));
                return again;
              }
              return local;
            }
            var created = {
              id: apiUser.id,
              firstName: apiUser.first_name,
              lastName: apiUser.last_name,
              email: apiUser.email,
              role: mapped,
              title: apiUser.title || "",
              initials: ((apiUser.first_name || "?").charAt(0) + (apiUser.last_name || "?").charAt(0)).toUpperCase()
            };
            state.users.push(created);
            sessionStorage.setItem(SESSION, JSON.stringify({ id: created.id, role: created.role, access_token: json.data.access_token }));
            await this.hydrateFromApi();
            return created;
          }
        } catch (e) {}
      }
      var u = state.users.find(function (x) { return x.email === email && x.password === password; });
      if (!u) return null;
      var session = { id: u.id, role: u.role };
      sessionStorage.setItem(SESSION, JSON.stringify(session));
      return u;
    },
    logout: function () {
      sessionStorage.removeItem(SESSION);
      if (window.TalendusAPI) window.TalendusAPI.clearSession();
    },
    session: function () {
      try { return JSON.parse(sessionStorage.getItem(SESSION) || "null"); } catch (e) { return null; }
    },
    me: function () {
      var s = this.session();
      return s ? this.user(s.id) : null;
    },
    can: function (module) {
      var me = this.me();
      if (!me) return false;
      return (PERMS[me.role] || []).indexOf(module) !== -1;
    },
    nid: function (prefix) {
      return prefix + "-" + Math.random().toString(36).slice(2, 8);
    }
  };
})(window);
