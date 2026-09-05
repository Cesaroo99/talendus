(function () {
  var api = window.TalendusAPI;
  if (!api) return;
  var root = document.getElementById("tl-native-app");
  if (!root) return;

  var PERSONA_KEY = "talendus_mobile_persona";
  var LANG_KEY = "talendus_locale";
  var LANG_CHOSEN_KEY = "talendus_locale_chosen";
  var EN = {
    home: "Home",
    jobs: "Jobs",
    hiring: "Needs",
    messages: "Messages",
    me: "Me",
    hello: "Hello",
    welcomeTitle: "You are",
    welcomeLead: "Choose how you want to work with Talendus.",
    tagline: "Placement agency · Every industry",
    talent: "Looking for work",
    talentHint: "A consultant follows you. Submit your resume — we call you when a real mandate fits.",
    employer: "I want to hire",
    employerHint: "Hand us a hiring need. We search, present files, and a consultant calls you back.",
    next: "Continue",
    haveAccount: "I already have an account",
    createAccount: "Create my account",
    login: "Sign in",
    register: "Create an account",
    logout: "Sign out",
    email: "Email",
    password: "Password",
    first: "First name",
    last: "Last name",
    company: "Company name",
    submitLogin: "Sign in",
    submitRegister: "Create my account",
    needAccount: "No account yet?",
    back: "Back",
    call: "Call Talendus",
    wa: "WhatsApp",
    search: "Search a role",
    filters: "Filters",
    emptyJobs: "No roles to show yet.",
    apply: "Ask Talendus to present me",
    applied: "Request sent to your consultant.",
    emptyMsgs: "Write to your consultant. They follow your file with you.",
    write: "Your message",
    send: "Send",
    loading: "Loading…",
    err: "Something went wrong.",
    apps: "My applications",
    emptyApps: "No applications yet. Open Jobs to ask Talendus to present you.",
    city: "City",
    title: "The role you want",
    skills: "Skills",
    save: "Save",
    saved: "Saved.",
    removed: "Removed.",
    passwordUpdated: "Password updated.",
    cv: "Resume",
    upload: "Add my resume",
    uploadDoc: "Add the document",
    uploading: "Sending the file…",
    uploadedOk: "File sent.",
    completeness: "Your file",
    completeFile: "Finish my file",
    statsApps: "Applications",
    statsInterviews: "Interviews",
    hiringLead: "Describe the role in a few lines. Talendus takes the search from there.",
    newNeed: "Hand over a hiring need",
    needTitle: "Role to fill",
    location: "City or area",
    notes: "What you need",
    sendNeed: "Send to Talendus",
    needSent: "Talendus has the need. A consultant will follow up.",
    emptyHiring: "No hiring request yet. Start with one role.",
    emptyThread: "No messages in this conversation yet.",
    consultant: "Your consultant",
    mediate: "A consultant studies your file and gets back to you. Call or write whenever you want to move forward.",
    mediateEmployer: "A consultant takes your hire. Describe the role — we call you back with a shortlist.",
    loginTalentLead: "Sign in to your talent space.",
    loginEmployerLead: "Sign in to your hiring space.",
    loginGenericLead: "Sign in. We open the space that matches your account.",
    registerTalentLead: "Two minutes. Then your consultant can consider you.",
    registerEmployerLead: "Two minutes. Then you can hand us a hiring need.",
    wrongPersonaTalent: "This account is a talent space. We opened that for you.",
    wrongPersonaEmployer: "This account is a company space. We opened that for you.",
    help: "Need help?",
    updateApp: "A new Talendus app is available. Install it to send your resume from the phone.",
    updateAppBtn: "Update the app",
    nextJob: "Roles that may fit",
    openJobs: "See roles",
    openApps: "Follow my applications",
    presented: "Presented files",
    switchPrompt: "Not the right space?",
    changeChoice: "Change",
    notifs: "Updates",
    emptyNotifs: "No updates yet.",
    markAll: "Mark all as read",
    interviews: "Interviews",
    emptyInterviews: "No interview scheduled.",
    savedJobs: "Saved roles",
    emptySaved: "No saved roles yet.",
    saveJob: "Save this role",
    unsaveJob: "Saved",
    alerts: "Job alerts",
    emptyAlerts: "No alert yet. Add a keyword, we watch for you.",
    alertKeywords: "Keywords",
    createAlert: "Create an alert",
    cover: "A line for your consultant (optional)",
    withdraw: "Withdraw",
    withdrawn: "Application withdrawn.",
    alreadyApplied: "Talendus already has this request.",
    viewApp: "Follow this application",
    notFound: "This page is no longer available.",
    readMore: "Read more",
    alertsLead: "Add a keyword. We watch matching roles for you.",
    forgot: "Forgot password?",
    forgotSent: "If an account exists, we sent a reset email.",
    invoices: "Invoices",
    emptyInvoices: "No invoice yet.",
    noBilling: "Billing is not available for this access.",
    downloadPdf: "Download PDF",
    contracts: "Mandates",
    emptyContracts: "No mandate to sign.",
    sign: "Sign",
    signed: "Signed",
    readMandate: "Read the mandate",
    clientReceived: "Received",
    clientOpened: "Opened",
    availability: "Availability",
    missing: "Still to complete",
    nextInterview: "Next interview",
    unsigned: "To sign",
    toPay: "To pay",
    deleteAlert: "Remove",
    pay: "Pay",
    confirmInterview: "Confirm",
    cancelInterview: "Cancel",
    interviewUpdated: "Interview updated.",
    settings: "Settings",
    currentPass: "Current password",
    newPass: "New password",
    changePass: "Update password",
    prefs: "Notifications",
    notifyApp: "In the app",
    notifyEmail: "By email",
    notifyApps: "Applications",
    notifyMsgs: "Messages",
    notifyMatch: "Matching roles",
    notifyInt: "Interviews",
    pipeline: "Pipeline",
    companyProfile: "Company",
    emptyPipeline: "No file presented yet.",
    appDetail: "Application",
    history: "Follow-up",
    space: "Your space",
    profile: "My profile",
    documents: "Resume",
    account: "Account",
    helpTitle: "Talk to Talendus",
    emailUs: "Email",
    phone: "Phone",
    bio: "Summary",
    experience: "Experience",
    languages: "Languages",
    sector: "Industry",
    contract: "Contract type",
    salary: "Desired pay",
    mobility: "Mobility",
    province: "Province",
    photo: "Photo",
    add: "Add",
    remove: "Remove",
    education: "Education",
    certs: "Certifications",
    school: "School",
    diploma: "Diploma",
    companyName: "Company",
    roleHeld: "Role",
    years: "Years",
    downloadCv: "Download",
    noCv: "No resume yet. Add one so a consultant can study your path.",
    cvReady: "Resume on file",
    groupFile: "Your file",
    groupFollow: "Follow-up",
    groupHire: "Hiring",
    groupCompany: "Company",
    groupAccount: "Account",
    seeAll: "See all",
    nextStep: "To do now",
    myNeeds: "Your hiring needs",
    addNeed: "New need",
    seats: "Openings",
    website: "Website",
    address: "Address",
    size: "Company size",
    description: "Description",
    candidate: "Candidate",
    presentedFile: "Presented file",
    jobCity: "City",
    jobSector: "Industry",
    shift: "Shift",
    schedule: "Hours",
    workMode: "Workplace",
    anyChoice: "All",
    jobEducation: "Education",
    jobCerts: "Certifications",
    jobOpenings: "Openings",
    jobStart: "Start date",
    moreFilters: "Narrow the search",
    pick: "Select",
    searchOccupation: "Search a role",
    viaTalendus: "Via Talendus",
    seeJob: "View opening",
    fileSaved: "Saved to Downloads.",
    chooseFile: "Choose a file",
    noFile: "No file chosen",
    filesChosen: "files chosen",
    needFile: "Choose a file first.",
    otherDocs: "Other documents",
    emptyDocs: "No other document yet.",
    multiHint: "You can tick more than one.",
    overtime: "Overtime",
    license: "Driver’s licence",
    union: "Union",
    travel: "Travel",
    benefits: "Benefits",
    shiftPref: "Preferred shift",
    contactUs: "A consultant answers. Call, write or send a WhatsApp.",
    photoHint: "A photo helps your consultant recognise you.",
    expHint: "Add roles you have held. It helps us match you.",
    inboxEmpty: "No file presented yet. Hand us a need, we come back with people.",
    appsHint: "Each application is followed by your consultant.",
    profileLead: "The clearer this is, the faster a consultant can call you for a real mandate.",
    companyLead: "Keep the company file up to date so we brief the right people.",
    needLead: "Describe the role. A consultant opens the search and calls you back.",
    country: "Country",
    birth: "Date of birth",
    startDate: "Start date",
    experienceLevel: "Experience level",
    workStatus: "Work status",
    workAuth: "Work authorization",
    canSponsor: "We can sponsor a candidate",
    sponsorYes: "Sponsorship available",
    occupation: "Occupation",
    editNeed: "Edit this need",
    legalName: "Legal name",
    linkedin: "LinkedIn",
    noAccount: "No account yet? Create one",
    forgotTitle: "Forgot password",
    forgotLead: "Enter the email of your Talendus space. If it exists, we send a reset link.",
    sendReset: "Send the link",
    forgotNeedEmail: "Enter your email first.",
    resetTitle: "New password",
    resetLead: "Choose a password with at least 8 characters.",
    resetBtn: "Update password",
    verifyTitle: "Confirming your email…",
    verifyOk: "Email verified. You can sign in.",
    networkErr: "Cannot reach Talendus. Check your connection and try again.",
    sessionLost: "Sign-in could not be saved on this device. Try again.",
    pushLead: "Get Talendus updates in your phone’s notification bar.",
    pushEnable: "Enable phone notifications",
    notifyPush: "Phone notification bar",
    pushOn: "Updates will appear in your notification bar.",
    joinCall: "Join the call",
    waitHost: "Waiting for the recruiter to start the call.",
    callReady: "The recruiter has started the call. You can join.",
    callAudio: "Audio call",
    callVideo: "Video call",
    langTitle: "Language",
    langFr: "Français",
    langEn: "English",
    callConnecting: "Connecting the interview…"
  };
  var FR = {
    home: "Accueil",
    jobs: "Offres",
    hiring: "Besoins",
    messages: "Messages",
    me: "Moi",
    hello: "Bonjour",
    welcomeTitle: "Vous êtes",
    welcomeLead: "Choisissez comment avancer avec Talendus.",
    tagline: "Agence de placement · Tous secteurs",
    talent: "Je cherche un emploi",
    talentHint: "Un conseiller vous suit. Déposez votre CV, on vous rappelle pour un vrai mandat.",
    employer: "Je recrute",
    employerHint: "Confiez-nous un besoin. On cherche, on vous présente des dossiers, un conseiller vous rappelle.",
    next: "Continuer",
    haveAccount: "J’ai déjà un compte",
    createAccount: "Créer mon compte",
    login: "Connexion",
    register: "Créer un compte",
    logout: "Déconnexion",
    email: "Courriel",
    password: "Mot de passe",
    first: "Prénom",
    last: "Nom",
    company: "Nom de l’entreprise",
    submitLogin: "Me connecter",
    submitRegister: "Créer mon compte",
    needAccount: "Pas encore de compte ?",
    back: "Retour",
    call: "Appeler Talendus",
    wa: "WhatsApp",
    search: "Rechercher un poste",
    filters: "Filtres",
    emptyJobs: "Aucune offre à afficher pour le moment.",
    apply: "Demander à être présenté",
    applied: "Demande envoyée à votre conseiller.",
    emptyMsgs: "Écrivez à votre conseiller. Il suit votre dossier avec vous.",
    write: "Votre message",
    send: "Envoyer",
    loading: "Chargement…",
    err: "Une erreur s’est produite.",
    apps: "Mes candidatures",
    emptyApps: "Aucune candidature pour le moment. Ouvrez Offres pour demander à être présenté.",
    city: "Ville",
    title: "Le poste que vous visez",
    skills: "Compétences",
    save: "Enregistrer",
    saved: "Enregistré.",
    removed: "Retiré.",
    passwordUpdated: "Mot de passe mis à jour.",
    cv: "CV",
    upload: "Ajouter mon CV",
    uploadDoc: "Ajouter le document",
    uploading: "Envoi du fichier…",
    uploadedOk: "Fichier envoyé.",
    completeness: "Votre dossier",
    completeFile: "Compléter mon dossier",
    statsApps: "Candidatures",
    statsInterviews: "Entretiens",
    hiringLead: "Décrivez le poste en quelques lignes. Talendus prend la recherche.",
    newNeed: "Confier un besoin",
    needTitle: "Poste à pourvoir",
    location: "Ville ou secteur",
    notes: "Votre besoin",
    sendNeed: "Envoyer à Talendus",
    needSent: "Talendus a bien reçu le besoin. Un conseiller fait le suivi.",
    emptyHiring: "Aucun besoin pour le moment. Commencez par un poste.",
    emptyThread: "Aucun message dans cette conversation.",
    consultant: "Votre conseiller",
    mediate: "Un conseiller étudie votre dossier et vous relance. Appelez-nous ou écrivez-nous dès que vous voulez avancer.",
    mediateEmployer: "Un conseiller prend votre recrutement. Décrivez le poste, on vous rappelle avec une shortlist.",
    loginTalentLead: "Entrez dans votre espace talent.",
    loginEmployerLead: "Entrez dans votre espace entreprise.",
    loginGenericLead: "Connectez-vous. On ouvre l’espace qui correspond à votre compte.",
    registerTalentLead: "Deux minutes. Ensuite, votre conseiller peut vous considérer.",
    registerEmployerLead: "Deux minutes. Ensuite, vous pouvez confier un besoin.",
    wrongPersonaTalent: "Ce compte est un espace talent. Nous l’avons ouvert pour vous.",
    wrongPersonaEmployer: "Ce compte est un espace entreprise. Nous l’avons ouvert pour vous.",
    help: "Besoin d’aide ?",
    updateApp: "Une nouvelle version de l’appli Talendus est disponible. Installez-la pour déposer un CV depuis le téléphone.",
    updateAppBtn: "Mettre à jour l’appli",
    nextJob: "Postes qui peuvent convenir",
    openJobs: "Voir les offres",
    openApps: "Suivre mes candidatures",
    presented: "Dossiers présentés",
    switchPrompt: "Ce n’est pas le bon espace ?",
    changeChoice: "Changer",
    notifs: "Suivi",
    emptyNotifs: "Aucune nouvelle pour le moment.",
    markAll: "Tout marquer comme lu",
    interviews: "Entretiens",
    emptyInterviews: "Aucun entretien planifié.",
    savedJobs: "Offres gardées",
    emptySaved: "Aucune offre gardée pour le moment.",
    saveJob: "Garder cette offre",
    unsaveJob: "Offre gardée",
    alerts: "Alertes emploi",
    emptyAlerts: "Aucune alerte. Ajoutez un mot-clé, on surveille pour vous.",
    alertKeywords: "Mots-clés",
    createAlert: "Créer une alerte",
    cover: "Un mot pour votre conseiller (facultatif)",
    withdraw: "Retirer",
    withdrawn: "Candidature retirée.",
    alreadyApplied: "Talendus a déjà cette demande.",
    viewApp: "Suivre cette candidature",
    notFound: "Cette page n’est plus disponible.",
    readMore: "Lire la suite",
    alertsLead: "Ajoutez un mot-clé. On surveille les offres pour vous.",
    forgot: "Mot de passe oublié ?",
    forgotSent: "Si un compte existe, un courriel de réinitialisation part.",
    invoices: "Factures",
    emptyInvoices: "Aucune facture pour le moment.",
    noBilling: "La facturation n’est pas disponible pour cet accès.",
    downloadPdf: "Télécharger le PDF",
    contracts: "Mandats",
    emptyContracts: "Aucun mandat à signer.",
    sign: "Signer",
    signed: "Signé",
    readMandate: "Lire le mandat",
    clientReceived: "Reçu",
    clientOpened: "Ouvert",
    availability: "Disponibilité",
    missing: "À compléter",
    nextInterview: "Prochain entretien",
    unsigned: "À signer",
    toPay: "À payer",
    deleteAlert: "Supprimer",
    pay: "Payer",
    confirmInterview: "Confirmer",
    cancelInterview: "Annuler",
    interviewUpdated: "Entretien mis à jour.",
    settings: "Paramètres",
    currentPass: "Mot de passe actuel",
    newPass: "Nouveau mot de passe",
    changePass: "Mettre à jour le mot de passe",
    prefs: "Notifications",
    notifyApp: "Dans l’appli",
    notifyEmail: "Par courriel",
    notifyApps: "Candidatures",
    notifyMsgs: "Messages",
    notifyMatch: "Offres qui correspondent",
    notifyInt: "Entretiens",
    pipeline: "Pipeline",
    companyProfile: "Entreprise",
    emptyPipeline: "Aucun dossier présenté pour le moment.",
    appDetail: "Candidature",
    history: "Suivi",
    space: "Votre espace",
    profile: "Mon profil",
    documents: "CV",
    account: "Compte",
    helpTitle: "Parler à Talendus",
    emailUs: "Courriel",
    phone: "Téléphone",
    bio: "Résumé",
    experience: "Expérience",
    languages: "Langues",
    sector: "Secteur",
    contract: "Type de contrat",
    salary: "Salaire souhaité",
    mobility: "Mobilité",
    province: "Province",
    photo: "Photo",
    add: "Ajouter",
    remove: "Retirer",
    education: "Formations",
    certs: "Certifications",
    school: "École",
    diploma: "Diplôme",
    companyName: "Entreprise",
    roleHeld: "Poste",
    years: "Années",
    downloadCv: "Télécharger",
    noCv: "Aucun CV pour le moment. Ajoutez-en un pour qu’un conseiller étudie votre parcours.",
    cvReady: "CV au dossier",
    groupFile: "Votre dossier",
    groupFollow: "Suivi",
    groupHire: "Recrutement",
    groupCompany: "Entreprise",
    groupAccount: "Compte",
    seeAll: "Tout voir",
    nextStep: "À faire maintenant",
    myNeeds: "Vos besoins",
    addNeed: "Nouveau besoin",
    seats: "Postes",
    website: "Site web",
    address: "Adresse",
    size: "Taille",
    description: "Description",
    candidate: "Candidat",
    presentedFile: "Dossier présenté",
    jobCity: "Ville",
    jobSector: "Secteur",
    shift: "Quart",
    schedule: "Horaire",
    workMode: "Présence",
    anyChoice: "Tous",
    jobEducation: "Formation",
    jobCerts: "Certifications",
    jobOpenings: "Postes à pourvoir",
    jobStart: "Entrée en poste",
    moreFilters: "Préciser la recherche",
    pick: "Choisir",
    searchOccupation: "Rechercher un métier",
    viaTalendus: "Par Talendus",
    seeJob: "Voir l’offre",
    fileSaved: "Fichier enregistré dans Téléchargements.",
    chooseFile: "Choisir un fichier",
    noFile: "Aucun fichier choisi",
    filesChosen: "fichiers choisis",
    needFile: "Choisissez d’abord un fichier.",
    otherDocs: "Autres documents",
    emptyDocs: "Aucun autre document pour le moment.",
    multiHint: "Vous pouvez en cocher plusieurs.",
    overtime: "Heures sup.",
    license: "Permis",
    union: "Syndicat",
    travel: "Déplacements",
    benefits: "Avantages",
    shiftPref: "Quart souhaité",
    contactUs: "Un conseiller vous répond. Appelez, écrivez ou envoyez un WhatsApp.",
    photoHint: "Une photo aide votre conseiller à vous reconnaître.",
    expHint: "Ajoutez les postes que vous avez tenus. Ça nous aide à vous placer.",
    inboxEmpty: "Aucun dossier présenté pour le moment. Confiez un besoin, on revient avec des profils.",
    appsHint: "Chaque candidature est suivie par votre conseiller.",
    profileLead: "Plus c’est clair, plus vite un conseiller peut vous rappeler pour un vrai mandat.",
    companyLead: "Tenez la fiche à jour pour qu’on briefe les bonnes personnes.",
    needLead: "Décrivez le poste. Un conseiller ouvre la recherche et vous rappelle.",
    country: "Pays",
    birth: "Date de naissance",
    startDate: "Date de début",
    experienceLevel: "Niveau d’expérience",
    workStatus: "Statut d’autorisation",
    workAuth: "Autorisation de travail",
    canSponsor: "Nous pouvons parrainer un candidat",
    sponsorYes: "Parrainage possible",
    occupation: "Métier",
    editNeed: "Modifier ce besoin",
    legalName: "Raison sociale",
    linkedin: "LinkedIn",
    noAccount: "Pas encore de compte ? Créer un compte",
    forgotTitle: "Mot de passe oublié",
    forgotLead: "Indiquez le courriel de votre espace Talendus. S’il existe, un lien de réinitialisation part.",
    sendReset: "Envoyer le lien",
    forgotNeedEmail: "Indiquez d’abord votre courriel.",
    resetTitle: "Nouveau mot de passe",
    resetLead: "Choisissez un mot de passe d’au moins 8 caractères.",
    resetBtn: "Mettre à jour",
    verifyTitle: "Vérification du courriel…",
    verifyOk: "Courriel vérifié. Vous pouvez vous connecter.",
    networkErr: "Impossible de joindre Talendus. Vérifiez la connexion, puis réessayez.",
    sessionLost: "La connexion n’a pas pu être enregistrée sur cet appareil. Réessayez.",
    pushLead: "Recevez les suivis Talendus dans la barre de notifications du téléphone.",
    pushEnable: "Activer les notifications du téléphone",
    notifyPush: "Barre de notifications du téléphone",
    pushOn: "Les suivis apparaîtront dans la barre de notifications.",
    joinCall: "Rejoindre l’appel",
    waitHost: "En attente que le recruteur lance l’appel.",
    callReady: "Le recruteur a lancé l’appel. Vous pouvez rejoindre.",
    callAudio: "Appel audio",
    callVideo: "Appel vidéo",
    langTitle: "Langue",
    langFr: "Français",
    langEn: "English",
    callConnecting: "Connexion à l’entretien…"
  };

  function pageIsEn() {
    var path = (location.pathname || "").toLowerCase();
    return path.indexOf("/en/") === 0;
  }
  function storedLocale() {
    try { return localStorage.getItem(LANG_KEY) || ""; } catch (e) { return ""; }
  }
  function localeChosen() {
    try { return localStorage.getItem(LANG_CHOSEN_KEY) === "1"; } catch (e) { return false; }
  }
  function detectLang() {
    if (localeChosen()) {
      var stored = storedLocale().toLowerCase();
      if (stored.indexOf("en") === 0) return true;
      if (stored.indexOf("fr") === 0) return false;
    }
    return pageIsEn();
  }
  var isEn = detectLang();
  var t = isEn ? EN : FR;
  document.documentElement.lang = isEn ? "en-CA" : "fr-CA";
  function applyLocale(locale, persist, chosen) {
    var wantEn = String(locale || "").toLowerCase().indexOf("en") === 0;
    isEn = wantEn;
    t = isEn ? EN : FR;
    document.documentElement.lang = isEn ? "en-CA" : "fr-CA";
    try { localStorage.setItem(LANG_KEY, isEn ? "en-CA" : "fr-CA"); } catch (e) {}
    if (chosen) {
      try { localStorage.setItem(LANG_CHOSEN_KEY, "1"); } catch (e) {}
    }
    if (persist && state.user) {
      api.request("/users/me/preferences", { method: "PATCH", body: { locale: isEn ? "en-CA" : "fr-CA" } }).catch(function () {});
    }
  }

  var state = {
    user: api.currentUser(),
    contact: { phone_e164: "12635585225", phone_display: "263 558 5225", email: "info@talendus.ca", demo: false },
    jobs: [],
    job: null,
    dash: null,
    profile: null,
    apps: [],
    threads: [],
    directory: [],
    conversation: [],
    hiring: [],
    notifs: [],
    interviews: [],
    saved: [],
    alerts: [],
    inbox: [],
    invoices: [],
    contracts: [],
    jobOptions: null,
    jobShift: "",
    jobSchedule: "",
    jobWorkMode: "",
    jobTitle: "",
    jobAuth: "",
    jobSponsor: "",
    prefs: null,
    company: null,
    application: null,
    appsReady: false,
    docs: [],
    query: "",
    jobCity: "",
    jobSector: "",
    jobContract: "",
    jobExperience: "",
    need: null,
    notice: "",
    error: "",
    mismatch: "",
    authEmail: ""
  };

  var icons = {
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/></svg>',
    jobs: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5h8v2"/></svg>',
    msg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 6h14v10H8l-3 3V6z"/></svg>',
    me: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.5"/><path d="M5 19c1.5-3.2 4-5 7-5s5.5 1.8 7 5"/></svg>',
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 3h3l1 4-2 1a12 12 0 006 6l1-2 4 1v3c0 1-1 2-2 2C10 18 6 14 6 7c0-1 1-2 1-4z"/></svg>',
    chevron: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 6l6 6-6 6"/></svg>',
    talent: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.2"/><path d="M5 19c1.4-3 3.8-4.6 7-4.6S17.6 16 19 19"/><path d="M17 4.5l2 2 3.2-3.2"/></svg>',
    hire: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6h8v2"/><path d="M12 12v4"/><path d="M10 14h4"/></svg>',
    bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9a6 6 0 1112 0c0 7 3 7 3 7H3s3 0 3-7"/><path d="M10 19a2 2 0 004 0"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/></svg>'
  };
  var MARK = '<svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg"><path fill="#ffffff" fill-rule="evenodd" d="M18 1.5c9.113 0 16.5 7.387 16.5 16.5S27.113 34.5 18 34.5 1.5 27.113 1.5 18 8.887 1.5 18 1.5zm-7.25 9.75h14.5a1.75 1.75 0 1 1 0 3.5h-5.5v12.75a1.75 1.75 0 1 1-3.5 0V14.75h-5.5a1.75 1.75 0 1 1 0-3.5z"/></svg>';
  function brandOrbit(cls) {
    return '<div class="tn-orbit' + (cls ? " " + cls : "") + '" aria-hidden="true">' +
      '<span class="tn-ring tn-ring-a"></span><span class="tn-ring tn-ring-b"></span><span class="tn-ring tn-ring-c"></span>' +
      '<div class="tn-mark">' + MARK + "</div></div>";
  }

  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function dataOf(json) { return json && json.data ? json.data : json; }
  function getPersona() {
    try { return sessionStorage.getItem(PERSONA_KEY) || ""; } catch (e) { return ""; }
  }
  function setPersona(value) {
    try {
      if (value) sessionStorage.setItem(PERSONA_KEY, value);
      else sessionStorage.removeItem(PERSONA_KEY);
    } catch (e) {}
  }
  function staffRole(role) {
    return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
  }
  function isEmployer(user) {
    user = user || state.user;
    return !!(user && user.role === "EMPLOYER");
  }
  function isCandidate(user) {
    user = user || state.user;
    return !!(user && user.role === "CANDIDATE");
  }
  function canonicalize(name, id) {
    var aliases = {
      dashboard: "home", home: "home", profile: "profile", documents: "cv", cv: "cv", resume: "cv",
      settings: "settings", account: "settings", applications: "apps", candidatures: "apps",
      application: "app", apps: "apps", saved: "saved", sauvegardees: "saved", alerts: "alerts",
      alertes: "alerts", notifications: "notifs", notifs: "notifs", entretiens: "interviews",
      interviews: "interviews", pipeline: "pipeline", ats: "pipeline", company: "company",
      billing: "invoices", facturation: "invoices", invoices: "invoices", contrats: "contracts",
      mandats: "contracts", contracts: "contracts", hiring: "hiring", messages: "messages",
      me: "me", jobs: "jobs", job: "job", inbox: "inbox", help: "help", aide: "help",
      need: "need", "hiring-new": "need", "job-new": "need",
      forgot: "forgot", reset: "reset", verify: "verify", login: "login", register: "register",
      call: "call", appel: "call"
    };
    name = aliases[name] || name;
    if (isCandidate() && name === "jobs" && id) name = "job";
    if (isEmployer()) {
      if (name === "hiring" && id) name = "need";
      if (name === "jobs" || name === "job" || name === "job-edit") name = id ? "need" : "hiring";
      if (name === "apps" || name === "app") name = "inbox";
      if (name === "profile" || name === "cv") name = "company";
    }
    return { name: name, id: id || "" };
  }
  function stashAuthToken(name, id) {
    var key = "tn-" + name + "-token";
    if (id) {
      try { sessionStorage.setItem(key, id); } catch (e) {}
      var hash = location.hash || "";
      if (hash.indexOf("#/" + name + "/") === 0 || hash.indexOf("#" + name + "/") === 0) {
        try { history.replaceState(null, "", location.pathname + location.search + "#/" + name); } catch (e) {}
      }
      return id;
    }
    try { return sessionStorage.getItem(key) || ""; } catch (e) { return ""; }
  }
  function clearAuthToken(name) {
    try { sessionStorage.removeItem("tn-" + name + "-token"); } catch (e) {}
  }
  function route() {
    var raw = (location.hash || "").replace(/^#/, "");
    var query = {};
    var qIndex = raw.indexOf("?");
    if (qIndex >= 0) {
      raw.slice(qIndex + 1).split("&").forEach(function (part) {
        var kv = part.split("=");
        if (!kv[0]) return;
        try {
          query[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
        } catch (err) {}
      });
      raw = raw.slice(0, qIndex);
    }
    var parts = raw.replace(/^\//, "").split("/").filter(Boolean);
    var name = parts[0];
    var id = decodeURIComponent(parts.slice(1).join("/"));
    if (!name) name = state.user ? "home" : "welcome";
    var mapped = canonicalize(name, id);
    if (!mapped.id && query.token) mapped.id = query.token;
    mapped.query = query;
    if (mapped.name === "reset" || mapped.name === "verify") {
      mapped.id = stashAuthToken(mapped.name, mapped.id);
    }
    return mapped;
  }
  function allowedRoute(name) {
    if (!state.user) return ["welcome", "login", "register", "forgot", "reset", "verify"].indexOf(name) !== -1;
    if (isCandidate()) return ["home", "jobs", "job", "apps", "app", "messages", "me", "notifs", "alerts", "saved", "interviews", "settings", "profile", "cv", "help", "call"].indexOf(name) !== -1;
    if (isEmployer()) return ["home", "hiring", "need", "messages", "me", "notifs", "interviews", "inbox", "invoices", "contracts", "pipeline", "company", "settings", "help", "call"].indexOf(name) !== -1;
    return name === "home" || name === "me" || name === "messages" || name === "settings";
  }
  function portalHash(href) {
    if (!href) return "#/home";
    var hash = "";
    try {
      var u = new URL(href, location.origin);
      hash = (u.hash || "").replace(/^#\/?/, "");
      var m = u.pathname.match(/\/(candidate|employer)(?:\/(.*))?$/);
      if (m && m[2]) hash = m[2];
    } catch (e) {
      var bits = String(href).split("#");
      hash = (bits[1] || "").replace(/^\//, "");
    }
    var parts = hash.split("/").filter(Boolean);
    var mapped = canonicalize(parts[0] || "home", parts.slice(1).join("/"));
    return "#/" + mapped.name + (mapped.id ? "/" + mapped.id : "");
  }
  function go(hash) {
    if ((location.hash || "") === hash) render();
    else location.hash = hash;
  }
  function contactMail() { return (state.contact && state.contact.email) || "info@talendus.ca"; }
  function hasPublicPhone() {
    var c = state.contact || {};
    if (c.demo) return false;
    return String(c.phone_e164 || "").replace(/\D/g, "").length >= 10;
  }
  function telHref() {
    if (!hasPublicPhone()) return "mailto:" + contactMail();
    return "tel:+" + String(state.contact.phone_e164 || "").replace(/\D/g, "");
  }
  function waHref() {
    if (!hasPublicPhone()) return "mailto:" + contactMail();
    var n = String(state.contact.phone_e164 || "").replace(/\D/g, "");
    var msg = encodeURIComponent(isEn ? "Hello Talendus" : "Bonjour Talendus");
    return "https://wa.me/" + n + "?text=" + msg;
  }
  function nativeAppVersion() {
    var ua = navigator.userAgent || "";
    var m = ua.match(/TalendusApp\/(\d+(?:\.\d+)*)/);
    if (m) return m[1];
    try {
      if (window.TalendusNative && typeof window.TalendusNative.appVersion === "function") {
        return String(window.TalendusNative.appVersion() || "");
      }
    } catch (e) {}
    return "";
  }
  function versionLt(a, b) {
    var as = String(a || "").split(".").map(function (n) { return parseInt(n, 10) || 0; });
    var bs = String(b || "").split(".").map(function (n) { return parseInt(n, 10) || 0; });
    var len = Math.max(as.length, bs.length);
    for (var i = 0; i < len; i++) {
      var x = as[i] || 0;
      var y = bs[i] || 0;
      if (x < y) return true;
      if (x > y) return false;
    }
    return false;
  }
  function needsApkUpdate() {
    var ua = navigator.userAgent || "";
    if (ua.indexOf("TalendusApp/") === -1 && !window.TalendusNative) return false;
    var v = nativeAppVersion();
    if (!v) return /TalendusApp\/1\.[0-7](?:\D|$)/.test(ua);
    return versionLt(v, "1.8");
  }
  function apkUpdateBanner() {
    if (!needsApkUpdate()) return "";
    return '<div class="tn-card tn-push-card tn-update-card"><p class="tn-meta">' + esc(t.updateApp) +
      '</p><a class="tn-btn" href="/download/talendus.apk">' + esc(t.updateAppBtn) + "</a></div>";
  }
  function setNotice(msg, err) {
    state.notice = err ? "" : (msg || "");
    state.error = err ? (msg || t.err) : "";
  }
  function flash() {
    var bits = [];
    if (state.mismatch) bits.push('<p class="tn-ok">' + esc(state.mismatch) + "</p>");
    if (state.error) bits.push('<p class="tn-error">' + esc(state.error) + "</p>");
    if (state.notice) bits.push('<p class="tn-ok">' + esc(state.notice) + "</p>");
    return bits.join("");
  }
  function helpLine() {
    var label = hasPublicPhone() ? (state.contact.phone_display || t.call) : contactMail();
    return '<p class="tn-help">' + esc(t.help) + ' <a href="' + telHref() + '">' + esc(label) + "</a></p>";
  }
  function statusLabel(s) {
    var key = String(s || "").toUpperCase().replace(/-/g, "_");
    var fr = {
      SENT: "Envoyée", SUBMITTED: "Candidature envoyée", RECEIVED: "Reçue", REVIEW: "À l’étude",
      UNDER_REVIEW: "À l’étude", SHORTLISTED: "Présélection", PRESELECT: "Présélection",
      INTERVIEW: "Entretien", SECOND_INTERVIEW: "2e entretien", OFFER_SENT: "Offre d’emploi",
      SCHEDULED: "Planifié", CONFIRMED: "Confirmé", CANCELLED: "Annulé", COMPLETED: "Terminé",
      NO_SHOW: "Absent", HIRED: "Embauchée", REJECTED: "Non retenue", WITHDRAWN: "Retirée",
      PRESENTED: "Présenté", OPEN: "Ouvert", NEW: "Nouveau", IN_PROGRESS: "En cours", CLOSED: "Clos",
      PAID: "Payée", PENDING: "En attente", OVERDUE: "En retard", SENT_INV: "Envoyée",
      PUBLISHED: "Publiée", DRAFT: "Brouillon", PAUSED: "En pause", ARCHIVED: "Archivée",
      REQUEST_SUBMITTED: "Besoin transmis", CLIENT_CONTACTED: "Échange avec Talendus",
      NEEDS_CONFIRMED: "Profil défini", JOB_BEING_PREPARED: "Offre en préparation",
      CLIENT_VALIDATION: "Validation demandée", JOB_PUBLISHED: "Recherche lancée",
      SOURCING: "Recherche en cours", SCREENING: "Présélection en cours",
      INTERVIEWS: "Entretiens Talendus", SHORTLIST: "Shortlist disponible",
      CLIENT_REVIEW: "Profils à consulter", HIRING: "Décision en cours",
      TALENDUS: "Talendus", CLIENT: "Client", PHONE: "Téléphone", VIDEO: "Visio",
      ONSITE: "Sur place", OFFER: "Offre", OWNER: "Propriétaire", ADMIN: "Administrateur",
      HR: "RH", RECRUITER: "Recruteur", MEMBER: "Membre", BILLING: "Facturation",
      NOUVEAUX: "Nouveau", PRESELECTION: "Présélection", ENTRETIEN_TALENDUS: "Entretien",
      PRESENTATION: "Présenté", ENTRETIEN_CLIENT: "Entretien client", PLACEMENT: "Embauchée",
      PENDING_VALIDATION: "En validation", REFUNDED: "Remboursée", FILLED: "Pourvu",
      ACTIVE: "Actif", EXPIRED: "Expiré"
    };
    var en = {
      SENT: "Sent", SUBMITTED: "Submitted", RECEIVED: "Received", REVIEW: "Under review",
      UNDER_REVIEW: "Under review", SHORTLISTED: "Shortlisted", PRESELECT: "Shortlist",
      INTERVIEW: "Interview", SECOND_INTERVIEW: "Second interview", OFFER_SENT: "Offer sent",
      SCHEDULED: "Scheduled", CONFIRMED: "Confirmed", CANCELLED: "Cancelled", COMPLETED: "Done",
      NO_SHOW: "No-show", HIRED: "Hired", REJECTED: "Not retained", WITHDRAWN: "Withdrawn",
      PRESENTED: "Presented", OPEN: "Open", NEW: "New", IN_PROGRESS: "In progress", CLOSED: "Closed",
      PAID: "Paid", PENDING: "Pending", OVERDUE: "Overdue", PUBLISHED: "Published", DRAFT: "Draft",
      PAUSED: "Paused", ARCHIVED: "Archived", REQUEST_SUBMITTED: "Need submitted",
      CLIENT_CONTACTED: "Talking with Talendus", NEEDS_CONFIRMED: "Profile defined",
      JOB_BEING_PREPARED: "Offer being prepared", CLIENT_VALIDATION: "Validation requested",
      JOB_PUBLISHED: "Search launched", SOURCING: "Search in progress",
      SCREENING: "Screening", INTERVIEWS: "Talendus interviews", SHORTLIST: "Shortlist ready",
      CLIENT_REVIEW: "Profiles to review", HIRING: "Your decision",
      TALENDUS: "Talendus", CLIENT: "Client", PHONE: "Phone", VIDEO: "Video",
      ONSITE: "On site", OFFER: "Offer", OWNER: "Owner", ADMIN: "Administrator",
      HR: "HR", RECRUITER: "Recruiter", MEMBER: "Member", BILLING: "Billing",
      NOUVEAUX: "New", PRESELECTION: "Shortlist", ENTRETIEN_TALENDUS: "Interview",
      PRESENTATION: "Presented", ENTRETIEN_CLIENT: "Client interview", PLACEMENT: "Hired",
      PENDING_VALIDATION: "Pending validation", REFUNDED: "Refunded", FILLED: "Filled",
      ACTIVE: "Active", EXPIRED: "Expired"
    };
    var mapped = (isEn ? en : fr)[key];
    if (mapped) return mapped;
    if (s) return String(s).replace(/_/g, " ");
    return "";
  }
  function langSwitch() {
    return '<div class="tn-langs" role="group" aria-label="' + esc(t.langTitle) + '">' +
      '<button type="button" class="tn-lang' + (isEn ? "" : " is-on") + '" data-locale="fr-CA">' + esc(t.langFr) + "</button>" +
      '<button type="button" class="tn-lang' + (isEn ? " is-on" : "") + '" data-locale="en-CA">' + esc(t.langEn) + "</button>" +
      "</div>";
  }
  function optionLabel(item) {
    if (!item) return "";
    if (typeof item === "string") return item;
    return isEn ? (item.label_en || item.label || item.value) : (item.label || item.value);
  }
  function optionValue(item) {
    if (!item) return "";
    return typeof item === "string" ? item : (item.value || item.label || "");
  }
  function optionGroup(item) {
    if (!item || typeof item === "string") return "";
    return isEn ? (item.group_en || item.group || "") : (item.group || "");
  }
  function catalogLabel(items, value) {
    if (!value) return "";
    var found = (items || []).find(function (item) { return String(optionValue(item)) === String(value); });
    return found ? optionLabel(found) : String(value);
  }
  function choiceSelect(name, items, selected, allLabel, required) {
    if (items && items.length && items[0] && items[0].group) {
      return groupedPick(name, items, selected, allLabel, required);
    }
    var html = '<select name="' + name + '"' + (required ? " required" : "") + '><option value="">' + esc(allLabel == null ? t.anyChoice : allLabel) + "</option>";
    var seen = {};
    var openGroup = null;
    (items || []).forEach(function (item) {
      var val = optionValue(item);
      if (!val || seen[val]) return;
      seen[val] = true;
      var group = optionGroup(item);
      if (group !== openGroup) {
        if (openGroup) html += "</optgroup>";
        if (group) html += '<optgroup label="' + esc(group) + '">';
        openGroup = group || null;
      }
      html += '<option value="' + esc(val) + '"' + (String(selected || "") === String(val) ? " selected" : "") + ">" + esc(optionLabel(item)) + "</option>";
    });
    if (openGroup) html += "</optgroup>";
    if (selected && !seen[String(selected)]) {
      html += '<option value="' + esc(selected) + '" selected>' + esc(selected) + "</option>";
    }
    return html + "</select>";
  }
  function groupedPick(name, items, selected, allLabel, required) {
    var empty = allLabel == null ? t.anyChoice : allLabel;
    var shown = selected ? catalogLabel(items, selected) : empty;
    var list = name === "title" ? "occupations" : name;
    return '<div class="tn-pick">' +
      '<input type="hidden" name="' + name + '" value="' + esc(selected || "") + '"' + (required ? " required" : "") + ">" +
      '<button type="button" class="tn-pick-btn" data-pick-open data-pick-list="' + esc(list) +
      '" data-pick-empty="' + esc(empty) + '"' + (required ? " data-pick-required" : "") + ">" +
      '<span data-pick-label>' + esc(shown) + "</span>" + icons.chevron + "</button></div>";
  }
  function closePickSheet() {
    var sheet = document.querySelector(".tn-pick-sheet");
    if (sheet) sheet.remove();
  }
  function openPickSheet(input, items, emptyLabel, required) {
    closePickSheet();
    if (!input) return;
    items = items || [];
    var sheet = document.createElement("div");
    sheet.className = "tn-pick-sheet is-on";
    sheet.setAttribute("role", "dialog");
    sheet.innerHTML = '<div class="tn-pick-card">' +
      '<input type="search" class="tn-pick-search" placeholder="' + esc(t.searchOccupation) + '" autocomplete="off">' +
      '<div class="tn-pick-list"></div>' +
      '<button type="button" class="tn-btn tn-btn-ghost" data-pick-close>' + esc(t.back) + "</button></div>";
    document.body.appendChild(sheet);
    var listEl = sheet.querySelector(".tn-pick-list");
    var searchEl = sheet.querySelector(".tn-pick-search");
    function paint(q) {
      q = String(q || "").toLowerCase().trim();
      var html = "";
      var openGroup = "";
      if (!required && !q) {
        html += '<button type="button" class="tn-pick-option' + (input.value ? "" : " is-on") +
          '" data-pick-value="">' + esc(emptyLabel || t.anyChoice) + "</button>";
      }
      items.forEach(function (item) {
        var val = optionValue(item);
        var label = optionLabel(item);
        if (!val) return;
        if (q && (label + " " + val + " " + optionGroup(item)).toLowerCase().indexOf(q) === -1) return;
        var group = optionGroup(item);
        if (group && group !== openGroup) {
          html += '<p class="tn-pick-group">' + esc(group) + "</p>";
          openGroup = group;
        }
        html += '<button type="button" class="tn-pick-option' + (String(input.value) === String(val) ? " is-on" : "") +
          '" data-pick-value="' + esc(val) + '">' + esc(label) + "</button>";
      });
      listEl.innerHTML = html || '<p class="tn-meta">' + esc(t.emptyJobs) + "</p>";
    }
    paint("");
    searchEl.addEventListener("input", function () { paint(searchEl.value); });
    sheet.addEventListener("click", function (ev) {
      if (ev.target === sheet || ev.target.closest("[data-pick-close]")) {
        closePickSheet();
        return;
      }
      var opt = ev.target.closest("[data-pick-value]");
      if (!opt) return;
      input.value = opt.getAttribute("data-pick-value") || "";
      var wrap = input.closest(".tn-pick");
      var lab = wrap && wrap.querySelector("[data-pick-label]");
      if (lab) lab.textContent = catalogLabel(items, input.value) || emptyLabel || t.pick;
      input.dispatchEvent(new Event("change", { bubbles: true }));
      closePickSheet();
    });
    setTimeout(function () { searchEl.focus(); }, 40);
  }
  function labeledChoice(name, label, items, selected, allLabel, required) {
    var id = "tn-f-" + name;
    return '<label for="' + id + '">' + esc(label) + "</label>" +
      choiceSelect(name, items, selected, allLabel, required).replace("<select ", '<select id="' + esc(id) + '" ');
  }
  function selectedSet(raw) {
    var out = {};
    String(raw || "").split(",").forEach(function (part) {
      var value = part.trim();
      if (!value) return;
      if (/bilingue|fr\/en|français et anglais|french and english/i.test(value)) {
        out["Français"] = true;
        out["Anglais"] = true;
        return;
      }
      out[value] = true;
    });
    return out;
  }
  function languageItems() {
    var picks = jobOpts().language_choices;
    return (picks && picks.length) ? picks : (jobOpts().languages || []);
  }
  function choiceGroup(name, items, selected, label) {
    var picked = selectedSet(selected);
    var seen = {};
    var html = '<fieldset class="tn-choices"><legend>' + esc(label) + "</legend><p class=\"tn-meta\">" + esc(t.multiHint) + "</p><div class=\"tn-choice-grid\">";
    function add(val, text) {
      if (!val || seen[val]) return;
      seen[val] = true;
      html += '<label class="tn-chip-check"><input type="checkbox" name="' + name + '" value="' + esc(val) + '"' +
        (picked[val] ? " checked" : "") + "> " + esc(text || val) + "</label>";
    }
    (items || []).forEach(function (item) {
      add(optionValue(item), optionLabel(item));
    });
    Object.keys(picked).forEach(function (val) { add(val, val); });
    return html + "</div></fieldset>";
  }
  function hasNativePicker() {
    try {
      if (!window.TalendusNative) return false;
      if (typeof window.TalendusNative.canPickFiles === "function") return !!window.TalendusNative.canPickFiles();
      return typeof window.TalendusNative.openDocumentPicker === "function";
    } catch (e) {
      return false;
    }
  }
  var CV_ACCEPT = ".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp,application/pdf,image/png,image/jpeg";
  function filePicker(accept, multiple) {
    var imagesOnly = !!(accept && accept.indexOf("image/") === 0 && accept.indexOf("pdf") === -1);
    var native = hasNativePicker();
    return '<div class="tn-file">' +
      (native
        ? '<button type="button" class="tn-file-btn" data-native-pick data-multiple="' + (multiple ? "1" : "0") +
          '" data-images="' + (imagesOnly ? "1" : "0") + '">' + esc(t.chooseFile) + "</button>"
        : "") +
      '<label class="tn-file-hit"' + (native ? " hidden" : "") + ">" +
      '<input class="tn-file-input" type="file" name="file"' +
      (accept ? ' accept="' + esc(accept) + '"' : "") +
      (multiple ? " multiple" : "") + ">" +
      (native ? "" : '<span class="tn-file-btn">' + esc(t.chooseFile) + "</span>") +
      "</label>" +
      '<p class="tn-file-name">' + esc(t.noFile) + "</p></div>";
  }
  function pickedFiles(form) {
    if (form && form._tnFiles && form._tnFiles.length) return form._tnFiles.slice();
    var input = form.querySelector("input[type=file]");
    var list = input && input.files;
    var out = [];
    if (!list) return out;
    for (var i = 0; i < list.length; i++) out.push(list[i]);
    return out;
  }
  function showFormNotice(form, msg, err) {
    setNotice(msg, !!err);
    var flashBox = root.querySelector("[data-flash]");
    if (flashBox) flashBox.innerHTML = flash();
    var nameEl = form && form.querySelector(".tn-file-name");
    if (nameEl) nameEl.textContent = msg;
  }
  function filesFromNative(rows) {
    var out = [];
    (rows || []).forEach(function (row) {
      if (!row || !row.data) return;
      var raw = atob(row.data);
      var buf = new Uint8Array(raw.length);
      for (var i = 0; i < raw.length; i++) buf[i] = raw.charCodeAt(i);
      out.push(nativeFile(buf, row.name || "document", row.type || "application/octet-stream"));
    });
    return out;
  }
  function nativeFile(buf, name, type) {
    try {
      return new File([buf], name, { type: type });
    } catch (e) {
      var blob = new Blob([buf], { type: type });
      try { blob.name = name; } catch (err) {}
      return blob;
    }
  }
  function sendPickedFiles(form, given) {
    if (!isCandidate() || form.getAttribute("data-busy") === "1") return Promise.resolve();
    var files = (given && given.length) ? given : pickedFiles(form);
    if (!files.length) {
      showFormNotice(form, t.needFile, true);
      return Promise.resolve();
    }
    form.setAttribute("data-busy", "1");
    var btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;
    setNotice(t.uploading);
    var flashBox = root.querySelector("[data-flash]");
    if (flashBox) flashBox.innerHTML = flash();
    var isAvatar = form.matches("[data-avatar]");
    var isCv = form.matches("[data-cv]");
    var fallback = isAvatar ? "photo.jpg" : "document.pdf";
    return uploadEach(files, function (file) {
      var payload = new FormData();
      api.appendFile(payload, file, fallback);
      if (form.matches("[data-doc]")) payload.append("kind", "other");
      if (isAvatar) return api.request("/users/me/avatar", { method: "POST", body: payload });
      if (isCv) return api.uploadResume(payload);
      return api.request("/documents", { method: "POST", body: payload });
    }).then(function () {
      return done(t.uploadedOk);
    }).catch(function (err) {
      form.removeAttribute("data-busy");
      if (btn) btn.disabled = false;
      showFormNotice(form, (err && err.message) || t.err, true);
    });
  }
  function formChoice(form, name) {
    var boxes = form.querySelectorAll('input[type="checkbox"][name="' + name + '"]');
    if (!boxes.length) return String(new FormData(form).get(name) || "");
    return Array.prototype.map.call(form.querySelectorAll('input[type="checkbox"][name="' + name + '"]:checked'), function (el) {
      return el.value;
    }).filter(Boolean).join(", ");
  }
  function uploadEach(files, sendOne) {
    var list = [];
    for (var i = 0; i < files.length; i++) list.push(files[i]);
    return list.reduce(function (chain, file) {
      return chain.then(function () { return sendOne(file); });
    }, Promise.resolve());
  }
  function jobOpts() {
    return state.jobOptions || {};
  }
  function loadJobOptions() {
    if (state.jobOptions) return Promise.resolve(state.jobOptions);
    return api.request("/jobs/options").then(function (json) {
      state.jobOptions = dataOf(json) || {};
      return state.jobOptions;
    }).catch(function () {
      state.jobOptions = state.jobOptions || {};
      return state.jobOptions;
    });
  }
  function jobFacts(job) {
    if (!job) return "";
    var rows = [
      [t.jobCity, job.location],
      [t.jobSector, job.sector],
      [t.contract, job.contract_type],
      [t.schedule, job.schedule],
      [t.shift, job.shift],
      [t.workMode, job.work_mode],
      [t.languages, job.languages],
      [t.overtime, job.overtime],
      [t.license, job.driver_license],
      [t.union, job.unionized],
      [t.travel, job.travel],
      [t.workAuth, job.work_authorization && job.work_authorization !== "ouvert" ? catalogLabel(jobOpts().work_requirements, job.work_authorization) : ""],
      [t.sponsorYes, job.can_sponsor ? (isEn ? "Yes" : "Oui") : ""],
      [t.salary, job.salary_display],
      [t.experienceLevel, job.experience_level],
      [t.jobEducation, job.education_required],
      [t.jobCerts, job.certifications],
      [t.jobStart, job.start_date],
      [t.jobOpenings, job.openings && job.openings > 1 ? String(job.openings) : ""],
      [t.benefits, job.benefits]
    ].filter(function (row) { return row[1]; });
    if (!rows.length) return "";
    return '<dl class="tn-facts">' + rows.map(function (row) {
      return "<div><dt>" + esc(row[0]) + "</dt><dd>" + esc(row[1]) + "</dd></div>";
    }).join("") + "</dl>";
  }
  function appTracker(app, mini) {
    var tracker = (app && app.tracker) || {};
    var steps = tracker.steps || [];
    if (!steps.length) return "";
    var html = '<ol class="tn-tracker' + (mini ? " is-mini" : "") + '"' + (mini ? ' aria-hidden="true"' : "") + ">";
    steps.forEach(function (step) {
      html += '<li class="is-' + esc(step.state || "todo") + '">';
      if (!mini) {
        html += "<b>" + esc(statusLabel(step.key)) + "</b>";
        if (step.at) html += "<span>" + esc(when(step.at)) + "</span>";
      }
      html += "</li>";
    });
    html += "</ol>";
    return html;
  }
  function personName(row) {
    return (((row && row.first_name) || "") + " " + ((row && row.last_name) || "")).trim();
  }
  function initialsOf(user) {
    user = user || state.user || {};
    var a = String(user.first_name || "").charAt(0);
    var b = String(user.last_name || "").charAt(0);
    return ((a + b) || String(user.email || "?").charAt(0)).toUpperCase();
  }
  function identityHead() {
    var u = state.user || {};
    var name = personName(u) || t.me;
    var face = window.__tlAvatarUrl
      ? '<div class="tn-avatar"><img src="' + esc(window.__tlAvatarUrl) + '" alt=""></div>'
      : '<div class="tn-avatar" aria-hidden="true">' + esc(initialsOf(u)) + "</div>";
    return '<div class="tn-identity">' + face +
      "<div><h1 class=\"tn-title\">" + esc(name) + '</h1><p class="tn-meta">' + esc(u.email || "") + "</p></div></div>";
  }
  function menuGroup(title, items) {
    return "<h2 class=\"tn-section\">" + esc(title) + "</h2>" +
      '<nav class="tn-menu">' + items.map(function (it) {
        var badge = it[2] ? '<span class="tn-menu-badge">' + esc(it[2]) + "</span>" : "";
        return '<a href="' + it[0] + '"><span>' + esc(it[1]) + "</span>" + badge +
          '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>";
      }).join("") + "</nav>";
  }
  function backTo(href) {
    return '<a class="tn-back" href="' + href + '">' + esc(t.back) + "</a>";
  }
  function statLink(href, value, label) {
    return '<a class="tn-stat" href="' + href + '"><b>' + esc(value) + "</b><span>" + esc(label) + "</span></a>";
  }
  function when(iso) {
    if (!iso) return "";
    try { return new Date(iso).toLocaleString(isEn ? "en-CA" : "fr-CA", { dateStyle: "medium", timeStyle: "short" }); }
    catch (e) { return iso; }
  }
  function money(n) {
    var v = Number(n || 0);
    return v.toLocaleString(isEn ? "en-CA" : "fr-CA") + " $";
  }
  function unreadCount() {
    return (state.notifs || []).filter(function (n) { return !n.is_read; }).length;
  }
  function nextInterview() {
    var now = Date.now();
    return (state.interviews || []).filter(function (row) {
      return row.scheduled_at && new Date(row.scheduled_at).getTime() >= now && row.status !== "CANCELLED" && row.status !== "COMPLETED" && row.status !== "NO_SHOW";
    }).sort(function (a, b) { return new Date(a.scheduled_at) - new Date(b.scheduled_at); })[0] || null;
  }
  function missingChips() {
    var missing = ((state.dash && state.dash.completeness && state.dash.completeness.missing) || []).slice(0, 4);
    var labels = {
      name: isEn ? "Name" : "Nom", phone: isEn ? "Phone" : "Téléphone", photo: isEn ? "Photo" : "Photo",
      city: t.city, title: t.title, skills: t.skills, resume: t.cv, bio: isEn ? "Summary" : "Résumé",
      experience: isEn ? "Experience" : "Expérience", availability: t.availability
    };
    if (!missing.length) return "";
    return "<p class=\"tn-meta\">" + esc(t.missing) + "</p><div class=\"tn-chips\">" +
      missing.map(function (key) { return '<span class="tn-chip">' + esc(labels[key] || key) + "</span>"; }).join("") + "</div>";
  }
  function canJoinCall(row) {
    return !!(row && (row.can_join_call || row.can_start_call));
  }
  function callActions(row) {
    if (!row || !row.in_app_call) return "";
    if (row.status === "CANCELLED" || row.status === "COMPLETED" || row.status === "NO_SHOW") {
      return '<p class="tn-meta">' + esc(row.status_label || statusLabel(row.status)) + "</p>";
    }
    if (!canJoinCall(row)) {
      return '<p class="tn-meta">' + esc(t.waitHost) + "</p>";
    }
    var audio = '<a class="tn-btn tn-btn-ghost" href="#/call/' + encodeURIComponent(row.id) + '?video=0">' + esc(t.callAudio) + "</a>";
    var video = row.call_video === false ? "" : '<a class="tn-btn" href="#/call/' + encodeURIComponent(row.id) + '?video=1">' + esc(t.callVideo) + "</a>";
    return '<div class="tn-row-actions"><p class="tn-meta">' + esc(row.can_start_call ? t.callReady : t.joinCall) + "</p>" + audio + video + "</div>";
  }
  function interviewCard() {
    var row = nextInterview();
    if (!row) return "";
    return '<div class="tn-card"><h3>' + esc(t.nextInterview) + "</h3><p class=\"tn-meta\">" +
      esc(when(row.scheduled_at) + (row.location ? " · " + row.location : "") + (row.type ? " · " + (statusLabel(row.type) || row.type_label || "") : "")) +
      "</p>" + (canJoinCall(row) ? callActions(row) : '<a class="tn-btn tn-btn-ghost" href="#/interviews">' + esc(t.seeAll) + "</a>") + "</div>";
  }

  function topBar() {
    var unread = unreadCount();
    return '<header class="tn-top"><a class="tn-brand" href="#/home">' + brandOrbit("is-sm") + "<span>Talendus</span></a>" +
      '<div class="tn-top-actions"><a class="tn-icon-btn" href="#/notifs" aria-label="' + esc(t.notifs) + '">' + icons.bell +
      (unread ? '<span class="tn-badge">' + unread + "</span>" : "") + "</a>" +
      '<a class="tn-icon-btn" href="' + telHref() + '" aria-label="' + esc(t.call) + '">' + icons.phone + "</a></div></header>";
  }
  function gateBar() {
    return "";
  }
  function tabs() {
    if (!state.user) return "";
    var r = route().name;
    if (r === "call") return "";
    var items = isEmployer() ? [
      { href: "#/home", key: "home", label: t.home, icon: icons.home },
      { href: "#/hiring", key: "hiring", label: t.hiring, icon: icons.hire },
      { href: "#/messages", key: "messages", label: t.messages, icon: icons.msg },
      { href: "#/me", key: "me", label: t.me, icon: icons.me }
    ] : [
      { href: "#/home", key: "home", label: t.home, icon: icons.home },
      { href: "#/jobs", key: "jobs", label: t.jobs, icon: icons.jobs },
      { href: "#/messages", key: "messages", label: t.messages, icon: icons.msg },
      { href: "#/me", key: "me", label: t.me, icon: icons.me }
    ];
    var msgUnread = ((state.dash && state.dash.stats && state.dash.stats.unread_messages) || 0);
    return '<nav class="tn-tabs" aria-label="Talendus">' + items.map(function (item) {
      var on = r === item.key;
      if (item.key === "jobs") on = on || r === "job";
      if (item.key === "hiring") on = on || r === "need" || r === "pipeline" || r === "inbox";
      if (item.key === "me") on = on || ["settings", "company", "apps", "app", "profile", "cv", "saved", "alerts", "interviews", "help", "invoices", "contracts", "call"].indexOf(r) !== -1;
      var badge = (item.key === "messages" && msgUnread) ? '<span class="tn-badge">' + msgUnread + "</span>" : "";
      return '<a href="' + item.href + '" class="' + (on ? "is-on" : "") + '">' + item.icon + badge + "<span>" + esc(item.label) + "</span></a>";
    }).join("") + "</nav>";
  }

  function personaKey() {
    var r = route();
    if (r.id === "employer" || r.id === "talent") return r.id;
    return getPersona() || "";
  }
  function loginHref() {
    var p = personaKey();
    return p ? "#/login/" + p : "#/login";
  }
  function registerHref() {
    var p = personaKey();
    return p ? "#/register/" + p : "#/register";
  }

  function welcomeView() {
    return '<div class="tn-gate">' +
      '<div class="tn-gate-brand">' +
      brandOrbit() +
      '<p class="tn-word">Talendus</p>' +
      '<p class="tn-tag">' + esc(t.tagline) + "</p>" +
      "</div>" +
      "<h1 class=\"tn-title tn-title-light\">" + esc(t.welcomeTitle) + "</h1>" +
      (t.welcomeLead ? '<p class="tn-lead tn-lead-light">' + esc(t.welcomeLead) + "</p>" : "") +
      '<a class="tn-persona" href="#/login/talent" data-choose="talent">' +
        '<span class="tn-persona-icon" aria-hidden="true">' + icons.talent + "</span>" +
        "<span><strong>" + esc(t.talent) + "</strong></span>" +
        '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>" +
      '<a class="tn-persona" href="#/login/employer" data-choose="employer">' +
        '<span class="tn-persona-icon" aria-hidden="true">' + icons.hire + "</span>" +
        "<span><strong>" + esc(t.employer) + "</strong></span>" +
        '<span class="tn-chevron" aria-hidden="true">' + icons.chevron + "</span></a>" +
      apkUpdateBanner() + helpLine() + langSwitch() + "</div>";
  }

  function authView() {
    var r = route();
    var persona = personaKey();
    var employer = persona === "employer";
    var backWelcome = '<a class="tn-back" href="#/welcome">' + esc(t.back) + "</a>";
    var head = '<div class="tn-gate"><div class="tn-gate-brand">' + brandOrbit("is-md") + '<p class="tn-word">Talendus</p></div><div class="tn-sheet">';
    if (r.name === "forgot") {
      return head + backWelcome.replace("#/welcome", loginHref()) +
        "<h1 class=\"tn-title\">" + esc(t.forgotTitle) + "</h1><p class=\"tn-lead\">" + esc(t.forgotLead) + "</p>" + flash() +
        '<form class="tn-form" data-forgot>' +
        "<label for=\"tn-forgot-email\">" + esc(t.email) + '</label><input id="tn-forgot-email" name="email" type="email" autocomplete="username" inputmode="email" required value="' + esc(state.authEmail || "") + '">' +
        '<button class="tn-btn" type="submit">' + esc(t.sendReset) + "</button></form>" +
        '<p class="tn-note tn-auth-alt"><a href="' + loginHref() + '">' + esc(t.login) + "</a></p>" +
        helpLine() + langSwitch() + "</div></div>";
    }
    if (r.name === "reset") {
      return head + backWelcome.replace("#/welcome", loginHref()) +
        "<h1 class=\"tn-title\">" + esc(t.resetTitle) + "</h1><p class=\"tn-lead\">" + esc(t.resetLead) + "</p>" + flash() +
        '<form class="tn-form" data-reset>' +
        '<input type="hidden" name="token" value="' + esc(r.id || "") + '">' +
        "<label for=\"tn-new-pass\">" + esc(t.newPass) + '</label><input id="tn-new-pass" name="password" type="password" required minlength="8" autocomplete="new-password">' +
        '<button class="tn-btn" type="submit">' + esc(t.resetBtn) + "</button></form>" +
        helpLine() + langSwitch() + "</div></div>";
    }
    if (r.name === "verify") {
      return head + "<h1 class=\"tn-title\">" + esc(t.verifyTitle) + "</h1>" + flash() +
        '<p class="tn-note tn-auth-alt"><a href="' + loginHref() + '">' + esc(t.login) + "</a></p>" +
        helpLine() + langSwitch() + "</div></div>";
    }
    if (r.name === "login") {
      var lead = employer ? t.loginEmployerLead : (persona === "talent" ? t.loginTalentLead : t.loginGenericLead);
      return head + backWelcome + "<h1 class=\"tn-title\">" + esc(t.login) + "</h1><p class=\"tn-lead\">" + esc(lead) + "</p>" + flash() +
        '<form class="tn-form" data-login>' +
        "<label for=\"tn-email\">" + esc(t.email) + '</label><input id="tn-email" name="email" type="email" autocomplete="username" inputmode="email" required value="' + esc(state.authEmail || "") + '">' +
        "<label for=\"tn-pass\">" + esc(t.password) + '</label><input id="tn-pass" name="password" type="password" autocomplete="current-password" required>' +
        '<button class="tn-btn" type="submit">' + esc(t.submitLogin) + "</button></form>" +
        '<p class="tn-forgot"><a class="tn-auth-link" href="#/forgot">' + esc(t.forgot) + "</a></p>" +
        '<p class="tn-note tn-auth-alt">' + esc(t.needAccount) + ' <a href="' + registerHref() + '">' + esc(t.register) + "</a></p>" +
        '<p class="tn-note">' + esc(t.switchPrompt) + ' <a href="#/welcome">' + esc(t.changeChoice) + "</a></p>" +
        helpLine() + langSwitch() + "</div></div>";
    }
    var regLead = employer ? t.registerEmployerLead : t.registerTalentLead;
    var regTitle = employer ? t.employer : t.talent;
    return head + '<a class="tn-back" href="' + loginHref() + '">' + esc(t.back) + "</a>" +
      "<h1 class=\"tn-title\">" + esc(regTitle) + "</h1><p class=\"tn-lead\">" + esc(regLead) + "</p>" + flash() +
      '<form class="tn-form" data-register data-role="' + (employer ? "EMPLOYER" : "CANDIDATE") + '">' +
      '<input class="tn-hp" name="website_url" tabindex="-1" autocomplete="off">' +
      "<label for=\"tn-first\">" + esc(t.first) + '</label><input id="tn-first" name="first_name" autocomplete="given-name" required>' +
      "<label for=\"tn-last\">" + esc(t.last) + '</label><input id="tn-last" name="last_name" autocomplete="family-name" required>' +
      "<label for=\"tn-reg-email\">" + esc(t.email) + '</label><input id="tn-reg-email" name="email" type="email" autocomplete="email" inputmode="email" required>' +
      "<label for=\"tn-reg-pass\">" + esc(t.password) + '</label><input id="tn-reg-pass" name="password" type="password" autocomplete="new-password" required minlength="8">' +
      (employer ? "<label for=\"tn-company\">" + esc(t.company) + '</label><input id="tn-company" name="company_name" autocomplete="organization" required>' : "") +
      '<button class="tn-btn" type="submit">' + esc(t.submitRegister) + "</button></form>" +
      '<p class="tn-note tn-auth-alt">' + esc(t.haveAccount) + ' <a href="' + loginHref() + '">' + esc(t.login) + "</a></p>" +
      '<p class="tn-note">' + esc(t.switchPrompt) + ' <a href="#/welcome">' + esc(t.changeChoice) + "</a></p>" +
      helpLine() + langSwitch() + "</div></div>";
  }

  function jobCard(job) {
    if (!job) return "";
    var href = "#/job/" + encodeURIComponent(job.slug || job.id);
    var loc = job.location || "";
    var pay = job.salary_display || job.salary || "";
    var hours = job.schedule || "";
    var shift = job.shift || "";
    var typ = job.contract_type || "";
    var sector = job.sector || "";
    var exp = expChip(job.experience_level);
    var facts = "";
    if (loc) facts += "<div><dt>" + esc(t.jobCity) + "</dt><dd>" + esc(loc) + "</dd></div>";
    if (pay) facts += "<div><dt>" + esc(t.salary) + "</dt><dd>" + esc(pay) + "</dd></div>";
    if (hours) facts += "<div><dt>" + esc(t.schedule) + "</dt><dd>" + esc(hours) + "</dd></div>";
    if (shift) facts += "<div><dt>" + esc(t.shift) + "</dt><dd>" + esc(shift) + "</dd></div>";
    return '<a class="tn-job-card" href="' + href + '">' +
      '<div class="tn-job-card-banner"><span class="tn-job-card-icon" aria-hidden="true">' + sectorGlyph(sector) +
      '</span><div><p class="tn-job-card-cat">' + esc(sector || t.jobs) + '</p><p class="tn-job-card-via">' +
      esc(t.viaTalendus) + "</p></div></div>" +
      '<div class="tn-job-card-body">' +
      '<div class="tn-job-card-top">' + (typ ? '<span class="tn-chip">' + esc(typ) + "</span>" : "") +
      (exp ? '<span class="tn-chip">' + esc(exp) + "</span>" : "") + "</div>" +
      "<h3>" + esc(job.title || t.jobs) + "</h3>" +
      (facts ? '<dl class="tn-job-facts-mini">' + facts + "</dl>" : "") +
      '<span class="tn-job-card-cta">' + esc(t.seeJob) + "</span></div></a>";
  }
  function expChip(raw) {
    var key = String(raw || "").toLowerCase().replace(/é/g, "e");
    if (!key) return "";
    if (key.indexOf("debut") >= 0 || key.indexOf("entry") >= 0) return isEn ? "Entry-level" : "Débutant";
    if (key.indexOf("inter") >= 0 || key.indexOf("mid") >= 0) return isEn ? "Mid-level" : "Intermédiaire";
    if (key.indexOf("senior") >= 0) return isEn ? "Senior" : "Expérimenté";
    return raw;
  }
  function sectorGlyph(sector) {
    var key = String(sector || "").toLowerCase().replace(/é/g, "e").replace(/è/g, "e");
    var path = "M4 11l8-7 8 7M6 10v9h12v-9";
    if (/entrepot|logistiq|warehouse/.test(key)) path = "M3 9l9-5 9 5v10l-9 5-9-5V9zM12 4v16";
    else if (/prod|manuf|usine/.test(key)) path = "M4 20V9l5 3V9l5 3V6l6 3v11H4z";
    else if (/transport|chauff/.test(key)) path = "M3 16h13V8H3v8zm13 0h4l3-4v4h-1M6 19a2 2 0 100-4 2 2 0 000 4zm10 0a2 2 0 100-4 2 2 0 000 4z";
    else if (/sante|health|soin/.test(key)) path = "M12 21s-7-4.4-7-10a4 4 0 017-2 4 4 0 017 2c0 5.6-7 10-7 10z";
    else if (/tech|info/.test(key)) path = "M4 6h16v10H4V6zm4 14h8";
    else if (/admin|bureau|finance/.test(key)) path = "M4 20h16V8l-8-4-8 4v12zm4-8h2m4 0h2m-8 4h2m4 0h2";
    else if (/resto|commerce|vente/.test(key)) path = "M4 10h16l-1 10H5L4 10zm4-6h8v6";
    else if (/construct|chantier/.test(key)) path = "M3 20h18M6 20V10l6-4 6 4v10M10 20v-5h4v5";
    else path = "M4 8h16v12H4V8zm4-4h8v4";
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="' + path + '"/></svg>';
  }
  function quickLinks(items) {
    return '<div class="tn-quick">' + items.map(function (it) {
      return '<a href="' + it[0] + '">' + esc(it[1]) + "</a>";
    }).join("") + "</div>";
  }

  function homeView() {
    var name = (state.user && state.user.first_name) || "";
    var dash = state.dash || {};
    var stats = dash.stats || {};
    if (isEmployer()) {
      var needs = state.hiring || [];
      return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
        flash() +
        apkUpdateBanner() +
        pushBanner() +
        '<div class="tn-stats">' +
        statLink("#/hiring", stats.active_jobs || needs.length || 0, t.hiring) +
        statLink("#/inbox", stats.applications || 0, t.presented) +
        statLink("#/interviews", stats.interviews || 0, t.interviews) +
        statLink("#/notifs", stats.unread_notifications || unreadCount(), t.notifs) +
        "</div>" +
        '<a class="tn-btn" href="#/need">' + esc(t.addNeed) + "</a>" +
        interviewCard() +
        (needs.length ? "<h2 class=\"tn-section\">" + esc(t.myNeeds) + "</h2><div class=\"tn-grid\">" +
          needs.slice(0, 3).map(function (row) {
            return '<a class="tn-job" href="#/need/' + encodeURIComponent(row.id) + '"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' +
              esc([row.location, statusLabel(row.status) || row.status_label].filter(Boolean).join(" · ")) + "</p></a>";
          }).join("") + "</div>" : "") +
        dashNotifs();
    }
    var pct = (dash.completeness && dash.completeness.percent) || 0;
    var hasCv = !!(dash.completeness && dash.completeness.checks && dash.completeness.checks.resume);
    var matches = (dash.matches || []).map(function (row) { return jobCard(row.job || row); }).join("");
    var next = "";
    if (!hasCv) {
      next = '<section class="tn-card tn-file-card"><p class="tn-kicker">' + esc(t.cv) + "</p>" +
        '<p class="tn-meta">' + esc(t.noCv) + "</p>" +
        '<form class="tn-form" data-cv>' + filePicker(CV_ACCEPT, false) +
        '<button class="tn-btn" type="submit">' + esc(t.upload) + "</button></form></section>";
    } else if (pct < 80) {
      next = '<section class="tn-card tn-file-card"><p class="tn-kicker">' + esc(t.nextStep) + "</p>" +
        '<p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
        '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
        missingChips() +
        '<a class="tn-btn" href="#/profile">' + esc(t.completeFile) + "</a></section>";
    }
    return '<p class="tn-kicker">' + esc(t.space) + "</p><h1 class=\"tn-title\">" + esc(t.hello) + (name ? " " + esc(name) : "") + "</h1>" +
      flash() + apkUpdateBanner() + pushBanner() + next + interviewCard() +
      '<div class="tn-stats">' +
      statLink("#/apps", stats.applications || 0, t.statsApps) +
      statLink("#/interviews", stats.interviews || 0, t.statsInterviews) +
      statLink("#/saved", stats.saved_jobs || (state.saved || []).length, t.savedJobs) +
      statLink("#/notifs", stats.unread_notifications || unreadCount(), t.notifs) +
      "</div>" +
      dashNotifs() +
      "<h2 class=\"tn-section\">" + esc(t.nextJob) + "</h2>" +
      '<div class="tn-grid">' + (matches || state.jobs.slice(0, 4).map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>") + "</div>" +
      '<a class="tn-text-link" href="#/jobs">' + esc(t.openJobs) + "</a>";
  }

  function dashNotifs() {
    var rows = ((state.dash && state.dash.notifications) || state.notifs || []).slice(0, 3);
    if (!rows.length) return "";
    return "<h2 class=\"tn-section\">" + esc(t.notifs) + "</h2><div class=\"tn-grid\">" + rows.map(function (n) {
      return '<button type="button" class="tn-job tn-notif' + (n.is_read ? "" : " is-unread") + '" data-open-notif="' +
        esc(n.id) + '" data-href="' + esc(n.href || "") + '"><h3>' + esc(n.title || t.notifs) +
        '</h3><p class="tn-meta">' + esc(n.message || when(n.created_at)) + "</p></button>";
    }).join("") + "</div>";
  }

  function activeJobFilterCount() {
    return [state.jobCity, state.jobSector, state.jobContract, state.jobShift, state.jobSchedule, state.jobWorkMode, state.jobExperience, state.jobTitle, state.jobAuth, state.jobSponsor]
      .filter(Boolean).length;
  }
  function jobFiltersAreOpen() {
    if (state.jobFiltersOpen == null) return activeJobFilterCount() > 0;
    return !!state.jobFiltersOpen;
  }
  function jobsGridHtml() {
    return state.jobs.map(jobCard).join("") || '<div class="tn-empty">' + esc(t.emptyJobs) + "</div>";
  }
  function jobsView() {
    var o = jobOpts();
    var filterCount = activeJobFilterCount();
    var filtersOpen = jobFiltersAreOpen();
    return "<h1 class=\"tn-title\">" + esc(t.jobs) + "</h1>" +
      '<form class="tn-search" data-search-jobs role="search">' +
      '<label class="tn-search-bar"><span class="tn-search-icon" aria-hidden="true">' + icons.search + "</span>" +
      '<input name="q" type="search" placeholder="' + esc(t.search) + '" value="' + esc(state.query || "") +
      '" enterkeyhint="search" autocomplete="off" aria-label="' + esc(t.search) + '"></label>' +
      '<button type="button" class="tn-filter-toggle' + (filterCount ? " is-on" : "") + '" data-toggle-filters aria-expanded="' +
      (filtersOpen ? "true" : "false") + '" aria-controls="tn-job-filters">' +
      esc(t.filters) + (filterCount ? " · " + filterCount : "") + "</button>" +
      '<div class="tn-filters" id="tn-job-filters"' + (filtersOpen ? "" : " hidden") + ">" +
      choiceSelect("title", o.occupations, state.jobTitle, t.occupation) +
      choiceSelect("location", o.locations, state.jobCity, t.jobCity) +
      choiceSelect("sector", o.sectors, state.jobSector, t.jobSector) +
      choiceSelect("contract_type", o.contract_types, state.jobContract, t.contract) +
      choiceSelect("shift", o.shifts, state.jobShift, t.shift) +
      choiceSelect("schedule", o.schedules, state.jobSchedule, t.schedule) +
      choiceSelect("work_mode", o.work_modes, state.jobWorkMode, t.workMode) +
      choiceSelect("experience", o.experience_levels, state.jobExperience, t.experienceLevel) +
      choiceSelect("work_authorization", o.work_requirements, state.jobAuth, t.workAuth) +
      choiceSelect("can_sponsor", o.sponsor_filters, state.jobSponsor, t.sponsorYes) +
      "</div></form>" +
      '<div class="tn-grid" data-jobs-grid>' + jobsGridHtml() + "</div>";
  }

  function existingAppForJob(job) {
    if (!job) return null;
    return (state.apps || []).find(function (a) {
      if (!a || a.status === "WITHDRAWN") return false;
      var j = a.job || {};
      return j.id === job.id || j.slug === job.slug || a.job_id === job.id;
    }) || null;
  }

  function jobView() {
    var job = state.job;
    if (!job) {
      if (route().id && !state.detailMiss) return backTo("#/jobs") + '<div class="tn-empty">' + esc(t.loading) + "</div>";
      return backTo("#/jobs") + '<div class="tn-empty">' + esc(t.notFound) + "</div>";
    }
    var full = job.description || job.qualifications || "";
    var open = !!state.jobDescOpen;
    var body = (!open && full.length > 900) ? full.slice(0, 900) + "…" : full;
    var more = (!open && full.length > 900)
      ? '<button type="button" class="tn-text-link" data-job-more>' + esc(t.readMore) + "</button>"
      : "";
    var saved = !!(job.saved || (state.saved || []).some(function (row) { return (row.id || (row.job && row.job.id)) === job.id; }));
    var existing = existingAppForJob(job);
    var applyBlock;
    if (!state.appsReady) {
      applyBlock = '<p class="tn-lead">' + esc(t.loading) + "</p>";
    } else if (existing) {
      applyBlock = '<p class="tn-lead">' + esc(t.alreadyApplied) + '</p><a class="tn-btn" href="#/app/' + encodeURIComponent(existing.id) + '">' + esc(t.viewApp) + "</a>";
    } else {
      applyBlock = '<form class="tn-form" data-apply-form data-job="' + esc(job.id) + '"><label for="tn-cover">' + esc(t.cover) + '</label><textarea id="tn-cover" name="cover_note" maxlength="4000"></textarea>' +
        '<button class="tn-btn" type="submit">' + esc(t.apply) + "</button></form>";
    }
    return '<a class="tn-back" href="#/jobs">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(job.title) + "</h1>" +
      jobFacts(job) +
      (body ? '<div class="tn-card"><p>' + esc(body) + "</p>" + more + "</div>" : "") +
      (job.benefits ? '<div class="tn-card"><p>' + esc(t.benefits) + " · " + esc(job.benefits) + "</p></div>" : "") +
      flash() + applyBlock +
      '<button type="button" class="tn-btn tn-btn-ghost" data-save-job="' + esc(job.id) + '">' + esc(saved ? t.unsaveJob : t.saveJob) + "</button>";
  }

  function messagesView() {
    var r = route();
    if (r.id) {
      var who = state.threads.concat(state.directory).find(function (p) { return String(p.user_id || p.id) === String(r.id); }) || {};
      var name = ((who.first_name || "") + " " + (who.last_name || "")).trim() || t.consultant;
      return '<a class="tn-back" href="#/messages">' + esc(t.back) + "</a><h1 class=\"tn-title\">" + esc(name) + "</h1>" +
        '<div class="tn-msg-list">' + (state.conversation.map(function (m) {
          var mine = state.user && m.sender_id === state.user.id;
          return '<div class="tn-bubble' + (mine ? " mine" : "") + '">' + esc(m.body) + "</div>";
        }).join("") || '<div class="tn-empty">' + esc(t.emptyThread) + "</div>") + "</div>" +
        '<form class="tn-composer" data-send-msg data-to="' + esc(r.id) + '"><input name="body" required placeholder="' + esc(t.write) + '" autocomplete="off"><button class="tn-btn" type="submit">' + esc(t.send) + "</button></form>";
    }
    var list = state.threads.length ? state.threads : state.directory.map(function (p) {
      return { user_id: p.id, first_name: p.first_name, last_name: p.last_name, last_message: t.consultant, unread: 0 };
    });
    return "<h1 class=\"tn-title\">" + esc(t.messages) + "</h1><p class=\"tn-lead\">" + esc(isEmployer() ? t.mediateEmployer : t.mediate) + "</p><div class=\"tn-grid\">" +
      (list.map(function (th) {
        var label = ((th.first_name || "") + " " + (th.last_name || "")).trim() || t.consultant;
        return '<a class="tn-thread" href="#/messages/' + encodeURIComponent(th.user_id) + '"><strong>' + esc(label) + "</strong><p class=\"tn-meta\">" + esc(th.last_message || "") + "</p></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyMsgs) + "</div>") + "</div>";
  }

  function hiringView() {
    return "<h1 class=\"tn-title\">" + esc(t.myNeeds) + "</h1><p class=\"tn-lead\">" + esc(t.hiringLead) + "</p>" + flash() +
      '<a class="tn-btn" href="#/need">' + esc(t.addNeed) + "</a>" +
      '<div class="tn-grid tn-stack">' + (state.hiring.map(function (row) {
        return '<a class="tn-job" href="#/need/' + encodeURIComponent(row.id) + '"><h3>' + esc(row.title) + '</h3><p class="tn-meta">' +
          esc([row.location, row.sector, row.seats ? (row.seats + " " + t.seats) : ""].filter(Boolean).join(" · ")) +
          '</p><span class="tn-status">' + esc(statusLabel(row.status) || row.status_label || "") + "</span></a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyHiring) + "</div>") + "</div>";
  }
  function needView() {
    var r = route();
    var n = r.id ? (state.need || {}) : {};
    var o = jobOpts();
    if (r.id && !state.need) {
      if (!state.detailMiss) return backTo("#/hiring") + '<div class="tn-empty">' + esc(t.loading) + "</div>";
      return backTo("#/hiring") + '<div class="tn-empty">' + esc(t.notFound) + "</div>";
    }
    return backTo("#/hiring") + "<h1 class=\"tn-title\">" + esc(r.id ? t.editNeed : t.addNeed) + "</h1><p class=\"tn-lead\">" + esc(t.needLead) + "</p>" + flash() +
      '<form class="tn-form" data-hiring' + (r.id ? ' data-id="' + esc(r.id) + '"' : "") + '>' +
      labeledChoice("title", t.needTitle, o.occupations, n.title, t.pick, true) +
      labeledChoice("location", t.location, o.locations, n.location, t.pick) +
      labeledChoice("sector", t.sector, o.sectors, n.sector, t.pick) +
      labeledChoice("contract_type", t.contract, o.contract_types, n.contract_type, t.pick) +
      labeledChoice("experience_level", t.experienceLevel, o.experience_levels, n.experience_level, t.pick) +
      labeledChoice("shift", t.shift, o.shifts, n.shift, t.pick) +
      labeledChoice("schedule", t.schedule, o.schedules, n.schedule, t.pick) +
      labeledChoice("work_mode", t.workMode, o.work_modes, n.work_mode, t.pick) +
      choiceGroup("languages", languageItems(), n.languages, t.languages) +
      labeledChoice("overtime", t.overtime, o.overtime, n.overtime, t.pick) +
      labeledChoice("driver_license", t.license, o.driver_licenses, n.driver_license, t.pick) +
      labeledChoice("unionized", t.union, o.union_status, n.unionized, t.pick) +
      labeledChoice("travel", t.travel, o.travel, n.travel, t.pick) +
      labeledChoice("work_authorization", t.workAuth, o.work_requirements, n.work_authorization || "ouvert", t.pick) +
      '<label class="tn-check"><input type="checkbox" name="can_sponsor" value="true"' + (n.can_sponsor ? " checked" : "") + "> " + esc(t.canSponsor) + "</label>" +
      "<label>" + esc(t.seats) + '</label><input name="seats" type="number" min="1" value="' + esc(n.seats || 1) + '">' +
      "<label>" + esc(t.startDate) + '</label><input name="start_date" type="date" value="' + esc(n.start_date || "") + '">' +
      "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(n.skills || "") + '">' +
      "<label>" + esc(t.salary) + '</label><input name="salary_display" value="' + esc(n.salary_display || "") + '">' +
      "<label>" + esc(t.notes) + '</label><textarea name="notes" placeholder="' + esc(t.notes) + '">' + esc(n.notes || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(r.id ? t.save : t.sendNeed) + "</button></form>";
  }

  function listBlock(title, empty, items, backHref) {
    return (backHref ? backTo(backHref) : "") + "<h1 class=\"tn-title\">" + esc(title) + "</h1>" + flash() + '<div class="tn-grid">' +
      (items && items.length ? items.join("") : '<div class="tn-empty">' + esc(empty) + "</div>") + "</div>";
  }
  function notifsView() {
    return backTo("#/home") + "<h1 class=\"tn-title\">" + esc(t.notifs) + "</h1>" + flash() +
      ((state.notifs || []).length ? '<button type="button" class="tn-btn tn-btn-ghost" data-read-all>' + esc(t.markAll) + "</button>" : "") +
      '<div class="tn-grid">' + ((state.notifs || []).map(function (n) {
        return '<button type="button" class="tn-job tn-notif' + (n.is_read ? "" : " is-unread") + '" data-open-notif="' +
          esc(n.id) + '" data-href="' + esc(n.href || "") + '"><h3>' +
          esc(n.title || t.notifs) + '</h3><p class="tn-meta">' + esc(n.message || when(n.created_at)) + "</p></button>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyNotifs) + "</div>") + "</div>";
  }
  function interviewsView() {
    return listBlock(t.interviews, t.emptyInterviews, (state.interviews || []).map(function (row) {
      var actions = callActions(row);
      if (isCandidate() && (row.status === "SCHEDULED" || !row.status)) {
        actions += '<div class="tn-row-actions"><button type="button" class="tn-btn" data-int-status="CONFIRMED" data-int-id="' +
          esc(row.id) + '">' + esc(t.confirmInterview) + '</button><button type="button" class="tn-btn tn-btn-ghost" data-int-status="CANCELLED" data-int-id="' +
          esc(row.id) + '">' + esc(t.cancelInterview) + "</button></div>";
      }
      var job = row.job || {};
      return '<div class="tn-job"><h3>' + esc(job.title || row.job_title || statusLabel(row.type) || row.type_label || t.interviews) + "</h3><p class=\"tn-meta\">" +
        esc([when(row.scheduled_at), row.location, statusLabel(row.status)].filter(Boolean).join(" · ")) + "</p>" + actions + "</div>";
    }), "#/me");
  }
  function callView() {
    return '<div class="tn-empty">' + esc(t.callConnecting) + "</div>";
  }
  function savedView() {
    return listBlock(t.savedJobs, t.emptySaved, (state.saved || []).map(function (row) {
      var job = row.job || row;
      var id = job.id || job.slug || "";
      var existing = existingAppForJob(job);
      var cta;
      if (!state.appsReady) cta = '<span class="tn-meta">' + esc(t.loading) + "</span>";
      else if (existing) cta = '<a class="tn-btn" href="#/app/' + encodeURIComponent(existing.id) + '">' + esc(t.viewApp) + "</a>";
      else cta = '<button type="button" class="tn-btn" data-apply="' + esc(id) + '">' + esc(t.apply) + "</button>";
      return '<div class="tn-saved">' + jobCard(job) +
        '<div class="tn-row-actions">' + cta + "</div></div>";
    }), "#/me");
  }
  function alertsView() {
    var o = jobOpts();
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.alerts) + "</h1>" +
      '<p class="tn-lead">' + esc(t.alertsLead) + "</p>" + flash() +
      '<form class="tn-form" data-alert><label>' + esc(t.alertKeywords) + '</label><input name="keywords" required>' +
      labeledChoice("city", t.city, o.locations, "", t.pick) +
      labeledChoice("sector", t.sector, o.sectors, "", t.pick) +
      labeledChoice("contract_type", t.contract, o.contract_types, "", t.pick) +
      '<button class="tn-btn" type="submit">' + esc(t.createAlert) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + ((state.alerts || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.keywords || row.city || t.alerts) + '</h3><p class="tn-meta">' +
          esc([row.city, row.sector, row.contract_type].filter(Boolean).join(" · ")) +
          '</p><button type="button" class="tn-btn tn-btn-ghost" data-del-alert="' + esc(row.id) + '">' + esc(t.deleteAlert) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyAlerts) + "</div>") + "</div>";
  }
  function inboxView() {
    var r = route();
    if (r.id) return inboxDetail();
    return listBlock(t.presented, t.inboxEmpty, (state.inbox || []).map(function (a) {
      var job = a.job || {};
      var cand = a.candidate || {};
      var label = personName(cand) || cand.title || t.candidate;
      return '<a class="tn-job" href="#/inbox/' + encodeURIComponent(a.id) + '"><h3>' + esc(label) +
        '</h3><p class="tn-meta">' + esc([cand.title, job.title, cand.city].filter(Boolean).join(" · ")) +
        '</p><span class="tn-status">' + esc(statusLabel(a.status || a.pipeline_stage)) + "</span></a>";
    }), "#/hiring");
  }
  function inboxDetail() {
    var a = state.application;
    var r = route();
    if (!a) {
      if (r.id && !state.detailMiss) return backTo("#/inbox") + '<div class="tn-empty">' + esc(t.loading) + "</div>";
      return backTo("#/inbox") + '<div class="tn-empty">' + esc(t.notFound) + "</div>";
    }
    var job = a.job || {};
    var cand = a.candidate || {};
    return backTo("#/inbox") + "<h1 class=\"tn-title\">" + esc(personName(cand) || t.presentedFile) + "</h1>" +
      '<p class="tn-meta">' + esc([cand.title, cand.city, job.title].filter(Boolean).join(" · ")) + "</p>" +
      '<span class="tn-status">' + esc(statusLabel(a.status)) + "</span>" + flash() +
      appTracker(a) +
      (cand.skills ? '<div class="tn-card"><p>' + esc(cand.skills) + "</p></div>" : "") +
      (a.cover_note ? '<div class="tn-card"><p>' + esc(a.cover_note) + "</p></div>" : "") +
      '<a class="tn-btn tn-btn-ghost" href="#/messages">' + esc(t.messages) + "</a>";
  }
  function pipelineView() {
    var groups = {};
    (state.inbox || []).forEach(function (a) {
      var key = a.pipeline_stage || a.status || t.presented;
      (groups[key] = groups[key] || []).push(a);
    });
    var keys = Object.keys(groups);
    if (!keys.length) return listBlock(t.pipeline, t.emptyPipeline, [], "#/hiring");
    return backTo("#/hiring") + "<h1 class=\"tn-title\">" + esc(t.pipeline) + "</h1>" + flash() + keys.map(function (key) {
      return "<h2 class=\"tn-section\">" + esc(statusLabel(key) || key) + "</h2><div class=\"tn-grid\">" + groups[key].map(function (a) {
        var job = a.job || {};
        var cand = a.candidate || {};
        var label = personName(cand) || job.title || t.presented;
        return '<a class="tn-job" href="#/inbox/' + encodeURIComponent(a.id) + '"><h3>' + esc(label) +
          '</h3><p class="tn-meta">' + esc([cand.title, job.title].filter(Boolean).join(" · ")) +
          '</p><span class="tn-status">' + esc(statusLabel(a.status || "")) + "</span></a>";
      }).join("") + "</div>";
    }).join("");
  }
  function appView() {
    var a = state.application;
    var r = route();
    if (!a) {
      if (r.id && !state.detailMiss) return backTo("#/apps") + '<div class="tn-empty">' + esc(t.loading) + "</div>";
      return backTo("#/apps") + '<div class="tn-empty">' + esc(t.notFound) + "</div>";
    }
    var job = a.job || {};
    return backTo("#/apps") + "<h1 class=\"tn-title\">" + esc(job.title || t.appDetail) + "</h1>" +
      '<p class="tn-meta">' + esc([job.location, job.shift, job.schedule, statusLabel(a.status)].filter(Boolean).join(" · ")) + "</p>" + flash() +
      appTracker(a) +
      (a.cover_note ? '<div class="tn-card"><p>' + esc(a.cover_note) + "</p></div>" : "") +
      (a.status === "WITHDRAWN" ? "" : '<button type="button" class="tn-btn tn-btn-ghost" data-withdraw="' + esc(a.id) + '">' + esc(t.withdraw) + "</button>");
  }
  function companyView() {
    var c = state.company || {};
    var o = jobOpts();
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.companyProfile) + "</h1><p class=\"tn-lead\">" + esc(t.companyLead) + "</p>" + flash() +
      '<form class="tn-form" data-company data-id="' + esc(c.id || "") + '"><label>' + esc(t.company) +
      '</label><input name="name" value="' + esc(c.name || "") + '" required>' +
      labeledChoice("city", t.city, o.locations, c.city, t.pick) +
      labeledChoice("sector", t.sector, o.sectors, c.sector, t.pick) +
      "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(c.address || "") + '">' +
      labeledChoice("country", t.country, o.countries, c.country || "Canada", t.pick) +
      "<label>" + esc(t.website) + '</label><input name="website" value="' + esc(c.website || "") + '" inputmode="url">' +
      "<label>" + esc(t.email) + '</label><input name="email" type="email" value="' + esc(c.email || "") + '">' +
      "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(c.phone || "") + '" inputmode="tel">' +
      labeledChoice("size_label", t.size, o.company_sizes, c.size_label, t.pick) +
      "<label>" + esc(t.legalName) + '</label><input name="legal_name" value="' + esc(c.legal_name || "") + '">' +
      "<label>" + esc(t.linkedin) + '</label><input name="linkedin_url" value="' + esc(c.linkedin_url || "") + '">' +
      "<label>" + esc(t.description) + '</label><textarea name="description">' + esc(c.description || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>";
  }
  function settingsView() {
    var p = state.prefs || {};
    function check(name, label, on) {
      return '<label class="tn-check"><input type="checkbox" name="' + name + '"' + (on ? " checked" : "") + "> " + esc(label) + "</label>";
    }
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.settings) + "</h1>" + flash() +
      '<div class="tn-card"><p class="tn-meta">' + esc(t.langTitle) + "</p>" + langSwitch() + "</div>" +
      '<form class="tn-form" data-password><label>' + esc(t.currentPass) + '</label><input name="current_password" type="password" required autocomplete="current-password">' +
      "<label>" + esc(t.newPass) + '</label><input name="new_password" type="password" required minlength="8" autocomplete="new-password">' +
      '<button class="tn-btn" type="submit">' + esc(t.changePass) + "</button></form>" +
      '<form class="tn-form" data-prefs><p class="tn-meta">' + esc(t.prefs) + "</p>" +
      check("notify_in_app", t.notifyApp, p.notify_in_app !== false) +
      check("notify_push", t.notifyPush, p.notify_push || pushAllowed()) +
      check("notify_email", t.notifyEmail, p.notify_email !== false) +
      check("notify_application", t.notifyApps, p.notify_application !== false) +
      check("notify_message", t.notifyMsgs, p.notify_message !== false) +
      (isCandidate() ? check("notify_match", t.notifyMatch, p.notify_match !== false) : "") +
      check("notify_interview", t.notifyInt, p.notify_interview !== false) +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>";
  }
  function invoicesView() {
    if (state.company && state.company.can_read_invoices === false) {
      return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.invoices) + "</h1>" +
        '<div class="tn-empty">' + esc(t.noBilling) + "</div>";
    }
    return listBlock(t.invoices, t.emptyInvoices, (state.invoices || []).map(function (inv) {
      var payable = inv.status === "SENT" || inv.status === "PENDING" || inv.status === "OVERDUE";
      return '<div class="tn-job"><h3>' + esc(inv.number || t.invoices) + "</h3><p class=\"tn-meta\">" +
        esc(money(inv.amount) + " · " + statusLabel(inv.status || "")) + '</p><div class="tn-row-actions">' +
        (payable ? '<button type="button" class="tn-btn" data-pay="' + esc(inv.id) + '">' + esc(t.pay) + "</button>" : "") +
        '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="invoices" data-id="' +
        esc(inv.id) + '">' + esc(t.downloadPdf) + "</button></div></div>";
    }), "#/me");
  }
  function contractsView() {
    (state.contracts || []).forEach(function (row) {
      if (row && row.id && row.sent_at && !row.opened_at && !row.signed && !row.client_signed && api.openContract) {
        api.openContract(row.id).catch(function () {});
      }
    });
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.contracts) + "</h1>" + flash() + '<div class="tn-grid">' +
      ((state.contracts || []).map(function (row) {
        var status = row.client_signed || row.signed ? t.signed : (row.opened_at ? t.clientOpened : (row.sent_at ? t.clientReceived : t.unsigned));
        var read = row.terms
          ? '<details class="tn-job"><summary>' + esc(t.readMandate) + "</summary><p class=\"tn-meta\" style=\"white-space:pre-wrap\">" + esc(row.terms) + "</p></details>"
          : "";
        return '<div class="tn-job"><h3>' + esc(row.document_name || row.type || t.contracts) + '</h3><p class="tn-meta">' +
          esc(status) + "</p>" + read +
          (row.signed || row.client_signed ? "" : '<button type="button" class="tn-btn" data-sign="' + esc(row.id) + '">' + esc(t.sign) + "</button>") +
          '<button type="button" class="tn-btn tn-btn-ghost" data-pdf="contracts" data-id="' + esc(row.id) + '">' + esc(t.downloadPdf) + "</button></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyContracts) + "</div>") + "</div>";
  }

  function appsView() {
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.apps) + "</h1><p class=\"tn-lead\">" + esc(t.appsHint) + "</p>" + flash() +
      '<div class="tn-grid">' + (state.apps.map(function (a) {
        var job = a.job || {};
        return '<a class="tn-job" href="#/app/' + encodeURIComponent(a.id) + '"><h3>' + esc(job.title || t.apps) +
          '</h3><p class="tn-meta">' + esc(job.location || "") + '</p><span class="tn-status">' + esc(statusLabel(a.status)) + "</span>" +
          appTracker(a, true) + "</a>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyApps) + "</div>") + "</div>";
  }
  function profileView() {
    var u = state.user || {};
    var p = state.profile || {};
    var resumes = p.resumes || [];
    function listBlockMini(title, rows, emptyTxt, formAttrs, fields, delAttr) {
      var items = (rows || []).map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.role || row.diploma || row.name || "") + "</h3><p class=\"tn-meta\">" +
          esc([row.company, row.school, row.issuer, row.years, row.year].filter(Boolean).join(" · ")) +
          '</p><button type="button" class="tn-btn tn-btn-ghost" ' + delAttr + '="' + esc(row.id) + '">' + esc(t.remove) + "</button></div>";
      }).join("");
      return "<h2 class=\"tn-section\">" + esc(title) + "</h2>" + (items || '<p class="tn-meta">' + esc(emptyTxt) + "</p>") +
        '<form class="tn-form" ' + formAttrs + ">" + fields + '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.add) + "</button></form>";
    }
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.profile) + "</h1><p class=\"tn-lead\">" + esc(t.profileLead) + "</p><div data-flash>" + flash() + "</div>" +
      '<form class="tn-form" data-cv><label>' + esc(t.cv) + "</label><p class=\"tn-meta\">" +
      esc(resumes.length ? (resumes[0].original_name || t.cvReady) : t.noCv) + "</p>" +
      filePicker(CV_ACCEPT, false) +
      '<button class="tn-btn" type="submit">' + esc(t.upload) + "</button></form>" +
      '<form class="tn-form" data-avatar><label>' + esc(t.photo) + '</label><p class="tn-meta">' + esc(t.photoHint) + "</p>" +
      filePicker("image/*", false) +
      '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.save) + "</button></form>" +
      '<form class="tn-form" data-profile>' +
      "<label>" + esc(t.first) + '</label><input name="first_name" value="' + esc(u.first_name || "") + '" autocomplete="given-name">' +
      "<label>" + esc(t.last) + '</label><input name="last_name" value="' + esc(u.last_name || "") + '" autocomplete="family-name">' +
      "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(u.phone || p.phone || "") + '" inputmode="tel">' +
      "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(p.address || "") + '" autocomplete="street-address">' +
      labeledChoice("city", t.city, jobOpts().locations, p.city, t.pick) +
      labeledChoice("province", t.province, jobOpts().provinces, p.province || "Québec", t.pick) +
      labeledChoice("country", t.country, jobOpts().countries, p.country || "Canada", t.pick) +
      "<label>" + esc(t.birth) + '</label><input name="birth_date" type="date" value="' + esc(p.birth_date || "") + '">' +
      labeledChoice("title", t.title, jobOpts().occupations, p.title, t.pick) +
      labeledChoice("work_status", t.workStatus, jobOpts().work_statuses, p.work_status, t.pick) +
      labeledChoice("sector", t.sector, jobOpts().sectors, p.sector, t.pick) +
      "<label>" + esc(t.experience) + '</label><input name="years_experience" type="number" min="0" value="' + esc(p.years_experience || "") + '">' +
      "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(p.skills || "") + '">' +
      choiceGroup("languages", languageItems(), p.languages, t.languages) +
      labeledChoice("availability", t.availability, jobOpts().availability, p.availability, t.pick) +
      choiceGroup("contract_type", jobOpts().contract_types, p.contract_type, t.contract) +
      choiceGroup("shift_preference", jobOpts().shifts, p.shift_preference, t.shiftPref) +
      labeledChoice("mobility", t.mobility, jobOpts().mobility, p.mobility, t.pick) +
      "<label>" + esc(t.salary) + '</label><input name="desired_salary_min" type="number" value="' + esc(p.desired_salary_min || "") + '">' +
      "<label>" + esc(t.bio) + '</label><textarea name="bio">' + esc(p.bio || "") + "</textarea>" +
      '<button class="tn-btn" type="submit">' + esc(t.save) + "</button></form>" +
      listBlockMini(t.experience, p.experiences, t.expHint, "data-exp",
        "<label>" + esc(t.companyName) + '</label><input name="company" required>' +
        "<label>" + esc(t.roleHeld) + '</label><input name="role" required>' +
        "<label>" + esc(t.years) + '</label><input name="years">', "data-del-exp") +
      listBlockMini(t.education, p.education, "", "data-edu",
        "<label>" + esc(t.school) + '</label><input name="school" required>' +
        "<label>" + esc(t.diploma) + '</label><input name="diploma">', "data-del-edu") +
      listBlockMini(t.certs, p.certifications, "", "data-cert",
        "<label>" + esc(t.certs) + '</label><input name="name" required>', "data-del-cert");
  }
  function cvView() {
    var p = state.profile || {};
    var resumes = p.resumes || [];
    var docs = state.docs || [];
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.documents) + "</h1><div data-flash>" + flash() + "</div>" +
      '<form class="tn-form" data-cv><label>' + esc(t.cv) + "</label>" +
      filePicker(CV_ACCEPT, true) +
      '<button class="tn-btn" type="submit">' + esc(t.upload) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + (resumes.map(function (r) {
        return '<div class="tn-job"><h3>' + esc(r.original_name || t.cv) + '</h3><p class="tn-meta">' +
          esc(r.is_primary ? t.cvReady : when(r.created_at)) + '</p><div class="tn-row-actions">' +
          '<button type="button" class="tn-btn" data-dl-cv="' + esc(r.id) + '">' + esc(t.downloadCv) + "</button>" +
          '<button type="button" class="tn-btn tn-btn-ghost" data-del-cv="' + esc(r.id) + '">' + esc(t.remove) + "</button></div></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.noCv) + "</div>") + "</div>" +
      '<form class="tn-form" data-doc><label>' + esc(t.otherDocs) + "</label>" +
      filePicker("", true) +
      '<button class="tn-btn tn-btn-ghost" type="submit">' + esc(t.uploadDoc) + "</button></form>" +
      '<div class="tn-grid tn-stack">' + (docs.map(function (row) {
        return '<div class="tn-job"><h3>' + esc(row.original_name || t.otherDocs) + '</h3><p class="tn-meta">' +
          esc(when(row.created_at)) + '</p><div class="tn-row-actions">' +
          '<button type="button" class="tn-btn" data-dl-doc="' + esc(row.id) + '" data-name="' + esc(row.original_name || "document") + '">' +
          esc(t.downloadCv) + "</button>" +
          '<button type="button" class="tn-btn tn-btn-ghost" data-del-doc="' + esc(row.id) + '">' + esc(t.remove) + "</button></div></div>";
      }).join("") || '<div class="tn-empty">' + esc(t.emptyDocs) + "</div>") + "</div>";
  }
  function helpView() {
    var mail = contactMail();
    var phoneBtn = hasPublicPhone()
      ? '<a class="tn-btn" href="' + telHref() + '">' + esc(t.call) + " · " + esc(state.contact.phone_display || "") + "</a>" +
        '<a class="tn-btn tn-btn-ghost" href="' + waHref() + '">' + esc(t.wa) + "</a>"
      : "";
    return backTo("#/me") + "<h1 class=\"tn-title\">" + esc(t.helpTitle) + "</h1><p class=\"tn-lead\">" + esc(t.contactUs) + "</p>" +
      '<div class="tn-help-actions">' + phoneBtn +
      '<a class="tn-btn' + (phoneBtn ? " tn-btn-ghost" : "") + '" href="mailto:' + esc(mail) + '">' + esc(t.emailUs) + " · " + esc(mail) + "</a></div>";
  }
  function meView() {
    var html = identityHead() + flash();
    if (isCandidate()) {
      var pct = ((state.dash && state.dash.completeness && state.dash.completeness.percent) || 0);
      html += '<p class="tn-meta">' + esc(t.completeness) + " · " + pct + "%</p>" +
        '<div class="tn-progress"><span style="width:' + pct + '%"></span></div>' +
        menuGroup(t.groupFile, [["#/profile", t.profile], ["#/cv", t.documents], ["#/apps", t.apps, state.apps.length || ""], ["#/saved", t.savedJobs], ["#/alerts", t.alerts]]) +
        menuGroup(t.groupFollow, [["#/interviews", t.interviews], ["#/notifs", t.notifs, unreadCount() || ""], ["#/messages", t.messages]]) +
        menuGroup(t.groupAccount, [["#/settings", t.settings], ["#/help", t.helpTitle]]);
    } else {
      var stats = (state.dash && state.dash.stats) || {};
      html += '<p class="tn-meta">' + esc((state.dash && state.dash.company_name) || "") + "</p>" +
        menuGroup(t.groupHire, [["#/need", t.addNeed], ["#/hiring", t.myNeeds, (state.hiring || []).length || ""], ["#/inbox", t.presented, stats.applications || ""], ["#/pipeline", t.pipeline], ["#/interviews", t.interviews]]) +
        menuGroup(t.groupCompany, (function () {
          var items = [["#/company", t.companyProfile], ["#/contracts", t.contracts]];
          if (!state.company || state.company.can_read_invoices !== false) items.push(["#/invoices", t.invoices]);
          return items;
        })()) +
        menuGroup(t.groupAccount, [["#/settings", t.settings], ["#/help", t.helpTitle]]);
    }
    html += '<p class="tn-note">' + esc(t.switchPrompt) + ' <a href="#/welcome">' + esc(t.changeChoice) + "</a></p>";
    html += '<button class="tn-btn tn-btn-ghost tn-logout" data-logout>' + esc(t.logout) + "</button>";
    return html;
  }

  function screenHtml() {
    var name = route().name;
    if (!state.user) {
      if (["login", "register", "forgot", "reset", "verify"].indexOf(name) !== -1) return authView();
      return welcomeView();
    }
    if (isCandidate()) {
      if (name === "jobs") return jobsView();
      if (name === "job") return jobView();
      if (name === "messages") return messagesView();
      if (name === "notifs") return notifsView();
      if (name === "interviews") return interviewsView();
      if (name === "call") return callView();
      if (name === "saved") return savedView();
      if (name === "alerts") return alertsView();
      if (name === "apps") return appsView();
      if (name === "app") return appView();
      if (name === "profile") return profileView();
      if (name === "cv") return cvView();
      if (name === "help") return helpView();
      if (name === "settings") return settingsView();
      if (name === "me") return meView();
      return homeView();
    }
    if (name === "hiring") return hiringView();
    if (name === "need") return needView();
    if (name === "messages") return messagesView();
    if (name === "notifs") return notifsView();
    if (name === "interviews") return interviewsView();
    if (name === "call") return callView();
    if (name === "inbox") return inboxView();
    if (name === "pipeline") return pipelineView();
    if (name === "invoices") return invoicesView();
    if (name === "contracts") return contractsView();
    if (name === "company") return companyView();
    if (name === "settings") return settingsView();
    if (name === "help") return helpView();
    if (name === "me") return meView();
    return homeView();
  }

  function render() {
    document.body.classList.toggle("tn-gated", !state.user);
    var chrome = state.user ? topBar() : gateBar();
    root.innerHTML = chrome + '<main id="tn-screen" class="tn-screen">' + screenHtml() + "</main>" + tabs();
  }

  var FRESH_MS = 25000;
  var fetchedAt = {};
  function isFresh(key) {
    return !!(fetchedAt[key] && (Date.now() - fetchedAt[key]) < FRESH_MS);
  }
  function stamp(key) {
    fetchedAt[key] = Date.now();
  }
  function bustCache(keys) {
    if (!keys) { fetchedAt = {}; return; }
    keys.forEach(function (k) { delete fetchedAt[k]; });
  }
  function pull(key, runner, field, asList) {
    if (isFresh(key) && state[field] != null) {
      if (field === "apps") state.appsReady = true;
      return Promise.resolve();
    }
    return runner().then(function (json) {
      var value = dataOf(json);
      state[field] = asList ? (value || []) : value;
      if (field === "apps") state.appsReady = true;
      stamp(key);
    }).catch(function () {
      if (state[field] == null) state[field] = asList ? [] : null;
      if (field === "apps") state.appsReady = true;
    });
  }

  function loadJobs(q) {
    var extra = arguments[1] || {};
    if (q != null) state.query = q || "";
    if (extra.location != null) state.jobCity = extra.location;
    if (extra.sector != null) state.jobSector = extra.sector;
    if (extra.contract_type != null) state.jobContract = extra.contract_type;
    if (extra.shift != null) state.jobShift = extra.shift;
    if (extra.schedule != null) state.jobSchedule = extra.schedule;
    if (extra.work_mode != null) state.jobWorkMode = extra.work_mode;
    if (extra.experience != null) state.jobExperience = extra.experience;
    if (extra.title != null) state.jobTitle = extra.title;
    if (extra.work_authorization != null) state.jobAuth = extra.work_authorization;
    if (extra.can_sponsor != null) state.jobSponsor = extra.can_sponsor;
    var key = "jobs:" + [state.query, state.jobCity, state.jobSector, state.jobContract, state.jobShift, state.jobSchedule, state.jobWorkMode, state.jobExperience, state.jobTitle, state.jobAuth, state.jobSponsor].join(":");
    if (isFresh(key) && state.jobs && state.jobs.length) return Promise.resolve();
    return api.jobs({
      q: state.query || "",
      location: state.jobCity || "",
      sector: state.jobSector || "",
      contract_type: state.jobContract || "",
      shift: state.jobShift || "",
      schedule: state.jobSchedule || "",
      work_mode: state.jobWorkMode || "",
      experience: state.jobExperience || "",
      title: state.jobTitle || "",
      work_authorization: state.jobAuth || "",
      can_sponsor: state.jobSponsor === "true" || state.jobSponsor === true ? true : "",
      page_size: 20,
      sort: "published_at"
    }).then(function (json) {
      state.jobs = dataOf(json) || [];
      stamp(key);
    }).catch(function () { state.jobs = []; });
  }
  var jobSearchTimer = 0;
  function readJobSearch(form) {
    var fd = new FormData(form);
    return {
      q: fd.get("q") != null ? fd.get("q") : state.query,
      extra: {
        location: fd.get("location") != null ? fd.get("location") : state.jobCity,
        sector: fd.get("sector") != null ? fd.get("sector") : state.jobSector,
        contract_type: fd.get("contract_type") != null ? fd.get("contract_type") : state.jobContract,
        shift: fd.get("shift") != null ? fd.get("shift") : state.jobShift,
        schedule: fd.get("schedule") != null ? fd.get("schedule") : state.jobSchedule,
        work_mode: fd.get("work_mode") != null ? fd.get("work_mode") : state.jobWorkMode,
        experience: fd.get("experience") != null ? fd.get("experience") : state.jobExperience,
        title: fd.get("title") != null ? fd.get("title") : state.jobTitle,
        work_authorization: fd.get("work_authorization") != null ? fd.get("work_authorization") : state.jobAuth,
        can_sponsor: fd.get("can_sponsor") != null ? fd.get("can_sponsor") : state.jobSponsor
      }
    };
  }
  function paintJobResults() {
    var grid = root.querySelector("[data-jobs-grid]");
    var toggle = root.querySelector("[data-toggle-filters]");
    if (toggle) {
      var count = activeJobFilterCount();
      toggle.classList.toggle("is-on", !!count);
      toggle.textContent = t.filters + (count ? " · " + count : "");
    }
    if (grid && route().name === "jobs") {
      grid.innerHTML = jobsGridHtml();
      return;
    }
    render();
  }
  function runJobSearch(form) {
    if (!form || !isCandidate()) return Promise.resolve();
    var spec = readJobSearch(form);
    return loadJobs(spec.q, spec.extra).then(paintJobResults);
  }
  function scheduleJobSearch(form) {
    clearTimeout(jobSearchTimer);
    jobSearchTimer = setTimeout(function () { runJobSearch(form); }, 280);
  }

  function loadSessionData() {
    state.user = api.currentUser();
    if (!state.user) {
      state.dash = null;
      bustCache();
      return Promise.resolve();
    }
    var name = route().name;
    var tasks = [];
    function need(key, runner, field, asList) {
      tasks.push(pull(key, runner, field, asList));
    }
    need("prefs", function () { return api.request("/users/me/preferences"); }, "prefs", false);
    need("notifs", function () { return api.notifications(); }, "notifs", true);
    if (isCandidate()) {
      if (name === "home" || name === "me" || name === "apps") {
        need("candDash", function () { return api.request("/candidates/me/dashboard"); }, "dash", false);
      }
      if (name === "me" || name === "profile" || name === "cv") {
        need("profile", function () { return api.profile(); }, "profile", false);
      }
      if (name === "cv") {
        need("docs", function () { return api.request("/documents"); }, "docs", true);
      }
      if (name === "me" || name === "apps" || name === "app" || name === "job" || name === "saved") {
        need("apps", function () { return api.myApplications(); }, "apps", true);
      }
      if (name === "saved" || name === "job") {
        need("saved", function () { return api.request("/jobs/saved"); }, "saved", true);
      }
      if (name === "alerts") need("alerts", function () { return api.request("/alerts"); }, "alerts", true);
      if (name === "interviews" || name === "home" || name === "call") {
        need("interviews", function () { return api.request("/interviews"); }, "interviews", true);
      }
    } else if (isEmployer()) {
      if (name === "home" || name === "me") {
        need("empDash", function () { return api.request("/companies/me/dashboard"); }, "dash", false);
      }
      if (name === "home" || name === "hiring" || name === "need" || name === "me") {
        need("hiring", function () { return api.request("/hiring-requests"); }, "hiring", true);
      }
      if (name === "inbox" || name === "pipeline") {
        need("inbox", function () { return api.request("/applications"); }, "inbox", true);
      }
      if (name === "invoices") need("invoices", function () { return api.request("/invoices"); }, "invoices", true);
      if (name === "contracts") need("contracts", function () { return api.request("/contracts"); }, "contracts", true);
      if (name === "company" || name === "me" || name === "invoices") need("company", function () { return api.request("/companies/me"); }, "company", false);
      if (name === "interviews" || name === "home" || name === "call") {
        need("interviews", function () { return api.request("/interviews"); }, "interviews", true);
      }
    }
    if (name === "messages") {
      need("threads", function () { return api.request("/messages"); }, "threads", true);
      need("directory", function () { return api.request("/messages/directory"); }, "directory", true);
    }
    return Promise.all(tasks).then(function () {
      quietPushSync();
    });
  }

  function syncHash() {
    var r = route();
    if (!allowedRoute(r.name)) {
      var fallback = state.user ? "#/home" : "#/welcome";
      if ((location.hash || "") !== fallback) {
        location.replace(fallback);
        return false;
      }
      return true;
    }
    var wanted = "#/" + r.name + (r.id ? "/" + r.id : "");
    var rawHash = location.hash || "";
    var qAt = rawHash.indexOf("?");
    if (qAt >= 0) wanted += rawHash.slice(qAt);
    var raw = (location.hash || "").replace(/^#\/?/, "").split("/")[0];
    if (state.user && raw && raw !== r.name && raw !== "welcome") {
      location.replace(wanted);
      return false;
    }
    return true;
  }

  function loadRoute() {
    state.user = api.currentUser();
    if (route().name !== "job") state.jobDescOpen = false;
    if (!syncHash()) return Promise.resolve();
    var r = route();
    function sameId(obj, id) {
      if (!obj || !id) return false;
      return String(obj.id) === String(id) || String(obj.slug) === String(id);
    }
    if (r.name === "job" && r.id && !sameId(state.job, r.id)) { state.job = null; state.detailMiss = false; }
    if (r.name === "app" && r.id && !sameId(state.application, r.id)) { state.application = null; state.detailMiss = false; }
    if (r.name === "inbox" && r.id && !sameId(state.application, r.id)) { state.application = null; state.detailMiss = false; }
    if (r.name === "need" && r.id && !sameId(state.need, r.id)) { state.need = null; state.detailMiss = false; }
    render();
    var pending = [loadSessionData(), loadJobOptions()];
    if (state.user && isCandidate() && (r.name === "home" || r.name === "jobs")) {
      var haveMatches = !!(state.dash && (state.dash.matches || []).length);
      if (r.name === "jobs" || !haveMatches) pending.push(loadJobs(state.query));
    }
    if (state.user && isCandidate() && r.name === "job" && r.id) {
      pending.push(api.request("/jobs/" + encodeURIComponent(r.id)).then(function (json) { state.job = dataOf(json); state.detailMiss = !state.job; }).catch(function () { state.job = null; state.detailMiss = true; }));
    }
    if (state.user && isCandidate() && r.name === "app" && r.id) {
      pending.push(api.request("/applications/" + encodeURIComponent(r.id)).then(function (json) { state.application = dataOf(json); state.detailMiss = !state.application; }).catch(function () { state.application = null; state.detailMiss = true; }));
    }
    if (state.user && isEmployer() && r.name === "inbox" && r.id) {
      pending.push(api.request("/applications/" + encodeURIComponent(r.id)).then(function (json) { state.application = dataOf(json); state.detailMiss = !state.application; }).catch(function () { state.application = null; state.detailMiss = true; }));
    }
    if (state.user && isEmployer() && r.name === "need" && r.id) {
      pending.push(api.request("/hiring-requests/" + encodeURIComponent(r.id)).then(function (json) { state.need = dataOf(json); state.detailMiss = !state.need; }).catch(function () { state.need = null; state.detailMiss = true; }));
    }
    if (state.user && r.name === "settings") {
      pending.push(api.request("/users/me/preferences").then(function (json) { state.prefs = dataOf(json) || {}; }).catch(function () { state.prefs = {}; }));
    }
    if (state.user && isEmployer() && r.name === "company") {
      pending.push(api.request("/companies/me").then(function (json) { state.company = dataOf(json); }).catch(function () { state.company = null; }));
    }
    if (state.user && r.name === "messages" && r.id) {
      pending.push(api.request("/messages/" + encodeURIComponent(r.id)).then(function (json) { state.conversation = dataOf(json) || []; }).catch(function () { state.conversation = []; }));
    }
    if (!state.user && r.name === "verify" && r.id) {
      pending.push(api.verifyEmail(r.id).then(function () { clearAuthToken("verify"); setNotice(t.verifyOk); }).catch(fail));
    }
    return Promise.all(pending).then(function () {
      if (!localeChosen() && !storedLocale() && state.prefs && state.prefs.locale) {
        var prefEn = String(state.prefs.locale).toLowerCase().indexOf("en") === 0;
        if (!(prefEn && !pageIsEn())) applyLocale(state.prefs.locale, false);
      }
      if (!syncHash()) return;
      render();
      syncCallScreen();
    }).catch(function () { render(); });
  }

  function afterAuth() {
    return hydrateSession().then(function () {
      var user = api.currentUser();
      if (!user) {
        fail({ message: t.sessionLost });
        return;
      }
      var chosen = getPersona();
      state.mismatch = "";
      state.authEmail = "";
      if (chosen === "talent" && isEmployer(user)) state.mismatch = t.wrongPersonaEmployer;
      if (chosen === "employer" && isCandidate(user)) state.mismatch = t.wrongPersonaTalent;
      setPersona(isEmployer(user) ? "employer" : "talent");
      setNotice("");
      applyLocale(isEn ? "en-CA" : "fr-CA", true);
      go("#/home");
      enablePush(true);
      return loadRoute();
    });
  }

  function hydrateSession() {
    if (!api.currentUser()) return Promise.resolve();
    return api.me().then(function (json) {
      var user = dataOf(json);
      if (!user) return;
      state.user = user;
      if (staffRole(user.role)) {
        location.replace("/admin/");
        return new Promise(function () {});
      }
      setPersona(user.role === "EMPLOYER" ? "employer" : "talent");
      syncNativeAuth();
    }).catch(function () {});
  }

  function fail(err) {
    var msg = (err && err.code === "NETWORK") ? t.networkErr : ((err && err.message) || t.err);
    setNotice(msg, true);
    render();
  }
  function done(msg) {
    setNotice(msg || "");
    bustCache();
    return loadRoute();
  }

  root.addEventListener("click", function (e) {
    var locBtn = e.target.closest("[data-locale]");
    if (locBtn) {
      e.preventDefault();
      applyLocale(locBtn.getAttribute("data-locale"), !!state.user, true);
      render();
      return;
    }
    var nativePick = e.target.closest("[data-native-pick]");
    if (nativePick) {
      e.preventDefault();
      if (!hasNativePicker()) return;
      var form = nativePick.closest("form");
      if (!form) return;
      var id = "p" + Date.now() + "-" + Math.floor(Math.random() * 10000);
      window.__tnNativeForms = window.__tnNativeForms || {};
      window.__tnNativeForms[id] = form;
      var kind = form.matches("[data-cv]") ? "cv" : (form.matches("[data-doc]") ? "doc" : (form.matches("[data-avatar]") ? "avatar" : ""));
      var token = "";
      try { token = localStorage.getItem("talendus_access_token") || ""; } catch (e) {}
      nativePick.disabled = true;
      try {
        window.TalendusNative.openDocumentPicker(
          id,
          nativePick.getAttribute("data-multiple") === "1" ? 1 : 0,
          nativePick.getAttribute("data-images") === "1" ? 1 : 0,
          kind,
          token
        );
      } catch (err) {
        nativePick.disabled = false;
        var input = form.querySelector(".tn-file-input");
        if (input) input.click();
        else showFormNotice(form, t.err, true);
      }
      return;
    }
    if (e.target.closest("[data-enable-push]")) {
      e.preventDefault();
      enablePush(true).then(function (ok) {
        if (ok) setNotice(t.pushOn);
        render();
      }).catch(fail);
      return;
    }
    var filterToggle = e.target.closest("[data-toggle-filters]");
    if (filterToggle) {
      e.preventDefault();
      state.jobFiltersOpen = !jobFiltersAreOpen();
      render();
      return;
    }
    var pickOpen = e.target.closest("[data-pick-open]");
    if (pickOpen) {
      e.preventDefault();
      var wrap = pickOpen.closest(".tn-pick");
      var input = wrap && wrap.querySelector("input");
      var listName = pickOpen.getAttribute("data-pick-list") || "occupations";
      openPickSheet(
        input,
        jobOpts()[listName] || jobOpts().occupations || [],
        pickOpen.getAttribute("data-pick-empty") || t.anyChoice,
        pickOpen.hasAttribute("data-pick-required")
      );
      return;
    }
    var choose = e.target.closest("[data-choose]");
    if (choose) setPersona(choose.getAttribute("data-choose"));
    var applyBtn = e.target.closest("[data-apply]");
    if (applyBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.apply({ job_id: applyBtn.getAttribute("data-apply") }).then(function () { done(t.applied); }).catch(function (err) {
        if (err && err.code === "APPLICATION_ALREADY_EXISTS") { done(t.alreadyApplied); return; }
        fail(err);
      });
    }
    var moreBtn = e.target.closest("[data-job-more]");
    if (moreBtn) {
      e.preventDefault();
      state.jobDescOpen = true;
      render();
      return;
    }
    var saveBtn = e.target.closest("[data-save-job]");
    if (saveBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      var jobId = saveBtn.getAttribute("data-save-job");
      var already = (state.saved || []).some(function (row) { return String(row.id || (row.job && row.job.id)) === String(jobId); });
      (already ? api.unsaveJob(jobId) : api.saveJob(jobId)).then(function () { done(already ? t.removed : t.saved); }).catch(fail);
    }
    var withdraw = e.target.closest("[data-withdraw]");
    if (withdraw) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/applications/" + withdraw.getAttribute("data-withdraw") + "/withdraw", { method: "POST" })
        .then(function () { done(t.withdrawn); }).catch(fail);
    }
    var delAlert = e.target.closest("[data-del-alert]");
    if (delAlert) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/alerts/" + delAlert.getAttribute("data-del-alert"), { method: "DELETE" })
        .then(function () { done(t.removed); }).catch(fail);
    }
    var readOne = e.target.closest("[data-read-notif]");
    if (readOne) {
      e.preventDefault();
      api.request("/notifications/" + readOne.getAttribute("data-read-notif") + "/read", { method: "POST" })
        .then(function () { return loadRoute(); }).catch(fail);
    }
    var openNotif = e.target.closest("[data-open-notif]");
    if (openNotif) {
      e.preventDefault();
      var href = openNotif.getAttribute("data-href") || "";
      var dest = portalHash(href);
      var nid = openNotif.getAttribute("data-open-notif");
      var jump = function () { go(dest); loadRoute(); };
      if (nid) api.request("/notifications/" + nid + "/read", { method: "POST" }).then(jump).catch(jump);
      else jump();
    }
    if (e.target.closest("[data-read-all]")) {
      e.preventDefault();
      api.request("/notifications/read-all", { method: "POST" }).then(function () {
        bustCache(["notifs"]);
        return loadRoute();
      }).catch(fail);
    }
    var intBtn = e.target.closest("[data-int-status]");
    if (intBtn) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/interviews/" + intBtn.getAttribute("data-int-id") + "/status", {
        method: "POST",
        body: { status: intBtn.getAttribute("data-int-status") }
      }).then(function () { done(t.interviewUpdated); }).catch(fail);
    }
    var signBtn = e.target.closest("[data-sign]");
    if (signBtn) {
      e.preventDefault();
      if (!isEmployer()) return;
      var signer = ((state.user.first_name || "") + " " + (state.user.last_name || "")).trim();
      api.signContract(signBtn.getAttribute("data-sign"), { signer_name: signer, accepted: true })
        .then(function () { done(t.signed); }).catch(fail);
    }
    var pdfBtn = e.target.closest("[data-pdf]");
    if (pdfBtn) {
      e.preventDefault();
      var kind = pdfBtn.getAttribute("data-pdf");
      var id = pdfBtn.getAttribute("data-id");
      api.download("/" + kind + "/" + id + "/pdf", kind === "invoices" ? "facture.pdf" : "mandat.pdf")
        .then(function () { setNotice(t.fileSaved); }).catch(fail);
    }
    var payBtn = e.target.closest("[data-pay]");
    if (payBtn) {
      e.preventDefault();
      if (!isEmployer()) return;
      api.request("/invoices/" + payBtn.getAttribute("data-pay") + "/checkout", { method: "POST" }).then(function (json) {
        var url = json && json.data && json.data.checkout_url;
        if (url) location.assign(url);
        else fail({ message: t.err });
      }).catch(fail);
    }
    var delRow = e.target.closest("[data-del-exp], [data-del-edu], [data-del-cert]");
    if (delRow) {
      e.preventDefault();
      if (!isCandidate()) return;
      var kind = delRow.hasAttribute("data-del-exp") ? "experiences" : (delRow.hasAttribute("data-del-edu") ? "education" : "certifications");
      var rid = delRow.getAttribute("data-del-exp") || delRow.getAttribute("data-del-edu") || delRow.getAttribute("data-del-cert");
      api.request("/candidates/me/" + kind + "/" + rid, { method: "DELETE" }).then(function () { done(t.removed); }).catch(fail);
    }
    var delCv = e.target.closest("[data-del-cv]");
    if (delCv) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/resume/" + delCv.getAttribute("data-del-cv"), { method: "DELETE" }).then(function () { done(t.removed); }).catch(fail);
    }
    var dlCv = e.target.closest("[data-dl-cv]");
    if (dlCv) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.download("/candidates/resumes/" + dlCv.getAttribute("data-dl-cv") + "/file", "cv.pdf")
        .then(function () { setNotice(t.fileSaved); }).catch(fail);
    }
    var delDoc = e.target.closest("[data-del-doc]");
    if (delDoc) {
      e.preventDefault();
      api.request("/documents/" + delDoc.getAttribute("data-del-doc"), { method: "DELETE" }).then(function () { done(t.removed); }).catch(fail);
    }
    var dlDoc = e.target.closest("[data-dl-doc]");
    if (dlDoc) {
      e.preventDefault();
      api.download("/documents/" + dlDoc.getAttribute("data-dl-doc") + "/file", dlDoc.getAttribute("data-name") || "document")
        .then(function () { setNotice(t.fileSaved); }).catch(fail);
    }
    if (e.target.closest("[data-logout]")) {
      e.preventDefault();
      api.logout().then(function () {
        state.user = null;
        state.mismatch = "";
        bustCache();
        setPersona("");
        setNotice("");
        go("#/welcome");
        loadRoute();
      });
    }
  });

  root.addEventListener("submit", function (e) {
    var form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.matches("[data-search-jobs]")) {
      e.preventDefault();
      clearTimeout(jobSearchTimer);
      runJobSearch(form);
    } else if (form.matches("[data-login]")) {
      e.preventDefault();
      var loginData = new FormData(form);
      var loginEmail = String(loginData.get("email") || "").trim();
      var loginBtn = form.querySelector("button[type=submit]");
      state.authEmail = loginEmail;
      if (loginBtn) loginBtn.disabled = true;
      api.login(loginEmail, loginData.get("password")).then(afterAuth).catch(function (err) {
        if (loginBtn) loginBtn.disabled = false;
        fail(err);
      });
    } else if (form.matches("[data-forgot]")) {
      e.preventDefault();
      var forgotEmail = String(new FormData(form).get("email") || "").trim();
      state.authEmail = forgotEmail;
      if (!forgotEmail) { fail({ message: t.forgotNeedEmail }); return; }
      api.forgotPassword(forgotEmail).then(function () { setNotice(t.forgotSent); render(); }).catch(fail);
    } else if (form.matches("[data-reset]")) {
      e.preventDefault();
      var resetData = Object.fromEntries(new FormData(form).entries());
      if (!resetData.token || !resetData.password) { fail({ message: t.err }); return; }
      api.resetPassword(resetData.token, resetData.password).then(function () {
        clearAuthToken("reset");
        setNotice(t.passwordUpdated);
        go(loginHref());
        return loadRoute();
      }).catch(fail);
    } else if (form.matches("[data-apply-form]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var cover = (new FormData(form).get("cover_note") || "").trim();
      var payload = { job_id: form.getAttribute("data-job") };
      if (cover) payload.cover_note = cover;
      api.apply(payload).then(function () { done(t.applied); }).catch(function (err) {
        if (err && err.code === "APPLICATION_ALREADY_EXISTS") { done(t.alreadyApplied); go("#/apps"); return loadRoute(); }
        fail(err);
      });
    } else if (form.matches("[data-alert]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/alerts", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-register]")) {
      e.preventDefault();
      var data = Object.fromEntries(new FormData(form).entries());
      data.role = form.getAttribute("data-role") || (getPersona() === "employer" ? "EMPLOYER" : "CANDIDATE");
      api.register(data).then(afterAuth).catch(fail);
    } else if (form.matches("[data-send-msg]")) {
      e.preventDefault();
      if (!state.user) return;
      api.request("/messages", { method: "POST", body: { recipient_id: form.getAttribute("data-to"), body: new FormData(form).get("body") } }).then(function () {
        form.reset();
        loadRoute();
      }).catch(fail);
    } else if (form.matches("[data-hiring]")) {
      e.preventDefault();
      if (!isEmployer()) return;
      var hire = Object.fromEntries(new FormData(form).entries());
      hire.languages = formChoice(form, "languages");
      hire.can_sponsor = !!(form.can_sponsor && form.can_sponsor.checked);
      if (hire.seats) hire.seats = Number(hire.seats) || 1;
      var hid = form.getAttribute("data-id");
      var req = hid
        ? api.request("/hiring-requests/" + hid, { method: "PATCH", body: hire })
        : api.request("/hiring-requests", { method: "POST", body: hire });
      req.then(function () {
        setNotice(hid ? t.saved : t.needSent);
        bustCache();
        go("#/hiring");
        return loadRoute();
      }).catch(fail);
    } else if (form.matches("[data-profile]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      var d = Object.fromEntries(new FormData(form).entries());
      d.languages = formChoice(form, "languages");
      d.contract_type = formChoice(form, "contract_type");
      d.shift_preference = formChoice(form, "shift_preference");
      Promise.all([
        api.request("/users/me", { method: "PATCH", body: { first_name: d.first_name, last_name: d.last_name, phone: d.phone } }),
        api.updateProfile({
          city: d.city, province: d.province, country: d.country, address: d.address, birth_date: d.birth_date,
          title: d.title, sector: d.sector, skills: d.skills,
          bio: d.bio, languages: d.languages, availability: d.availability, contract_type: d.contract_type,
          mobility: d.mobility, shift_preference: d.shift_preference, work_status: d.work_status,
          years_experience: d.years_experience ? Number(d.years_experience) : null,
          desired_salary_min: d.desired_salary_min ? Number(d.desired_salary_min) : null
        })
      ]).then(function () { return api.me(); }).then(function (json) {
        var user = dataOf(json);
        if (user) state.user = user;
        done(t.saved);
      }).catch(fail);
    } else if (form.matches("[data-avatar]") || form.matches("[data-cv]") || form.matches("[data-doc]")) {
      e.preventDefault();
      sendPickedFiles(form);
    } else if (form.matches("[data-exp]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/experiences", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-edu]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/education", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-cert]")) {
      e.preventDefault();
      if (!isCandidate()) return;
      api.request("/candidates/me/certifications", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-password]")) {
      e.preventDefault();
      api.request("/auth/change-password", { method: "POST", body: Object.fromEntries(new FormData(form).entries()) })
        .then(function () { form.reset(); done(t.saved); }).catch(fail);
    } else if (form.matches("[data-prefs]")) {
      e.preventDefault();
      var prefs = {
        notify_in_app: !!(form.notify_in_app && form.notify_in_app.checked),
        notify_email: !!(form.notify_email && form.notify_email.checked),
        notify_application: !!(form.notify_application && form.notify_application.checked),
        notify_message: !!(form.notify_message && form.notify_message.checked),
        notify_interview: !!(form.notify_interview && form.notify_interview.checked),
        notify_push: !!(form.notify_push && form.notify_push.checked)
      };
      if (form.notify_match) prefs.notify_match = !!form.notify_match.checked;
      api.request("/users/me/preferences", { method: "PATCH", body: prefs }).then(function () {
        return prefs.notify_push ? enablePush(true) : disablePush();
      }).then(function () { done(t.saved); }).catch(fail);
    } else if (form.matches("[data-company]")) {
      e.preventDefault();
      if (!isEmployer()) return;
      var cid = form.getAttribute("data-id");
      if (!cid) return;
      var body = Object.fromEntries(new FormData(form).entries());
      if (!body.email) delete body.email;
      api.request("/companies/" + cid, { method: "PATCH", body: body })
        .then(function () { done(t.saved); }).catch(fail);
    }
  });

  root.addEventListener("input", function (e) {
    var form = e.target.closest("[data-search-jobs]");
    if (!form || e.target.name !== "q") return;
    scheduleJobSearch(form);
  });
  root.addEventListener("change", function (e) {
    var fileInput = e.target.closest(".tn-file-input");
    if (fileInput) {
      var box = fileInput.closest(".tn-file");
      var nameEl = box && box.querySelector(".tn-file-name");
      var files = fileInput.files || [];
      if (nameEl) {
        if (!files.length) nameEl.textContent = t.noFile;
        else if (files.length === 1) nameEl.textContent = files[0].name;
        else nameEl.textContent = files.length + " " + t.filesChosen;
      }
      var form = fileInput.closest("form");
      if (form && files.length && (form.matches("[data-cv]") || form.matches("[data-doc]") || form.matches("[data-avatar]"))) {
        sendPickedFiles(form);
      }
      return;
    }
    var form = e.target.closest("[data-search-jobs]");
    if (!form || e.target.name === "q") return;
    clearTimeout(jobSearchTimer);
    runJobSearch(form);
  });
  root.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    var input = e.target.closest("[data-search-jobs] input[name='q']");
    if (!input || !input.form) return;
    e.preventDefault();
    clearTimeout(jobSearchTimer);
    runJobSearch(input.form);
  });

  window.addEventListener("hashchange", loadRoute);
  window.__tnReceiveFiles = function (id, rows, error) {
    var forms = window.__tnNativeForms || {};
    var form = forms[id];
    delete forms[id];
    var pickBtn = form && form.querySelector("[data-native-pick]");
    if (pickBtn) pickBtn.disabled = false;
    if (!form) return;
    if (error) {
      showFormNotice(form, error, true);
      return;
    }
    var files = filesFromNative(rows);
    if (!files.length) return;
    form._tnFiles = files;
    var nameEl = form.querySelector(".tn-file-name");
    if (nameEl) {
      nameEl.textContent = files.length === 1 ? files[0].name : (files.length + " " + t.filesChosen);
    }
    sendPickedFiles(form, files);
  };
  window.__tnUploadDone = function (id, ok, message) {
    var forms = window.__tnNativeForms || {};
    var form = forms[id];
    delete forms[id];
    var pickBtn = form && form.querySelector("[data-native-pick]");
    if (pickBtn) pickBtn.disabled = false;
    if (!form) return;
    if (!ok) {
      showFormNotice(form, message || t.err, true);
      return;
    }
    done(message || t.uploadedOk);
  };
  window.addEventListener("talendus:session-set", function () { syncNativeAuth(); });
  window.addEventListener("talendus:session-cleared", function () {
    try { if (window.TalendusNative && window.TalendusNative.clearAuth) window.TalendusNative.clearAuth(); } catch (e) {}
  });
  function urlBase64ToUint8Array(base64String) {
    var padding = "=".repeat((4 - base64String.length % 4) % 4);
    var base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
    var rawData = atob(base64);
    var outputArray = new Uint8Array(rawData.length);
    for (var i = 0; i < rawData.length; ++i) outputArray[i] = rawData.charCodeAt(i);
    return outputArray;
  }
  function nativePush() {
    try { return window.TalendusNative && typeof window.TalendusNative.showNotification === "function"; } catch (e) { return false; }
  }
  function syncNativeAuth() {
    if (!nativePush()) return;
    try {
      var token = localStorage.getItem("talendus_access_token") || "";
      if (token && window.TalendusNative.setAuthToken) window.TalendusNative.setAuthToken(token);
      if (!token && window.TalendusNative.clearAuth) window.TalendusNative.clearAuth();
    } catch (e) {}
  }
  function pushAllowed() {
    try {
      if (nativePush() && typeof window.TalendusNative.notificationsEnabled === "function") {
        if (window.TalendusNative.notificationsEnabled()) return true;
      }
    } catch (e) {}
    return typeof Notification !== "undefined" && Notification.permission === "granted";
  }
  function pushBanner() {
    if (!state.user) return "";
    if (pushAllowed()) return "";
    try { if (localStorage.getItem("talendus_push_ok") === "1" && pushAllowed()) return ""; } catch (e) {}
    if (typeof Notification !== "undefined" && Notification.permission === "denied" && !nativePush()) return "";
    if (typeof Notification === "undefined" && !nativePush()) return "";
    return '<div class="tn-card tn-push-card"><p class="tn-meta">' + esc(t.pushLead) +
      '</p><button type="button" class="tn-btn" data-enable-push>' + esc(t.pushEnable) + "</button></div>";
  }
  function seenPushIds() {
    try { return JSON.parse(localStorage.getItem("talendus_push_seen") || "[]"); } catch (e) { return []; }
  }
  function storeSeenPush(ids) {
    try { localStorage.setItem("talendus_push_seen", JSON.stringify(ids.slice(-80))); } catch (e) {}
  }
  function mirrorUnreadToNative(rows) {
    if (!nativePush()) return;
    rows = rows || state.notifs || [];
    var seen = seenPushIds();
    var changed = false;
    rows.forEach(function (n) {
      if (!n || n.is_read || seen.indexOf(n.id) !== -1) return;
      seen.push(n.id);
      changed = true;
    });
    if (changed) storeSeenPush(seen);
  }
  function enablePush(interactive) {
    if (!state.user && !api.currentUser()) return Promise.resolve(false);
    syncNativeAuth();
    if (nativePush()) {
      try { if (window.TalendusNative.requestPermission) window.TalendusNative.requestPermission(); } catch (e) {}
      if (pushAllowed()) {
        try { localStorage.setItem("talendus_push_ok", "1"); } catch (e) {}
      }
    }
    if (!("serviceWorker" in navigator) || !("PushManager" in window) || typeof Notification === "undefined") {
      return Promise.resolve(pushAllowed());
    }
    var ask = Notification.permission === "granted"
      ? Promise.resolve("granted")
      : (interactive ? Notification.requestPermission() : Promise.resolve(Notification.permission));
    return ask.then(function (perm) {
      if (perm !== "granted") return pushAllowed();
      return navigator.serviceWorker.ready.then(function (reg) {
        return api.request("/push/vapid-public-key").then(function (json) {
          var key = dataOf(json) && dataOf(json).public_key;
          if (!key) return pushAllowed();
          return reg.pushManager.getSubscription().then(function (existing) {
            return existing || reg.pushManager.subscribe({
              userVisibleOnly: true,
              applicationServerKey: urlBase64ToUint8Array(key)
            });
          }).then(function (sub) {
            var raw = sub.toJSON();
            if (!raw.endpoint || !raw.keys) return false;
            return api.request("/push/subscribe", {
              method: "POST",
              body: { endpoint: raw.endpoint, keys: { p256dh: raw.keys.p256dh, auth: raw.keys.auth } }
            }).then(function () {
              try { localStorage.setItem("talendus_push_ok", "1"); } catch (e) {}
              return true;
            });
          });
        });
      });
    }).catch(function () { return pushAllowed(); });
  }
  function disablePush() {
    try { localStorage.removeItem("talendus_push_ok"); } catch (e) {}
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) return Promise.resolve();
    return navigator.serviceWorker.ready.then(function (reg) {
      return reg.pushManager.getSubscription().then(function (sub) {
        if (!sub) return;
        var endpoint = sub.endpoint;
        return sub.unsubscribe().catch(function () {}).then(function () {
          return api.request("/push/subscribe", { method: "DELETE", body: { endpoint: endpoint } }).catch(function () {});
        });
      });
    }).catch(function () {});
  }
  function quietPushSync() {
    if (!state.user) return;
    syncNativeAuth();
    if (typeof Notification !== "undefined" && Notification.permission === "granted") enablePush(false);
    else if (nativePush()) enablePush(false);
    mirrorUnreadToNative();
  }
  function pollNotifs() {
    if (!state.user || !api.currentUser()) return;
    api.notifications(true).then(function (json) {
      var unread = dataOf(json) || [];
      mirrorUnreadToNative(unread);
      var prev = unreadCount();
      if (unread.length) {
        var byId = {};
        (state.notifs || []).forEach(function (n) { byId[n.id] = n; });
        unread.forEach(function (n) { byId[n.id] = n; });
        state.notifs = Object.keys(byId).map(function (id) { return byId[id]; });
      }
      if (unreadCount() !== prev) render();
    }).catch(function () {});
  }
  function syncCallScreen() {
    var r = route();
    if (r.name === "call" && r.id && window.TalendusCall) {
      var q = r.query || {};
      var video = q.video !== "0" && q.video !== "false";
      window.TalendusCall.start({
        interviewId: r.id,
        video: video,
        onHangup: function () {
          if (route().name === "call") go("#/interviews");
        }
      });
      return;
    }
    if (window.TalendusCall && window.TalendusCall.isLive()) window.TalendusCall.hangup();
  }
  var INSTALL_LIVE = false;
  function registerSw() {
    var native = !!(window.TalendusNative || (navigator.userAgent || "").indexOf("TalendusApp/") !== -1);
    if (!INSTALL_LIVE && !native) return;
    if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
    }
  }
  if (window.requestIdleCallback) window.requestIdleCallback(registerSw, { timeout: 2500 });
  else setTimeout(registerSw, 1200);
  setInterval(pollNotifs, 20000);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
      pollNotifs();
      if (nativePush()) {
        try { window.TalendusNative.requestPermission(); } catch (e) {}
      }
    }
  });
  api.services().then(function (json) {
    var data = dataOf(json) || {};
    if (data.contact) state.contact = data.contact;
  }).catch(function () {});
  syncNativeAuth();
  hydrateSession().then(loadRoute).catch(function () { render(); });
  render();
})();
