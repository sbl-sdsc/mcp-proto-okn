# PFOA ToxCast Analysis - Chat Transcript

## Query 1: 

> Which biological targets does perfluorooctanoic acid (PFOA) interact with?

### Analysis Process
I searched the ToxCast database (biobricks-toxcast knowledge graph) to identify all biological targets that PFOA has been tested against.

### Database Information
- **Chemical Identified**: Perfluorooctanoic acid (DTXSID8031865)
- **Total Assays**: 1,396 different assays
- **Data Source**: EPA ToxCast InvitroDB

### Biological Targets and Pathways

#### Nuclear Receptors
- **Androgen Receptor (AR)** - agonist and antagonist activities
- **Estrogen Receptors (ERα, ERβ)** - multiple assays in human and various species
- **Peroxisome Proliferator-Activated Receptors (PPARα, PPARγ, PPARδ)**
- **Thyroid Hormone Receptors (TRα, TRβ)**
- **Glucocorticoid Receptor (GR)**
- **Progesterone Receptor (PR)**
- **Retinoic Acid Receptors (RARα, RARβ, RARγ)**
- **Retinoid X Receptors (RXRα, RXRβ)**
- **Liver X Receptors (LXRα, LXRβ)**
- **Farnesoid X Receptor (FXR)**
- **Vitamin D Receptor (VDR)**
- **Constitutive Androstane Receptor (CAR)**
- **Pregnane X Receptor (PXR)**
- **Estrogen-Related Receptors (ERRα, ERRγ)**

#### Transcription Factors & Signaling Pathways
- **Aryl Hydrocarbon Receptor (AhR)**
- **p53 tumor suppressor**
- **NF-κB (nuclear factor kappa B)**
- **AP-1 (activator protein 1)**
- **STAT3**
- **HIF-1α (hypoxia-inducible factor)**
- **Nrf2/ARE (antioxidant response element)**

#### Metabolic Enzymes
- **Cytochrome P450 enzymes**: CYP1A1, CYP1A2, CYP2B6, CYP2C9, CYP2C19, CYP2C8, CYP2E1, CYP3A4, CYP3A5, CYP3A7, CYP4A11, CYP7A1, CYP19A1
- **UDP-glucuronosyltransferases**: UGT1A1, UGT1A6
- **Sulfotransferases**: SULT2A1
- **Glutathione S-transferases**: GSTA2, GSTM3

#### Transporters
- **ABC transporters**: ABCB1/P-glycoprotein, ABCB11, ABCC2, ABCC3, ABCG2
- **Organic anion transporters**: SLCO1B1/OATP1B1, SLC22A1

#### Cell Signaling & Kinases
- Multiple protein kinases (AKT1, AKT2, GSK3β, PI3Kα, protein kinase A, various MAPKs)
- Protein phosphatases (PPP1CA, PPP2CA, PTEN, PTPN1, PTPN2, etc.)

#### Inflammatory & Immune Markers
- Cytokines and chemokines (IL-6, IL-8, IL-1α, TNFα, MCP-1, MIG, etc.)
- Adhesion molecules (ICAM-1, VCAM-1, E-selectin)
- Matrix metalloproteinases (MMP1, MMP3, MMP9, MMP10)

#### Cellular Stress & Toxicity Markers
- Cell viability and cytotoxicity
- Apoptosis markers (caspases, BAX, BCL2)
- DNA damage (H2AX phosphorylation)
- Mitochondrial function
- Oxidative stress markers

---

## Query 2: 

> Which of these assays have a positive result?

### Results Summary
**147 out of 1,396 assays showed positive results** (hitcall = 1.0)

### Key Positive Findings by Category

