# Neuro Literature Research Report

**Research question:** Which diagnostic methods, EEG features, and machine-learning models are used for epilepsy detection and seizure prediction?
**Condition filter:** epilepsy
**Generated:** 2026-10-26 23:28:50
**Evidence passages selected:** 8

## Summary

This report combines retrieved passages with a transparent, rule-based overview of terms and limitations mentioned in those passages. The synthesis is a navigation aid, not an independently verified systematic review or a substitute for reading the full papers.

## Cross-paper overview

The selected evidence contains passages from **3 distinct paper ID(s)**.

- **EPI03:** 3 selected passage(s) (EPI03, p. 1, EPI03, p. 11).
- **EPI05:** 4 selected passage(s) (EPI05, p. 4, EPI05, p. 2, EPI05, p. 1).
- **EPI04:** 1 selected passage(s) (EPI04, p. 5).

## Imaging modalities mentioned

### Detected modalities

- **MRI (including structural and T1/T2-weighted MRI):** mentioned in EPI03, p. 1.

## Machine-learning methods mentioned

### Detected methods

- **deep learning (general):** mentioned in EPI03, p. 1.

## Candidate research gaps and limitations

- **Clinical translation and routine-use limitations:** cues found in EPI04, p. 5. Candidate issue mentioned in the retrieved passages; check the full papers before treating it as a research gap.

## Interpretation notes

- A detected term means that it appears in a selected passage; it does not establish that a method is effective or clinically recommended.
- Candidate gaps are inferred from limitations or future-work language in the selected passages, not from a comprehensive review of all 25 PDFs.
- Verify every claim against the complete source paper and its methods/results before using it in academic work.

## Retrieved evidence

### Evidence 1: EPI03

- **Condition:** Epilepsy
- **Page:** 1
- **Source file:** data/papers/epilepsy/ep2.pdf
- **Cosine distance:** 0.2785945534706116
- **Review warnings:** None detected

**Retrieved passage:**

in the brain, which indicate the brain’s bioelectric activity [9]. Diagnosing epilepsy with EEG signals is time-consuming and strenuous, as the epileptologist or neurologist needs to screen the EEG signals minutely. Also, there is a possibility of human error, and hence, developing a computer-based diagnosis may alleviate these problems. Many machine learning algorithms have been developed using statistical, frequency domain and nonlinear parameters to detect epileptic seizures [10], [11], [12], [13], [14], [15]. In conventional machine learning techniques, the selection of features and classiﬁers is made by trial and error method. Also, one needs to have sound knowledge of signal processing and data mining to develop a robust model. Such models perform well for limited data. Nowadays, with the increase in the availability of data, machine learning techniques may not perform very well. Hence, the deep learning techniques, which are the state-of-art methods, have been employed. In traditional machine learning algorithms, most simulations were executed in the Matlab software environment, but the arXiv:2007.01276v3 [cs.LG] 29 May 2021

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 2: EPI03

- **Condition:** Epilepsy
- **Page:** 11
- **Source file:** data/papers/epilepsy/ep2.pdf
- **Cosine distance:** 0.308040976524353
- **Review warnings:** None detected

**Retrieved passage:**

the detection of epileptic seizures through the handheld devices or wearables, and thus the patient can be provided with proper treatment in time. Moreover, a cap with EEG electrodes in it can obtain the EEG signals and sent to the model kept in the cloud, so it can achieve real-time detection. Additionally, if we can detect interictal periods (early stage of seizure), early-stage immediately, the patient can take medication immediately and prevent seizure. Finally, this ﬁeld of research requires more research by combining different screening methods for more precise and fast detection of epileptic seizures and also applying semi-supervised and unsupervised methods to further overcome the dataset size limits. APPENDIX A Table X shows details about all the works reviewed in this study.

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 3: EPI03

- **Condition:** Epilepsy
- **Page:** 1
- **Source file:** data/papers/epilepsy/ep2.pdf
- **Cosine distance:** 0.3195246458053589
- **Review warnings:** None detected

**Retrieved passage:**

