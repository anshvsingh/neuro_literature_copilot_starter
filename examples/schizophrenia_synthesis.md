# Neuro Literature Research Report

**Research question:** Which biomarkers, neuroimaging methods, and machine-learning models are used for schizophrenia detection and classification?
**Condition filter:** schizophrenia
**Generated:** 2026-10-26 23:31:21
**Evidence passages selected:** 8

## Summary

This report combines retrieved passages with a transparent, rule-based overview of terms and limitations mentioned in those passages. The synthesis is a navigation aid, not an independently verified systematic review or a substitute for reading the full papers.

## Cross-paper overview

The selected evidence contains passages from **4 distinct paper ID(s)**.

- **SCH02:** 3 selected passage(s) (SCH02, p. 1, SCH02, p. 5, SCH02, p. 7).
- **SCH03:** 2 selected passage(s) (SCH03, p. 1, SCH03, p. 3).
- **SCH04:** 1 selected passage(s) (SCH04, p. 2).
- **SCH05:** 2 selected passage(s) (SCH05, p. 1, SCH05, p. 2).

## Imaging modalities mentioned

### Detected modalities

- **MRI (including structural and T1/T2-weighted MRI):** mentioned in SCH03, p. 1, SCH04, p. 2, SCH05, p. 1, SCH03, p. 3, SCH05, p. 2.
- **diffusion tensor imaging (DTI):** mentioned in SCH04, p. 2.

## Machine-learning methods mentioned

### Detected methods

- **Convolutional neural networks (CNNs):** mentioned in SCH03, p. 3.
- **3D CNNs:** mentioned in SCH03, p. 3.

## Candidate research gaps and limitations

- **Validation and generalizability:** cues found in SCH03, p. 1, SCH02, p. 5, SCH02, p. 7, SCH03, p. 3. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.
- **Potential data leakage or evaluation concerns:** cues found in SCH03, p. 3. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.

## Interpretation notes

- A detected term means that it appears in a selected passage; it does not establish that a method is effective or clinically recommended.
- Candidate gaps are inferred from limitations or future-work language in the selected passages, not from a comprehensive review of all 25 PDFs.
- Verify every claim against the complete source paper and its methods/results before using it in academic work.

## Retrieved evidence

### Evidence 1: SCH02

- **Condition:** Schizophrenia
- **Page:** 1
- **Source file:** data/papers/schizophrenia/sz1.pdf
- **Cosine distance:** 0.2886825203895569
- **Review warnings:** None detected

**Retrieved passage:**

Other studies also affirm the enlargement of ventricles in ­schizophrenia3,4. While gray matter reductions are most consistently reported in the subcortical regions, reductions have also been identified in areas such as the prefrontal, temporal, cingulate, and cerebellar ­cortices5,6. Loss of gray matter volume has been shown to not only mark the onset of schizophrenia but also progress alongside the ­illness7. Despite these documented changes, accurate and rapid detection of schizophrenia remains a pressing prob- lem; previous studies are limited to only characterizing structural abnormalities at a group level, with no concrete method to make individual diagnoses at a subject level. Additionally, the diagnosis of schizophrenia based on DSM-5 criteria is costly both in terms of time and resources, without ensuring objectivity. Therefore, it is impera- tive to develop an objective screening tool to diagnose schizophrenia and potentially improve patient prognosis by allowing for earlier intervention. Various attempts have been proposed to take advantage of the structural alterations present in schizophrenia for classification using neuroimaging data. Machine learning algorithms have historically presented the ability OPEN 1Department of Biomedical Engineering, Columbia University, New York, NY, USA. 2Department of Applied Mathematics, Columbia University, New York, NY, USA. 3Department of Psychiatry, Columbia University, New York, NY, USA. 4The Mortimer B. Zuckerman Mind Brain Behavior Institute, Columbia University, New York, NY, USA. 5Department of Radiology,

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 2: SCH03

- **Condition:** Schizophrenia
- **Page:** 1
- **Source file:** data/papers/schizophrenia/sz2.pdf
- **Cosine distance:** 0.29804617166519165
- **Review warnings:** None detected

**Retrieved passage:**

