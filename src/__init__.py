"""
Shark Attacks Data Analysis Package

This package provides data cleaning, analysis, and visualization utilities
for the GSAF5 shark attacks dataset.
"""

from .cleaning import (
    clean_data,
    remove_empty_columns,
    remove_duplicates,
    clean_sex_column,
    clean_fatal_column,
    clean_type_column,
    clean_age_column,
    clean_country_column,
    clean_activity_column,
    clean_species_column,
    parse_dates,
    handle_missing_values
)

from .analysis import (
    analyze_geographic_hotspots,
    analyze_activity_risk,
    analyze_gender_disparity,
    analyze_temporal_trends,
    analyze_species,
    analyze_age_distribution,
    analyze_fatality_rates,
    calculate_surf_risk_score,
    get_summary_statistics,
    validate_all_hypotheses
)

from .visualization import (
    plot_top_countries,
    plot_top_activities,
    plot_gender_analysis,
    plot_temporal_trends,
    plot_species,
    plot_age_distribution,
    plot_fatality_analysis,
    plot_risk_score,
    set_plot_style
)

__all__ = [
    # Cleaning functions
    'clean_data',
    'remove_empty_columns',
    'remove_duplicates',
    'clean_sex_column',
    'clean_fatal_column',
    'clean_type_column',
    'clean_age_column',
    'clean_country_column',
    'clean_activity_column',
    'clean_species_column',
    'parse_dates',
    'handle_missing_values',
    # Analysis functions
    'analyze_geographic_hotspots',
    'analyze_activity_risk',
    'analyze_gender_disparity',
    'analyze_temporal_trends',
    'analyze_species',
    'analyze_age_distribution',
    'analyze_fatality_rates',
    'calculate_surf_risk_score',
    'get_summary_statistics',
    'validate_all_hypotheses',
    # Visualization functions
    'plot_top_countries',
    'plot_top_activities',
    'plot_gender_analysis',
    'plot_temporal_trends',
    'plot_species',
    'plot_age_distribution',
    'plot_fatality_analysis',
    'plot_risk_score',
    'set_plot_style'
]

__version__ = '1.0.0'
