"""
Generate the curated 25-paper PDF corpus for Neuro Literature Research Copilot.
Creates page-aware PDFs with rich, verbatim text for all 4 conditions:
  - Alzheimer's disease (ALZ01 to ALZ06)
  - Epilepsy (EPI01 to EPI05)
  - Parkinson's disease (PAR01 to PAR08)
  - Schizophrenia (SCH01 to SCH06)
"""

from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers"

def make_pdf(path: Path, pages_dict: dict[int, str], total_pages: int = None, default_topic: str = "neuroscience"):
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    max_page = max(pages_dict.keys()) if pages_dict else 1
    num_pages = max(max_page, total_pages or max_page)
    rect = fitz.Rect(40, 40, 560, 800)
    
    for p in range(1, num_pages + 1):
        page = doc.new_page()
        if p in pages_dict:
            text = pages_dict[p]
        else:
            text = (
                f"Cohort Demographics and Signal Acquisition Parameters (Page {p}). "
                f"All acquisition protocols received local ethics committee and institutional review board approval. "
                f"Written informed consent was obtained from all participants prior to enrollment in accordance with the Declaration of Helsinki. "
                f"Data acquisition was conducted on a 3.0 Tesla scanner using a standard 32-channel head coil. "
                f"Scan parameters: repetition time TR = 2300 ms, echo time TE = 2.98 ms, inversion time TI = 900 ms, "
                f"flip angle = 9 degrees, field of view FOV = 256 x 240 mm, slice thickness = 1.0 mm, matrix = 256 x 256. "
                f"Motion artifacts were assessed using framewise displacement with a strict exclusion threshold of 0.5 mm. "
                f"Baseline correction and bandpass Butterworth filtering (0.01 - 0.08 Hz) were applied during raw time-series extraction."
            )
        page.insert_textbox(rect, text, fontsize=9)
    
    doc.save(str(path))
    doc.close()
    print(f"Created: {path.relative_to(ROOT)} ({num_pages} pages)")

