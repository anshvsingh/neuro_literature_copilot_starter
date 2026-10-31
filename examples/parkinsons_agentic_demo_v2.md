# Neuro Literature Research Report

**Research question:** Which imaging modalities and machine-learning models are used for Parkinson disease detection, and what limitations affect their clinical application?
**Condition filter:** parkinsons
**Generated:** 2026-10-31 13:50:00
**Evidence passages selected:** 8

## Adaptive research planning and retrieval

The workflow first searched the original question and then used keyword-based coverage checks to decide whether additional searches were needed.

**Planner:** deterministic rule-based coverage checks

**Retrieval rounds:**

- **R1 — Original research question:** 5 passages returned; 4 new unique passages.
  - Query: Which imaging modalities and machine-learning models are used for Parkinson disease detection, and what limitations affect their clinical application?
- **R2 — Targeted methods and modalities search:** 5 passages returned; 2 new unique passages.
  - Query: Which imaging modalities, biomarkers, signal features, datasets, and machine-learning or deep-learning models are reported for Parkinson's disease? Research question: Which imaging modalities and machine-learning models are used for Parkinson disease detection, and what limitations affect their clinical application?
- **R3 — Targeted limitations and validation search:** 5 passages returned; 2 new unique passages.
  - Query: What limitations, validation problems, data leakage risks, dataset biases, generalizability concerns, clinical translation issues, and future research directions are reported for Parkinson's disease? Research question: Which imaging modalities and machine-learning models are used for Parkinson disease detection, and what limitations affect their clinical application?

- **Unique passages collected:** 8
- **Passages included in report:** 8
- **Distinct paper IDs:** 3

**Important:** The planner uses keyword-based coverage checks. Retrieved passages and generated synthesis still require human verification.
## Summary

This report combines retrieved passages with a transparent, rule-based overview of terms and limitations mentioned in those passages. The synthesis is a navigation aid, not an independently verified systematic review or a substitute for reading the full papers.

## Cross-paper overview

The selected evidence contains passages from **3 distinct paper ID(s)**.

- **PAR07:** 2 selected passage(s) (PAR07, p. 2, PAR07, p. 4).
- **PAR08:** 4 selected passage(s) (PAR08, p. 1, PAR08, p. 8, PAR08, p. 7, PAR08, p. 10).
- **PAR02:** 2 selected passage(s) (PAR02, p. 15).

## Imaging modalities mentioned

### Detected modalities

- **MRI (including structural and T1/T2-weighted MRI):** mentioned in PAR08, p. 1, PAR02, p. 15, PAR07, p. 4.
- **SPECT:** mentioned in PAR07, p. 2, PAR07, p. 4.
- **multimodal imaging:** mentioned in PAR02, p. 15, PAR08, p. 8, PAR08, p. 10.

## Machine-learning methods mentioned

### Detected methods

- **Convolutional neural networks (CNNs):** mentioned in PAR07, p. 4.
- **3D CNNs:** mentioned in PAR07, p. 4.
- **AlexNet / transfer learning:** mentioned in PAR07, p. 4.
- **DenseNet:** mentioned in PAR07, p. 4.
- **deep learning (general):** mentioned in PAR07, p. 2, PAR08, p. 1, PAR02, p. 15, PAR08, p. 8.
- **computer-aided diagnosis (CAD):** mentioned in PAR07, p. 2, PAR08, p. 1, PAR08, p. 7.

## Candidate research gaps and limitations

- **Validation and generalizability:** cues found in PAR02, p. 15, PAR08, p. 8, PAR07, p. 4. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Potential data leakage or evaluation concerns:** cues found in PAR07, p. 4. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Clinical translation and routine-use limitations:** cues found in PAR08, p. 1, PAR08, p. 10. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Need to evaluate multimodal approaches:** cues found in PAR02, p. 15, PAR08, p. 8, PAR08, p. 10. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Modality coverage may be incomplete:** cues found in PAR02, p. 15. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.

## Interpretation notes

- A detected term means that it appears in a selected passage; it does not establish that a method is effective or clinically recommended.
- Candidate gaps are inferred from limitations or future-work language in the selected passages, not from a comprehensive review of all 25 PDFs.
- Verify every claim against the complete source paper and its methods/results before using it in academic work.

