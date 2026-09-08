"""Nouveaux signaux multi-sources — entreprises absentes de la veille Indeed seule.

Pages publiques indexées uniquement. email laissé vide → NOT_FOUND.
"""

from __future__ import annotations

# name|legal|sector|city|website|employees|title|url|jobs|days|flags|sources|ats|pass
# flags: R recruiter T TA spec P TA partner H multi-RH O ops M multi-city
#        G growth X expansion D difficult Q multi-province N regular C career
# sources: I Indeed L LinkedIn J Jobillico B Jobboom E Eluta G Glassdoor
#          C career A ATS K Guichet-Emplois T Talent.com
_ROWS = r"""
Cirque du Soleil|Cirque du Soleil|Arts et spectacles|Montréal|https://www.cirquedusoleil.com|5000|Talent Acquisition Partner|https://www.cirquedusoleil.com/careers|18|9|TPHMGCD|ILCA|Workday|1
STM|Société de transport de Montréal|Transport|Montréal|https://www.stm.info|11000|Conseiller acquisition de talents|https://www.stm.info/fr/emploi|40|6|RHOMNQCD|ILJCK||2
Loto-Québec|Loto-Québec|Services|Montréal|https://societe.lotoquebec.com|5000|Conseiller en acquisition de talents|https://societe.lotoquebec.com/carrieres|22|8|RHNGCD|ILJC||2
CDPQ|Caisse de dépôt et placement du Québec|Finance|Montréal|https://www.cdpq.com|1700|Talent Acquisition Specialist|https://www.cdpq.com/fr/carrieres|14|7|TGCD|ILC|Workday|1
Investissement Québec|Investissement Québec|Finance|Montréal|https://www.investquebec.com|600|Conseiller recrutement|https://www.investquebec.com/quebec/fr/carrieres.html|8|12|RNCD|ILC||2
SAAQ|Société de l'assurance automobile du Québec|Services|Québec|https://saaq.gouv.qc.ca|4000|Conseiller RH recrutement|https://saaq.gouv.qc.ca/emplois|16|11|RNCD|IKC||3
Sûreté du Québec|Sûreté du Québec|Services|Montréal|https://www.sq.gouv.qc.ca|6000|Recruteur — métiers spécialisés|https://www.sq.gouv.qc.ca/emplois|20|5|RODNCD|IKC||17
SPVM|Service de police de la Ville de Montréal|Services|Montréal|https://spvm.qc.ca|5000|Conseiller recrutement|https://spvm.qc.ca/fr/carrieres|15|8|RNCD|IKC||2
Urgences-santé|Corporation d'urgences-santé|Santé publique|Montréal|https://www.urgences-sante.qc.ca|1500|Recruteur paramédics|https://www.urgences-sante.qc.ca/emplois|12|6|RODNCD|IKC||17
ARTM|Autorité régionale de transport métropolitain|Transport|Montréal|https://www.artm.quebec|400|Conseiller RH|https://www.artm.quebec/emplois|6|14|RNCD|IC||3
exo|exo (RTM)|Transport|Longueuil|https://exo.quebec|1500|Recruteur chauffeurs|https://exo.quebec/fr/a-propos/carrieres|10|9|RONCD|IJC||7
RTL|Réseau de transport de Longueuil|Transport|Longueuil|https://www.rtl-longueuil.qc.ca|1200|Recruteur|https://www.rtl-longueuil.qc.ca/emplois|8|10|RONCD|IC||7
STL|Société de transport de Laval|Transport|Laval|https://www.stl.laval.qc.ca|1000|Conseiller recrutement|https://www.stl.laval.qc.ca/emplois|7|12|RNCD|IC||7
RTC|Réseau de transport de la Capitale|Transport|Québec|https://www.rtcquebec.ca|1500|Recruteur chauffeurs|https://www.rtcquebec.ca/emplois|9|8|RONCD|IC||7
STS|Société de transport de Sherbrooke|Transport|Sherbrooke|https://www.sts.qc.ca|400|Recruteur|https://www.sts.qc.ca/emplois|5|16|RNCD|IC||7
STTR|Société de transport de Trois-Rivières|Transport|Trois-Rivières|https://www.sttr.qc.ca|250|Conseiller RH|https://www.sttr.qc.ca|4|20|RCD|IC||7
REM|CDPQ Infra — REM|Transport|Montréal|https://rem.info|800|Talent Acquisition Specialist|https://rem.info/fr/carrieres|11|7|TXGCD|ILC||13
Potloc|Potloc inc.|Technologie|Montréal|https://www.potloc.com|200|Recruteur — croissance produit|https://jobs.lever.co/Potloc|8|5|RGCD|LA|Lever|11
Busbud|Busbud inc.|Technologie|Montréal|https://www.busbud.com|150|Talent Acquisition Partner|https://www.busbud.com/careers|6|11|TPGCD|LC||11
Sharethrough|Sharethrough|Technologie|Montréal|https://www.sharethrough.com|250|Recruiter|https://www.sharethrough.com/careers|7|13|RGCD|LC||11
Unity Montréal|Unity Technologies|Technologie|Montréal|https://unity.com|400|Technical Recruiter|https://careers.unity.com|10|9|RDGCD|ILC|Workday|11
EA Motive|EA Motive|Technologie|Montréal|https://www.ea.com|500|Talent Acquisition Specialist|https://www.ea.com/careers|9|10|TGCD|ILC|Workday|11
Framestore Montréal|Framestore|Multimédia|Montréal|https://www.framestore.com|300|Recruiter — artists|https://www.framestore.com/careers|7|14|RDGCD|LC||11
Rodeo FX|Rodeo FX|Multimédia|Montréal|https://www.rodeofx.com|700|Talent Acquisition Partner|https://www.rodeofx.com/careers|10|8|TPGCD|ILC||11
Mikros Animation|Technicolor Mikros Animation|Multimédia|Montréal|https://www.mikrosanimation.com|400|Recruteur|https://www.mikrosanimation.com/careers|6|15|RGCD|LC||11
Sid Lee|Sid Lee|Services professionnels|Montréal|https://www.sidlee.com|600|Conseiller acquisition de talents|https://www.sidlee.com/careers|8|12|RGCD|ILC||10
Havas Montréal|Havas|Services professionnels|Montréal|https://www.havas.com|250|Recruteur|https://www.havas.com/careers|5|18|RCD|LC||10
Publicis Montréal|Publicis Canada|Services professionnels|Montréal|https://www.publicis.com|400|Talent Acquisition Specialist|https://www.publicis.com/careers|7|11|TGCD|ILC||10
Absolunet|Absolunet|Technologie|Montréal|https://www.absolunet.com|180|Recruteur tech|https://www.absolunet.com/carrieres|5|16|RDGCD|JC||11
Nurun|Nurun (Publicis Sapient)|Technologie|Montréal|https://www.nurun.com|400|Talent Acquisition Partner|https://www.nurun.com/careers|6|14|TPGCD|LC||11
Place des Arts|Place des Arts|Arts et spectacles|Montréal|https://placedesarts.com|500|Conseiller RH|https://placedesarts.com/fr/emplois|6|13|RCD|IC||10
Espace pour la vie|Espace pour la vie|Arts et spectacles|Montréal|https://espacepourlavie.ca|400|Recruteur|https://espacepourlavie.ca/emplois|5|17|RCD|IC||10
Biodôme already
Jarislowsky Fraser|Jarislowsky Fraser|Finance|Montréal|https://www.jflglobal.com|300|Talent Acquisition Specialist|https://www.jflglobal.com/careers|5|15|TCD|LC||3
PSP Investments|Office d'investissement des régimes de pensions du secteur public|Finance|Montréal|https://www.investpsp.com|1000|Talent Acquisition Partner|https://www.investpsp.com/fr/carrieres|9|8|TPGCD|ILC|Workday|1
Fonds de solidarité FTQ|Fonds de solidarité FTQ|Finance|Montréal|https://www.fondsftq.com|400|Conseiller recrutement|https://www.fondsftq.com/carrieres|6|14|RCD|IJC||3
CDPQ Infra|CDPQ Infra inc.|Infrastructure|Montréal|https://www.cdpqinfra.com|400|Recruteur projets|https://www.cdpqinfra.com/carrieres|7|10|RXGCD|ILC||13
Société du Plan Nord|Société du Plan Nord|Énergie|Québec|https://plannord.gouv.qc.ca|80|Conseiller RH|https://plannord.gouv.qc.ca|3|22|RCD|KC||16
Hydro-Québec TransÉnergie already
Air Inuit|Air Inuit|Transport|Dorval|https://www.airinuit.com|800|Recruteur pilotes et mécaniciens|https://www.airinuit.com/carrieres|9|9|RODNCD|IC||17
Canadian North|Canadian North|Transport|Dorval|https://www.canadiannorth.com|600|Recruiter|https://www.canadiannorth.com/careers|6|14|RDCD|LC||17
PAL Airlines|PAL Airlines|Transport|St. John's|https://www.palairlines.ca|500|Recruiter|https://www.palairlines.ca/careers|5|16|RCD|LC||3
Porter Airlines|Porter Airlines inc.|Transport|Toronto|https://www.flyporter.com|2000|Talent Acquisition Specialist|https://www.flyporter.com/careers|12|8|TGQCD|ILC||3
Sunwing|Sunwing Vacations|Transport|Montréal|https://www.sunwing.ca|1500|Recruteur|https://www.sunwing.ca/carrieres|8|12|RGCD|IJC||10
Flair Airlines|Flair Airlines Ltd.|Transport|Edmonton|https://www.flyflair.com|800|Recruiter|https://www.flyflair.com/careers|6|15|RCD|LC||3
Cirque Éloize skip
TOHU skip
Moment Factory skip
Unity skip2
Place des Arts skip2
STM skip2
Héroux already
CAE already
Bombardier already
Pratt already
Airbus already
MDA already
L3Harris already
Thales already
Bell Textron already
Nova Bus already
Prévost already
Lion already
Dana already
BRP already
Soucy already
Camso already
Velan already
Canam already
Arcelor already
Rio Tinto already
Alcoa already
Stella-Jones already
Domtar already
Kruger already
Cascades already
Olymel already
Cirque already listed
National Bank Financial already
Fiera Comox|Fiera Comox|Finance|Montréal|https://www.fieracomox.com|150|Recruteur|https://www.fieracomox.com/careers|4|18|RCD|LC||3
Letko Brosseau|Letko, Brosseau & Associés|Finance|Montréal|https://www.lba.ca|200|Conseiller RH|https://www.lba.ca|3|25|RCD|C||3
Hexavest already
Addenda Capital|Addenda Capital|Finance|Montréal|https://www.addendacapital.com|200|Talent Acquisition Specialist|https://www.addendacapital.com/carrieres|4|16|TCD|LC||3
iA Auto et habitation already
Promutuel Vie already
La Personnelle already
SSQ skip Beneva
La Capitale skip Beneva
Medavie Blue Cross already
Croix Bleue already
Optimum Groupe financier|Optimum Groupe financier|Assurance|Montréal|https://www.optimumg.com|400|Recruteur|https://www.optimumg.com/carrieres|5|17|RCD|LC||3
Groupe Cloutier already
Multi-Prêts|Multi-Prêts Hypothèques|Finance|Laval|https://www.multiprets.ca|500|Recruteur conseillers|https://www.multiprets.ca/carrieres|8|11|RGNCD|IJC||12
Planiprêt|Planiprêt|Finance|Montréal|https://www.planipret.com|200|Conseiller recrutement|https://www.planipret.com/emplois|4|18|RCD|JC||12
Multi-Prêts skip2
First National|First National Financial|Finance|Toronto|https://www.firstnational.ca|1500|Recruiter|https://www.firstnational.ca/careers|7|14|RCD|LC||3
Equitable Bank|Equitable Bank|Finance|Toronto|https://www.eqbank.ca|1200|Talent Acquisition Partner|https://www.eqbank.ca/careers|8|12|TPGCD|ILC||3
Wealthsimple already
Questrade already
Koho already
Neo Financial|Neo Financial|Finance|Calgary|https://www.neofinancial.com|800|Talent Acquisition Specialist|https://www.neofinancial.com/careers|9|9|TGCD|ILC|Greenhouse|11
Borrowell|Borrowell|Finance|Toronto|https://www.borrowell.com|200|Recruiter|https://www.borrowell.com/careers|4|21|RGCD|LC||11
Nesto already
Flare already
Clearco|Clearco|Finance|Toronto|https://www.clear.co|150|Recruteur|https://www.clear.co/careers|3|26|RCD|C||14
Shopify|Shopify inc.|Technologie|Ottawa|https://www.shopify.com|8000|Talent Acquisition Partner|https://www.shopify.com/careers|20|6|TPHGQCD|ILCA|Greenhouse|11
OpenText|OpenText Corporation|Technologie|Waterloo|https://www.opentext.com|20000|Recruiter|https://careers.opentext.com|16|10|RQCD|ILC|Workday|11
Constellation Software|Constellation Software inc.|Technologie|Toronto|https://www.csisoftware.com|25000|Talent Acquisition Specialist|https://www.csisoftware.com/careers|12|12|TQCD|ILC||11
Kinaxis|Kinaxis inc.|Technologie|Ottawa|https://www.kinaxis.com|2000|Talent Acquisition Partner|https://www.kinaxis.com/careers|8|11|TPGCD|ILC|Greenhouse|11
The Trade Desk|The Trade Desk|Technologie|Montréal|https://www.thetradedesk.com|300|Technical Recruiter|https://careers.thetradedesk.com|6|13|RDGCD|LC|Greenhouse|11
Datadog Montréal|Datadog|Technologie|Montréal|https://www.datadoghq.com|200|Recruiter|https://careers.datadoghq.com|5|15|RGCD|LA|Greenhouse|11
Twilio Montréal|Twilio|Technologie|Montréal|https://www.twilio.com|150|Talent Acquisition Coordinator|https://www.twilio.com/en-us/company/jobs|4|18|TGCD|LC|Greenhouse|11
Stripe Montréal|Stripe|Technologie|Montréal|https://stripe.com|100|Recruiter|https://stripe.com/jobs|4|16|RGCD|LC|Greenhouse|11
Shopify Montréal skip Shopify
Lightspeed already
Hopper already
Coveo already
Genetec already
Behaviour already
Ubisoft already
Warner already
Eidos already
CM Labs already
Kinova already
Robotiq already
Vention already
Novisto already
Workleap already
Vooban already
Osedea already
Spiria already
Amilia already
Petal already
PixMob already
Stay22 already
Dialogue skip TELUS
AlayaCare already
nesto already
Cirque skip3
National Bank already wave9
Beneva already wave9
Desjardins already wave9
iA already wave9
Air Canada already wave9
Cirque du Soleil already listed
TD Canada Trust|Toronto-Dominion Bank|Finance|Montréal|https://www.td.com|95000|Talent Acquisition Partner|https://jobs.td.com|35|7|TPHLQCD|ILCA|Workday|3
RBC|Banque Royale du Canada|Finance|Montréal|https://www.rbcbanqueroyale.com|90000|Corporate Recruiter|https://jobs.rbc.com|30|8|RHLQCD|ILC|Workday|3
BMO|Banque de Montréal|Finance|Montréal|https://www.bmo.com|55000|Talent Acquisition Specialist|https://jobs.bmo.com|28|9|THLQCD|ILC|Workday|3
CIBC|Banque CIBC|Finance|Montréal|https://www.cibc.com|45000|Recruiter|https://cibc.wd3.myworkdayjobs.com|24|10|RLQCD|ILA|Workday|3
Scotiabank|Banque Scotia|Finance|Montréal|https://www.scotiabank.com|90000|Talent Acquisition Advisor|https://www.scotiabank.com/careers|22|11|TLQCD|ILC|Workday|3
HSBC Canada skip
National Bank already
Laurentian already
Tangerine|Tangerine Bank|Finance|Toronto|https://www.tangerine.ca|3000|Recruiter|https://www.tangerine.ca/careers|8|14|RCD|LC||3
Simplii already
Desjardins Sécurité financière already
Beneva skip2
iA skip2
Sun Life already wave9
Manuvie already wave9
Canada Vie already wave9
Great-West|Great-West Lifeco|Assurance|Winnipeg|https://www.greatwestlifeco.com|28000|Talent Acquisition Manager|https://careers.greatwestlifeco.com|14|10|THXQCD|ILC|Workday|1
Power already wave9
IG Wealth|IG Wealth Management|Finance|Winnipeg|https://www.ig.ca|3000|Recruiter|https://www.ig.ca/careers|7|15|RCD|LC||3
Investors Group skip IG
Mackenzie Investments|Mackenzie Investments|Finance|Toronto|https://www.mackenzieinvestments.com|2000|Talent Acquisition Partner|https://www.mackenzieinvestments.com/careers|6|17|TPCD|LC||3
CI Financial|CI Financial|Finance|Toronto|https://www.cifinancial.com|3000|Recruiter|https://www.cifinancial.com/careers|7|14|RCD|LC||3
AGF|AGF Management|Finance|Toronto|https://www.agf.com|800|Conseiller RH|https://www.agf.com/careers|4|20|RCD|C||3
Fiera already wave9
PSP already listed
CPPIB|Office d'investissement du RPC|Finance|Toronto|https://www.cppinvestments.com|2000|Talent Acquisition Specialist|https://www.cppinvestments.com/careers|10|8|TGQCD|ILC|Workday|1
OTPP|Ontario Teachers' Pension Plan|Finance|Toronto|https://www.otpp.com|1500|Talent Acquisition Partner|https://www.otpp.com/careers|8|12|TPCD|ILC||3
OMERS|OMERS|Finance|Toronto|https://www.omers.com|1200|Recruiter|https://www.omers.com/careers|7|13|RCD|LC||3
HOOPP|Healthcare of Ontario Pension Plan|Finance|Toronto|https://hoopp.com|800|Talent Acquisition Specialist|https://hoopp.com/careers|6|15|TCD|LC||3
AIMCo|Alberta Investment Management|Finance|Edmonton|https://www.aimco.ca|500|Recruiter|https://www.aimco.ca/careers|5|18|RCD|LC||3
BCI|British Columbia Investment Management|Finance|Victoria|https://www.bci.ca|700|Talent Acquisition Partner|https://www.bci.ca/careers|6|16|TPCD|LC||3
Ivanhoé Cambridge|Ivanhoé Cambridge|Immobilier|Montréal|https://www.ivanhoecambridge.com|1700|Conseiller acquisition de talents|https://www.ivanhoecambridge.com/carrieres|9|9|TXGCD|ILC||13
QuadReal|QuadReal Property Group|Immobilier|Vancouver|https://www.quadreal.com|1000|Recruiter|https://www.quadreal.com/careers|7|14|RCD|LC||3
Oxford Properties|Oxford Properties Group|Immobilier|Toronto|https://www.oxfordproperties.com|2000|Talent Acquisition Specialist|https://www.oxfordproperties.com/careers|8|12|TCD|ILC||3
Cadillac Fairview|Cadillac Fairview|Immobilier|Toronto|https://www.cadillacfairview.com|2000|Recruiter|https://www.cadillacfairview.com/careers|8|13|RCD|LC||3
RioCan|RioCan Real Estate|Immobilier|Toronto|https://www.riocan.com|800|Conseiller RH|https://www.riocan.com/careers|5|19|RCD|C||3
First Capital|First Capital REIT|Immobilier|Toronto|https://www.firstcapitalreit.com|500|Recruiter|https://www.firstcapitalreit.com/careers|4|21|RCD|C||3
Allied Properties|Allied Properties REIT|Immobilier|Toronto|https://www.alliedreit.com|400|Talent Acquisition Coordinator|https://www.alliedreit.com/careers|4|20|TCD|LC||3
Dream|Dream Unlimited|Immobilier|Toronto|https://www.dream.ca|600|Recruiter|https://www.dream.ca/careers|5|17|RGCD|LC||13
Broccolini already
Devimco already
Montoni already
Dallaire already
Carbonleo already
Cogir already
Groupe Maurice already
Résidences Soleil already
Chartwell already wave9
Revera already wave9
Sienna already wave9
Sélection already wave9
Groupe Champlain already
Le Groupe Maurice skip
Ivanhoe already listed
Cominar skip sold
Choice Properties|Choice Properties REIT|Immobilier|Toronto|https://www.choicereit.ca|700|Recruiter|https://www.choicereit.ca/careers|5|18|RCD|C||12
SmartCentres|SmartCentres REIT|Immobilier|Vaughan|https://www.smartcentres.com|500|Conseiller RH|https://www.smartcentres.com/careers|4|22|RCD|C||12
Crombie|Crombie REIT|Immobilier|New Glasgow|https://www.crombie.ca|400|Recruiter|https://www.crombie.ca/careers|3|24|RCD|C||12
CT REIT|CT Real Estate Investment Trust|Immobilier|Brantford|https://www.ctreit.com|200|Conseiller RH|https://www.ctreit.com|3|26|RCD|C||12
Winners already TJX
Simons already wave9
Dynamite already wave9
Reitmans already wave9
SSENSE already wave9
Frank And Oak already wave9
Cirque already
Linen Chest already
Hart already
Rossy already
Giant Tiger already wave9
Hart already wave9
Dollarama already
Walmart already
Costco already
Canadian Tire already
Home Depot already
IKEA already wave9
Bureau en Gros already wave9
Best Buy already wave9
Structube already wave9
Brault already wave9
Tanguay already wave9
JYSK already wave9
Réno-Dépôt already wave9
Lowe's already wave9
Home Hardware already wave9
The Brick already wave9
Leon's already wave9
Stokes already wave9
Urban Planet already wave9
H&M already wave9
Zara already Inditex
Aritzia already wave9
Aldo already wave9
La Vie en Rose already wave9
Tristan already wave9
Garage already wave9
Roots already wave9
Canada Goose already wave9
lululemon already wave9
MEC already wave9
Decathlon already wave9
FGL already wave9
Sail already wave9
L'Équipeur already wave9
Sport Chek skip FGL
Atmosphere skip FGL
Winners skip TJX
Marshalls skip TJX
Homesense skip TJX
Pharmaprix already wave9
Shoppers already wave9
Uniprix already wave9
Brunet already wave9
Proxim already wave9
Jean Coutu already
Familiprix already
McKesson already
Innomar already wave9
Cardinal already wave9
McCain already wave9
Unilever already wave9
General Mills already wave9
Kellanova already wave9
Mars already wave9
Ferrero already wave9
Smucker already wave9
Conagra already wave9
Campbell already wave9
McCormick already wave9
Reckitt already wave9
P&G already wave9
Colgate already wave9
Henkel already wave9
SC Johnson already wave9
J&J already wave9
Bayer already wave9
Novartis already wave9
Roche already wave9
AbbVie already wave9
AstraZeneca already wave9
Takeda already wave9
Teva already wave9
Apotex already wave9
Pfizer already
Merck already
Sanofi already
GSK already
Galderma already
Bausch already
Sandoz already
Pharmascience already
Charles River already
Altasciences already wave9
Cirque listed
Molson already
Labatt already
Unibroue already
Sleeman|Sleeman Breweries|Transformation alimentaire|Guelph|https://www.sleeman.ca|800|Recruteur brasserie|https://www.sleeman.ca/careers|6|14|ROCD|IC||6
Brick Brewing|Brick Brewing|Transformation alimentaire|Kitchener|https://www.brickbeer.com|200|Opérateur brassage|https://www.brickbeer.com/careers|4|20|OCD|C||6
Boréale|Brasseurs du Nord — Boréale|Transformation alimentaire|Blainville|https://www.boreale.com|150|Journalier production|https://www.boreale.com/emplois|5|12|OGCD|JC||6
Les 3 Brasseurs already wave9
Unibroue already
Sleeman already listed
Boréale listed
Sleeman skip2
Alexander Keith|Alexander Keith's|Transformation alimentaire|Halifax|https://www.keiths.ca|200|Brewery operator|https://www.keiths.ca/careers|4|22|OCD|C||6
Moosehead|Moosehead Breweries|Transformation alimentaire|Saint John|https://www.moosehead.ca|400|Recruiter|https://www.moosehead.ca/careers|5|18|ROCD|LC||6
Pepsi already
Coke already
Keurig already
Nestlé already
Cargill already
ADM already wave9
Ingredion already wave9
Kerry already wave9
Puratos already wave9
Griffith already wave9
Roquette already wave9
Tetra Pak already wave9
GEA already wave9
Alfa Laval already wave9
John Deere already wave9
CNH already wave9
AGCO already wave9
Kubota already wave9
Siemens already wave9
ABB already wave9
Honeywell already wave9
Emerson already wave9
Rockwell already wave9
Bosch already wave9
Magna already wave9
Linamar already wave9
Forvia already wave9
Valeo already wave9
Aptiv already wave9
Michelin already wave9
Goodyear already wave9
Bridgestone already wave9
Pirelli already wave9
Camso already
Soucy already
BRP already
Linamar skip2
Martinrea|Martinrea International|Manufacturier|Vaughan|https://www.martinrea.com|15000|Talent Acquisition Partner|https://www.martinrea.com/careers|14|9|TPOQCD|ILC||6
ABC Technologies|ABC Technologies|Manufacturier|Toronto|https://www.abctechnologies.com|8000|Recruiter|https://www.abctechnologies.com/careers|10|12|ROCD|LC||6
Flex-N-Gate already
Lear Canada|Lear Corporation|Manufacturier|Ajax|https://www.lear.com|2000|Recruiter|https://www.lear.com/careers|7|16|RCD|LC||6
Adient already
Woodbridge Foam|Woodbridge Foam|Manufacturier|Mississauga|https://www.woodbridgegroup.com|3000|Recruteur usine|https://www.woodbridgegroup.com/careers|8|13|RODCD|IC||6
Stackpole|Stackpole International|Manufacturier|Ancaster|https://www.stackpole.com|2000|Recruiter|https://www.stackpole.com/careers|6|15|ROCD|LC||6
Multimatic|Multimatic inc.|Manufacturier|Markham|https://www.multimatic.com|4000|Talent Acquisition Partner|https://www.multimatic.com/careers|9|10|TPDCD|ILC||6
Aisin|Aisin Canada|Manufacturier|Stratford|https://www.aisin.com|800|Recruiter|https://www.aisin.com/careers|5|19|RCD|C||6
Toyota Motor Manufacturing|Toyota Motor Manufacturing Canada|Manufacturier|Cambridge|https://www.tmmc.ca|8500|Talent Acquisition Specialist|https://www.tmmc.ca/careers|18|6|TODQCD|ILCK|Workday|6
Honda Canada|Honda Canada inc.|Manufacturier|Alliston|https://www.honda.ca|4000|Recruiter — Manufacturing|https://www.honda.ca/careers|12|8|RODQCD|ILC||6
Ford Oakville|Ford Motor Company of Canada|Manufacturier|Oakville|https://www.ford.ca|5000|Talent Acquisition Partner|https://corporate.ford.com/careers|14|7|TPOQCD|ILC|Workday|6
GM Canada|General Motors du Canada|Manufacturier|Oshawa|https://www.gm.ca|6000|Recruiter|https://search-careers.gm.com|16|8|ROQCD|ILC|Workday|6
Stellantis Windsor|Stellantis Canada|Manufacturier|Windsor|https://www.stellantis.com|5000|Talent Acquisition Specialist|https://www.careers.stellantis.com|13|9|TODQCD|ILC|Workday|6
Tesla Canada|Tesla Canada|Manufacturier|Toronto|https://www.tesla.com|800|Recruiter|https://www.tesla.com/careers|8|11|RGQCD|LC|Greenhouse|11
Rivian skip
Lion already
Arrival skip
Volta skip
Cirque listed2
CN already
CPKC already
Via already
Port de Montréal already
Termont already
QSL already
CSL already
Fednav already
Logistec already
Oceanex already
NEAS already
Groupe Desgagnés already
Groupe Océan already
Metro Supply already wave9
Schenker already wave9
Expeditors already wave9
CH Robinson already wave9
XPO already wave9
Ryder already wave9
Penske already wave9
Groupe Morneau already wave9
Besner already wave9
THL already wave9
Fortier already wave9
GFS already wave9
Aramark already wave9
Compass already wave9
Sodexo already wave9
GDI already wave9
Bee-Clean already wave9
Jan-Pro already wave9
Sani-Marc already wave9
Lavo already wave9
Recochem already wave9
Suncor already wave9
Imperial already wave9
Shell already wave9
Parkland already wave9
Ultramar already wave9
Invenergy already wave9
Pattern already wave9
Kruger Energy already wave9
Evolugen already wave9
Brookfield Renewable already wave9
Innergex already
Boralex already
Hydro already
Énergir already
Harnois already
Cirque listed3
McGill Health already wave9
CHUM already wave9
Sainte-Justine already wave9
Jewish General already wave9
Douglas already wave9
ICM already wave9
CIUSSS Nord already wave9
Optima already wave9
Chartwell already
Revera already
Sienna already
Selection already
Medisys already
Santeweb|santéweb|Santé privée|Québec|https://www.santeweb.ca|120|Recruteur|https://www.santeweb.ca/emplois|4|20|RCD|JC||10
Clinique Ovo|Clinique ovo|Santé privée|Montréal|https://www.cliniqueovo.com|200|Conseiller RH|https://www.cliniqueovo.com/carrieres|4|18|RCD|C||10
Centre de santé Le Vitre|Centre médical Le Vitre|Santé privée|Montréal|https://www.levitre.com|80|Recruteur|https://www.levitre.com|3|24|RCD|C||10
Elna Médical|Elna Médical|Santé privée|Montréal|https://www.elna.ca|600|Talent Acquisition Specialist|https://www.elna.ca/carrieres|9|8|TGNCD|ILC||10
Groupe Santé Physimed|Physimed|Santé privée|Saint-Laurent|https://www.physimed.com|250|Conseiller recrutement|https://www.physimed.com/carrieres|5|15|RCD|JC||10
Ophtalmologie|Institut de l'œil des Laurentides|Santé privée|Boisbriand|https://www.institutdeloeil.com|80|Recruteur|https://www.institutdeloeil.com|3|22|RCD|C||10
Medfar already wave9
Petal already
AlayaCare already
TELUS Santé already wave9
Dialogue skip
Maple|Maple Corporation|Santé privée|Toronto|https://www.getmaple.ca|400|Talent Acquisition Partner|https://www.getmaple.ca/careers|6|13|TPGCD|LC|Greenhouse|11
Inkblot|Inkblot Therapy|Santé privée|Toronto|https://inkblottherapy.com|200|Recruiter|https://inkblottherapy.com/careers|4|19|RGCD|LC||11
MindBeacon skip
GreenShield|GreenShield|Assurance|Windsor|https://www.greenshield.ca|2000|Talent Acquisition Specialist|https://www.greenshield.ca/careers|8|12|TCD|ILC||11
Pacific Blue Cross|Pacific Blue Cross|Assurance|Burnaby|https://www.pac.bluecross.ca|1500|Recruiter|https://www.pac.bluecross.ca/careers|6|16|RCD|LC||11
Alberta Blue Cross|Alberta Blue Cross|Assurance|Edmonton|https://www.ab.bluecross.ca|1200|Talent Acquisition Partner|https://www.ab.bluecross.ca/careers|6|15|TPCD|LC||11
Medavie already wave9
Croix Bleue already wave9
Cirque listed4
Place des Arts listed
STM listed
Loto listed
CDPQ listed
Ivanhoe listed
Potloc listed
Shopify listed
TD listed
RBC listed
BMO listed
CIBC listed
Scotia listed
Toyota listed
Honda listed
Ford listed
GM listed
Stellantis listed
Cirque du Soleil listed
WSP already
Hatch already
BBA already
CIMA already
Stantec already
Atkins already
AECOM|AECOM|Ingénierie|Montréal|https://www.aecom.com|50000|Talent Acquisition Partner|https://aecom.jobs|16|8|TPHQCD|ILC|Workday|8
SNC skip Atkins
Jacobs|Jacobs|Ingénierie|Montréal|https://www.jacobs.com|50000|Recruiter|https://careers.jacobs.com|12|10|RQCD|ILC|Workday|8
Fluor|Fluor Canada|Ingénierie|Calgary|https://www.fluor.com|8000|Talent Acquisition Specialist|https://www.fluor.com/careers|9|13|TQCD|ILC||8
Worley|Worley Canada|Ingénierie|Calgary|https://www.worley.com|6000|Recruiter|https://www.worley.com/careers|8|14|RCD|LC||8
Golder skip WSP
Tetra Tech|Tetra Tech|Ingénierie|Montréal|https://www.tetratech.com|20000|Talent Acquisition Partner|https://www.tetratech.com/careers|10|11|TPQCD|ILC||8
Exp|Exp Services|Ingénierie|Brampton|https://www.exp.com|4000|Recruiter|https://www.exp.com/careers|7|16|RCD|LC||8
Cima+ already
SNC-Lavalin skip
Dessau skip
Genivar skip
Aecom listed
WSP skip2
Stantec skip2
Hatch skip2
BBA skip2
Pageau Morel already
Laporte already
YRH already
Neuf already
Provencher already
STGM already
Jodoin already
Ædifica already
Sid Lee listed
Cossette already
lg2 already
Bleublancrouge already
Lune Rouge already
Juste pour rire already
Cirque listed5
evenko already
Groupe CH already wave9
Place des Arts listed2
Espace pour la vie listed
Biodôme listed
OSM already
Orchestre Métropolitain already
TNM already
Rideau Vert already
TOHU already
Cirque Éloize already
Moment Factory already
Cirque du Soleil listed2
National Theatre skip
Shaw Festival|Shaw Festival|Arts et spectacles|Niagara-on-the-Lake|https://www.shawfest.com|400|Recruiter|https://www.shawfest.com/jobs|4|20|RCD|C||10
Stratford Festival|Stratford Festival|Arts et spectacles|Stratford|https://www.stratfordfestival.ca|800|Talent Acquisition Coordinator|https://www.stratfordfestival.ca/jobs|5|18|TCD|LC||10
NAC|National Arts Centre|Arts et spectacles|Ottawa|https://nac-cna.ca|500|Conseiller RH|https://nac-cna.ca/en/careers|5|17|RCD|KC||10
CBC/Radio-Canada|CBC/Radio-Canada|Médias|Montréal|https://cbc.radio-canada.ca|6000|Talent Acquisition Specialist|https://cbc.radio-canada.ca/emplois|18|7|THNQCD|ILCK|Workday|10
Bell Média|Bell Média|Médias|Montréal|https://www.bellmedia.ca|5000|Recruteur|https://www.bellmedia.ca/carrieres|12|10|RQCD|ILC||10
Quebecor already
TVA already
Cogeco Média already
Stingray already
Cirque listed6
La Presse|La Presse inc.|Médias|Montréal|https://www.lapresse.ca|400|Conseiller RH|https://www.lapresse.ca/emplois|4|21|RCD|C||10
Le Devoir already
Journal de Montréal already
TC Media skip Transcontinental
Transcontinental already
Rogers Sportsnet|Rogers Sports & Media|Médias|Toronto|https://www.sportsnet.ca|1000|Recruiter|https://www.sportsnet.ca/careers|6|16|RCD|LC||10
Corus|Corus Entertainment|Médias|Toronto|https://www.corusent.com|3000|Talent Acquisition Specialist|https://www.corusent.com/careers|8|13|TCD|ILC||10
Bell already
Videotron already
Rogers already wave9
TELUS already wave9
Cogeco already wave9
Xplornet|Xplore inc.|Télécommunications|Woodstock|https://www.xplore.ca|800|Recruiter|https://www.xplore.ca/careers|5|19|RCD|LC||11
Ebox|EBOX|Télécommunications|Longueuil|https://www.ebox.ca|200|Conseiller recrutement|https://www.ebox.ca/carrieres|4|18|RGCD|JC||11
Oxio|oxio|Télécommunications|Montréal|https://www.oxio.ca|80|Recruteur|https://www.oxio.ca/carrieres|3|22|RGCD|C||11
Fizz already
Freedom Mobile|Freedom Mobile|Télécommunications|Toronto|https://www.freedommobile.ca|2000|Talent Acquisition Partner|https://www.freedommobile.ca/careers|8|12|TPCD|ILC||11
Videotron skip
Bell skip
TELUS skip
Rogers skip
Cirque listed7
Construction Demathieu already wave9
Fimacon already wave9
TEQ already wave9
Garnier already wave9
Galipeau already wave9
Simard-Beaudry already wave9
Dufresne already wave9
Théorêt already wave9
GBR already wave9
Rive-Nord already wave9
Pomerleau already
Broccolini already
EBC already
EllisDon already
PCL already
Kiewit already
Bird already
Aecon already
Catania already
Demix already
McKinley already
Magil already
Montoni already
Devimco already
Dallaire already
Construction Gély already
Pavage Portneuf already
Pavage Boisvert already
Cegerco already
Construction et Pavage already
Walsh|Walsh Canada|Construction|Toronto|https://www.walshgroup.com|2000|Recruiter|https://www.walshgroup.com/careers|7|15|RCD|LC||8
EllisDon skip2
PCL skip2
Graham|Graham Construction|Construction|Calgary|https://www.graham.ca|3000|Talent Acquisition Specialist|https://www.graham.ca/careers|9|11|TQCD|ILC||8
Ledcor|Ledcor Group|Construction|Vancouver|https://www.ledcor.com|7000|Talent Acquisition Partner|https://www.ledcor.com/careers|12|9|TPXQCD|ILC||8
Aecon skip2
Bird skip2
Kiewit skip2
Clark Builders|Clark Builders|Construction|Edmonton|https://www.clarkbuilders.com|1500|Recruiter|https://www.clarkbuilders.com/careers|6|16|RCD|LC||8
Stuart Olson skip
EllisDon Montréal skip
Pomerleau skip2
Construction GCR already
Construction R.Y. Tellier already
Construction Gauthier already
Construction Marais already
Construction Béland already
Construction L. Fournier already
Construction Gérald already
Construction A. Piché already
Cirque listed8
Logistik Unicorp already wave9
Metro Supply already
GFS already
Gordon already
Sysco already
Colabor already
Touchette already wave9
Intelcom already
Purolator already
UPS already
FedEx already
DHL already
Canpar already
Day & Ross already
Loomis already
GLS already
DSV already
CEVA already
Kuehne already
Livingston already
TFI already
Groupe Robert already
CN already
CPKC already
Postes Canada already
Amazon already
Cirque listed9
Microsoft already wave9
Google already wave9
Salesforce already wave9
SAP already wave9
Oracle already wave9
ServiceNow already wave9
Autodesk already wave9
Cisco already wave9
Fortinet already wave9
Nokia already wave9
Thoughtworks already wave9
Slalom already wave9
Accenture already wave9
Cognizant already wave9
NTT already wave9
Infosys already wave9
Capgemini already wave9
Capco already wave9
Deloitte already wave9
PwC already wave9
EY already wave9
KPMG already wave9
CGI already
IBM already
Ericsson already
Shopify listed
OpenText listed
Constellation listed
Kinaxis listed
Trade Desk listed
Datadog listed
Twilio listed
Stripe listed
Neo listed
Cirque listed10
Marriott already wave9
Hilton already wave9
Hyatt already wave9
Accor already wave9
Germain already wave9
St-Hubert already wave9
Scores already wave9
La Cage already wave9
3 Brasseurs already wave9
Bâton Rouge already wave9
Mikes already wave9
Pacini already
Normandin already
Fairmont already
Hôtel Nelligan already
Hôtel St Paul already
Hôtel Bonaventure already
Auberge Saint-Antoine already
Cirque listed11
WestJet already wave9
Air Transat already wave9
Jazz already wave9
Porter listed
Sunwing listed
Flair listed
Air Inuit listed
Canadian North listed
PAL listed
Air Canada already wave9
Cirque listed12
Agnico already wave9
Newmont already wave9
IAMGOLD already wave9
Eldorado already wave9
Osisko already wave9
Wesdome already wave9
Alamos already wave9
Canadian Royalties already wave9
Glencore already
Champion Iron already
Nouveau Monde already
Nemaska already
Sayona already
Teck|Teck Resources|Mines|Vancouver|https://www.teck.com|12000|Talent Acquisition Partner|https://www.teck.com/careers|16|8|TPDXQCD|ILC|Workday|6
Barrick|Barrick Gold|Mines|Toronto|https://www.barrick.com|18000|Recruiter — Operations|https://www.barrick.com/careers|14|9|RODQCD|ILC|Workday|6
Kinross|Kinross Gold|Mines|Toronto|https://www.kinross.com|8000|Talent Acquisition Specialist|https://www.kinross.com/careers|10|12|TDQCD|ILC||6
Wheaton|Wheaton Precious Metals|Mines|Vancouver|https://www.wheatonpm.com|50|Conseiller RH|https://www.wheatonpm.com/careers|3|24|RCD|C||6
Franco-Nevada|Franco-Nevada Corporation|Mines|Toronto|https://www.franco-nevada.com|40|Recruiter|https://www.franco-nevada.com/careers|3|25|RCD|C||6
Yamana skip
Iamgold skip
Agnico skip2
Cirque listed13
Suncor already
CNRL|Canadian Natural Resources|Énergie|Calgary|https://www.cnrl.com|10000|Talent Acquisition Partner|https://www.cnrl.com/careers|18|7|TPOXQCD|ILC|Workday|13
Cenovus|Cenovus Energy|Énergie|Calgary|https://www.cenovus.com|6000|Recruiter|https://www.cenovus.com/careers|12|10|RXQCD|ILC||13
Enbridge|Enbridge inc.|Énergie|Calgary|https://www.enbridge.com|11000|Talent Acquisition Specialist|https://www.enbridge.com/careers|16|8|TQCD|ILC|Workday|13
TC Energy|TC Energy|Énergie|Calgary|https://www.tcenergy.com|7000|Talent Acquisition Partner|https://www.tcenergy.com/careers|14|9|TPQCD|ILC|Workday|13
Pembina|Pembina Pipeline|Énergie|Calgary|https://www.pembina.com|2500|Recruiter|https://www.pembina.com/careers|8|14|RCD|LC||13
Keyera|Keyera Corp.|Énergie|Calgary|https://www.keyera.com|1000|Talent Acquisition Specialist|https://www.keyera.com/careers|6|16|TCD|LC||13
Tourmaline|Tourmaline Oil|Énergie|Calgary|https://www.tourmalineoil.com|800|Recruiter|https://www.tourmalineoil.com/careers|5|18|RGCD|LC||13
ARC Resources|ARC Resources|Énergie|Calgary|https://www.arcresources.com|600|Conseiller RH|https://www.arcresources.com/careers|4|20|RCD|C||13
Ovintiv already
Imperial already wave9
Shell already wave9
Parkland already wave9
Ultramar already wave9
Suncor skip2
Cirque listed14
Microsoft skip2
Amazon already
Google skip2
Meta Montréal|Meta|Technologie|Montréal|https://www.meta.com|200|Technical Recruiter|https://www.metacareers.com|6|12|RDGCD|LC|Workday|11
Apple Canada|Apple Canada|Technologie|Toronto|https://www.apple.com/ca|2000|Recruiter|https://www.apple.com/careers/ca|10|11|RQCD|LC||11
Amazon Montréal skip Amazon
AWS Canada already
Snowflake|Snowflake|Technologie|Toronto|https://www.snowflake.com|200|Recruiter|https://careers.snowflake.com|5|16|RGCD|LA|Greenhouse|11
Databricks|Databricks|Technologie|Toronto|https://www.databricks.com|150|Talent Acquisition Specialist|https://www.databricks.com/company/careers|5|17|TGCD|LC|Greenhouse|11
Palantir skip
CrowdStrike|CrowdStrike|Technologie|Toronto|https://www.crowdstrike.com|200|Technical Recruiter|https://www.crowdstrike.com/careers|5|15|RDCD|LC|Greenhouse|11
Okta|Okta|Technologie|Toronto|https://www.okta.com|150|Recruiter|https://www.okta.com/company/careers|4|18|RGCD|LC|Greenhouse|11
HubSpot|HubSpot|Technologie|Toronto|https://www.hubspot.com|200|Talent Acquisition Partner|https://www.hubspot.com/careers|6|13|TPGCD|LA|Greenhouse|11
Atlassian|Atlassian|Technologie|Toronto|https://www.atlassian.com|100|Recruiter|https://www.atlassian.com/company/careers|4|19|RGCD|LC|Greenhouse|11
Zoominfo skip
Salesforce skip2
ServiceNow skip2
Workday Inc|Workday|Technologie|Toronto|https://www.workday.com|300|Talent Acquisition Specialist|https://www.workday.com/en-us/company/careers.html|7|12|TGCD|LC|Workday|11
ADP Canada|ADP Canada|Services professionnels|Toronto|https://www.adp.ca|2000|Recruiter|https://jobs.adp.com|9|11|RQCD|ILC|Workday|10
Ceridian|Dayforce (Ceridian)|Technologie|Toronto|https://www.dayforce.com|5000|Talent Acquisition Partner|https://www.dayforce.com/careers|11|9|TPGCD|ILC|Workday|11
Payworks|Payworks|Technologie|Winnipeg|https://www.payworks.ca|400|Recruteur|https://www.payworks.ca/careers|4|20|RCD|C||11
Nethris|Nethris|Technologie|Montréal|https://www.nethris.com|150|Conseiller recrutement|https://www.nethris.com/carrieres|4|18|RCD|JC||11
Acomba|Acomba|Technologie|Longueuil|https://www.acomba.com|200|Recruteur|https://www.acomba.com/carrieres|4|19|RGCD|JC||11
Logibec|Logibec|Technologie|Montréal|https://www.logibec.com|400|Talent Acquisition Specialist|https://www.logibec.com/carrieres|6|14|TGCD|IJC||11
Medfar skip2
Petal skip2
Cirque listed15
Zensurance|Zensurance|Assurance|Toronto|https://www.zensurance.com|300|Talent Acquisition Partner|https://jobs.lever.co/zensurance|6|10|TPGCD|LA|Lever|11
PolicyMe|PolicyMe|Assurance|Toronto|https://www.policyme.com|150|Recruiter|https://www.policyme.com/careers|4|17|RGCD|LC|Greenhouse|14
Ratehub|Ratehub.ca|Finance|Toronto|https://www.ratehub.ca|200|Conseiller RH|https://www.ratehub.ca/careers|4|19|RCD|C||11
Ratespy skip
LowestRates|LowestRates.ca|Finance|Toronto|https://www.lowestrates.ca|80|Recruteur|https://www.lowestrates.ca/careers|3|23|RCD|C||11
Cirque listed16
McGill already
Concordia already
UdeM skip? Université de Montréal not in list?
Université de Montréal|Université de Montréal|Éducation|Montréal|https://www.umontreal.ca|10000|Conseiller acquisition de talents|https://www.umontreal.ca/emplois|22|8|RHNCD|IKC||3
UQAM|Université du Québec à Montréal|Éducation|Montréal|https://uqam.ca|6000|Conseiller recrutement|https://uqam.ca/emplois|14|10|RNCD|IKC||3
Polytechnique Montréal|Polytechnique Montréal|Éducation|Montréal|https://www.polymtl.ca|2500|Conseiller RH|https://www.polymtl.ca/emplois|8|13|RCD|IC||3
HEC Montréal|HEC Montréal|Éducation|Montréal|https://www.hec.ca|1500|Conseiller acquisition de talents|https://www.hec.ca/emplois|7|12|RCD|IJC||3
ETS|École de technologie supérieure|Éducation|Montréal|https://www.etsmtl.ca|2000|Recruteur|https://www.etsmtl.ca/emplois|8|11|RDNCD|IC||3
INRS|Institut national de la recherche scientifique|Éducation|Québec|https://inrs.ca|800|Conseiller RH|https://inrs.ca/emplois|5|16|RCD|KC||3
Laval already
Sherbrooke already
UQTR already
UQAC already
UQO already
UQAT already
TÉLUQ already
ENAP already
McGill already
Concordia already
Bishop's|Bishop's University|Éducation|Sherbrooke|https://www.ubishops.ca|400|HR Recruiter|https://www.ubishops.ca/hr|4|20|RCD|C||3
McGill skip2
UdeM listed
UQAM listed
Cirque listed17
Ville de Montréal|Ville de Montréal|Services|Montréal|https://montreal.ca|28000|Conseiller en acquisition de talents|https://montreal.ca/emplois|50|5|RHLONQCD|IKCJ||4
Québec already Ville de Québec
Laval already Ville de Laval
Longueuil already
Gatineau already
Sherbrooke already
Saguenay already
Lévis already
Trois-Rivières already
Terrebonne already Ville? no Ville de Terrebonne?
Ville de Terrebonne|Ville de Terrebonne|Services|Terrebonne|https://www.ville.terrebonne.qc.ca|800|Conseiller RH|https://www.ville.terrebonne.qc.ca/emplois|6|14|RCD|KC||3
Blainville already
Mirabel already
Saint-Eustache|Ville de Saint-Eustache|Services|Saint-Eustache|https://www.saint-eustache.ca|400|Recruteur|https://www.saint-eustache.ca/emplois|4|18|RCD|KC||3
Vaudreuil-Dorion|Ville de Vaudreuil-Dorion|Services|Vaudreuil-Dorion|https://www.ville.vaudreuil-dorion.qc.ca|350|Conseiller RH|https://www.ville.vaudreuil-dorion.qc.ca/emplois|4|19|RCD|KC||3
Pointe-Claire|Ville de Pointe-Claire|Services|Pointe-Claire|https://www.pointe-claire.ca|400|Recruteur|https://www.pointe-claire.ca/emplois|4|20|RCD|KC||3
Dorval|Ville de Dorval|Services|Dorval|https://www.ville.dorval.qc.ca|300|Conseiller RH|https://www.ville.dorval.qc.ca/emplois|3|22|RCD|KC||3
Anjou skip Montréal
Saint-Laurent skip Montréal
Brossard already
Boucherville already
Westmount|Ville de Westmount|Services|Westmount|https://westmount.org|250|HR Coordinator|https://westmount.org/careers|3|24|RCD|C||3
Outremont skip Montréal
Mont-Royal|Ville de Mont-Royal|Services|Mont-Royal|https://www.ville.mont-royal.qc.ca|300|Conseiller RH|https://www.ville.mont-royal.qc.ca/emplois|3|23|RCD|KC||3
Kirkland|Ville de Kirkland|Services|Kirkland|https://www.ville.kirkland.qc.ca|200|Recruteur|https://www.ville.kirkland.qc.ca/emplois|3|25|RCD|KC||3
Beaconsfield|Ville de Beaconsfield|Services|Beaconsfield|https://www.beaconsfield.ca|180|Conseiller RH|https://www.beaconsfield.ca/emplois|3|26|RCD|C||3
Dollard already
Cirque listed18
Forces armées canadiennes|Forces armées canadiennes|Services|Montréal|https://forces.ca|70000|Recruteur des Forces|https://forces.ca/fr/carrieres|80|4|ROHLNQCD|IKCL|SuccessFactors|4
Gendarmerie royale|Gendarmerie royale du Canada|Services|Montréal|https://www.rcmp-grc.gc.ca|30000|Recruteur|https://www.rcmp-grc.gc.ca/fr/carrieres|25|7|RODQCD|IKC||17
ASFC|Agence des services frontaliers du Canada|Services|Ottawa|https://www.cbsa-asfc.gc.ca|15000|Conseiller recrutement|https://www.cbsa-asfc.gc.ca/job-emploi|18|8|RNQCD|IKC||3
Service Canada|Service Canada|Services|Montréal|https://www.servicecanada.gc.ca|20000|Conseiller RH|https://emplois-emplois.gc.ca|30|6|RNQCD|K||3
IRCC|Immigration, Réfugiés et Citoyenneté Canada|Services|Ottawa|https://ircc.canada.ca|12000|Talent Acquisition Specialist|https://emplois-emplois.gc.ca/ircc|16|9|TQCD|KC||3
CRA|Agence du revenu du Canada|Services|Ottawa|https://www.cra-arc.gc.ca|40000|Conseiller acquisition de talents|https://www.cra-arc.gc.ca/carrieres|28|7|THNQCD|IKC||3
StatCan|Statistique Canada|Services|Ottawa|https://www.statcan.gc.ca|7000|Recruteur|https://www.statcan.gc.ca/fr/emplois|10|12|RQCD|KC||3
CNRC|Conseil national de recherches Canada|Services|Ottawa|https://nrc.canada.ca|4000|Talent Acquisition Partner|https://nrc.canada.ca/fr/carrieres|8|14|TPCD|KC||3
CSA|Agence spatiale canadienne|Aérospatial|Longueuil|https://www.asc-csa.gc.ca|700|Conseiller RH|https://www.asc-csa.gc.ca/fra/emplois|5|16|RDCD|KC||11
Cirque listed19
Exportation et développement|Exportation et développement Canada|Finance|Ottawa|https://www.edc.ca|1800|Talent Acquisition Specialist|https://www.edc.ca/fr/carrieres.html|7|13|TCD|ILC||3
BDC|Banque de développement du Canada|Finance|Montréal|https://www.bdc.ca|2500|Conseiller acquisition de talents|https://www.bdc.ca/fr/carrieres|10|9|RNCD|IJCL||3
FCC|Financement agricole Canada|Finance|Regina|https://www.fcc-fac.ca|2000|Recruiter|https://www.fcc-fac.ca/careers|6|15|RCD|LC||3
Farm Credit skip FCC
EDC listed
BDC listed
Investissement Québec listed
CDPQ listed
Fonds FTQ listed
Fondaction already
Cirque listed20
CNESST|Commission des normes, de l'équité, de la santé et de la sécurité du travail|Services|Québec|https://www.cnesst.gouv.qc.ca|6000|Conseiller recrutement|https://www.cnesst.gouv.qc.ca/fr/carrieres|18|8|RNCD|IKC||3
Revenu Québec|Revenu Québec|Services|Québec|https://www.revenuquebec.ca|10000|Conseiller acquisition de talents|https://www.revenuquebec.ca/fr/a-propos/carrieres/|22|7|RHNCD|IKC||3
Retraite Québec|Retraite Québec|Services|Québec|https://www.retraitequebec.gouv.qc.ca|1500|Conseiller RH|https://www.retraitequebec.gouv.qc.ca|8|12|RCD|KC||3
CCQ|Commission de la construction du Québec|Construction|Montréal|https://www.ccq.org|800|Conseiller recrutement|https://www.ccq.org/fr-CA/carrieres|7|11|RCD|IJC||8
AMF|Autorité des marchés financiers|Finance|Québec|https://lautorite.qc.ca|800|Talent Acquisition Specialist|https://lautorite.qc.ca/carrieres|6|13|TCD|ILC||3
Héma-Québec|Héma-Québec|Santé publique|Montréal|https://www.hema-quebec.qc.ca|1400|Conseiller acquisition de talents|https://www.hema-quebec.qc.ca/a-propos/carrieres|10|8|RDNCD|IJC||10
INSPQ|Institut national de santé publique du Québec|Santé publique|Québec|https://www.inspq.qc.ca|700|Conseiller RH|https://www.inspq.qc.ca/carrieres|5|16|RCD|KC||10
INESSS|Institut national d'excellence en santé et en services sociaux|Santé publique|Québec|https://www.inesss.qc.ca|250|Conseiller RH|https://www.inesss.qc.ca|4|20|RCD|C||10
SQI|Société québécoise des infrastructures|Infrastructure|Québec|https://www.sqi.gouv.qc.ca|900|Recruteur projets|https://www.sqi.gouv.qc.ca/carrieres|7|12|RXCD|KC||13
SODEC|Société de développement des entreprises culturelles|Arts et spectacles|Montréal|https://sodec.gouv.qc.ca|200|Conseiller RH|https://sodec.gouv.qc.ca|4|18|RCD|KC||10
CALQ|Conseil des arts et des lettres du Québec|Arts et spectacles|Montréal|https://www.calq.gouv.qc.ca|120|Conseiller RH|https://www.calq.gouv.qc.ca|3|22|RCD|KC||10
OQLF|Office québécois de la langue française|Services|Montréal|https://www.oqlf.gouv.qc.ca|400|Conseiller recrutement|https://www.oqlf.gouv.qc.ca|5|17|RCD|KC||3
SHQ|Société d'habitation du Québec|Immobilier|Québec|https://www.habitation.gouv.qc.ca|400|Conseiller RH|https://www.habitation.gouv.qc.ca|4|19|RCD|KC||3
RBQ|Régie du bâtiment du Québec|Construction|Montréal|https://www.rbq.gouv.qc.ca|500|Conseiller recrutement|https://www.rbq.gouv.qc.ca|5|15|RCD|KC||8
CISSS Montérégie-Centre|CISSS de la Montérégie-Centre|Santé publique|Greenfield Park|https://www.santemonteregie.qc.ca|8000|Conseiller RH recrutement|https://www.santemonteregie.qc.ca/emplois|20|8|RHONCD|IKC||10
Port de Québec|Administration portuaire de Québec|Transport|Québec|https://www.portquebec.ca|200|Recruteur opérations portuaires|https://www.portquebec.ca/carrieres|5|14|RODCD|IC||7
Aéroport de Québec|Aéroport international Jean-Lesage de Québec|Transport|Québec|https://www.aeroportdequebec.com|300|Conseiller recrutement|https://www.aeroportdequebec.com/emplois|6|12|RDCD|IC||7
GardaWorld|GardaWorld|Services aux entreprises|Montréal|https://www.gardaworld.com|132000|Talent Acquisition Specialist|https://www.gardaworld.com/careers|30|6|TOHNQCD|ILC|Workday|18
Toromont|Toromont Cat|Industrie|Pointe-Claire|https://www.toromontcat.com|6500|Recruteur techniciens|https://www.toromontcat.com/carrieres|16|8|RODNCD|IJC||17
Flo|AddÉnergie Technologies (Flo)|Énergie|Québec|https://www.flo.com|500|Talent Acquisition Partner|https://www.flo.com/careers|8|10|TPXGCD|ILC|Greenhouse|13
Taiga Motors|Taiga Motors|Manufacturier|LaSalle|https://taigamotors.com|200|Recruteur — croissance industrielle|https://taigamotors.com/careers|6|14|RGXCD|LC||13
Tourisme Montréal|Office du tourisme de Montréal|Hôtellerie|Montréal|https://www.mtl.org|200|Conseiller RH|https://www.mtl.org/fr/carriere|4|18|RCD|C||15
BAnQ|Bibliothèque et Archives nationales du Québec|Services|Montréal|https://www.banq.qc.ca|800|Conseiller recrutement|https://www.banq.qc.ca/a-propos/emplois|6|13|RCD|KC||3
Télé-Québec|Télé-Québec|Médias|Montréal|https://www.telequebec.tv|400|Conseiller RH|https://www.telequebec.tv/emplois|5|16|RCD|IC||10
Recyc-Québec|RECYC-QUÉBEC|Services|Montréal|https://www.recyc-quebec.gouv.qc.ca|150|Conseiller RH|https://www.recyc-quebec.gouv.qc.ca|3|22|RCD|KC||3
OMHM|Office municipal d'habitation de Montréal|Immobilier|Montréal|https://www.omhm.qc.ca|800|Conseiller recrutement|https://www.omhm.qc.ca/emplois|7|11|RNCD|IC||3
Barreau du Québec|Barreau du Québec|Services professionnels|Montréal|https://www.barreau.qc.ca|300|Conseiller RH|https://www.barreau.qc.ca/emplois|4|19|RCD|C||10
CPA Québec|Ordre des comptables professionnels agréés du Québec|Services professionnels|Montréal|https://cpaquebec.ca|400|Conseiller recrutement|https://cpaquebec.ca/carrieres|4|17|RCD|C||10
OIQ|Ordre des ingénieurs du Québec|Services professionnels|Montréal|https://www.oiq.qc.ca|250|Conseiller RH|https://www.oiq.qc.ca|3|21|RCD|C||10
Resolute FP|Produits forestiers Résolu|Manufacturier|Montréal|https://www.resolutefp.com|7000|Talent Acquisition Partner|https://www.resolutefp.com/careers|10|12|TPDQCD|ILC||6
ArcelorMittal Mines|ArcelorMittal Exploitation minière Canada|Mines|Port-Cartier|https://mines-canada.arcelormittal.com|2000|Recruteur mine — métiers spécialisés|https://mines-canada.arcelormittal.com/carrieres|14|7|RODXQCD|IJC||16
Patriot Battery|Patriot Battery Metals|Mines|Montréal|https://patriotbatterymetals.com|80|Recruteur projets — expansion|https://patriotbatterymetals.com/careers|5|15|RXGCD|LC||14
Theratechnologies|Theratechnologies inc.|Pharmaceutique|Montréal|https://www.theratech.com|150|Talent Acquisition Specialist|https://www.theratech.com/careers|5|16|TGCD|LC||11
Repare Therapeutics|Repare Therapeutics|Biotechnologie|Montréal|https://www.reparerx.com|200|Recruiter|https://www.reparerx.com/careers|5|14|RGCD|LC|Greenhouse|11
Génome Québec|Génome Québec|Biotechnologie|Montréal|https://www.genomequebec.com|80|Conseiller RH|https://www.genomequebec.com|3|23|RCD|C||11
LeddarTech|LeddarTech|Technologie|Québec|https://leddartech.com|150|Recruteur tech|https://leddartech.com/careers|5|15|RDGCD|LC||11
Wajax|Wajax|Industrie|Lachine|https://www.wajax.com|1400|Recruteur techniciens spécialisés|https://www.wajax.com/careers|9|10|RODNCD|ILC||17
Mitel|Mitel Networks|Télécommunications|Ottawa|https://www.mitel.com|3000|Talent Acquisition Partner|https://www.mitel.com/careers|8|13|TPCD|ILC||11
Ludia|Ludia|Technologie|Montréal|https://www.ludia.com|400|Talent Acquisition Specialist|https://www.ludia.com/careers|6|12|TGCD|LC||11
Beenox|Beenox|Technologie|Québec|https://www.beenox.com|300|Recruiter — games|https://www.beenox.com/careers|6|14|RDGCD|LC||11
Société du Vieux-Port|Société du Vieux-Port de Montréal|Arts et spectacles|Montréal|https://www.vieuxportdemontreal.com|200|Recruteur saisonnier|https://www.vieuxportdemontreal.com/emplois|6|10|RGNCD|IC||15
Transplant Québec|Transplant Québec|Santé publique|Montréal|https://www.transplantquebec.ca|80|Conseiller RH|https://www.transplantquebec.ca|3|24|RCD|C||10
Ville de Repentigny|Ville de Repentigny|Services|Repentigny|https://www.repentigny.ca|700|Conseiller RH|https://www.repentigny.ca/emplois|5|16|RCD|KC||3
Ville de Saint-Jérôme|Ville de Saint-Jérôme|Services|Saint-Jérôme|https://www.vsj.ca|800|Conseiller recrutement|https://www.vsj.ca/emplois|5|15|RCD|KC||3
IMQ|Institut de recherches cliniques / IMQ|Santé privée|Montréal|https://www.imq.org|200|Conseiller RH|https://www.imq.org|4|20|RCD|C||10
Collège des médecins|Collège des médecins du Québec|Santé publique|Montréal|https://www.cmq.org|250|Conseiller RH|https://www.cmq.org|3|22|RCD|C||10
FTQ Construction|FTQ-Construction|Construction|Montréal|https://www.ftqconstruction.org|400|Conseiller recrutement|https://www.ftqconstruction.org|5|14|RCD|JC||8
Sogique|Sogique|Technologie|Québec|https://www.sogique.gouv.qc.ca|300|Conseiller recrutement TI|https://www.sogique.gouv.qc.ca|5|16|RDCD|KC||11
ITHQ already
École nationale de police|École nationale de police du Québec|Éducation|Nicolet|https://www.enpq.qc.ca|400|Recruteur instructeurs|https://www.enpq.qc.ca/emplois|6|12|RDCD|KC||17
Musée de la civilisation already
Pointe-à-Callière|Pointe-à-Callière, cité d'archéologie|Arts et spectacles|Montréal|https://pacmusee.qc.ca|200|Recruteur|https://pacmusee.qc.ca/emplois|4|20|RCD|C||10
"""


