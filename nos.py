import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, Circle
import io
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Set page configuration
st.set_page_config(
    page_title="Newcastle-Ottawa Scale Assessment Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .developer-info {
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .assessment-container {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .study-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #dee2e6;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .domain-header {
        background: linear-gradient(135deg, #6c757d, #495057);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    
    .high-risk {
        background-color: #dc3545;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
    }
    
    .good-quality {
        background-color: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
    }
    
    .fair-quality {
        background-color: #ffc107;
        color: black;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
    }
    
    .poor-quality {
        background-color: #dc3545;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
    }
    
    .summary-container {
        background: linear-gradient(135deg, #e8f5e8, #d1ecf1);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
    
    .star-display {
        font-size: 1.2rem;
        color: #ffd700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'studies' not in st.session_state:
    st.session_state.studies = []
if 'current_study' not in st.session_state:
    st.session_state.current_study = {}

# Newcastle-Ottawa Scale criteria
NOS_CRITERIA = {
    "Cohort Studies": {
        "Selection": {
            "representativeness": {
                "question": "1. Representativeness of the exposed cohort",
                "options": {
                    "truly_representative": "Truly representative of the average population in the community (★)",
                    "somewhat_representative": "Somewhat representative of the average population in the community (★)",
                    "selected_group": "Selected group of users (e.g., nurses, volunteers)",
                    "no_description": "No description of the derivation of the cohort"
                },
                "stars": {"truly_representative": 1, "somewhat_representative": 1, "selected_group": 0, "no_description": 0}
            },
            "selection_nonexposed": {
                "question": "2. Selection of the non-exposed cohort",
                "options": {
                    "same_community": "Drawn from the same community as the exposed cohort (★)",
                    "different_source": "Drawn from a different source",
                    "no_description": "No description of the derivation of the non-exposed cohort"
                },
                "stars": {"same_community": 1, "different_source": 0, "no_description": 0}
            },
            "ascertainment_exposure": {
                "question": "3. Ascertainment of exposure",
                "options": {
                    "secure_record": "Secure record (e.g., surgical records) (★)",
                    "structured_interview": "Structured interview where blind to case/control status (★)",
                    "written_self_report": "Written self-report",
                    "no_description": "No description"
                },
                "stars": {"secure_record": 1, "structured_interview": 1, "written_self_report": 0, "no_description": 0}
            },
            "outcome_not_present": {
                "question": "4. Demonstration that outcome of interest was not present at start of study",
                "options": {
                    "yes": "Yes (★)",
                    "no": "No"
                },
                "stars": {"yes": 1, "no": 0}
            }
        },
        "Comparability": {
            "comparability": {
                "question": "5. Comparability of cohorts on the basis of the design or analysis",
                "options": {
                    "most_important": "Study controls for the most important factor (★)",
                    "additional_factor": "Study controls for any additional factor (★)",
                    "no_control": "No control for confounding factors"
                },
                "stars": {"most_important": 1, "additional_factor": 1, "no_control": 0},
                "max_stars": 2
            }
        },
        "Outcome": {
            "assessment_outcome": {
                "question": "6. Assessment of outcome",
                "options": {
                    "independent_blind": "Independent blind assessment (★)",
                    "record_linkage": "Record linkage (★)",
                    "self_report": "Self-report",
                    "no_description": "No description"
                },
                "stars": {"independent_blind": 1, "record_linkage": 1, "self_report": 0, "no_description": 0}
            },
            "adequate_followup_length": {
                "question": "7. Was follow-up long enough for outcomes to occur",
                "options": {
                    "yes": "Yes (★)",
                    "no": "No"
                },
                "stars": {"yes": 1, "no": 0}
            },
            "adequacy_followup": {
                "question": "8. Adequacy of follow up of cohorts",
                "options": {
                    "complete_followup": "Complete follow up - all subjects accounted for (★)",
                    "small_loss": "Subjects lost to follow up unlikely to introduce bias - small number lost (★)",
                    "high_loss": "High rate of follow up but no description of those lost",
                    "no_statement": "No statement"
                },
                "stars": {"complete_followup": 1, "small_loss": 1, "high_loss": 0, "no_statement": 0}
            }
        }
    },
    "Case-Control Studies": {
        "Selection": {
            "case_definition": {
                "question": "1. Is the case definition adequate?",
                "options": {
                    "independent_validation": "Yes, with independent validation (★)",
                    "record_linkage": "Yes, e.g., record linkage or based on self-reports",
                    "no_description": "No description"
                },
                "stars": {"independent_validation": 1, "record_linkage": 0, "no_description": 0}
            },
            "representativeness_cases": {
                "question": "2. Representativeness of the cases",
                "options": {
                    "consecutive_series": "Consecutive or obviously representative series of cases (★)",
                    "potential_selection": "Potential for selection biases or not stated"
                },
                "stars": {"consecutive_series": 1, "potential_selection": 0}
            },
            "selection_controls": {
                "question": "3. Selection of Controls",
                "options": {
                    "community_controls": "Community controls (★)",
                    "hospital_controls": "Hospital controls",
                    "no_description": "No description"
                },
                "stars": {"community_controls": 1, "hospital_controls": 0, "no_description": 0}
            },
            "definition_controls": {
                "question": "4. Definition of Controls",
                "options": {
                    "no_history": "No history of disease (endpoint) (★)",
                    "no_description": "No description of source"
                },
                "stars": {"no_history": 1, "no_description": 0}
            }
        },
        "Comparability": {
            "comparability": {
                "question": "5. Comparability of cases and controls on the basis of the design or analysis",
                "options": {
                    "most_important": "Study controls for the most important factor (★)",
                    "additional_factor": "Study controls for any additional factor (★)",
                    "no_control": "No control for confounding factors"
                },
                "stars": {"most_important": 1, "additional_factor": 1, "no_control": 0},
                "max_stars": 2
            }
        },
        "Exposure": {
            "ascertainment_exposure": {
                "question": "6. Ascertainment of exposure",
                "options": {
                    "secure_record": "Secure record (e.g., surgical records) (★)",
                    "structured_interview": "Structured interview where blind to case/control status (★)",
                    "interview_not_blinded": "Interview not blinded to case/control status",
                    "written_self_report": "Written self-report or medical record only",
                    "no_description": "No description"
                },
                "stars": {"secure_record": 1, "structured_interview": 1, "interview_not_blinded": 0, "written_self_report": 0, "no_description": 0}
            },
            "same_method": {
                "question": "7. Same method of ascertainment for cases and controls",
                "options": {
                    "yes": "Yes (★)",
                    "no": "No"
                },
                "stars": {"yes": 1, "no": 0}
            },
            "non_response_rate": {
                "question": "8. Non-Response rate",
                "options": {
                    "same_rate": "Same rate for both groups (★)",
                    "non_respondents": "Non-respondents described",
                    "rate_different": "Rate different and no designation"
                },
                "stars": {"same_rate": 1, "non_respondents": 0, "rate_different": 0}
            }
        }
    },
    "Cross-Sectional Studies": {
        "Selection": {
            "representativeness": {
                "question": "1. Representativeness of the sample",
                "options": {
                    "truly_representative": "Truly representative of the average population (★)",
                    "somewhat_representative": "Somewhat representative of the average population (★)",
                    "selected_group": "Selected group of users",
                    "no_description": "No description of the sampling strategy"
                },
                "stars": {"truly_representative": 1, "somewhat_representative": 1, "selected_group": 0, "no_description": 0}
            },
            "sample_size": {
                "question": "2. Sample size",
                "options": {
                    "justified": "Justified and satisfactory (★)",
                    "not_justified": "Not justified"
                },
                "stars": {"justified": 1, "not_justified": 0}
            },
            "non_respondents": {
                "question": "3. Non-respondents",
                "options": {
                    "comparability": "Comparability between respondents and non-respondents characteristics is established (★)",
                    "response_rate": "Response rate satisfactory or non-respondents described",
                    "no_description": "No description of non-respondents"
                },
                "stars": {"comparability": 1, "response_rate": 0, "no_description": 0}
            },
            "exposure_outcome": {
                "question": "4. Ascertainment of the exposure (or risk factor)",
                "options": {
                    "validated_tool": "Validated measurement tool (★)",
                    "non_validated": "Non-validated measurement tool or unclear"
                },
                "stars": {"validated_tool": 1, "non_validated": 0}
            }
        },
        "Comparability": {
            "comparability": {
                "question": "5. The subjects in different outcome groups are comparable",
                "options": {
                    "most_important": "Study controls for the most important confounding factor (★)",
                    "additional_factor": "Study controls for additional confounding factors (★)",
                    "no_control": "No control for confounding factors"
                },
                "stars": {"most_important": 1, "additional_factor": 1, "no_control": 0},
                "max_stars": 2
            }
        },
        "Outcome": {
            "assessment_outcome": {
                "question": "6. Assessment of the outcome",
                "options": {
                    "independent_blind": "Independent blind assessment (★)",
                    "record_linkage": "Record linkage (★)",
                    "self_report": "Self-report",
                    "no_description": "No description"
                },
                "stars": {"independent_blind": 1, "record_linkage": 1, "self_report": 0, "no_description": 0}
            },
            "statistical_test": {
                "question": "7. Statistical test",
                "options": {
                    "appropriate": "The statistical test used to analyze the data is clearly described and appropriate (★)",
                    "inappropriate": "The statistical test is not appropriate, not described or incomplete"
                },
                "stars": {"appropriate": 1, "inappropriate": 0}
            }
        }
    }
}

def calculate_total_stars(assessment, study_type):
    """Calculate total stars for an assessment"""
    total_stars = 0
    criteria = NOS_CRITERIA[study_type]
    
    for domain_name, domain in criteria.items():
        for criterion_name, criterion in domain.items():
            if criterion_name in assessment:
                selected_option = assessment[criterion_name]
                if selected_option in criterion["stars"]:
                    stars = criterion["stars"][selected_option]
                    # Handle special case for comparability (can have 2 stars)
                    if criterion_name == "comparability" and "max_stars" in criterion:
                        if selected_option == "most_important":
                            total_stars += 1
                        elif selected_option == "additional_factor":
                            total_stars += 2
                    else:
                        total_stars += stars
    
    return total_stars

def get_quality_rating(total_stars, study_type):
    """Determine quality rating based on total stars"""
    if study_type in ["Cohort Studies", "Case-Control Studies"]:
        max_stars = 9
        if total_stars >= 7:
            return "Good Quality", "#28a745"
        elif total_stars >= 5:
            return "Fair Quality", "#ffc107"
        else:
            return "Poor Quality", "#dc3545"
    else:  # Cross-sectional
        max_stars = 8
        if total_stars >= 6:
            return "Good Quality", "#28a745"
        elif total_stars >= 4:
            return "Fair Quality", "#ffc107"
        else:
            return "Poor Quality", "#dc3545"

def create_robvis_plot(studies_data):
    """Create a robvis-style visualization"""
    if not studies_data:
        return None
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(studies_data) * 0.8)))
    
    # Define colors
    colors = {"Good Quality": "#28a745", "Fair Quality": "#ffc107", "Poor Quality": "#dc3545"}
    
    # Prepare data
    study_names = [study['study_name'] for study in studies_data]
    qualities = [get_quality_rating(study['total_stars'], study['study_type'])[0] for study in studies_data]
    
    # Create horizontal bar chart
    y_positions = range(len(study_names))
    bar_colors = [colors[quality] for quality in qualities]
    
    bars = ax.barh(y_positions, [1]*len(study_names), color=bar_colors, alpha=0.7, edgecolor='black', linewidth=1)
    
    # Customize the plot
    ax.set_yticks(y_positions)
    ax.set_yticklabels(study_names, fontsize=10)
    ax.set_xlabel('Quality Assessment', fontsize=12, fontweight='bold')
    ax.set_title('Newcastle-Ottawa Scale Quality Assessment Summary', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    
    # Add star ratings as text
    for i, (bar, study) in enumerate(zip(bars, studies_data)):
        stars_text = "★" * study['total_stars']
        quality_text = f"{qualities[i]} ({study['total_stars']}/9 stars)"
        ax.text(0.5, i, quality_text, ha='center', va='center', fontweight='bold', fontsize=10, color='white')
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, edgecolor='black') 
                      for quality, color in colors.items()]
    ax.legend(legend_elements, colors.keys(), loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    return fig

def create_detailed_assessment_plot(studies_data):
    """Create detailed domain-by-domain assessment plot"""
    if not studies_data:
        return None
    
    # Prepare data for heatmap
    study_names = [study['study_name'] for study in studies_data]
    
    # Get all unique domains across study types
    all_domains = set()
    for study in studies_data:
        study_type = study['study_type']
        for domain in NOS_CRITERIA[study_type].keys():
            all_domains.add(domain)
    
    all_domains = sorted(list(all_domains))
    
    # Create matrix
    matrix = []
    for study in studies_data:
        row = []
        study_type = study['study_type']
        assessment = study['assessment']
        
        for domain in all_domains:
            if domain in NOS_CRITERIA[study_type]:
                domain_stars = 0
                domain_criteria = NOS_CRITERIA[study_type][domain]
                
                for criterion_name, criterion in domain_criteria.items():
                    if criterion_name in assessment:
                        selected_option = assessment[criterion_name]
                        if selected_option in criterion["stars"]:
                            stars = criterion["stars"][selected_option]
                            if criterion_name == "comparability" and "max_stars" in criterion:
                                if selected_option == "most_important":
                                    domain_stars += 1
                                elif selected_option == "additional_factor":
                                    domain_stars += 2
                            else:
                                domain_stars += stars
                
                # Normalize to 0-1 scale based on max possible stars for domain
                max_domain_stars = len(domain_criteria)
                if domain == "Comparability":
                    max_domain_stars = 2
                
                row.append(domain_stars / max_domain_stars if max_domain_stars > 0 else 0)
            else:
                row.append(np.nan)  # Domain not applicable for this study type
        
        matrix.append(row)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, max(6, len(studies_data) * 0.5)))
    
    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(range(len(all_domains)))
    ax.set_xticklabels(all_domains, rotation=45, ha='right')
    ax.set_yticks(range(len(study_names)))
    ax.set_yticklabels(study_names)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Domain Quality Score', rotation=270, labelpad=15)
    
    # Add text annotations
    for i in range(len(study_names)):
        for j in range(len(all_domains)):
            if not np.isnan(matrix[i][j]):
                text = f"{matrix[i][j]:.1f}"
                ax.text(j, i, text, ha="center", va="center", color="black", fontweight='bold')
    
    ax.set_title('Newcastle-Ottawa Scale - Domain-wise Quality Assessment', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig

def export_to_png(fig, filename):
    """Export matplotlib figure to PNG"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    img_buffer.seek(0)
    return img_buffer

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Newcastle-Ottawa Scale Assessment Tool</h1>
        <h3>Systematic Risk of Bias Assessment for Observational Studies</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer information
    st.markdown("""
    <div class="developer-info">
        <strong>🎓 Developed by:</strong> Muhammad Nabeel Saddique<br>
        <strong>📚 Institution:</strong> 4th Year MBBS Student, King Edward Medical University, Lahore, Pakistan<br>
        <strong>🔬 Research Focus:</strong> Systematic Review, Meta-Analysis, Evidence-Based Medicine<br>
        <strong>🏢 Founder:</strong> Nibras Research Academy - Mentoring young researchers in systematic reviews<br>
        <strong>🛠️ Research Tools Expertise:</strong> Rayyan, Zotero, EndNote, WebPlotDigitizer, Meta-Converter, RevMan, MetaXL, Jamovi, CMA, OpenMeta, R Studio
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.header("🎛️ Assessment Controls")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Action",
        ["Add New Study", "View All Studies", "Generate Report", "Export Data"]
    )
    
    if page == "Add New Study":
        st.header("📝 Add New Study Assessment")
        
        with st.form("study_assessment"):
            col1, col2 = st.columns(2)
            
            with col1:
                study_name = st.text_input("Study Name/Identifier", placeholder="e.g., Smith et al. 2023")
                study_type = st.selectbox("Study Type", list(NOS_CRITERIA.keys()))
                
            with col2:
                authors = st.text_input("Authors", placeholder="Smith J, Brown K, Wilson L")
                publication_year = st.number_input("Publication Year", min_value=1900, max_value=2024, value=2023)
            
            journal = st.text_input("Journal", placeholder="Journal of Clinical Medicine")
            doi = st.text_input("DOI (optional)", placeholder="10.1000/xyz123")
            
            st.subheader(f"Assessment Criteria for {study_type}")
            
            assessment = {}
            criteria = NOS_CRITERIA[study_type]
            
            for domain_name, domain in criteria.items():
                st.markdown(f'<div class="domain-header">{domain_name}</div>', unsafe_allow_html=True)
                
                for criterion_name, criterion in domain.items():
                    st.write(f"**{criterion['question']}**")
                    
                    # Create radio button options with star indicators
                    options_display = []
                    option_keys = []
                    for key, description in criterion['options'].items():
                        stars = criterion['stars'].get(key, 0)
                        star_display = "★" * stars if stars > 0 else "☆"
                        options_display.append(f"{description} {star_display}")
                        option_keys.append(key)
                    
                    selected_idx = st.radio(
                        f"Select option for {criterion_name}:",
                        range(len(options_display)),
                        format_func=lambda x: options_display[x],
                        key=criterion_name
                    )
                    
                    assessment[criterion_name] = option_keys[selected_idx]
                
                st.write("")  # Add spacing
            
            # Notes section
            notes = st.text_area("Additional Notes", placeholder="Any additional comments about the study quality...")
            
            submitted = st.form_submit_button("Save Assessment", type="primary")
            
            if submitted:
                if study_name:
                    total_stars = calculate_total_stars(assessment, study_type)
                    quality_rating, quality_color = get_quality_rating(total_stars, study_type)
                    
                    study_data = {
                        "study_name": study_name,
                        "authors": authors,
                        "publication_year": publication_year,
                        "journal": journal,
                        "doi": doi,
                        "study_type": study_type,
                        "assessment": assessment,
                        "total_stars": total_stars,
                        "quality_rating": quality_rating,
                        "notes": notes,
                        "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.studies.append(study_data)
                    
                    st.success(f"✅ Assessment saved successfully!")
                    st.info(f"**Quality Rating:** {quality_rating} ({total_stars}/9 stars)")
                else:
                    st.error("Please provide a study name.")
    
    elif page == "View All Studies":
        st.header("📚 All Study Assessments")
        
        if st.session_state.studies:
            for idx, study in enumerate(st.session_state.studies):
                with st.expander(f"{study['study_name']} - {study['quality_rating']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Authors:** {study['authors']}")
                        st.write(f"**Year:** {study['publication_year']}")
                        st.write(f"**Journal:** {study['journal']}")
                        
                    with col2:
                        st.write(f"**Study Type:** {study['study_type']}")
                        st.write(f"**Stars:** {'★' * study['total_stars']}")
                        st.write(f"**Quality:** {study['quality_rating']}")
                        
                    with col3:
                        st.write(f"**DOI:** {study.get('doi', 'N/A')}")
                        st.write(f"**Assessed:** {study['assessment_date']}")
                    
                    if study.get('notes'):
                        st.write(f"**Notes:** {study['notes']}")
                    
                    # Show detailed assessment
                    if st.checkbox(f"Show detailed assessment", key=f"detail_{idx}"):
                        criteria = NOS_CRITERIA[study['study_type']]
                        
                        for domain_name, domain in criteria.items():
                            st.write(f"**{domain_name}**")
                            domain_stars = 0
                            
                            for criterion_name, criterion in domain.items():
                                selected_option = study['assessment'].get(criterion_name, "")
                                if selected_option in criterion['options']:
                                    option_text = criterion['options'][selected_option]
                                    stars = criterion['stars'].get(selected_option, 0)
                                    
                                    if criterion_name == "comparability" and "max_stars" in criterion:
                                        if selected_option == "most_important":
                                            stars = 1
                                        elif selected_option == "additional_factor":
                                            stars = 2
                                    
                                    domain_stars += stars
                                    star_display = "★" * stars if stars > 0 else "☆"
                                    st.write(f"- {criterion['question']}: {option_text} {star_display}")
                            
                            st.write(f"*Domain Stars: {domain_stars}*")
                            st.write("")
                    
                    # Delete button
                    if st.button(f"Delete Study", key=f"delete_{idx}", type="secondary"):
                        st.session_state.studies.pop(idx)
                        st.experimental_rerun()
        else:
            st.info("No studies assessed yet. Go to 'Add New Study' to start.")
    
    elif page == "Generate Report":
        st.header("📊 Visual Risk of Bias Report")
        
        if st.session_state.studies:
            # Summary statistics
            total_studies = len(st.session_state.studies)
            good_quality = len([s for s in st.session_state.studies if s['quality_rating'] == 'Good Quality'])
            fair_quality = len([s for s in st.session_state.studies if s['quality_rating'] == 'Fair Quality'])
            poor_quality = len([s for s in st.session_state.studies if s['quality_rating'] == 'Poor Quality'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Studies", total_studies)
            with col2:
                st.metric("Good Quality", good_quality, delta=f"{good_quality/total_studies*100:.1f}%")
            with col3:
                st.metric("Fair Quality", fair_quality, delta=f"{fair_quality/total_studies*100:.1f}%")
            with col4:
                st.metric("Poor Quality", poor_quality, delta=f"{poor_quality/total_studies*100:.1f}%")
            
            # Generate visualizations
            st.subheader("📈 Quality Assessment Summary")
            
            # ROBvis-style plot
            fig1 = create_robvis_plot(st.session_state.studies)
            if fig1:
                st.pyplot(fig1)
                
                # Export button for summary plot
                img_buffer1 = export_to_png(fig1, "nos_summary_plot.png")
                st.download_button(
                    label="📥 Download Summary Plot (PNG)",
                    data=img_buffer1.getvalue(),
                    file_name=f"nos_summary_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
            
            st.subheader("🔍 Detailed Domain Assessment")
            
            # Detailed assessment plot
            fig2 = create_detailed_assessment_plot(st.session_state.studies)
            if fig2:
                st.pyplot(fig2)
                
                # Export button for detailed plot
                img_buffer2 = export_to_png(fig2, "nos_detailed_plot.png")
                st.download_button(
                    label="📥 Download Detailed Plot (PNG)",
                    data=img_buffer2.getvalue(),
                    file_name=f"nos_detailed_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
            
            # Study type distribution
            st.subheader("📊 Study Type Distribution")
            study_types = [study['study_type'] for study in st.session_state.studies]
            type_counts = pd.Series(study_types).value_counts()
            
            fig3, ax = plt.subplots(figsize=(8, 6))
            colors_pie = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
            wedges, texts, autotexts = ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
                                             colors=colors_pie, startangle=90)
            ax.set_title('Distribution of Study Types', fontsize=14, fontweight='bold')
            st.pyplot(fig3)
            
            # Export pie chart
            img_buffer3 = export_to_png(fig3, "study_types_distribution.png")
            st.download_button(
                label="📥 Download Study Types Plot (PNG)",
                data=img_buffer3.getvalue(),
                file_name=f"study_types_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
            
        else:
            st.info("No studies to generate report. Please assess some studies first.")
    
    elif page == "Export Data":
        st.header("💾 Export Assessment Data")
        
        if st.session_state.studies:
            # Prepare data for export
            export_data = []
            for study in st.session_state.studies:
                row = {
                    'Study_Name': study['study_name'],
                    'Authors': study['authors'],
                    'Publication_Year': study['publication_year'],
                    'Journal': study['journal'],
                    'DOI': study.get('doi', ''),
                    'Study_Type': study['study_type'],
                    'Total_Stars': study['total_stars'],
                    'Quality_Rating': study['quality_rating'],
                    'Assessment_Date': study['assessment_date'],
                    'Notes': study.get('notes', '')
                }
                
                # Add individual criteria assessments
                for criterion, response in study['assessment'].items():
                    row[f'NOS_{criterion}'] = response
                
                export_data.append(row)
            
            df = pd.DataFrame(export_data)
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV export
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"nos_assessment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # JSON export
                json_data = json.dumps(st.session_state.studies, indent=2, default=str)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name=f"nos_assessment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Summary statistics
            st.subheader("📈 Summary Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Quality Distribution:**")
                quality_dist = df['Quality_Rating'].value_counts()
                for quality, count in quality_dist.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"- {quality}: {count} ({percentage:.1f}%)")
            
            with col2:
                st.write("**Study Type Distribution:**")
                type_dist = df['Study_Type'].value_counts()
                for study_type, count in type_dist.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"- {study_type}: {count} ({percentage:.1f}%)")
            
            # Clear all data option
            st.subheader("🗑️ Data Management")
            if st.button("Clear All Assessment Data", type="secondary"):
                if st.checkbox("I confirm I want to delete all data"):
                    st.session_state.studies = []
                    st.success("All assessment data has been cleared.")
                    st.experimental_rerun()
        
        else:
            st.info("No data to export. Please assess some studies first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Newcastle-Ottawa Scale Assessment Tool</strong></p>
        <p>Developed for systematic review and meta-analysis research</p>
        <p>© 2024 Muhammad Nabeel Saddique | Nibras Research Academy</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()