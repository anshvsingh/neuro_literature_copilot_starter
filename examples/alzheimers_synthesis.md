# Neuro Literature Research Report

**Research question:** Which biomarkers, imaging modalities, and machine-learning models are used for Alzheimer's disease detection and prediction?
**Condition filter:** alzheimers
**Generated:** 2026-10-26 23:27:04
**Evidence passages selected:** 8

## Summary

This report combines retrieved passages with a transparent, rule-based overview of terms and limitations mentioned in those passages. The synthesis is a navigation aid, not an independently verified systematic review or a substitute for reading the full papers.

## Cross-paper overview

The selected evidence contains passages from **3 distinct paper ID(s)**.

- **ALZ06:** 3 selected passage(s) (ALZ06, p. 5, ALZ06, p. 1, ALZ06, p. 45).
- **ALZ05:** 2 selected passage(s) (ALZ05, p. 1, ALZ05, p. 10).
- **ALZ01:** 3 selected passage(s) (ALZ01, p. 2, ALZ01, p. 4, ALZ01, p. 1).

## Imaging modalities mentioned

### Detected modalities

- **MRI (including structural and T1/T2-weighted MRI):** mentioned in ALZ06, p. 5, ALZ05, p. 1, ALZ01, p. 2, ALZ01, p. 4, ALZ01, p. 1.
- **CT:** mentioned in ALZ05, p. 10, ALZ01, p. 1.
- **multimodal imaging:** mentioned in ALZ05, p. 10.

## Machine-learning methods mentioned

### Detected methods

- **Convolutional neural networks (CNNs):** mentioned in ALZ06, p. 1, ALZ06, p. 45, ALZ01, p. 1.
- **deep learning (general):** mentioned in ALZ06, p. 5, ALZ06, p. 45, ALZ01, p. 2, ALZ01, p. 1.

## Candidate research gaps and limitations

- **Validation and generalizability:** cues found in ALZ05, p. 10. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Need to evaluate multimodal approaches:** cues found in ALZ05, p. 10. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.

## Interpretation notes

- A detected term means that it appears in a selected passage; it does not establish that a method is effective or clinically recommended.
- Candidate gaps are inferred from limitations or future-work language in the selected passages, not from a comprehensive review of all 25 PDFs.
- Verify every claim against the complete source paper and its methods/results before using it in academic work.

## Retrieved evidence

### Evidence 1: ALZ06

- **Condition:** Alzheimer's disease
- **Page:** 5
- **Source file:** data/papers/alzheimers/az5.pdf
- **Cosine distance:** 0.2768095135688782
- **Review warnings:** None detected

**Retrieved passage:**

1. Introduction Alzheimer's disease (AD), a chronic neurodegenerative disease causing the death of nerve cells and tissue loss throughout the brain, usually starts slowly and worsens over time ​(McKhann et al., 1984)​. AD is expected to affect 1 out of 85 people in the world by the year 2050 ​(Brookmeyer et al., 2007)​. The cost of caring for AD patients is also expected to rise dramatically, thus the need of individual computer-aided systems for early and accurate AD diagnosis. Magnetic resonance imaging (MRI) offers the possibility to study pathological brain changes associated with AD in vivo ​(Ewers et al., 2011)​. Over the past decades, neuroimaging data have been increasingly used to characterize AD by means of machine learning (ML) methods, offering promising tools for individualized diagnosis and prognosis ​(Falahati et al., 2014; Haller et al., 2011; Rathore et al., 2017)​. A large number of studies have proposed to use predefined features (including regional and voxel-based measurements) obtained from image preprocessing pipelines in combination with different types of classifiers, such as support vector machines (SVM) or random forests. Such approach is often referred to as conventional ML ​(LeCun et al., 2015)​. More recently, deep learning (DL), as a newly emerging ML methodology, has made a big leap in the domain of medical imaging ​(Bernal et al., 2018; J. Liu et al.,

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 2: ALZ05

- **Condition:** Alzheimer's disease
- **Page:** 1
- **Source file:** data/papers/alzheimers/az4.pdf
- **Cosine distance:** 0.3238452672958374
- **Review warnings:** None detected

**Retrieved passage:**

