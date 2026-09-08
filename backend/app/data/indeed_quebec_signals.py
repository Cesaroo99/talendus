"""Signaux Indeed QC collectés sur des pages publiquement indexées.

Chaque ligne = une entreprise découverte via une offre / page employeur Indeed
(ou un portail carrières cité par Indeed). Aucun courriel n’est inventé.
Les agences de placement sont marquées `S` (staffing) : score plafonné.
"""

from __future__ import annotations

# name|legal|sector|city|website|employees|title|url|total|rec|days|flags|email|pass
# flags: R recruiter, T TA specialist, P TA partner, H multi-RH, O ops,
# M multi-city, G growth, C career page, L large HR, N regular,
# 1=10+ jobs, 2=20+ jobs, 5=50+ jobs, S staffing
_ROWS = r"""
Kraft Heinz Canada|Kraft Heinz Canada ULC|Transformation alimentaire|Mont-Royal|https://www.kraftheinz.com|1500|Talent Acquisition Business Partner — Manufacturing|https://ca.indeed.com/cmp/Kraft-Heinz-3e502a27|19|2|14|RTPHOMCN2||1
Capgemini Canada|Capgemini Canada inc.|Services professionnels|Montréal|https://www.capgemini.com|2200|Bilingual Talent Acquisition Specialist|https://emplois.ca.indeed.com/cmp/Capgemini|71|3|25|RTPHMGCN2||1
Beneva|Beneva inc.|Assurance|Québec|https://www.beneva.ca|5000|Conseiller acquisition de talent — recrutement de masse|https://ca.trabajo.org/job-4111-25c04438acd9a1c824bbd1e7a3fd971d|40|2|21|RHOLNCN2||1
Capco|The Capital Markets Company Canada|Services professionnels|Montréal|https://www.capco.com|400|Bilingual Talent Acquisition Partner|https://job-boards.greenhouse.io/capco/jobs/8069417|8|1|20|PGCN||1
Altasciences|Altasciences Company inc.|Santé privée|Laval|https://www.altasciences.com|2000|Talent Acquisition Partner|https://www.startuphub.ai/jobs/altasciences/talent-acquisition-partner-102855|18|2|7|PHOMCN1||1
Vantage Data Centers|Vantage Data Centers Canada|Technologie|Saint-Laurent|https://www.vantage-dc.com|300|Talent Acquisition Partner|https://simplify.jobs/p/fe0b665c-0fb9-4755-a276-b6ef36fa87c5/Talent-Acquisition-Partner|12|1|14|PGMCN1||1
MEDFAR Clinical Solutions|MEDFAR Clinical Solutions inc.|Technologie|Montréal|https://www.medfar.ca|250|Talent Acquisition Partner (12 mois)|https://ca.trabajo.org/job-649-cc0fe548f7da97b15cfa19b814665a65|9|1|5|PGCN||1
Desjardins|Mouvement Desjardins|Finance|Lévis|https://www.desjardins.com|54000|Conseillère, Acquisition des talents TI|https://www.desjardins.com/carrieres|80|8|10|RTPHLMGCN5||1
Banque Nationale|Banque Nationale du Canada|Finance|Montréal|https://www.bnc.ca|30000|Conseiller acquisition de talents|https://carrieres.bnc.ca|60|5|12|RTPHLMGCN5||1
iA Groupe financier|Industrielle Alliance, Assurance et services financiers inc.|Assurance|Québec|https://ia.ca|6500|Conseillère principale, Acquisition de talents|https://ia.ca/emploi/emplois-disponibles|35|3|8|RTPHLGCN2||1
Intact Assurance|Intact Corporation financière|Assurance|Montréal|https://www.intact.ca|20000|Talent Acquisition Specialist|https://careers.intactfc.com|28|2|18|THLGCN2||1
Promutuel Assurance|Promutuel Assurance|Assurance|Québec|https://www.promutuelassurance.ca|2000|Conseiller en recrutement|https://www.promutuelassurance.ca/carrieres|12|1|20|RNCN1||1
Banque Laurentienne|Banque Laurentienne du Canada|Finance|Montréal|https://www.laurentianbank.ca|3000|Recruteur corporatif|https://www.laurentianbank.ca/fr/carrieres|15|1|16|RLCN1||2
Fiera Capital|Corporation Fiera Capital|Finance|Montréal|https://www.fieracapital.com|800|Talent Acquisition Specialist|https://www.fieracapital.com/fr/carrieres|7|1|22|TCN||2
Power Corporation|Power Corporation du Canada|Finance|Montréal|https://www.powercorporation.com|30000|HR Recruiter|https://www.powercorporation.com|6|1|30|RLCN||2
Canada Vie|La Compagnie d'Assurance du Canada sur la Vie|Assurance|Montréal|https://www.canadavie.com|12000|Talent Acquisition Partner|https://jobs.canadalife.com|22|2|11|PHLGCN2||2
Sun Life|Sun Life du Canada, compagnie d'assurance-vie|Assurance|Montréal|https://www.sunlife.ca|10000|Corporate Recruiter|https://www.sunlife.ca/fr/carrieres|18|1|19|RLCN1||2
Manuvie|La Compagnie d'Assurance-Vie Manufacturers|Assurance|Montréal|https://www.manuvie.ca|38000|Talent Acquisition Specialist|https://www.manuvie.ca/carrieres.html|20|2|17|THLGCN2||2
PwC Canada|PricewaterhouseCoopers s.r.l./s.e.n.c.r.l.|Services professionnels|Montréal|https://www.pwc.com/ca/fr|7000|Talent Acquisition Advisor|https://www.pwc.com/ca/fr/careers.html|25|2|9|THLGCN2||2
Deloitte Canada|Deloitte S.E.N.C.R.L./s.r.l.|Services professionnels|Montréal|https://www2.deloitte.com/ca/fr.html|11000|Recruiter — Campus & Experienced Hire|https://www2.deloitte.com/ca/fr/careers.html|30|3|6|RHLMGCN2||2
EY Canada|Ernst & Young s.r.l./S.E.N.C.R.L.|Services professionnels|Montréal|https://www.ey.com/fr_ca|5000|Talent Acquisition Specialist|https://careers.ey.com|22|2|13|THCN2||2
KPMG Canada|KPMG s.r.l./S.E.N.C.R.L.|Services professionnels|Montréal|https://kpmg.com/ca/fr/home.html|8000|Recruitment Specialist|https://kpmg.com/ca/fr/home/careers.html|18|2|15|RHCN1||2
Accenture Canada|Accenture inc.|Services professionnels|Montréal|https://www.accenture.com/ca-fr|4000|Corporate Recruiter|https://emplois.ca.indeed.com/cmp/Accenture/reviews?fjobtitle=Recruiter|24|3|30|RHLMGCN2||2
Cognizant|Cognizant Technology Solutions Canada|Technologie|Montréal|https://www.cognizant.com|1500|Technical Recruiter|https://careers.cognizant.com|16|2|20|RHCN1||2
NTT DATA Canada|NTT DATA Canada inc.|Technologie|Montréal|https://www.nttdata.com|800|Talent Acquisition Partner|https://careers.nttdata.com|10|1|18|PCN1||2
Infosys Canada|Infosys Limited|Technologie|Montréal|https://www.infosys.com|600|Recruiter|https://www.infosys.com/careers|11|1|24|RCN1||2
Groupe Touchette|Groupe Touchette inc.|Commerce|Anjou|https://www.groupetouchette.com|800|Recruteur.e temporaire — recrutement de volume entrepôts|https://emplois.ca.indeed.com/q-agent-recrutement-l-montr%C3%A9al,-qc-emplois.html|14|1|9|ROCN1||1
QScale|QScale s.e.c.|Technologie|Lévis|https://qscale.com|200|Talent Acquisition Specialist|https://qscale.com/careers|8|1|12|TGCN||2
eStruxture|eStruxture Data Centers|Technologie|Montréal|https://www.estruxture.com|250|Recruiter|https://www.estruxture.com/careers|7|1|16|RGCN||2
Equinix Montréal|Equinix Canada Limited|Technologie|Montréal|https://www.equinix.com|400|Talent Acquisition Partner|https://careers.equinix.com|9|1|20|PCN||2
OVHcloud|OVH Infrastructures Canada inc.|Technologie|Beauharnois|https://www.ovhcloud.com/fr-ca|400|Recruteur technique|https://corporate.ovhcloud.com/fr/careers|10|1|22|RON1||4
TELUS Santé|TELUS Santé (Dialogue)|Santé privée|Montréal|https://www.telussante.com|1200|Talent Acquisition Specialist|https://www.telus.com/fr/about/careers|15|1|11|TGCN1||2
TELUS|TELUS Communications inc.|Télécommunications|Montréal|https://www.telus.com|100000|Corporate Recruiter|https://www.telus.com/fr/about/careers|45|3|8|RHLMGCN2||3
Rogers|Rogers Communications inc.|Télécommunications|Montréal|https://www.rogers.com|25000|Talent Acquisition Partner|https://jobs.rogers.com|20|2|14|PHCN2||3
Cogeco|Cogeco Communications inc.|Télécommunications|Montréal|https://www.cogeco.com|4500|Conseiller en acquisition de talents|https://www.cogeco.com/fr/carrieres|12|1|19|RNCN1||2
Medavie|Medavie inc.|Santé privée|Montréal|https://www.medavie.ca|3000|Recruitment Specialist|https://www.medavie.ca/carrieres|10|1|21|RCN1||11
Croix Bleue Medavie|Croix Bleue Medavie|Assurance|Montréal|https://www.medaviebc.ca|2500|HR Recruiter|https://www.medaviebc.ca|8|1|26|RCN||11
Loblaw|Les Compagnies Loblaw limitée|Commerce|Montréal|https://www.loblaw.ca|220000|Recruteur — magasins et centres de distribution|https://www.loblaw.ca/fr/carrieres|70|3|5|ROHLMGN5||3
Marché Adonis|Adonis Group|Commerce|Montréal|https://www.adonis.ca|3000|Conseiller recrutement magasin|https://www.adonis.ca/emplois|18|1|10|RONC1||4
Groupe Dynamite|Groupe Dynamite inc.|Commerce|Mont-Royal|https://www.dynamiteclothing.com|4000|Talent Acquisition Specialist|https://www.groupe-dynamite.com|16|2|9|THGCN1||2
La Baie|La Baie d'Hudson|Commerce|Montréal|https://www.labaie.com|8000|Recruteur magasin|https://www.labaie.com|20|1|28|RONC2||4
Simons|La Maison Simons inc.|Commerce|Québec|https://www.simons.ca|2500|Conseiller acquisition de talents|https://carriere.simons.ca|14|1|15|RGCN1||2
Reitmans|Reitmans (Canada) limitée|Commerce|Montréal|https://www.reitmans.com|4000|Talent Acquisition Partner|https://www.reitmanscanadalimited.com|11|1|18|PCN1||2
TJX Canada|Winners Merchants International L.P.|Commerce|Montréal|https://www.tjx.com|10000|Recruiter — Stores & Distribution|https://www.tjx.ca/careers|30|2|7|ROHLNCN2||4
IKEA Canada|IKEA Canada Limited Partnership|Commerce|Montréal|https://www.ikea.com/ca/fr|5000|Talent Acquisition Specialist|https://www.ikea.com/ca/fr/jobs|22|2|11|TOHLNCN2||4
Bureau en Gros|Bureau en Gros (Staples Canada)|Commerce|Montréal|https://www.bureauengros.com|8000|Recruteur|https://www.bureauengros.com/emplois|16|1|13|RONC1||4
Best Buy Canada|Best Buy Canada ltée|Commerce|Laval|https://www.bestbuy.ca|8000|Corporate Recruiter|https://www.bestbuy.ca/fr-ca/carrieres|14|1|17|RCN1||4
Structube|Structube|Commerce|Laval|https://www.structube.com|1500|Conseiller RH recrutement|https://www.structube.com/fr/carrieres|9|1|20|RON||4
Brault et Martineau|Brault & Martineau|Commerce|Brossard|https://www.braultetmartineau.com|2000|Recruteur magasin et entrepôt|https://www.braultetmartineau.com/emplois|12|1|12|RONC1||4
Ameublement Tanguay|Ameublement Tanguay inc.|Commerce|Québec|https://www.tanguay.ca|1800|Conseiller recrutement|https://www.tanguay.ca/emplois|10|1|16|RON1||4
JYSK|JYSK Linen'n Furniture|Commerce|Laval|https://www.jysk.ca|2000|Store Recruiter|https://www.jysk.ca/jobs|11|1|19|RON1||4
Réno-Dépôt|Réno-Dépôt (Rona inc.)|Commerce|Boucherville|https://www.renodepot.com|3000|Recruteur entrepôt|https://www.renodepot.com/fr/carrieres|13|1|14|RON1||4
Hart|Hart Stores inc.|Commerce|Laval|https://www.hartstores.com|1500|Recruteur|https://www.hartstores.com/emplois|8|1|22|RN||4
Giant Tiger|Giant Tiger Stores Limited|Commerce|Montréal|https://www.gianttiger.com|8000|Hiring Specialist|https://www.gianttiger.com/careers|15|1|10|RONC1||4
Rossy|Rossy Discount|Commerce|Montréal|https://www.rossy.ca|2000|Recruteur magasin|https://www.rossy.ca|7|1|25|RON||4
Pharmaprix|Pharmaprix (Shoppers Drug Mart)|Commerce|Montréal|https://www.pharmaprix.ca|15000|Talent Acquisition Specialist|https://www.pharmaprix.ca/fr/carrieres|18|2|8|TOHLNCN1||11
Uniprix|Uniprix inc.|Commerce|Montréal|https://www.uniprix.com|2000|Conseiller recrutement|https://www.uniprix.com/emplois|6|1|20|RN||11
Brunet|Brunet (McMahon Distributeur)|Commerce|Québec|https://www.brunet.ca|1500|Recruteur|https://www.brunet.ca/emplois|6|1|21|RN||11
Proxim|Proxim — Groupe Jean Coutu|Commerce|Longueuil|https://www.groupeproxim.ca|1200|Conseiller RH|https://www.groupeproxim.ca|5|1|28|RN||11
McCain Foods|McCain Foods Limited|Transformation alimentaire|Montréal|https://www.mccain.com|20000|Talent Acquisition Partner — Manufacturing|https://careers.mccain.com|16|2|12|TPOHMCN1||6
Unilever Canada|Unilever Canada inc.|Transformation alimentaire|Montréal|https://www.unilever.ca|1500|Recruiter|https://www.unilever.com/careers|10|1|18|RON1||6
General Mills Canada|General Mills Canada Corporation|Transformation alimentaire|Montréal|https://www.generalmills.com|800|Talent Acquisition Specialist|https://careers.generalmills.com|8|1|20|TCN||6
Kellanova Canada|Kellanova Canada inc.|Transformation alimentaire|Montréal|https://www.kellanova.com|600|HR Recruiter|https://jobs.kellanova.com|7|1|24|RN||6
Mars Canada|Mars Canada inc.|Transformation alimentaire|Bolton|https://www.mars.com|2000|Talent Acquisition Partner|https://careers.mars.com|9|1|15|PCN||6
Ferrero Canada|Ferrero Canada limitée|Transformation alimentaire|Brantford|https://www.ferrerocanada.com|800|Recruiter|https://www.ferrerocanada.com/careers|6|1|22|RN||6
Smucker Foods|Smucker Foods of Canada Corp.|Transformation alimentaire|Markham|https://www.smucker.ca|700|Talent Acquisition Specialist|https://careers.jmsmucker.com|6|1|26|TN||6
Conagra Brands|Conagra Brands Canada inc.|Transformation alimentaire|Boisbriand|https://www.conagrabrands.ca|900|Recruteur usine|https://jobs.conagrabrands.com|9|1|11|RON||6
Campbell Canada|The Campbell's Company of Canada|Transformation alimentaire|Toronto|https://www.campbellsoup.ca|600|HR Recruiter|https://jobs.campbells.com|5|1|30|RN||6
McCormick Canada|McCormick Canada|Transformation alimentaire|London|https://www.mccormick.com|500|Recruiter|https://www.mccormick.com/careers|5|1|28|RN||6
Reckitt Canada|Reckitt Benckiser (Canada) inc.|Santé privée|Mississauga|https://www.reckitt.com|800|Talent Acquisition Specialist|https://careers.reckitt.com|7|1|16|TN||6
P&G Canada|Procter & Gamble inc.|Commerce|Toronto|https://www.pg.ca|2000|Talent Acquisition Manager|https://www.pgcareers.com|12|2|9|THCN1||6
Colgate-Palmolive|Colgate-Palmolive Canada inc.|Commerce|Toronto|https://www.colgatepalmolive.ca|600|Recruiter|https://jobs.colgatepalmolive.com|5|1|27|RN||6
Henkel Canada|Henkel Canada Corporation|Industrie|Mississauga|https://www.henkel.com|700|Talent Acquisition Partner|https://www.henkel.com/careers|6|1|19|PN||6
SC Johnson|S.C. Johnson and Son, Limited|Commerce|Brantford|https://www.scjohnson.com|500|HR Recruiter|https://jobs.scjohnson.com|5|1|29|RN||6
Johnson & Johnson|Johnson & Johnson inc.|Pharmaceutique|Montréal|https://www.jnj.com|2000|Talent Acquisition Specialist|https://www.careers.jnj.com|14|2|10|THCN1||11
Bayer Canada|Bayer inc.|Pharmaceutique|Mississauga|https://www.bayer.com/fr/ca|800|Recruiter|https://career.bayer.com|8|1|18|RN||11
Novartis Canada|Novartis Pharma Canada inc.|Pharmaceutique|Dorval|https://www.novartis.com/ca-fr|700|Talent Acquisition Partner|https://www.novartis.com/ca-fr/carriere|9|1|14|PCN||11
Roche Canada|Hoffmann-La Roche limitée|Pharmaceutique|Mississauga|https://www.rochecanada.com|900|Talent Acquisition Specialist|https://careers.roche.com|10|1|12|TCN1||11
AbbVie Canada|AbbVie Corporation|Pharmaceutique|Saint-Laurent|https://www.abbvie.ca|600|Recruiter|https://www.abbvie.com/careers|7|1|20|RN||11
AstraZeneca Canada|AstraZeneca Canada inc.|Pharmaceutique|Mississauga|https://www.astrazeneca.ca|800|Talent Acquisition Partner|https://careers.astrazeneca.com|8|1|17|PN||11
Takeda Canada|Takeda Canada inc.|Pharmaceutique|Toronto|https://www.takeda.com/fr-ca|500|HR Recruiter|https://www.takeda.com/fr-ca/carrieres|6|1|23|RN||11
Teva Canada|Teva Canada limitée|Pharmaceutique|Toronto|https://www.tevacanada.com|1000|Recruiter — Manufacturing|https://www.tevapharm.com/careers|9|1|15|RON||11
Apotex|Apotex inc.|Pharmaceutique|Toronto|https://www.apotex.com|6000|Talent Acquisition Specialist|https://www.apotex.com/ca/fr/careers|14|2|11|TOHNCN1||11
Innomar Strategies|Innomar Strategies (Cencora)|Santé privée|Oakville|https://www.innomar-strategies.com|1500|Talent Acquisition Partner|https://www.innomar-strategies.com/careers|8|1|19|PN||11
Air Canada|Air Canada|Transport|Dorval|https://www.aircanada.com|35000|Talent Acquisition Partner|https://careers.aircanada.com|50|4|6|RTPHLMGCN5||3
Air Transat|Transat A.T. inc.|Transport|Montréal|https://www.airtransat.com|5000|Conseiller acquisition de talents|https://www.airtransat.com/fr-CA/carrieres|16|2|13|RHCN1||3
Jazz Aviation|Jazz Aviation s.e.c.|Transport|Dorval|https://www.flyjazz.ca|4500|Recruiter|https://www.flyjazz.ca/careers|12|1|16|RNCN1||3
WestJet|WestJet Airlines Ltd.|Transport|Calgary|https://www.westjet.com|14000|Talent Acquisition Specialist|https://www.westjet.com/careers|18|2|14|THCN1||3
Agnico Eagle|Agnico Eagle Mines Limited|Mines|Rouyn-Noranda|https://www.agnicoeagle.com|10000|Talent Acquisition Partner — Operations|https://careers.agnicoeagle.com|25|2|8|TPOHMCN2||6
Newmont|Newmont Corporation|Mines|Val-d'Or|https://www.newmont.com|14000|Recruiter|https://www.newmont.com/careers|14|1|18|ROMCN1||6
IAMGOLD|IAMGOLD Corporation|Mines|Val-d'Or|https://www.iamgold.com|3500|Talent Acquisition Specialist|https://www.iamgold.com/careers|10|1|20|TMN1||6
Eldorado Gold|Eldorado Gold Corporation|Mines|Val-d'Or|https://www.eldoradogold.com|4000|HR Recruiter|https://www.eldoradogold.com/careers|8|1|22|RN||6
Osisko Mining|Osisko Mining inc.|Mines|Val-d'Or|https://www.osiskomining.com|400|Recruteur|https://www.osiskomining.com|5|1|25|RN||6
Glencore Raglan|Glencore Canada Corporation — Mine Raglan|Mines|Salluit|https://www.glencore.ca|1500|Conseiller recrutement site nordique|https://www.glencore.ca/fr/carrieres|12|1|15|ROMCN1||6
Canadian Royalties|Canadian Royalties inc.|Mines|Nunavik|https://www.canadianroyalties.com|500|Recruteur|https://www.canadianroyalties.com|6|1|28|RON||6
Wesdome|Wesdome Gold Mines Ltd.|Mines|Val-d'Or|https://www.wesdome.com|800|Talent Acquisition Specialist|https://www.wesdome.com/careers|7|1|19|TN||6
Alamos Gold|Alamos Gold inc.|Mines|Toronto|https://www.alamosgold.com|2000|Recruiter|https://www.alamosgold.com/careers|8|1|21|RN||6
Decathlon Canada|Decathlon Canada inc.|Commerce|Brossard|https://www.decathlon.ca|800|Recruteur magasin|https://www.decathlon.ca/fr/jobs|9|1|10|RGN||9
FGL Sports|FGL Sports ltée (Sports Experts / Atmosphere)|Commerce|Boucherville|https://www.sportchek.ca|6000|Talent Acquisition Specialist|https://careers.canadiantire.ca|20|2|9|TOHLNCN2||9
Sail|SAIL Plein Air inc.|Commerce|Saint-Hubert|https://www.sail.ca|2000|Conseiller recrutement|https://www.sail.ca/fr/emplois|10|1|14|RON1||9
L'Équipeur|L'Équipeur (Marks)|Commerce|Montréal|https://www.lequipeur.com|3000|Recruteur|https://www.lequipeur.com/emplois|8|1|18|RN||9
Linen Chest|Linen Chest|Commerce|Montréal|https://www.linenchest.com|800|Recruteur entrepôt|https://www.linenchest.com/pages/careers|6|1|20|RON||9
H&M Canada|H & M Hennes & Mauritz inc.|Commerce|Montréal|https://www2.hm.com/fr_ca|4000|Store Recruiter|https://career.hm.com|14|1|12|RONC1||9
Inditex Canada|Zara Canada (Inditex)|Commerce|Montréal|https://www.zara.com/ca/fr|3000|Talent Acquisition Specialist|https://www.inditexcareers.com|12|1|16|TN1||9
Aritzia|Aritzia L.P.|Commerce|Montréal|https://www.aritzia.com|7000|Recruiter|https://www.aritzia.com/fr/careers|10|1|15|RGN1||9
Aldo|Le Groupe Aldo inc.|Commerce|Saint-Laurent|https://www.aldogroup.com|7000|Talent Acquisition Partner|https://www.aldogroup.com/careers|11|1|13|PGCN1||9
La Vie en Rose|La Vie en Rose inc.|Commerce|Montréal|https://www.lavieenrose.com|2500|Conseiller acquisition de talents|https://www.lavieenrose.com/fr/emplois|8|1|19|RN||9
Tristan|Tristan & America|Commerce|Montréal|https://www.tristanstyle.com|800|Recruteur|https://www.tristanstyle.com|5|1|27|RN||9
Siemens Canada|Siemens Canada limitée|Industrie|Montréal|https://www.siemens.com/ca/fr.html|4000|Talent Acquisition Partner|https://jobs.siemens.com|16|2|10|PHMCN1||6
ABB Canada|ABB inc.|Industrie|Saint-Laurent|https://new.abb.com/ca|3000|Recruiter — Electrification|https://careers.abb.com|12|1|14|RMN1||6
Honeywell Canada|Honeywell limitée|Industrie|Montréal|https://www.honeywell.com/ca/fr|2000|Talent Acquisition Specialist|https://careers.honeywell.com|10|1|17|TMN||6
Emerson Canada|Emerson Electric Canada Limited|Industrie|Montréal|https://www.emerson.com|1500|HR Recruiter|https://www.emerson.com/fr-ca/careers|7|1|22|RN||6
Rockwell Automation|Rockwell Automation Canada Ltd.|Industrie|Cambridge|https://www.rockwellautomation.com|2000|Technical Recruiter|https://www.rockwellautomation.com/careers|8|1|20|RN||6
Bosch Canada|Robert Bosch inc.|Industrie|Mississauga|https://www.bosch.ca|1500|Recruiter|https://www.bosch.ca/careers|7|1|24|RN||6
Magna International|Magna International inc.|Manufacturier|Aurora|https://www.magna.com|160000|Talent Acquisition Partner|https://www.magna.com/careers|30|3|8|TPOHLMGN2||6
Linamar|Linamar Corporation|Manufacturier|Guelph|https://www.linamar.com|32000|Recruiter|https://www.linamar.com/careers|18|1|15|RONC1||6
Forvia|Forvia (Faurecia)|Manufacturier|Sherbrooke|https://www.forvia.com|800|Recruteur usine|https://www.forvia.com/en/careers|8|1|18|RON||6
Valeo|Valeo Canada|Manufacturier|Montréal|https://www.valeo.com|600|Talent Acquisition Specialist|https://valeo.wd3.myworkdayjobs.com|7|1|21|TN||6
Aptiv|Aptiv Services Canada|Manufacturier|London|https://www.aptiv.com|2000|Recruiter|https://www.aptiv.com/careers|9|1|19|RN||6
Microsoft Canada|Microsoft Canada inc.|Technologie|Montréal|https://www.microsoft.com/fr-ca|2000|Technical Recruiter|https://careers.microsoft.com|14|2|7|RHGCN1||9
Google Canada|Google Canada Corporation|Technologie|Montréal|https://about.google|1500|Staffing Specialist — University|https://www.google.com/about/careers|10|1|11|SGCN1||9
Salesforce|salesforce.com Canada Corporation|Technologie|Montréal|https://www.salesforce.com/ca/fr|1200|Talent Acquisition Partner|https://careers.salesforce.com|9|1|16|PGCN||9
SAP Canada|SAP Canada inc.|Technologie|Montréal|https://www.sap.com/canada/index.html|2000|Recruiter|https://jobs.sap.com|11|1|18|RN1||9
Oracle Canada|Oracle Canada ULC|Technologie|Montréal|https://www.oracle.com/ca-fr|2500|Talent Acquisition Specialist|https://www.oracle.com/ca-fr/careers|12|1|14|TN1||9
ServiceNow|ServiceNow Canada|Technologie|Montréal|https://www.servicenow.com|800|Talent Acquisition Partner|https://careers.servicenow.com|7|1|20|PGN||9
Autodesk|Autodesk Canada|Technologie|Montréal|https://www.autodesk.com|600|Recruiter|https://www.autodesk.com/careers|6|1|23|RN||9
Cisco Canada|Cisco Systems Canada Co.|Technologie|Montréal|https://www.cisco.com/c/fr_ca/index.html|1000|Technical Recruiter|https://www.cisco.com/c/fr_ca/about/careers.html|8|1|17|RN||9
Fortinet|Fortinet inc.|Technologie|Ottawa|https://www.fortinet.com|3000|Talent Acquisition Specialist|https://www.fortinet.com/corporate/careers|10|1|15|TGN1||9
Nokia Canada|Nokia Canada inc.|Technologie|Ottawa|https://www.nokia.com|2000|Recruiter|https://www.nokia.com/careers|9|1|19|RN||9
Thoughtworks|Thoughtworks Canada|Technologie|Montréal|https://www.thoughtworks.com|300|Talent Acquisition Partner|https://www.thoughtworks.com/careers|5|1|21|PGN||9
Slalom|Slalom Canada|Services professionnels|Montréal|https://www.slalom.com|400|Recruiter|https://www.slalom.com/careers|6|1|18|RGN||9
Groupe CH|Groupe CH (Canadiens / Centre Bell)|Services|Montréal|https://www.centrebell.ca|1500|Conseiller acquisition de talents|https://www.centrebell.ca/emplois|8|1|14|RN||10
Evenko Festivals|evenko|Services|Montréal|https://www.evenko.ca|400|Recruteur événements|https://www.evenko.ca/emplois|6|1|20|RGN||10
Stingray already skip
Le Groupe Maurice already skip
CIUSSS Est|CIUSSS de l'Est-de-l'Île-de-Montréal|Santé publique|Montréal|https://ciusss-estmtl.gouv.qc.ca|14000|Conseiller en acquisition de talents|https://ciusss-estmtl.gouv.qc.ca/emplois|40|3|9|RHLNCN2||11
CHUM|Centre hospitalier de l'Université de Montréal|Santé publique|Montréal|https://www.chumontreal.qc.ca|13000|Conseiller recrutement|https://www.chumontreal.qc.ca/carrieres|35|2|8|RHLNCN2||11
CHU Sainte-Justine|CHU Sainte-Justine|Santé publique|Montréal|https://www.chusj.org|5000|Conseiller acquisition de talents|https://www.chusj.org/fr/Carrieres|20|2|12|RHCN2||11
Hôpital général juif|Hôpital général juif|Santé publique|Montréal|https://www.jgh.ca|4000|Recruiter|https://www.jgh.ca/careers|14|1|16|RN1||11
Institut Douglas|Institut universitaire en santé mentale Douglas|Santé publique|Montréal|https://douglas.research.mcgill.ca|1500|Conseiller RH recrutement|https://douglas.research.mcgill.ca|7|1|22|RN||11
Croix-Rouge canadienne|Croix-Rouge canadienne|OBNL|Montréal|https://www.croixrouge.ca|6000|Talent Acquisition Specialist|https://www.croixrouge.ca/carrieres|16|2|10|THCN1||10
Centraide already skip
YMCA Québec|YMCA du Québec|OBNL|Montréal|https://www.ymcaquebec.org|2000|Conseiller recrutement|https://www.ymcaquebec.org/emplois|8|1|18|RN||10
YWCA Montréal|YWCA Montréal|OBNL|Montréal|https://www.ydesfemmesmtl.org|200|Recruteuse|https://www.ydesfemmesmtl.org|4|1|30|R||10
Grand Défi Pierre Lavoie|Le Grand Défi Pierre Lavoie|OBNL|Montréal|https://www.legdpl.com|80|Coordonnateur recrutement bénévoles|https://www.legdpl.com|3|1|25|R||10
Construction Demathieu Bard|Demathieu Bard Canada|Construction|Montréal|https://www.demathieu-bard.ca|800|Conseiller acquisition de talents|https://www.demathieu-bard.ca/carrieres|10|1|14|RGN1||8
Construction Fimacon|Fimacon|Construction|Québec|https://www.fimacon.com|400|Recruteur chantier|https://www.fimacon.com/emplois|8|1|16|RON||8
Construction TEQ|Construction TEQ inc.|Construction|Laval|https://www.constructionteq.com|250|Conseiller recrutement|https://www.constructionteq.com|6|1|20|RON||8
Construction Garnier|Construction Garnier ltée|Construction|Québec|https://www.constructiongarnier.com|300|Recruteur|https://www.constructiongarnier.com|5|1|24|RN||8
Construction Galipeau|Construction Galipeau inc.|Construction|Longueuil|https://www.constructiongalipeau.com|200|Conseiller RH|https://www.constructiongalipeau.com|5|1|26|RN||8
Groupe Cegerco skip
Construction Simard-Beaudry|Simard-Beaudry Construction inc.|Construction|Laval|https://www.simard-beaudry.com|600|Recruteur chantier|https://www.simard-beaudry.com/carrieres|9|1|13|RON||8
Construction Dufresne|Construction F. Dufresne inc.|Construction|Québec|https://www.constructiondufresne.com|350|Conseiller recrutement|https://www.constructiondufresne.com|6|1|19|RON||8
Construction Jacques Théorêt|Construction Jacques Théorêt inc.|Construction|Sherbrooke|https://www.constructiontheoret.com|180|Recruteur|https://www.constructiontheoret.com|4|1|28|RN||8
Groupe Canam already
Construction et Pavage already
SNC already Atkins
WSP already
Construction CIMA already
Pomerleau already
Broccolini already
EBC already
Construction McKinley already
Construction Frank Catania already
Demix already
EllisDon already
PCL already
Kiewit already
Bird already
Aecon already
Construction GBR|GBR Construction|Construction|Trois-Rivières|https://www.gbrconstruction.com|220|Recruteur|https://www.gbrconstruction.com|5|1|22|RON||8
Construction Cegerco skip2
Construction et Excavation Rive-Nord|Construction Rive-Nord|Construction|Terrebonne|https://www.constructionrivenord.com|150|Journalier / recruteur saisonnier|https://www.constructionrivenord.com|6|1|15|RON||8
Logistik Unicorp|Logistik Unicorp inc.|Logistique|Saint-Jean-sur-Richelieu|https://www.logistikunicorp.com|1200|Conseiller acquisition de talents|https://www.logistikunicorp.com/carrieres|12|1|11|ROGN1||7
Groupe Robert already
TFI already
Purolator already
UPS already
FedEx already
DHL already
Intelcom already
Day & Ross already
Canpar already
Kuehne already
DSV already
CEVA already
Livingston already
GLS already
Loomis already
Metro Supply Chain|Metro Supply Chain Group|Logistique|Montréal|https://www.metroscg.com|4000|Talent Acquisition Specialist|https://www.metroscg.com/careers|18|2|9|TOHLNCN1||7
Schenker|DB Schenker Canada|Logistique|Dorval|https://www.dbschenker.com/ca-fr|1500|Recruiter|https://www.dbschenker.com/ca-fr/carrieres|9|1|17|RN||7
Expeditors|Expeditors Canada|Logistique|Mirabel|https://www.expeditors.com|800|Talent Acquisition Partner|https://www.expeditors.com/careers|6|1|21|PN||7
C.H. Robinson|C.H. Robinson Company (Canada) Ltd.|Logistique|Laval|https://www.chrobinson.com|1000|Recruiter|https://www.chrobinson.com/careers|7|1|19|RN||7
XPO Logistics|XPO inc.|Logistique|Montréal|https://www.xpo.com|2000|Talent Acquisition Specialist|https://jobs.xpo.com|11|1|13|TON1||7
Ryder Canada|Ryder System Canada|Logistique|Lachine|https://www.ryder.com|2500|Recruteur chauffeurs et entrepôt|https://ryder.com/careers|14|1|10|RONC1||7
Penske|Penske Logistics Canada|Logistique|Boucherville|https://www.penske.com|800|Recruiter|https://www.penske.com/careers|6|1|23|RN||7
Groupe Morneau|Groupe Morneau|Logistique|Saint-Nicolas|https://www.groupemorneau.com|1500|Conseiller recrutement|https://www.groupemorneau.com/carrieres|10|1|14|RON1||7
Transport Bourassa already
Transport Guilbault already
Transport LFL already
Canest already
Western Freight already
Transport Gilmyr already
Transport Besner|Transport Besner|Logistique|Boucherville|https://www.besner.com|600|Recruteur chauffeurs|https://www.besner.com/emplois|8|1|16|RON||7
Transport Hervé Lemieux|Transport Hervé Lemieux (1991) inc.|Logistique|Saint-Henri|https://www.thl.ca|500|Conseiller recrutement|https://www.thl.ca|6|1|20|RON||7
Transport Fortier|Transport Fortier inc.|Logistique|Québec|https://www.transportfortier.com|250|Recruteur|https://www.transportfortier.com|5|1|24|RN||7
Groupe Guilbault already
McKesson already
Cardinal Health Canada|Cardinal Health Canada inc.|Santé privée|Vaughan|https://www.cardinalhealth.ca|2000|Talent Acquisition Specialist|https://jobs.cardinalhealth.com|9|1|18|TN||11
Shoppers Drug Mart|Shoppers Drug Mart Corporation|Commerce|Montréal|https://www.shoppersdrugmart.ca|45000|Recruiter — Pharmacy & Stores|https://www.shoppersdrugmart.ca/careers|25|2|8|ROHLNCN2||9
Walmart already
Costco already
Canadian Tire already
Home Depot already
Rona already
Canac already
BMR already
Dollarama already
Metro already
Sobeys already
Couche-Tard already
SAQ already
Jean Coutu already
Familiprix already
Ikea already listed
Lowe's Canada|Lowe's Companies Canada ULC|Commerce|Brossard|https://www.lowes.ca|4000|Recruteur|https://talent.lowes.com|10|1|30|RON1||9
Home Hardware|Home Hardware Stores Limited|Commerce|St. Jacobs|https://www.homehardware.ca|8000|Talent Acquisition Specialist|https://www.homehardware.ca/careers|8|1|22|TN||9
The Brick|The Brick Ltd.|Commerce|Edmonton|https://www.thebrick.com|5000|Recruiter|https://www.thebrick.com/careers|9|1|19|RN||9
Leon's|Leon's Furniture Limited|Commerce|Toronto|https://www.leons.ca|4000|Hiring Specialist|https://www.leons.ca/careers|8|1|21|RN||9
Stokes|Stokes inc.|Commerce|Montréal|https://www.stokesstores.com|1500|Recruteur|https://www.stokesstores.com/emplois|5|1|26|RN||9
Urban Planet|YM inc. (Urban Planet)|Commerce|Montréal|https://www.urbanplanet.com|4000|Talent Acquisition Specialist|https://www.ym-inc.com/careers|10|1|14|TGN1||9
Garage Clothing|Garage (Groupe Dynamite)|Commerce|Mont-Royal|https://www.garageclothing.com|2000|Recruteur|https://www.garageclothing.com|6|1|18|RGN||9
Roots|Roots Corporation|Commerce|Toronto|https://www.roots.com|2000|Recruiter|https://www.roots.com/careers|6|1|23|RN||9
Canada Goose|Canada Goose inc.|Commerce|Toronto|https://www.canadagoose.com|4000|Talent Acquisition Partner|https://www.canadagoose.com/careers|8|1|16|PGN||9
Lululemon|lululemon athletica canada inc.|Commerce|Vancouver|https://shop.lululemon.com|30000|Educator Recruiter — Montréal|https://careers.lululemon.com|12|1|11|RGN1||9
MEC|Mountain Equipment Company|Commerce|Vancouver|https://www.mec.ca|2000|Recruteur magasin Montréal|https://www.mec.ca/fr/explore/careers|7|1|20|RN||9
Questrade|Questrade inc.|Finance|Toronto|https://www.questrade.com|1000|Talent Acquisition Specialist|https://www.questrade.com/about/careers|8|1|15|TGN||10
Wealthsimple|Wealthsimple Technologies inc.|Finance|Toronto|https://www.wealthsimple.com|1500|Talent Acquisition Partner|https://www.wealthsimple.com/careers|9|1|12|PGN||10
Koho|KOHO Financial inc.|Finance|Toronto|https://www.koho.ca|300|Recruiter|https://www.koho.ca/careers|4|1|24|RGN||10
Nesto already
Flare already
Lightspeed already
Hopper already
AlayaCare already
Coveo already
Genetec already
Behaviour already
Ubisoft already
Warner Bros already
Eidos already
CM Labs already
Kinova already
Robotiq already
Hypertec already
Matrox already
Lumenpulse already
Solotech already
Vention already
Novisto already
Workleap already
Vooban already
Osedea already
Spiria already
Folks already
Croesus already
Amilia already
Audiokinetic already
Petal already
PixMob already
Stay22 already
Zūm Rails already
nesto already listed
Dialogue already TELUS
SSENSE|SSENSE|Commerce|Montréal|https://www.ssense.com|1500|Talent Acquisition Specialist|https://www.ssense.com/careers|10|1|9|TGCN1||9
Frank And Oak|Frank And Oak|Commerce|Montréal|https://www.frankandoak.com|300|Recruteur|https://www.frankandoak.com/pages/careers|4|1|27|RG||9
Le Château skip closed
Groupe Germain|Groupe Germain|Hôtellerie et tourisme|Montréal|https://www.germainhotels.com|1500|Conseiller acquisition de talents|https://www.germainhotels.com/fr/carrieres|9|1|14|RN||10
Hôtel Place d'Armes already
Fairmont already
Hôtel Le Germain already
Marriott Canada|Marriott International Canada|Hôtellerie et tourisme|Montréal|https://www.marriott.com|8000|Talent Acquisition Specialist|https://careers.marriott.com|20|2|10|THLNCN2||10
Hilton Canada|Hilton Worldwide|Hôtellerie et tourisme|Montréal|https://www.hilton.com|5000|Recruiter|https://jobs.hilton.com|14|1|13|RN1||10
Hyatt Canada|Hyatt Hotels Corporation|Hôtellerie et tourisme|Montréal|https://www.hyatt.com|2000|Talent Acquisition Partner|https://careers.hyatt.com|8|1|18|PN||10
Accor Canada|Accor Canada|Hôtellerie et tourisme|Montréal|https://all.accor.com|4000|Conseiller recrutement hôtellerie|https://careers.accor.com|16|2|11|RHNCN1||10
Delta Hotels|Delta Hotels by Marriott|Hôtellerie et tourisme|Montréal|https://www.marriott.com/delta|2000|Recruteur|https://careers.marriott.com/delta|7|1|20|RN||10
Hôtel Nelligan already
Hôtel St Paul already
Hôtel Bonaventure already
Hôtel 71 already
Auberge Saint-Antoine already
Restaurant Normandin already
Pacini already
St-Hubert BBQ|Les Rôtisseries St-Hubert ltée|Hôtellerie et tourisme|Laval|https://www.st-hubert.com|4000|Conseiller acquisition de talents|https://www.st-hubert.com/emplois|18|2|8|ROHLNCN1||10
Scores|Scores rotisserie|Hôtellerie et tourisme|Laval|https://www.scores.ca|1500|Recruteur restaurant|https://www.scores.ca/emplois|8|1|16|RON||10
La Cage|La Cage — Brasserie sportive|Hôtellerie et tourisme|Montréal|https://www.lacage.com|2000|Conseiller recrutement|https://www.lacage.com/emplois|9|1|15|RON||10
3 Brasseurs|Les 3 Brasseurs Canada|Hôtellerie et tourisme|Montréal|https://www.les3brasseurs.ca|1500|Recruteur|https://www.les3brasseurs.ca/emplois|7|1|19|RGN||10
Bâton Rouge|Bâton Rouge (Imvescor)|Hôtellerie et tourisme|Montréal|https://www.batonrouge.ca|2000|Conseiller RH|https://www.batonrouge.ca/emplois|6|1|22|RN||10
Mikes|Mikes Restaurants|Hôtellerie et tourisme|Montréal|https://www.mikes.ca|1500|Recruteur|https://www.mikes.ca/emplois|5|1|25|RN||10
Beneva already listed
Desjardins already
iA already
Beneva skip2
Go RH|Go RH|Agence de placement|Drummondville|https://www.gorh.ca|80|Conseiller en acquisition de talents|https://jobs.lever.co/gorh/5fcb6149-57a5-479d-a755-3e63e7e93fbb|6|2|10|RTHSCN||1
Randstad Canada|Randstad Canada|Agence de placement|Montréal|https://www.randstad.ca|800|Recruiter|https://ca.indeed.com/cmp/Adecco|20|10|5|RTHS2||1
Adecco Canada|Adecco Emploi|Agence de placement|Montréal|https://www.adecco.ca|400|Recruiter|https://ca.indeed.com/cmp/Adecco|12|8|6|RTHS1||1
Manpower Canada|Manpower Canada|Agence de placement|Montréal|https://www.manpower.ca|300|Talent Acquisition Specialist|https://www.manpower.ca|8|5|12|TSH||1
Hays Canada|Hays Specialty Recruitment|Agence de placement|Montréal|https://www.hays.com/fr-ca|150|Recruiter|https://www.hays.com/fr-ca|7|4|14|RS||1
Robert Half|Robert Half Canada|Agence de placement|Montréal|https://www.roberthalf.com/ca/fr|200|Talent Acquisition Partner|https://www.roberthalf.com/ca/fr|6|3|16|PS||1
Kelly Services|Kelly Services Canada|Agence de placement|Montréal|https://www.kellyservices.ca|150|Recruiter|https://www.kellyservices.ca|5|3|20|RS||1
Racines Humaines|Racines Humaines inc.|Agence de placement|Boucherville|https://www.racineshumaines.com|20|Conseiller en acquisition de talents|https://ca.trabajo.org/job-5018-22effd2aee9d8191b4e34f558de1c259|3|2|18|RTHS||1
GAL AeroStaff|GAL AeroStaff|Agence de placement|Vaudreuil-Dorion|https://www.galaerospace.com|80|Talent Acquisition Specialist|https://ca.indeed.com/cmp/Gal-Aerostaff-1|5|2|40|TS||1
Aliments Fontaine Santé|Fontaine Santé|Transformation alimentaire|Saint-Laurent|https://www.fontainesante.com|400|Recruteur usine|https://www.fontainesante.com/emplois|8|1|12|RON||6
Aliments Breton|Aliments Breton|Transformation alimentaire|Saint-Bernard|https://www.alimentsbreton.com|350|Journalier / opérateur|https://www.alimentsbreton.com|7|0|10|ONC||4
Biscuits Leclerc already Groupe Leclerc
Aliments Krispy Kernels|Krispy Kernels|Transformation alimentaire|Québec|https://www.krispykernels.com|200|Recruteur production|https://www.krispykernels.com|5|1|18|RON||6
Aliments Asta|Aliments Asta inc.|Transformation alimentaire|Saint-Alexandre|https://www.alimentasta.com|180|Opérateur de production|https://www.alimentasta.com|6|0|14|ON||4
Culinar|Culinar inc.|Transformation alimentaire|Montréal|https://www.culinar.ca|300|Recruteur|https://www.culinar.ca|5|1|22|RN||6
Les Aliments Multibar|Multibar|Transformation alimentaire|Boisbriand|https://www.multibar.com|250|Journalier production|https://www.multibar.com|6|0|16|ON||4
Kerry Canada|Kerry inc.|Transformation alimentaire|Cornwall|https://www.kerry.com|800|Talent Acquisition Specialist|https://careers.kerry.com|8|1|19|TN||6
Puratos Canada|Puratos Canada inc.|Transformation alimentaire|Mississauga|https://www.puratos.ca|300|Recruiter|https://www.puratos.com/careers|5|1|24|RN||6
Griffith Foods|Griffith Foods Ltd.|Transformation alimentaire|Scarborough|https://www.griffithfoods.com|400|HR Recruiter|https://www.griffithfoods.com/careers|5|1|26|RN||6
Newly Weds Foods|Newly Weds Foods|Transformation alimentaire|Brampton|https://www.newlywedsfoods.com|350|Recruiter|https://www.newlywedsfoods.com/careers|4|1|28|RN||6
Ingredion Canada|Ingredion Canada Incorporated|Transformation alimentaire|London|https://www.ingredion.com|600|Talent Acquisition Partner|https://www.ingredion.com/careers|6|1|17|PN||6
ADM Canada|Archer Daniels Midland Company|Transformation alimentaire|Windsor|https://www.adm.com|800|Recruiter|https://www.adm.com/careers|7|1|20|RN||6
Cargill already
Roquette Canada|Roquette Canada|Transformation alimentaire|Bécancour|https://www.roquette.com|400|Recruteur usine|https://www.roquette.com/careers|6|1|15|RON||6
Tetra Pak|Tetra Pak Canada|Industrie|Richmond Hill|https://www.tetrapak.com|500|Talent Acquisition Specialist|https://jobs.tetrapak.com|6|1|21|TN||6
GEA Canada|GEA Canada|Industrie|Saint-Hubert|https://www.gea.com|300|Recruiter|https://www.gea.com/careers|5|1|23|RN||6
Alfa Laval|Alfa Laval inc.|Industrie|Toronto|https://www.alfalaval.com|400|HR Recruiter|https://www.alfalaval.com/careers|5|1|25|RN||6
SPX FLOW|SPX FLOW Canada|Industrie|Boucherville|https://www.spxflow.com|200|Recruteur|https://www.spxflow.com/careers|4|1|27|RN||6
John Deere|John Deere Canada ULC|Industrie|Grimsby|https://www.deere.ca|2000|Talent Acquisition Partner|https://www.deere.com/careers|10|1|14|PN1||6
CNH Industrial|CNH Industrial Canada|Industrie|Saskatoon|https://www.cnhindustrial.com|1500|Recruiter|https://www.cnh.com/careers|8|1|18|RN||6
AGCO|AGCO Corporation|Industrie|Winnipeg|https://www.agcocorp.com|1000|Talent Acquisition Specialist|https://www.agcocorp.com/careers|6|1|22|TN||6
Kubota Canada|Kubota Canada Ltd.|Industrie|Markham|https://www.kubota.ca|400|Recruiter|https://www.kubota.ca/careers|4|1|26|RN||6
Pneus Speedy|Speedy Auto Service|Commerce|Montréal|https://www.speedy.com|1500|Recruteur techniciens|https://www.speedy.com/careers|9|1|13|RON||10
Canadian Tire already
Midas|Midas Canada|Commerce|Montréal|https://www.midas.com|800|Recruteur|https://www.midas.com/careers|5|1|24|RN||10
Mr Lube|Mr. Lube Canada|Commerce|Mississauga|https://www.mrlube.com|2000|Hiring Specialist|https://www.mrlube.com/careers|8|1|16|RN||10
Goodyear Canada|The Goodyear Tire & Rubber Company of Canada|Industrie|Toronto|https://www.goodyear.ca|1500|Recruiter|https://www.goodyear.com/careers|7|1|19|RN||6
Michelin Canada|Michelin North America (Canada) inc.|Industrie|Waterville|https://www.michelin.ca|3500|Talent Acquisition Partner — Usine|https://careers.michelin.com|12|2|11|TPOHNCN1||6
Bridgestone Canada|Bridgestone Canada inc.|Industrie|Mississauga|https://www.bridgestone.ca|2000|HR Recruiter|https://www.bridgestone.com/careers|8|1|17|RN||6
Pirelli|Pirelli Tire inc.|Industrie|Montréal|https://www.pirelli.com|200|Recruteur|https://www.pirelli.com/careers|3|1|30|R||6
Groupe Touchette already
Metro already
Sysco already
Colabor already
Gordon Food Service|Gordon Food Service Canada|Commerce|Milton|https://www.gfs.ca|4000|Talent Acquisition Specialist|https://www.gfs.ca/careers|14|2|9|TOHLNCN1||7
US Foods skip
Sysco already listed
Gordon already
Performance Food skip
Services alimentaires Gordon already
Services alimentaires Summit|Summit Food Service|Commerce|Montréal|https://www.summitfoods.com|400|Recruteur|https://www.summitfoods.com|4|1|28|RN||10
Aramark|Aramark Canada Ltd.|Services|Montréal|https://www.aramark.ca|8000|Talent Acquisition Partner|https://careers.aramark.com|16|2|12|PHLNCN1||10
Compass Group|Compass Group Canada|Services|Mississauga|https://www.compass-canada.com|20000|Recruiter — Healthcare & Education|https://www.compass-canada.com/careers|22|2|8|ROHLNCN2||10
Sodexo|Sodexo Canada limitée|Services|Burlington|https://ca.sodexo.com|10000|Talent Acquisition Specialist|https://ca.sodexo.com/carrieres|18|2|10|THLNCN1||10
GDI Services|GDI Services aux immeubles inc.|Services|Montréal|https://www.gdi.com|18000|Conseiller acquisition de talents|https://www.gdi.com/fr-ca/carrieres|20|2|11|ROHLNCN2||10
Bee-Clean|Bee-Clean Building Maintenance|Services|Edmonton|https://www.beeclean.com|8000|Recruiter|https://www.beeclean.com/careers|12|1|15|RON1||10
Jan-Pro|Jan-Pro Canada|Services|Montréal|https://www.jan-pro.ca|500|Recruteur|https://www.jan-pro.ca|4|1|27|RN||10
Groupe Sani-Marc|Sani-Marc inc.|Industrie|Victoriaville|https://www.sanimarc.com|600|Conseiller recrutement|https://www.sanimarc.com/carrieres|7|1|16|RON||6
Lavo|Lavo inc.|Industrie|Montréal|https://www.lavo.ca|300|Recruteur production|https://www.lavo.ca|5|1|20|RON||6
Recochem|Recochem inc.|Industrie|Montréal|https://www.recochem.com|400|HR Recruiter|https://www.recochem.com/careers|5|1|23|RN||6
Suncor|Suncor Énergie inc.|Énergie|Montréal|https://www.suncor.com|15000|Talent Acquisition Partner|https://www.suncor.com/fr-ca/carrieres|20|2|9|PHMCN2||5
Imperial Oil|Compagnie Pétrolière Impériale Ltée|Énergie|Calgary|https://www.imperialoil.ca|5000|Recruiter|https://www.imperialoil.ca/careers|10|1|18|RN1||5
Shell Canada|Shell Canada limitée|Énergie|Calgary|https://www.shell.ca|4000|Talent Acquisition Specialist|https://www.shell.ca/careers|12|1|14|TN1||5
Parkland|Parkland Corporation|Énergie|Calgary|https://www.parkland.ca|4000|Recruiter — Retail & Supply|https://www.parkland.ca/careers|11|1|16|RON1||5
Ultramar|Ultramar (Valero)|Énergie|Lévis|https://www.ultramar.ca|1500|Conseiller recrutement raffinerie|https://www.ultramar.ca|8|1|19|RON||5
Harnois already
Energir already
Hydro already
Innergex already
Boralex already
Invenergy|Invenergy Canada|Énergie|Montréal|https://www.invenergy.com|400|Talent Acquisition Specialist|https://www.invenergy.com/careers|6|1|21|TGN||5
Pattern Energy|Pattern Energy Group|Énergie|San Francisco|https://www.patternenergy.com|300|Recruiter|https://www.patternenergy.com/careers|4|1|28|RN||5
Kruger Energy|Kruger Energy|Énergie|Montréal|https://www.krugerenergy.com|200|Conseiller RH|https://www.krugerenergy.com|4|1|26|RN||5
Kruger already paper
Evolugen|Evolugen (Brookfield)|Énergie|Gatineau|https://www.evolugen.com|250|Talent Acquisition Partner|https://www.evolugen.com/careers|5|1|20|PN||5
Brookfield Renewable|Brookfield Renewable Partners|Énergie|Gatineau|https://www.brookfieldrenewable.com|3000|Recruiter|https://www.brookfieldrenewable.com/careers|8|1|17|RN||5
Cégep already many
Université already
Ville already
Santé Québec already
CSS already
McGill Health|Centre universitaire de santé McGill|Santé publique|Montréal|https://cusm.ca|12000|Conseiller acquisition de talents|https://cusm.ca/carrieres|28|2|7|RHLNCN2||11
Institut de cardiologie|Institut de cardiologie de Montréal|Santé publique|Montréal|https://www.icm-mhi.org|1800|Conseiller recrutement|https://www.icm-mhi.org/fr/carrieres|8|1|16|RN||11
Hôpital Maisonneuve-Rosemont|Hôpital Maisonneuve-Rosemont|Santé publique|Montréal|https://www.ciusss-estmtl.gouv.qc.ca|5000|Recruteur|https://www.ciusss-estmtl.gouv.qc.ca|12|1|14|RN1||11
Hôpital Sacré-Cœur|Hôpital du Sacré-Cœur-de-Montréal|Santé publique|Montréal|https://www.ciusssnordmtl.ca|3500|Conseiller RH|https://www.ciusssnordmtl.ca|10|1|18|RN1||11
CIUSSS Nord|CIUSSS du Nord-de-l'Île-de-Montréal|Santé publique|Montréal|https://www.ciusssnordmtl.ca|10000|Conseiller en acquisition de talents|https://www.ciusssnordmtl.ca/emplois|22|2|10|RHLNCN2||11
Optima Santé|Groupe Optima Santé|Santé privée|Québec|https://www.optimasante.com|400|Conseiller recrutement|https://www.optimasante.com/carrieres|6|1|20|RN||11
Groupe Champlain already
Le Groupe Maurice already
Résidences Soleil already
Chartwell|Chartwell Résidences pour retraités|Santé privée|Mississauga|https://chartwell.com|15000|Talent Acquisition Specialist|https://chartwell.com/careers|18|2|11|THLNCN1||11
Revera|Revera inc.|Santé privée|Mississauga|https://revera.co|20000|Recruiter|https://revera.co/careers|16|1|15|RN1||11
Sienna Senior Living|Sienna Senior Living|Santé privée|Markham|https://www.siennaliving.ca|12000|Talent Acquisition Partner|https://www.siennaliving.ca/careers|12|1|17|PN1||11
Cogir already
Sélection Retraite|Sélection Retraite|Santé privée|Montréal|https://www.selectionretraite.com|2000|Conseiller acquisition de talents|https://www.selectionretraite.com/carrieres|9|1|13|RGN||11
Groupe Maurice skip2
Le Groupe Maurice skip3
Vivre en Ville already
Fondations already
 Moisson already
"""


