"""
Data cleaning classes and functions for Shark Attacks dataset.
This module provides modular cleaning functionality for the GSAF5 dataset.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime


class DataCleaner:
    """
    Data cleaning pipeline for shark attacks dataset.

    This class handles all data cleaning operations including:
    - Empty column removal
    - Duplicate removal
    - Column standardization (Sex, Fatal, Type, Age, Country, Activity, Species)
    - Date parsing
    - Missing value handling

    Attributes:
        df (pd.DataFrame): The dataframe being cleaned
        verbose (bool): Whether to track cleaning steps
        cleaning_log (list): Log of cleaning operations performed
    """

    def __init__(self, df, verbose=False):
        """
        Initialize the DataCleaner with a dataframe.

        Args:
            df (pd.DataFrame): Input dataframe to clean
            verbose (bool): Whether to log cleaning steps
        """
        self.df = df.copy()
        self.verbose = verbose
        self.cleaning_log = []

    def log_step(self, message):
        """Add a message to the cleaning log if verbose mode is on."""
        if self.verbose:
            self.cleaning_log.append(message)

    def remove_empty_columns(self):
        """
        Remove columns that are completely empty or contain only NaN values.
        Also removes unnamed columns with >95% missing values.

        Returns:
            self: For method chaining
        """
        # Identify columns with all NaN values
        empty_cols = self.df.columns[self.df.isnull().all()].tolist()

        # Also remove columns that are named "Unnamed: X" and have >95% missing values
        unnamed_cols = [col for col in self.df.columns
                       if col.startswith('Unnamed:') and self.df[col].isnull().sum() / len(self.df) > 0.95]

        cols_to_drop = list(set(empty_cols + unnamed_cols))

        self.df = self.df.drop(columns=cols_to_drop)
        self.log_step(f"Removed {len(cols_to_drop)} empty/unnamed columns")

        return self

    def remove_duplicates(self):
        """
        Remove duplicate rows from the dataset.

        Returns:
            self: For method chaining
        """
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)

        self.log_step(f"Removed {removed} duplicate rows")

        return self

    def clean_sex_column(self):
        """
        Standardize the Sex column to contain only 'M', 'F', or NaN.

        Returns:
            self: For method chaining
        """
        if 'Sex' not in self.df.columns:
            return self

        # Strip whitespace and convert to uppercase
        self.df['Sex'] = self.df['Sex'].astype(str).str.strip().str.upper()

        # Map variations to standard values
        sex_mapping = {
            'M': 'M',
            'F': 'F',
            'MALE': 'M',
            'FEMALE': 'F',
            'N': np.nan,
            'NAN': np.nan,
            '.': np.nan,
            '': np.nan
        }

        self.df['Sex'] = self.df['Sex'].replace(sex_mapping)

        # Set anything not M or F to NaN
        self.df.loc[~self.df['Sex'].isin(['M', 'F']), 'Sex'] = np.nan

        self.log_step(f"Cleaned Sex column - unique values: {self.df['Sex'].unique()}")

        return self

    def clean_fatal_column(self):
        """
        Standardize the Fatal Y/N column to contain only 'Y', 'N', or NaN.

        Returns:
            self: For method chaining
        """
        if 'Fatal Y/N' not in self.df.columns:
            return self

        # Strip whitespace and convert to uppercase
        self.df['Fatal Y/N'] = self.df['Fatal Y/N'].astype(str).str.strip().str.upper()

        # Map variations to standard values
        fatal_mapping = {
            'Y': 'Y',
            'N': 'N',
            'YES': 'Y',
            'NO': 'N',
            'F': 'Y',  # F might mean Fatal
            'M': np.nan,
            'UNKNOWN': np.nan,
            'NAN': np.nan,
            '': np.nan,
            '2017': np.nan  # Sometimes has erroneous data
        }

        self.df['Fatal Y/N'] = self.df['Fatal Y/N'].replace(fatal_mapping)

        # Set anything not Y or N to NaN
        self.df.loc[~self.df['Fatal Y/N'].isin(['Y', 'N']), 'Fatal Y/N'] = np.nan

        self.log_step(f"Cleaned Fatal Y/N column - unique values: {self.df['Fatal Y/N'].unique()}")

        return self

    def clean_type_column(self):
        """
        Standardize the Type column (Unprovoked, Provoked, etc.).

        Returns:
            self: For method chaining
        """
        if 'Type' not in self.df.columns:
            return self

        # Strip whitespace
        self.df['Type'] = self.df['Type'].astype(str).str.strip()

        # Replace 'Invalid' or 'Questionable' with NaN
        self.df.loc[self.df['Type'].isin(['Invalid', 'Questionable', 'Unconfirmed', 'Unverified']), 'Type'] = np.nan

        self.log_step(f"Cleaned Type column - unique values: {self.df['Type'].nunique()}")

        return self

    def clean_age_column(self):
        """
        Clean and standardize the Age column to numeric values.
        Handles formats like '25', 'ca. 30', '20s', 'Teen', 'adult', etc.

        Returns:
            self: For method chaining
        """
        if 'Age' not in self.df.columns:
            return self

        def parse_age(age_str):
            """Parse various age formats to a numeric value."""
            if pd.isna(age_str):
                return np.nan

            age_str = str(age_str).strip().lower()

            # Handle empty strings
            if age_str in ['', 'nan', 'unknown', '?']:
                return np.nan

            # Extract first number found
            numbers = re.findall(r'\d+', age_str)
            if numbers:
                age = int(numbers[0])
                # Validate reasonable age range
                if 0 < age < 120:
                    return age

            # Handle text descriptions
            age_text_mapping = {
                'teen': 15,
                'teenager': 15,
                'adult': 30,
                'child': 8,
                'boy': 10,
                'girl': 10,
                'young': 25,
                'elderly': 70,
                'middle': 45
            }

            for key, value in age_text_mapping.items():
                if key in age_str:
                    return value

            return np.nan

        self.df['Age'] = self.df['Age'].apply(parse_age)

        self.log_step(f"Cleaned Age column - valid ages: {self.df['Age'].notna().sum()}")

        return self

    def clean_country_column(self):
        """
        Standardize country names and fix common inconsistencies.

        Returns:
            self: For method chaining
        """
        if 'Country' not in self.df.columns:
            return self

        # Strip whitespace and standardize case
        self.df['Country'] = self.df['Country'].astype(str).str.strip().str.upper()

        # Common country name standardizations
        country_mapping = {
            'USA': 'USA',
            'UNITED STATES': 'USA',
            'UNITED STATES OF AMERICA': 'USA',
            'US': 'USA',
            'AUSTRALIA': 'AUSTRALIA',
            'SOUTH AFRICA': 'SOUTH AFRICA',
            'RSA': 'SOUTH AFRICA',
            'REPUBLIC OF SOUTH AFRICA': 'SOUTH AFRICA',
            'ENGLAND': 'UNITED KINGDOM',
            'SCOTLAND': 'UNITED KINGDOM',
            'WALES': 'UNITED KINGDOM',
            'UK': 'UNITED KINGDOM'
        }

        self.df['Country'] = self.df['Country'].replace(country_mapping)

        # Replace 'NAN' string with actual NaN
        self.df.loc[self.df['Country'] == 'NAN', 'Country'] = np.nan

        self.log_step(f"Cleaned Country column - unique countries: {self.df['Country'].nunique()}")

        return self

    def clean_activity_column(self):
        """
        Standardize activity descriptions.

        Returns:
            self: For method chaining
        """
        if 'Activity' not in self.df.columns:
            return self

        # Strip whitespace and standardize case
        self.df['Activity'] = self.df['Activity'].astype(str).str.strip().str.title()

        # Replace 'Nan' with actual NaN
        self.df.loc[self.df['Activity'].str.lower() == 'nan', 'Activity'] = np.nan

        self.log_step(f"Cleaned Activity column - unique activities: {self.df['Activity'].nunique()}")

        return self

    def clean_species_column(self):
        """
        Clean and standardize shark species information.

        Returns:
            self: For method chaining
        """
        # Note: Column name has a trailing space
        species_col = 'Species ' if 'Species ' in self.df.columns else 'Species'

        if species_col not in self.df.columns:
            return self

        # Strip whitespace
        self.df[species_col] = self.df[species_col].astype(str).str.strip()

        # Replace invalid/unknown markers with NaN
        invalid_markers = [
            'Invalid', 'Unknown', 'Not stated', 'Unconfirmed',
            'Shark involvement not confirmed',
            'Shark involvement prior to death was not confirmed',
            'No shark involvement', 'Questionable', 'nan'
        ]

        self.df.loc[self.df[species_col].isin(invalid_markers), species_col] = np.nan

        # Standardize common species names
        species_mapping = {
            'White shark': 'White Shark',
            'white shark': 'White Shark',
            'Great white shark': 'White Shark',
            'Great White Shark': 'White Shark',
            'Tiger shark': 'Tiger Shark',
            'tiger shark': 'Tiger Shark',
            'Bull shark': 'Bull Shark',
            'bull shark': 'Bull Shark'
        }

        self.df[species_col] = self.df[species_col].replace(species_mapping)

        self.log_step(f"Cleaned Species column - unique species: {self.df[species_col].nunique()}")

        return self

    def parse_dates(self):
        """
        Parse and standardize date information using regex patterns.
        Creates a standardized 'Date_Parsed' column.

        Returns:
            self: For method chaining
        """
        if 'Date' not in self.df.columns:
            return self

        def extract_date(date_str, year_str):
            """Extract date from various formats."""
            if pd.isna(date_str):
                return np.nan

            date_str = str(date_str).strip()

            # Pattern: "27th November" or "10th November" etc.
            pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)'
            match = re.search(pattern, date_str)

            if match and year_str and str(year_str).isdigit():
                day = match.group(1)
                month = match.group(2)
                year = str(year_str).strip()

                try:
                    # Construct date string and parse
                    date_obj = pd.to_datetime(f"{day} {month} {year}", format='%d %B %Y', errors='coerce')
                    return date_obj
                except:
                    return np.nan

            return np.nan

        # Apply date parsing
        self.df['Date_Parsed'] = self.df.apply(lambda row: extract_date(row['Date'], row['Year']), axis=1)

        # Also ensure Year is numeric
        self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')

        parsed_count = self.df['Date_Parsed'].notna().sum()
        self.log_step(f"Parsed {parsed_count} dates successfully")

        return self

    def handle_missing_values(self, threshold=0.7):
        """
        Handle missing values based on a threshold.
        Drops columns with more than threshold% missing values.

        Args:
            threshold (float): Proportion of missing values above which to drop column

        Returns:
            self: For method chaining
        """
        initial_cols = len(self.df.columns)

        # Calculate missing percentage for each column
        missing_pct = self.df.isnull().sum() / len(self.df)

        # Drop columns exceeding threshold
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
        self.df = self.df.drop(columns=cols_to_drop)

        self.log_step(f"Dropped {len(cols_to_drop)} columns with >{threshold*100}% missing values")

        return self

    def clean_all(self, threshold=0.7):
        """
        Run the complete cleaning pipeline.

        Args:
            threshold (float): Missing value threshold for column removal

        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        self.log_step(f"Starting cleaning pipeline - Initial shape: {self.df.shape}")

        (self
         .remove_empty_columns()
         .remove_duplicates()
         .clean_sex_column()
         .clean_fatal_column()
         .clean_type_column()
         .clean_age_column()
         .clean_country_column()
         .clean_activity_column()
         .clean_species_column()
         .parse_dates()
         .handle_missing_values(threshold))

        self.log_step(f"Cleaning complete - Final shape: {self.df.shape}")

        return self.df

    def get_cleaning_report(self):
        """
        Get a summary report of all cleaning operations performed.

        Returns:
            dict: Dictionary containing cleaning statistics
        """
        return {
            'steps_performed': len(self.cleaning_log),
            'log': self.cleaning_log,
            'final_shape': self.df.shape,
            'columns': list(self.df.columns)
        }


