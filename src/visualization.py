"""
Visualization functions for Shark Attacks dataset.
This module provides reusable plotting functions for data visualization.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_top_countries(top_countries, top3_pct=None, figsize=(12, 6), save_path='reports/h1_geographic.png'):
    """
    Plot top countries by shark attacks.

    Args:
        top_countries (pd.Series): Series with country attack counts
        top3_pct (float, optional): Percentage for top 3 countries annotation
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/h1_geographic.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    top_countries.plot(kind='bar', color='steelblue', ax=ax)
    ax.set_title('Top 10 Countries by Shark Attacks', fontsize=16, fontweight='bold')
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel('Number of Attacks', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')

    if top3_pct:
        ax.text(0.98, 0.98, f'Top 3 = {top3_pct:.1f}%',
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_top_activities(top_activities, activity_pct=None, figsize=(12, 6), save_path='reports/h2_activities.png'):
    """
    Plot top activities during shark attacks.

    Args:
        top_activities (pd.Series): Series with activity counts
        activity_pct (float, optional): Percentage for surfing/swimming annotation
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/h2_activities.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    top_activities.plot(kind='barh', color='coral', ax=ax)
    ax.set_title('Top 10 Activities During Shark Attacks', fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Attacks', fontsize=12)
    ax.set_ylabel('Activity', fontsize=12)
    ax.grid(axis='x', alpha=0.3)

    if activity_pct:
        ax.text(0.98, 0.02, f'Surfing + Swimming = {activity_pct:.1f}%',
                transform=ax.transAxes,
                verticalalignment='bottom',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_gender_analysis(gender_counts, fatal_by_gender, ratio=None, figsize=(14, 6), save_path='reports/h3_gender.png'):
    """
    Plot gender distribution and fatality rates.

    Args:
        gender_counts (pd.Series): Gender distribution counts
        fatal_by_gender (pd.Series): Fatality rates by gender
        ratio (float, optional): Male to female ratio
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/h3_gender.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Pie chart
    colors = ['#3498db', '#e74c3c']
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors, ax=ax1)
    ax1.set_title('Shark Attacks by Gender', fontsize=16, fontweight='bold')
    ax1.set_ylabel('')

    if ratio:
        ax1.text(0, -1.3, f'M:F Ratio = {ratio:.1f}:1',
                 ha='center',
                 fontsize=11,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Fatality rate bar chart
    fatal_by_gender.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=ax2)
    ax2.set_title('Fatality Rate by Gender', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Gender', fontsize=12)
    ax2.set_ylabel('Fatality Rate (%)', fontsize=12)
    ax2.set_xticklabels(['Male', 'Female'], rotation=0)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_temporal_trends(attacks_by_decade, attacks_by_year, increase_pct=None, figsize=(14, 10), save_path='reports/h4_temporal.png'):
    """
    Plot temporal trends - decades and yearly.

    Args:
        attacks_by_decade (pd.Series): Attacks by decade
        attacks_by_year (pd.Series): Attacks by year
        increase_pct (float, optional): Percentage increase over time
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/h4_temporal.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    # Decade trend
    attacks_by_decade.plot(kind='bar', color='teal', ax=ax1)
    ax1.set_title('Shark Attacks by Decade', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Decade', fontsize=12)
    ax1.set_ylabel('Number of Attacks', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)

    if increase_pct:
        ax1.text(0.98, 0.98, f'{increase_pct:.0f}% increase',
                 transform=ax1.transAxes,
                 verticalalignment='top',
                 horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Recent years trend
    attacks_by_year.plot(kind='line', marker='o', color='darkred', linewidth=2, ax=ax2)
    ax2.set_title('Shark Attacks Trend (Recent 50 Years)', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Number of Attacks', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.fill_between(attacks_by_year.index, attacks_by_year.values, alpha=0.3, color='darkred')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_species(top_species, figsize=(12, 6), save_path='reports/species.png'):
    """
    Plot top shark species involved in attacks.

    Args:
        top_species (pd.Series): Top species counts
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/species.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    top_species.plot(kind='barh', color='darkslategray', ax=ax)
    ax.set_title('Top 10 Shark Species Involved in Attacks', fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Attacks', fontsize=12)
    ax.set_ylabel('Species', fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_age_distribution(age_data, figsize=(14, 6), save_path='reports/age_distribution.png'):
    """
    Plot age distribution with histogram and box plot.

    Args:
        age_data (pd.Series): Age data
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/age_distribution.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Histogram
    ax1.hist(age_data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    ax1.set_title('Age Distribution of Shark Attack Victims', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Age', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.axvline(age_data.mean(), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {age_data.mean():.1f}')
    ax1.axvline(age_data.median(), color='green', linestyle='--', linewidth=2,
                label=f'Median: {age_data.median():.1f}')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # Box plot
    ax2.boxplot(age_data, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightcoral', alpha=0.7),
                medianprops=dict(color='darkred', linewidth=2))
    ax2.set_title('Age Distribution Box Plot', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Age', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_fatality_analysis(fatal_counts, fatality_by_country, overall_rate=None, figsize=(14, 6), save_path='reports/fatality.png'):
    """
    Plot fatality rates overall and by country.

    Args:
        fatal_counts (pd.Series): Overall fatality counts
        fatality_by_country (pd.Series): Fatality rates by country
        overall_rate (float, optional): Overall fatality rate percentage
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/fatality.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Overall fatality pie chart
    fatal_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90,
                      colors=['#2ecc71', '#e74c3c'], ax=ax1,
                      labels=['Non-Fatal', 'Fatal'])
    ax1.set_title('Overall Attack Outcomes', fontsize=16, fontweight='bold')
    ax1.set_ylabel('')

    if overall_rate:
        ax1.text(0, -1.3, f'Fatality Rate = {overall_rate:.1f}%',
                 ha='center',
                 fontsize=11,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Fatality by country
    fatality_by_country.plot(kind='bar', color='crimson', ax=ax2)
    ax2.set_title('Fatality Rate by Country (Top 5)', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Country', fontsize=12)
    ax2.set_ylabel('Fatality Rate (%)', fontsize=12)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_risk_score(surf_by_country, n_safest=7, n_riskiest=8, figsize=(14, 8), save_path='reports/risk_score.png'):
    """
    Plot surf location risk scores.

    Args:
        surf_by_country (pd.DataFrame): DataFrame with risk scores
        n_safest (int): Number of safest countries to show
        n_riskiest (int): Number of riskiest countries to show
        figsize (tuple): Figure size
        save_path (str, optional): Path to save the figure (default: reports/risk_score.png)

    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Show safest and riskiest
    top_bottom = pd.concat([surf_by_country.head(n_safest), surf_by_country.tail(n_riskiest)])
    colors = ['green' if x < 30 else 'orange' if x < 50 else 'red' for x in top_bottom['Risk_Score']]

    top_bottom['Risk_Score'].plot(kind='barh', color=colors, ax=ax)
    ax.set_title('Surf Location Risk Score by Country\n(Lower = Safer)',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Risk Score', fontsize=12)
    ax.set_ylabel('Country', fontsize=12)
    ax.axvline(30, color='green', linestyle='--', alpha=0.5, label='Low Risk (<30)')
    ax.axvline(50, color='orange', linestyle='--', alpha=0.5, label='Medium Risk (30-50)')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def set_plot_style(style='seaborn-v0_8-darkgrid', palette='husl'):
    """
    Set global plotting style for consistency.

    Args:
        style (str): Matplotlib style
        palette (str): Seaborn color palette
    """
    plt.style.use(style)
    sns.set_palette(palette)