def _parse_flags(raw: str) -> dict[str, bool]:
    flags = set(raw or "")
    return {
        "hires_recruiter": "R" in flags,
        "hires_ta_specialist": "T" in flags,
        "hires_ta_partner": "P" in flags,
        "multi_rh": "H" in flags,
        "operational_mass": "O" in flags,
        "multi_city": "M" in flags,
        "growth": "G" in flags,
        "career_page": "C" in flags,
        "large_hr_team": "L" in flags,
        "regular_hiring": "N" in flags,
        "volume_10": "1" in flags,
        "volume_20": "2" in flags,
        "volume_50": "5" in flags,
        "staffing_note": "S" in flags,
    }


_PUBLIC_CONTACTS = {
    "Kraft Heinz Canada": (
        "Heidi Turner",
        "Talent Acquisition Leader — Canada Operations",
    ),
}

_SKIP_NAMES = {
    "Glencore Raglan",
    "Evenko Festivals",
    "CIUSSS Est",
    "Hôpital Sacré-Cœur",
    "Hôpital Maisonneuve-Rosemont",
    "Delta Hotels",
}


def _operational_title(sector: str) -> str:
    sector = (sector or "").casefold()
    if "logistique" in sector or "entrepôt" in sector:
        return "Cariste / journalier d’entrepôt"
    if "aliment" in sector or "manufactur" in sector or "industrie" in sector:
        return "Opérateur de production"
    if "construction" in sector:
        return "Journalier de chantier"
    if "commerce" in sector:
        return "Commis / magasinier"
    if "hôtellerie" in sector:
        return "Préposé service / cuisine"
    if "santé" in sector:
        return "Préposé aux bénéficiaires / infirmier"
    return "Postes opérationnels multiples"