around neurons Lakhan et al. [2024]. One of the earliest and most common symptoms of AD is difficulty remembering new information, as the disease often starts in the areas of the brain responsible for learning. Additional symptoms may include behavioral changes, profound confusion about time, events, and places, as well as uncertainty about the identity of family members and friends. These symptoms progress gradually, leading to worsening memory loss and significant challenges with swallowing, speaking, and walking Guo et al. [2022]. Over the past two decades, extensive research has been conducted to detect Alzheimer’s disease (AD) using artificial intelligence techniques. Machine learning algorithms, such as neural networks and support vector machines (SVMs), have been widely applied to analyze brain imaging data, including positron emission tomography (PET) and magnetic resonance imaging (MRI) Kazemi and Houghten [2018]. However, the detection of AD presents significant challenges due to low image quality, issues with brain segmentation and preprocess- ing, the lack of sufficiently large databases, and the inherent complexity of medical images. Effective classification re- quires a robust ability to identify distinguishing features in similar brain images Qin et al. [2022]. A systematic literature review demonstrated that deep learn- ing models consistently outperform traditional machine learn- ing approaches in Alzheimer’s disease detection. Among the 114 studies analyzed, 18 directly compared both paradigms, providing strong

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 3: ALZ06

- **Condition:** Alzheimer's disease
- **Page:** 1
- **Source file:** data/papers/alzheimers/az5.pdf
- **Cosine distance:** 0.3337017297744751
- **Review warnings:** None detected

**Retrieved passage:**

Convolutional Neural Networks for Classification of Alzheimer’s Disease: Overview and Reproducible Evaluation Junhao Wen​a,b,c,d,e*​, Elina Thibeau-Sutre​a,b,c,d,e*​, Mauricio Diaz-Melo​e,a,b,c,d​, Jorge Samper-González​e,a,b,c,d​, Alexandre Routier​e,a,b,c,d​, Simona Bottani​e,a,b,c,d​, Didier Dormont​e,a,b,c,d,f​, Stanley Durrleman​e,a,b,c,d​, Ninon Burgos​a,b,c,d,e​, Olivier Colliot​a,b,c,d,e,f,g,†​ , for the Alzheimer’s Disease Neuroimaging Initiative and the Australian Imaging Biomarkers and Lifestyle flagship study of 1 ageing 2 a​Institut du Cerveau et de la Moelle épinière, ICM, F-75013, Paris, France b​Sorbonne Université, F-75013, Paris, France c​Inserm, U 1127, F-75013, Paris, France d​CNRS, UMR 7225, F-75013, Paris, France e​Inria, Aramis project-team, F-75013, Paris, France f​AP-HP, Hôpital de la Pitié Salpêtrière, Department of Neuroradiology, F-75013, Paris, France g​AP-HP, Hôpital de la Pitié Salpêtrière, Department of Neurology, F-75013, Paris, France *denotes shared first authorship †​Corresponding author: Olivier Colliot, PhD - ​olivier.colliot@upmc.fr ICM – Brain and Spinal Cord Institute ARAMIS team Pitié-Salpêtrière Hospital 47-83, boulevard de l’Hôpital, 75651 Paris Cedex 13, France 1 Data used in preparation of this article were obtained from the Alzheimer’s Disease Neuroimaging Initiative (ADNI) database (adni.loni.usc.edu). As such, the investigators within the ADNI contributed to the design and implementation of ADNI and/or provided data but did not participate in analysis or writing of this report. A complete listing of ADNI investigators can be found at: http://adni.loni.usc.edu/wp-content/uploads/how_to_apply/ADNI_Acknowledgement_List.pdf 2 Data used in the preparation of this article was obtained from the Australian Imaging Biomarkers and Lifestyle flagship

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 4: ALZ06

- **Condition:** Alzheimer's disease
- **Page:** 45
- **Source file:** data/papers/alzheimers/az5.pdf
- **Cosine distance:** 0.34196019172668457
- **Review warnings:** None detected

**Retrieved passage:**