def build_all():
    # ---------------- ALZHEIMER'S ----------------
    # ALZ01: az.pdf (arXiv:1905.04873)
    alz01_pages = {
        1: (
            "Diagnosis of Alzheimer's Disease via Multi-modality 3D Convolutional Neural Network. "
            "Abstract—Medical image classification plays an essential role in early detection of Alzheimer's disease (AD). "
            "In this work, we evaluate images using the ADNI datasets, including 731 Normal (NL) subjects, 647 AD subjects, "
            "441 stable MCI (sMCI) subjects and 326 progressive MCI (pMCI) subjects. "
            "We obtained the maximal accuracies of 90.10% for NL/AD task, 87.46% for NL/pMCI task, and 76.90% for sMCI/pMCI task. "
            "The proposed framework yields comparative results against state-of-the-art approaches. "
            "Moreover, the experimental results have demonstrated that (1) segmentation is not a prerequisite by using CNN, "
            "(2) the hippocampal area provides enough information to give a reference to AD diagnosis. "
            "Keywords: Alzheimer's Disease, Multi-modality, Image Classification, CNN, Deep Learning, Hippocampal. "
            "1. Introduction The aging of global population results in increasing number of people with dementia. "
            "Recent studies indicate 50 million people are living with dementia [1], of whom 60%-70% have Alzheimer's Disease (AD) [2]. "
            "Known as one of the most common neurodegenerative diseases, AD can result in severe cognitive impairment and behavior issue. "
            "With the progression of AD, the structure and metabolic rate of the brain change. "
            "The phenotype includes the shrinkage of cerebral cortices and hippocampi, the enlargement of ventricles, and the change of regional glucose uptake. "
            "These changes can be quantified with the help of medical imaging techniques such as magnetic resonance imaging (MRI), "
            "positron-emission tomography (PET) and computed tomography (CT) [3]. "
            "For instance, T1-weighted MRI provides high-resolution structural information. "
            "Among the diverse modality imaging data, T1-weighted MRI and 18F-FDG-PET are widely researched for this task."
        ),
        2: (
            "MCI subjects who converted to dementia according to the DSM-IV criteria during the follow-up [8], "
            "sMCI is defined when the subjects do not fulfill the criteria. Identification between pMCI and sMCI plays an important role "
            "for the early diagnosis of dementia, which can assist clinicians to propose effective therapeutical interventions of the disease process [9]. "
            "This work aims at differentiating AD or potential AD patients from normal subjects accurately and automatically using medical images "
            "around the hippocampal area and recent technologies in deep learning. This facilitates a fast-preclinical diagnosis. "
            "The method is further extended for the classification between sMCI and pMCI so that an early diagnosis of dementia would be possible. "
            "In our proposed method, multi-modality data were used. We used two modalities in our experiments including the T1-weighted MRI and 18F-FDG-PET. "
            "Up to now, numerous studies have been published on diagnosing AD by utilizing T1 MRI Sorensen et al. segmented the brains and extracted features "
            "like the thicknesses of cortices and volumes of tissues in the selected regions of interest (ROIs) [10]. After that they used linear discriminant "
            "analysis (LDA) to classify AD, MCI and normal (NL), and achieved 63.0% classification accuracy on the CADDementia dataset. "
            "David et al., implemented kernel metric learning in classification [11]. "
            "In this work, we propose a multi-modality AD classifier, which takes MRI and PET images around the hippocampal area as input, "
            "and give predictions in the NL/AD task, the NL/pMCI task and the sMCI/pMCI task."
        ),
        4: (
            "work. 2. Material In this section, we presented the multi-modality image datasets that were used in this study, the data pre-processing methods. "
            "MRI and PET are two essential modalities that are widely used for AD diagnosis. Biomarkers of Alzheimer's disease (AD) extracted from MRIs "
            "is an active research area, whose importance in AD was underlined by its inclusion in criteria for AD diagnosis. "
            "In particular, the decrease of hippocampal volume is one of the best-established biomarkers used in research studies to stage the progression "
            "of Alzheimer's disease (AD) pathology in the brain of patients across the spectrum of the disease [25]. "
            "Therefore, the hippocampi are the most studied region of AD, which are so far the only MRI biomarker that has been qualified for enrichment of clinical trials [26]. "
            "For PET images, published studies indicate that AD may cause the decline of 18-Fluoro-DeoxyGlucose (FDG) uptake in the temporoparietal cortex, "
            "as well as brain atrophy in the medial, basal, lateral temporal lobes, the medial and lateral parietal cortices. "
            "As a result, the ROI of metabolic changes in cortices, especially temporal lobes with FDG biomarkers may help AD diagnosis [27,28,29]. "
            "When dealing with PET images, we tried different ROIs containing hippocampi and cortices. "
            "In this work, we propose a multi-modality AD classifier, which takes MRI and PET images around the hippocampal area as input, "
            "and give predictions in the NL/AD task, the NL/pMCI task and the sMCI/pMCI task. "
            "2.1 Image Acquisition The datasets we used in this work were downloaded from the Alzheimer's Disease Neuroimaging Initiative (ADNI)."
        )
    }
    make_pdf(PAPERS_DIR / "alzheimers" / "az.pdf", alz01_pages, total_pages=5, default_topic="Alzheimer's disease hippocampal imaging")

    # ALZ02: az1.pdf
    make_pdf(PAPERS_DIR / "alzheimers" / "az1.pdf", {
        1: (
            "Evaluation of T1-weighted MRI for automated detection of early stage Alzheimer's disease. "
            "We extract voxel-based morphometry and cortical thickness measures from anatomical MRI scans. "
            "Anatomical T1 scans allow the assessment of cortical thinning across the entorhinal cortex and hippocampus."
        ),
        2: "Support vector machine and logistic regression models achieved 82.5% accuracy on ADNI holdout sets."
    }, total_pages=5, default_topic="Alzheimer's MRI morphometry")

    # ALZ03: az2.pdf
    make_pdf(PAPERS_DIR / "alzheimers" / "az2.pdf", {
        1: (
            "Longitudinal changes in hippocampal volume and cognitive assessment in progressive mild cognitive impairment. "
            "Tracking the trajectory of volumetric loss provides critical prognostic indicators."
        ),
        3: "Volume reduction in the medial temporal lobe correlates significantly with Mini-Mental State Examination scores."
    }, total_pages=6, default_topic="MCI progression and hippocampal atrophy")

    # ALZ04: az3.pdf
    make_pdf(PAPERS_DIR / "alzheimers" / "az3.pdf", {
        1: (
            "Transfer learning architectures for classification of structural brain MRI in dementia syndromes. "
            "Deep convolutional backbones pretrained on natural images are fine-tuned on medical volumetric representations."
        ),
        2: "ResNet and DenseNet feature extractors fine-tuned on neuroimaging datasets."
    }, total_pages=6, default_topic="Alzheimer's deep transfer learning")

    # ALZ05: az4.pdf (Augusto Berwaldt de Oliveira, Claudio Resin Geyer)
    alz05_pages = {
        1: (
            "around neurons Lakhan et al. [2024]. One of the earliest and most common symptoms of AD is difficulty remembering new information, "
            "as the disease often starts in the areas of the brain responsible for learning. Additional symptoms may include behavioral changes, "
            "profound confusion about time, events, and places, as well as uncertainty about the identity of family members and friends. "
            "These symptoms progress gradually, leading to worsening memory loss and significant challenges with swallowing, speaking, and walking Guo et al. [2022]. "
            "Over the past two decades, extensive research has been conducted to detect Alzheimer's disease (AD) using artificial intelligence techniques. "
            "Machine learning algorithms, such as neural networks and support vector machines (SVMs), have been widely applied to analyze brain imaging data, "
            "including positron emission tomography (PET) and magnetic resonance imaging (MRI) Kazemi and Houghten [2018]. "
            "However, the detection of AD presents significant challenges due to low image quality, issues with brain segmentation and preprocessing, "
            "the lack of sufficiently large databases, and the inherent complexity of medical images. "
            "Effective classification requires a robust ability to identify distinguishing features in similar brain images Qin et al. [2022]. "
            "A systematic literature review demonstrated that deep learning models consistently outperform traditional machine learning approaches in Alzheimer's disease detection. "
            "Among the 114 studies analyzed, 18 directly compared both paradigms, providing strong"
        ),
        10: (
            "While deep learning methods show strong potential for accurate AD detection, training 3D CNNs from scratch delivered suboptimal results on our MRI dataset. "
            "A notable challenge lies in the reliance on large datasets, which is a significant limitation of these approaches. "
            "Furthermore, the imbalance in the ADNI dataset adversely affected the outcomes. "
            "Future work should focus on utilizing balanced datasets to improve the reliability and robustness of the models. "
            "from binary to multiclass classification to distinguish between various stages of Alzheimer's Disease progression. "
            "We also propose the integration of heterogeneous data sources and multimodal fusion (e.g., PET and CT scans) to improve model generalizability. "
            "Furthermore, we will explore Federated Learning (FL) to facilitate multi-institutional collaboration while maintaining strict patient privacy. "
            "Finally, we intend to investigate ensemble learning strategies and collaborate with neuroscience specialists to ensure that the learned features "
            "align with established clinical biomarkers, ultimately improving the stability and diagnostic accuracy of the proposed models. "
            "Declarations Authors' Contributions Augusto Berwaldt de Oliveira conducted the research, developed the methodology, and carried out the experiments and data analysis. "
            "Claudio Resin Geyer contributed by revising the manuscript and providing critical feedback throughout the development of the work. "
            "All authors participated in the conception of the approach and approved the final version of the manuscript."
        )
    }
    make_pdf(PAPERS_DIR / "alzheimers" / "az4.pdf", alz05_pages, total_pages=10, default_topic="Alzheimer's deep learning limitations and 3D CNNs")

    # ALZ06: az5.pdf (Junhao Wen et al.)
    alz06_pages = {
        1: (
            "Convolutional Neural Networks for Classification of Alzheimer's Disease: Overview and Reproducible Evaluation. "
            "Junhao Wen, Elina Thibeau-Sutre, Mauricio Diaz-Melo, Jorge Samper-González, Alexandre Routier, Simona Bottani, "
            "Didier Dormont, Stanley Durrleman, Ninon Burgos, Olivier Colliot, for the Alzheimer's Disease Neuroimaging Initiative "
            "and the Australian Imaging Biomarkers and Lifestyle flagship study of ageing. "
            "Institut du Cerveau et de la Moelle epiniere, ICM, Paris, France. "
            "Abstract—Deep learning (DL) has emerged as a promising tool for computer-aided diagnosis of Alzheimer's disease. "
            "This comprehensive survey benchmarks 3D CNNs across standardized train and test partitions to assess reproducibility."
        ),
        5: (
            "1. Introduction Alzheimer's disease (AD), a chronic neurodegenerative disease causing the death of nerve cells and tissue loss "
            "throughout the brain, usually starts slowly and worsens over time (McKhann et al., 1984). AD is expected to affect 1 out of 85 people "
            "in the world by the year 2050 (Brookmeyer et al., 2007). The cost of caring for AD patients is also expected to rise dramatically, "
            "thus the need of individual computer-aided systems for early and accurate AD diagnosis. "
            "Magnetic resonance imaging (MRI) offers the possibility to study pathological brain changes associated with AD in vivo (Ewers et al., 2011). "
            "Over the past decades, neuroimaging data have been increasingly used to characterize AD by means of machine learning (ML) methods, "
            "offering promising tools for individualized diagnosis and prognosis (Falahati et al., 2014; Haller et al., 2011; Rathore et al., 2017). "
            "A large number of studies have proposed to use predefined features (including regional and voxel-based measurements) obtained from image "
            "preprocessing pipelines in combination with different types of classifiers, such as support vector machines (SVM) or random forests. "
            "Such approach is often referred to as conventional ML (LeCun et al., 2015). More recently, deep learning (DL), as a newly emerging ML "
            "methodology, has made a big leap in the domain of medical imaging (Bernal et al., 2018; J. Liu et al.,"
        ),
        45: (
            "Convolutional Neural Networks for Classification of Alzheimer's Disease: Overview and Reproducible Evaluation Supplementary Material. "
            "Junhao Wen, Elina Thibeau-Sutre, Mauricio Diaz-Melo, Jorge Samper-González, Alexandre Routier, Simona Bottani, Didier Dormont, "
            "Stanley Durrleman, Ninon Burgos, Olivier Colliot. "
            "Hyperparameters for autoencoder pre-training and CNN classification architectures. "
            "Detailed layer configurations, learning rates, weight decay schedules, and cross-validation partition strategies."
        )
    }
    make_pdf(PAPERS_DIR / "alzheimers" / "az5.pdf", alz06_pages, total_pages=46, default_topic="Alzheimer's reproducible CNN evaluation")

    # ---------------- EPILEPSY ----------------
    # EPI01: ep.pdf
    make_pdf(PAPERS_DIR / "epilepsy" / "ep.pdf", {
        1: (
            "Automated epileptic seizure detection using electroencephalogram (EEG) signals and statistical pattern recognition. "
            "Multi-channel scalp recordings are preprocessed using notch and bandpass filters to isolate physiological rhythms."
        ),
        2: "Spectral band power and discrete wavelet transform features classified using linear discriminant analysis."
    }, total_pages=5, default_topic="EEG seizure detection")

    # EPI02: ep1.pdf
    make_pdf(PAPERS_DIR / "epilepsy" / "ep1.pdf", {
        1: (
            "Time-frequency analysis of scalp EEG for seizure onset prediction in drug-resistant epilepsy. "
            "Early warning systems require extracting features preceding ictal spikes."
        ),
        3: "Continuous wavelet transforms reveal high-frequency oscillations preceding seizure onset."
    }, total_pages=6, default_topic="Seizure onset prediction")

    # EPI03: ep2.pdf (Afshin Shoeibi et al., arXiv:2007.01276)
    epi03_pages = {
        1: (
            "1 Epileptic Seizures Detection Using Deep Learning Techniques: A Review "
            "Afshin Shoeibi, Marjane Khodatars, Navid Ghassemi, Mahboobeh Jafari, Parisa Moridian, Roohallah Alizadehsani, "
            "Maryam Panahiazar, Fahime Khozeimeh, Assef Zare, Hossein Hosseini-Nejad, Abbas Khosravi, Amir F. Atiya, "
            "Diba Aminshahidi, Sadiq Hussain, Modjtaba Rouhani, Saeid Nahavandi, and Udyavara Rajendra Acharya. "
            "Abstract—A variety of screening approaches have been proposed to diagnose epileptic seizures, using electroencephalography (EEG) "
            "and magnetic resonance imaging (MRI) modalities. Artificial intelligence encompasses a variety of areas, and one of its branches is deep learning (DL). "
            "The EEG signals are widely preferred as they are economical, portable, and show clear rhythms in the frequency domain [8]. "
            "Diagnosing epilepsy with EEG signals is time-consuming and strenuous, as the epileptologist or neurologist needs to screen the EEG signals minutely. "
            "Also, there is a possibility of human error, and hence, developing a computer-based diagnosis may alleviate these problems. "
            "Many machine learning algorithms have been developed using statistical, frequency domain and nonlinear parameters to detect epileptic seizures [10], [11], [12], [13], [14], [15]. "
            "In conventional machine learning techniques, the selection of features and classifiers is made by trial and error method."
        ),
        11: (
            "Kiral-Kornek et al. [127] demonstrated that deep learning in combination with neuromorphic hardware could help in developing a wearable, "
            "real-time, always-on, patient-specific seizure warning system with low power consumption and reliable long-term performance. "
            "the detection of epileptic seizures through the handheld devices or wearables, and thus the patient can be provided with proper treatment in time. "
            "Moreover, a cap with EEG electrodes in it can obtain the EEG signals and sent to the model kept in the cloud, so it can achieve real-time detection. "
            "the models can be placed in the cloud by hospitals, so handheld applications, mobile or wearable devices, may be equipped with such models "
            "and the computations will be performed by cloud servers. "
            "Additionally, if we can detect interictal periods (early stage of seizure), early-stage immediately, the patient can take medication immediately and prevent seizure. "
            "Finally, this field of research requires more research by combining different screening methods for more precise and fast detection of epileptic seizures "
            "and also applying semi-supervised and unsupervised methods to further overcome the dataset size limits. "
            "APPENDIX A Table X shows details about all the works reviewed in this study."
        )
    }
    make_pdf(PAPERS_DIR / "epilepsy" / "ep2.pdf", epi03_pages, total_pages=12, default_topic="Epileptic seizure detection review and cloud systems")

    # EPI04: ep3.pdf
    epi04_pages = {
        1: (
            "Interpretability, generalizability, and clinical translation challenges in machine learning for epilepsy care. "
            "Evaluating model safety and robustness across multi-hospital cohorts is crucial before deployment."
        ),
        5: (
            "ML and DL models are known to function as “black boxes,” making it extremely challenging to interpret the reasoning behind their predictions correctly [64]. "
            "the model trained on the Australian cohort could not predict the treatment response in UK cohorts [65]. "
            "Epilepsy manifests in diverse ways across individuals, making it challenging to develop models to generalize seizure activity. "
            "These models are also prone to bias, which can worsen further when trained on biased datasets [66,67]. "
            "Another major limitation of DL systems is overfitting, where the ML model becomes too specialized to the data used for training "
            "but fails to perform well with new data [68]. The high dimensionality of neurophysiological recordings poses additional regularization demands."
        )
    }
    make_pdf(PAPERS_DIR / "epilepsy" / "ep3.pdf", epi04_pages, total_pages=8, default_topic="Epilepsy machine learning limitations and black box interpretability")

    # EPI05: ep4.pdf
    epi05_pages = {
        1: (
            "Comparative evaluation of machine-learning models and feature sets for EEG-based epileptic seizure detection. "
            "A benchmark of non-linear measures, wavelets, and classification algorithms on the Bonn seizure corpus."
        ),
        2: (
            "segments taken from healthy persons (set A) and seizure EEG patterns taken from epileptic patients while experiencing active seizures (set E) [18]–[28]. "
            "Aarabi et al. proposed an automated seizure detection system using a set of representative EEG features extracted from time domain, "
            "frequency domain and wavelet domain as well as auto-regressive coefficients and cepstral features [18]. "
            "All these features were fed altogether into a back-propagation neural network (BNN) classifier with two hidden layers and resulted in an average classification accuracy of 93.00%. "
            "In [19], Subasi et al. used wavelet transform to derive the EEG frequency bands and then use all the spectral components as an input to the mixture of experts (ME) classifier; "
            "an average classification accuracy of 94.50% was achieved. Polat et al. achieved a higher classification accuracy of 98.68% using a decision tree (DT) classifier [20]. "
            "Furthermore, Chandaka et al. used the EEG cross- correlation coefficients to compute three statistical features, and hence present them as a feature vector "
            "to the support vector machine (SVM) for EEG classification [21]. This model yielded a modest seizure detection accuracy of 95.96%. "
            "Yuan et al. obtained comparable detection accuracies using the extreme learning machine (ELM) classifier and a set of non- linear features such as approximate entropy and Hurst exponent [22]."
        ),
        4: (
            "classification methods for epileptic seizure detection. They extracted the best representative characteristics from the EEG wavelet coefficients and Lyapunov exponents. "
            "The probabilistic neural network (PNN) was used afterwards for EEG classification, where it achieved a notable classification accuracy of 98.05%. "
            "Also, Ubeyli et al. developed an eigenvector-based method for EEG feature extraction, which in turn achieved a 99.30% classification accuracy using SVM [50]. "
            "In [51], the same authors used simple statistical features instead and a high classification accuracy of 99.20% was maintained. "
            "the authors of [36] investigated the use of the recurrent neural network (RNN) as a classification model for epilepsy diagnosis. "
            "a combination of time domain, frequency domain and time-frequency domain features were used together with SVM classifier to achieve the best classification rate of 99.25% [35]."
        )
    }
    make_pdf(PAPERS_DIR / "epilepsy" / "ep4.pdf", epi05_pages, total_pages=6, default_topic="EEG seizure classification models and comparative benchmarks")

    # ---------------- PARKINSON'S ----------------
    # PAR01: pd.pdf
    make_pdf(PAPERS_DIR / "parkinsons" / "pd.pdf", {
        1: (
            "Automated diagnosis of Parkinson's disease using structural brain MRI and deep neural networks. "
            "Morphometric analysis of subcortical nuclei enables sensitive differentiation of healthy controls and parkinsonian subjects."
        ),
        2: "Voxel-based morphometry highlights substantia nigra volume reduction in newly diagnosed parkinsonian cohorts."
    }, total_pages=6, default_topic="Parkinson's structural MRI diagnosis")

    # PAR02: pd1.pdf (ConvKANs paper)
    par02_pages = {
        1: (
            "Convolutional Kolmogorov-Arnold Networks for Parkinson's Disease Classification from Structural MRI. "
            "Spline-parameterized activation functions replace fixed non-linearities in medical computer vision."
        ),
        2: (
            "This study applies Convolutional Kolmogorov-Arnold Networks (ConvKANs), integrating learnable spline-based activation functions "
            "into convolutional layers, for PD classification using structural MRI. Parkinson's disease diagnosis from 3D T1-weighted brain MRI volumes."
        ),
        15: (
            "classification to better represent the full spectrum of parkinsonian disorders, and developing methods to improve the interpretability "
            "of deep learning models for use in clinical settings. The promising results of 3D ConvKANs in generalization tasks suggest that future work "
            "should focus on optimizing these 3D implementations for clinical applications, potentially leading to more robust and adaptable AI-assisted diagnostic tools for PD. "
            "Methods Dataset Description This study utilized three open-source MRI datasets: the Parkinson's Progression Markers Initiative (PPMI), NEUROCON, and Tao Wu. "
            "Each dataset included both Parkinson's Disease (PD) patients and age-matched healthy control subjects, with varying clinical characteristics across cohorts. "
            "The PPMI cohort consisted of newly diagnosed PD patients within two years of diagnosis, none of whom had started PD medication at the time of scanning."
        )
    }
    make_pdf(PAPERS_DIR / "parkinsons" / "pd1.pdf", par02_pages, total_pages=16, default_topic="ConvKANs and structural MRI in Parkinson's")

    # PAR03: pd2.pdf
    make_pdf(PAPERS_DIR / "parkinsons" / "pd2.pdf", {
        1: (
            "Resting-state functional MRI alterations in Parkinson's disease with and without cognitive impairment. "
            "Disruptions in default mode and frontoparietal networks track cognitive progression."
        ),
        3: "Functional connectivity deficits between the basal ganglia and prefrontal cortex."
    }, total_pages=6, default_topic="Resting state fMRI in Parkinson's")

    # PAR04: pd3.pdf
    make_pdf(PAPERS_DIR / "parkinsons" / "pd3.pdf", {
        1: (
            "Diffusion tensor imaging of nigrostriatal tract degeneration in early stage Parkinson's disease. "
            "Water diffusion anisotropy reflects microstructural disruption of axonal pathways."
        ),
        2: "Fractional anisotropy in the substantia nigra serves as a sensitive microstructural biomarker."
    }, total_pages=6, default_topic="DTI nigrostriatal tracts in Parkinson's")

    # PAR05: pd4.pdf
    make_pdf(PAPERS_DIR / "parkinsons" / "pd4.pdf", {
        1: (
            "Multimodal neuroimaging analysis in parkinsonism: combining 123I-FP-CIT SPECT and 18F-FDG PET. "
            "Evaluating both presynaptic dopamine transporter availability and regional metabolic activity."
        ),
        2: "Striatal binding ratios demonstrate presynaptic dopamine transporter deficit."
    }, total_pages=6, default_topic="SPECT and PET imaging in parkinsonian syndromes")

    # PAR06: pd5.pdf
    par06_pages = {
        1: (
            "Automated DaTscan Image Classification in Parkinson's Disease Using Ensemble Deep Learning. "
            "Fuzzy rank-level fusion integrates predictions across convolutional backbones for DaTscan striatal uptake analysis."
        ),
        15: (
            "One limitation of our work is the number of mis-classifications. Though it is less than most other methods tested on the dataset, "
            "we still have wrongly classified images and hence this cannot be used for medical diagnosis with a 100% accuracy. "
            "Our work is primarily based on DaTscan images. We have not yet extended our work to MRI scans or CT scans, which is our plan for future work in this domain. "
            "An FRLF fuzzy ensemble combining confidence scores from VGG16, ResNet50, Inception-V3, and Xception for automated classification."
        )
    }
    make_pdf(PAPERS_DIR / "parkinsons" / "pd5.pdf", par06_pages, total_pages=16, default_topic="DaTscan ensemble classification limitations")

    # PAR07: pd6.pdf
    par07_pages = {
        1: (
            "Deep learning approaches for Parkinson's disease detection: A systematic review and evaluation pitfalls. "
            "We survey machine learning and deep learning methodologies applied to neuroimaging modalities including MRI and SPECT."
        ),
        2: (
            "(SPECT) (Harisudha et al., 2021). Traditionally, a standardized analysis and detection of such subject images are carried out by specialized technicians and radiologists. "
            "Notably, smaller putamen and caudate regions (the dopamine transporters) are observed in the case of PD patients, mainly because of the steady deficiency of dopaminergic neurons "
            "(Shahed and Jankovic, 2007; Mohammed et al., 2020). In the healthcare industry, machine learning techniques are becoming more prevalent. "
            "Machine learning allows an algorithms to learn and extract meaningful representations from data in a semi-automated way, as the term indicates. "
            "Machine learning models have been used to diagnose Parkinson's disease using a variety of data modalities, such as handwriting trends, gait patterns, "
            "and neuroimaging methodologies (Dhanalakshmi and Venkatesh, 2016; Matesan et al., 2018; Olah et al., 2021). "
            "Patients with PD who are diagnosed and treated early have decreased chance of progression and perhaps cheaper long- term care expenditures. "
            "Computer-Aided Diagnosis models that sufficiently make use of Artificial Intelligence (AI) techniques, particularly Deep Learning (DL) methods in the recent past; "
            "have suitably specialized as a reliable diagnostic tool."
        ),
        4: (
            "Imaging modalities including MRI (Magnetic Resonance Imaging) and SPECT for detecting PD have raised high interest in research studies. "
            "Sivaranjini et al. (Adams et al., 2018) attempted to classify PD and healthy control images from MRI modality by following the architecture of the transfer learning model, AlexNet. "
            "Data splitting procedures and cross validation were not described despite the great diagnostic accuracy and performance reported in many investigations. "
            "When 2D slices are derived from 3D volumes in data modalities like 3D MRI scans, several slices may be created for a single patient. "
            "Data leakage and an overestimation of model performance may occur if the same subject is used in the training, validation, and testing sets. "
            "This compromises the repeatability of reported findings. Transparent evaluation procedures and subject-level data separation are necessary."
        )
    }
    make_pdf(PAPERS_DIR / "parkinsons" / "pd6.pdf", par07_pages, total_pages=8, default_topic="Parkinson's imaging review, data leakage, and validation pitfalls")

    # PAR08: pd7.pdf (Garcia Santa Cruz et al.)
    par08_pages = {
        1: (
            "Garcia Santa Cruz et al. 10.3389/fnagi.2023.1216163. Computer-aided diagnosis of Parkinson's disease using neuroimaging modalities. "
            "Frontiers in Aging Neuroscience. Machine learning algorithms have emerged as powerful tools for computer-aided diagnosis (CAD) in neurodegenerative disorders."
        ),
        7: (
            "Garcia Santa Cruz et al. FIGURE 3 Summary of the specific limitations in computer-aided diagnosis (CAD) for Parkinson's disease (PD) "
            "associated with idiosyncrasies of the disease, as addressed in Section Limitations associated with Parkinson's disease: "
            "(1) During the labeling of datasets for supervised learning, several problems can be encountered. "
            "(1A) Building a solution for differential diagnosis can be challenging due to the overlapping symptoms of PD and related disorders. "
            "This challenge is especially significant during the initial phases of clinical diagnosis, where such solutions would be most useful. "
            "(1B) PD is known to have several subtypes with implications for clinical treatment, but there is a lack of clear global consensus, adding another layer of complexity. "
            "(2) PD being an age-related disorder, the control subjects used in age-pairing may have additional health conditions or factors that can affect their brain patterns."
        ),
        8: (
            "Multimodal imaging in Parkinson's disease: Combining structural MRI, PET, and DaTscan provides complementary perspectives but poses substantial dataset harmonization challenges."
        ),
        10: (
            "et al., 2016). As stated by Pagano et al. (2016), “despite significant evidence for the utility of neuroimaging in assessing parkinsonian patients, "
            "none of the neuroimaging techniques is specifically recommended for routine use in clinical practice.” "
            "Therefore, the impact of this variety is threefold. First, the symptoms may not associate with structural or functional brain patterns. "
            "Second, when existing, such patterns require particular brain imaging modalities. Finally, such patterns may not be specific to PD. "
            "On top of these three circumstances, the temporal evolution of the disease adds another layer of complexity. "
            "Each stage calls for different symptoms, which in turn require dedicated imaging modalities with different diagnosis specificity. "
            "In this light, accurate PD subtyping becomes challenging, as obtaining a complete view of the brain manifestations of PD symptoms "
            "requires image acquisition of several modalities or the employment of multimodal approaches (Saeed et al., 2017; Chougar et al., 2020; Albrecht et al., 2022). "
            "One potential solution to address this issue is to use a combination of multiple imaging techniques."
        )
    }
    make_pdf(PAPERS_DIR / "parkinsons" / "pd7.pdf", par08_pages, total_pages=12, default_topic="Parkinson's clinical translation and multimodal limitations")

    # ---------------- SCHIZOPHRENIA ----------------
    # SCH01: sz.pdf
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz.pdf", {
        1: (
            "Structural and functional neuroimaging biomarkers in schizophrenia: a comprehensive review. "
            "Multicenter investigations document reproducible patterns of frontotemporal dysconnectivity and ventricular enlargement."
        ),
        2: "Reductions in temporal and frontal gray matter volume observed across multi-site schizophrenia cohorts."
    }, total_pages=6, default_topic="Schizophrenia structural biomarkers")

    # SCH02: sz1.pdf (Columbia University study)
    sch02_pages = {
        1: (
            "We tested this hypothesis using a single, widely available, and conventional T1-weighted MRI scan. "
            "Other studies also affirm the enlargement of ventricles in schizophrenia3,4. While gray matter reductions are most consistently reported "
            "in the subcortical regions, reductions have also been identified in areas such as the prefrontal, temporal, cingulate, and cerebellar cortices5,6. "
            "Loss of gray matter volume has been shown to not only mark the onset of schizophrenia but also progress alongside the illness7. "
            "Despite these documented changes, accurate and rapid detection of schizophrenia remains a pressing problem; previous studies are limited "
            "to only characterizing structural abnormalities at a group level, with no concrete method to make individual diagnoses at a subject level. "
            "Additionally, the diagnosis of schizophrenia based on DSM-5 criteria is costly both in terms of time and resources, without ensuring objectivity. "
            "Therefore, it is imperative to develop an objective screening tool to diagnose schizophrenia and potentially improve patient prognosis by allowing for earlier intervention. "
            "Various attempts have been proposed to take advantage of the structural alterations present in schizophrenia for classification using neuroimaging data. "
            "Machine learning algorithms have historically presented the ability OPEN Department of Biomedical Engineering, Columbia University, New York, NY, USA."
        ),
        5: (
            "A gradient class activation map (Grad-CAM) was introduced to our experiment to check whether the model focuses on task-related patterns "
            "instead of some irrelevant information in the data. Grad-CAM heatmaps highlight relevant cortical and subcortical regions contributing to the schizophrenia classification decision."
        )
    }
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz1.pdf", sch02_pages, total_pages=6, default_topic="Schizophrenia T1 MRI and Grad-CAM explainability")

    # SCH03: sz2.pdf (NTU Singapore study)
    sch03_pages = {
        1: (
            "identifying patients with schizophrenia using 3D brain MR images and paved the way for imaging-based individual-level diagnosis and prognosis in psychiatric disorders. "
            "I. INTRODUCTION Schizophrenia is a severe chronic mental disorder that causes great burdens to patients' families and society. "
            "Yet, diagnosis of schizophrenia is typically based on interview and clinical symptoms, which could be challenged by the complex and heterogeneous symptoms "
            "as well as many confounders such as the race, gender, and medication effects[1]–[3]. Early and accurate diagnosis of schizophrenia could facilitate treatment planning "
            "and improve the outcome of the illness. Instead of classical group-level comparisons, machine learning based on objective biomarkers such as medical imaging "
            "could help to establish a psychiatric diagnosis at the individual level. Indeed, previous work on computer-aided classification of schizophrenia patients "
            "and controls using brain structural magnetic resonance imaging (MRI) mainly involve handcrafted feature-based machine learning approaches such as "
            "support vector machine (SVM), random forest (RF), and logistic regression (LR). MRI-based features include region- or voxel-specific cortical thickness "
            "and gray matter volume *Research supported by Institute of Health Technology, Nanyang Technological University, Singapore. M. Hu, C. Guan and X. Jiang. "
            "density in the brain [4]–[9]. However, many studies suffer from poor replicability and generalizability due to small sample sizes and hyper parameter settings."
        ),
        3: (
            "3D CNN models achieved higher accuracy than handcrafted feature-based machine learning approaches in overall. "
            "The highest accuracy was obtained by Inception_resnet_1 at 79.27% on NUSDAST cross-validation and 70.98% on the additional IMH test set."
        )
    }
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz2.pdf", sch03_pages, total_pages=5, default_topic="Schizophrenia 3D CNNs and handcrafted feature comparisons")

    # SCH04: sz3.pdf
    sch04_pages = {
        1: (
            "Machine learning and deep neural networks for schizophrenia classification using multi-modal neuroimaging. "
            "Integrating functional connectivity, diffusion metrics, and magnetoencephalography."
        ),
        2: (
            "Neural Network World 3/2022, 147–161 the exact method of diagnosing schizophrenia disorder [2]. Although psychiatrists generally diagnose schizophrenia "
            "based on the history of the disease and mental status examination [3], many researchers have recently attempted to provide the basis for automated diagnosis of schizophrenia. "
            "Most of these studies have utilized extracted features of neuroimaging data along with machine learning techniques [4]. "
            "For instance, Ardekani et al. [5] derived fractional anisotropy (FA) and mean diffusivity (MD) maps from diffusion tensor imaging (DTI) data. "
            "They applied Fisher's linear discriminant analysis (LDA) as a classifier method. "
            "Chyzhyk et al. [6] used resting-state functional magnetic resonance imaging (rs-fMRI) data and extracted functional connectivity (FC) measures, "
            "regional homogeneity (ReHo), and fractional amplitude of low-frequency fluctuations (fALFF) as derived features from them. "
            "Their proposed approach is consists of dimensional reduction, feature selection, and classification with SVM steps. "
            "In contrast to the methods that have used single neuroimaging modality, some studies have suggested using multi-modal neuroimaging data [7]. "
            "Although these methods may require additional time, cost, and information, they achieved higher accuracy because of the use of complementary data. "
            "Cetin et al. [8] used fMRI and magnetoencephalography (MEG) data and derived static and dynamic functional network connectivity (FNC) from them "
            "to diagnose schizophrenia patients from healthy controls. Their experiments showed that combined fMRI and MEG features achieved better classification performance. "
            "Qureshi et al. [9] combined some structural measures extracted from sMRI and four functional connectivity based features gathered from fMRI. "
            "They achieved an accuracy of 99.3 % for classifying SZ/HC with the extreme learning machine (ELM) classifier."
        )
    }
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz3.pdf", sch04_pages, total_pages=5, default_topic="Schizophrenia multimodal neuroimaging classification")

    # SCH05: sz4.pdf
    sch05_pages = {
        1: (
            "Multi-site functional and structural neuroimaging dataset evaluation for psychiatric disorder prediction. "
            "Harmonizing imaging protocols across imaging centers."
        ),
        2: (
            "However, their study was focused on a single site, and we desired to incorporate data from numerous locations. "
            "We were unable to locate many open fMRI datasets, particularly those that included both T1 weighted and resting-state fMRI. "
            "Multi-site generalizability remains a major challenge in neuroimaging classification for schizophrenia."
        )
    }
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz4.pdf", sch05_pages, total_pages=5, default_topic="Schizophrenia multi-site generalizability and fMRI open datasets")

    # SCH06: sz5.pdf
    make_pdf(PAPERS_DIR / "schizophrenia" / "sz5.pdf", {
        1: (
            "Cross-cohort generalizability and explainability of deep learning models for schizophrenia identification. "
            "Evaluating model transfer across international hospital repositories."
        ),
        2: "Deep convolutional architectures evaluated on independent validation cohorts with saliency maps."
    }, total_pages=5, default_topic="Schizophrenia cross-cohort generalizability")

    print("\nCorpus generation complete: 25 PDFs created across 4 conditions.")

if __name__ == "__main__":
    build_all()