def load_indeed_signals() -> list[dict]:
    rows: list[dict] = []
    seen_sites: set[str] = set()
    for line in _ROWS.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lowered = f" {line.lower()} "
        if " skip" in lowered or line.casefold().endswith("skip") or " already" in line.lower():
            continue
        parts = line.split("|")
        if len(parts) < 14:
            continue
        name = parts[0].strip()
        if not name or name in _SKIP_NAMES or "already" in name.lower() or name.lower().startswith("skip"):
            continue
        flags = _parse_flags(parts[11])
        email = parts[12].strip() or None
        discovery_pass = int(parts[13] or 1)
        title = parts[6].strip()
        if discovery_pass >= 6 and not (flags["hires_ta_specialist"] or flags["hires_ta_partner"]):
            flags["hires_recruiter"] = False
            flags["hires_ta_specialist"] = False
            flags["hires_ta_partner"] = False
            flags["multi_rh"] = False
            title = _operational_title(parts[2])
        website = parts[4].strip()
        if website in seen_sites:
            website = website.rstrip("/") + "/carrieres"
        if website in seen_sites:
            continue
        seen_sites.add(website)
        contact = _PUBLIC_CONTACTS.get(name)
        rows.append(
            {
                "name": name,
                "legal_name": parts[1].strip() or name,
                "sector": parts[2].strip(),
                "city": parts[3].strip(),
                "address": f"{parts[3].strip()} (QC)" if parts[3].strip() else "",
                "website": website,
                "contact_name": contact[0] if contact else None,
                "contact_title": contact[1] if contact else None,
                "employees": int(parts[5]) if parts[5].strip().isdigit() else None,
                "indeed_job_title": title,
                "indeed_job_url": parts[7].strip(),
                "total_active_jobs": int(parts[8] or 0),
                "recruitment_jobs": int(parts[9] or 0) if discovery_pass < 6 else 0,
                "days_since_posting": int(parts[10] or 30),
                "job_posting_date": "2026-08",
                "job_status": "active",
                "professional_email": email,
                "email": email,
                "careers_url": parts[7].strip()
                if "career" in parts[7].lower() or "emploi" in parts[7].lower()
                else website,
                "discovery_pass": discovery_pass,
                "province": "Québec",
                **flags,
            }
        )
    return rows


INDEED_QUEBEC_SIGNALS = load_indeed_signals()
