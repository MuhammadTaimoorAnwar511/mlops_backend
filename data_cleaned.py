import pandas as pd
import os

def clean_and_analyze_data():
    # Load the data
    input_file = "Data/bitcoin_prices.csv"
    output_file = "Data/bitcoin_prices_cleaned.csv"

    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    # Load data into a DataFrame
    data = pd.read_csv(input_file, parse_dates=["Date"])

    # Display basic info
    print("Initial Data Overview:")
    print(data.info())
    print("\nSummary Statistics:")
    print(data.describe())

    # Check for missing values
    print("\nChecking for missing values:")
    print(data.isnull().sum())

    # Check for duplicates
    print("\nChecking for duplicate rows:")
    duplicate_count = data.duplicated().sum()
    if duplicate_count > 0:
        print(f"Found {duplicate_count} duplicate rows. Removing duplicates...")
        data = data.drop_duplicates()
    else:
        print("No duplicate rows found.")

    # Check for negative values in relevant columns
    print("\nChecking for negative values:")
    relevant_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in relevant_columns:
        if (data[col] < 0).any():
            print(f"Warning: Negative values found in column '{col}'")
            print(data[data[col] < 0])
        else:
            print(f"No negative values in column '{col}'")

    # Add Adj Close column by copying values from Close
    data['Adj Close'] = data['Close']

    # Retain only the relevant columns
    cleaned_data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Save cleaned data
    os.makedirs("Data", exist_ok=True)
    cleaned_data.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to {output_file}")

if __name__ == "__main__":
    clean_and_analyze_data()