#### 1. Estrogen Receptor Activity (Strong Signal)
**ERα (Estrogen Receptor Alpha)** - Multiple positive hits across species:
- ATG_ERa_TRANS_up
- ATG_ERE_CIS_up (Estrogen Response Element)
- ATG_hERa_EcoTox2_up
- ATG_hERa_XSP2_up
- ATG_chERa_XSP2_up (chicken)
- ATG_frER1_EcoTox2_up (fathead minnow)
- ATG_frER1_XSP2_up (fathead minnow)
- ATG_frER2_XSP2_up (fathead minnow)
- ATG_trERa_XSP2_up (trout)
- ATG_zfER2a_XSP2_up (zebrafish)
- ATG_zfER2b_XSP2_up (zebrafish)
- TOX21_ERa_BLA_Antagonist_ch2
- TOX21_ERa_BLA_Antagonist_ratio

**ERβ (Estrogen Receptor Beta)**:
- ATG_hERb_XSP2_up
- TOX21_ERb_BLA_Agonist_viability
- TOX21_ERb_BLA_Antagonist_ratio
- TOX21_ERb_BLA_Antagonist_viability

**ERR (Estrogen-Related Receptor)**:
- TOX21_ERR_Antagonist

#### 2. PPAR (Peroxisome Proliferator-Activated Receptor) Activation (Very Strong Signal)

**PPARα** - Multiple species:
- ATG_PPARa_TRANS_up
- ATG_hPPARa_EcoTox2_up (human)
- ATG_frPPARa_EcoTox2_up (fathead minnow)
- ATG_jmPPARa_EcoTox2_up (Japanese medaka)
- ATG_rtPPARa_EcoTox2_up (rat)
- ATG_zfPPARa_EcoTox2_up (zebrafish)
- ATG_PPRE_CIS_up (PPAR Response Element)

**PPARγ**:
- ATG_PPARg_TRANS_up
- ATG_hPPARg_EcoTox2_up
- ATG_hPPARg_XSP2_up
- ATG_jmPPARg_EcoTox2_up (Japanese medaka)
- ATG_mPPARg_XSP2_up (mouse)
- NVS_NR_hPPARg
- TOX21_PPARg_BLA_antagonist_ratio

**PPARδ**:
- TOX21_PPARd_BLA_agonist_ratio
- TOX21_PPARd_BLA_Antagonist_ch2
- TOX21_PPARd_BLA_antagonist_ratio

#### 3. RXR (Retinoid X Receptor) Activation
- ATG_RXRb_TRANS_up
- ATG_hRXRb_EcoTox2_up (human)
- ATG_frRXRb_EcoTox2_up (fathead minnow)
- ATG_jmRXRb_EcoTox2_up (Japanese medaka)
- TOX21_RXR_BLA_Agonist_ratio

#### 4. Hepatic Gene Expression Changes (Liver Effects)

**Drug Metabolizing Enzymes**:
- LTEA_HepaRG_CYP1A1_up
- LTEA_HepaRG_CYP2B6_up
- LTEA_HepaRG_CYP2C19_up
- LTEA_HepaRG_CYP2C8_up
- LTEA_HepaRG_CYP2E1_up
- LTEA_HepaRG_CYP3A7_up
- LTEA_HepaRG_CYP4A11_up
- LTEA_HepaRG_CYP4A22_up
- CLD_CYP2B6_24hr
- CLD_GSTA2_48hr

**Transporters**:
- LTEA_HepaRG_ABCC2_up
- LTEA_HepaRG_ABCC3_up

**Phase II Enzymes**:
- LTEA_HepaRG_UGT1A1_up
- LTEA_HepaRG_SULT2A1_up

**Lipid Metabolism**:
- LTEA_HepaRG_ACLY_up (ATP citrate lyase)
- LTEA_HepaRG_ACOX1_up (acyl-CoA oxidase)
- LTEA_HepaRG_FABP1_up (fatty acid binding protein)
- LTEA_HepaRG_FASN_up (fatty acid synthase)
- LTEA_HepaRG_HMGCS2_up (HMG-CoA synthase)
- LTEA_HepaRG_PDK4_up (pyruvate dehydrogenase kinase)
- CLD_HMGCS2_48hr