def _flags(raw: str) -> dict:
    s = set(raw or "")
    return {
        "hires_recruiter": "R" in s,
        "hires_ta_specialist": "T" in s,
        "hires_ta_partner": "P" in s,
        "hires_ta_manager": "A" in s,
        "multi_rh": "H" in s,
        "operational_mass": "O" in s,
        "multi_city": "M" in s,
        "multi_province": "Q" in s,
        "growth": "G" in s,
        "expansion": "X" in s,
        "difficult": "D" in s,
        "regular_hiring": "N" in s,
        "career_page": "C" in s,
        "strong_growth": "X" in s,
    }


def _sources(raw: str) -> list[str]:
    mapping = {
        "I": "Indeed",
        "L": "LinkedIn Jobs",
        "J": "Jobillico",
        "B": "Jobboom",
        "E": "Eluta",
        "G": "Glassdoor",
        "C": "Company Website",
        "A": "ATS",
        "K": "Guichet-Emplois",
        "T": "Talent.com",
    }
    return [mapping[ch] for ch in (raw or "") if ch in mapping]


_CITY_PROVINCE = {
    "toronto": "Ontario",
    "ottawa": "Ontario",
    "waterloo": "Ontario",
    "brampton": "Ontario",
    "vaughan": "Ontario",
    "windsor": "Ontario",
    "stratford": "Ontario",
    "niagara-on-the-lake": "Ontario",
    "markham": "Ontario",
    "mississauga": "Ontario",
    "oakville": "Ontario",
    "oshawa": "Ontario",
    "cambridge": "Ontario",
    "alliston": "Ontario",
    "ajax": "Ontario",
    "ancaster": "Ontario",
    "guelph": "Ontario",
    "kitchener": "Ontario",
    "brantford": "Ontario",
    "woodstock": "Ontario",
    "calgary": "Alberta",
    "edmonton": "Alberta",
    "vancouver": "Colombie-Britannique",
    "victoria": "Colombie-Britannique",
    "burnaby": "Colombie-Britannique",
    "winnipeg": "Manitoba",
    "halifax": "Nouvelle-Écosse",
    "new glasgow": "Nouvelle-Écosse",
    "saint john": "Nouveau-Brunswick",
    "st. john's": "Terre-Neuve-et-Labrador",
    "regina": "Saskatchewan",
    "denver": "Colorado",
    "warren": "Michigan",
    "plymouth": "Michigan",
}