## Retrieved evidence

### Evidence 1: PAR07

- **Condition:** Parkinson's disease
- **Page:** 2
- **Source file:** data/papers/parkinsons/pd6.pdf
- **Cosine distance:** 0.2482616901397705
- **Review warnings:** None detected

**Retrieved passage:**

(SPECT) (Harisudha et al., 2021). Traditionally, a standardized analysis and detection of such subject images are carried out by specialized technicians and radiologists. Notably, smaller putamen and caudate regions (the dopamine transporters) are observed in the case of PD patients, mainly because of the steady deﬁciency of dopaminergic neurons (Shahed and Jankovic, 2007; Mohammed et al., 2020). In the healthcare industry, machine learning techniques are becoming more prevalent. Machine learning allows an algorithms to learn and extract meaningful representations from data in a semi-automated way, as the term indicates. Machine learning models have been used to diagnose Parkinson’s disease using a variety of data modalities, such as handwriting trends, gait patterns, and neuroimaging methodologies (Dhanalakshmi and Venkatesh, 2016; Matesan et al., 2018; Oláh et al., 2021). Patients with PD who are diagnosed and treated early have decreased chance of progression and perhaps cheaper long- term care expenditures. Computer-Aided Diagnosis models that suﬃciently make use of Artiﬁcial Intelligence (AI) techniques, particularly Deep Learning (DL) methods in the recent past; have suitably specialized as a reliable diagnostic tool (Matesan et al., 2018; Oláh et al., 2021). With the advancement in central processing unit (CPU) and graphics processing unit (GPU), better availability of reliable databases with ease of access in online platforms, and rapid improvisation of learning algorithms (Rumman et al., 2019; Bevilacqua

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 2: PAR08

- **Condition:** Parkinson's disease
- **Page:** 1
- **Source file:** data/papers/parkinsons/pd7.pdf
- **Cosine distance:** 0.294123113155365
- **Review warnings:** None detected

**Retrieved passage:**

of PD in brain MRI. The main challenges in applying ML to medical diagnosis and its implications for PD are also addressed, including current limitations for safe translation into hospitals. These challenges are analyzed at three levels: disease-speciﬁc, task- speciﬁc, and technology-speciﬁc. Finally, potential future directions for each challenge and future perspectives are discussed. KEYWORDS Parkinson’s disease, translational ML, neuroimaging, machine learning, deep learning, computer-aided diagnosis, digital health Introduction Computer-aided diagnosis (CAD) systems based on medical imaging has the potential to assist clinical practice in the diagnosis of Parkinson’s disease (PD). However, the suitability of CAD systems for this application is still being evaluated, and several key aspects must be taken into consideration. The primary objective of CAD systems is not to replace radiologists and clinicians, but to support them in improving the quality and eﬃciency of their diagnoses (Chen et al., 2013). Although CAD systems have been in use for several decades, with successful applications in detecting pulmonary nodules (Xu et al., 1997) and breast cancer (Mangasarian et al., 1995), they were previously reliant on manual feature extraction based on domain knowledge. However, with the recent emergence of Machine Learning (ML) techniques, such as Deep Learning (DL), the automatic extraction of features from imaging data has become possible Frontiers in Aging Neuroscience 01 frontiersin.org

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 3: PAR02

- **Condition:** Parkinson's disease
- **Page:** 15
- **Source file:** data/papers/parkinsons/pd1.pdf
- **Cosine distance:** 0.2998831868171692
- **Review warnings:** None detected

**Retrieved passage:**

15 In conclusion, this study offers a thorough evaluation of deep learning architectures for MRI-based Parkinson's Disease classification, with the novel development and validation of ConvKANs marking a significant advancement in the field. Although MRI is not currently a primary diagnostic tool for PD, our findings demonstrate that with careful model selection and refinement, MRI analysis could become an integral part of a multimodal diagnostic approach. The superior performance of ConvKANs in isolated dataset analyses and the promising generalization of 3D ConvKANs in hold-out testing underscore the potential of this architecture in neuroimaging. However, the observed variability in performance across datasets and between isolated and hold- out analyses highlights the need for robust validation across diverse cohorts to ensure reliability in clinical applications. As personalized medicine advances in the treatment of neurodegenerative disorders, the integration of advanced imaging techniques with clinical expertise offers significant potential to enhance patient outcomes through more accurate diagnosis, prognosis, and treatment planning in PD. Future research should address the limitations identified in this study, particularly by increasing the sample size for 3D analyses, exploring multi-class classification to better represent the full spectrum of parkinsonian disorders, and developing methods to improve the interpretability of deep learning models for use in clinical settings. The promising results of 3D ConvKANs in generalization tasks suggest that future work should

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 4: PAR08

- **Condition:** Parkinson's disease
- **Page:** 8
- **Source file:** data/papers/parkinsons/pd7.pdf
- **Cosine distance:** 0.27147775888442993
- **Review warnings:** None detected

**Retrieved passage:**

of limitations and future directions at the three levels: disease-speciﬁc, task-speciﬁc, and technology-speciﬁc. Limitations Directions Parkinson’s disease Disease heterogeneity Considering subgroups of PD and careful assessment of controls Patients’ comorbidities Large and Long studies and control of unwanted correlations Error rate at diagnosis Acknowledging errors and employing noise-labeled techniques Extended times of disease progression Institutional incentives, importance of consistency in protocols High variability of prodromal markers Multimodal prodromal markers, epigenetics changes Lack of ground truth Objective measures, holistic multidisciplinary approach Clinical brain imaging datasets Complexity of brain imaging Multimodal approach, combination with clinical measures Lack of standardization in acquisition Standardization of acquisition, sharing study assumptions Lack of standardization in preprocessing Sharing raw data and reproducible code ability Lack of standardization in annotation Assisted annotation with guidelines and unsupervised learning Machine learning/deep learning Generalization issues Avoid overﬁtting, control for spurious correlations Algorithmic Bias Acknowledge algorithm bias and prioritize fairness strategies Need for better interpretability Prioritize transparency and ethics, GDPR compliance Model explainability Use explainable ML algorithms, employ interpretability methods Model uncertainty Documentation of uncertainty sources, calibration methods Costly systems to develop and maintain Pre-train models, cloud computing, decentralized ML Security and privacy challenges Proactive security and privacy strategies deﬁned clinically or pathologically (instead of etiologically). PD presents high variability at both prodromal and clinical phases (He et al., 2018). We can

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 5: PAR07

- **Condition:** Parkinson's disease
- **Page:** 4
- **Source file:** data/papers/parkinsons/pd6.pdf
- **Cosine distance:** 0.3100767731666565
- **Review warnings:** None detected

**Retrieved passage:**

Thakur et al. DenseNet Model for PD Classiﬁcation studies. Imaging modalities including MRI (Magnetic Resonance Imaging) and SPECT for detecting PD have raised high interest in research studies. Sivaranjini et al. (Adams et al., 2018) attempted to classify PD and healthy control images from MRI modality by following the architecture of the transfer learning model, AlexNet. This model successfully recognizes the structural diﬀerences in normal and PD subjects and yields optimal results. Chakraborty et al. (Magesh et al., 2020) carried out data pre-processing for 3T T1-Weighted MRI brain scans and designed a 3D CNN model for extracting complex patterns in the brain images of normal and PD cohorts. All studies that employed accuracy in model assessment obtained a diagnostic accuracy above chance values for each research. It’s possible certain data types may not be generalizable enough to forecast how eﬀectively they may help us discriminate between Parkinson’s disease and other Parkinsonian illnesses, but the application of machine learning to many various kinds of data led to great diagnostic accuracy in PD. Data splitting procedures and cross validation were not described despite the great diagnostic accuracy and performance reported in many investigations. When 2D slices are derived from 3D volumes in data modalities like 3D MRI scans, several slices may be created for a single patient. Data leakage and an overestimation

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 6: PAR02

- **Condition:** Parkinson's disease
- **Page:** 15
- **Source file:** data/papers/parkinsons/pd1.pdf
- **Cosine distance:** 0.30159497261047363
- **Review warnings:** None detected

**Retrieved passage:**

classification to better represent the full spectrum of parkinsonian disorders, and developing methods to improve the interpretability of deep learning models for use in clinical settings. The promising results of 3D ConvKANs in generalization tasks suggest that future work should focus on optimizing these 3D implementations for clinical applications, potentially leading to more robust and adaptable AI-assisted diagnostic tools for PD. Methods Dataset Description This study utilized three open-source MRI datasets: the Parkinson's Progression Markers Initiative (PPMI), NEUROCON, and Tao Wu.18,19 Each dataset included both Parkinson's Disease (PD) patients and age-matched healthy control subjects, with varying clinical characteristics across cohorts. The PPMI cohort consisted of newly diagnosed PD patients within two years of diagnosis, none of whom had started PD medication at the time of scanning. A subset of the PPMI dataset was randomly selected to match the sample size and MRI sequences of the other datasets for comparative purposes. Both the NEUROCON and Tao Wu datasets consisted

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 7: PAR08

- **Condition:** Parkinson's disease
- **Page:** 7
- **Source file:** data/papers/parkinsons/pd7.pdf
- **Cosine distance:** 0.3187183737754822
- **Review warnings:** None detected

**Retrieved passage:**

Garcia Santa Cruz et al. 10.3389/fnagi.2023.1216163 FIGURE 3 Summary of the speciﬁc limitations in computer-aided diagnosis (CAD) for Parkinson’s disease (PD) associated with idiosyncrasies of the disease, as addressed in Section Limitations associated with Parkinson’s disease: (1) During the labeling of datasets for supervised learning, several problems can be encountered. (1A) Building a solution for diﬀerential diagnosis can be challenging due to the overlapping symptoms of PD and related disorders. This challenge is especially signiﬁcant during the initial phases of clinical diagnosis, where such solutions would be most useful. (1B) PD is known to have several subtypes with implications for clinical treatment, but there is a lack of clear global consensus, adding another layer of complexity. (2) PD being an age-related disorder, the control subjects used in age-pairing may have additional health conditions or factors that can aﬀect their (Continued) Frontiers in Aging Neuroscience 07 frontiersin.org

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 8: PAR08

- **Condition:** Parkinson's disease
- **Page:** 10
- **Source file:** data/papers/parkinsons/pd7.pdf
- **Cosine distance:** 0.32351547479629517
- **Review warnings:** None detected

**Retrieved passage:**

et al., 2016). As stated by Pagano et al. (2016), “despite signiﬁcant evidence for the utility of neuroimaging in assessing parkinsonian patients, none of the neuroimaging techniques is speciﬁcally recommended for routine use in clinical practice.” Therefore, the impact of this variety is threefold. First, the symptoms may not associate with structural or functional brain patterns. Second, when existing, such patterns require particular brain imaging modalities. Finally, such patterns may not be speciﬁc to PD. On top of these three circumstances, the temporal evolution of the disease adds another layer of complexity. Each stage calls for diﬀerent symptoms, which in turn require dedicated imaging modalities with diﬀerent diagnosis speciﬁcity. In this light, accurate PD subtyping becomes challenging, as obtaining a complete view of the brain manifestations of PD symptoms requires image acquisition of several modalities or the employment of multimodal approaches (Saeed et al., 2017; Chougar et al., 2020; Albrecht et al., 2022). One potential solution to address this issue is to use a combination of multiple imaging techniques. Multimodal approaches can provide a more complete and accurate picture of the disease by capturing diﬀerent aspects of brain function and structure, as well as the density of neurotransmitter receptors such as dopamine receptors. Additionally, clinical assessments can be supplemented by speciﬁc neuropsychological questionnaires or physiological tests, with subsequent conﬁrmation by

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

## Limitations

- Reference detection relies on text-based heuristics and can make mistakes.
- Retrieval relevance does not guarantee factual accuracy or complete coverage.
- The synthesis uses keyword/rule matching; it does not deeply interpret context, resolve contradictions, or prove causal relationships.
- Research gaps are candidates based only on the selected passages and require full-paper review.
