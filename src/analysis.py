"""
Analysis functions for Shark Attacks dataset.
This module provides reusable analysis functions for hypothesis testing and insights.
"""

import pandas as pd
import numpy as np


def analyze_geographic_hotspots(df, top_n=10):
    """
    Analyze geographic distribution of shark attacks.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        top_n (int): Number of top countries to return

    Returns:
        dict: Dictionary containing analysis results
    """
    top_countries = df['Country'].value_counts().head(top_n)
    top3_total = top_countries.head(3).sum()
    top3_percentage = (top3_total / len(df)) * 100

    return {
        'top_countries': top_countries,
        'top3_percentage': top3_percentage,
        'top3_countries': top_countries.head(3).index.tolist()
    }


def analyze_activity_risk(df, top_n=10):
    """
    Analyze which activities have the highest shark attack rates.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        top_n (int): Number of top activities to return

    Returns:
        dict: Dictionary containing analysis results
    """
    top_activities = df['Activity'].value_counts().head(top_n)

    # Calculate surfing + swimming percentage
    surfing_swimming = df[df['Activity'].str.contains('Surfing|Swimming', case=False, na=False)]
    activity_percentage = (len(surfing_swimming) / len(df)) * 100

    return {
        'top_activities': top_activities,
        'surfing_swimming_pct': activity_percentage,
        'surfing_count': len(df[df['Activity'].str.contains('Surfing', case=False, na=False)]),
        'swimming_count': len(df[df['Activity'].str.contains('Swimming', case=False, na=False)])
    }


def analyze_gender_disparity(df):
    """
    Analyze gender distribution in shark attacks.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe

    Returns:
        dict: Dictionary containing analysis results
    """
    gender_counts = df['Sex'].value_counts()
    male_count = gender_counts.get('M', 0)
    female_count = gender_counts.get('F', 0)
    ratio = male_count / female_count if female_count > 0 else 0

    # Fatality rate by gender
    fatal_by_gender = df.groupby('Sex')['Fatal Y/N'].apply(
        lambda x: (x == 'Y').sum() / len(x) * 100
    )

    return {
        'gender_counts': gender_counts,
        'male_count': male_count,
        'female_count': female_count,
        'ratio': ratio,
        'fatality_by_gender': fatal_by_gender
    }