1 Epileptic Seizures Detection Using Deep Learning Techniques: A Review Afshin Shoeibi, Marjane Khodatars, Navid Ghassemi, Mahboobeh Jafari, Parisa Moridian, Roohallah Alizadehsani, Maryam Panahiazar, Fahime Khozeimeh, Assef Zare, Hossein Hosseini-Nejad, Abbas Khosravi, Amir F. Atiya, Diba Aminshahidi, Sadiq Hussain, Modjtaba Rouhani, Saeid Nahavandi, and Udyavara Rajendra Acharya Abstract—A variety of screening approaches have been pro- posed to diagnose epileptic seizures, using electroencephalogra- phy (EEG) and magnetic resonance imaging (MRI) modalities. Artiﬁcial intelligence encompasses a variety of areas, and one of its branches is deep learning (DL). Before the rise of DL, conven- tional machine learning algorithms involving feature extraction were performed. This limited their performance to the ability of those handcrafting the features. However, in DL, the extraction of features and classiﬁcation are entirely automated. The advent of these techniques in many areas of medicine, such as in the diagnosis of epileptic seizures, has made signiﬁcant advances. In this study, a comprehensive overview of works focused on automated epileptic seizure detection using DL techniques and neuroimaging modalities is presented. Various methods proposed to diagnose epileptic seizures automatically using EEG and MRI modalities are described. In addition, rehabilitation systems developed for epileptic seizures using DL have been analyzed, and a summary is provided. The rehabilitation tools include cloud computing techniques and hardware required for implementation of DL algorithms. The important challenges

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 4: EPI05

- **Condition:** Epilepsy
- **Page:** 4
- **Source file:** data/papers/epilepsy/ep4.pdf
- **Cosine distance:** 0.32164329290390015
- **Review warnings:** None detected

**Retrieved passage:**

classiﬁcation methods for epileptic seizure detection. They extracted the best representative characteristics from the EEG wavelet coefﬁcients and Lyapunov exponents. The probabilistic neural network (PNN) was used afterwards for EEG classiﬁcation, where it achieved a notable classiﬁ- cation accuracy of 98.05%. Also, ¨Ubeyli et al. developed an eigenvector-based method for EEG feature extraction, which in turn achieved a 99.30% classiﬁcation accuracy using SVM [50]. In [51], the same authors used simple statistical features instead and a high classiﬁcation accuracy of 99.20% was maintained.

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 5: EPI05

- **Condition:** Epilepsy
- **Page:** 2
- **Source file:** data/papers/epilepsy/ep4.pdf
- **Cosine distance:** 0.3252251148223877
- **Review warnings:** None detected

**Retrieved passage:**

segments taken from healthy persons (set A) and seizure EEG patterns taken from epileptic patients while experiencing active seizures (set E) [18]–[28]. Aarabi et al. proposed an automated seizure detection system using a set of representative EEG features extracted from time domain, frequency domain and wavelet domain as well as auto-regressive coefﬁcients and cepstral features [18]. All these features were fed altogether into a back-propagation neural network (BNN) classiﬁer with two hidden layers and resulted in an average classiﬁcation accuracy of 93.00%. In [19], Subasi et al. used wavelet transform to derive the EEG frequency bands and then use all the spectral components as an input to the mixture of experts (ME) classiﬁer; an average classiﬁcation accuracy of 94.50% was achieved. Polat et al. achieved a higher classiﬁcation accuracy of 98.68% using a decision tree (DT) classiﬁer [20]. Furthermore, Chandaka et al. used the EEG cross- correlation coefﬁcients to compute three statistical features, and hence present them as a feature vector to the support vector machine (SVM) for EEG classiﬁcation [21]. This model yielded a modest seizure detection accuracy of 95.96%. Yuan et al. obtained comparable detection accuracies using the extreme learning machine (ELM) classiﬁer and a set of non- linear features such as approximate entropy and Hurst expo- nent [22]. Wavelet transform was also used in [23] to analyze

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 6: EPI05

- **Condition:** Epilepsy
- **Page:** 1
- **Source file:** data/papers/epilepsy/ep4.pdf
- **Cosine distance:** 0.32741791009902954
- **Review warnings:** None detected

**Retrieved passage:**