identifying patients with schizophrenia using 3D brain MR images and paved the way for imaging-based individual-level diagnosis and prognosis in psychiatric disorders. I. INTRODUCTION Schizophrenia is a severe chronic mental disorder that causes great burdens to patients’ families and society. Yet, diagnosis of schizophrenia is typically based on interview and clinical symptoms, which could be challenged by the complex and heterogeneous symptoms as well as many confounders such as the race, gender, and medication effects[1]–[3]. Early and accurate diagnosis of schizophrenia could facilitate treatment planning and improve the outcome of the illness. Instead of classical group-level comparisons, machine learning based on objective biomarkers such as medical imaging could help to establish a psychiatric diagnosis at the individual level. Indeed, previous work on computer-aided classification of schizophrenia patients and controls using brain structural magnetic resonance imaging (MRI) mainly involve handcrafted feature-based machine learning approaches such as support vector machine (SVM), random forest (RF), and logistic regression (LR). MRI-based features include region- or voxel-specific cortical thickness and gray matter volume *Research supported by Institute of Health Technology, Nanyang Technological University, Singapore, Singapore M. Hu, C. Guan and X. Jiang are with Nanyang Technological University, Singapore, Singapore (email: hume0004@e.ntu.edu.sg) density in the brain [4]–[9]. However, many studies suffer from poor replicability and generalizability due to small sample sizes and hyper parameter settings. The

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 3: SCH04

- **Condition:** Schizophrenia
- **Page:** 2
- **Source file:** data/papers/schizophrenia/sz3.pdf
- **Cosine distance:** 0.34244662523269653
- **Review warnings:** None detected

**Retrieved passage:**

Neural Network World 3/2022, 147–161 the exact method of diagnosing schizophrenia disorder [2]. Although psychiatrists generally diagnose schizophrenia based on the history of the disease and mental status examination [3], many researchers have recently attempted to provide the basis for automated diagnosis of schizophrenia. Most of these studies have utilized extracted features of neuroimaging data along with machine learning techniques [4]. For instance, Ardekani et al. [5] derived fractional anisotropy (FA) and mean diffu- sivity (MD) maps from diffusion tensor imaging (DTI) data. They applied Fisher’s linear discriminant analysis (LDA) as a classifier method. Chyzhyk et al. [6] used resting-state functional magnetic resonance imaging (rs-fMRI) data and extracted functional connectivity (FC) measures, regional homogeneity (ReHo), and frac- tional amplitude of low-frequency fluctuations (fALFF) as derived features from them. Their proposed approach is consists of dimensional reduction, feature selec- tion, and classification with SVM steps. In contrast to the methods that have used single neuroimaging modality, some studies have suggested using multi-modal neu- roimaging data [7]. Although these methods may require additional time, cost, and information, they achieved higher accuracy because of the use of comple- mentary data. Cetin et al. [8] used fMRI and magnetoencephalography (MEG) data and derived static and dynamic functional network connectivity (FNC) from them to diagnose schizophrenia patients from healthy controls. Their experiments showed that combined

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 4: SCH02

- **Condition:** Schizophrenia
- **Page:** 5
- **Source file:** data/papers/schizophrenia/sz1.pdf
- **Cosine distance:** 0.35382330417633057
- **Review warnings:** None detected

**Retrieved passage:**

5 Vol.:(0123456789) Scientific Reports | (2023) 13:14433 | https://doi.org/10.1038/s41598-023-41359-z www.nature.com/scientificreports/ the model-generated classification and the ground truth labels. The ROC curves, one for each trained classifi- cation model, represent the classification performances at each potential numerical threshold to binarize the predicted schizophrenia likelihood score. The sensitivity and specificity (the sum of which peaks at the operat- ing point), as well as the area under the ROC curve (AUC), demonstrate the effectiveness of the classification method. The significance of the difference among these ROC curves was calculated using DeLong’s ­test30. Generalization evaluation of the model. To demonstrate the generalization of the models, data from COBRE and NMorphCH studies were selected to train the model, and data from BrainGluSchi with a nearly similar acquisition configuration was used for evaluating the capability of model generalization. The same train- ing strategies and hyperparameter settings were maintained in the experiment. Explainability of the model with grad‑CAM. To validate the models, a gradient class activation map (Grad-CAM) was introduced to our experiment to check whether the model focuses on task-related patterns instead of some irrelevant information in the data. After excluding the possibility of the model focusing on meaningless regions in the data by applying a rough brain mask, we further investigated the brain regions that had the most contributions to the schizophrenia classification task by

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 5: SCH05

- **Condition:** Schizophrenia
- **Page:** 1
- **Source file:** data/papers/schizophrenia/sz4.pdf
- **Cosine distance:** 0.35535019636154175
- **Review warnings:** None detected

**Retrieved passage:**