**Stress Response & Other Hepatic Genes**:
- LTEA_HepaRG_DDIT3_up (DNA damage-inducible transcript 3)
- LTEA_HepaRG_GADD45B_up (growth arrest and DNA damage)
- LTEA_HepaRG_GADD45G_up
- LTEA_HepaRG_NFE2L2_up (Nrf2)
- LTEA_HepaRG_XBP1_up (X-box binding protein 1)
- LTEA_HepaRG_CAT_up (catalase)
- LTEA_HepaRG_FMO3_up (flavin-containing monooxygenase)
- LTEA_HepaRG_FOXO3_up
- LTEA_HepaRG_IL6R_up (IL-6 receptor)
- LTEA_HepaRG_SDHB_up (succinate dehydrogenase)
- LTEA_HepaRG_TGFA_up (transforming growth factor alpha)
- LTEA_HepaRG_ALPP_dn (alkaline phosphatase, decreased)
- LTEA_HepaRG_CDKN1A_dn (p21, decreased)
- LTEA_HepaRG_THRSP_dn (thyroid hormone responsive, decreased)

#### 5. Thyroid Hormone Disruption

**Thyroid Receptor Antagonism**:
- ATG_hTRa_XSP2_dn (downregulation)
- ATG_THRa1_TRANS_dn

**Thyroid Transport Protein**:
- CCTE_GLTED_hTTR_dn (reduced transthyretin binding)

#### 6. Oxidative Stress & Antioxidant Response
- ATG_NRF2_ARE_CIS_up (Nrf2/ARE pathway activation)
- LTEA_HepaRG_CAT_up (catalase)
- TOX21_ARE_BLA_Agonist_ch2
- TOX21_ARE_BLA_agonist_ratio

#### 7. Neurotoxicity

**Reduced Cell Viability & Neurite Outgrowth**:
- UKN4_HCS_LUHMES_cell_viability_dn
- UKN4_HCS_LUHMES_neurite_outgrowth_dn
- UKN5_HCS_SBAD2_cell_viability_dn
- UKN5_HCS_SBAD2_neurite_outgrowth_dn
- IUF_NPC1a_proliferation_BrdU_72hr_dn

**Neuronal Network Activity (MEA assays)**:
- CCTE_Shafer_MEA_dev_network_spike_duration_std_dn
- CCTE_Shafer_MEA_dev_network_spike_peak_dn
- CCTE_Shafer_MEA_dev_per_network_spike_spike_percent_up
- CCTE_Shafer_MEA_dev_spike_duration_mean_dn

#### 8. Inflammatory Responses

**Cytokines & Chemokines**:
- BSK_3C_IL8_up
- BSK_IMphg_IL8_up
- BSK_LPS_IL8_up
- BSK_BT_xTNFa_up
- BSK_LPS_TNFa_down
- BSK_CASM3C_MIG_up
- BSK_BF4T_MCP1_down
- BSK_4H_Eotaxin3_down
- BSK_4H_Eotaxin3_up
- BSK_LPS_MCSF_up
- BSK_IMphg_IL10_down

**Matrix Metalloproteinases**:
- BSK_BE3C_MMP1_up
- BSK_BE3C_MMP9_up

**Adhesion Molecules & Other Inflammatory Markers**:
- BSK_3C_uPAR_down
- BSK_3C_VCAM1_down
- BSK_4H_uPAR_down
- BSK_KF3CT_ICAM1_down
- BSK_KF3CT_PAI1_down
- BSK_LPS_Eselectin_up
- BSK_LPS_Thrombomodulin_up
- BSK_BE3C_IP10_down
- BSK_BF4T_tPA_down

#### 9. Cell Proliferation & Cytotoxicity

**Increased Proliferation**:
- BSK_BT_Bcell_Proliferation_up
- BSK_CASM3C_Proliferation_up
- BSK_hDFCGF_Proliferation_up

**Cytotoxicity & Cell Viability**:
- BSK_BT_PBMCCytotoxicity_up
- BSK_3C_SRB_down (reduced viability)
- APR_HepG2_CellLoss_72h_dn
- TOX21_RT_HEPG2_GLO_00hr_ctrl_viability

