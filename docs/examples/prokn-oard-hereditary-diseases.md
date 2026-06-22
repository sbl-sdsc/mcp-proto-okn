# Chat Transcript

## Hereditary Diseases Common to ProKN and OARD-KG (by MONDO ID)

👤 **User**

List hereditary diseases common among ProKN and OARD-KG using MONDO ids.

---

🧠 **Assistant**

To answer this I needed to reconcile how each graph represents diseases, find the overlap by MONDO identifier, and then restrict to hereditary diseases.

**How the two graphs represent diseases**

- **OARD-KG** stores diseases directly as MONDO URIs (e.g., `http://purl.obolibrary.org/obo/MONDO_0000050`), typed via `biolink:category` → `biolink:Disease`. It contains **2,297** MONDO disease nodes.
- **ProKN** stores diseases as Disease Ontology (DOID) nodes (class `http://purl.uniprot.org/core/Disease`) but cross-references MONDO through `rdfs:seeAlso`. It carries **3,147** distinct MONDO links.

**Finding the overlap**

A single cross-`GRAPH` query returned 0 (the named graphs sit behind separate endpoints), so I used a **federated SPARQL query** with a `SERVICE` call from the ProKN endpoint out to the OARD-KG endpoint, joining on the shared MONDO URI:

```sparql
SELECT (COUNT(DISTINCT ?mondo) AS ?n) WHERE {
  ?d a <http://purl.uniprot.org/core/Disease> ;
     <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?mondo .
  FILTER(STRSTARTS(STR(?mondo), "http://purl.obolibrary.org/obo/MONDO_"))
  SERVICE <https://apps.okn.us/oard-kg/sparql> {
    ?mondo <https://w3id.org/biolink/vocab/category> <https://w3id.org/biolink/vocab/Disease> .
  }
}
```

This yields **445** diseases shared by both graphs.

**Restricting to hereditary diseases**

The MONDO term for hereditary disease is **MONDO:0003847**. Ontology expansion of this term timed out (the subtree is very large), so I added a second `SERVICE` call to **Ubergraph**, whose materialized `subClassOf` closure lets a direct `subClassOf` edge stand in for the full transitive descendant set:

```sparql
SELECT DISTINCT ?mondo ?label WHERE {
  ?d a <http://purl.uniprot.org/core/Disease> ;
     <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?mondo .
  FILTER(STRSTARTS(STR(?mondo), "http://purl.obolibrary.org/obo/MONDO_"))
  SERVICE <https://apps.okn.us/oard-kg/sparql> {
    ?mondo <https://w3id.org/biolink/vocab/category> <https://w3id.org/biolink/vocab/Disease> ;
           <http://www.w3.org/2000/01/rdf-schema#label> ?label .
  }
  SERVICE <https://ubergraph.apps.renci.org/sparql> {
    ?mondo <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://purl.obolibrary.org/obo/MONDO_0003847> .
  }
}
ORDER BY ?label
```

**Result: 323 hereditary diseases** are common to ProKN and OARD-KG (out of the 445 total disease overlaps).