& Van De Ville, 2013; X. Li et al., 2014). In this study, we ﬁrst collected fMRI raw datasets from two publicly available repositories including 300+ partici- pants and developed a 3D convolutional network to train on the images by aggregating information over the timesteps for every subject for the automatic diagnosis of individuals with schizophrenia. We compare our model with various baseline models and record the performance. 2 Related Work Machine learning has had a signiﬁcant impact on schizophrenia diagnosis studies. Along with MRI and fMRI, the researchers analysed data from genetics, elec- troencephalography, and even audio interviews (Cortes- arXiv:2210.05240v1 [cs.CV] 11 Oct 2022

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 6: SCH02

- **Condition:** Schizophrenia
- **Page:** 7
- **Source file:** data/papers/schizophrenia/sz1.pdf
- **Cosine distance:** 0.3556092381477356
- **Review warnings:** None detected

**Retrieved passage:**

characteristics (ROC) curves for schizophrenia classification on the dataset. The green line represents the ROC curve of the benchmark model with the input of T1W WH scans. The red line represents the ROC curve of the SE-VGG-11BN with the input of T1W WB scans. (B) Bar plot of the classification performance of these models in terms of the accuracy (at the default operating threshold of 0.5, Th = 0.5), sensitivity, specificity, and the area under the ROC curve (AUC). (C) Table quantitatively summarizes the performance of these models. The p-value of the ROC test (DeLong’s test) indicated our model is significantly better than the benchmark model at a level of 0.05. (D) Generalizability of the two models trained by COBRE and NMorphCH datasets on unseen BrainGluSchi test dataset. Considering components A through D, SE-VGG-11BN exhibits a significantly better performance than the benchmark model.

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 7: SCH03

- **Condition:** Schizophrenia
- **Page:** 3
- **Source file:** data/papers/schizophrenia/sz2.pdf
- **Cosine distance:** 0.3734742999076843
- **Review warnings:** None detected

**Retrieved passage:**

and specificity were reported for testing group with results obtained by ensemble approach and shown in Table III. The highest testing accuracy was also obtained by inception_resnet_1 model at 70.98%. Hand- crafted feature-based machine learning approaches obtained very low accuracy. 3D CNN models with fully connected layers also have low performance. 3D CNN models with more complex architectures obtained higher accuracy as well as more balanced sensitivity and specificity. IV. DISCUSSION This study validated the use of CNN on classification of schizophrenia patients and controls based on structural MRI. 3D CNN models trained from scratch performed better than handcrafted feature-based machine learning, highlighting the potential of using CNN on classification of schizophrenia patients and controls. Unlike other diseases with obvious alterations on neuroimaging, the neuroanatomical alterations in schizophrenia tend to be subtle and sparsely distributed. The Figure 3. Architectures of Inception_resnet Models TABLE II. Cross-validation Results on NUSDAST Dataset acc sp se AUC Handcrafted Feature-Based Machine Learning Linear SVM 60.77% 60.48% 61.08% 0.646 Non-Linear SVM 69.15% 70.20% 68.10% 0.741 3D CNN Models Sequential_1 77.63% 80.39% 75.00% 0.802 Sequential_2 76.50% 75.91% 77.07% 0.779 Sequential_3 73.91% 73.13% 74.57% 0.753 Inception_1 78.19% 77.22% 79.07% 0.795 Inception_2 76.24% 78.08% 74.42% 0.773 Inception_Resnet_1 79.27% 80.44% 78.15% 0.803 Inception_Resnet_2 78.76% 81.54% 76.10% 0.803 (acc-accuracy, sp-specificity, se-sensitivity) TABLE III. Additional Testing Results on IMH Dataset acc sp

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 8: SCH05

- **Condition:** Schizophrenia
- **Page:** 2
- **Source file:** data/papers/schizophrenia/sz4.pdf
- **Cosine distance:** 0.3840761184692383
- **Review warnings:** None detected

**Retrieved passage:**

on a single site, and we desired to incorporate data from nu- merous locations, which is where (Zeng et al., 2018) came in handy. The writers of this article combined private and publicly available datasets. That, we believe, is the only ef- fort in this area that utilized such a vast sample space for model training. We were unable to locate many open fMRI datasets, particularly those that included both T1 weighted and resting-state fMRI. Finally, we chose two locations, COBRE and UCLA. 3 Materials and Methods 3.1 Participants The dataset is made up of 120 schizophrenia patients and 206 healthy people who were gathered from two different imaging resources. Refer to Table 1. The ﬁrst subgroup was developed at the University of California, Los Ange- les (UCLA: 50 schizophrenics and 122 healthy controls; patients were allowed to use stable medications) (Bilder et al., 2016). The second group comes from the Center for Biomedical Research Excellence (COBRE) (COBRE: 69 Schizophrenia Strict Spectrum patients, 11 Schizoaffec- tive Spectrum patients, and 84 healthy controls; all of the patients were on antipsychotic medications) (Aine et al., 2017). All individuals were screened and rejected if they had a history of neurological illness, mental retardation, seri- ous head trauma resulting in a loss of consciousness lasting more than 5 minutes, or a history of substance

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

## Limitations

- Reference detection relies on text-based heuristics and can make mistakes.
- Retrieval relevance does not guarantee factual accuracy or complete coverage.
- The synthesis uses keyword/rule matching; it does not deeply interpret context, resolve contradictions, or prove causal relationships.
- Research gaps are candidates based only on the selected passages and require full-paper review.
