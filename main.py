import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO
import zipfile


# Function to generate dataset report
def generate_dataset_report(df, report_folder):
    # Summary statistics for continuous data
    continuous_data_summary = df.describe()

    # Count of unique values for categorical data
    categorical_data_summary = df.select_dtypes(include='object').nunique()

    # Plot histograms for continuous data
    for column in df.select_dtypes(include='number').columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[column], kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        histogram_path = os.path.join(report_folder, f'{column}_histogram.png')
        plt.savefig(histogram_path)
        plt.close()

    # Save summary statistics to a file
    with open(os.path.join(report_folder, 'dataset_report.txt'), 'w') as report_file:
        report_file.write("Summary Statistics for Continuous Data:\n")
        report_file.write(continuous_data_summary.to_string() + "\n\n")
        report_file.write("Count of Unique Values for Categorical Data:\n")
        report_file.write(categorical_data_summary.to_string())

    return report_folder


# Function to create a zip file containing the report folder
def create_zip_report(report_folder):
    with zipfile.ZipFile('report.zip', 'w') as zipf:
        for root, dirs, files in os.walk(report_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), report_folder))


# Streamlit UI
def main():
    st.title("Dataset Report Generator")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload a dataset (CSV file)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded dataset:")
        st.write(df.head())

        # Button to generate report
        if st.button("Generate Report"):
            report_folder = 'report'
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)

            generate_dataset_report(df, report_folder)
            st.success("Dataset report generated successfully!")

            # Create a zip file containing the report folder
            create_zip_report(report_folder)

            # Provide download link for the zip file
            with open('report.zip', 'rb') as f:
                zip_bytes = f.read()
            st.download_button(label="Download Report", data=BytesIO(zip_bytes), file_name="report.zip")


if __name__ == "__main__":
    main()