def analyze_temporal_trends(df, start_year=1900, end_year=2025):
    """
    Analyze temporal trends in shark attacks over time.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        start_year (int): Start year for analysis
        end_year (int): End year for analysis

    Returns:
        dict: Dictionary containing analysis results
    """
    # Filter for valid years
    df_temporal = df[df['Year'].notna() &
                     (df['Year'] >= start_year) &
                     (df['Year'] <= end_year)].copy()

    # Attacks by decade
    df_temporal['Decade'] = (df_temporal['Year'] // 10) * 10
    attacks_by_decade = df_temporal['Decade'].value_counts().sort_index()

    # Attacks by year (recent 50 years)
    recent_cutoff = end_year - 50
    recent_years = df_temporal[df_temporal['Year'] >= recent_cutoff]
    attacks_by_year = recent_years.groupby('Year').size()

    # Calculate trend
    early_avg = attacks_by_decade.iloc[:5].mean() if len(attacks_by_decade) >= 5 else 0
    recent_avg = attacks_by_decade.iloc[-5:].mean() if len(attacks_by_decade) >= 5 else 0
    increase_pct = ((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0

    return {
        'attacks_by_decade': attacks_by_decade,
        'attacks_by_year': attacks_by_year,
        'early_avg': early_avg,
        'recent_avg': recent_avg,
        'increase_percentage': increase_pct
    }


def analyze_species(df, top_n=10):
    """
    Analyze shark species involved in attacks.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        top_n (int): Number of top species to return

    Returns:
        pd.Series: Top species by attack count
    """
    species_col = 'Species ' if 'Species ' in df.columns else 'Species'
    top_species = df[species_col].value_counts().head(top_n)
    return top_species


def analyze_age_distribution(df):
    """
    Analyze age distribution of shark attack victims.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe

    Returns:
        dict: Dictionary containing age statistics
    """
    df_age = df[df['Age'].notna()]

    return {
        'stats': df_age['Age'].describe(),
        'mean': df_age['Age'].mean(),
        'median': df_age['Age'].median(),
        'mode': df_age['Age'].mode().values[0] if len(df_age['Age'].mode()) > 0 else None,
        'age_data': df_age['Age']
    }


def analyze_fatality_rates(df, top_n_countries=5):
    """
    Analyze fatality rates overall and by country.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        top_n_countries (int): Number of top countries to analyze

    Returns:
        dict: Dictionary containing fatality analysis
    """
    fatal_counts = df['Fatal Y/N'].value_counts()
    total_with_data = fatal_counts.sum()
    fatality_rate = (fatal_counts.get('Y', 0) / total_with_data) * 100 if total_with_data > 0 else 0

    # Fatality by country (top N)
    top_countries_list = df['Country'].value_counts().head(top_n_countries).index
    fatality_by_country = df[df['Country'].isin(top_countries_list)].groupby('Country')['Fatal Y/N'].apply(
        lambda x: (x == 'Y').sum() / len(x) * 100 if len(x) > 0 else 0
    ).sort_values(ascending=False)

    return {
        'fatal_counts': fatal_counts,
        'overall_fatality_rate': fatality_rate,
        'fatality_by_country': fatality_by_country
    }


def calculate_surf_risk_score(df, min_attacks=10):
    """
    Calculate risk scores for surfing locations by country.
    Risk score combines attack frequency and fatality rate.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe
        min_attacks (int): Minimum number of attacks for statistical relevance

    Returns:
        pd.DataFrame: Countries with risk scores (sorted by risk)
    """
    # Filter for surfing-related activities
    df_surfing = df[df['Activity'].str.contains('Surf', case=False, na=False)]

    # Calculate attacks and fatality rate by country
    surf_by_country = df_surfing.groupby('Country').agg({
        'Fatal Y/N': ['count', lambda x: (x == 'Y').sum() / len(x) * 100 if len(x) > 0 else 0]
    }).round(2)

    surf_by_country.columns = ['Attack_Count', 'Fatality_Rate']

    # Filter for statistical relevance
    surf_by_country = surf_by_country[surf_by_country['Attack_Count'] >= min_attacks]

    # Calculate risk score (lower is better)
    # Formula: (normalized attack count * 50) + fatality rate
    max_attacks = surf_by_country['Attack_Count'].max()
    surf_by_country['Risk_Score'] = (
        (surf_by_country['Attack_Count'] / max_attacks * 50) +
        (surf_by_country['Fatality_Rate'])
    ).round(2)

    # Sort by risk score
    surf_by_country = surf_by_country.sort_values('Risk_Score')

    return surf_by_country


def get_summary_statistics(df):
    """
    Get overall summary statistics for the dataset.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe

    Returns:
        dict: Dictionary containing summary statistics
    """
    return {
        'total_attacks': len(df),
        'date_range': (df['Year'].min(), df['Year'].max()),
        'countries_count': df['Country'].nunique(),
        'activities_count': df['Activity'].nunique(),
        'avg_age': df['Age'].mean(),
        'median_age': df['Age'].median(),
        'overall_fatality_rate': (df['Fatal Y/N'] == 'Y').sum() / len(df) * 100
    }


def validate_all_hypotheses(df):
    """
    Run all hypothesis tests and return results in a single call.

    Args:
        df (pd.DataFrame): Cleaned shark attacks dataframe

    Returns:
        dict: Dictionary containing all hypothesis test results
    """
    h1 = analyze_geographic_hotspots(df)
    h2 = analyze_activity_risk(df)
    h3 = analyze_gender_disparity(df)
    h4 = analyze_temporal_trends(df)

    return {
        'h1_geographic': h1,
        'h2_activity': h2,
        'h3_gender': h3,
        'h4_temporal': h4,
        'summary': get_summary_statistics(df)
    }
