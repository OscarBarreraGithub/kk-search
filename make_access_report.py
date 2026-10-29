from pathlib import Path
import json, html, shutil, subprocess
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).parent;B=ROOT/'kk_data_access_2026-10-28'
S=json.loads((B/'collection_summary.json').read_text())
out=ROOT/'KK_Data_Access_Report.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleKK',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=colors.HexColor('#122E43'),spaceAfter=15))
styles.add(ParagraphStyle(name='DeckKK',fontName='Helvetica',fontSize=12,leading=17,textColor=colors.HexColor('#31556A'),spaceAfter=15))
styles.add(ParagraphStyle(name='BodyKK',fontName='Helvetica',fontSize=9.5,leading=13.2,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallKK',fontName='Helvetica',fontSize=8,leading=10.5,spaceAfter=5))
styles.add(ParagraphStyle(name='CellKK',fontName='Helvetica',fontSize=8.4,leading=11))
styles.add(ParagraphStyle(name='HeadKK',fontName='Helvetica-Bold',fontSize=14,leading=18,textColor=colors.HexColor('#122E43'),spaceBefore=10,spaceAfter=9))
story=[]
def p(s,style='BodyKK'):story.append(Paragraph(s,styles[style]))
def h(s):p(s,'HeadKK')
def link(label,url):return '<a href="'+html.escape(url,quote=True)+'" color="#176B88">'+html.escape(label)+'</a>'
def table(rows,widths,pad=7):
    t=Table([[Paragraph(str(c),styles['CellKK']) for c in r] for r in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDEBF1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#7BA0B5')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7F9')])]))
    story.append(t);story.append(Spacer(1,10))
def page(title):story.append(PageBreak());h(title)

p('Data access and collection<br/>for arXiv:2610.31458','TitleKK')
p('A public-data starting package, an inventory of larger datasets, and the route to missing collaboration inputs.','DeckKK')
p('Snapshot: 29 October 2026 UTC. The collection directory is dated 28 October. No physics reproduction, signal fit, or significance calculation has been performed.')
h('What is ready')
table([
 ['Collected locally','Verified contents'],
 ['Published sources',f"{S['paper_pdfs']} paper PDFs and {S['result_figure_pdfs']} official figure/table PDFs, across {S['result_page_directories']} result-page directories. These are publications and plots, not event datasets."],
 ['Public analyst repository',f"Pinned CMS EXO-21-010 code snapshot; {S['public_repo_root_files']} ROOT files opened and {S['exported_repo_histograms']} TH1 histograms exported as JSON. Includes observed spectra, signal templates and example fit artifacts."],
 ['Additional numerical spectrum','44 bins of the inclusive CMS four-jet spectrum from a secondary repository. Original HEPData comparison remains outstanding.'],
 ['Collision/simulation samples','4 complete ROOT files: 120,814 total entries, including 10,000 simulated entries; 251.6 MB. All four match CERN checksums; jet columns were read successfully.'],
 ['Acquisition inventory',f"{S['opendata_records']} CERN records and {S['enumerated_event_files']:,} listed event files, with locations, sizes and checksums. Formats and streams overlap: these are not 77,540 independent datasets."],
 ['Run quality and luminosity','CMS 2016 certified-run JSON plus luminosity, prescale and normalization-tag files downloaded.']
],[145,371])
h('What we can claim now')
p('<b>Public data are sufficient to begin a reproducibility audit and a partial event-level study.</b> Exact reproduction of the latest published fits and significance values is not yet secured. The small sample files test access and format; they are not statistically representative samples and do not establish that the claimed high-mass events are included.')
p('The practical first bulk dataset is CMS 2016 G/H JetHT NanoAOD: <b>310.24 GB</b>, 142 files and 244,738,738 events. The complete ATLAS 2015-2016 research release is <b>49.18 TB</b>. Both are public; storage and analysis coverage are the immediate constraints.')
p('Primary sources: '+link('Target paper','https://arxiv.org/abs/2610.31458')+'; '+link('CMS 2016G','https://opendata.cern.ch/record/30525')+'; '+link('CMS 2016H','https://opendata.cern.ch/record/30558')+'; '+link('ATLAS 2015','https://opendata.cern.ch/record/80000')+'; '+link('ATLAS 2016','https://opendata.cern.ch/record/80001')+'.','SmallKK')

page('1 / Trace the paper to the correct measurements')
p('The target is a phenomenological interpretation of several searches. Its plots do not correspond to one downloadable dataset. The following mapping separates measurements, reinterpretations and theory inputs.')
table([
 ['Target component','Underlying source and access status'],
 ['Figure 1: graviton / hh interpretation','Theory and earlier phenomenology: 2610.05889, 2606.29922 and 2506.09490. PDFs collected, with additional HH and diboson comparisons. Numerical model code has not been identified.'],
 ['Figure 2: CMS paired dijets','Run 2: EXO-21-010 / 2206.09997v3 (138 fb-1). Run 3: EXO-25-004 (90 fb-1 of 2024 data). Official public plots collected; Run 2 HEPData identified. Full Run 3 event release not established.'],
 ['Figure 3: ATLAS paired dijets','EXOT-2022-18 / 2307.14944v2 (140 fb-1). Paper, 103 figure/table PDFs and HEPData reference collected. Open 2015-2016 events cover only part of this exposure.'],
 ['Figure 4: broad four-jet p-values','CMS EXO-24-038 / 2507.17884, now merged into EXO-21-010. The collected 2206.09997v3 includes the addendum. The standalone EXO-24-038 page and PDF were not downloaded.'],
 ['Figure 5: nonresonant p-values','CMS EXO-21-010. Public plots collected. Analyst repository is especially relevant here, but its 2021 snapshot must be checked against the final selection and revisions.'],
 ['Figure 6: KK-gluon cross sections','Theory paper hep-ph/0701166. PDF collected. Reproduction needs model parameters, PDF set, perturbative choices and collider energy; the plot alone is not a modern 13/13.6 TeV prediction.'],
 ['Figure 7: dibosons','CMS B2G-20-009 / 2210.00043v2 (138 fb-1). Paper, 163 public figure/table PDFs and HEPData reference collected.'],
 ['Figure 8: dileptons','CMS EXO-25-021, including a 283 fb-1 Run 3 result. Public page and 36 plots/tables collected. PAS PDF blocked by the CDS access challenge.'],
 ['Other relevant checks','b-tagged paired dijets EXO-24-039; earlier paired dijets EXO-17-021; ATLAS ttbar EXOT-2018-49; Run 2 dilepton, diphoton, HH and heavy-resonance searches.']
],[146,370])
p('<b>Provenance correction:</b> reference [1] in the target names the b-jet search 2609.21850 and the Run 3 PAS. The untagged Run 2 excesses require the additional EXO-21-010 and EXO-24-038 sources. The broad reinterpretation and original search reuse the same collisions; do not combine them as independent evidence.')
p(link('CMS original plus erratum/addendum','https://arxiv.org/abs/2206.09997v3')+'; '+link('Broad-search merger notice','https://arxiv.org/abs/2507.17884v2')+'.','SmallKK')

page('2 / Numerical inputs: useful, with clear provenance')
h('Public analysis repository')
p(link('tw-hu/CMSAnalysis','https://github.com/tw-hu/CMSAnalysis/tree/8c4e503bcf874159240cd81096fab2ee0c57b95d')+' is pinned at commit <font name="Courier">8c4e503bcf874159240cd81096fab2ee0c57b95d</font>. The README identifies it as scripts for CMS EXO-21-010. A source archive and extracted tree are included.')
p('All 57 ROOT files were opened with uproot. The 48 exported TH1 objects include seven observed average-dijet-mass histograms, signal templates and systematic variants. Other objects include example RooWorkspaces and fit outputs. Reading the ROOT containers does not validate that custom RooFit classes can be loaded or that the fit can run.')
table([
 ['Observed histogram file','Bins','Sum of visible-bin contents'],
 ['PFJetHT_RunII_asl0.root','3,591','34,209'],
 ['PFJetHT_RunII_asl0_no4J.root','3,656','81,668'],
 ['PFJetHT_RunII_asl1.root','3,445','38,032'],
 ['PFJetHT_RunII_asl1_no4J.root','3,484','59,481'],
 ['PFJetHT_RunII_asl2.root','3,404','5,158'],
 ['PFJetHT_RunII_asl2_no4J.root','3,404','5,189'],
 ['PFJetHT_RunII_asl3.root','1,625','33,033'],
],[280,64,172])
p('<b>Do not sum these as independent event samples.</b> They include alternative selections and categories. This is a public analyst snapshot, not a certified final numerical release. Its date precedes the published erratum and addendum.')
h('What the repository still needs')
p('The README requires CMSSW, a specific Combine branch, CombineHarvester and custom RooFit classes. Input picotrees are referenced on Rutgers storage. A second public June 2021 README points to the final 13-alpha-bin datacards and workspaces in a CMS group EOS area. Those referenced files have not been obtained or authenticated against. The code snapshot is therefore not a self-contained final-fit package.')
h('Independent copy of the inclusive spectrum')
p('A 44-bin copy of CMS Figure 15 is preserved from '+link('hftsoi/symbolfit','https://github.com/hftsoi/symbolfit/blob/d6c8bf035bedf30da4e8f4ae777dc6ca5c453cdf/examples/datasets/dijet_pair/dataset.py')+'. It includes centers, widths and asymmetric uncertainties. The original source file is archived; values were parsed without executing it. It explicitly cites HEPData, but has not yet been compared to that export. Treat it as provisional.')
p('The official plot labels the cross-section density in pb/TeV; the copied mass centers are in GeV. This unit assignment is recorded in the JSON. No likelihood or bin-to-bin covariance is supplied by this copy.','SmallKK')

page('3 / Public collision datasets and storage requirements')
p('Sizes below are decimal GB/TB from CERN metadata or enumerated file sizes. These are remote dataset sizes, not downloaded volumes. Manifests are saved under <font name="Courier">opendata/manifests/</font>.')
table([
 ['Dataset / CERN record IDs','Events / files','Remote size','Role'],
 ['CMS 2016 G/H JetHT NanoAOD<br/>30525, 30558','244.74 million<br/>142','310.24 GB','First event-level acquisition'],
 ['CMS 2016 G/H JetHT MiniAOD<br/>30508, 30541','244.80 million<br/>2,545','9.12 TB','Richer format; overlaps NanoAOD'],
 ['CMS 2015D JetHT MiniAOD<br/>24124','76.52 million<br/>1,607','1.51 TB','Additional 13 TeV run'],
 ['CMS 2012 B/C/D JetHT AOD<br/>6010, 6036, 24450','68.86 million<br/>6,292 listed','23.19 TB','8 TeV cross-check; metadata issue below'],
 ['ATLAS 2015 PHYSLITE<br/>80000','1.69 billion<br/>10,049','10.28 TB','Public research release'],
 ['ATLAS 2016 PHYSLITE<br/>80001','5.38 billion<br/>45,571','38.90 TB','Public research release'],
 ['ATLAS QCD nominal MC collection<br/>80014','313.88 million<br/>2,097','3.16 TB','Mixture; choose subprocesses carefully'],
 ['CMS 2016 QCD HT1000-1500 NanoAOD<br/>63079','12.25 million<br/>24','28.44 GB','One background slice, not complete QCD'],
 ['CMS 2016G enhanced PF NanoAOD<br/>31308','120.52 million<br/>842 ROOT files','1.52 TB listed','Alternative to standard NanoAOD'],
],[190,100,70,156])
p('Also catalogued: 2016 G/H DoubleEG (159.51 GB), DoubleMuon (88.25 GB), SingleElectron (257.06 GB) and SingleMuon (259.66 GB) NanoAOD streams, and corresponding MiniAOD records. They support dilepton/control studies; streams overlap and require event-level deduplication and trigger accounting.')
h('Checks completed on real files')
p('Downloaded: CMS JetHT 2016G (107,505 events); ATLAS 2015 (1,578); ATLAS 2016 (1,731); ATLAS MC (10,000). All pass byte-size and Adler-32 checks. Jet pt/eta/phi/m columns were read for the first 10 entries of each file. The selected MC file belongs to Sherpa single-photon pt 35-70 in the broad QCD record; it tests transport/format and is not a dedicated four-jet background sample.')
h('Coverage and metadata caveats')
p('Open CMS 2016 G/H is a subset of Run 2, and does not reproduce the 138 fb-1 measurement. Open ATLAS 2015-2016 is also a subset of the 140 fb-1 paired-dijet search. The 8 TeV data cannot directly test production of an 8.6 TeV resonance. No full relevant Run 3 event release was established.')
p('Record 6036 declares 2,212 files but lists 2,210 in the retrieved indices; two file entries need reconciliation. Record 31308 has an inconsistent aggregate byte count and includes a separate luminosity JSON; use the enumerated sizes and distinguish 842 ROOT files from the auxiliary file.','SmallKK')

page('4 / Official numerical exports still to obtain')
p('HEPData exports were blocked by a Cloudflare access challenge in this environment. This is a retrieval problem, not evidence that the data are private. The records below were identified from official source pages. Record-specific export contents and versions have not yet been verified.')
rows=[['Analysis','HEPData record','Priority']]
for r in json.loads((B/'hepdata_access.json').read_text()):
    rows.append([r['analysis'].replace('_',' '),link(r['record_id'],r['record_url']),r['priority']])
table(rows,[236,180,100])
p('<b>Most useful immediate help:</b> open the four core records in a normal browser, download the complete YAML submission including auxiliary resources, and attach the archives. Preserve the DOI/version and do not export only a screenshot. CSV or ROOT exports are useful additions. The comparison records can follow.')
h('Other blocked or unfinished public downloads')
p('The CMS PAS PDFs for EXO-25-004 and EXO-25-021 returned the CDS anti-bot page instead of a PDF. Their public result-page plots are already collected. If browser access works, attach the two PDFs: '+link('EXO-25-004','https://cds.cern.ch/record/2947130/files/EXO-25-004-pas.pdf')+' and '+link('EXO-25-021','https://cds.cern.ch/record/2961528/files/EXO-25-021-pas.pdf')+'.')
p('Later fetches of additional comparison plots encountered network tunnel 403 failures. The package records every failed URL separately; 266 unsuccessful targets remain in the log, including exploratory invalid/obsolete targets. These should be triaged, not treated as 266 required datasets. The source paper PDFs already contain many of the corresponding figures.','SmallKK')

page('5 / What Harvard can provide, and what it cannot')
h('A practical institutional route')
p('Harvard has an active ATLAS group led by Melissa Franklin, John Huth and Masahiro Morii. A group member could assess whether this proposed study is suitable for collaboration work and help locate approved analysis inputs. Affiliation with Harvard alone does not establish permission to access internal ATLAS or CMS data.')
p('For a non-ATLAS researcher, an ATLAS Short-Term Association can potentially include collision and simulation access. It requires a written scientific proposal, agreement with the relevant group leadership and formal collaboration endorsement. Approval is project-specific. An association for interacting with Monte Carlo authors does not itself grant direct data access.')
p('Harvard FAS Research Computing can supply computing and storage through an eligible lab/PI account. That is a separate authorization from experimental data access. I have not inspected your Harvard, CERN or cluster accounts, and have not established your eligibility or existing memberships.')
p('Official routes: '+link('Harvard ATLAS group and contacts','https://lppc.physics.harvard.edu/harvard-atlas-group')+'; '+link('ATLAS external collaboration procedure','https://atlas.cern/Discover/Collaboration/External-Collaboration')+'; '+link('FASRC account request','https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/')+'; '+link('FASRC eligibility','https://docs.rc.fas.harvard.edu/kb/account-qualifications/')+'.','SmallKK')
h('Concrete missing inputs to request')
table([
 ['Owner / route','Specific request'],
 ['CMS EXO-21-010 / EXO-24-038 analysis team','Final observed histograms for every alpha category; final datacards and RooWorkspaces; custom RooFit PDFs; background-envelope settings; nuisance parameters and correlations; resonance templates over masses, mass ratios and widths; versions matching the erratum/addendum.'],
 ['CMS EXO-25-004 / EXO-25-021 teams','Public numerical tables or a releaseable statistical model, category definitions, selections, efficiency/acceptance information and significance scan definitions. These may be enough without unrestricted event access.'],
 ['ATLAS EXOT-2022-18 team','Complete final histograms, likelihood/workspace if releasable, calibration and event-selection details needed to relate PHYSLITE to the published result. Ask whether open-data coverage can support a useful independent study.'],
 ['Authors of arXiv:2610.31458','Model code and parameters; definitions of manually drawn event contours; original numerical values used in derived rate and branching-ratio estimates; treatment of common datasets, trial factors and correlated excesses.'],
],[155,361])
h('Information needed from you')
p('<b>1.</b> Your Harvard school/department, research group or PI, and whether you already have FASRC/CERN/ATLAS/CMS access. Names/status are enough; do not send passwords or tokens.<br/><b>2.</b> A usable compute/storage destination. Roughly 0.5-1 TB is a reasonable planning allowance for the 310 GB CMS input plus outputs; ATLAS needs selective reading or a substantially larger allocation.<br/><b>3.</b> The four core HEPData exports if browser download works for you.')
p('No account applications, collaboration requests or messages to researchers have been sent.','SmallKK')

page('6 / How to use the collection')
table([
 ['Path inside the package','Purpose'],
 ['collection_summary.json','Counts and scope of this snapshot.'],
 ['papers/; analyses/','Downloaded source papers, official result pages, plots and discovered links. A PDF is not a substitute for its numerical table.'],
 ['code/','Pinned CMS code archive/tree, README files and inventory of ROOT objects.'],
 ['numerical/','48 exported repository histograms and the provisional 44-bin inclusive spectrum. Preserve their provenance labels.'],
 ['opendata/records/; opendata/manifests/','Original CERN metadata; normalized file-by-file JSONL lists and original XRootD URI lists for 34 records.'],
 ['opendata/samples/; opendata/auxiliary/','The four complete test files and downloaded luminosity/run-quality inputs.'],
 ['opendata/validated_samples.json; sample_column_checks.json','Expected/observed checksums, tree entries and successful column reads. The column-check file is in opendata/.'],
 ['hepdata_access.json; pending_public_downloads.json','Exact public record/export URLs and failed download targets.'],
 ['acquire_events.py; verify_package.py','Budget-limited event downloader (dry run by default) and package integrity verification.'],
 ['download_log.jsonl; SHA256.json','Retrieval provenance and byte-level inventory of delivered files.'],
],[227,289],pad=4)
h('Recommended acquisition order')
p('<b>First:</b> obtain and inspect the core HEPData exports, resolve their versions and compare the provisional numerical inputs. This is much smaller than event-level reprocessing and directly tests the published curves.<br/><b>Second:</b> stage CMS 2016 G/H NanoAOD on the chosen storage, then select additional MC slices and corrections required by the exact selection. Do not assume the single QCD HT slice is adequate.<br/><b>Third:</b> develop a PHYSLITE skim against a small ATLAS subset before attempting a multi-terabyte transfer.<br/><b>In parallel:</b> request releaseable final likelihood inputs through the experimental teams or a Harvard collaborator.')
h('Downloader examples')
p('<font name="Courier">python3 verify_package.py</font><br/><br/><font name="Courier">python3 acquire_events.py --record 30525 --record 30558<br/>--out /data/kk --max-gb 320</font>','SmallKK')
p('The second command is one logical command and only prints a plan. Append <font name="Courier">--execute</font> to transfer the selected 310.24 GB. For a smaller transport test, use <font name="Courier">--limit-files 1</font> and an appropriate byte budget. Run it on the storage host. It checks sizes and CERN checksums and leaves failures in an acquisition log; it does not install CMSSW or run a physics analysis.')
p('CMS NanoAOD can be read with standard ROOT or Python uproot/awkward. MiniAOD/AOD require the corresponding CMS software environment. The native public analyst code uses older CMSSW/Combine components and should be isolated before execution. ATLAS PHYSLITE jets use MeV; CMS NanoAOD jets use GeV. Apply validated-run masks, trigger selections, luminosity accounting and experiment-specific object corrections before interpreting yields.')
p('Guidance: '+link('CMS NanoAOD getting started','https://opendata.cern.ch/docs/cms-getting-started-nanoaod')+'; '+link('CMS research data guide','https://opendata.cern.ch/docs/cms-guide-for-research')+'. The package includes raw search responses for provenance; unsuccessful search queries are not evidence that a dataset does not exist.','SmallKK')

def footer(c,d):
    c.setStrokeColor(colors.HexColor('#B6CAD5'));c.line(48,42,564,42)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#557080'))
    c.drawString(48,29,'KK PAPER / DATA ACCESS / 29 OCT 2026')
    c.drawRightString(564,29,str(d.page))
doc=SimpleDocTemplate(str(out),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=55,title='Data access for arXiv:2610.31458',author='Research data collection')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
shutil.copy2(out,B/out.name)
print(out)