Convolutional Neural Networks for Classification of Alzheimer’s Disease: Overview and Reproducible Evaluation Supplementary Material Junhao Wen​a,b,c,d,e*​, Elina Thibeau-Sutre​a,b,c,d,e*​, Mauricio Diaz-Melo​e,a,b,c,d​, Jorge Samper-González​e,a,b,c,d​, Alexandre Routier​e,a,b,c,d​, Simona Bottani​e,a,b,c,d​, Didier Dormont​e,a,b,c,d,f​, Stanley Durrleman​e,a,b,c,d​, Ninon Burgos​a,b,c,d,e​, Olivier Colliot​a,b,c,d,e,f,g,†​ , for the Alzheimer’s Disease Neuroimaging Initiative and the Australian Imaging Biomarkers and Lifestyle flagship study of ageing a​Institut du Cerveau et de la Moelle épinière, ICM, F-75013, Paris, France b​Sorbonne Université, F-75013, Paris, France c​Inserm, U 1127, F-75013, Paris, France d​CNRS, UMR 7225, F-75013, Paris, France e​Inria, Aramis project-team, F-75013, Paris, France f​AP-HP, Hôpital de la Pitié Salpêtrière, Department of Neuroradiology, F-75013, Paris, France g​AP-HP, Hôpital de la Pitié Salpêtrière, Department of Neurology, F-75013, Paris, France *denotes shared first authorship We present additional methodological explanations, tables and figures in this supplementary material. More specifically, we first present in detail the methodology of our literature review (eMethod 1) and a brief introduction of the involved topics, namely deep learning, image preprocessing and AD (eMethod 2). We then describe the datasets used in our study in eMethod 3. From eTable1 to eTable3, we present the architecture hyperparameters for the chosen models. The training hyperparameters for autoencoder pre-training and classification are shown in eTable 4 and eTable 5, respectively. Lastly, the monitoring of training process, including the display of the training/validation loss and accuracy, is presented from eFigure

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 5: ALZ05

- **Condition:** Alzheimer's disease
- **Page:** 10
- **Source file:** data/papers/alzheimers/az4.pdf
- **Cosine distance:** 0.3615031838417053
- **Review warnings:** None detected

**Retrieved passage:**

from binary to multiclass classification to distinguish between various stages of Alzheimer’s Disease progression. We also propose the integration of heteroge- neous data sources and multimodal fusion (e.g., PET and CT scans) to improve model generalizability. Furthermore, we will explore Federated Learning (FL) to facilitate multi-institutional collaboration while maintaining strict patient privacy. Finally, we intend to investigate en- semble learning strategies and collaborate with neuroscience specialists to ensure that the learned features align with estab- lished clinical biomarkers, ultimately improving the stability and diagnostic accuracy of the proposed models. Declarations Authors’ Contributions Augusto Berwaldt de Oliveira conducted the research, developed the methodology, and carried out the experiments and data analy- sis. Claudio Resin Geyer contributed by revising the manuscript and providing critical feedback throughout the development of the work. All authors participated in the conception of the approach and approved the final version of the manuscript. . Competing interests The authors declare that they have no competing interests. Acknowledgements Data collection and sharing for this project were funded by the Alzheimer’s Disease Neuro- imaging Initiative (ADNI), National Institutes of Health (Grant No. U01 AG024904), and DOD ADNI (Department of Defense Award No. W81XWH-12-2-0012). ADNI is funded by the National Institute on Aging (NIA), the National Insti- tute of Biomedical Imaging and Bioengineering (NIBIB), and gener- ous contributions from the following:

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 6: ALZ01

- **Condition:** Alzheimer's disease
- **Page:** 2
- **Source file:** data/papers/alzheimers/az.pdf
- **Cosine distance:** 0.3659132719039917
- **Review warnings:** None detected

**Retrieved passage:**