# Convenience function for simple usage
def clean_data(filepath, save_cleaned=True, verbose=False):
    """
    Convenience function to clean shark attacks data from a CSV file.

    Args:
        filepath (str): Path to the raw CSV file
        save_cleaned (bool): Whether to save the cleaned data to a new file
        verbose (bool): Whether to show cleaning progress

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    # Load data
    df = pd.read_csv(filepath, sep=";", low_memory=False)

    # Clean using DataCleaner class
    cleaner = DataCleaner(df, verbose=verbose)
    df_clean = cleaner.clean_all()

    # Save if requested
    if save_cleaned:
        output_path = filepath.replace('.csv', '_cleaned.csv')
        df_clean.to_csv(output_path, index=False)

    return df_clean


# Legacy standalone functions for backward compatibility
def remove_empty_columns(df):
    """Remove empty columns from dataframe."""
    cleaner = DataCleaner(df)
    return cleaner.remove_empty_columns().df

def remove_duplicates(df):
    """Remove duplicate rows from dataframe."""
    cleaner = DataCleaner(df)
    return cleaner.remove_duplicates().df

def clean_sex_column(df):
    """Clean Sex column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_sex_column().df

def clean_fatal_column(df):
    """Clean Fatal Y/N column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_fatal_column().df

def clean_type_column(df):
    """Clean Type column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_type_column().df

def clean_age_column(df):
    """Clean Age column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_age_column().df

def clean_country_column(df):
    """Clean Country column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_country_column().df

def clean_activity_column(df):
    """Clean Activity column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_activity_column().df

def clean_species_column(df):
    """Clean Species column."""
    cleaner = DataCleaner(df)
    return cleaner.clean_species_column().df

def parse_dates(df):
    """Parse dates."""
    cleaner = DataCleaner(df)
    return cleaner.parse_dates().df

def handle_missing_values(df, threshold=0.5):
    """Handle missing values."""
    cleaner = DataCleaner(df)
    return cleaner.handle_missing_values(threshold).df


if __name__ == "__main__":
    # Example usage
    df_clean = clean_data('data/shark_attacks.csv', verbose=True)
