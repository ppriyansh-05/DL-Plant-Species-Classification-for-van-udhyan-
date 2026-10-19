"""
Generate Microsoft Word (.docx) CA3 Academic Report
Includes:
- Professional academic typography, tables, and borders
- Embedded figures (pipeline architecture, experimental comparison, species distribution)
- Fully formatted sections per the rubric
"""
import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_report_docx():
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Deep Learning-Based Plant Species Classification for Urban Plantation Monitoring at Van Udyan, Pune")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.name = 'Calibri'
    r_title.font.color.rgb = RGBColor(0x1a, 0x36, 0x5d)

    # Subtitle / Metadata
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("Continuous Assessment Report (CA3) • Deep Learning (Semester 5)\nField Collaboration: Reform Social Welfare Foundation (RSWF), Pune\nStudent Project Team • October 2026")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    r_div = p_div.add_run("_________________________________________________________________________________")
    r_div.font.color.rgb = RGBColor(0xcc, 0xcc, 0xcc)

    # Abstract Box
    p_abs_h = doc.add_heading("Abstract", level=2)
    p_abs_h.paragraph_format.space_before = Pt(8)
    p_abs_h.paragraph_format.space_after = Pt(4)
    
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.space_after = Pt(8)
    r_abs = p_abs.add_run(
        "Automated taxonomic identification using deep convolutional neural networks provides scalable, objective surveillance for urban reforestation projects. This investigation addresses computer-vision-based plant species identification across three plantation zones at the Van Udyan urban forest reserve in Pune, Maharashtra, in partnership with the Reform Social Welfare Foundation (RSWF).\n\n"
        "Two sequential empirical experiments were developed and evaluated: (1) An initial 38-species baseline model using MobileNetV2 achieved 10.53% held-out test accuracy and 9.29% accuracy on an independent benchmark of 140 authentic field photographs, hindered by extreme class imbalance and botanical data scarcity. (2) A refined Top-15 model focusing on the best-supported Van Udyan species with in-situ training adaptation. Comparing architectures strictly on validation performance, EfficientNetB0 achieved 26.28% validation accuracy (outperforming MobileNetV2 at 21.90%). On the held-out test split, EfficientNetB0 achieved 23.78% top-1 accuracy. On an untouched 30-image field benchmark (2 photos per species), the model yielded 13.33% top-1 and 33.33% top-3 accuracy.\n\n"
        "While observed test accuracy improved from 10.53% to 23.78%, the target 50% accuracy was not achieved, and field performance remains preliminary. These findings indicate that while domain-adapted transfer learning and focused taxonomic scoping substantially improve representation, fine-grained vegetative similarity and limited in-situ sample sizes remain primary bottlenecks for automated field monitoring."
    )
    r_abs.font.size = Pt(10)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_after = Pt(14)
    r_kw = p_kw.add_run("Keywords: Deep Learning, Plant Species Classification, Urban Forestry, Transfer Learning, MobileNetV2, EfficientNetB0, Data Leakage Prevention, Van Udyan Pune.")
    r_kw.font.bold = True
    r_kw.font.size = Pt(9.5)
    r_kw.font.color.rgb = RGBColor(0x2b, 0x5c, 0x8f)

    # 1. Introduction
    doc.add_heading("1. Introduction", level=1)
    doc.add_paragraph(
        "Urban ecological restoration initiatives, such as the Van Udyan project managed by the Reform Social Welfare Foundation (RSWF) in Pune, Maharashtra, are critical for reviving degraded urban landscapes, sequestering carbon, reducing urban heat islands, and creating multi-layered habitat corridors for native fauna.\n\n"
        "Monitoring the survival, phenological maturation, and species-level distribution of planted saplings across diverse zones (Zone 1, Zone 2, and Zone 3) requires frequent botanical inventories. However, manual audits present substantial operational limitations including taxonomic expertise bottlenecks, field volunteer fatigue, and severe budget constraints.\n\n"
        "Automated image classification using deep learning offers an objective, high-throughput solution. However, applying computer vision to real-world ecological restoration presents severe domain challenges including severe class imbalance, observation-level data leakage across multi-angle burst photos, and domain shifts between pristine web observations and rugged field surveillance photos."
    )

    # 2. Literature Review
    doc.add_heading("2. Literature Review", level=1)
    doc.add_paragraph(
        "Automated botanical identification has progressed from handcrafted morphological feature extraction to deep convolutional representation learning (LeCun et al., 2015). Early identification frameworks extracted geometric descriptors from leaf contours and venation skeletons, classifying them via Support Vector Machines or Random Forests (Cope et al., 2012). While effective on flat, clean, laboratory-scanned leaves, these handcrafted techniques fail in real-world forestry scenarios involving partial occlusion, herbivore damage, non-uniform backgrounds, and variable outdoor illumination.\n\n"
        "The application of deep transfer learning from natural image corpora (ImageNet) established a new paradigm in ecological computer vision (Wäldchen & Mäder, 2018). Large convolutional models such as ResNet-50 (He et al., 2016) demonstrated strong feature extraction capabilities but introduce substantial parameter overhead (>25M parameters). To address computational constraints on mobile edge devices, Sandler et al. (2018) developed MobileNetV2, introducing inverted residual bottlenecks with linear bottleneck units and depthwise separable convolutions (~3.4M parameters). Concurrently, Tan & Le (2019) introduced EfficientNet, demonstrating that compound scaling across depth, width, and resolution yields superior representation with compact parameter footprints (~5.3M parameters for EfficientNetB0).\n\n"
        "A critical deficiency highlighted in ecological computer vision literature is observation-level data leakage (Kelling et al., 2019). Distributing multi-angle photographs of the same specimen across both training and test partitions causes severe metric inflation. This investigation enforces strict observation-level grouping and hash disjointness to prevent evaluation contamination."
    )

    # 3. Methodology
    doc.add_heading("3. Methodology", level=1)
    doc.add_paragraph(
        "The methodology combines field data extraction, ethically licensed community data collection, leakage-free partitioning, and transfer learning architectures tailored for edge deployment."
    )

    doc.add_heading("3.1 Target Taxa & Scope Refinement", level=2)
    doc.add_paragraph(
        "The initial field survey inventory documented 38 tree and shrub taxa across Zones 1, 2, and 3 of Van Udyan. Following the baseline experiment, the taxonomic scope was refined to the 15 best-supported species possessing reliable NGO ground-truth records, confirmed botanical nomenclature, and sufficient training imagery: Alstonia scholaris, Azadirachta indica, Bauhinia variegata, Bombax ceiba, Cordia dichotoma, Dalbergia latifolia, Erythrina variegata, Ficus benghalensis, Ficus religiosa, Mangifera indica, Pongamia pinnata, Syzygium cumini, Tectona grandis, Terminalia bellirica, and Terminalia catappa."
    )

    doc.add_heading("3.2 Dataset Assembly & Curation", level=2)
    doc.add_paragraph(
        "1. Van Udyan Ground Truth: In-situ field photographs were extracted from the OpenPyXL drawing layer of Zone Wise Plants.xlsx. An automated audit quarantined Row 74 (labeled as '?' in Zone 2) to maintain strict label hygiene.\n"
        "2. Supplementary iNaturalist Observations: A custom rate-limited harvesting engine collected research-grade observations with tiered geographic priority (Pune -> Maharashtra -> India -> Global). To ensure legal compliance, only Creative Commons-licensed images (CC0, CC-BY, CC-BY-NC, CC-BY-SA, CC-BY-NC-SA) were downloaded. Non-commercial derivative restrictions (-ND) and non-attributed images were rejected."
    )

    doc.add_heading("3.3 Leakage Prevention & Partitioning Protocol", level=2)
    doc.add_paragraph(
        "To guarantee zero evaluation leakage, images were partitioned strictly by unique observation ID. For the Top-15 experiment, 69 authentic Van Udyan field photos were integrated into the training (54) and validation (15) splits so the network could learn real-world field conditions. Crucially, exactly 30 authentic field photos (2 per species) were permanently isolated in test_van_udyan_benchmark/ and never exposed during model development."
    )

    # Add Pipeline Diagram Figure
    pipe_fig = Path("docs/figures/pipeline_architecture_diagram.png")
    if pipe_fig.exists():
        doc.add_paragraph().paragraph_format.space_before = Pt(8)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(pipe_fig), width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run("Figure 1: End-to-End Pipeline & Architecture: Van Udyan Plant AI (EfficientNetB0).")
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True

    # Partition Summary Table
    p_t_head = doc.add_paragraph()
    r_th = p_t_head.add_run("Table 1: Top-15 Dataset Partitioning and Domain Composition")
    r_th.bold = True
    r_th.font.size = Pt(10)

    table1 = doc.add_table(rows=6, cols=5)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    headers = ["Partition", "Total Images", "iNaturalist", "Van Udyan Field", "Evaluation Purpose"]
    for i, h in enumerate(headers):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "2B5C8F")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    row_data = [
        ["Train", "698", "644", "54", "Feature learning with field adaptation"],
        ["Validation", "137", "122", "15", "Model selection & early stopping"],
        ["Held-Out Test", "143", "143", "0", "Unbiased out-of-sample evaluation"],
        ["Field Benchmark", "30", "0", "30", "Untouched localized field assessment (2/sp)"],
        ["Grand Total", "1,008", "909", "99", "100% SHA-256 Hash Disjoint"]
    ]

    for row_idx, r_vals in enumerate(row_data, start=1):
        for col_idx, val in enumerate(r_vals):
            cell = table1.cell(row_idx, col_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if row_idx == 5:
                cell.paragraphs[0].runs[0].font.bold = True
            bg = "F2F5F8" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 4. Results & Discussion
    doc.add_heading("4. Results and Discussion", level=1)
    doc.add_paragraph(
        "Both experiments were executed on Google Colab using an NVIDIA Tesla T4 GPU. Table 2 summarizes the verified empirical results across both training runs."
    )

    # Comparative Table
    p_t2_head = doc.add_paragraph()
    r_t2h = p_t2_head.add_run("Table 2: Comparative Empirical Results (38-Class Baseline vs. Top-15 Model)")
    r_t2h.bold = True
    r_t2h.font.size = Pt(10)

    table2 = doc.add_table(rows=12, cols=3)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = False

    t2_headers = ["Metric / Parameter", "Experiment 1: 38-Class Baseline", "Experiment 2: Top-15 Focused Model"]
    for i, h in enumerate(t2_headers):
        cell = table2.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "1F77B4")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    comp_rows = [
        ["Taxonomic Scope", "38 species", "15 species"],
        ["Model Backbone", "MobileNetV2", "EfficientNetB0 (Selected)"],
        ["Training Split Images", "1,050", "698 (644 iNat + 54 Field)"],
        ["Validation Split Images", "236", "137 (122 iNat + 15 Field)"],
        ["Validation Accuracy (MobileNetV2)", "Not recorded", "21.90%"],
        ["Validation Accuracy (EfficientNetB0)", "Not evaluated", "26.28% (Selected)"],
        ["Held-Out Test Top-1 Accuracy", "10.53% (24 / 228)", "23.78% (34 / 143)"],
        ["Held-Out Test Top-3 Accuracy", "21.93% (50 / 228)", "Not recorded (Null in JSON)"],
        ["Field Benchmark Top-1 Accuracy", "9.29% (13 / 140)", "13.33% (4 / 30)"],
        ["Field Benchmark Top-3 Accuracy", "20.00% (28 / 140)", "33.33% (10 / 30)"],
        ["Status Relative to 50% Target", "Not Achieved", "Not Achieved (Preliminary)"]
    ]

    for row_idx, r_vals in enumerate(comp_rows, start=1):
        for col_idx, val in enumerate(r_vals):
            cell = table2.cell(row_idx, col_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if col_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Add Accuracy Comparison Chart
    comp_fig = Path("docs/figures/experimental_accuracy_comparison.png")
    if comp_fig.exists():
        p_cimg = doc.add_paragraph()
        p_cimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cimg.add_run().add_picture(str(comp_fig), width=Inches(5.5))
        p_ccap = doc.add_paragraph()
        p_ccap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ccap.paragraph_format.space_after = Pt(12)
        r_ccap = p_ccap.add_run("Figure 2: Empirical Accuracy Comparison Across Evaluation Partitions.")
        r_ccap.font.size = Pt(9.5)
        r_ccap.font.italic = True

    doc.add_heading("4.1 Scientific Evaluation of Scope Refinement", level=2)
    doc.add_paragraph(
        "Narrowing the taxonomic scope from 38 to 15 classes increased held-out test top-1 accuracy from 10.53% to 23.78% (a relative improvement of 125.8%). Similarly, field benchmark top-1 accuracy improved from 9.29% to 13.33%, with top-3 benchmark accuracy reaching 33.33%.\n\n"
        "However, this comparison must be interpreted with scientific rigor:\n"
        "1. Random Guessing Baselines: A 15-class random guessing baseline has an expected accuracy of 6.67%, whereas a 38-class baseline has an expected accuracy of 2.63%. The Top-15 model exceeds random guessing by a factor of 3.56, compared to 4.00 for the 38-class model.\n"
        "2. Sample Size Disparity: The 38-class field benchmark contained 140 images, whereas the Top-15 benchmark evaluated 30 images (2 per species). Consequently, the Top-15 benchmark exhibits higher statistical variance.\n"
        "3. Target Accuracy Assessment: The project set a target of 50% top-1 accuracy. With an observed test accuracy of 23.78%, the target accuracy was not achieved. The system cannot be considered ready for autonomous field deployment without human supervision."
    )

    doc.add_heading("4.2 Error Analysis and Ecological Limitations", level=2)
    doc.add_paragraph(
        "1. Fine-Grained Morphological Convergence: Closely related species exhibit high visual similarity. For example, Terminalia bellirica and Terminalia catappa share obovate leaf arrangements, while juvenile Ficus religiosa and Ficus benghalensis present similar bark textures and leaf venation.\n"
        "2. Phenological Asynchrony: Deciduous species such as Bombax ceiba and Erythrina variegata shed their leaves entirely during the dry season and produce dense scarlet blossoms. When a model trained primarily on foliage images is presented with a leafless flowering branch, feature extraction fails.\n"
        "3. In-Situ Photography Artifacts: Field photographs captured by NGO volunteers exhibit motion blur, harsh overhead solar glare, partial shadow occlusions, and background competition from weeds and grass.\n"
        "4. Dataset Scale Constraints: While 698 training images represents a usable initial corpus, deep neural networks typically require hundreds of varied photographs per class to achieve robust invariance to perspective, lighting, and season."
    )

    # Add Species Distribution Chart
    dist_fig = Path("docs/figures/top15_species_distribution.png")
    if dist_fig.exists():
        p_dimg = doc.add_paragraph()
        p_dimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dimg.add_run().add_picture(str(dist_fig), width=Inches(5.5))
        p_dcap = doc.add_paragraph()
        p_dcap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dcap.paragraph_format.space_after = Pt(12)
        r_dcap = p_dcap.add_run("Figure 3: Top-15 Dataset Distribution Across Partition Splits.")
        r_dcap.font.size = Pt(9.5)
        r_dcap.font.italic = True

    # 5. Web Deployment & System Integration
    doc.add_heading("5. Web Deployment & System Integration", level=1)
    doc.add_paragraph(
        "To provide a functional tool for RSWF field volunteers, an interactive web application titled Van Udyan Plant AI was developed using Python and Streamlit. The application loads the trained EfficientNetB0 model, applies exact preprocessing, and outputs the top-3 predicted species with confidence scores. Crucially, a low-confidence threshold (<40%) warns field staff when specimens cannot be recognized with high certainty, avoiding misleading diagnoses.\n\n"
        "The system is configured for cloud deployment on Render connected to Supabase Storage, maintaining complete isolation of private model binaries and credentials."
    )

    # 6. Academic Integrity & AI Usage Disclosure
    doc.add_heading("6. Academic Integrity & AI Usage Disclosure", level=1)
    doc.add_paragraph(
        "In compliance with institutional academic integrity guidelines:\n"
        "- AI Tool Assistance: Generative AI tools were utilized during this project for exploratory script scaffolding, CSS styling assistance for the web user interface, and formatting validation.\n"
        "- Authenticity of Results: All experimental accuracy scores, image counts, and performance metrics presented in this report represent genuine, unmanipulated outputs from executions on Google Colab GPU runtimes. No performance scores, confusion matrices, or evaluation statistics have been fabricated or artificially inflated.\n"
        "- Attribution of External Assets: All community-contributed photographs obtained from iNaturalist are acknowledged under their respective Creative Commons licences, with creator usernames and URLs documented in repository manifests. Field survey imagery remains the intellectual property of Reform Social Welfare Foundation (RSWF), Pune."
    )

    # 7. Conclusion & Future Work
    doc.add_heading("7. Conclusion", level=1)
    doc.add_paragraph(
        "This investigation demonstrated the application of transfer learning to urban plantation monitoring at Van Udyan, Pune. While establishing an observation-grouped, leakage-free dataset and refining the classification scope to 15 key species yielded a held-out test accuracy of 23.78% (with top-3 field benchmark accuracy of 33.33%), significant challenges remain before achieving autonomous reliability. Future work should focus on multi-part botanical imaging (bark, canopy, and leaf), temporal-phenological metadata conditioning, and active learning with volunteer feedback."
    )

    # 8. References
    doc.add_heading("8. References", level=1)
    refs = [
        "Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 4510–4520. https://doi.org/10.1109/CVPR.2018.00474",
        "Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97:6105–6114. https://doi.org/10.48550/arXiv.1905.11946",
        "He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 770–778. https://doi.org/10.1109/CVPR.2016.90",
        "Wäldchen, J., & Mäder, P. (2018). Machine learning for image based species identification. Methods in Ecology and Evolution, 9(11), 2216–2225. https://doi.org/10.1111/2041-210X.13075",
        "Cope, J. S., Corney, D., Clark, J. Y., Remagnino, P., & Wilkin, P. (2012). Plant species identification using digital morphometrics: A review. Expert Systems with Applications, 39(8), 7562–7573. https://doi.org/10.1016/j.eswa.2012.01.073",
        "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436–444. https://doi.org/10.1038/nature14539",
        "Kelling, S., Lagoze, C., Wong, W. K., Fink, D., Damoulas, T., & Sullivan, B. L. (2019). Mitigating data leakage in biodiversity machine learning workflows. Ecological Informatics, 53, 100980.",
        "iNaturalist. (2026). iNaturalist Open Data API v1 Documentation. California Academy of Sciences & National Geographic Society. https://api.inaturalist.org/v1/"
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        r_r = p_ref.add_run(r)
        r_r.font.size = Pt(9.5)

    out_path = Path("docs/Deep_Learning_CA3_Academic_Report_Van_Udyan.docx")
    doc.save(str(out_path))
    print(f"Generated Word report: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    create_report_docx()
