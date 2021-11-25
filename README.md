# On Generating Transferable Targeted Perturbations (ICCV'21)
[Muzammal Naseer](https://scholar.google.ch/citations?user=tM9xKA8AAAAJ&hl=en), [Salman Khan](https://scholar.google.com/citations?user=M59O9lkAAAAJ&hl=en), [Munawar Hayat](https://scholar.google.ch/citations?user=Mx8MbWYAAAAJ&hl=en&oi=ao), [Fahad Shahbaz Khan](https://scholar.google.ch/citations?user=zvaeYnUAAAAJ&hl=en&oi=ao), and [Fatih Porikli](https://scholar.google.com/citations?user=VpB8NZ8AAAAJ&hl=en)

[Paper](https://openaccess.thecvf.com/content/ICCV2021/papers/Naseer_On_Generating_Transferable_Targeted_Perturbations_ICCV_2021_paper.pdf) ([arXiv](https://arxiv.org/abs/2103.14641)), [5-min Presentation](https://drive.google.com/file/d/1KSe9Zp6_uADkMgXQkHpoKtN85Q1sX_Wv/view?usp=sharing), [Poster](https://drive.google.com/file/d/1kIMIwUHcaHYpWiphHmT38_S0ruS2TrrG/view?usp=sharing)

> **Abstract:** *While the untargeted black-box transferability of adversarial perturbations has been extensively studied before, changing an unseen model's decisions to a specific \`targeted\' class remains a challenging feat. In this paper, we propose a new generative approach for highly transferable targeted perturbations (ours). We note that the existing methods are less suitable for this task due to their reliance on class-boundary information that changes from one model to another, thus reducing transferability. In contrast, our approach matches the  perturbed image \`distribution\' with that of the target class, leading to high targeted transferability rates. To this end, we propose a new objective function that not only aligns the global distributions of source and target images, but also matches the local neighbourhood structure between the two domains. Based on the proposed objective, we train a generator function that can adaptively synthesize perturbations specific to a given input. Our generative approach is independent of the source or target domain labels, while consistently performs well against state-of-the-art methods on a wide range of attack settings. As an example, we achieve 32.63% target transferability from (an adversarially weak) VGG19<sub>BN</sub> to (a strong) WideResNet on ImageNet val. set, which is 4x higher than the previous best generative attack and 16x better than instance-specific iterative attack.*
> 

## Updates \& News
- TTP Training is available (13/07/2021).
- TTP Evaluation against state-of-the-art input processing defense, [NRP](https://github.com/Muzammal-Naseer/NRP), is available (13/07/2021).
- TTP Evaluation against unknown (black-box) training: [SIN](https://github.com/rgeirhos/Stylized-ImageNet), [Augmix](https://github.com/google-research/augmix) is available (13/07/2021).


## Citation
If you find our work, this repository and pretrained adversarial generators useful. Please consider giving a star :star: and cite our work.
```bibtex
@InProceedings{Naseer_2021_ICCV,
    author    = {Naseer, Muzammal and Khan, Salman and Hayat, Munawar and Khan, Fahad Shahbaz and Porikli, Fatih},
    title     = {On Generating Transferable Targeted Perturbations},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
    month     = {October},
    year      = {2021},
    pages     = {7708-7717}
}
```

### Contents  
1) [Contributions](#Contributions) 
2) [Target Transferability Vs Model Disparity](#Target-Transferability-Vs-Model-Disparity)
3) [Pretrained Targeted Generator](#Pretrained-Targeted-Generator) 
4) [Training](#Training)
5) [Evaluation](#Evaluation)
7) [Why Augmentations boost Transferability?](#Why-Augmentations-boost-Transferability)
8) [Why Ensemble of weak Models maximizes Transferability?](#Why-Ensemble-of-weak-Models-maximizes-Transferability)
9) [Generative Vs Iterative Attacks](#Generative-Vs-Iterative-Attacks)
     * [Key Developments made by Iterative Attacks](#Key-Developments-made-by-Iterative-Attacks)
     * [Key Developments made by Generative Attacks](#Key-Developments-made-by-Generative-Attacks)
10) [Tracking SOTA Targeted Transferability](#Tracking-SOTA-Targeted-Transferability) 
11) [What Can You Do?](#What-Can-You-Do)  
12) [Visual Examples](#Visual-Examples) 

## Contributions
1. We designed a new training mechanism that allows an adversarial generator to explore  augmented  adversarial space during  training  which  enhances  transferability  of adversarial examples during inference. 
2. We propose maximizing the mutual agreement between the given source and the target distributions. Our relaxed objective provides two crucial benifts: a) Generator can now model target ditribution by pushing global statistics between source and target domain closer in the discriminator's latent space, and b)  Training is not dependent on class impressions anymore, so our method can provide targeted guidance to the generator without the need of classification boundary information.  This allows an attacker to learn targeted generative perturbations from the unsupervised features.
3. We propose a diverse and consistent experimental settings to evaluate target transferability of adversarial attacks: [Unknown Target Model](#Unknown-Target-Model),  [Unknown Training Mechanism](#Unknown-Training-Mechanism)
, and [Unknown Input Processing](#Unknown-Training-Mechanism).
3. We provide a platform to track targeted transferability. Please see [Tracking SOTA Targeted Transferability](#Tracking-SOTA-Targeted-Transferability). (kindly let us know if you have a new attack method, we will add your results here)

<p align="center">
     <img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/concept_fig.png" > 
</p>

## Target Transferability Vs Model Disparity
<sup>([top](#contents))</sup>
Our analysis indicates that there is a fundemental difference between Targeted and Untargeted transferability. Model disparity plays a critical role in how the targeted perturbations are transferred from one model to another. Here is an example (average transferability accross 10 targets):

<p align="center">
     <img width="400" height="300" src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/resnet_within_family.png" > 
</p>

- Observe that transferring targeted perturbations from a smaller model to a larger one (e.g., ResNet18 to ResNet152 is difficult as we increase the size discrepancy. This phenomenon holds true for untarget transferability.
- Targeted transferability trend remains the same even from larger to smaller models. For example, target transferability  from ResNet152 to ResNet50 is higher than from ResNet152 to ResNet18 even though ResNet18 is weaker than ResNet50. This is where targeted transferability differs from the untargeted case. 
- It is important to note that this behavior is common accross all targeted attacks (iterative or generative) which indicates that this property stems from disparity between the source and the target model. For example, depth between different ResNet models or skip connections between ResNet and DenseNet family reduce the targeted transferability. 
- We note that the dependence on disparity in model architectures can be mitigated with ensemble learning from the models of same family. Targeted transferability from ensemble of e.g., VGG models can be higher than any of the individual VGG model. This is important because an attacker can learn strong transferable targeted patterns from weak models.


## Pretrained Targeted Generator
<sup>([top](#contents))</sup> 
*If you find our pretrained Adversarial Generators useful, please consider [citing our work](#Citation).*

Class to Label Mapping

```
Class Number: Class Name
24: Great Grey Owl
99: Goose
245: French Bulldog
344: Hippopotamus
471: Cannon
555: Fire Engine
661: Model T
701: Parachute
802: Snowmobile
919: Street Sign       
```
### Targeted Adversarial Generators trained against Single ImageNet Model.
This is how the pretrianed generators are saved: _"netG_Discriminator_sourceDomain_epoch_targetDomain.pth" e.g., netG_vgg11_IN_19_24.pth means that generator is trained agisnt vgg11 (Discriminator) for 20 epoch by maximizing agreement between the source domain (natural images from ImageNet (IN)) and the target domain (images of Grey Owl)._ 
|Source Model|24|99|245|344|471|555|661|701|802|919|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|VGG11|[Grey Owl](https://drive.google.com/drive/folders/1Xd-h6NRKMXVBWkPgc5vy8X5sMlw442Zk?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1ZiadyYoTolB1dplGWmciVyzTBEQCh5WD?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1PFqZfdeP5QQYUSsva_was92Dzr6qvK6S?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/19x5gfKZ28k66pggD6mN8pqyiaVewVsD0?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1bdxAkO9yGNOeURpkRs1L2y5L2N3d57TL?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1lwkzm3AnKipboBoadDH6O2wt9ZNC-Gk3?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1uiSutPu4JwB6djZAU9pD51QpqgBneefs?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1SyqKpPNYI9WrL4igrhQCb3AcHm4HM0vC?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1vn9OPYDA_TpVJ8RXQPktfmnMtIxlIbkW?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1IXLnR4-0XulRBdRtOp45wUSy2LNO4n8F?usp=sharing)|
|VGG13|[Grey Owl](https://drive.google.com/drive/folders/1_EpJKucMJeEUvo4G5W4Taqfz4tQyNQtC?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1OmCMBYZONVr2CFQ-F4TX3bj1nLxWejgE?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1fK4fMiOOMNlbxS9Wz6whZrAR4z_TWCK1?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1CZHd5DgeTB4LQUMTRDCyP_TtXL1Dulq-?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1ehff0pY_q2bs3RaCBPubDQWeIypF28kZ?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1ER0uvkzWyE56i2i4d0DM67ZhejKXQrXF?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1pli4J8xAHOxsXJFkz_wl8HrpVZbw-Xdg?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1m700WOQvmjTY0x8WhWhmLdrBVBEY6Wqr?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1FJcDWkcWJl_yTFp4Jc3rPKWnu7_0_3d4?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1UOA0ClK3EbvuLDIfNBShA3iFI11DfEdb?usp=sharing)|
|VGG16|[Grey Owl](https://drive.google.com/drive/folders/16GnlZRKsr1Qc-Cc30rBM1DxSbNpAfPz7?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1SSBubg8IoGIRwkG9KbDfNWgtRaaDhwnm?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1RYpLMPstFFHfajogpoAn6Fx3A9cC1iDU?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1NFxxQ3EnhkxF9j7337kd17D_gIzW8YGh?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/103JXrnjy9PMNUnrxsT-HbJ55ay9it9CB?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1_AGPdMLEet_JC5IV-JpmmiBvNLFwJOtk?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1ERHDAmQUs_z6JXLRMwf6GIgYQYT8mvNT?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/19PrJQWrsYlBwLR6paJAnD0t2xZm6p-6O?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1DzBgLLLwdWeyoqnyIjFtvUc4M4GDzwcY?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1cqEe_U579LbkfjsyDZH_w7ucAZnbSC0j?usp=sharing)|
|VGG19|[Grey Owl](https://drive.google.com/drive/folders/1k6DfRUx_xYqiGbJQeMDepHfUUPfu_xVb?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1_5DqBfoejnlNuYvEmZS6IT3u21yPX6KJ?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1UYPMD92KFM4OLVuCW85a108GwqQPcjtx?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1PVcE4AAksj4gIdsq5j4wkC9zRLd2gNFY?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1AgJYYP9HuqIEH2RD4D4wX9jj_j4S_Ka4?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1PZ3O-J2ypXnGRV9z03fzZzwb0qiojZcQ?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1f_RMrSe27XRYfrKG12Io0MxelJDogHp1?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1A3oMe5hARWynkjkArLbsvO1lK_MEaKVa?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1ORoXo0eSiZxYVAxBgA4r5GU7L6ufVv2S?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/11Ko8lO454kodyQE8__gPo83JYRJObpod?usp=sharing)|
|VGG11_BN|[Grey Owl](https://drive.google.com/drive/folders/1xCPG2MAFd-BXw37946WRV7OGzirRFp1d?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1EXylkOoqGTkYtQRnrJiqhsngyL9ak9v9?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1FWxlvkBgukj32H3ZKAdS7u2bQsmpEBt1?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1UQ-o-TdJdL1qtYXq-fogvaCGUk7BDDlp?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1h9m6orTqkFC7caj_oeuA3WferNAX_I6I?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1Se1zJ0wLzEQM0B0i3AcOU1SAVOPJUmgu?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1AMp9eT3J3EChDC6ikbjkmN52nNLuIf_E?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1VrLyOJuW5ddGTXAirCjL37Yxspap2HzB?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1_S-nnESnnGF7Npwr6hxxIoxCs9kDmhhL?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/17W8m31T2Q5ZSZTP5SdEVJup6ggj7CmXB?usp=sharing)|
|VGG13_BN|[Grey Owl](https://drive.google.com/drive/folders/1RgPZHD1oyq9jmkMQvdTI8tTe_ztdGdJ3?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1C4u2iMmYIe6UgkzjBeuhv99WmvkjvOJs?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1cadyJN9WQKQtHtdgoseDXtPR5b153Xne?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1q-JvcsK1azFNxIP0kQ60ckyigQMSuGht?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1XpoBrId11DsNOdLaukU78FeH6q5_rD9n?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1g5fv_VhMuiW7JlJGpwo5657_Bsshtmt-?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1Csa3kylpRZpohedNERnaV2CIi0hp8YMr?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1u6qzdDENin8MWKsAhEw8-4em_oj4MBm5?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1xGxk6YMmJSqh11IPf-8hgaYgMSZRWQlw?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1DrMQyPMMPmWwWRhsnJ8RWmvtzFZstMAK?usp=sharing)|
|VGG16_BN|[Grey Owl](https://drive.google.com/drive/folders/1HmAgtC4Ye3ZO34b1297glF7F1h4PA7V6?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1e9cTNHl7qetApusqWnf6z7S91xuyFuiV?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1L7n9IRYet0jWiYQPvIm_pV8TcIfx9aVe?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1gLczwB8FRrOgtYTWzNDAAp24C90Mt6YS?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1py85L8iUzLGNVbux2ky5H4oAS7fBvyMD?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1uYPwoA7Sg2zkzJz3AyQH8OUV-0s4snYu?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1c9cRxUVd6XCgg1AnMQD0wzKyTHNA0ZDo?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1Mg_RHsnOC_r30ILtKtKdnoU51hgAEzsI?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1e3OLzQCy4VEtgJ2awR1ALPGhVTCMgCYD?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/11yKcrjw9c5yHeAAt9jzyW5sshrIxxqUW?usp=sharing)|
|VGG19_BN|[Grey Owl](https://drive.google.com/drive/folders/16psM3ufNw-ZGSufuMQeXrLNm8yWdk0Wx?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1kFB2aUTGd6yxscz9ZmqFjJtuwp5-GUA_?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1Ajg4CwOSDbzklUWAZHcC1nUtUB2v7nff?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1NIdN1UZbRBQ0sv7Lpf_tBF2jhAltxLud?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1bzuj4A7eT_Goj905cxZ_oLAxH3TWk8DJ?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1gN2jz0sWzoI6fnYjRVkQ5lGuhHJ7excC?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1CNX0s62lTikcS50oo3KkJ_FOTIZh3_Qi?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1w6GJddcCFYZxjSlLws8ZEQ1zAJLF1smj?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1b766d_V63dyFPMMeYDH_smWYScDwEVNu?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1atGItbmG8G-4atYsir-oW5VqqU28hvUN?usp=sharing)|
|ResNet18|[Grey Owl](https://drive.google.com/drive/folders/1yjThKPBch8n4jDbCFpnGdiHRQ3ScD94K?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1pRzQ7HOR9k881vFv-f9WjFr2Ql1xiNHL?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1VKd5BlHBdvgjKO6IIjH1i6SjbCKkmTs0?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1g_kFrhly0jhMVq5xOaPqjTXggDWA6eUl?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1deScnNWBe1zYFY53Rpe3a1Jws6E8DC0o?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1WF-dI3KfCVi3MAKKhsDxVsIxHEE-lTgt?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1M0Y-1OSWuT55dvsc4N3qleypvW9DYEZT?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1j5ECPuIgcdNSCyEQEePVxOK84vm0zj1o?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1CmwCQ0F4oYP6TsegyJy0KmwvNdZaWHlc?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1hDAC-M6bKwhG3f7VoRoHpPTe1gPnFMf5?usp=sharing)|
|ResNet50|[Grey Owl](https://drive.google.com/drive/folders/1uMLsSCnKzojh__5pkN6ZMoWi17NcoqLI?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1Nwf_Nv0bNKlA5aJOODWfHknEIYtQuJuQ?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/15D5Z6J_tM98nEmcMiT45XjjkEj98PALw?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1xh_vVjeivwrEjJKSyeJ53-u3G56RUnhT?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1XjFlEVQ-Yx0EZ1ABP16wa5cWWi5-wjKU?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1V5wSBB5KUsDaFvwzBGDQv6JWBsErtsmZ?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1sfWPoCQOjpH56EHVkfiGsSbM0oIjYuom?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1IHK6PQ4PsDaSxKaFIxeTvI9cv8VvJFLp?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1C5BV1iADj28OSeXCDArTp-zuPlMhyfSC?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1rCS-r0IHKK4ySSWRj57xc4srRirkB0CJ?usp=sharing)|
|ResNet101|[Grey Owl](https://drive.google.com/drive/folders/1ttvWfydrg4DoOrB53QtzvcUv1k5GI6Vb?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1GUVCRqMsb_8tUrl3B4ZK-FDQygfnxIB-?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1K7cJcp-rCwHS7WkQe8nlDZF2xJBwvZEQ?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1eFIi9rZeOhafJytNvWyQ1d2U7oLzdVvD?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1XRwjgn09Ag2AYEHPOCn426t8hLfcwuOG?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1Z4eKJ2lvhElpAOGZxIQ3rn0iTuKMkj0y?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1CQc8PpVcXsPgjWl968l1p32WgvJKypi3?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1sEcDQ7am9AiWTh_V2Zvr_5muGDAU3FUA?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1QcApy1B2LWp3U5IYdwLykeAUEBe0GLAW?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1QuY4LZk8YstwtETr9YlUR6vxU63nuApS?usp=sharing)|
|ResNet152|[Grey Owl](https://drive.google.com/drive/folders/1IJbstlO4qv8PViibGHUFpLHFHS0rGOzq?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1jtGi6vjdUo8niIvJQEEX6xldFo9vZ6iI?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1BLkx7zeYqRwoUzM9Me_Do923GutxdUjd?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1igu8Z1qGFDvIbTSeiTpQ73p4WZtgCf1U?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1cy-23vWys0viauUaZS4QZ9ajc6dBHMK8?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1A58flmCP4q0PDgrqy5MPXtZxBpqbWI6H?usp=sharing)|[Model T](https://drive.google.com/drive/folders/14Khp76D0ROK32ogKO6TOW_c-1tzUJKfl?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1vxE4ok3u_6O_AdM268754lbm509n2rPi?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1xcE2is2T1jwUdL9uCutlR7ThUilJ8l0u?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/14bB0osF6XFlTtkRbcZ4viTUr-Wob-0hr?usp=sharing)|
|Dense121|[Grey Owl](https://drive.google.com/drive/folders/1MmMS5U3EeFYMEPA1mj0DCv_nusvdQVtR?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1wvrQ0CcG0IRb6nZoyNxrjaKEsxdmHax5?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1a2OCPLX8w988FZRGhGsDobXcr1VYMLUE?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1YhKKSPEktGPmPybu-onQMO32cXAC4r4o?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1XKcxMsE_baBaUpGZxMc4qoXgg_PNkWpR?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1zXfcgeT7axAReaQ6fHDy1ehVR2dY2fvE?usp=sharing)|[Model T](https://drive.google.com/drive/folders/15d2_NbxhQ4_7LAGZwJTlmTWVZVMxE_Ie?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1UV4N6XSuyPDq8pk0Nm-PqwaYtRqCu2Js?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1XGnoJU7JJvP7u9PYAm62lZ-BtxiUT_6c?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1qv1h_Q9MjmqfURPNemgBRfxFswscAhm0?usp=sharing)|
|Dense161|[Grey Owl](https://drive.google.com/drive/folders/1Wbzak1AZHw4k0yiILJyXQQVbTNCbvTbX?usp=sharing)|[Goose](https://drive.google.com/drive/folders/12ssCGhshTT-wH8iR3uU_NOEpub3CySJT?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1ZADa2JnBOLzeL0Ua7aEXqQGXITRI0JS8?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/16HSCehbMBVxTGLEIZ0CVvc583q0jJOVq?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1DOVwqOC0Q4-4JrZfm0uJ_0vIO79kJaDj?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1ZrRYFKGao8-ZFxt6FXyFk3WFb2Ehsu0d?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1GILObgWEODeaMwpLfZuOj34fLROYAHyn?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/13p4lAQlMoWS9Fv75nyBAsd5Kvm8ulJ03?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1zLoHhuDwO63lQ-LAh8vhRnR3CqtQJldv?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1rbHHMeCNC9YIw5tIIv9tgLOKyVYRe1JQ?usp=sharing)|
|Dense169|[Grey Owl](https://drive.google.com/drive/folders/1RGnB7HWdA38iFIgy03XDdJkJasgsyoiv?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1O-9mWpOVbgB3B5FqHpEOvURUtG0gAQH2?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1Aggq3kfcyH0G1dkvWi6e1yKh0sPzqsmH?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1TOi2YuZp_amOYEAk4xDK21TXtJD7_1Eh?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/19uy45t2RPzvUmyedIl38H8Ojo7UXCQES?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1rrGQoZdhnOLGV3nO0voVU8V467fbZbLY?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1kvWhXu8CjtS6kP1QFGEpTgBgyx5IUScd?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1Trl60kmD7xnyHiZhtoPGRufi_YgGw8n5?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1Z4SjPWg7iVg6Tjc-PIursv5zqJHhvApt?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1rkoJRP5zVVp2YS-dG63_TgMz2udUKV3e?usp=sharing)|
|Dense201|[Grey Owl](https://drive.google.com/drive/folders/1hyiRZMbOJMPUgm1NOKXM0solKPXu0_z8?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1XIwjeEE-A-u5njeO1tjGRDW5CGMz2iTj?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1wobu6mNBQXCE8rCh1TmH69JCUSkgLO0S?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/16qveFxjmsEp1DfvfjABNCKhDyChviYBN?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1HxDKOGzr3C2X57jNakUlUO06qjxF1pC6?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1l5KJrNNM0htOYLU8KS0KCzf0ODaUQpRV?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1IR1V9eH8CneeGlc2A2_qf9GM5zx0fzQ6?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1SQjP39kUInCxU_1eYVzEcnq6DefhG7t7?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1jpKICDLh45-e-tEeY3k-w-z50EG5Okn6?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1cbxrc_mg13okCXnQeDeSV1Kz24tNTmmt?usp=sharing)|

### Targeted Adversarial Generators trained against Ensemble of ImageNet Model.

|Source Ensemble|24|99|245|344|471|555|661|701|802|919|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|VGG{11,13,16,19}<sub>BN</sub>|[Grey Owl](https://drive.google.com/drive/folders/1WK-4izLIyVNvEBNAluUILo7fZCvpwdlV?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1I6dyD8R7MnU4PaEaSzcWf9uRiglCq150?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1v4GRQqZ0bEARsEPMIE3mr5yKuLn_EXR8?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1p-kabJhHuoCgo2dNSwMDfTd2ne4jgV-n?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1-YcttOAVy3ZJTLcYUJYG_uHyP_NRhtO-?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1ef9tNkhJnMtDw_x5nd308c98XePrgzGh?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1eZbLQUhkgbc0FYOdrSU70G-4OUpMJUNW?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1D_rWCtZIZJFh7O6xiRWK1FnL7NnBQuB_?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1AQYl1Me2qsibXzK_gV3VXsNEn4RrZHLw?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1s8LtT3UKRedCZ0sxOYh5oZvJ6PB35U2U?usp=sharing)|
|Res{18,50,101,152}|[Grey Owl](https://drive.google.com/drive/folders/1Y1J2tSfMUwQ8zfHdUUlQjCCKdEe9Nldh?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1mO198an6-a8mVqHc6wfLULe9Y8jRaKu4?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1M84sjeLsM-6f_s6hVVWhH5sKlLtBT3_9?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1qC42bAUTZJ7-SO40W-wtgsZzKTVgBrOT?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1D7iky2kRHyuh5R6V-yu25AhC2TLP8MbO?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1uYXXua68Y-Ni0RzGsOH7qBRz-hnBFqwe?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1OPURdtuay3rMxVznwerZ6PCC8V0mY-9z?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1oHweeXbVJ1v3UVYCy_BXvKSrWPwKKe2e?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1EnI4tJ9sVQ0XHU6RhlyA-KaQRJ_aVYVN?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/167JunY-n9LO9g1yCjQz0zVGLzUMRVM43?usp=sharing)|
|Dense{121,161,169,201}|[Grey Owl](https://drive.google.com/drive/folders/1Xv08sE8hd12mN4g5q4dN3BEokG68wJUF?usp=sharing)|[Goose](https://drive.google.com/drive/folders/1_eQTXoP4GLrmO8PMPxluGA_B-ZrOxEAg?usp=sharing)|[French Bulldog](https://drive.google.com/drive/folders/1wQwo36cmXUw9-dYpOLqYwUeWkpdc9dil?usp=sharing)|[Hippopotamus](https://drive.google.com/drive/folders/1664xKwTRBHVCu-i7jZs2ScItySSjJUVp?usp=sharing)|[Cannon](https://drive.google.com/drive/folders/1CWAe_au0oGO-gVeo2icAqoo7fZAcWCmB?usp=sharing)|[Fire Engine](https://drive.google.com/drive/folders/1NSWShM0wg-DAFELlZQy6KYgZ_Y7dJpoM?usp=sharing)|[Model T](https://drive.google.com/drive/folders/1eMX-vxkJDJrwnjG-NbFZeOUhU2bEKhDg?usp=sharing)|[Parachute](https://drive.google.com/drive/folders/1i5edSMj7-zPrH315l2DioAZi-w3H4KXU?usp=sharing)|[Snowmobile](https://drive.google.com/drive/folders/1w0cV-5sdg6_JLa0ms1BzgY6Em0eSMpyR?usp=sharing)|[Street Sign](https://drive.google.com/drive/folders/1g8Vtc8M6Zc0qqwDzgzwt1eCreKqVTOvd?usp=sharing)|

### Targeted Adversarial Generators trained against ResNet50.
We trained generator for 100 targets but for ResNet50 only. These generators are for rest of the 90 targets distributed across ImageNet Classes.

|Source Model|3|16|36|48|52|69|71|85|107|114|130|138|142|151|162|178|189|193|207|212|228|240|260|261|276|285|291|309|317|328|340|358|366|374|390|393|404|420|430|438|442|453|464|485|491|506|513|523|538|546|569|580|582|599|605|611|629|638|646|652|678|689|707|717|724|735|748|756|766|779|786|791|813|827|836|849|859|866|879|885|893|901|929|932|946|958|963|980|984|992|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|ResNet50|[Tiger Shark](https://drive.google.com/drive/folders/1fI_XsbodMl8Is2sFdr5ZU9Qcou60xXOC?usp=sharing)|[Bulbul](https://drive.google.com/drive/folders/1r4xfWgjs9tdZtOwU5h6lOJcFoj5cYD5F?usp=sharing)|[Terrapin](https://drive.google.com/drive/folders/1rT60MIZHvz6-AzmFuk5VMdAgZUO4iC9K?usp=sharing)|[Komodo Dragon](https://drive.google.com/drive/folders/1htoZFTWngUohv8GUNX0nFN6yNN7daun6?usp=sharing)|[Thunder Snake](https://drive.google.com/drive/folders/1O00Hopt0IYQVSyPXQsG_Evg07oW5pXCn?usp=sharing)|[Trilobite](https://drive.google.com/drive/folders/1C9RgAmvYSyh48FIUs0tMdeg4yZcjmsdK?usp=sharing)|[Scorpion](https://drive.google.com/drive/folders/1-MCYTM-Q2qeuoP99aUrXPTnyUvWvGdDi?usp=sharing)|[Quail](https://drive.google.com/drive/folders/1wU77D8Cc2UcNVCvCdS8bhPwi634HkJ7S?usp=sharing)|[Jellyfish](https://drive.google.com/drive/folders/1oIWd_iqvC-MXCOJuyhNL5WTwPjTGqsFH?usp=sharing)|[Slug](https://drive.google.com/drive/folders/1UKA2_wRTlPkm0BkqyWvKgcKtXPXWy_ze?usp=sharing)|[Flamingo](https://drive.google.com/drive/folders/1d7e1eY7ksXuCmGNsPghsgN9y9_uqZ5ME?usp=sharing)|[Bustard](https://drive.google.com/drive/folders/1hVsbfCgVJi_qw50_liPHgcwwYbFlqqec?usp=sharing)|[Dowitcher](https://drive.google.com/drive/folders/1ExF72qzFb5mU4pu4F99Mrj8iXRqCsMPB?usp=sharing)|[Chihuahua](https://drive.google.com/drive/folders/1hI7NkCWpDlZC9xCgTTudhunOUHb6je7n?usp=sharing)|[Beagle](https://drive.google.com/drive/folders/14cQ1hfxm6FbGNakgLGfFfPkkJwQ5gvde?usp=sharing)|[Weimaraner](https://drive.google.com/drive/folders/1uJZxqHU-TnI0SsaMaLyot2s4qig-wjAb?usp=sharing)|[Lakeland Terrier](https://drive.google.com/drive/folders/1taRysT4irnTcg7kVDhuaJRGESaaw2wnp?usp=sharing)|[Australian Terrier](https://drive.google.com/drive/folders/1Lz8xXjMiBtBzHdj4KSRzLbYTh_mcJN3W?usp=sharing)|[Golden Retriever](https://drive.google.com/drive/folders/1jDkhmf4TujTGSi_Z90kkowuZRZSgulK0?usp=sharing)|[English Setter](https://drive.google.com/drive/folders/1z19p93VfdqcthIToH4w_qxg153mXMFXD?usp=sharing)|[Komondor](https://drive.google.com/drive/folders/1V9avSlR39V97lHBbM-g6zKcxoHNo62vt?usp=sharing)|[Appenzeller](https://drive.google.com/drive/folders/1wJP4Bk81EYaQ8rZkdyz-__ybri9jMp86?usp=sharing)|[Chow](https://drive.google.com/drive/folders/1s9ZQmZcdwFEby1xeyh2sy1NmvppjCMqi?usp=sharing)|[Keeshond](https://drive.google.com/drive/folders/1SYMV4Xr85r4rGrPMzBmTwvIt6TuCSm2O?usp=sharing)|[Hyena](https://drive.google.com/drive/folders/1_9fMuZ3WazBBVVLcozdzvGQJMB_Yy-7O?usp=sharing)|[Egyptian Cat](https://drive.google.com/drive/folders/1Nh88yfOc6-N7-TtoXpIiChXuTXEPrXdj?usp=sharing)|[Lion](https://drive.google.com/drive/folders/1_mEy5QQS6S3SbHXulowrFczu4Z4u39Q-?usp=sharing)|[Bee](https://drive.google.com/drive/folders/11CESAr_oI3JEfcZAJU_NLExjIxPHBWag?usp=sharing)|[Leafhopper](https://drive.google.com/drive/folders/1SWUYnuL_IETZy_52eIqO0uVpptqWvkuh?usp=sharing)|[Sea Urchin](https://drive.google.com/drive/folders/1V76wha8PeIdDoLBwx4jM0hxz1-DuwXIs?usp=sharing)|[Zebra](https://drive.google.com/drive/folders/1_Tui8L10ljwquEfABbY_74SV_l5LMxnn?usp=sharing)|[Polecat](https://drive.google.com/drive/folders/1bIe1uSkJm1YlEgzVdHCgdAWnPVMG8u1D?usp=sharing)|[Gorilla](https://drive.google.com/drive/folders/1EAXLfOAVF4X-6zW-O7clprtQxm_TN_Cq?usp=sharing)|[Langur](https://drive.google.com/drive/folders/14Y5icSx5IF1x4gk2CRQh8i_zaQzUhqEA?usp=sharing)|[Eel](https://drive.google.com/drive/folders/1V7c6UQ1QS8N9emHdWZsr8DCvKDeMMkec?usp=sharing)|[Anemone Fish](https://drive.google.com/drive/folders/1-CYYOhuuS7HSCGpysTlNCaiAucTAcE7d?usp=sharing)|[Airliner](https://drive.google.com/drive/folders/1Z56gdh0Gp02bm7Rck_WomuBRZ6N1PQHr?usp=sharing)|[Banjo](https://drive.google.com/drive/folders/1Z56gdh0Gp02bm7Rck_WomuBRZ6N1PQHr?usp=sharing)|[Basketball](https://drive.google.com/drive/folders/1WWI9mL8ecBgQuZ4DG5rgmzn2M9I9Tb5C?usp=sharing)|[Beaker](https://drive.google.com/drive/folders/1iTsVEH9H-pnr3HvpWhokyhwItGQ57wAS?usp=sharing)|[Bell Cote](https://drive.google.com/drive/folders/10HH-YBWmnMYhLd4d5xG-CRZ2olVRgeB0?usp=sharing)|[Bookcase](https://drive.google.com/drive/folders/1o6YK_L5wv6o5dsVHxm0O9M0sZCmBn6bs?usp=sharing)|[Buckle](https://drive.google.com/drive/folders/14JBuEp6KP5k_dE2g5TNyHwGQ_vIYOov8?usp=sharing)|[CD Player](https://drive.google.com/drive/folders/1_T4WFkIcdEYLEo42fAptdasc7iGmJltl?usp=sharing)|[Chain Saw](https://drive.google.com/drive/folders/1rleHJeP5z4_Ibxi2k61Rvc5tgijkapsY?usp=sharing)|[Coil](https://drive.google.com/drive/folders/1Pm6W4vfoV0CQIjJL_Crwd7FY0HNkzQoL?usp=sharing)|[Cornet](https://drive.google.com/drive/folders/1z4zpdpi4bbyyjrEy5nARdXqSF8Twxcql?usp=sharing)|[Crutch](https://drive.google.com/drive/folders/1gZ3cznPWK6b4qbQUUNmvevTQzjDnFvFo?usp=sharing)|[Dome](https://drive.google.com/drive/folders/1ZFNoRO6Cs-mr-ImeQ0-gVbMp_kXyX6oN?usp=sharing)|[Electric Guitar](https://drive.google.com/drive/folders/1KCUYBQRyoDvu9nXDpix_v_jdbxEmqXVl?usp=sharing)|[Garbage Truck](https://drive.google.com/drive/folders/1REQIoEdw2aamusVtbD1vYQRSSE8b54-z?usp=sharing)|[Greenhouse](https://drive.google.com/drive/folders/1cqKhJZqDJeku9PqohxVt1eeHLesi8I0q?usp=sharing)|[Grocery Store](https://drive.google.com/drive/folders/1X8eArLD67YV2nIlLMakC8Oo6lFfcds8P?usp=sharing)|[Honeycomb](https://drive.google.com/drive/folders/1DsHFC7ONveANfP3BjAySOBe2LZz34qeN?usp=sharing)|[iPod](https://drive.google.com/drive/folders/1xgnH9NeUg6iE3-iGTb-8AbqkhiMl8-oY?usp=sharing)|[Jigsaw Puzzle](https://drive.google.com/drive/folders/1XHiB4WQ4EO2jL7CDSGGhd0ka3qxVNYuD?usp=sharing)|[Lipstick](https://drive.google.com/drive/folders/1jHpFqnICmeWc0p7L71z0wa6oIRPy70ew?usp=sharing)|[Maillot](https://drive.google.com/drive/folders/1uyIPKAT1dvd9-kVRc5BQ28VCyBbE4UqP?usp=sharing)|[Maze](https://drive.google.com/drive/folders/1roaEbHZgXak5e0Lc7vThlPjhySg03ObZ?usp=sharing)|[Military Uniform](https://drive.google.com/drive/folders/18c0K9kszSm-vY4lC6hJiuaJeWNQw1vhc?usp=sharing)|[Neck Brace](https://drive.google.com/drive/folders/1dGCrjeUvc9raZwu4R2tmuvXHAU4yJrkV?usp=sharing)|[Overskirt](https://drive.google.com/drive/folders/1PyCikNF9soDGDko7_NAvh8Dn4ZP0xpU-?usp=sharing)|[Pay-phone](https://drive.google.com/drive/folders/1OJ5QE9uqWlLUom2j0YKckm_YG7J2oP3q?usp=sharing)|[Pickup](https://drive.google.com/drive/folders/1Ww43snwVcVDYtgiHXx29Op1mj229k9lz?usp=sharing)|[Pirate](https://drive.google.com/drive/folders/1duCcFLFnG0xCIoHnYnDRmk2A0M7XlBCr?usp=sharing)|[Poncho](https://drive.google.com/drive/folders/1TNQZDFidGWdu6oQnmU0pUvOCGYlbddAp?usp=sharing)|[Purse](https://drive.google.com/drive/folders/11RuTwqBz5QfQFy8cv8_akapjClIJVykg?usp=sharing)|[Rain Barrel](https://drive.google.com/drive/folders/19_oovfpIQsfBKLdQbobZFXvG9TqmvYvv?usp=sharing)|[Rotisserie](https://drive.google.com/drive/folders/1vrqXhDd51P3FKYFZ2rJ5hEOBQjFX4yYg?usp=sharing)|[School Bus](https://drive.google.com/drive/folders/17yZuDDDmCUPN0OwrOYPk_afg-1r1Hb5L?usp=sharing)|[Sewing Machine](https://drive.google.com/drive/folders/1jt9TBCPu8joM4EAxz8gXiSuflWpwI64m?usp=sharing)|[Shopping Cart](https://drive.google.com/drive/folders/12ZsX-UHSiPFqkZeDhEx2hCpQ6zZ_6SgN?usp=sharing)|[Spatula](https://drive.google.com/drive/folders/1-jtUSWLlSFvRJfpv305HGEIEO2s_XfwN?usp=sharing)|[Stove](https://drive.google.com/drive/folders/1Pbzr96pkFew4EwxRBlmiFoF1OznHdGrR?usp=sharing)|[Sunglass](https://drive.google.com/drive/folders/1Sj_PR0aTjLv2JbpozhsBQRFP82CAzobH?usp=sharing)|[Teapot](https://drive.google.com/drive/folders/15ILIWbyYWVP6-ckJd8lawhgabqVxuaNG?usp=sharing)|[Toaster](https://drive.google.com/drive/folders/1KHhhL12IKojaJXgqbYcgKlKbvWkV9lAg?usp=sharing)|[Tractor](https://drive.google.com/drive/folders/1wYwVcVeTrlpz5c5If07pPrIQwAr1alkt?usp=sharing)|[Umbrella](https://drive.google.com/drive/folders/1s_nPR33fiajQw_Agn2Rx57klOhJlOhGj?usp=sharing)|[Velvet](https://drive.google.com/drive/folders/1psptODSqTp1bxpkF1gB2ZjJOAYnPkydB?usp=sharing)|[Wallet](https://drive.google.com/drive/folders/1PWOOyETSgf5atrxRhQGjL52RQOFa4mcG?usp=sharing)|[Whiskey Jug](https://drive.google.com/drive/folders/1CRf3B1Mwv5Codx_DV4iOavsBjijfbZTZ?usp=sharing)|[Ice Lolly](https://drive.google.com/drive/folders/1cIlrKFRyGnZqlSDZ7NdNb-qKa9oWYhUb?usp=sharing)|[Pretzel](https://drive.google.com/drive/folders/1exFKdRIHg1OmHPs3r8X3crFwWY3_MK06?usp=sharing)|[Cardoon](https://drive.google.com/drive/folders/1c3dnqukLMO_bHN9mdCdx0oAVh9mVEXXk?usp=sharing)|[Hay](https://drive.google.com/drive/folders/1lb2ayMfYvaE46xBlRjjdIbh_di3TVtbv?usp=sharing)|[Pizza](https://drive.google.com/drive/folders/14gxrhhO-3MOjI7NS531PzSaIM2e5zOyR?usp=sharing)|[Volcano](https://drive.google.com/drive/folders/1cWozNq2RnKXpDb3zP6KyT-nctlHjdu-I?usp=sharing)|[Rapeseed](https://drive.google.com/drive/folders/1mLPdaYNAjwxJRcBkdRbCPy48KTzxMVap?usp=sharing)|[Agaric](https://drive.google.com/drive/folders/1Ljjd-MfjTpWxRbeRxTDFyS1Zqw56-sDr?usp=sharing)|


## Training

1. _Source Domain dataset:_ You can start with paintings dataset such as described in [Cross Domain Attack](https://github.com/Muzammal-Naseer/Cross-domain-perturbations).
2. _Target Domain dataset:_ We obtain samples of a certain target domain (e.g. ImageNet class) from ImageNet training set.

Run the script with your target of choice:
```
 ./scripts/train.sh
```

## Evaluation
1. Download any or all of the pretrained generators to directory "pretrained_generators".
2. Download ImageNet models trained with [stylized ImageNet](https://github.com/rgeirhos/Stylized-ImageNet) and [augmentations](https://github.com/google-research/augmix) to directory "pretrained_models"
 
Run the following command to evaluate transferability of a target to (black-box) model on the ImageNet-Val.
```
  python eval.py  --data_dir data/IN/val --source_model res50 --source_domain IN --target 24 --eps 16 --target_model vgg19_bn 
```

### 10/100-Targets (all-source)
Perturb all samples of ImageNet validation (excluding the target class samples) to each of the 10/100 targets and observe the average target transferability to (black-box) model.

```
  python eval_all.py  --data_dir data/IN/val --source_model res50 --source_domain IN  --eps 16 --num_targets 100 --target_model vgg19_bn 
```

### 10-Targets (sub-source)
Select the samples of 10 target classes from ImageNet validation. Perturb the samples of these classes (excluding the target class samples) to each of 10 targets and observe the average target transferability to (black-box) model.

```
  python eval_sub.py  --data_dir data/IN/val --source_model res50 --source_domain IN --eps 16--target_model vgg19_bn 
```

##  Why Augmentations Boost Transferability?
<sup>([top](#contents))</sup>
_[Ilyas et al.](https://arxiv.org/abs/1905.02175)  showed that adversarial examples can be explained by features of the attacked class label. In our targeted attack case, we wish to imprint the features of the target class distribution onto the source samples within an allowed distance. However, black-box (unknown) model might apply different set of transformations (from one layer to another) to process such features and reduce the target transferability. Training on adversarial augmented samples allows the generator to capture such targeted features that are robust to transformations that may vary from one model to another._

##  Why Ensemble of Weak Models Maximizes Transferability?
<sup>([top](#contents))</sup>
_Different models of the same family of networks can exploit different information to make prediction. One such example is shown in here. Generators are trained against Dense121 and Dense169 to target Snowmobile distribution. Unrestricted generator outputs reveal that Dense121 is more focused on Snowmobile's blades while Dense169 emphasizes the background pine tree patterns to discriminate Snowmobile samples. This complementary information from different models of the same family helps the generator to capture more generic global patterns which transfer better than any of the individual models._

|Original Image|Source Model: Dense121, Target: Snowmobile|Source Model: Dense169, Target: Snowmobile|
|---|:---:|:---:|
| <img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/original_dense.png" > | <img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_dense121_802.png" >| <img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_dense169_802.png" > 

##  Generative Vs Iterative Attacks

-  Image-specific (iterative) attacks run iterative optimization for each given sample. This optimization is expensive as it has to be repeated for each sample independently. On the other hand, a generator requires training but can adapt to input sample with a farward pass only.
- Targeted global perturbations are more transferable as indicated by our results. Iteratively optimizing for a target using a single image inherently lacks the ability to model global perturbations. This is where generative methods excel as they can model such perturbations during training phase.

### Key Developments made by Iterative Attacks
* [PGD](https://arxiv.org/abs/1706.06083) attack has lower transferability due to overfitting (ICRL-2018).
* [MI](https://arxiv.org/abs/1710.06081) intorduced momentum. It accumulates gradients over iterations to reduce overfitting (CVPR-2018).
* [DIM](https://arxiv.org/abs/1803.06978) introduced input transformations like padding or rescaling to diversify patterns. Think of it as a regulation in the input space to reduce overfitting (CVPR-2019).
* [Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) introduced triplet loss to push adversarial examples towards the target label while increasing their distance from the original label (CVPR 2020).
* [FDA-fd](https://arxiv.org/abs/2004.12519) introduced a method to model class-wise distribution within feature space across differnt layers of a network. Then transfer targeted perturbations from the single optimal layer (ICLR 2020).
* [FDA-N](https://arxiv.org/abs/2004.14861) adapts the FDA-fd across multiple layers and the classifier as well (NeurIPS 2020).
* [SGM](https://arxiv.org/abs/2002.05990) found that while back-propagating, giving more weightage to gradients from skip connections increases transferability (ICLR 2020).
* [LinBP](https://arxiv.org/abs/2012.03528) found that linear back-propagation can boost transferability (NeurIPS 2020).

### Key Developments made by Generative Attacks
* [GAP](https://arxiv.org/abs/1712.02328) introduced a mechanism to train generative networks against pretrained-models via cross-entropy (CVPR 2018).
* [CDA](https://arxiv.org/abs/1905.11736) introduced a mechanism to train generative network against pretrained-model via relativistic cross-entropy (NeurIPS 2019).
* [TTP](#Citation) introudced generative training to match a source and target domain within latent space of a pretrained-model based on gloabl distribution matching objectives. It does not rely on data annotations (labels) or classification boundary information (ICCV 2021).

## Tracking SOTA Targeted Transferability
<sup>([top](#contents))</sup>
Results on 10-Targets (sub-source) settings. 
* Select 500 samples belonging to 10 targets {24,99,245,344,471,555,661,701,802,919} from ImageNet validation set.
* Remove the samples of the target class. You are left with 450 samples.
* Run target attack to map these 450 samples to selected target (perturbation budget l_inf=16).
* Repeat this process for all the 10 targets.
* Report average target accuracy.

```
Updating....Meanwhile, please have a look at our paper. 
```
#### Unknown Target Model
<sup>([top](#contents))</sup>
_Attacker  has  access  to  a  pretrained  discriminator  trained  on labeled data but has no knowledge about the architecture of the  target  model._
|Method| Attack type | Source Model| Target Model| Distance |24|99|245|344|471|555|661|701|802|919|Average|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
[PGD](https://arxiv.org/abs/1706.06083)| Iterative | ResNet50|Dense121|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|Dense121|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|Dense121|16|
[Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) |Iterative | ResNet50|Dense121|16|
[FDA-fd](https://arxiv.org/abs/2004.12519)|Iterative | ResNet50|Dense121|16|
[FDA-N](https://arxiv.org/abs/2004.14861) |Iterative | ResNet50|Dense121|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|Dense121|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|Dense121|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|Dense121|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|Dense121|16|
[TTP](#Citation)|Generative|ResNet50|Dense121|16|
[PGD](https://arxiv.org/abs/1706.06083)| Iterative | ResNet50|Dense121|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|VGG19_BN|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|VGG19_BN|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|VGG19_BN|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|VGG19_BN|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|VGG19_BN|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|VGG19_BN|16|
[TTP](#Citation)|Generative|ResNet50|VGG19_BN|16|

#### Unknown Training Mechanism
<sup>([top](#contents))</sup>
_Attacker  has  knowledge about the architecture of the  target  model but unaware of its training mechanism._
|Method| Attack type | Source Model| Target Model| Distance |24|99|245|344|471|555|661|701|802|919|Average|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
[PGD](https://arxiv.org/abs/1706.06083)| Iterative | ResNet50|SIN|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|SIN|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|SIN|16|
[Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) |Iterative | ResNet50|SIN|16|
[FDA-fd](https://arxiv.org/abs/2004.12519)|Iterative | ResNet50|SIN|16|
[FDA-N](https://arxiv.org/abs/2004.14861) |Iterative | ResNet50|SIN|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|SIN|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|SIN|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|SIN|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|SIN|16|
[TTP](#Citation)|Generative|ResNet50|SIN|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|Augmix|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|Augmix|16|
[Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) |Iterative | ResNet50|Augmix|16|
[FDA-fd](https://arxiv.org/abs/2004.12519)|Iterative | ResNet50|Augmix|16|
[FDA-N](https://arxiv.org/abs/2004.14861) | Iterative | ResNet50|Augmix|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|Augmix|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|Augmix|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|Augmix|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|Augmix|16|
[TTP](#Citation)|Generative|ResNet50|Augmix|16|
[PGD](https://arxiv.org/abs/1706.06083)| Iterative | ResNet50|ADV|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|ADV|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|ADV|16|
[Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) |Iterative | ResNet50|ADV|16|
[FDA-fd](https://arxiv.org/abs/2004.12519)|Iterative | ResNet50|ADV|16|
[FDA-N](https://arxiv.org/abs/2004.14861) |Iterative | ResNet50|ADV|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|ADV|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|ADV|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|ADV|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|ADV|16|
[TTP](#Citation)|Generative|ResNet50|ADV|16|

#### Unknown Input Processing
<sup>([top](#contents))</sup>
_Attacker  has  knowledge about the architecture of the  target  model but unaware of the input processing defense._
|Method| Attack type | Source Model| Input Processing| Distance |24|99|245|344|471|555|661|701|802|919|Average|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
[PGD](https://arxiv.org/abs/1706.06083)| Iterative|ResNet50|NRP|16|
[MI](https://arxiv.org/abs/1710.06081)| Iterative | ResNet50|NRP|16|
[DIM](https://arxiv.org/abs/1803.06978)| Iterative | ResNet50|NRP|16|
[Po-TRIP](https://openaccess.thecvf.com/content_CVPR_2020/papers/Li_Towards_Transferable_Targeted_Attack_CVPR_2020_paper.pdf) |Iterative | ResNet50|NRP|16|
[FDA-fd](https://arxiv.org/abs/2004.12519)|Iterative|ResNet50|NRP|16|
[FDA-N](https://arxiv.org/abs/2004.14861) |Iterative|ResNet50|NRP|16|
[SGM](https://arxiv.org/abs/2002.05990)| Iterative | ResNet50|NRP|16|
[SGM+LinBP](https://arxiv.org/abs/2012.03528)| Iterative | ResNet50|NRP|16|
[GAP](https://arxiv.org/abs/1712.02328)|Generative|ResNet50|NRP|16|
[CDA](https://arxiv.org/abs/1905.11736)|Generative|ResNet50|NRP|16|
[TTP](#Citation)|Generative|ResNet50|NRP|16|


##  What Can You Do? 

```
We will highlight future research directions here.
```

##  References
<sup>([top](#contents))</sup>
Code depends on [BasicSR](https://github.com/xinntao/BasicSR). We thank them for their wonderful code base. 

##  Visual Examples
<sup>([top](#contents))</sup>
Here are some of the unrestricted targeted patterns found by our method (TTP). This is just for visualization purposes. It is important to note that during inference, these adversaries are projected within a valid distance (e.g l_inf<=16).


|Source Model: ResNet50, &nbsp; &nbsp; &nbsp; &nbsp; Target: Jellyfish|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_1st_pages_107.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Lipstick|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_1st_pages_629.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Stove|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_2st_pages_827.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Rapeseed|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_2st_pages_984.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Anemone Fish|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_3st_pages_393.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Banjo|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_3st_pages_420.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Sea Urchin|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_4st_pages_328.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Parachute|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_4st_pages_701.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Buckle|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_5st_pages_464.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: iPOD|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_5st_pages_605.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Bookcase|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_6st_pages_453.png" >|

|Source Model: ResNet50,  &nbsp; &nbsp; &nbsp; &nbsp; Target: Sewing Machine|
|---|
|<img src="https://github.com/Muzammal-Naseer/TTP/blob/main/assets/unrestricted_adv_6st_pages_786.png" >|
