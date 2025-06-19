# 📊 Newcastle-Ottawa Scale Assessment Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Build Status](https://github.com/username/nos-assessment-tool/workflows/CI/badge.svg)](https://github.com/username/nos-assessment-tool/actions)

A comprehensive web-based tool for conducting Newcastle-Ottawa Scale (NOS) risk of bias assessments in systematic reviews and meta-analyses. Generate publication-ready robvis-style visualizations for observational studies.

## 🚀 Features

- **Complete NOS Implementation**: Cohort, Case-Control, and Cross-Sectional studies
- **Interactive Assessment Forms**: Step-by-step guided evaluation with star ratings
- **Publication-Ready Visualizations**: robvis-style plots and domain heatmaps
- **Quality Classification**: Automated Good/Fair/Poor quality rating system
- **Data Export**: CSV, JSON, and high-resolution PNG formats
- **Multi-Study Management**: Assess and compare multiple studies simultaneously
- **Academic Integration**: Built specifically for systematic review workflows
- **Research-Grade Output**: Publication-quality plots for journals and conferences

## 🎯 Study Types Supported

### Cohort Studies (9-star scale)
- **Selection** (4 stars): Representativeness, non-exposed selection, exposure ascertainment, outcome demonstration
- **Comparability** (2 stars): Confounding factor control
- **Outcome** (3 stars): Assessment method, follow-up length, adequacy of follow-up

### Case-Control Studies (9-star scale)
- **Selection** (4 stars): Case definition, representativeness, control selection, control definition
- **Comparability** (2 stars): Confounding factor control
- **Exposure** (3 stars): Ascertainment method, same method for cases/controls, non-response rate

### Cross-Sectional Studies (8-star scale)
- **Selection** (4 stars): Representativeness, sample size justification, non-respondents, exposure ascertainment
- **Comparability** (2 stars): Confounding factor control
- **Outcome** (2 stars): Assessment method, statistical test appropriateness

## 🛠️ Installation

### Quick Start with Docker
```bash
git clone https://github.com/username/nos-assessment-tool.git
cd nos-assessment-tool
docker-compose up
```
Navigate to `http://localhost:8501` in your browser.

### Local Installation
```bash
# Clone repository
git clone https://github.com/username/nos-assessment-tool.git
cd nos-assessment-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Cloud Deployment
Deploy instantly on Streamlit Cloud, Heroku, or AWS. See [deployment guide](docs/installation.md) for details.

## 📖 Quick Start Guide

### 1. Basic Assessment Workflow
1. **Add New Study**: Enter study details and select study type
2. **Complete Assessment**: Answer NOS criteria questions with star ratings
3. **Save Assessment**: Store evaluation with quality classification
4. **Generate Report**: Create publication-ready visualizations

### 2. Batch Processing
```python
# Import multiple studies from CSV
python scripts/batch_assessment.py --input studies.csv --output results.json
```

### 3. Export Options
- **Data Export**: CSV and JSON formats for statistical analysis
- **Visual Export**: High-resolution PNG plots (300 DPI) for publications
- **Report Generation**: Comprehensive HTML reports with all assessments

## 📊 Visualization Examples

The tool generates publication-quality plots similar to robvis:

- **Summary Assessment Plot**: Horizontal bar chart showing overall study quality
- **Detailed Domain Heatmap**: Color-coded matrix of domain-specific assessments
- **Quality Distribution**: Pie charts and bar plots for quality overview
- **Study Type Analysis**: Distribution and comparison across study designs

## 🔬 Academic Applications

### Systematic Review Integration
- **Reference Manager Compatibility**: Import from Zotero, EndNote, Mendeley
- **Quality Assessment Workflow**: Standardized NOS evaluation process
- **Risk of Bias Visualization**: Professional plots for manuscript submission
- **Meta-Analysis Preparation**: Export quality scores for statistical analysis

### Research Output
- **Manuscript Figures**: Publication-ready plots for peer-reviewed journals
- **Conference Presentations**: High-quality visualizations for academic conferences
- **Grant Applications**: Professional quality assessment documentation
- **Teaching Materials**: Educational tool for evidence-based medicine training

## 👨‍🎓 Developer

**Muhammad Nabeel Saddique**
- 4th Year MBBS Student, King Edward Medical University, Lahore, Pakistan
- Founder: Nibras Research Academy
- Research Focus: Systematic Review, Meta-Analysis, Evidence-Based Medicine
- Email: nabeel.saddique@kemu.edu.pk

### Research Tools Expertise
Rayyan, Zotero, EndNote, WebPlotDigitizer, Meta-Converter, RevMan, MetaXL, Jamovi, Comprehensive Meta-Analysis (CMA), OpenMeta, R Studio

## 🏥 Nibras Research Academy

This tool is part of the educational resources developed by Nibras Research Academy, where young researchers are mentored in:
- Systematic review methodology
- Meta-analysis techniques
- Research publication strategies
- Evidence synthesis methods

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [User Manual](docs/user_guide.md)
- [NOS Methodology](docs/nos_methodology.md)
- [API Reference](docs/api_reference.md)
- [Examples & Tutorials](docs/examples/)

## 🤝 Contributing

We welcome contributions from the research community! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Research Contributions
- New study type implementations
- Additional visualization options
- Integration with reference managers
- Statistical analysis features
- Validation studies

## 📊 Quality Standards

- **Code Quality**: PEP 8 compliance, comprehensive testing
- **Documentation**: Extensive user guides and API documentation
- **Validation**: Based on original NOS methodology by Wells et al.
- **Reproducibility**: All assessments are fully reproducible and exportable

## 📄 Citation

If you use this tool in your research, please cite:

```bibtex
@software{saddique2024nos,
  author = {Saddique, Muhammad Nabeel},
  title = {Newcastle-Ottawa Scale Assessment Tool},
  year = {2024},
  url = {https://github.com/username/nos-assessment-tool},
  version = {1.0.0}
}
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **King Edward Medical University** for academic support
- **Nibras Research Academy** for research infrastructure
- **Newcastle-Ottawa Scale developers** for the original methodology
- **Open-source community** for tools and libraries
- **robvis package developers** for visualization inspiration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/username/nos-assessment-tool/issues)
- **Email**: support@nibrasresearch.com
- **Documentation**: [User Guide](docs/user_guide.md)
- **Community**: [GitHub Discussions](https://github.com/username/nos-assessment-tool/discussions)

## 🔗 Related Tools

- [RevMan](https://training.cochrane.org/online-learning/core-software-cochrane-reviews/revman) - Cochrane systematic reviews
- [robvis](https://github.com/mcguinlu/robvis) - Risk of bias visualization
- [Rayyan](https://www.rayyan.ai/) - Systematic review screening
- [Meta-Converter](https://www.meta-converter.com/) - Effect size calculation

---

**Disclaimer**: This software is for research and educational purposes. Users should verify all assessments and follow established systematic review guidelines. Not intended as a substitute for expert methodological judgment.