| # | MONDO ID | Disease |
|---|----------|---------|
| 1 | MONDO:0007037 | achondroplasia |
| 2 | MONDO:0008713 | acrodermatitis enteropathica |
| 3 | MONDO:0008294 | acute intermittent porphyria |
| 4 | MONDO:0018544 | adrenoleukodystrophy |
| 5 | MONDO:0009897 | adult polyglucosan body disease |
| 6 | MONDO:0043209 | albinism |
| 7 | MONDO:0008752 | Alexander disease |
| 8 | MONDO:0013282 | alpha 1-antitrypsin deficiency |
| 9 | MONDO:0011399 | alpha thalassemia |
| 10 | MONDO:0018965 | Alport syndrome |
| 11 | MONDO:0016241 | alternating hemiplegia of childhood |
| 12 | MONDO:0007088 | Alzheimer disease type 1 |
| 13 | MONDO:0012790 | amyotrophic lateral sclerosis type 10 |
| 14 | MONDO:0012945 | amyotrophic lateral sclerosis type 11 |
| 15 | MONDO:0011223 | amyotrophic lateral sclerosis type 4 |
| 16 | MONDO:0008222 | Andersen-Tawil syndrome |
| 17 | MONDO:0019154 | androgen insensitivity syndrome |
| 18 | MONDO:0013426 | aneurysm-osteoarthritis syndrome |
| 19 | MONDO:0008397 | aplasia of lacrimal and salivary glands |
| 20 | MONDO:0008815 | argininosuccinic aciduria |
| 21 | MONDO:0008830 | aspartylglucosaminuria |
| 22 | MONDO:0018266 | ataxia - telangiectasia variant |
| 23 | MONDO:0008840 | ataxia telangiectasia |
| 24 | MONDO:0014500 | atrial conduction disease |
| 25 | MONDO:0020290 | atrioventricular septal defect |
| 26 | MONDO:0016244 | atypical hemolytic-uremic syndrome |
| 27 | MONDO:0009411 | autoimmune polyendocrine syndrome type 1 |
| 28 | MONDO:0009925 | autosomal recessive inherited pseudoxanthoma elasticum |
| 29 | MONDO:0009675 | autosomal recessive limb-girdle muscular dystrophy type 2A |
| 30 | MONDO:0009677 | autosomal recessive limb-girdle muscular dystrophy type 2C |
| 31 | MONDO:0009889 | autosomal recessive polycystic kidney disease |
| 32 | MONDO:0013743 | autosomal systemic lupus erythematosus type 16 |
| 33 | MONDO:0008854 | Bardet-Biedl syndrome 1 |
| 34 | MONDO:0010543 | Barth syndrome |
| 35 | MONDO:0010311 | Becker muscular dystrophy |
| 36 | MONDO:0007534 | Beckwith-Wiedemann syndrome |
| 37 | MONDO:0009276 | Bernard-Soulier syndrome |
| 38 | MONDO:0019402 | beta thalassemia |
| 39 | MONDO:0008029 | Bethlem myopathy |
| 40 | MONDO:0008947 | bilateral striopallidodentate calcinosis |
| 41 | MONDO:0009665 | biotinidase deficiency |
| 42 | MONDO:0008876 | Bloom syndrome |
| 43 | MONDO:0011510 | Bohring-Opitz syndrome |
| 44 | MONDO:0015263 | Brugada syndrome |
| 45 | MONDO:0012742 | Brugada syndrome 3 |
| 46 | MONDO:0015270 | butyrylcholinesterase deficiency |
| 47 | MONDO:0008828 | camptodactyly-arthropathy-coxa vara-pericarditis syndrome |
| 48 | MONDO:0010079 | Canavan disease |
| 49 | MONDO:0009376 | carbamoyl phosphate synthetase I deficiency disease |
| 50 | MONDO:0010753 | cardiac valvular dysplasia, X-linked |
| 51 | MONDO:0009705 | carnitine palmitoyl transferase 1A deficiency |
| 52 | MONDO:0015564 | Castleman disease |
| 53 | MONDO:0017990 | catecholaminergic polymorphic ventricular tachycardia |
| 54 | MONDO:0015626 | Charcot-Marie-Tooth disease |
| 55 | MONDO:0019011 | Charcot-Marie-Tooth disease type 1 |
| 56 | MONDO:0007309 | Charcot-Marie-Tooth disease type 1A |
| 57 | MONDO:0010621 | CHILD syndrome |
| 58 | MONDO:0010826 | childhood absence epilepsy |
| 59 | MONDO:0011184 | childhood apraxia of speech |
| 60 | MONDO:0007319 | chondrocalcinosis 2 |
| 61 | MONDO:0018305 | chronic granulomatous disease |
| 62 | MONDO:0015991 | citrullinemia |
| 63 | MONDO:0008988 | citrullinemia type I |
| 64 | MONDO:0008728 | classic congenital adrenal hyperplasia due to 21-hydroxylase deficiency |
| 65 | MONDO:0009258 | classic galactosemia |
| 66 | MONDO:0009348 | classic Hodgkin lymphoma |
| 67 | MONDO:0016064 | cleft palate |
| 68 | MONDO:0007617 | Coffin-Siris syndrome 1 |
| 69 | MONDO:0014276 | combined immunodeficiency due to CD3gamma deficiency |
| 70 | MONDO:0014197 | combined immunodeficiency due to MALT1 deficiency |
| 71 | MONDO:0015517 | common variable immunodeficiency |
| 72 | MONDO:0009006 | complement component 2 deficiency |
| 73 | MONDO:0018479 | congenital adrenal hyperplasia |
| 74 | MONDO:0008730 | congenital adrenal hyperplasia due to 17-alpha-hydroxylase deficiency |
| 75 | MONDO:0013184 | congenital diarrhea 5 with tufting enteropathy |
| 76 | MONDO:0013825 | congenital diarrhea 6 |
| 77 | MONDO:0009210 | congenital factor V deficiency |
| 78 | MONDO:0008720 | congenital isolated adrenocorticotropic hormone deficiency |
| 79 | MONDO:0008725 | congenital lipoid adrenal hyperplasia due to STAR deficency |
| 80 | MONDO:0009732 | congenital nephrotic syndrome, Finnish type |
| 81 | MONDO:0019306 | congenital non-bullous ichthyosiform erythroderma |
| 82 | MONDO:0009114 | congenital sucrase-isomaltase deficiency |
| 83 | MONDO:0009026 | Costello syndrome |
| 84 | MONDO:0015469 | craniosynostosis |
| 85 | MONDO:0007405 | Crouzon syndrome |
| 86 | MONDO:0009061 | cystic fibrosis |
| 87 | MONDO:0009067 | cystinuria |
| 88 | MONDO:0010281 | Danon disease |
| 89 | MONDO:0007417 | Darier disease |
| 90 | MONDO:0015612 | Dent disease |
| 91 | MONDO:0010472 | developmental and epileptic encephalopathy, 36 |
| 92 | MONDO:0015253 | Diamond-Blackfan anemia |
| 93 | MONDO:0007269 | dilated cardiomyopathy 1A |
| 94 | MONDO:0018949 | distal myopathy |
| 95 | MONDO:0007473 | Duane retraction syndrome |
| 96 | MONDO:0010679 | Duchenne muscular dystrophy |
| 97 | MONDO:0007496 | dystonia 12 |
| 98 | MONDO:0007492 | early-onset generalized limb-onset dystonia |
| 99 | MONDO:0011060 | early-onset non-syndromic cataract |
| 100 | MONDO:0020066 | Ehlers-Danlos syndrome |
| 101 | MONDO:0016002 | Ehlers-Danlos syndrome, kyphoscoliotic type 1 |
| 102 | MONDO:0017314 | Ehlers-Danlos syndrome, vascular type |
| 103 | MONDO:0021569 | Emery-Dreifuss muscular dystrophy 2, autosomal dominant |
| 104 | MONDO:0011724 | encephalopathy due to GLUT1 deficiency |
| 105 | MONDO:0017610 | epidermolysis bullosa simplex |
| 106 | MONDO:0007239 | epidermolytic hyperkeratosis |
| 107 | MONDO:0016028 | erythromelalgia |
| 108 | MONDO:0010526 | Fabry disease |
| 109 | MONDO:0007100 | familial amyloid neuropathy |
| 110 | MONDO:0010188 | familial isolated deficiency of vitamin E |
| 111 | MONDO:0000608 | familial juvenile hyperuricemic nephropathy |
| 112 | MONDO:0008073 | familial juvenile hyperuricemic nephropathy type 1 |
| 113 | MONDO:0009387 | familial lipoprotein lipase deficiency |
| 114 | MONDO:0019171 | familial long QT syndrome |
| 115 | MONDO:0018088 | familial Mediterranean fever |
| 116 | MONDO:0009297 | familial renal glucosuria |
| 117 | MONDO:0007606 | fibrodysplasia ossificans progressiva |
| 118 | MONDO:0007097 | Finnish type amyloidosis |
| 119 | MONDO:0100339 | Friedreich ataxia |
| 120 | MONDO:0017276 | frontotemporal dementia |
| 121 | MONDO:0005321 | Fuchs' endothelial dystrophy |
| 122 | MONDO:0017719 | gangliosidosis |
| 123 | MONDO:0011719 | gastrointestinal stromal tumor |
| 124 | MONDO:0018150 | Gaucher disease |
| 125 | MONDO:0009904 | Gitelman syndrome |
| 126 | MONDO:0011612 | glycine encephalopathy |
| 127 | MONDO:0002412 | glycogen storage disease |
| 128 | MONDO:0012747 | glycogen storage disease due to aldolase A deficiency |
| 129 | MONDO:0009292 | glycogen storage disease due to glycogen branching enzyme deficiency |
| 130 | MONDO:0013046 | glycogen storage disease due to muscle beta-enolase deficiency |
| 131 | MONDO:0009865 | glycogen storage disease due to phosphoglycerate mutase deficiency |
| 132 | MONDO:0002413 | glycogen storage disease I |
| 133 | MONDO:0009290 | glycogen storage disease II |
| 134 | MONDO:0009291 | glycogen storage disease III |
| 135 | MONDO:0010598 | glycogen storage disease IXa |
| 136 | MONDO:0009293 | glycogen storage disease V |
| 137 | MONDO:0009294 | glycogen storage disease VI |
| 138 | MONDO:0018149 | GM1 gangliosidosis |
| 139 | MONDO:0009260 | GM1 gangliosidosis type 1 |
| 140 | MONDO:0011603 | GNE myopathy |
| 141 | MONDO:0021001 | hemochromatosis type 1 |
| 142 | MONDO:0010602 | hemophilia A |
| 143 | MONDO:0010604 | hemophilia B |
| 144 | MONDO:0019623 | hereditary angioedema |
| 145 | MONDO:0033946 | hereditary angioedema with C1Inh deficiency |
| 146 | MONDO:0007648 | hereditary diffuse gastric adenocarcinoma |
| 147 | MONDO:0019180 | hereditary hemorrhagic telangiectasia |
| 148 | MONDO:0011445 | hereditary spastic paraplegia 11 |
| 149 | MONDO:0010733 | hereditary spastic paraplegia 2 |
| 150 | MONDO:0008437 | hereditary spastic paraplegia 3A |
| 151 | MONDO:0008438 | hereditary spastic paraplegia 4 |
| 152 | MONDO:0010047 | hereditary spastic paraplegia 5A |
| 153 | MONDO:0019312 | Hermansky-Pudlak syndrome |
| 154 | MONDO:0009353 | homocystinuria due to methylene tetrahydrofolate reductase deficiency |
| 155 | MONDO:0018328 | homozygous familial hypercholesterolemia |
| 156 | MONDO:0007739 | Huntington disease |
| 157 | MONDO:0007818 | Hyper-IgE recurrent infection syndrome 1 |
| 158 | MONDO:0010626 | hyper-IgM syndrome type 1 |
| 159 | MONDO:0009849 | hyperimmunoglobulinemia D with periodic fever |
| 160 | MONDO:0008224 | hyperkalemic periodic paralysis |
| 161 | MONDO:0018473 | hyperlipoproteinemia type 3 |
| 162 | MONDO:0007762 | hyperlipoproteinemia type V |
| 163 | MONDO:0007768 | hyperparathyroidism 2 with jaw tumors |
| 164 | MONDO:0017774 | hypobetalipoproteinemia |
| 165 | MONDO:0018555 | hypogonadotropic hypogonadism |
| 166 | MONDO:0018570 | hypophosphatasia |
| 167 | MONDO:0019052 | inborn errors of metabolism |
| 168 | MONDO:0007403 | inherited Creutzfeldt-Jakob disease |
| 169 | MONDO:0008788 | IRIDA syndrome |
| 170 | MONDO:0009876 | isolated growth hormone deficiency type IA |
| 171 | MONDO:0010139 | isolated thyroid-stimulating hormone deficiency |
| 172 | MONDO:0002441 | Jervell and Lange-Nielsen syndrome |
| 173 | MONDO:0018772 | Joubert syndrome |
| 174 | MONDO:0017612 | junctional epidermolysis bullosa |
| 175 | MONDO:0009696 | juvenile myoclonic epilepsy |
| 176 | MONDO:0020367 | juvenile open angle glaucoma |
| 177 | MONDO:0017380 | juvenile polyposis syndrome |
| 178 | MONDO:0018800 | Kallmann syndrome |
| 179 | MONDO:0010735 | Kennedy disease |
| 180 | MONDO:0015486 | keratoconus |
| 181 | MONDO:0012548 | Kostmann syndrome |
| 182 | MONDO:0009499 | Krabbe disease |
| 183 | MONDO:0009697 | Lafora disease |
| 184 | MONDO:0009509 | Landau-Kleffner syndrome |
| 185 | MONDO:0011579 | late-onset retinal degeneration |
| 186 | MONDO:0010788 | Leber hereditary optic neuropathy |
| 187 | MONDO:0009723 | Leigh syndrome |
| 188 | MONDO:0016532 | Lennox-Gastaut syndrome |
| 189 | MONDO:0007481 | Leri-Weill dyschondrosteosis |
| 190 | MONDO:0018875 | Li-Fraumeni syndrome |
| 191 | MONDO:0008323 | Liddle syndrome |
| 192 | MONDO:0016971 | limb-girdle muscular dystrophy |
| 193 | MONDO:0012173 | long chain 3-hydroxyacyl-CoA dehydrogenase deficiency |
| 194 | MONDO:0013367 | long QT syndrome 2 |
| 195 | MONDO:0013372 | long QT syndrome 5 |
| 196 | MONDO:0012736 | long QT syndrome 9 |
| 197 | MONDO:0010939 | low phospholipid associated cholelithiasis |
| 198 | MONDO:0019313 | lymphatic malformation |
| 199 | MONDO:0016537 | lymphoproliferative syndrome |
| 200 | MONDO:0005835 | Lynch syndrome |
| 201 | MONDO:0015912 | macrothrombocytopenia and granulocyte inclusions with or without nephritis or sensorineural hearing loss |
| 202 | MONDO:0009020 | macular corneal dystrophy |
| 203 | MONDO:0018493 | malignant hyperthermia of anesthesia |
| 204 | MONDO:0009563 | maple syrup urine disease |
| 205 | MONDO:0007947 | Marfan syndrome |
| 206 | MONDO:0011431 | MASS syndrome |
| 207 | MONDO:0009568 | mast syndrome |
| 208 | MONDO:0007452 | maturity-onset diabetes of the young type 1 |
| 209 | MONDO:0018919 | McCune-Albright syndrome |
| 210 | MONDO:0008721 | medium chain acyl-CoA dehydrogenase deficiency |
| 211 | MONDO:0018868 | metachromatic leukodystrophy |
| 212 | MONDO:0013254 | microcephaly, seizures, and developmental delay |
| 213 | MONDO:0020756 | migraine, familial hemiplegic, 1 |
| 214 | MONDO:0010159 | mismatch repair cancer syndrome 1 |
| 215 | MONDO:0012791 | mitochondrial DNA depletion syndrome, encephalomyopathic form with methylmalonic aciduria |
| 216 | MONDO:0044714 | mitochondrial myopathy-cerebellar ataxia-pigmentary retinopathy syndrome |
| 217 | MONDO:0017575 | mitochondrial neurogastrointestinal encephalomyopathy |
| 218 | MONDO:0009685 | Miyoshi myopathy |
| 219 | MONDO:0009341 | Mowat-Wilson syndrome |
| 220 | MONDO:0009650 | mucolipidosis type II |
| 221 | MONDO:0019249 | mucopolysaccharidosis |
| 222 | MONDO:0001586 | mucopolysaccharidosis type 1 |
| 223 | MONDO:0018937 | mucopolysaccharidosis type 3 |
| 224 | MONDO:0009282 | multiple acyl-CoA dehydrogenase deficiency |
| 225 | MONDO:0007540 | multiple endocrine neoplasia type 1 |
| 226 | MONDO:0008082 | multiple endocrine neoplasia type 2B |
| 227 | MONDO:0018939 | muscle-eye-brain disease |
| 228 | MONDO:0020121 | muscular dystrophy |
| 229 | MONDO:0000171 | muscular dystrophy-dystroglycanopathy, type A |
| 230 | MONDO:0012041 | MUTYH-related attenuated familial adenomatous polyposis |
| 231 | MONDO:0012154 | myopia 6 |
| 232 | MONDO:0016107 | myotonic dystrophy |
| 233 | MONDO:0008056 | myotonic dystrophy type 1 |
| 234 | MONDO:0011266 | myotonic dystrophy type 2 |
| 235 | MONDO:0010794 | NARP syndrome |
| 236 | MONDO:0009735 | Netherton syndrome |
| 237 | MONDO:0016987 | neuroacanthocytosis |
| 238 | MONDO:0009578 | neurocutaneous melanocytosis |
| 239 | MONDO:0018975 | neurofibromatosis type 1 |
| 240 | MONDO:0007039 | neurofibromatosis type 2 |
| 241 | MONDO:0009744 | neuronal ceroid lipofuscinosis 1 |
| 242 | MONDO:0009756 | Niemann-Pick disease type A |
| 243 | MONDO:0018982 | Niemann-Pick disease type C |
| 244 | MONDO:0008060 | nonsyndromic congenital nail disorder 1 |
| 245 | MONDO:0009366 | normal pressure hydrocephalus |
| 246 | MONDO:0017138 | Opitz G/BBB syndrome |
| 247 | MONDO:0008133 | optic atrophy 3 |
| 248 | MONDO:0019019 | osteogenesis imperfecta |
| 249 | MONDO:0017198 | osteopetrosis |
| 250 | MONDO:0011972 | ovarian hyperstimulation syndrome |
| 251 | MONDO:0008195 | paramyotonia congenita of Von Eulenburg |
| 252 | MONDO:0700089 | paroxysmal nonkinesigenic dyskinesia 1 |
| 253 | MONDO:0019631 | persistent hyperplastic primary vitreous |
| 254 | MONDO:0013968 | PGM1-CDG |
| 255 | MONDO:0009861 | phenylketonuria |
| 256 | MONDO:0015643 | photosensitive epilepsy |
| 257 | MONDO:0012589 | Pitt-Hopkins syndrome |
| 258 | MONDO:0008907 | PMM2-CDG |
| 259 | MONDO:0008272 | polysyndactyly 4 |
| 260 | MONDO:0008300 | Prader-Willi syndrome |
| 261 | MONDO:0016575 | primary ciliary dyskinesia |
| 262 | MONDO:0007571 | primary erythermalgia |
| 263 | MONDO:0007572 | primary familial polycythemia due to EPO receptor mutation |
| 264 | MONDO:0002474 | primary hyperoxaluria |
| 265 | MONDO:0009823 | primary hyperoxaluria type 1 |
| 266 | MONDO:0007240 | progressive familial heart block, type 1A |
| 267 | MONDO:0008892 | progressive familial intrahepatic cholestasis type 1 |
| 268 | MONDO:0020074 | progressive myoclonus epilepsy |
| 269 | MONDO:0019037 | progressive supranuclear palsy |
| 270 | MONDO:0011628 | propionic acidemia |
| 271 | MONDO:0019992 | pseudohypoparathyroidism |
| 272 | MONDO:0009329 | pulmonary venoocclusive disease 2 |
| 273 | MONDO:0015597 | pustulosis palmaris et plantaris |
| 274 | MONDO:0019169 | pyruvate dehydrogenase deficiency |
| 275 | MONDO:0010717 | pyruvate dehydrogenase E1-alpha deficiency |
| 276 | MONDO:0009179 | recessive dystrophic epidermolysis bullosa |
| 277 | MONDO:0019200 | retinitis pigmentosa |
| 278 | MONDO:0011137 | retinitis pigmentosa 19 |
| 279 | MONDO:0011272 | retinitis pigmentosa 25 |
| 280 | MONDO:0013395 | retinitis pigmentosa 4 |
| 281 | MONDO:0006952 | retinopathy of prematurity |
| 282 | MONDO:0010726 | Rett syndrome |
| 283 | MONDO:0015776 | rhizomelic chondrodysplasia punctata |
| 284 | MONDO:0008392 | Roussy-Levy syndrome |
| 285 | MONDO:0010006 | Sandhoff disease |
| 286 | MONDO:0009655 | Sanfilippo syndrome type A |
| 287 | MONDO:0011760 | Scheie syndrome |
| 288 | MONDO:0015974 | severe combined immunodeficiency |
| 289 | MONDO:0014168 | severe combined immunodeficiency due to CORO1A deficiency |
| 290 | MONDO:0009549 | severe early-childhood-onset retinal dystrophy |
| 291 | MONDO:0014206 | severe early-onset pulmonary alveolar proteinosis due to MARS deficiency |
| 292 | MONDO:0008722 | short chain acyl-CoA dehydrogenase deficiency |
| 293 | MONDO:0009833 | Shwachman-Diamond syndrome |
| 294 | MONDO:0011382 | sickle cell anemia |
| 295 | MONDO:0008394 | Silver-Russell syndrome |
| 296 | MONDO:0010035 | Smith-Lemli-Opitz syndrome |
| 297 | MONDO:0008165 | southeast Asian ovalocytosis |
| 298 | MONDO:0009672 | spinal muscular atrophy, type III |
| 299 | MONDO:0010056 | spinal muscular atrophy, type IV |
| 300 | MONDO:0007738 | spondyloepiphyseal dysplasia with congenital joint dislocations |
| 301 | MONDO:0019353 | Stargardt disease |
| 302 | MONDO:0008501 | Sturge-Weber syndrome |
| 303 | MONDO:0011959 | sweet syndrome |
| 304 | MONDO:0008919 | systemic primary carnitine deficiency disease |
| 305 | MONDO:0010100 | Tay-Sachs disease |
| 306 | MONDO:0008555 | thrombocytopenia 2 |
| 307 | MONDO:0014837 | thrombocytopenia 6 |
| 308 | MONDO:0012868 | thrombophilia due to protein S deficiency, autosomal dominant |
| 309 | MONDO:0010131 | thyroid hormone resistance, generalized, autosomal recessive |
| 310 | MONDO:0010979 | Timothy syndrome |
| 311 | MONDO:0009383 | transient familial neonatal hyperbilirubinemia |
| 312 | MONDO:0008612 | tuberous sclerosis 1 |
| 313 | MONDO:0013199 | tuberous sclerosis 2 |
| 314 | MONDO:0019499 | Turner syndrome |
| 315 | MONDO:0004739 | urea cycle disorder |
| 316 | MONDO:0010168 | Usher syndrome type 1 |
| 317 | MONDO:0007931 | vitelliform macular dystrophy 2 |
| 318 | MONDO:0008667 | von Hippel-Lindau disease |
| 319 | MONDO:0010200 | Wilson disease |
| 320 | MONDO:0010518 | Wiskott-Aldrich syndrome |
| 321 | MONDO:0010264 | X-linked adrenal hypoplasia congenita |
| 322 | MONDO:0024551 | X-linked lymphoproliferative disease due to SH2D1A deficiency |
| 323 | MONDO:0019609 | Zellweger spectrum disorders |

**Caveats**

- The hereditary classification relies on MONDO's `hereditary disease` (MONDO:0003847) subtree, so a few broad parent terms (e.g., "inborn errors of metabolism," "muscular dystrophy") appear alongside specific diseases.
- The ProKN↔OARD-KG link depends on ProKN's curated MONDO cross-references (`rdfs:seeAlso`) rather than a shared primary identifier.

---

*Created by [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) 0.6.0 on 2026-05-30*

Model: claude-opus-4-8