live in low- and middle- income countries and cannot afford consulting neurologists or The ﬁrst author is funded by Vanier Canada Graduate Scholarship from the Natural Sciences and Engineering Research Council of Canada (NSERC). ⋆Corresponding Author: ramy@ece.ubc.ca §Ramy Hussein, Z. Jane Wang and Rabab Ward are with the Department of Electrical and Computer Engineering, University of British Columbia, Vancouver, BC V6T 1Z4, Canada. †Hamid Palangi is with Microsoft Research AI, Redmond, WA 98052, United States. practitioners [3]. Those limitations have encouraged scholars to develop automatic EEG-based seizure detection systems. A vast number of methods have been developed for auto- matic seizure detection using EEG signals. Extracting features that best describe the behaviour of EEGs is of great importance for automatic seizure detection systems’ performance. Several feature extraction and selection techniques have been reported in the literature. Most of them use hand-wrought features in the time-domain [4], [5], frequency-domain [6]–[8], time- frequency domain [9]–[12] or sometimes in a combination of two domains [13]. However, these domain-based methods encounter three main challenges. First, they are sensitive (not robust enough) to acute variations in seizure patterns. This is because the EEG data is non-stationary and its statistical features change across different subjects and over time for the same subject. Secondly, EEG data acquisition systems are very susceptible to a diverse range of artifacts

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 7: EPI04

- **Condition:** Epilepsy
- **Page:** 5
- **Source file:** data/papers/epilepsy/ep3.pdf
- **Cosine distance:** 0.3282245397567749
- **Review warnings:** None detected

**Retrieved passage:**

(FNN) variant [63]. This system had great potential for both offline and online sorting of spikes in brain-computer interface (BCI) applications. The potential future integration of DL interfaces into neural implants offers an avenue to enhance classification performance and improve therapeutic outcomes for individuals with epileptic seizures [62]. Limitations of ML in epilepsy detection The application of AI and its subdisciplines in the field of seizure detection is undeniably going to shape the future of neuroscience. Effective treatment and improved medical and surgical outcomes are only possible if accurate and timely detection of seizure activity is detected. However, many limitations to the real-world applications of these systems diminish their potential. ML and DL models are known to function as “black boxes,” making it extremely challenging to interpret the reasoning behind their predictions correctly [64]. In medical applications, interpretability is crucial as accurate diagnosis and appropriate treatment depend on it. The lack of interpretability to AI models poses a significant limitation to their adoption in clinical practice. A recent study validated a classifier and predicted treatment response in an Australian cohort of newly diagnosed epilepsy patients. It assessed the validity of the classifier in two independent United Kingdom (UK) cohorts of newly diagnosed patients. This study investigated the predictive utility of five single- nucleotide polymorphisms (SNPs) in seizure control. It was

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

### Evidence 8: EPI05

- **Condition:** Epilepsy
- **Page:** 4
- **Source file:** data/papers/epilepsy/ep4.pdf
- **Cosine distance:** 0.3334652781486511
- **Review warnings:** None detected

**Retrieved passage:**

seizure diagnostic accuracy of 96.60%. Furthermore, ¨Ubeyli et al. adopted wavelet transform to obtain and analyze the main spectral rhythms of the EEG signals [39]. Then, the statistical features that characterize the behavior of the EEGs were extracted and tested using the multilayer perceptron neural network (MLPNN) classiﬁer. The results showed sensitivity, speciﬁcity, and classiﬁcation accuracy of 96.00%, 94.00%, and 94.83%, respectively. In [40], a feature extraction method based on the sample entropy was used together with the ELM classiﬁer and resulted in sensitivity, speciﬁcity, and classiﬁcation accuracy of 97.26%, 98.77%, and 95.67%, respectively. Also, a set of temporal and spectral EEG features forming a more representative feature vector was fed into a MLPNN for EEG classiﬁcation [41]. The epilepsy detection rates produced by this method were 97.46% for sensitivity, 98.74% for speciﬁcity, and 97.50% for classiﬁcation accuracy. In an effort to alleviate the computational complexity burden in seizure detection systems, Acharya et al. relaxed the need of any pre-processing techniques and worked directly on the raw EEG data [42], [43]. In [42], a set of robust EEG features including approximate entropy, sample entropy and phase entropy was computed from the recorded EEG signals and then fed into fuzzy Sugeno classiﬁer (FSC) for EEG classiﬁcation. This approach notably boosted the classiﬁcation accuracy to 98.10%. In addition, Acharya et al. proposed,

**Verification note:** Confirm that the passage supports the claim you intend to make.

---

## Limitations

- Reference detection relies on text-based heuristics and can make mistakes.
- Retrieval relevance does not guarantee factual accuracy or complete coverage.
- The synthesis uses keyword/rule matching; it does not deeply interpret context, resolve contradictions, or prove causal relationships.
- Research gaps are candidates based only on the selected passages and require full-paper review.