**Mitochondrial & Cellular Effects**:
- APR_HepG2_MitoMembPot_72h_dn (mitochondrial membrane potential disruption)
- APR_HepG2_MicrotubuleCSK_72h_up
- TOX21_MMP_fitc
- BSK_MyoF_CollagenIV_up

#### 10. Other Nuclear Receptor & Transcription Factor Effects

**Nuclear Receptors**:
- NVS_NR_hCAR_Antagonist (CAR antagonism)
- ATG_PXRE_CIS_up (PXR activation)
- ATG_NURR1_TRANS_up

**Transcription Factors**:
- ATG_AP_1_CIS_up (AP-1)
- ATG_Sp1_CIS_up (Sp1)
- ATG_p53_CIS_dn (p53, decreased)
- ATG_TCF_b_cat_CIS_dn (Wnt/β-catenin, decreased)
- ATG_DR4_LXR_CIS_dn (LXR, decreased)
- ATG_ISRE_CIS_dn (interferon-stimulated response element, decreased)
- ATG_RORE_CIS_dn (ROR response element, decreased)

#### 11. Enzyme & Receptor Binding

**Enzymes**:
- NVS_ADME_rCYP2A2
- NVS_ADME_rCYP2C11_Activator
- NVS_ENZ_hACP1 (acid phosphatase)
- NVS_ENZ_hBACE (beta-secretase)
- NVS_ENZ_hPI3Ka (phosphoinositide 3-kinase)
- NVS_ENZ_hPPP1CA (protein phosphatase 1)
- NVS_ENZ_hPPP2CA (protein phosphatase 2)
- NVS_ENZ_hTie2 (tyrosine kinase)

**GPCRs**:
- NVS_GPCR_gLTB4 (leukotriene B4 receptor)
- NVS_GPCR_hAdoRA2a (adenosine A2a receptor)
- NVS_GPCR_hLTB4_BLT1 (leukotriene B4 receptor)

#### 12. Additional Cellular Effects
- BSK_hDFCGF_EGFR_down (EGFR downregulation)
- BSK_LPS_PGE2_down (prostaglandin E2 reduction)

---

## Summary of Toxicological Profile

Based on the 147 positive assay results, PFOA demonstrates:

### Primary Mechanisms of Action
1. **Endocrine Disruption**: Strong estrogenic and anti-estrogenic activity; thyroid hormone disruption
2. **PPAR Agonism**: Potent activation of PPARα and PPARγ pathways across multiple species
3. **Metabolic Disruption**: Induction of hepatic drug-metabolizing enzymes and alterations in lipid metabolism
4. **Oxidative Stress Induction**: Activation of Nrf2/ARE antioxidant response pathways
5. **Neurotoxicity**: Reduced neuronal cell viability and neurite outgrowth
6. **Immunomodulation**: Effects on inflammatory cytokines and immune cell function

### Biological Systems Affected
- **Liver**: Extensive changes in metabolic enzyme expression and lipid metabolism
- **Endocrine System**: Multiple hormone receptor pathways disrupted
- **Nervous System**: Neurotoxic effects and altered neuronal network activity
- **Immune System**: Inflammatory cytokine modulation
- **Cellular Function**: Mitochondrial dysfunction, oxidative stress, altered proliferation

### Toxicological Significance
These findings are consistent with known PFOA health concerns including:
- Liver toxicity and metabolic disease
- Endocrine disruption (reproductive and thyroid effects)
- Developmental neurotoxicity
- Immune system dysfunction
- Potential carcinogenic effects (p53 pathway disruption)

---

## Technical Notes

**Database**: EPA ToxCast/Tox21 InvitroDB via BioBricks knowledge graph
**Chemical ID**: DTXSID8031865 (Perfluorooctanoic acid)
**CAS Number**: 335-67-1
**Total Assays**: 1,396
**Positive Hits**: 147 (10.5% hit rate)
**Data Format**: SPARQL queries against RDF knowledge graph

---

*Analysis completed: December 11, 2025*