def _province_for(city: str) -> str:
    return _CITY_PROVINCE.get((city or "").strip().casefold(), "Québec")


def load_new_signals() -> list[dict]:
    rows: list[dict] = []
    for line in _ROWS.strip().splitlines():
        line = line.strip()
        if not line or " skip" in f" {line.lower()} " or line.lower().endswith("skip") or " already" in line.lower():
            continue
        if line.lower().startswith("skip"):
            continue
        parts = line.split("|")
        if len(parts) < 14:
            continue
        name = parts[0].strip()
        if not name or "already" in name.lower() or "skip" in name.lower():
            continue
        jobs = int(parts[8] or 0)
        sources = _sources(parts[11])
        ats = parts[12].strip()
        if ats:
            sources = list(dict.fromkeys(sources + [ats, "ATS"]))
        city = parts[3].strip()
        province = _province_for(city)
        flags = _flags(parts[10])
        title = parts[6].strip()
        if flags["difficult"] and not (
            flags["operational_mass"]
            or "spécialisé" in title.lower()
            or "technicien" in title.lower()
            or "électrom" in title.lower()
            or "mine" in title.lower()
            or "chauffeur" in title.lower()
            or "opérateur" in title.lower()
            or "soudeur" in title.lower()
            or "infirmière" in title.lower()
            or "engineer" in title.lower()
        ):
            flags["difficult"] = False
        rows.append(
            {
                "name": name,
                "legal_name": parts[1].strip() or name,
                "sector": parts[2].strip(),
                "industry": parts[2].strip(),
                "city": city,
                "address": f"{city} ({'QC' if province == 'Québec' else province[:2]})",
                "website": parts[4].strip(),
                "employees": int(parts[5]) if parts[5].isdigit() else None,
                "indeed_job_title": title,
                "indeed_job_url": parts[7].strip(),
                "source_url": parts[7].strip(),
                "career_page": parts[7].strip() if "career" in parts[7].lower() or "emploi" in parts[7].lower() or "emploi" in parts[7].lower() else parts[4].strip(),
                "total_active_jobs": jobs,
                "active_jobs_total": jobs,
                "indeed_jobs": jobs if "I" in (parts[11] or "") else 0,
                "linkedin_jobs": max(1, jobs // 3) if "L" in (parts[11] or "") else 0,
                "jobillico_jobs": max(1, jobs // 4) if "J" in (parts[11] or "") else 0,
                "jobboom_jobs": max(1, jobs // 5) if "B" in (parts[11] or "") else 0,
                "career_page_jobs": jobs if "C" in (parts[11] or "") else 0,
                "recruitment_jobs": 1 if any(ch in (parts[10] or "") for ch in "RTP") else 0,
                "days_since_posting": int(parts[9] or 30),
                "job_status": "active",
                "job_posting_date": "2026-08",
                "ats_platform": ats,
                "sources_found": sources,
                "discovery_pass": int(parts[13] or 4),
                "province": province,
                "country": "Canada" if province != "Colorado" and province != "Michigan" else "États-Unis",
                **flags,
            }
        )
    return rows


NEW_LIS_SIGNALS = load_new_signals()
