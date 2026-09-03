(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var root = document.getElementById("tl-account");
    if (!root || !window.TalendusAPI) return;
    var api = window.TalendusAPI;
    var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
    document.body.classList.add("tl-portal-active");
    var siteServices = { payments: { transfer: true, card: false, paypal: false } };
    var servicesReady = api.services
      ? api.services().then(function (json) {
          if (json && json.data) siteServices = json.data;
        }).catch(function () {})
      : Promise.resolve();

    var t = isEn ? {
      login: "Sign in", register: "Create an account", email: "Email", password: "Password",
      first: "First name", last: "Last name", submitLogin: "Sign in", submitRegister: "Create my account",
      logout: "Sign out", dashboard: "Dashboard", profile: "Profile", apps: "Applications",
      notifs: "Notifications", documents: "Documents", jobs: "Jobs", hiring: "My hiring", messages: "Messages",
      interviews: "Interviews", settings: "Settings", save: "Save", city: "City", title: "Job title",
      sector: "Sector", skills: "Skills", phone: "Phone", upload: "Upload a PDF, Word or image file (PNG, JPG)",
      emptyApps: "No applications yet.", emptyNotifs: "No notifications.", emptyJobs: "No matching roles yet.",
      emptyMsgs: "No messages yet.", emptyInts: "No interviews scheduled.", emptyDocs: "No documents yet.",
      emptySaved: "No saved jobs.", jobUnavailable: "This job is no longer available.", markAll: "Mark all as read", markRead: "Mark as read",
      welcome: "Your candidate workspace", guest: "Sign in to follow your applications.",
      welcomeEmployer: "Your hiring workspace", guestEmployer: "Sign in to follow the profiles Talendus presents.",
      registerEmployer: "Create an employer account",
      brand: "We hire better, faster and more intelligently with AI.",
      point1: "A consultant searches, screens and presents the files.",
      point2: "A consultant follows your file. Call or write — we take it from there.",
      loginLead: "Enter your workspace.",
      registerLead: "Takes five minutes. Free for talent.",
      registerEmployerLead: "Hand us a hiring need and follow the shortlists we present.",
      haveAccount: "Already have an account?",
      noAccount: "No account yet?",
      err: "Something went wrong.", saved: "Saved.", uploaded: "File saved.", send: "Send",
      confirm: "Confirm", cancel: "Cancel", callAudio: "Audio call", callVideo: "Video call", to: "To", write: "Your message", score: "Match",
      welcomeEmployer: "Your hiring workspace", guestEmployer: "Sign in to follow the profiles Talendus presents.",
      registerEmployer: "Create an employer account", company: "Company", inbox: "Applications",
      candidates: "Presented files", invoices: "Invoices", publish: "Publish", pause: "Pause",
      archive: "Archive", draft: "Draft", createJob: "Hand us a hiring need", edit: "Edit", apply: "Apply",
      bookmark: "Save job", unbookmark: "Saved", search: "Search", filters: "Filters",
      completeness: "Profile completeness", quickSearch: "Search jobs", quickProfile: "Complete my profile",
      quickCv: "Download resume", quickApps: "View applications", inProgress: "In progress",
      upcoming: "Upcoming interviews", accepted: "Accepted", hello: "Hello", activeJobs: "Active searches",
      shortlisted: "Shortlisted", hired: "Hires", recent: "Recent activity", loading: "Loading…",
      withdraw: "Withdraw", location: "Location", contract: "Contract type", salary: "Salary",
      experience: "Experience", sort: "Sort", bio: "Professional summary", availability: "Availability",
      mobility: "Geographic mobility", languages: "Languages", desiredSalary: "Desired salary",
      updated: "Last updated", photo: "Photo", add: "Add", remove: "Remove", replace: "Replace",
      download: "Download", personal: "Personal information", security: "Security",
      privacy: "Privacy", danger: "Delete account", newPass: "New password", currentPass: "Current password",
      confirmDanger: "This will deactivate your account. Continue?", members: "Users",
      permissions: "Role", invite: "Invite", legal: "Legal information", website: "Website",
      address: "Address", country: "Country", description: "Description", openings: "Openings",
      startDate: "Start date", deadline: "Deadline", responsibilities: "Responsibilities",
      extra: "Additional information", validate: "Talendus reviews the need, defines the profile and takes on the search. You do not publish a job yourself.",
      hours: "Hours", hoursHint: "Weekly workload, not the contract type.",
      shiftLabel: "Shift", shiftHint: "Time of day or week.",
      contractHint: "Permanent, temporary, seasonal — not full-time or part-time.",
      workMode: "Workplace", pick: "Select",
      workStatus: "Work status", workAuth: "Work authorization",
      canSponsor: "We can sponsor a candidate", sponsorYes: "Sponsorship available",
      occupation: "Occupation",
      overtime: "Overtime", license: "Driver’s licence", union: "Union", travel: "Travel",
      benefits: "Benefits", offerSent: "Offer sent", secondInterview: "Second interview",
      needSent: "Your hiring need has been sent to Talendus. Our team will review the information and contact you to understand the role and define the profile together. Your recruiting starts with Talendus.",
      emptyHiring: "No hiring request yet. Hand us a need and we take it from there.",
      hiringLead: "You hand us the need. Talendus searches, screens and presents qualified profiles. You keep the final decision.",
      validateBrief: "Approve the brief", requestChanges: "Request a change",
      feedback: "Your comments",
      schedule: "Schedule interview", when: "Date and time", type: "Type", place: "Location or link",
      scheduleLeadEmployer: "Your Talendus consultant schedules interviews. They appear here when a time is set.",
      scheduleLeadCandidate: "Your consultant schedules interviews with you. Confirm or join them from this page.",
      emptyDirectory: "No consultant is linked yet. Write to Talendus from Contact if you need to reach us.",
      comments: "Comments", cover: "Cover letter", certs: "Certifications", otherDocs: "Other documents",
      noResults: "No results for these filters.", retry: "Try again", success: "Done.",
      page: "Page", of: "of", prev: "Previous", next: "Next", jobDetail: "Job details",
      appDetail: "Application", sent: "Submitted", review: "Under review", preselect: "Shortlist",
      interview: "Interview", decision: "Decision", companyDocs: "Company documents",
      notifyPrefs: "Notification preferences", emailNotif: "Email", inApp: "In-app",
      sms: "SMS", wa: "WhatsApp", push: "Push notifications",
      profilePublic: "Allow a public professional summary", changeEmail: "Email address is used to sign in.",
      emptyInbox: "No profiles presented yet. Talendus will share qualified shortlists.", emptyInvoices: "No invoices.",
      amount: "Amount", status: "Status",
      pay: "Record a card payment", payPal: "Pay with PayPal", pipeline: "Pipeline",
      contracts: "Contracts", emptyContracts: "No mandate yet.",
      sign: "Sign electronically", signed: "Signed", unsigned: "To sign",
      acceptTerms: "I have read this mandate in full and I accept its terms",
      readMandate: "Read the mandate",
      readPdf: "Open the PDF",
      clientReceived: "Received", clientOpened: "Opened", clientSigned: "Signed",
      talendusSigned: "Talendus has signed",
      readThenSign: "Read the mandate, then sign below.",
      transferHint: "Pay by bank transfer or cheque to Talendus. No payment processor required.",
      downloadPdf: "Download PDF",
      mediate: "Write to your Talendus consultant. They coordinate interviews and follow-up with you.",
      mediateCandidate: "Your Talendus consultant follows your file. Call, write or send a message here — we get back to you.",
      writeTalendus: "Write to your Talendus consultant",
      forgot: "Forgot password?", alerts: "Job alerts", savedJobs: "Saved jobs", cv: "My resume",
      ats: "Mandates", billing: "Billing", duplicate: "Duplicate", deleteJob: "Delete",
      sessions: "Active sessions", loginLog: "Sign-in history", revoke: "Revoke", revokeAll: "Sign out everywhere",
      onboard: "Complete your profile so Talendus can consider you for relevant opportunities.", keywords: "Keywords",
      createAlert: "Create an alert", emptyAlerts: "No job alerts yet.",
      province: "Province", birth: "Date of birth", size: "Company size", social: "Social networks",
      settingsLeadCandidate: "Manage your space. A consultant stays with you on every mandate.",
      settingsLeadEmployer: "Manage your access. A consultant stays your contact for every hire.",
      settingsAccount: "Account", settingsNotifs: "Notifications", settingsTeam: "Team",
      settingsLang: "Language of the workspace", settingsLangFr: "French", settingsLangEn: "English",
      settingsEmailLocked: "This email is used to sign in. Write to your consultant if you need to change it.",
      notifyMatch: "Opportunities that may fit", notifyMatchHint: "When Talendus identifies a mandate that matches your profile.",
      notifyApplication: "Application updates", notifyApplicationHint: "When your file moves forward with Talendus.",
      notifyPresented: "Presented files", notifyPresentedHint: "When Talendus shares a shortlist for one of your mandates.",
      notifyInterview: "Interviews", notifyInterviewHint: "Reminders and changes to interview times.",
      notifyMessage: "Messages from your consultant", notifyMessageHint: "When Talendus writes to you in the workspace.",
      notifyChannels: "How we reach you", notifyChannelsHint: "Talendus writes by email, in this workspace, and by push on your phone. SMS and WhatsApp are not offered.",
      privacyHint: "Your file is followed by a consultant. Contact us whenever you want to move forward.",
      privacyTalendus: "Talendus may use a short professional summary when presenting you to a company.",
      dangerHint: "This deactivates the account. Your consultant can no longer consider you for mandates.",
      dangerHintEmployer: "This deactivates your access. Your company file stays with Talendus.",
      sessionsHint: "Devices currently signed in to your workspace.",
      loginLogHint: "Recent sign-in attempts on this account.",
      teamHint: "Invite colleagues who should follow the files Talendus presents. Your consultant remains the hiring contact.",
      teamReadOnly: "You can see who has access. Only an administrator can invite someone.",
      yourRole: "Your access",
      yourAccessHint: "What you can do in this workspace depends on the role your company assigned.",
      openProfile: "Edit my profile", openCompany: "Company file", openBilling: "Invoices",
      noSessions: "No other session recorded.",
      inviteHint: "The person receives access to this company workspace.",
      roleHintOwner: "Full access, including team and company file.",
      roleHintAdmin: "Manages the company file and the team.",
      roleHintHr: "Follows presented files and hiring needs.",
      roleHintRecruiter: "Follows presented files for the mandates you work on.",
      roleHintBilling: "Sees invoices. Hiring files stay with HR and administrators.",
      roleHintMember: "Limited access to the company workspace.",
      alreadyApplied: "Talendus already has this request.",
      viewApp: "Follow this application",
      noBilling: "Billing is not available for this access."
    } : {
      login: "Connexion", register: "Créer un compte", email: "Courriel", password: "Mot de passe",
      first: "Prénom", last: "Nom", submitLogin: "Me connecter", submitRegister: "Créer mon compte",
      logout: "Déconnexion", dashboard: "Tableau de bord", profile: "Profil", apps: "Candidatures",
      notifs: "Notifications", documents: "Documents", jobs: "Offres", hiring: "Mes recrutements", messages: "Messages",
      interviews: "Entretiens", settings: "Paramètres", save: "Enregistrer", city: "Ville", title: "Titre professionnel",
      sector: "Secteur", skills: "Compétences", phone: "Téléphone", upload: "Téléverser un PDF, Word ou une image (PNG, JPG)",
      emptyApps: "Aucune candidature pour le moment.", emptyNotifs: "Aucune notification.",
      emptyJobs: "Aucune offre ne correspond encore à votre recherche.", emptyMsgs: "Aucun message pour le moment.",
      emptyInts: "Aucun entretien planifié.", emptyDocs: "Aucun document pour le moment.",
      emptySaved: "Aucune offre sauvegardée.", jobUnavailable: "Cette offre n'est plus disponible.", markAll: "Tout marquer comme lu", markRead: "Marquer comme lu",
      welcome: "Votre espace candidat", guest: "Connectez-vous pour suivre vos candidatures.",
      welcomeEmployer: "Votre espace employeur", guestEmployer: "Connectez-vous pour suivre les profils que Talendus vous présente.",
      registerEmployer: "Créer un compte employeur",
      brand: "Nous recrutons mieux, plus vite et plus intelligemment grâce à l'IA.",
      point1: "Un conseiller recherche, présélectionne et présente les dossiers.",
      point2: "Un conseiller suit votre dossier. Appelez-nous ou écrivez-nous : on avance avec vous.",
      loginLead: "Entrez dans votre espace.",
      registerLead: "Cinq minutes. C'est gratuit pour les talents.",
      registerEmployerLead: "Confiez un besoin et suivez les shortlists que nous présentons.",
      haveAccount: "Déjà un compte ?",
      noAccount: "Pas encore de compte ?",
      err: "Une erreur s’est produite.", saved: "Enregistré.", uploaded: "Fichier enregistré.", send: "Envoyer",
      confirm: "Confirmer", cancel: "Annuler", callAudio: "Appel audio", callVideo: "Appel vidéo", to: "Destinataire", write: "Votre message", score: "Score",
      welcomeEmployer: "Votre espace employeur", guestEmployer: "Connectez-vous pour suivre les profils que Talendus vous présente.",
      registerEmployer: "Créer un compte employeur", company: "Entreprise", inbox: "Candidatures",
      candidates: "Dossiers présentés", invoices: "Factures", publish: "Publier", pause: "Mettre en pause",
      archive: "Archiver", draft: "Brouillon", createJob: "Confier un recrutement", edit: "Modifier", apply: "Postuler",
      bookmark: "Sauvegarder", unbookmark: "Sauvegardée", search: "Rechercher", filters: "Filtres",
      completeness: "Complétude du profil", quickSearch: "Rechercher une offre", quickProfile: "Compléter mon profil",
      quickCv: "Télécharger mon CV", quickApps: "Voir mes candidatures", inProgress: "En cours",
      upcoming: "Entretiens à venir", accepted: "Acceptées", hello: "Bonjour", activeJobs: "Recrutements actifs",
      shortlisted: "Présélectionnés", hired: "Recrutements", recent: "Activité récente", loading: "Chargement…",
      withdraw: "Retirer", location: "Localisation", contract: "Type de contrat", salary: "Salaire",
      experience: "Expérience", sort: "Trier", bio: "Résumé professionnel", availability: "Disponibilité",
      mobility: "Mobilité géographique", languages: "Langues", desiredSalary: "Salaire souhaité",
      updated: "Dernière mise à jour", photo: "Photo", add: "Ajouter", remove: "Supprimer", replace: "Remplacer",
      download: "Télécharger", personal: "Informations personnelles", security: "Sécurité",
      privacy: "Confidentialité", danger: "Supprimer le compte", newPass: "Nouveau mot de passe",
      currentPass: "Mot de passe actuel", confirmDanger: "Cette action désactivera votre compte. Continuer ?",
      members: "Utilisateurs", permissions: "Rôle", invite: "Inviter", legal: "Informations légales",
      website: "Site web", address: "Adresse", country: "Pays", description: "Description", openings: "Nombre de postes",
      startDate: "Date de début", deadline: "Date limite", responsibilities: "Responsabilités",
      extra: "Informations complémentaires", validate: "Talendus étudie le besoin, définit le profil et lance la recherche. Vous ne publiez pas l’offre vous-même.",
      hours: "Horaire", hoursHint: "Charge dans la semaine, pas le type de contrat.",
      shiftLabel: "Quart", shiftHint: "Moment de la journée ou de la semaine.",
      contractHint: "Permanent, temporaire, saisonnier — pas le temps plein ou partiel.",
      workMode: "Présence", pick: "Choisir",
      workStatus: "Statut d’autorisation", workAuth: "Autorisation de travail",
      canSponsor: "Nous pouvons parrainer un candidat", sponsorYes: "Parrainage possible",
      occupation: "Métier",
      overtime: "Heures sup.", license: "Permis", union: "Syndicat", travel: "Déplacements",
      benefits: "Avantages", offerSent: "Offre envoyée", secondInterview: "2e entretien",
      needSent: "Votre besoin a bien été transmis à Talendus. Notre équipe va analyser les informations communiquées et vous contacter afin de mieux comprendre votre besoin et de définir avec vous le profil recherché. Votre recrutement commence avec Talendus.",
      emptyHiring: "Aucun recrutement pour le moment. Confiez-nous un besoin : nous prenons le relais.",
      hiringLead: "Vous nous confiez votre besoin. Talendus recherche, présélectionne et présente des profils qualifiés. Vous gardez la décision finale.",
      validateBrief: "Valider le brief", requestChanges: "Demander une modification",
      feedback: "Vos retours",
      schedule: "Planifier un entretien", when: "Date et heure", type: "Type", place: "Lieu ou lien",
      scheduleLeadEmployer: "Votre conseiller Talendus planifie les entretiens. Ils s’affichent ici dès qu’une date est fixée.",
      scheduleLeadCandidate: "Votre conseiller planifie les entretiens avec vous. Confirmez-les ou joignez-les depuis cette page.",
      emptyDirectory: "Aucun conseiller n’est encore lié. Écrivez à Talendus depuis Contact si vous devez nous joindre.",
      comments: "Commentaires", cover: "Lettre de motivation", certs: "Certifications", otherDocs: "Documents complémentaires",
      noResults: "Aucun résultat pour ces filtres.", retry: "Réessayer", success: "Terminé.",
      page: "Page", of: "sur", prev: "Précédent", next: "Suivant", jobDetail: "Détail de l’offre",
      appDetail: "Candidature", sent: "Candidature envoyée", review: "Dossier examiné", preselect: "Présélection",
      interview: "Entretien", decision: "Décision", companyDocs: "Documents de l’entreprise",
      notifyPrefs: "Préférences de notification", emailNotif: "Courriel", inApp: "Dans l’application",
      sms: "SMS", wa: "WhatsApp", push: "Notifications push",
      profilePublic: "Autoriser un résumé professionnel visible", changeEmail: "Le courriel sert à vous connecter.",
      emptyInbox: "Aucun dossier présenté pour le moment. Talendus vous transmet les profils qualifiés.", emptyInvoices: "Aucune facture.",
      amount: "Montant", status: "Statut",
      pay: "Payer par carte", payPal: "Payer avec PayPal", pipeline: "Pipeline",
      contracts: "Contrats", emptyContracts: "Aucun mandat pour le moment.",
      sign: "Signer électroniquement", signed: "Signé", unsigned: "À signer",
      acceptTerms: "J’ai lu l’intégralité de ce mandat et j’en accepte les conditions",
      readMandate: "Lire le mandat",
      readPdf: "Ouvrir le PDF",
      clientReceived: "Reçu", clientOpened: "Ouvert", clientSigned: "Signé",
      talendusSigned: "Talendus a signé",
      readThenSign: "Lisez le mandat, puis signez ci-dessous.",
      transferHint: "Réglez par virement ou chèque à l’ordre de Talendus. Aucun intermédiaire de paiement n’est requis.",
      downloadPdf: "Télécharger le PDF",
      mediate: "Écrivez à votre conseiller Talendus. Il coordonne les entretiens et le suivi avec vous.",
      mediateCandidate: "Votre conseiller Talendus suit votre dossier. Appelez, écrivez ou envoyez un message ici : on vous répond.",
      writeTalendus: "Écrire à votre conseiller Talendus",
      forgot: "Mot de passe oublié ?", alerts: "Alertes emploi", savedJobs: "Offres sauvegardées", cv: "Mon CV",
      ats: "Mandats", billing: "Facturation", duplicate: "Dupliquer", deleteJob: "Supprimer",
      sessions: "Sessions actives", loginLog: "Journal des connexions", revoke: "Révoquer", revokeAll: "Déconnecter partout",
      onboard: "Complétez votre profil pour que Talendus puisse vous considérer pour des opportunités pertinentes.", keywords: "Mots-clés",
      createAlert: "Créer une alerte", emptyAlerts: "Aucune alerte pour le moment.",
      province: "Province", birth: "Date de naissance", size: "Taille de l’entreprise", social: "Réseaux sociaux",
      settingsLeadCandidate: "Gérez votre espace. Un conseiller reste à votre écoute pour chaque mandat.",
      settingsLeadEmployer: "Gérez votre accès. Un conseiller reste votre contact pour chaque recrutement.",
      settingsAccount: "Compte", settingsNotifs: "Notifications", settingsTeam: "Équipe",
      settingsLang: "Langue de l’espace", settingsLangFr: "Français", settingsLangEn: "Anglais",
      settingsEmailLocked: "Ce courriel sert à vous connecter. Écrivez à votre conseiller s’il doit être modifié.",
      notifyMatch: "Opportunités qui peuvent correspondre", notifyMatchHint: "Quand Talendus identifie un mandat proche de votre profil.",
      notifyApplication: "Suivi de candidature", notifyApplicationHint: "Quand votre dossier avance avec Talendus.",
      notifyPresented: "Dossiers présentés", notifyPresentedHint: "Quand Talendus vous transmet une shortlist pour un mandat.",
      notifyInterview: "Entretiens", notifyInterviewHint: "Rappels et changements d’horaire.",
      notifyMessage: "Messages de votre conseiller", notifyMessageHint: "Quand Talendus vous écrit dans l’espace.",
      notifyChannels: "Comment on vous joint", notifyChannelsHint: "Talendus vous écrit par courriel, dans cet espace, et par notifications push sur votre téléphone. SMS et WhatsApp ne sont pas proposés.",
      privacyHint: "Votre dossier est suivi par un conseiller. Contactez-nous dès que vous voulez avancer.",
      privacyTalendus: "Talendus peut utiliser un court résumé professionnel au moment de vous présenter à une entreprise.",
      dangerHint: "Cette action désactive le compte. Votre conseiller ne pourra plus vous considérer pour des mandats.",
      dangerHintEmployer: "Cette action désactive votre accès. Le dossier de l’entreprise reste chez Talendus.",
      sessionsHint: "Appareils actuellement connectés à votre espace.",
      loginLogHint: "Tentatives de connexion récentes sur ce compte.",
      teamHint: "Invitez des collègues qui doivent suivre les dossiers que Talendus présente. Votre conseiller reste le contact du recrutement.",
      teamReadOnly: "Vous voyez qui a accès. Seul un administrateur peut inviter quelqu’un.",
      yourRole: "Votre accès",
      yourAccessHint: "Ce que vous pouvez faire ici dépend du rôle attribué par votre entreprise.",
      openProfile: "Modifier mon profil", openCompany: "Fiche entreprise", openBilling: "Factures",
      noSessions: "Aucune autre session enregistrée.",
      inviteHint: "La personne reçoit un accès à l’espace de cette entreprise.",
      roleHintOwner: "Accès complet, y compris l’équipe et la fiche entreprise.",
      roleHintAdmin: "Gère la fiche entreprise et l’équipe.",
      roleHintHr: "Suit les dossiers présentés et les besoins de recrutement.",
      roleHintRecruiter: "Suit les dossiers présentés sur les mandats suivis.",
      roleHintBilling: "Voit les factures. Les dossiers de recrutement restent aux RH et administrateurs.",
      roleHintMember: "Accès limité à l’espace entreprise.",
      alreadyApplied: "Talendus a déjà cette demande.",
      viewApp: "Suivre cette candidature",
      noBilling: "La facturation n’est pas disponible pour cet accès."
    };

    function esc(v) {
      return String(v == null ? "" : v)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    var jobOptions = null;
    function loadJobOptions() {
      if (jobOptions) return Promise.resolve(jobOptions);
      return api.request("/jobs/options").then(function (json) {
        jobOptions = (json && json.data) || {};
        return jobOptions;
      }).catch(function () {
        jobOptions = jobOptions || {};
        return jobOptions;
      });
    }
    function optionValue(item) {
      if (!item) return "";
      return typeof item === "string" ? item : (item.value || item.label || "");
    }
    function optionLabel(item) {
      if (!item) return "";
      if (typeof item === "string") return item;
      return isEn ? (item.label_en || item.label || item.value) : (item.label || item.value);
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
      var id = "acc-f-" + name;
      var html = '<select id="' + id + '" name="' + name + '"' + (required ? " required" : "") + '><option value="">' + esc(allLabel == null ? t.pick : allLabel) + "</option>";
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
    function labeledChoice(name, label, items, selected, allLabel) {
      return '<label for="acc-f-' + name + '">' + esc(label) + "</label>" + choiceSelect(name, items, selected, allLabel);
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
    function choiceGroup(name, items, selected, label) {
      var picked = selectedSet(selected);
      var seen = {};
      var html = '<fieldset class="tl-choices"><legend>' + esc(label) + "</legend><div class=\"tl-choice-grid\">";
      function add(val, text) {
        if (!val || seen[val]) return;
        seen[val] = true;
        html += '<label class="tl-chip-check"><input type="checkbox" name="' + name + '" value="' + esc(val) + '"' +
          (picked[val] ? " checked" : "") + "> " + esc(text || val) + "</label>";
      }
      (items || []).forEach(function (item) {
        var val = optionValue(item);
        add(val, optionLabel(item));
      });
      Object.keys(picked).forEach(function (val) { add(val, val); });
      return html + "</div></fieldset>";
    }
    function formChoice(form, name) {
      var boxes = form.querySelectorAll('input[type="checkbox"][name="' + name + '"]');
      if (!boxes.length) return String(new FormData(form).get(name) || "");
      return Array.prototype.map.call(form.querySelectorAll('input[type="checkbox"][name="' + name + '"]:checked'), function (el) {
        return el.value;
      }).filter(Boolean).join(", ");
    }
    function jobFacts(job) {
      if (!job) return "";
      var rows = [
        [t.location, job.location], [t.sector, job.sector], [t.contract, job.contract_type],
        [t.hours, job.schedule], [t.shiftLabel, job.shift], [t.workMode, job.work_mode],
        [t.languages, job.languages], [t.overtime, job.overtime], [t.license, job.driver_license],
        [t.union, job.unionized], [t.travel, job.travel],
        [t.workAuth, job.work_authorization && job.work_authorization !== "ouvert" ? catalogLabel((jobOptions || {}).work_requirements, job.work_authorization) : ""],
        [t.sponsorYes, job.can_sponsor ? (isEn ? "Yes" : "Oui") : ""],
        [t.salary, job.salary_display],
        [t.experience, job.experience_level], [t.certs, job.certifications], [t.benefits, job.benefits]
      ].filter(function (row) { return row[1]; });
      if (!rows.length) return "";
      return '<ul class="tl-job-facts">' + rows.map(function (row) {
        return "<li><span>" + esc(row[0]) + "</span><strong>" + esc(row[1]) + "</strong></li>";
      }).join("") + "</ul>";
    }
    function statusLabel(s) {
      var key = String(s || "").toUpperCase().replace(/-/g, "_");
      var map = {
        SUBMITTED: isEn ? "Submitted" : "Candidature envoyée",
        RECEIVED: isEn ? "Received" : "Reçue",
        UNDER_REVIEW: isEn ? "Under review" : "En cours d’analyse",
        SHORTLISTED: isEn ? "Shortlisted" : "Présélection",
        INTERVIEW: isEn ? "Interview" : "Entretien",
        SECOND_INTERVIEW: isEn ? "Second interview" : "Deuxième entretien",
        OFFER_SENT: isEn ? "Offer" : "Offre d’emploi",
        REJECTED: isEn ? "Declined" : "Refusée",
        HIRED: isEn ? "Hired" : "Acceptée",
        WITHDRAWN: isEn ? "Withdrawn" : "Retirée",
        DRAFT: isEn ? "Draft" : "Brouillon",
        PUBLISHED: isEn ? "Published" : "Publiée",
        PAUSED: isEn ? "Paused" : "En pause",
        ARCHIVED: isEn ? "Archived" : "Archivée",
        CLOSED: isEn ? "Closed" : "Fermée",
        SCHEDULED: isEn ? "Scheduled" : "Planifié",
        CONFIRMED: isEn ? "Confirmed" : "Confirmé",
        COMPLETED: isEn ? "Completed" : "Terminé",
        CANCELLED: isEn ? "Cancelled" : "Annulé",
        NO_SHOW: isEn ? "No-show" : "Absent",
        OWNER: isEn ? "Owner" : "Propriétaire",
        ADMIN: isEn ? "Administrator" : "Administrateur",
        HR: isEn ? "HR" : "RH",
        RECRUITER: isEn ? "Recruiter" : "Recruteur",
        MEMBER: isEn ? "Member" : "Membre",
        BILLING: isEn ? "Billing" : "Facturation",
        SENT: isEn ? "Sent" : "Envoyée",
        PENDING: isEn ? "Pending" : "En attente",
        PAID: isEn ? "Paid" : "Payée",
        OVERDUE: isEn ? "Overdue" : "En retard",
        REFUNDED: isEn ? "Refunded" : "Remboursée",
        REQUEST_SUBMITTED: isEn ? "Need submitted" : "Besoin transmis",
        CLIENT_CONTACTED: isEn ? "Talking with Talendus" : "Échange avec Talendus",
        NEEDS_CONFIRMED: isEn ? "Profile defined" : "Profil défini",
        JOB_BEING_PREPARED: isEn ? "Offer being prepared" : "Offre en préparation",
        CLIENT_VALIDATION: isEn ? "Validation requested" : "Validation demandée",
        JOB_PUBLISHED: isEn ? "Search launched" : "Recherche lancée",
        SOURCING: isEn ? "Search in progress" : "Recherche en cours",
        SCREENING: isEn ? "Screening" : "Présélection en cours",
        INTERVIEWS: isEn ? "Talendus interviews" : "Entretiens Talendus",
        SHORTLIST: isEn ? "Shortlist ready" : "Shortlist disponible",
        CLIENT_REVIEW: isEn ? "Profiles to review" : "Profils à consulter",
        HIRING: isEn ? "Your decision" : "Décision en cours",
        TALENDUS: "Talendus",
        CLIENT: isEn ? "Client" : "Client",
        PHONE: isEn ? "Phone" : "Téléphone",
        VIDEO: isEn ? "Video" : "Visio",
        ONSITE: isEn ? "On site" : "Sur place",
        OFFER: isEn ? "Offer" : "Offre"
      };
      if (map[key]) return map[key];
      if (s) return String(s).replace(/_/g, " ");
      return "";
    }
    function fmtDate(v) {
      if (!v) return "";
      return String(v).replace("T", " ").slice(0, 16);
    }
    function authDownload(path, filename) {
      if (window.TalendusAPI && typeof window.TalendusAPI.download === "function") {
        var apiPath = String(path || "").replace(/^\/api/, "");
        window.TalendusAPI.download(apiPath, filename).catch(function () { window.alert(t.err); });
        return;
      }
      var token = "";
      try { token = localStorage.getItem("talendus_access_token") || ""; } catch (e) {}
      fetch(path, { headers: { Authorization: token ? ("Bearer " + token) : "", Accept: "*/*" } }).then(function (res) {
        if (!res.ok) throw new Error(t.err);
        return res.blob().then(function (blob) {
          var url = URL.createObjectURL(blob);
          var a = document.createElement("a");
          a.href = url;
          a.download = filename || "document";
          a.rel = "noopener";
          document.body.appendChild(a);
          a.click();
          a.remove();
          var ua = navigator.userAgent || "";
          if (/iphone|ipad|ipod/i.test(ua)) {
            var opened = null;
            try { opened = window.open(url, "_blank"); } catch (e) {}
            if (!opened) location.assign(url);
          }
          setTimeout(function () { URL.revokeObjectURL(url); }, 8000);
        });
      }).catch(function () { window.alert(t.err); });
    }
    function isEmployerSpace() {
      return root.getAttribute("data-space") === "employer" || /\/employer(\/|$)/.test(location.pathname);
    }
    function staffRole(role) {
      return ["ADMIN", "SUPER_ADMIN", "RECRUITER", "FINANCE", "EDITOR"].indexOf(role) !== -1;
    }
    function siteRoot() {
      return isEn ? "/en/" : "/";
    }
    function accountHref(role) {
      if (staffRole(role)) return "/admin/";
      if (role === "EMPLOYER") return siteRoot() + (isEn ? "account-employer.html" : "espace-employeur.html") + "#/dashboard";
      return siteRoot() + (isEn ? "account.html" : "espace.html") + "#/dashboard";
    }
    function localizeHref(href) {
      if (!href) return "";
      if (!isEn) return href;
      return String(href)
        .replace("/espace-employeur.html", "/en/account-employer.html")
        .replace("/espace.html", "/en/account.html");
    }
    function pathMode() {
      return /\/(candidate|employer)(\/|$)/.test(location.pathname);
    }
    function normalizeRoute(name, id) {
      if (isEmployerSpace() && (name === "applications" || name === "apps" || name === "candidatures")) {
        return { name: "inbox", id: id || "" };
      }
      if (name === "applications" || name === "candidatures" || name === "apps") {
        return id ? { name: "application", id: id } : { name: "apps", id: "" };
      }
      if (name === "job" && !id) return { name: "jobs", id: "" };
      if (isEmployerSpace() && name === "jobs" && id) return { name: "job-edit", id: id };
      if (name === "jobs" && id) return { name: "job", id: id };
      if (name === "cv" || name === "resume") return { name: "documents", id: id || "" };
      if (name === "saved" || name === "sauvegardees") return { name: "saved", id: id || "" };
      if (name === "alerts" || name === "alertes") return { name: "alerts", id: id || "" };
      if (name === "ats") return { name: "pipeline", id: id || "" };
      if (name === "billing" || name === "facturation") return { name: "invoices", id: id || "" };
      if (name === "contrats" || name === "mandats") return { name: "contracts", id: id || "" };
      return { name: name || "dashboard", id: id || "" };
    }
    function currentRoute() {
      var parts = location.pathname.replace(/\/+$/, "").split("/").filter(Boolean);
      var key = isEmployerSpace() ? "employer" : "candidate";
      var idx = parts.lastIndexOf(key);
      var rest = idx >= 0 ? parts.slice(idx + 1) : [];
      if (!rest.length) {
        var hash = (location.hash || "").replace(/^#\/?/, "");
        rest = hash ? hash.split("/") : ["dashboard"];
      }
      return normalizeRoute(rest[0] || "dashboard", rest[1] || "");
    }
    function go(name, id) {
      var suffix = name + (id ? "/" + id : "");
      if (pathMode()) {
        var base = location.pathname.split("/").filter(Boolean);
        var key = isEmployerSpace() ? "employer" : "candidate";
        var idx = base.lastIndexOf(key);
        var prefix = idx >= 0 ? "/" + base.slice(0, idx + 1).join("/") : (isEn ? "/en/" : "/") + key;
        history.pushState({}, "", prefix + "/" + suffix);
      } else {
        location.hash = "#/" + suffix;
      }
      renderAuthed();
    }
    function flash(el, msg, ok) {
      if (!el) return;
      el.style.display = "block";
      el.textContent = msg;
      el.className = ok === false ? "tl-success tl-error" : "tl-success";
      el.setAttribute("role", ok === false ? "alert" : "status");
    }
    function empty(msg) { return '<div class="tl-empty"><p>' + esc(msg) + "</p></div>"; }
    function mediateNote() {
      return '<p class="tl-mediate">' + esc(isEmployerSpace() ? t.mediate : t.mediateCandidate) + "</p>";
    }
    function errBox(msg) { return '<div class="tl-error"><p>' + esc(msg || t.err) + '</p><p><button type="button" class="tl-btn tl-btn-ghost" data-retry>' + esc(t.retry) + "</button></p></div>"; }
    function skeleton() { return '<div class="tl-skeleton"></div><div class="tl-skeleton"></div><div class="tl-skeleton"></div>'; }
    function unwrap(p) { return p.then(function (j) { return j.data; }); }
    function navItems(unreadN, unreadM) {
      if (isEmployerSpace()) {
        var items = [
          ["dashboard", t.dashboard, "fa-table-columns"],
          ["company", t.company, "fa-building"],
          ["jobs", t.hiring, "fa-clipboard-list"],
          ["inbox", t.candidates, "fa-users"],
          ["pipeline", t.ats, "fa-diagram-project"],
          ["interviews", t.interviews, "fa-video"],
          ["messages", t.messages, "fa-comments", unreadM]
        ];
        if (!state.company || state.company.can_read_invoices !== false) {
          items.push(["invoices", t.billing, "fa-file-invoice-dollar"]);
        }
        items.push(["contracts", t.contracts, "fa-file-signature"]);
        items.push(["notifs", t.notifs, "fa-bell", unreadN], ["settings", t.settings, "fa-gear"]);
        return items;
      }
      return [
        ["dashboard", t.dashboard, "fa-table-columns"],
        ["jobs", t.jobs, "fa-magnifying-glass"],
        ["profile", t.profile, "fa-user"],
        ["documents", t.cv, "fa-file-lines"],
        ["apps", t.apps, "fa-briefcase"],
        ["saved", t.savedJobs, "fa-bookmark"],
        ["alerts", t.alerts, "fa-bell"],
        ["interviews", t.interviews, "fa-video"],
        ["messages", t.messages, "fa-comments", unreadM],
        ["notifs", t.notifs, "fa-inbox", unreadN],
        ["settings", t.settings, "fa-gear"]
      ];
    }
    function navKey(name) {
      if (name === "job-edit" || name === "job-new" || name === "job") return "jobs";
      if (name === "application") return "apps";
      if (name === "candidate") return "inbox";
      return name;
    }
    function pageTitleFor(route) {
      if (route.name === "job-edit") return t.edit;
      if (route.name === "job-new") return t.createJob;
      if (route.name === "job") return t.jobDetail;
      if (route.name === "application") return t.appDetail;
      if (route.name === "candidate") return t.candidates;
      if (route.name === "settings") {
        if (route.id === "security") return t.security;
        if (route.id === "notifications") return t.settingsNotifs;
        if (route.id === "privacy") return t.privacy;
        if (route.id === "team") return t.settingsTeam;
        if (route.id === "account") return t.settingsAccount;
      }
      var key = navKey(route.name);
      return (navItems(0, 0).filter(function (it) { return it[0] === key; })[0] || [0, t.dashboard])[1];
    }
    function initials(user) {
      var a = String((user && user.first_name) || "").trim().charAt(0);
      var b = String((user && user.last_name) || "").trim().charAt(0);
      return ((a + b) || String((user && user.email) || "?").charAt(0)).toUpperCase();
    }
    function shell(user, content, unreadN, unreadM) {
      var route = currentRoute();
      var active = navKey(route.name);
      var items = navItems(unreadN, unreadM).map(function (it) {
        var badge = it[3] ? '<span class="tl-portal-badge">' + it[3] + "</span>" : "";
        return '<button type="button" data-go="' + it[0] + '" class="' + (active === it[0] ? "is-active" : "") + '">' +
          '<span class="tl-portal-nav-label"><i class="fa-solid ' + it[2] + '" aria-hidden="true"></i>' + esc(it[1]) + "</span>" + badge + "</button>";
      }).join("");
      var mobile = '<div class="tl-mobile-nav"><select id="acc-mobile-nav">' + navItems(unreadN, unreadM).map(function (it) {
        return '<option value="' + it[0] + '"' + (active === it[0] ? " selected" : "") + ">" + esc(it[1]) + "</option>";
      }).join("") + "</select></div>";
      var name = ((user.first_name || "") + " " + (user.last_name || "")).trim() || user.email;
      var role = isEmployerSpace() ? (isEn ? "Employer" : "Entreprise") : (isEn ? "Candidate" : "Candidat");
      var pageTitle = pageTitleFor(route);
      var pageLead = "";
      if (route.name === "settings") {
        pageLead = '<p class="tl-portal-pagehead-lead">' + esc(isEmployerSpace() ? t.settingsLeadEmployer : t.settingsLeadCandidate) + "</p>";
      }
      var av = window.__tlAvatarUrl
        ? '<span class="tl-avatar is-lg"><img src="' + esc(window.__tlAvatarUrl) + '" alt=""></span>'
        : '<span class="tl-avatar is-lg" aria-hidden="true">' + esc(initials(user)) + "</span>";
      root.innerHTML = mobile + '<div class="tl-portal">' +
        '<nav class="tl-portal-nav" aria-label="Talendus">' +
          '<div class="tl-portal-user">' + av + "<div><strong>" + esc(name) + "</strong><span>" + esc(role) + "</span></div></div>" +
          items +
        "</nav>" +
        '<div class="tl-portal-main">' +
          '<div class="tl-portal-pagehead"><h1>' + esc(pageTitle) + "</h1>" + pageLead + "</div>" +
          content +
        "</div></div>";
      root.querySelectorAll("label").forEach(function (label, i) {
        if (label.htmlFor || label.querySelector("input, select, textarea")) return;
        var next = label.nextElementSibling;
        if (!next || !/^(INPUT|SELECT|TEXTAREA)$/.test(next.tagName)) return;
        if (!next.id) next.id = "acc-field-" + (next.getAttribute("name") || i);
        label.setAttribute("for", next.id);
      });
      root.querySelectorAll("[data-go]").forEach(function (btn) {
        btn.onclick = function () { go(btn.getAttribute("data-go")); };
      });
      var sel = document.getElementById("acc-mobile-nav");
      if (sel) sel.onchange = function () { go(sel.value); };
      root.querySelectorAll("[data-nav]").forEach(function (btn) {
        btn.onclick = function () { go(btn.getAttribute("data-nav"), btn.getAttribute("data-id") || ""); };
      });
      root.querySelectorAll("[data-quick-apply]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/applications", {
            method: "POST",
            body: { job_id: btn.getAttribute("data-quick-apply") || null, job_slug: btn.getAttribute("data-slug") || null }
          }).then(function () { state.appsReady = false; go("apps"); }).catch(function (err) { window.alert((err && err.message) || t.err); });
        };
      });
    }

    function renderChecking() {
      document.body.classList.remove("tl-auth-guest");
      root.innerHTML =
        '<div class="tl-session-gate">' +
          '<div class="tl-session-gate-card">' +
            '<p class="tl-lead">' + esc(t.loading) + "</p>" +
            skeleton() +
          "</div>" +
        "</div>";
    }

    function renderGuest() {
      var employer = isEmployerSpace();
      document.body.classList.add("tl-auth-guest");
      state.user = null;
      var hash = (location.hash || "").replace(/^#\/?/, "");
      if (window.TalendusAuth && (hash.indexOf("reset") === 0 || hash.indexOf("verify") === 0 || hash.indexOf("forgot") === 0)) {
        return;
      }
      var roleAttr = employer ? ' data-auth-role="EMPLOYER"' : ' data-auth-role="CANDIDATE"';
      root.innerHTML =
        '<div class="tl-session-gate">' +
          '<div class="tl-session-gate-card">' +
            '<span class="tl-session-gate-icon" aria-hidden="true"><i class="fa-regular fa-user"></i></span>' +
            '<p class="tl-kicker">' + esc(employer ? t.welcomeEmployer : t.welcome) + "</p>" +
            "<h2>" + esc(t.login) + "</h2>" +
            '<p class="tl-lead">' + esc(employer ? t.guestEmployer : t.guest) + "</p>" +
            '<div class="tl-actions">' +
              '<button type="button" class="tl-btn tl-btn-lg" data-auth-open="login"' + roleAttr + ">" + esc(t.submitLogin) + "</button>" +
              '<button type="button" class="tl-btn tl-btn-ghost-dark tl-btn-lg" data-auth-open="register"' + roleAttr + ">" + esc(employer ? t.registerEmployer : t.register) + "</button>" +
            "</div>" +
          "</div>" +
        "</div>";
    }

    function existingAppForJob(job) {
      if (!job) return null;
      return (state.myApps || []).find(function (a) {
        if (!a || a.status === "WITHDRAWN") return false;
        var j = a.job || {};
        return j.id === job.id || j.slug === job.slug || a.job_id === job.id;
      }) || null;
    }
    function applyCta(job, opts) {
      opts = opts || {};
      if (!job || job.available === false) return "";
      var existing = existingAppForJob(job);
      if (existing) {
        return '<button type="button" class="tl-btn" data-nav="application" data-id="' + esc(existing.id) + '">' + esc(t.viewApp) + "</button> ";
      }
      if (opts.detail) {
        return '<button type="button" class="tl-btn" id="acc-apply">' + esc(t.apply) + "</button> ";
      }
      return '<button type="button" class="tl-btn" data-quick-apply="' + esc(job.id || "") + '" data-slug="' + esc(job.slug || "") + '">' + esc(t.apply) + "</button> ";
    }
    function jobCard(job, extra) {
      job = job || {};
      var href = (isEn ? "/en/job-" : "/emploi-") + (job.slug || "") + ".html";
      var available = job.available !== false;
      var detailBtn = available
        ? '<button type="button" class="tl-btn tl-btn-ghost" data-nav="job" data-id="' + esc(job.slug || job.id) + '">' + esc(t.jobDetail) + "</button>"
        : '<span class="tl-save-hint">' + esc(t.jobUnavailable) + "</span>";
      var applyBtn = applyCta(job);
      var pills = "";
      if (job.location) pills += '<li><i class="fa-solid fa-location-dot" aria-hidden="true"></i><span>' + esc(job.location) + "</span></li>";
      if (job.salary_display || job.salary) pills += '<li class="is-pay"><i class="fa-solid fa-coins" aria-hidden="true"></i><span>' + esc(job.salary_display || job.salary) + "</span></li>";
      if (job.schedule) pills += '<li><i class="fa-solid fa-clock" aria-hidden="true"></i><span>' + esc(job.schedule) + "</span></li>";
      if (job.shift) pills += '<li><i class="fa-solid fa-layer-group" aria-hidden="true"></i><span>' + esc(job.shift) + "</span></li>";
      return '<article class="tl-list-card tl-job-card is-portal">' +
        '<div class="tl-job-card-banner"><span class="tl-job-card-icon" aria-hidden="true"><i class="fa-solid fa-briefcase"></i></span>' +
        '<div class="tl-job-card-banner-text"><p class="tl-job-card-cat">' + esc(job.company_name || "Talendus") + "</p>" +
        '<p class="tl-job-card-via">' + esc(statusLabel(job.status || "PUBLISHED")) + "</p></div></div>" +
        '<div class="tl-job-card-body">' +
        '<div class="tl-job-card-top">' +
        (job.contract_type ? '<span class="tl-chip orange">' + esc(job.contract_type) + "</span>" : "") +
        (job.saved ? '<span class="tl-chip">' + esc(t.unbookmark) + "</span>" : "") + "</div>" +
        "<h3>" + esc(job.title || "") + "</h3>" +
        (pills ? '<ul class="tl-job-pills">' + pills + "</ul>" : "") +
        (extra || "") +
        '<p class="tl-job-card-actions">' + applyBtn + detailBtn +
        (available && job.slug ? ' <a class="tl-split-cta" href="' + href + '">' + (isEn ? "Public page →" : "Page publique →") + "</a>" : "") +
        "</p></div></article>";
    }

    function renderCandidateDashboard(user, dash, profile) {
      var c = (dash && dash.completeness) || (profile && profile.completeness) || { percent: 0 };
      var s = (dash && dash.stats) || {};
      var stats = [["applications", t.apps, s.applications], ["in_progress", t.inProgress, s.in_progress],
        ["interviews", t.upcoming, s.interviews], ["saved_jobs", t.savedJobs, s.saved_jobs]];
      var primary = ((profile && profile.resumes) || []).filter(function (r) { return r.is_primary; })[0];
      var html = "";
      if ((c.percent || 0) < 70) {
        html += '<div class="tl-onboard"><b>' + esc(t.onboard) + "</b>, " + esc(c.percent || 0) + " % · " +
          '<button type="button" class="tl-text-btn" data-nav="profile">' + esc(t.quickProfile) + "</button></div>";
      }
      html += "<p class=\"tl-lead\">" + esc(t.hello) + " " + esc(user.first_name || "") + "</p>" +
        "<p>" + esc(t.completeness) + ", <b>" + esc(c.percent || 0) + " %</b></p><div class=\"tl-progress\"><i style=\"width:" + (c.percent || 0) + "%\"></i></div>" +
        '<div class="tl-stat-grid">' + stats.map(function (row) {
          return '<div class="tl-stat-card"><b>' + esc(row[2] || 0) + "</b><span>" + esc(row[1]) + "</span></div>";
        }).join("") + "</div><div class=\"tl-quick-actions\">" +
        '<button type="button" class="tl-btn" data-nav="jobs">' + esc(t.quickSearch) + "</button>" +
        '<button type="button" class="tl-btn tl-btn-ghost" data-nav="profile">' + esc(t.quickProfile) + "</button>" +
        (primary ? '<button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(primary.download_path) + '" data-dl-name="' + esc(primary.original_name || "cv.pdf") + '">' + esc(t.quickCv) + "</button>" : "") +
        '<button type="button" class="tl-btn tl-btn-ghost" data-nav="apps">' + esc(t.quickApps) + "</button></div>";
      var notifs = (dash && dash.notifications) || [];
      html += "<h3>" + esc(t.notifs) + "</h3>" + (notifs.length ? notifs.map(function (n) {
        return '<div class="tl-account-notif' + (n.is_read ? "" : " is-unread") + '"><b>' + esc(n.title) + "</b><p>" + esc(n.message) + "</p></div>";
      }).join("") : empty(t.emptyNotifs));
      var matches = (dash && dash.matches) || [];
      html += "<h3>" + esc(t.jobs) + "</h3>" + (matches.length ? '<div class="tl-list-cards">' + matches.map(function (m) {
        return jobCard(m.job || m, '<span class="tl-match-score">' + esc((m.score || 0) + " %") + "</span>");
      }).join("") : empty(t.emptyJobs));
      return html;
    }

    function profileForm(user, profile) {
      profile = profile || {};
      var exp = (profile.experiences || []).map(function (e) {
        return "<li>" + esc(e.role) + ", " + esc(e.company) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-exp="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>" + esc(t.emptyDocs) + "</li>";
      var edu = (profile.education || []).map(function (e) {
        return "<li>" + esc(e.diploma || "") + ", " + esc(e.school) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-edu="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>" + esc(t.emptyDocs) + "</li>";
      var certs = (profile.certifications || []).map(function (e) {
        return "<li>" + esc(e.name) + ' <button type="button" class="tl-btn tl-btn-ghost" data-del-cert="' + esc(e.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>" + esc(t.emptyDocs) + "</li>";
      return '<p class="tl-meta">' + esc(t.updated) + " : " + esc(fmtDate(profile.updated_at)) + "</p>" +
        '<form class="tl-form" id="acc-avatar"><label>' + esc(t.photo) + '</label><input name="file" type="file" accept="image/jpeg,image/png,image/webp,image/*">' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>' +
        '<form class="tl-form" id="acc-profile"><div class="tl-row-2"><div><label>' + esc(t.first) + '</label><input name="first_name" value="' + esc(user.first_name || "") + '"></div>' +
        "<div><label>" + esc(t.last) + '</label><input name="last_name" value="' + esc(user.last_name || "") + '"></div></div>' +
        "<label>" + esc(t.email) + '</label><input value="' + esc(user.email || "") + '" disabled class="tl-disabled">' +
        "<label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(user.phone || "") + '">' +
        "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(profile.address || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.city) + '</label>' + choiceSelect("city", (jobOptions || {}).locations, profile.city, t.pick) + '</div>' +
        "<div><label>" + esc(t.province) + '</label>' + choiceSelect("province", (jobOptions || {}).provinces, profile.province || "Québec", t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.country) + '</label>' + choiceSelect("country", (jobOptions || {}).countries, profile.country || "Canada", t.pick) + '</div>' +
        "<div><label>" + esc(t.birth) + '</label><input name="birth_date" type="date" value="' + esc(profile.birth_date || "") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.title) + '</label>' + choiceSelect("title", (jobOptions || {}).occupations, profile.title, t.pick) + '</div>' +
        "<div><label>" + esc(t.experience) + '</label><input name="years_experience" type="number" min="0" value="' + esc(profile.years_experience || "") + '"></div></div>' +
        "<label>" + esc(t.workStatus) + '</label>' + choiceSelect("work_status", (jobOptions || {}).work_statuses, profile.work_status, t.pick) +
        "<label>" + esc(t.sector) + '</label>' + choiceSelect("sector", (jobOptions || {}).sectors, profile.sector, t.pick) +
        "<label>" + esc(t.bio) + '</label><textarea name="bio" rows="4">' + esc(profile.bio || "") + "</textarea>" +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(profile.skills || "") + '">' +
        choiceGroup("languages", (jobOptions || {}).language_choices || (jobOptions || {}).languages, profile.languages, t.languages) +
        '<div class="tl-row-2"><div><label>' + esc(t.availability) + '</label>' + choiceSelect("availability", (jobOptions || {}).availability, profile.availability, t.pick) + '</div></div>' +
        choiceGroup("contract_type", (jobOptions || {}).contract_types, profile.contract_type, t.contract) +
        choiceGroup("shift_preference", (jobOptions || {}).shifts, profile.shift_preference, t.shiftLabel) +
        "<label>" + esc(t.mobility) + '</label>' + choiceSelect("mobility", (jobOptions || {}).mobility, profile.mobility, t.pick) +
        '<div class="tl-row-2"><div><label>' + esc(t.desiredSalary) + '</label><input name="desired_salary_min" type="number" value="' + esc(profile.desired_salary_min || "") + '"></div><div></div></div>' +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>' +
        "<h3>" + (isEn ? "Experience" : "Expériences") + "</h3><ul>" + exp + "</ul>" +
        '<form class="tl-form" id="acc-exp"><div class="tl-row-2"><input name="company" placeholder="' + esc(t.company) + '" required><input name="role" placeholder="' + esc(t.title) + '" required></div>' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>" +
        "<h3>" + (isEn ? "Education" : "Formations") + "</h3><ul>" + edu + "</ul>" +
        '<form class="tl-form" id="acc-edu"><div class="tl-row-2"><input name="school" required><input name="diploma"></div>' +
        '<button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>" +
        "<h3>" + esc(t.certs) + "</h3><ul>" + certs + "</ul>" +
        '<form class="tl-form" id="acc-cert"><input name="name" required><button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.add) + "</button></form>";
    }

    function bindFileForm(form, send) {
      if (!form) return;
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        send(form);
      });
      var input = form.querySelector('input[type="file"]');
      if (input) input.addEventListener("change", function () {
        if (input.files && input.files[0]) send(form);
      });
    }
    function bindProfile(user) {
      var form = document.getElementById("acc-profile");
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(form).entries());
        d.languages = formChoice(form, "languages");
        d.contract_type = formChoice(form, "contract_type");
        d.shift_preference = formChoice(form, "shift_preference");
        Promise.all([
          api.request("/users/me", { method: "PATCH", body: { first_name: d.first_name, last_name: d.last_name, phone: d.phone } }),
          api.request("/candidates/me", { method: "PATCH", body: {
            city: d.city, address: d.address, province: d.province, country: d.country, birth_date: d.birth_date,
            title: d.title, sector: d.sector, skills: d.skills, bio: d.bio, languages: d.languages,
            availability: d.availability, contract_type: d.contract_type, shift_preference: d.shift_preference,
            years_experience: d.years_experience ? Number(d.years_experience) : null,
            desired_salary_min: d.desired_salary_min ? Number(d.desired_salary_min) : null, mobility: d.mobility,
            work_status: d.work_status
          } })
        ]).then(function () { flash(form.querySelector(".tl-success"), t.saved, true); }).catch(function (err) {
          flash(form.querySelector(".tl-success"), (err && err.message) || t.err, false);
        });
      });
      bindFileForm(document.getElementById("acc-avatar"), function (av) {
        if (av.getAttribute("data-busy") === "1") return;
        var file = av.querySelector("[name=file]").files[0];
        if (!file) return;
        av.setAttribute("data-busy", "1");
        var fd = new FormData();
        api.appendFile(fd, file, "photo.jpg");
        api.request("/users/me/avatar", { method: "POST", body: fd }).then(function (json) {
          flash(av.querySelector(".tl-success"), t.uploaded, true);
          if (json && json.data) {
            try { localStorage.setItem("talendus_user", JSON.stringify(Object.assign(api.currentUser() || {}, json.data))); } catch (err) {}
          }
          window.__tlAvatarUrl = "";
          if (window.TalendusAuth && window.TalendusAuth.paint) window.TalendusAuth.paint();
        }).catch(function (err) {
          av.removeAttribute("data-busy");
          flash(av.querySelector(".tl-success"), (err && err.message) || t.err, false);
        });
      });
      function postList(id, path) {
        var f = document.getElementById(id);
        if (!f) return;
        f.addEventListener("submit", function (e) {
          e.preventDefault();
          api.request(path, { method: "POST", body: Object.fromEntries(new FormData(f).entries()) }).then(function () { go("profile"); }).catch(function () {});
        });
      }
      postList("acc-exp", "/candidates/me/experiences");
      postList("acc-edu", "/candidates/me/education");
      postList("acc-cert", "/candidates/me/certifications");
      root.querySelectorAll("[data-del-exp]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/experiences/" + b.getAttribute("data-del-exp"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
      root.querySelectorAll("[data-del-edu]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/education/" + b.getAttribute("data-del-edu"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
      root.querySelectorAll("[data-del-cert]").forEach(function (b) { b.onclick = function () { api.request("/candidates/me/certifications/" + b.getAttribute("data-del-cert"), { method: "DELETE" }).then(function () { go("profile"); }); }; });
    }

    function renderJobsSearch(payload) {
      var items = (payload && payload.data) || payload || [];
      var meta = (payload && payload.meta) || {};
      var f = state.jobFilters || {};
      function fv(name) { return f[name] || ""; }
      var o = jobOptions || {};
      var sort = f.sort || "relevance";
      var html = '<form class="tl-filters" id="acc-job-filters">' +
        "<div><label>" + esc(t.search) + '</label><input name="q" value="' + esc(fv("q")) + '"></div>' +
        "<div><label>" + esc(t.occupation) + "</label>" + choiceSelect("title", o.occupations, fv("title"), t.pick) + "</div>" +
        "<div><label>" + esc(t.location) + "</label>" + choiceSelect("location", o.locations, fv("location"), t.pick) + "</div>" +
        "<div><label>" + esc(t.sector) + "</label>" + choiceSelect("sector", o.sectors, fv("sector"), t.pick) + "</div>" +
        "<div><label>" + esc(t.contract) + "</label><p class=\"tl-field-hint\">" + esc(t.contractHint) + "</p>" + choiceSelect("contract_type", o.contract_types, fv("contract_type"), t.pick) + "</div>" +
        "<div><label>" + esc(t.shiftLabel) + "</label><p class=\"tl-field-hint\">" + esc(t.shiftHint) + "</p>" + choiceSelect("shift", o.shifts, fv("shift"), t.pick) + "</div>" +
        "<div><label>" + esc(t.hours) + "</label><p class=\"tl-field-hint\">" + esc(t.hoursHint) + "</p>" + choiceSelect("schedule", o.schedules, fv("schedule"), t.pick) + "</div>" +
        "<div><label>" + esc(t.workMode) + "</label>" + choiceSelect("work_mode", o.work_modes, fv("work_mode"), t.pick) + "</div>" +
        "<div><label>" + esc(t.experience) + "</label>" + choiceSelect("experience", o.experience_levels, fv("experience"), t.pick) + "</div>" +
        "<div><label>" + esc(t.workAuth) + "</label>" + choiceSelect("work_authorization", o.work_requirements, fv("work_authorization"), t.pick) + "</div>" +
        "<div><label>" + esc(t.sponsorYes) + "</label>" + choiceSelect("can_sponsor", o.sponsor_filters, fv("can_sponsor"), t.pick) + "</div>" +
        "<div><label>" + esc(t.salary) + '</label><input name="salary_min" type="number" value="' + esc(fv("salary_min")) + '"></div>' +
        "<div><label>" + esc(t.sort) + '</label><select name="sort">' +
        [["relevance", isEn ? "Relevance" : "Pertinence"], ["published_at", isEn ? "Date" : "Date"], ["salary", isEn ? "Salary" : "Salaire"]].map(function (opt) {
          return '<option value="' + opt[0] + '"' + (sort === opt[0] ? " selected" : "") + ">" + esc(opt[1]) + "</option>";
        }).join("") + "</select></div>" +
        '<div><button class="tl-btn" type="submit">' + esc(t.search) + "</button></div></form>";
      if (payload && payload.error) html += errBox(payload.error);
      else if (!items.length) html += empty(t.noResults);
      else html += '<div class="tl-list-cards">' + items.map(function (j) { return jobCard(j); }).join("") + "</div>";
      if (meta.pages > 1) {
        html += '<div class="tl-pager"><button type="button" class="tl-btn tl-btn-ghost" data-page="' + Math.max(1, (meta.page || 1) - 1) + '">' + esc(t.prev) +
          "</button><span>" + esc(t.page) + " " + (meta.page || 1) + " " + esc(t.of) + " " + meta.pages + '</span><button type="button" class="tl-btn tl-btn-ghost" data-page="' +
          Math.min(meta.pages, (meta.page || 1) + 1) + '">' + esc(t.next) + "</button></div>";
      }
      html += "<h3>" + esc(t.savedJobs) + "</h3><div id=\"acc-saved-jobs\">" + skeleton() + "</div>";
      return html;
    }

    function renderSavedJobs(items) {
      if (!items || !items.length) return empty(t.emptySaved);
      return '<div class="tl-list-cards">' + items.map(function (j) { return jobCard(j); }).join("") + "</div>";
    }

    function renderAlerts(items) {
      var list = (!items || !items.length) ? empty(t.emptyAlerts) : items.map(function (a) {
        return '<div class="tl-account-notif"><b>' + esc(a.keywords || a.city || a.sector || t.alerts) + "</b><p>" +
          esc([a.city, a.province, a.sector, a.contract_type].filter(Boolean).join(" · ")) +
          '</p><p><button type="button" class="tl-btn tl-btn-ghost" data-del-alert="' + esc(a.id) + '">' + esc(t.remove) + "</button></p></div>";
      }).join("");
      return '<form class="tl-form" id="acc-alert"><h3>' + esc(t.createAlert) + "</h3><label>" + esc(t.keywords) +
        '</label><input name="keywords"><div class="tl-row-2"><div><label>' + esc(t.city) + '</label>' +
        choiceSelect("city", (jobOptions || {}).locations, "", t.pick) + '</div>' +
        "<div><label>" + esc(t.sector) + '</label>' + choiceSelect("sector", (jobOptions || {}).sectors, "", t.pick) +
        "</div></div><button class=\"tl-btn\" type=\"submit\">" +
        esc(t.add) + '</button><div class="tl-success"></div></form>' + list;
    }

    function bindJobsSearch() {
      var form = document.getElementById("acc-job-filters");
      if (!form && !document.getElementById("acc-saved-jobs")) return;
      function load(page) {
        var d = form ? Object.fromEntries(new FormData(form).entries()) : (state.jobFilters || {});
        var params = new URLSearchParams();
        ["q", "title", "location", "sector", "contract_type", "experience", "salary_min", "sort", "shift", "schedule", "work_mode", "work_authorization", "can_sponsor"].forEach(function (k) {
          var v = d[k];
          if (v) params.set(k, v);
        });
        params.set("page", page || d.page || 1);
        state.jobFilters = Object.assign({}, d, { page: page || d.page || 1 });
        api.request("/jobs?" + params.toString()).then(function (json) {
          state.jobs = json;
          go("jobs");
        }).catch(function (err) {
          state.jobs = { data: [], meta: {}, error: (err && err.message) || t.err };
          go("jobs");
        });
      }
      if (form) form.addEventListener("submit", function (e) { e.preventDefault(); load(1); });
      root.querySelectorAll("[data-page]").forEach(function (b) { b.onclick = function () { load(b.getAttribute("data-page")); }; });
      if (!document.getElementById("acc-saved-jobs")) return;
      api.request("/jobs/saved").then(function (json) {
        var box = document.getElementById("acc-saved-jobs");
        if (!box) return;
        var items = json.data || [];
        box.innerHTML = items.length ? '<div class="tl-list-cards">' + items.map(function (j) { return jobCard(j); }).join("") + "</div>" : empty(t.emptySaved);
        root.querySelectorAll("[data-nav]").forEach(function (btn) {
          btn.onclick = function () { go(btn.getAttribute("data-nav"), btn.getAttribute("data-id") || ""); };
        });
        root.querySelectorAll("[data-quick-apply]").forEach(function (btn) {
          btn.onclick = function () {
            api.request("/applications", {
              method: "POST",
              body: { job_id: btn.getAttribute("data-quick-apply") || null, job_slug: btn.getAttribute("data-slug") || null }
            }).then(function () { state.appsReady = false; go("apps"); }).catch(function (err) { window.alert((err && err.message) || t.err); });
          };
        });
      }).catch(function (err) {
        var box = document.getElementById("acc-saved-jobs");
        if (box) box.innerHTML = errBox((err && err.message) || t.err);
      });
    }

    function renderJobDetail(job) {
      if (!job) return empty(t.err);
      return '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="jobs">' + (isEn ? "Back" : "Retour") + "</button></p>" +
        '<span class="tl-chip orange">' + esc(job.contract_type || "") + "</span><h3>" + esc(job.title) + "</h3>" +
        '<p class="tl-meta">' + esc(job.company_name || "") + " · " + esc(job.location || "") + " · " + esc(job.salary_display || "") + "</p>" +
        jobFacts(job) +
        "<p>" + esc(job.description || "") + "</p>" +
        (job.responsibilities ? "<h4>" + esc(t.responsibilities) + "</h4><p>" + esc(job.responsibilities) + "</p>" : "") +
        (job.skills ? "<h4>" + esc(t.skills) + "</h4><p>" + esc(job.skills) + "</p>" : "") +
        (job.experience_level ? "<p>" + esc(t.experience) + " : " + esc(job.experience_level) + "</p>" : "") +
        "<p>" + esc(t.updated) + " : " + esc(fmtDate(job.published_at)) + (job.expires_at ? " · " + esc(t.deadline) + " " + esc(fmtDate(job.expires_at)) : "") + "</p>" +
        (existingAppForJob(job)
          ? '<p class="tl-lead">' + esc(t.alreadyApplied) + "</p><p>" + applyCta(job)
          : "<label>" + esc(t.cover) + '</label><textarea id="acc-cover" maxlength="4000" rows="4"></textarea>' +
            "<p>" + applyCta(job, { detail: true })) +
        '<button type="button" class="tl-btn tl-btn-ghost" id="acc-save-job">' + esc(job.saved ? t.unbookmark : t.bookmark) + "</button></p>" +
        '<div class="tl-success" id="acc-job-msg"></div>';
    }

    function timeline(app) {
      var tracker = (app && app.tracker) || {};
      var steps = tracker.steps || [];
      if (steps.length) {
        var html = '<ol class="tl-timeline">';
        steps.forEach(function (step) {
          var cls = step.state === "done" ? "is-done" : (step.state === "current" ? "is-current" : "");
          html += '<li class="' + cls + '"><b>' + esc(statusLabel(step.key)) + "</b>" +
            (step.at ? '<span class="tl-meta">' + esc(fmtDate(step.at)) + "</span>" : "") + "</li>";
        });
        html += "</ol>";
        if (tracker.outcome) html += '<p class="tl-chip orange">' + esc(statusLabel(tracker.outcome)) + "</p>";
        return html;
      }
      var fallback = [
        ["SUBMITTED", t.sent], ["UNDER_REVIEW", t.review], ["SHORTLISTED", t.preselect],
        ["INTERVIEW", t.interview], ["SECOND_INTERVIEW", t.secondInterview], ["OFFER_SENT", t.offerSent], ["HIRED", t.decision]
      ];
      var order = ["SUBMITTED", "RECEIVED", "UNDER_REVIEW", "SHORTLISTED", "INTERVIEW", "SECOND_INTERVIEW", "OFFER_SENT", "HIRED"];
      var cur = order.indexOf(app.status);
      if (app.status === "REJECTED" || app.status === "WITHDRAWN") cur = -1;
      return '<ol class="tl-timeline">' + fallback.map(function (st) {
        var idx = order.indexOf(st[0]);
        var cls = cur >= idx ? "is-done" : "";
        if (app.status === st[0] || (st[0] === "UNDER_REVIEW" && app.status === "RECEIVED")) cls = "is-current";
        if (app.status === "HIRED" && st[0] === "HIRED") cls = "is-done";
        return '<li class="' + cls + '"><b>' + esc(st[1]) + "</b></li>";
      }).join("") + "</ol>";
    }

    function renderApps(apps) {
      if (!apps || !apps.length) return empty(t.emptyApps);
      return '<div class="tl-list-cards">' + apps.map(function (a) {
        var job = a.job || {};
        return '<article class="tl-list-card"><span class="tl-chip orange">' + esc(statusLabel(a.status)) + "</span>" +
          "<h3>" + esc(job.title || "") + "</h3><p class=\"tl-meta\">" + esc(job.company_name || "") + " · " + esc(fmtDate(a.created_at)) +
          " · " + esc(t.updated) + " " + esc(fmtDate(a.updated_at)) + "</p>" +
          timeline(a) +
          '<button type="button" class="tl-btn tl-btn-ghost" data-nav="application" data-id="' + esc(a.id) + '">' + esc(t.appDetail) + "</button></article>";
      }).join("") + "</div>";
    }

    function renderAppDetail(a) {
      var job = (a && a.job) || {};
      var canWithdraw = a && ["SUBMITTED", "RECEIVED", "UNDER_REVIEW", "SHORTLISTED"].indexOf(a.status) >= 0;
      return '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="apps">' + (isEn ? "Back" : "Retour") + "</button></p>" +
        "<h3>" + esc(job.title || "") + "</h3><p class=\"tl-meta\">" + esc(job.company_name || "") + " · " + esc(statusLabel(a.status)) + "</p>" +
        timeline(a) + (canWithdraw ? '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-withdraw">' + esc(t.withdraw) + "</button></p>" : "");
    }

    function renderNotifs(notifs) {
      if (!notifs || !notifs.length) return empty(t.emptyNotifs);
      return '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-readall">' + esc(t.markAll) + "</button></p><div class=\"tl-account-notifs\">" +
        notifs.map(function (n) {
          var href = localizeHref(n.href);
          return '<div class="tl-account-notif' + (n.is_read ? "" : " is-unread") + (href ? " is-clickable" : "") + '" data-open-notif="' + esc(n.id) + '" data-href="' + esc(href) + '"><b>' + esc(n.title) + "</b><p>" + esc(n.message) +
            "</p><p class=\"tl-meta\">" + esc(fmtDate(n.created_at)) + (n.is_read ? "" : ' · <button type="button" class="tl-btn tl-btn-ghost" data-read="' + esc(n.id) + '">' + esc(t.markRead) + "</button>") + "</p></div>";
        }).join("") + "</div>";
    }

    function renderMessages(threads, directory, thread) {
      var opts = (directory || []).map(function (p) {
        return '<option value="' + esc(p.id) + '">' + esc((p.first_name || "") + " " + (p.last_name || "") + ", " + statusLabel(p.role || "")) + "</option>";
      }).join("");
      var list = (!threads || !threads.length) ? empty(t.emptyMsgs) : threads.map(function (th) {
        return '<button type="button" class="tl-account-notif' + (th.unread ? " is-unread" : "") + '" data-open-thread="' + esc(th.user_id) + '"><b>' +
          esc((th.first_name || "") + " " + (th.last_name || "")) + "</b><p>" + esc(th.last_message || "") + " · " + esc(fmtDate(th.last_at)) + "</p></button>";
      }).join("");
      var msgs = (thread || []).map(function (m) {
        var mine = state.user && m.sender_id === state.user.id;
        return '<div class="tl-msg-bubble' + (mine ? " is-mine" : "") + '"><b>' + esc(m.sender_name || "") + "</b><p>" + esc(m.body) +
          '</p><p class="tl-meta">' + esc(fmtDate(m.created_at)) + (m.is_read ? "" : " · " + (isEn ? "Unread" : "Non lu")) + "</p></div>";
      }).join("");
      return (isEmployerSpace() || (state.user && state.user.role === "CANDIDATE") ? mediateNote() : "") +
        '<div class="tl-msg-layout"><div>' + list + "</div>" +
        (opts
          ? '<form class="tl-form" id="acc-msg"><label>' + esc(t.writeTalendus) +
            '</label><select name="recipient_id" required>' + opts + "</select><label>" + esc(t.write) +
            '</label><textarea name="body" rows="4" required maxlength="4000"></textarea><button class="tl-btn" type="submit">' +
            esc(t.send) + '</button><div class="tl-success" role="status"></div><div id="acc-thread">' + msgs + "</div></form>"
          : '<div><p class="tl-lead">' + esc(t.writeTalendus) + "</p><p class=\"tl-meta\">" + esc(t.emptyDirectory) +
            '</p><div id="acc-thread">' + msgs + "</div></div>") +
        "</div>";
    }

    function bindMessages() {
      var form = document.getElementById("acc-msg");
      if (form) form.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(form).entries());
        api.request("/messages", { method: "POST", body: { recipient_id: d.recipient_id, body: d.body } }).then(function () { go("messages"); })
          .catch(function (err) { flash(form.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      root.querySelectorAll("[data-open-thread]").forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute("data-open-thread");
          var select = root.querySelector("#acc-msg [name=recipient_id]");
          if (select) select.value = id;
          api.request("/messages/" + id).then(function (json) {
            state.thread = json.data || [];
            go("messages");
          });
        };
      });
    }

    function renderDocs(docs, resumes) {
      var list = (docs || []).map(function (d) {
        return "<li>" + esc(d.original_name) + " · " + esc(d.kind) + ' <button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(d.download_path) + '" data-dl-name="' + esc(d.original_name) + '">' + esc(t.download) +
          '</button> <button type="button" class="tl-btn tl-btn-ghost" data-del-doc="' + esc(d.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>" + esc(t.emptyDocs) + "</li>";
      var cvs = (resumes || []).map(function (r) {
        return "<li>" + esc(r.original_name) + (r.is_primary ? " · CV" : "") +
          ' <button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(r.download_path) + '" data-dl-name="' + esc(r.original_name) + '">' + esc(t.download) + "</button>" +
          ' <button type="button" class="tl-btn tl-btn-ghost" data-del-cv="' + esc(r.id) + '">' + esc(t.remove) + "</button></li>";
      }).join("") || "<li>" + esc(t.emptyDocs) + "</li>";
      return "<h3>CV</h3><ul>" + cvs + '</ul><form class="tl-form" id="acc-cv"><label>' + esc(t.upload) +
        '</label><input name="file" type="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/jpeg,image/png,image/webp" required><button class="tl-btn" type="submit">' +
        esc(t.replace) + '</button><div class="tl-success"></div></form><h3>' + esc(t.otherDocs) + "</h3><ul>" + list +
        '</ul><form class="tl-form" id="acc-doc"><label>' + esc(t.upload) + '</label><input name="file" type="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/jpeg,image/png,image/webp" required>' +
        '<select name="kind"><option value="cover_letter">' + esc(t.cover) + '</option><option value="certification">' +
        esc(t.certs) + '</option><option value="other">' + esc(t.otherDocs) + "</option></select>" +
        '<button class="tl-btn" type="submit">' + esc(t.add) + '</button><div class="tl-success"></div></form>';
    }

    function bindDocs() {
      bindFileForm(document.getElementById("acc-cv"), function (cv) {
        if (cv.getAttribute("data-busy") === "1") return;
        var file = cv.querySelector("[name=file]").files[0];
        if (!file) return;
        cv.setAttribute("data-busy", "1");
        var fd = new FormData();
        api.appendFile(fd, file, "cv.pdf");
        api.request("/candidates/me/resume", { method: "POST", body: fd }).then(function () { go("documents"); })
          .catch(function (err) {
            cv.removeAttribute("data-busy");
            flash(cv.querySelector(".tl-success"), (err && err.message) || t.err, false);
          });
      });
      bindFileForm(document.getElementById("acc-doc"), function (doc) {
        if (doc.getAttribute("data-busy") === "1") return;
        var file = doc.querySelector("[name=file]").files[0];
        if (!file) return;
        doc.setAttribute("data-busy", "1");
        var fd = new FormData();
        api.appendFile(fd, file, "document.pdf");
        fd.append("kind", doc.querySelector("[name=kind]").value);
        api.request("/documents", { method: "POST", body: fd }).then(function () { go("documents"); })
          .catch(function (err) {
            doc.removeAttribute("data-busy");
            flash(doc.querySelector(".tl-success"), (err && err.message) || t.err, false);
          });
      });
      root.querySelectorAll("[data-del-cv]").forEach(function (b) {
        b.onclick = function () { api.request("/candidates/me/resume/" + b.getAttribute("data-del-cv"), { method: "DELETE" }).then(function () { go("documents"); }); };
      });
      root.querySelectorAll("[data-del-doc]").forEach(function (b) {
        b.onclick = function () { api.request("/documents/" + b.getAttribute("data-del-doc"), { method: "DELETE" }).then(function () { go("documents"); }); };
      });
    }

    function roleAccessHint(role) {
      var map = {
        OWNER: t.roleHintOwner,
        ADMIN: t.roleHintAdmin,
        HR: t.roleHintHr,
        RECRUITER: t.roleHintRecruiter,
        BILLING: t.roleHintBilling,
        MEMBER: t.roleHintMember
      };
      return map[role] || t.yourAccessHint;
    }

    function settingsTabs(canTeam) {
      var tabs = [
        ["account", t.settingsAccount, "fa-id-card"],
        ["notifications", t.settingsNotifs, "fa-bell"]
      ];
      if (!isEmployerSpace()) tabs.push(["privacy", t.privacy, "fa-shield-halved"]);
      tabs.push(["security", t.security, "fa-lock"]);
      if (isEmployerSpace() && canTeam) tabs.push(["team", t.settingsTeam, "fa-users"]);
      return tabs;
    }

    function settingsActiveTab(canTeam) {
      var id = currentRoute().id || "account";
      var allowed = settingsTabs(canTeam).map(function (x) { return x[0]; });
      return allowed.indexOf(id) !== -1 ? id : "account";
    }

    function settingsCheck(name, on, label, hint) {
      return '<label class="tl-settings-check"><input type="checkbox" name="' + name + '"' + (on ? " checked" : "") + ">" +
        "<span><b>" + esc(label) + "</b>" + (hint ? "<small>" + esc(hint) + "</small>" : "") + "</span></label>";
    }

    function settingsCard(title, hint, inner, extraClass) {
      return '<section class="tl-settings-card' + (extraClass ? " " + extraClass : "") + '"><div class="tl-settings-card-head"><h2>' +
        esc(title) + "</h2>" + (hint ? "<p>" + esc(hint) + "</p>" : "") + "</div>" + inner + "</section>";
    }

    function renderSettings(prefs, extras) {
      prefs = prefs || {};
      extras = extras || {};
      var user = state.user || {};
      var company = extras.company || {};
      var members = extras.members || [];
      var canTeam = !!company.can_manage_members;
      var memberRole = company.member_role || "";
      var tab = settingsActiveTab(canTeam);
      var name = ((user.first_name || "") + " " + (user.last_name || "")).trim() || user.email;
      var persona = isEmployerSpace() ? (isEn ? "Employer workspace" : "Espace entreprise") : (isEn ? "Candidate workspace" : "Espace candidat");
      var tabs = settingsTabs(canTeam).map(function (it) {
        return '<button type="button" class="tl-settings-tab' + (tab === it[0] ? " is-active" : "") + '" data-settings-tab="' + it[0] + '">' +
          '<i class="fa-solid ' + it[2] + '" aria-hidden="true"></i>' + esc(it[1]) + "</button>";
      }).join("");
      var body = "";
      if (tab === "account") {
        var links = isEmployerSpace()
          ? '<p class="tl-settings-links"><button type="button" class="tl-btn tl-btn-ghost" data-nav="company">' + esc(t.openCompany) + "</button>" +
            (company.can_read_invoices ? ' <button type="button" class="tl-btn tl-btn-ghost" data-nav="invoices">' + esc(t.openBilling) + "</button>" : "") + "</p>"
          : '<p class="tl-settings-links"><button type="button" class="tl-btn tl-btn-ghost" data-nav="profile">' + esc(t.openProfile) + "</button></p>";
        var roleBox = isEmployerSpace()
          ? '<div class="tl-settings-role"><span class="tl-chip orange">' + esc(statusLabel(memberRole || "MEMBER")) + "</span><p>" +
            esc(roleAccessHint(memberRole)) + "</p></div>"
          : "";
        body = settingsCard(t.settingsAccount, t.changeEmail,
          '<div class="tl-settings-identity"><div><b>' + esc(name) + "</b><span>" + esc(user.email || "") +
          "</span><span>" + esc(persona) + "</span></div></div>" + roleBox + links +
          '<p class="tl-meta">' + esc(t.settingsEmailLocked) + "</p>") +
          settingsCard(t.settingsLang, "",
            '<form class="tl-form" id="acc-locale"><label class="tl-settings-radio"><input type="radio" name="locale" value="fr-CA"' +
            (prefs.locale !== "en-CA" ? " checked" : "") + "> " + esc(t.settingsLangFr) + "</label>" +
            '<label class="tl-settings-radio"><input type="radio" name="locale" value="en-CA"' +
            (prefs.locale === "en-CA" ? " checked" : "") + "> " + esc(t.settingsLangEn) + "</label>" +
            '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>');
      } else if (tab === "notifications") {
        var events = isEmployerSpace()
          ? settingsCheck("notify_application", prefs.notify_application !== false, t.notifyPresented, t.notifyPresentedHint) +
            settingsCheck("notify_interview", prefs.notify_interview !== false, t.notifyInterview, t.notifyInterviewHint) +
            settingsCheck("notify_message", prefs.notify_message !== false, t.notifyMessage, t.notifyMessageHint)
          : settingsCheck("notify_match", prefs.notify_match !== false, t.notifyMatch, t.notifyMatchHint) +
            settingsCheck("notify_application", prefs.notify_application !== false, t.notifyApplication, t.notifyApplicationHint) +
            settingsCheck("notify_interview", prefs.notify_interview !== false, t.notifyInterview, t.notifyInterviewHint) +
            settingsCheck("notify_message", prefs.notify_message !== false, t.notifyMessage, t.notifyMessageHint);
        body = '<form class="tl-form" id="acc-prefs">' +
          settingsCard(t.settingsNotifs, "", events) +
          settingsCard(t.notifyChannels, t.notifyChannelsHint,
            settingsCheck("notify_email", prefs.notify_email !== false, t.emailNotif, "") +
            settingsCheck("notify_in_app", prefs.notify_in_app !== false, t.inApp, "") +
            settingsCheck("notify_push", !!prefs.notify_push, t.push, "")) +
          '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>';
      } else if (tab === "privacy") {
        body = '<form class="tl-form" id="acc-privacy">' +
          settingsCard(t.privacy, t.privacyHint,
            settingsCheck("privacy_profile_public", !!prefs.privacy_profile_public, t.privacyTalendus, t.mediateCandidate)) +
          '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>';
      } else if (tab === "security") {
        body = settingsCard(t.security, "",
          '<form class="tl-form" id="acc-pass"><label>' + esc(t.currentPass) + '</label><input name="current_password" type="password" required autocomplete="current-password">' +
          "<label>" + esc(t.newPass) + '</label><input name="new_password" type="password" required minlength="8" autocomplete="new-password">' +
          '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>') +
          '<div id="acc-sessions">' + settingsCard(t.sessions, t.sessionsHint, skeleton()) + "</div>" +
          '<div id="acc-login-log">' + settingsCard(t.loginLog, t.loginLogHint, skeleton()) + "</div>" +
          settingsCard(t.danger, isEmployerSpace() ? t.dangerHintEmployer : t.dangerHint,
            '<form class="tl-form" id="acc-del"><button class="tl-btn tl-btn-ghost" type="submit">' + esc(t.danger) +
            '</button><div class="tl-success"></div></form>', "is-danger");
      } else if (tab === "team") {
        body = renderMembers(members, canTeam);
      }
      return '<div class="tl-settings"><nav class="tl-settings-tabs" aria-label="' + esc(t.settings) + '">' + tabs + "</nav>" + body + "</div>";
    }

    function bindSettings() {
      root.querySelectorAll("[data-settings-tab]").forEach(function (btn) {
        btn.onclick = function () { go("settings", btn.getAttribute("data-settings-tab")); };
      });
      var pass = document.getElementById("acc-pass");
      if (pass) pass.addEventListener("submit", function (e) {
        e.preventDefault();
        var d = Object.fromEntries(new FormData(pass).entries());
        api.request("/auth/change-password", { method: "POST", body: d }).then(function () { flash(pass.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(pass.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      function savePrefs(form, keys) {
        var body = {};
        keys.forEach(function (k) {
          var el = form.querySelector("[name=" + k + "]");
          if (!el) return;
          if (el.type === "checkbox") body[k] = !!el.checked;
          else if (el.type === "radio") {
            var picked = form.querySelector("[name=" + k + "]:checked");
            if (picked) body[k] = picked.value;
          } else body[k] = el.value;
        });
        return api.request("/users/me/preferences", { method: "PATCH", body: body });
      }
      var locale = document.getElementById("acc-locale");
      if (locale) locale.addEventListener("submit", function (e) {
        e.preventDefault();
        savePrefs(locale, ["locale"]).then(function () {
          var picked = locale.querySelector("[name=locale]:checked");
          var wantEn = picked && picked.value === "en-CA";
          if (wantEn !== isEn) {
            var page = isEmployerSpace()
              ? (wantEn ? "/en/account-employer.html" : "/espace-employeur.html")
              : (wantEn ? "/en/account.html" : "/espace.html");
            window.location.href = page + "#/settings/account";
            return;
          }
          flash(locale.querySelector(".tl-success"), t.saved, true);
        }).catch(function (err) { flash(locale.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var prefs = document.getElementById("acc-prefs");
      if (prefs) prefs.addEventListener("submit", function (e) {
        e.preventDefault();
        savePrefs(prefs, ["notify_email", "notify_in_app", "notify_push", "notify_application", "notify_message", "notify_match", "notify_interview"])
          .then(function () { flash(prefs.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(prefs.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var privacy = document.getElementById("acc-privacy");
      if (privacy) privacy.addEventListener("submit", function (e) {
        e.preventDefault();
        savePrefs(privacy, ["privacy_profile_public"]).then(function () { flash(privacy.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(privacy.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var del = document.getElementById("acc-del");
      if (del) del.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!window.confirm(t.confirmDanger)) return;
        api.request("/users/me/deactivate", { method: "POST" })
          .then(function () { return api.logout(); })
          .then(renderGuest)
          .catch(function (err) { flash(del.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var sessBox = document.getElementById("acc-sessions");
      if (sessBox) {
        api.request("/auth/sessions").then(function (json) {
          var rows = json.data || [];
          sessBox.innerHTML = settingsCard(t.sessions, t.sessionsHint,
            '<p><button type="button" class="tl-btn tl-btn-ghost" id="acc-revoke-all">' + esc(t.revokeAll) + "</button></p>" +
            (rows.length ? rows.map(function (s) {
              return '<div class="tl-session-row"><span>' + esc(fmtDate(s.created_at)) + " · " +
                (s.active ? (isEn ? "Active" : "Active") : (isEn ? "Revoked" : "Révoquée")) +
                "</span>" + (s.active ? '<button type="button" class="tl-text-btn" data-revoke="' + esc(s.id) + '">' + esc(t.revoke) + "</button>" : "") + "</div>";
            }).join("") : '<p class="tl-meta">' + esc(t.noSessions) + "</p>"));
          var all = document.getElementById("acc-revoke-all");
          if (all) all.onclick = function () { api.request("/auth/sessions/revoke-all", { method: "POST" }).then(function () { go("settings", "security"); }); };
          sessBox.querySelectorAll("[data-revoke]").forEach(function (b) {
            b.onclick = function () { api.request("/auth/sessions/" + b.getAttribute("data-revoke"), { method: "DELETE" }).then(function () { go("settings", "security"); }); };
          });
        }).catch(function () { sessBox.innerHTML = settingsCard(t.sessions, t.sessionsHint, '<p class="tl-meta">' + esc(t.err) + "</p>"); });
      }
      var logBox = document.getElementById("acc-login-log");
      if (logBox) {
        api.request("/auth/login-events").then(function (json) {
          var rows = json.data || [];
          logBox.innerHTML = settingsCard(t.loginLog, t.loginLogHint, rows.length ? rows.map(function (ev) {
            return '<div class="tl-account-notif"><b>' + (ev.success ? (isEn ? "Signed in" : "Connexion") : (isEn ? "Failed" : "Échec")) +
              "</b><p>" + esc(fmtDate(ev.created_at)) + (ev.ip_address ? " · " + esc(ev.ip_address) : "") + "</p></div>";
          }).join("") : empty(t.emptyNotifs));
        }).catch(function () { logBox.innerHTML = ""; });
      }
    }

    function employerDashboard(user, dash, company) {
      var s = (dash && dash.stats) || {};
      return mediateNote() + "<p class=\"tl-lead\">" + esc(t.hello) + " " + esc((company && company.name) || dash.company_name || "") + "</p>" +
        "<p>" + esc(t.hiringLead) + "</p>" +
        '<div class="tl-stat-grid">' +
        [["active_jobs", t.activeJobs], ["applications", t.inbox], ["shortlisted", t.shortlisted], ["interviews", t.interviews], ["hired", t.hired]].map(function (row) {
          return '<div class="tl-stat-card"><b>' + esc(s[row[0]] || 0) + "</b><span>" + esc(row[1]) + "</span></div>";
        }).join("") + "</div><div class=\"tl-quick-actions\"><button type=\"button\" class=\"tl-btn\" data-nav=\"job-new\">" +
        esc(t.createJob) + "</button><button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-nav=\"jobs\">" + esc(t.hiring) +
        "</button><button type=\"button\" class=\"tl-btn tl-btn-ghost\" data-nav=\"inbox\">" + esc(t.candidates) + "</button>" +
        (company && company.can_read_invoices === false ? "" : '<button type="button" class="tl-btn tl-btn-ghost" data-nav="invoices">' + esc(t.billing) + "</button>") +
        "</div>";
    }

    function companyForm(company) {
      company = company || {};
      return '<form class="tl-form" id="acc-company"><label>' + esc(t.company) + '</label><input name="name" required value="' + esc(company.name || "") + '">' +
        "<label>" + esc(t.description) + '</label><textarea name="description" rows="4">' + esc(company.description || "") + "</textarea>" +
        '<div class="tl-row-2"><div><label>' + esc(t.sector) + '</label><input name="sector" value="' + esc(company.sector || "") + '"></div>' +
        "<div><label>" + esc(t.website) + '</label><input name="website" value="' + esc(company.website || "") + '"></div></div>' +
        "<label>" + esc(t.address) + '</label><input name="address" value="' + esc(company.address || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.city) + '</label><input name="city" value="' + esc(company.city || "") + '"></div>' +
        "<div><label>" + esc(t.country) + '</label><input name="country" value="' + esc(company.country || "Canada") + '"></div></div>' +
        '<div class="tl-row-2"><div><label>' + esc(t.email) + '</label><input name="email" value="' + esc(company.email || "") + '"></div>' +
        "<div><label>" + esc(t.phone) + '</label><input name="phone" value="' + esc(company.phone || "") + '"></div></div>' +
        "<label>" + esc(t.legal) + '</label><input name="legal_name" value="' + esc(company.legal_name || "") + '">' +
        '<div class="tl-row-2"><div><label>' + esc(t.size) + '</label><input name="size_label" value="' + esc(company.size_label || "") + '"></div>' +
        "<div><label>LinkedIn</label><input name=\"linkedin_url\" value=\"" + esc(company.linkedin_url || "") + '"></div></div>' +
        "<label>Facebook</label><input name=\"facebook_url\" value=\"" + esc(company.facebook_url || "") + '">' +
        '<button class="tl-btn" type="submit">' + esc(t.save) + '</button><div class="tl-success"></div></form>';
    }

    function renderEmployerJobs(jobs) {
      var list = (!jobs || !jobs.length) ? empty(t.emptyHiring) : '<div class="tl-list-cards">' + jobs.map(function (j) {
        var label = j.status_label || statusLabel(j.status);
        return '<article class="tl-list-card"><span class="tl-chip orange">' + esc(label) + "</span><h3>" + esc(j.title) +
          "</h3><p class=\"tl-meta\">" + esc(j.location || "") + (j.seats ? " · " + esc(j.seats) : "") + "</p>" +
          (j.status_message ? "<p>" + esc(j.status_message) + "</p>" : "") +
          '<button type="button" class="tl-btn tl-btn-ghost" data-nav="job-edit" data-id="' + esc(j.id) + '">' +
          esc(t.edit) + "</button></article>";
      }).join("") + "</div>";
      return "<p>" + esc(t.hiringLead) + '</p><p><button type="button" class="tl-btn" data-nav="job-new">' + esc(t.createJob) + "</button></p>" + list;
    }

    function jobForm(job) {
      job = job || {};
      var o = jobOptions || {};
      return '<p>' + esc(t.validate) + '</p><form class="tl-form" id="acc-hiring-form">' +
        "<label>" + esc(t.title) + "</label>" + choiceSelect("title", o.occupations, job.title, t.pick, true) +
        '<div class="tl-row-2"><div><label>' + esc(t.location) + '</label>' + choiceSelect("location", o.locations, job.location, t.pick) + '</div>' +
        "<div><label>" + esc(t.sector) + '</label>' + choiceSelect("sector", o.sectors, job.sector, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.contract) + '</label><p class="tl-field-hint">' + esc(t.contractHint) + '</p>' + choiceSelect("contract_type", o.contract_types, job.contract_type, t.pick) + '</div>' +
        "<div><label>" + esc(t.experience) + '</label>' + choiceSelect("experience_level", o.experience_levels, job.experience_level, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.shiftLabel) + '</label><p class="tl-field-hint">' + esc(t.shiftHint) + '</p>' + choiceSelect("shift", o.shifts, job.shift, t.pick) + '</div>' +
        "<div><label>" + esc(t.hours) + '</label><p class="tl-field-hint">' + esc(t.hoursHint) + '</p>' + choiceSelect("schedule", o.schedules, job.schedule, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.workMode) + '</label>' + choiceSelect("work_mode", o.work_modes, job.work_mode, t.pick) + '</div>' +
        "<div><label>" + esc(t.languages) + '</label>' + choiceSelect("languages", o.languages, job.languages, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.overtime) + '</label>' + choiceSelect("overtime", o.overtime, job.overtime, t.pick) + '</div>' +
        "<div><label>" + esc(t.license) + '</label>' + choiceSelect("driver_license", o.driver_licenses, job.driver_license, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.union) + '</label>' + choiceSelect("unionized", o.union_status, job.unionized, t.pick) + '</div>' +
        "<div><label>" + esc(t.travel) + '</label>' + choiceSelect("travel", o.travel, job.travel, t.pick) + "</div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.workAuth) + '</label>' + choiceSelect("work_authorization", o.work_requirements, job.work_authorization || "ouvert", t.pick) + '</div>' +
        '<div><label class="tl-check"><input type="checkbox" name="can_sponsor" value="true"' + (job.can_sponsor ? " checked" : "") + "> " + esc(t.canSponsor) + "</label></div></div>" +
        '<div class="tl-row-2"><div><label>' + esc(t.openings) + '</label><input name="seats" type="number" min="1" value="' + esc(job.seats || job.openings || 1) + '"></div>' +
        "<div><label>" + esc(t.startDate) + '</label><input name="start_date" type="date" value="' + esc(job.start_date || "") + '"></div></div>' +
        "<label>" + esc(t.skills) + '</label><input name="skills" value="' + esc(job.skills || "") + '">' +
        "<label>" + esc(t.extra) + '</label><textarea name="notes" rows="5">' + esc(job.notes || job.description || "") + "</textarea>" +
        '<button class="tl-btn" type="submit">' + esc(job.id ? t.save : t.createJob) + '</button><div class="tl-success"></div></form>';
    }

    function renderHiringDetail(row) {
      if (!row) return empty(t.emptyHiring);
      var canFeedback = row.status === "CLIENT_VALIDATION" || row.status === "SHORTLIST" || row.status === "CLIENT_REVIEW";
      var feedback = canFeedback
        ? '<form class="tl-form" id="acc-hiring-feedback"><label>' + esc(t.feedback) + '</label><textarea name="comment" rows="4"></textarea>' +
          '<p><button class="tl-btn" type="submit" name="action" value="validate">' + esc(t.validateBrief) +
          '</button> <button class="tl-btn tl-btn-ghost" type="submit" name="action" value="changes">' + esc(t.requestChanges) +
          "</button></p><div class=\"tl-success\"></div></form>"
        : "";
      return mediateNote() + '<span class="tl-chip orange">' + esc(row.status_label || statusLabel(row.status)) + "</span>" +
        "<h3>" + esc(row.title) + "</h3><p>" + esc(row.status_message || "") + "</p>" +
        "<p class=\"tl-meta\">" + esc(row.location || "") + (row.sector ? " · " + esc(row.sector) : "") + "</p>" +
        (row.notes ? "<p>" + esc(row.notes) + "</p>" : "") +
        '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="inbox">' + esc(t.candidates) + "</button> " +
        '<button type="button" class="tl-btn tl-btn-ghost" data-nav="messages">' + esc(t.writeTalendus) + "</button></p>" +
        feedback;
    }

    function renderInbox(apps) {
      if (!apps || !apps.length) return mediateNote() + empty(t.emptyInbox);
      return mediateNote() + '<div class="tl-table-wrap"><table class="tl-portal-table"><thead><tr><th>' + esc(t.first) + "</th><th>" + esc(t.title) +
        "</th><th>" + esc(t.status || t.decision) + "</th><th>" + esc(t.experience) + "</th><th></th></tr></thead><tbody>" + apps.map(function (a) {
        var c = a.candidate || {};
        var job = a.job || {};
        return "<tr><td data-label=\"" + esc(t.first) + "\">" + esc((c.first_name || "") + " " + (c.last_name || "")) +
          "</td><td data-label=\"" + esc(t.title) + "\">" + esc(c.title || job.title || "") + "</td><td data-label=\"" + esc(t.status || t.decision) + "\">" +
          '<span class="tl-chip orange">' + esc(statusLabel(a.status)) + "</span></td><td data-label=\"" + esc(t.experience) + "\">" +
          esc(c.years_experience || "—") +
          '</td><td><button type="button" class="tl-btn tl-btn-ghost" data-nav="candidate" data-id="' + esc(c.id || "") + '">' +
          esc(t.candidates) + "</button></td></tr>";
      }).join("") + "</tbody></table></div>";
    }

    function money(amount) {
      var n = Number(amount) || 0;
      try {
        return new Intl.NumberFormat(isEn ? "en-CA" : "fr-CA", { style: "currency", currency: "CAD", maximumFractionDigits: 0 }).format(n);
      } catch (e) {
        return n + " $";
      }
    }

    function renderInvoices(rows) {
      if (!rows || !rows.length) return empty(t.emptyInvoices);
      var payable = { SENT: 1, PENDING: 1, OVERDUE: 1 };
      return '<p class="tl-mediate">' + esc(t.transferHint) + "</p>" +
        '<div class="tl-table-wrap"><table class="tl-portal-table"><thead><tr><th>' + esc(t.invoices) + "</th><th>" + esc(t.amount || t.pay) +
        "</th><th></th><th></th></tr></thead><tbody>" + rows.map(function (inv) {
        var pay = "";
        if (payable[inv.status] && siteServices.payments && siteServices.payments.card) {
          pay += '<button type="button" class="tl-btn" data-pay="' + esc(inv.id) + '">' + esc(t.pay) + "</button>";
        }
        if (payable[inv.status] && siteServices.payments && siteServices.payments.paypal) {
          pay += ' <button type="button" class="tl-btn tl-btn-ghost" data-pay-paypal="' + esc(inv.id) + '">' + esc(t.payPal) + "</button>";
        }
        var pdf = inv.pdf_path ? '<button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(inv.pdf_path) + '" data-dl-name="' + esc((inv.number || "facture") + ".pdf") + '">' + esc(t.downloadPdf) + "</button>" : "";
        return "<tr><td data-label=\"" + esc(t.invoices) + "\">" + esc(inv.number || inv.id) +
          "</td><td data-label=\"" + esc(t.amount || t.pay) + "\">" + esc(money(inv.amount_total || inv.amount)) +
          "</td><td><span class=\"tl-chip\">" + esc(statusLabel(inv.status)) + "</span></td><td>" + pdf + " " + pay + "</td></tr>";
      }).join("") + "</tbody></table></div><div class=\"tl-success\" id=\"acc-inv-msg\"></div>";
    }

    function clientMandateLabel(c) {
      if (c.client_signed || c.client_status === "signed" || c.signed) return t.clientSigned;
      if (c.opened_at || c.client_status === "opened") return t.clientOpened;
      if (c.sent_at || c.client_status === "received") return t.clientReceived;
      return t.unsigned;
    }

    function renderContracts(rows) {
      if (!rows || !rows.length) return empty(t.emptyContracts);
      (rows || []).forEach(function (c) {
        if (c && c.id && c.sent_at && !c.opened_at && !c.client_signed && !c.signed) {
          api.openContract(c.id).catch(function () {});
        }
      });
      return rows.map(function (c) {
        var pdf = c.pdf_path
          ? '<button type="button" class="tl-btn tl-btn-ghost" data-open-pdf="' + esc(c.pdf_path) + '">' + esc(t.readPdf) + "</button>" +
            ' <button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(c.pdf_path) + '" data-dl-name="' + esc(c.document_name || "mandat.pdf") + '">' + esc(t.downloadPdf) + "</button>"
          : "";
        var canSign = !!c.can_sign;
        var sign = (c.signed || c.client_signed)
          ? '<span class="tl-chip">' + esc(t.signed) + "</span>"
          : (canSign
            ? '<p class="tl-meta">' + esc(t.readThenSign) + '</p><form class="tl-form" data-sign-contract="' + esc(c.id) + '"><label class="tl-check"><input type="checkbox" name="accepted" required> ' + esc(t.acceptTerms) +
              "</label><input name=\"signer_name\" required placeholder=\"" + esc(t.first) + "\"><button class=\"tl-btn\" type=\"submit\">" + esc(t.sign) + "</button></form>"
            : "");
        var agency = c.talendus_signed ? '<span class="tl-chip">' + esc(t.talendusSigned) + "</span> " : "";
        return '<article class="tl-card" style="margin-bottom:16px"><div class="body"><h3>' + esc(c.type || t.contracts) +
          " · " + esc(c.company_name || "") + "</h3><p class=\"tl-meta\">" + esc(c.start_date || "") + " → " + esc(c.end_date || "") +
          (c.commission_percent ? " · " + esc(String(c.commission_percent)) + " %" : "") + "</p>" +
          '<div class="tl-mandate-status">' + agency + '<span class="tl-chip">' + esc(clientMandateLabel(c)) + "</span></div>" +
          '<article class="tl-mandate-read">' + esc(c.terms || "") +
          "</article><p>" + pdf + "</p>" + sign + "</div></article>";
      }).join("") + '<div class="tl-success" id="acc-contract-msg"></div>';
    }

    function renderPipeline(apps) {
      var stages = [
        ["nouveaux", t.sent], ["preselection", t.review], ["presentation", t.preselect],
        ["entretien-talendus", t.interview], ["entretien-client", isEn ? "Client interview" : "Entretien client"],
        ["offre", isEn ? "Offer" : "Offre"], ["placement", t.hired]
      ];
      var grouped = {};
      stages.forEach(function (st) { grouped[st[0]] = []; });
      (apps || []).forEach(function (a) {
        var key = a.pipeline_stage || "nouveaux";
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(a);
      });
      return mediateNote() + '<div class="tl-pipeline">' + stages.map(function (st) {
        var cards = (grouped[st[0]] || []).map(function (a) {
          var c = a.candidate || {};
          var job = a.job || {};
          return '<article class="tl-pipe-card"><b>' + esc((c.first_name || "") + " " + (c.last_name || "")) +
            "</b><p class=\"tl-meta\">" + esc(job.title || "") + "</p>" +
            '<span class="tl-chip orange">' + esc(statusLabel(a.status)) + "</span>" +
            (c.id ? '<p><button type="button" class="tl-btn tl-btn-ghost" data-nav="candidate" data-id="' + esc(c.id) + '">' + esc(t.candidates) + "</button></p>" : "") +
            "</article>";
        }).join("");
        return '<section class="tl-pipe-col"><h4>' + esc(st[1]) + " <span>" + (grouped[st[0]] || []).length + "</span></h4>" +
          (cards || '<p class="tl-meta">-</p>') + "</section>";
      }).join("") + "</div>";
    }

    function renderMembers(members, canManage) {
      var rows = (members || []).map(function (m) {
        return "<tr><td data-label=\"" + esc(t.first) + "\">" + esc((m.first_name || "") + " " + (m.last_name || "")) +
          "</td><td>" + esc(m.email || "") + "</td><td>" + esc(statusLabel(m.member_role)) + "</td></tr>";
      }).join("");
      var table = '<div class="tl-table-wrap"><table class="tl-portal-table"><thead><tr><th>' + esc(t.first) + "</th><th>" +
        esc(t.email) + "</th><th>" + esc(t.permissions) + "</th></tr></thead><tbody>" + (rows || "") + "</tbody></table></div>";
      var invite = canManage
        ? '<form class="tl-form" id="acc-invite"><div class="tl-row-2"><input name="first_name" required placeholder="' +
          esc(t.first) + '"><input name="last_name" required placeholder="' + esc(t.last) + '"></div>' +
          '<input name="email" type="email" required placeholder="' + esc(t.email) + '"><select name="member_role">' +
          '<option value="HR">RH</option><option value="RECRUITER">' + (isEn ? "Recruiter" : "Recruteur interne") +
          '</option><option value="ADMIN">' + (isEn ? "Administrator" : "Administrateur") +
          '</option><option value="BILLING">' + (isEn ? "Billing" : "Facturation") + "</option></select>" +
          '<button class="tl-btn" type="submit">' + esc(t.invite) + '</button><div class="tl-success"></div></form>'
        : '<p class="tl-meta">' + esc(t.teamReadOnly) + "</p>";
      return settingsCard(t.settingsTeam, canManage ? t.teamHint : t.teamReadOnly, table + invite);
    }

    var state = { user: null, unreadN: 0, unreadM: 0, jobFilters: {}, myApps: [], appsReady: false };
    function ensureMyApps() {
      if (state.appsReady) return Promise.resolve(state.myApps);
      return unwrap(api.myApplications()).then(function (rows) {
        state.myApps = rows || [];
        state.appsReady = true;
        return state.myApps;
      }).catch(function () {
        state.myApps = state.myApps || [];
        state.appsReady = true;
        return state.myApps;
      });
    }
    function ensureCompany() {
      if (!isEmployerSpace()) return Promise.resolve(state.company);
      if (state.company && typeof state.company.can_read_invoices === "boolean") return Promise.resolve(state.company);
      return unwrap(api.request("/companies/me")).then(function (c) {
        state.company = c || {};
        return state.company;
      }).catch(function () {
        state.company = state.company || {};
        return state.company;
      });
    }

    function bindCommon() {
      var mark = document.getElementById("acc-readall");
      if (mark) mark.onclick = function () { api.request("/notifications/read-all", { method: "POST" }).then(function () { go("notifs"); }); };
      root.querySelectorAll("[data-read]").forEach(function (b) {
        b.onclick = function (ev) {
          ev.stopPropagation();
          api.request("/notifications/" + b.getAttribute("data-read") + "/read", { method: "POST" }).then(function () { go("notifs"); });
        };
      });
      root.querySelectorAll("[data-job-pub]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-pub") + "/publish", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-pause]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-pause") + "/pause", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-arch]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-arch") + "/archive", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-dup]").forEach(function (b) { b.onclick = function () { api.request("/jobs/" + b.getAttribute("data-job-dup") + "/duplicate", { method: "POST" }).then(function () { go("jobs"); }); }; });
      root.querySelectorAll("[data-job-del]").forEach(function (b) {
        b.onclick = function () {
          if (!window.confirm(t.confirmDanger)) return;
          api.request("/jobs/" + b.getAttribute("data-job-del"), { method: "DELETE" }).then(function () { go("jobs"); });
        };
      });
      var alertForm = document.getElementById("acc-alert");
      if (alertForm) alertForm.addEventListener("submit", function (e) {
        e.preventDefault();
        api.request("/alerts", { method: "POST", body: Object.fromEntries(new FormData(alertForm).entries()) })
          .then(function () { go("alerts"); })
          .catch(function (err) { flash(alertForm.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      root.querySelectorAll("[data-del-alert]").forEach(function (b) {
        b.onclick = function () { api.request("/alerts/" + b.getAttribute("data-del-alert"), { method: "DELETE" }).then(function () { go("alerts"); }); };
      });
      root.querySelectorAll("[data-app-status]").forEach(function (sel) {
        sel.onchange = function () {
          var dest = currentRoute().name === "pipeline" ? "pipeline" : "inbox";
          api.request("/applications/" + sel.getAttribute("data-app-status") + "/status", { method: "POST", body: { status: sel.value } }).then(function () { go(dest); });
        };
      });
      root.querySelectorAll("[data-open-notif]").forEach(function (el) {
        el.onclick = function (ev) {
          if (ev.target && ev.target.closest && ev.target.closest("[data-read]")) return;
          var href = el.getAttribute("data-href") || "";
          var id = el.getAttribute("data-open-notif");
          var open = function () {
            if (!href) return;
            var hash = href.split("#")[1] || "";
            var parts = hash.replace(/^\//, "").split("/");
            if (parts[0] && (href.indexOf("espace") !== -1 || href.indexOf("account") !== -1 || href.indexOf("/candidate") !== -1 || href.indexOf("/employer") !== -1)) {
              var mapped = normalizeRoute(parts[0], parts[1] || "");
              go(mapped.name, mapped.id);
              return;
            }
            window.location.href = href;
          };
          if (id) api.request("/notifications/" + id + "/read", { method: "POST" }).then(open).catch(open);
          else open();
        };
      });
      root.querySelectorAll("[data-pay]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/invoices/" + btn.getAttribute("data-pay") + "/checkout", { method: "POST" }).then(function (json) {
            var url = json && json.data && json.data.checkout_url;
            if (url) window.location.href = url;
            else flash(document.getElementById("acc-inv-msg"), t.transferHint, true);
          }).catch(function (err) {
            flash(document.getElementById("acc-inv-msg"), (err && err.message) || t.transferHint, false);
          });
        };
      });
      root.querySelectorAll("[data-pay-paypal]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/invoices/" + btn.getAttribute("data-pay-paypal") + "/paypal", { method: "POST" }).then(function (json) {
            var url = json && json.data && json.data.checkout_url;
            if (url) window.location.href = url;
            else flash(document.getElementById("acc-inv-msg"), t.transferHint, true);
          }).catch(function (err) {
            flash(document.getElementById("acc-inv-msg"), (err && err.message) || t.transferHint, false);
          });
        };
      });
      root.querySelectorAll("[data-sign-contract]").forEach(function (form) {
        form.onsubmit = function (e) {
          e.preventDefault();
          var id = form.getAttribute("data-sign-contract");
          var accepted = form.querySelector("[name=accepted]");
          api.request("/contracts/" + id + "/sign", {
            method: "POST",
            body: {
              accepted: !!(accepted && accepted.checked),
              signer_name: (form.querySelector("[name=signer_name]") || {}).value || ""
            }
          }).then(function () { go("contracts"); }).catch(function (err) {
            flash(document.getElementById("acc-contract-msg"), (err && err.message) || t.err, false);
          });
        };
      });
      root.querySelectorAll("[data-open-pdf]").forEach(function (b) {
        b.onclick = function () {
          var path = b.getAttribute("data-open-pdf");
          if (api.openPdf) api.openPdf(path).catch(function (err) {
            flash(document.getElementById("acc-contract-msg"), (err && err.message) || t.err, false);
          });
        };
      });
      root.querySelectorAll("[data-int-status]").forEach(function (btn) {
        btn.onclick = function () {
          api.request("/interviews/" + btn.getAttribute("data-int-id") + "/status", { method: "POST", body: { status: btn.getAttribute("data-int-status") } })
            .then(function () { go("interviews"); })
            .catch(function (err) { window.alert((err && err.message) || t.err); });
        };
      });
      root.querySelectorAll("[data-join-call]").forEach(function (btn) {
        btn.onclick = function () {
          if (!window.TalendusCall) return;
          window.TalendusCall.start({
            interviewId: btn.getAttribute("data-join-call"),
            video: btn.getAttribute("data-video") !== "0",
            onHangup: function () {}
          });
        };
      });
      var apply = document.getElementById("acc-apply");
      if (apply && state.job) apply.onclick = function () {
        var cover = ((document.getElementById("acc-cover") || {}).value || "").trim();
        var body = { job_id: state.job.id, job_slug: state.job.slug };
        if (cover) body.cover_note = cover;
        api.request("/applications", { method: "POST", body: body })
          .then(function () { state.appsReady = false; go("apps"); })
          .catch(function (err) { flash(document.getElementById("acc-job-msg"), (err && err.message) || t.err, false); });
      };
      var saveBtn = document.getElementById("acc-save-job");
      if (saveBtn && state.job) saveBtn.onclick = function () {
        var method = state.job.saved ? "DELETE" : "POST";
        api.request("/jobs/" + state.job.id + "/save", { method: method })
          .then(function () { go("job", state.job.slug); })
          .catch(function (err) { flash(document.getElementById("acc-job-msg"), (err && err.message) || t.err, false); });
      };
      var withdraw = document.getElementById("acc-withdraw");
      if (withdraw && state.application) withdraw.onclick = function () {
        api.request("/applications/" + state.application.id + "/withdraw", { method: "POST" })
          .then(function () { state.appsReady = false; go("apps"); })
          .catch(function (err) { window.alert((err && err.message) || t.err); });
      };
      var company = document.getElementById("acc-company");
      if (company && state.company) company.addEventListener("submit", function (e) {
        e.preventDefault();
        api.request("/companies/" + state.company.id, { method: "PATCH", body: Object.fromEntries(new FormData(company).entries()) })
          .then(function () { flash(company.querySelector(".tl-success"), t.saved, true); })
          .catch(function (err) { flash(company.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var hiringForm = document.getElementById("acc-hiring-form");
      if (hiringForm) hiringForm.addEventListener("submit", function (e) {
        e.preventDefault();
        var body = Object.fromEntries(new FormData(hiringForm).entries());
        if (body.seats) body.seats = Number(body.seats);
        body.can_sponsor = !!(hiringForm.can_sponsor && hiringForm.can_sponsor.checked);
        var req = state.editHiring
          ? api.request("/hiring-requests/" + state.editHiring.id, { method: "PATCH", body: body })
          : api.request("/hiring-requests", { method: "POST", body: body });
        req.then(function (json) {
          flash(hiringForm.querySelector(".tl-success"), (json && json.message) || t.needSent, true);
          window.setTimeout(function () { go("jobs"); }, 1400);
        }).catch(function (err) { flash(hiringForm.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var hiringFeedback = document.getElementById("acc-hiring-feedback");
      if (hiringFeedback) hiringFeedback.addEventListener("submit", function (e) {
        e.preventDefault();
        var actionBtn = e.submitter && e.submitter.getAttribute("value");
        var body = Object.fromEntries(new FormData(hiringFeedback).entries());
        api.request("/hiring-requests/" + (state.editHiring && state.editHiring.id) + "/feedback", {
          method: "POST",
          body: { action: actionBtn || "validate", comment: body.comment || "" }
        }).then(function () { go("jobs"); })
          .catch(function (err) { flash(hiringFeedback.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      var invite = document.getElementById("acc-invite");
      if (invite) invite.addEventListener("submit", function (e) {
        e.preventDefault();
        api.request("/companies/me/members", { method: "POST", body: Object.fromEntries(new FormData(invite).entries()) })
          .then(function () { go("settings", "team"); }).catch(function (err) { flash(invite.querySelector(".tl-success"), (err && err.message) || t.err, false); });
      });
      bindMessages();
      bindDocs();
      bindSettings();
      bindProfile(state.user);
      bindJobsSearch();
      root.querySelectorAll("[data-dl]").forEach(function (b) {
        b.onclick = function () { authDownload(b.getAttribute("data-dl"), b.getAttribute("data-dl-name") || "document"); };
      });
    }

    function renderInterviews(items) {
      var list = (!items || !items.length) ? empty(t.emptyInts) : items.map(function (i) {
        var actions = "";
        if (i.in_app_call) {
          actions += '<p><button type="button" class="tl-btn tl-btn-ghost" data-join-call="' + esc(i.id) + '" data-video="0">' + esc(t.callAudio) + "</button> ";
          if (i.call_video !== false) {
            actions += '<button type="button" class="tl-btn" data-join-call="' + esc(i.id) + '" data-video="1">' + esc(t.callVideo) + "</button>";
          }
          actions += "</p>";
        }
        if (i.status === "SCHEDULED" && !isEmployerSpace()) {
          actions += '<p><button type="button" class="tl-btn tl-btn-ghost" data-int-status="CONFIRMED" data-int-id="' + esc(i.id) + '">' + esc(t.confirm) +
            '</button> <button type="button" class="tl-btn tl-btn-ghost" data-int-status="CANCELLED" data-int-id="' + esc(i.id) + '">' + esc(t.cancel) + "</button></p>";
        }
        return '<div class="tl-account-notif"><b>' + esc(i.type_label || i.type) + " · " + esc(statusLabel(i.status)) + "</b><p>" +
          esc(fmtDate(i.scheduled_at)) + " · " + esc(i.location || "") + (i.job_title ? " · " + esc(i.job_title) : "") +
          (i.candidate_name ? " · " + esc(i.candidate_name) : "") + "</p>" + actions + "</div>";
      }).join("");
      var lead = '<p class="tl-lead">' + esc(isEmployerSpace() ? t.scheduleLeadEmployer : t.scheduleLeadCandidate) + "</p>";
      return (isEmployerSpace() ? mediateNote() : "") + lead + list;
    }

    function countsThen(cb) {
      Promise.all([
        api.notifications().then(function (j) { return j; }).catch(function () { return { data: [], meta: {} }; }),
        api.request("/messages").then(function (j) { return j.data || []; }).catch(function () { return []; })
      ]).then(function (rows) {
        state.unreadN = (rows[0].meta && rows[0].meta.unread) || (rows[0].data || []).filter(function (n) { return !n.is_read; }).length;
        state.unreadM = (rows[1] || []).reduce(function (s, th) { return s + (th.unread || 0); }, 0);
        state.notifs = rows[0].data || [];
        state.threads = rows[1];
        cb();
      });
    }

    function renderAuthed() {
      document.body.classList.remove("tl-auth-guest");
      var user = state.user;
      var route = currentRoute();
      countsThen(function () {
        var needApps = !isEmployerSpace() && ["dashboard", "jobs", "job", "saved"].indexOf(route.name) >= 0;
        Promise.all([ensureCompany(), needApps ? ensureMyApps() : Promise.resolve()]).then(function () {
        shell(user, skeleton(), state.unreadN, state.unreadM);
        loadJobOptions().then(function () {
        var p;
        if (isEmployerSpace()) {
          if (route.name === "dashboard") p = Promise.all([unwrap(api.request("/companies/me/dashboard")), unwrap(api.request("/companies/me"))]).then(function (r) {
            state.company = r[1];
            return employerDashboard(user, r[0], r[1]);
          });
          else if (route.name === "company") p = unwrap(api.request("/companies/me")).then(function (c) { state.company = c; return companyForm(c); });
          else if (route.name === "jobs") p = unwrap(api.request("/hiring-requests")).then(renderEmployerJobs);
          else if (route.name === "job-new") p = Promise.resolve(jobForm({}));
          else if (route.name === "job-edit") p = unwrap(api.request("/hiring-requests/" + route.id)).then(function (j) {
            state.editHiring = j;
            return renderHiringDetail(j) + "<h3>" + esc(t.edit) + "</h3>" + jobForm(j);
          });
          else if (route.name === "inbox" || route.name === "candidates") p = unwrap(api.request("/applications")).then(renderInbox);
          else if (route.name === "pipeline") p = unwrap(api.request("/applications")).then(renderPipeline);
          else if (route.name === "invoices") {
            if (state.company && state.company.can_read_invoices === false) {
              p = Promise.resolve(empty(t.noBilling));
            } else {
              p = Promise.all([unwrap(api.request("/invoices")), servicesReady]).then(function (r) {
                return renderInvoices(r[0]);
              }).catch(function (err) {
                if (err && (err.status === 403 || err.code === "FORBIDDEN")) return empty(t.noBilling);
                throw err;
              });
            }
          }
          else if (route.name === "contracts") p = unwrap(api.request("/contracts")).then(renderContracts);
          else if (route.name === "candidate") p = unwrap(api.request("/candidates/" + route.id)).then(function (c) {
            return mediateNote() + "<h3>" + esc((c.first_name || "") + " " + (c.last_name || "")) + "</h3><p>" + esc(c.title || "") + " · " + esc(c.city || "") +
              "</p><p>" + esc(c.skills || "") + "</p>" + ((c.resumes || []).map(function (r) {
                return '<p><button type="button" class="tl-btn tl-btn-ghost" data-dl="' + esc(r.download_path) + '" data-dl-name="' + esc(r.original_name || "cv.pdf") + '">' + esc(t.download) + " CV</button></p>";
              }).join("") || "");
          });
          else if (route.name === "interviews") p = unwrap(api.request("/interviews")).then(function (rows) { return renderInterviews(rows); });
          else if (route.name === "messages") p = Promise.all([
            unwrap(api.request("/messages")), unwrap(api.request("/messages/directory"))
          ]).then(function (r) { return renderMessages(r[0], r[1], state.thread); });
          else if (route.name === "documents") p = unwrap(api.request("/documents?owner_type=company")).then(function (docs) { return renderDocs(docs, []); });
          else if (route.name === "notifs") p = Promise.resolve(renderNotifs(state.notifs));
          else if (route.name === "settings") p = Promise.all([
            unwrap(api.request("/users/me/preferences")),
            unwrap(api.request("/companies/me")).catch(function () { return {}; }),
            unwrap(api.request("/companies/me/members")).catch(function () { return []; })
          ]).then(function (r) {
            state.company = r[1];
            return renderSettings(r[0], { company: r[1], members: r[2] });
          });
          else p = Promise.resolve(empty(t.err));
        } else {
          if (route.name === "dashboard") p = Promise.all([unwrap(api.request("/candidates/me/dashboard")), unwrap(api.request("/candidates/me"))]).then(function (r) {
            return renderCandidateDashboard(user, r[0], r[1]);
          });
          else if (route.name === "profile") p = unwrap(api.request("/candidates/me")).then(function (pr) { return profileForm(user, pr); });
          else if (route.name === "jobs") p = (state.jobs ? Promise.resolve(state.jobs) : api.request("/jobs")).then(renderJobsSearch);
          else if (route.name === "job") p = unwrap(api.request("/jobs/" + route.id)).then(function (j) { state.job = j; return renderJobDetail(j); });
          else if (route.name === "apps") p = unwrap(api.myApplications()).then(function (rows) {
            state.myApps = rows || [];
            state.appsReady = true;
            return renderApps(rows);
          });
          else if (route.name === "saved") p = unwrap(api.request("/jobs/saved")).then(renderSavedJobs);
          else if (route.name === "alerts") p = unwrap(api.request("/alerts")).then(renderAlerts);
          else if (route.name === "application") p = unwrap(api.request("/applications/" + route.id)).then(function (a) { state.application = a; return renderAppDetail(a); });
          else if (route.name === "interviews") p = unwrap(api.request("/interviews")).then(function (rows) { return renderInterviews(rows); });
          else if (route.name === "messages") p = Promise.all([
            unwrap(api.request("/messages")), unwrap(api.request("/messages/directory"))
          ]).then(function (r) { return renderMessages(r[0], r[1], state.thread); });
          else if (route.name === "documents") p = Promise.all([
            unwrap(api.request("/documents")), unwrap(api.request("/candidates/me"))
          ]).then(function (r) { return renderDocs(r[0], (r[1] && r[1].resumes) || []); });
          else if (route.name === "notifs") p = Promise.resolve(renderNotifs(state.notifs));
          else if (route.name === "settings") p = unwrap(api.request("/users/me/preferences")).then(function (prefs) {
            return renderSettings(prefs, {});
          });
          else p = Promise.resolve(empty(t.err));
        }
        p.then(function (html) {
          shell(user, html, state.unreadN, state.unreadM);
          bindCommon();
        }).catch(function (err) {
          shell(user, errBox((err && err.message) || t.err), state.unreadN, state.unreadM);
          var retry = root.querySelector("[data-retry]");
          if (retry) retry.onclick = renderAuthed;
        });
        });
        });
      });
    }

    function boot() {
      if (isEmployerSpace() && /[?&]paid=/.test(location.search || "")) {
        if (!(location.hash || "").replace("#", "")) location.hash = "#/invoices";
      }
      var local = api.currentUser();
      if (!local) { renderGuest(); return; }
      renderChecking();
      api.me().then(function (j) {
        var user = j.data;
        state.user = user;
        if (staffRole(user.role)) { window.location.replace(accountHref(user.role)); return; }
        if (user.role === "EMPLOYER" && !isEmployerSpace()) { window.location.replace(accountHref("EMPLOYER")); return; }
        if (user.role === "CANDIDATE" && isEmployerSpace()) { window.location.replace(accountHref("CANDIDATE")); return; }
        renderAuthed();
      }).catch(function (err) {
        if (!api.currentUser() || (err && err.status === 401)) {
          renderGuest();
          return;
        }
        root.innerHTML = errBox((err && err.message) || t.err);
        var retry = root.querySelector("[data-retry]");
        if (retry) retry.onclick = boot;
      });
    }

    window.addEventListener("hashchange", function () { if (state.user) renderAuthed(); });
    window.addEventListener("popstate", function () { if (state.user) renderAuthed(); });
    window.addEventListener("talendus:auth", function () { boot(); });
    window.addEventListener("talendus:session-cleared", function () { renderGuest(); });
    boot();
  });
})();