MCI subjects who converted to dementia according to the DSM-IV criteria during the follow-up [8], sMCI is defined when the subjects do not fulfill the criteria. Identification between pMCI and sMCI plays an important role for the early diagnosis of dementia, which can assist clinicians to propose effective therapeutical interventions of the disease process [9]. This work aims at differentiating AD or potential AD patients from normal subjects accurately and automatically using medical images around the hippocampal area and recent technologies in deep learning. This facilitates a fast-preclinical diagnosis. The method is further extended for the classification between sMCI and pMCI so that an early diagnosis of dementia would be possible. In our proposed method, multi-modality data were used. We used two modalities in our experiments including the T1-weighted MRI and 18F-FDG-PET. Up to now, numerous studies have been published on diagnosing AD by utilizing T1 MRI Sorensen et al. segmented the brains and extracted features like the thicknesses of cortices and volumes of tissues in the selected regions of interest (ROIs) [10]. After that they used linear discriminant analysis (LDA) to classify AD, MCI and normal (NL), and achieved 63.0% classification accuracy on the CADDementia dataset. David et al., implemented kernel metric learning in classification [11]. Based on the segmentation results provided by FreeSurfer, morphological features like cortical volume,

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 7: ALZ01

- **Condition:** Alzheimer's disease
- **Page:** 4
- **Source file:** data/papers/alzheimers/az.pdf
- **Cosine distance:** 0.3698316812515259
- **Review warnings:** None detected

**Retrieved passage:**

work. 2. Material In this section, we presented the multi-modality image datasets that were used in this study, the data pre-processing methods. MRI and PET are two essential modalities that are widely used for AD diagnosis. Biomarkers of Alzheimer’s disease (AD) extracted from MRIs is an active research area, whose importance in AD was underlined by its inclusion in criteria for AD diagnosis. In particular, the decrease of hippocampal volume is one of the best-established biomarkers used in research studies to stage the progression of Alzheimer's disease (AD) pathology in the brain of patients across the spectrum of the disease [25]. Therefore, the hippocampi are the most studied region of AD, which are so far the only MRI biomarker that has been qualified for enrichment of clinical trials [26]. For PET images, published studies indicate that AD may cause the decline of 18-Fluoro- DeoxyGlucose (FDG) uptake in the temporoparietal cortex, as well as brain atrophy in the medial, basal, lateral temporal lobes, the medial and lateral parietal cortices. As a result, the ROI of metabolic changes in cortices, especially temporal lobes with FDG biomarkers may help AD diagnosis [27,28,29]. When dealing with PET images, we tried different ROIs containing hippocampi and cortices. 2.1 Image Acquisition The datasets we used in this work were downloaded from the Alzheimer’s Disease Neuroimaging Initiative

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 8: ALZ01

- **Condition:** Alzheimer's disease
- **Page:** 1
- **Source file:** data/papers/alzheimers/az.pdf
- **Cosine distance:** 0.37535035610198975
- **Review warnings:** None detected

**Retrieved passage:**

images using the ADNI datasets, including 731 Normal (NL) subjects, 647 AD subjects, 441 stable MCI (sMCI) subjects and 326 progressive MCI (pMCI) subjects. We obtained the maximal accuracies of 90.10% for NL/AD task, 87.46% for NL/pMCI task, and 76.90% for sMCI/pMCI task. The proposed framework yields comparative results against state-of-the-art approaches. Moreover, the experimental results have demonstrated that (1) segmentation is not a prerequisite by using CNN, (2) the hippocampal area provides enough information to give a reference to AD diagnosis. Keywords: Alzheimer’s Disease, Multi-modality, Image Classification, CNN, Deep Learning, Hippocampal 1. Introduction The aging of global population results in increasing number of people with dementia. Recent studies indicate 50 million people are living with dementia [1], of whom 60%-70% have Alzheimer’s Disease (AD) [2]. Known as one of the most common neurodegenerative diseases, AD can result in severe cognitive impairment and behavior issue. With the progression of AD, the structure and metabolic rate of the brain change. The phenotype includes the shrinkage of cerebral cortices and hippocampi, the enlargement of ventricles, and the change of regional glucose uptake. These changes can be quantified with the help of medical imaging techniques such as magnetic resonance imaging (MRI), positron-emission tomography (PET) and computed tomography (CT) [3]. For instance, T1-weighted MRI provides high-

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

## Limitations

- Reference detection relies on text-based heuristics and can make mistakes.
- Retrieval relevance does not guarantee factual accuracy or complete coverage.
- The synthesis uses keyword/rule matching; it does not deeply interpret context, resolve contradictions, or prove causal relationships.
- Research gaps are candidates based only on the selected passages and require full-paper review.
