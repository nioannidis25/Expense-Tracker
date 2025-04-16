import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded CSV file
file_path = "C:\\Users\\nioan\Downloads\\transactions_export_2025-04-13_cash-wallet.csv"
df = pd.read_csv(file_path)

# Copy the original dataframe for cleaning
df_clean = df.copy()

# Convert Date to datetime format
df_clean['Date'] = pd.to_datetime(df_clean['Date'])

# Create new fields for analysis
df_clean['Year'] = df_clean['Date'].dt.year
df_clean['Month'] = df_clean['Date'].dt.month
df_clean['Weekday'] = df_clean['Date'].dt.day_name()

# Create a new column "Clean_Amount" with absolute values for easier analysis
df_clean['Clean_Amount'] = df_clean['Amount'].abs()

# Normalize Category names (all lowercase, strip whitespace)
df_clean['Category name'] = df_clean['Category name'].str.strip().str.lower()

# Remove unnecessary fields
df_clean.drop(columns=['Wallet', 'Currency', 'Author', 'Note'], inplace=True)

# Show basic info and a sample to understand structure
print(df_clean.info())
print(df_clean.head())

# Filter only expenses
expenses_only = df_clean[df_clean['Type'] == 'Expense']

# Top 5 expense categories
top_expense_categories = expenses_only.groupby('Category name')['Clean_Amount'].sum().sort_values(ascending=False).head(5)

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(top_expense_categories.index, top_expense_categories.values)
plt.title('Top 5 expense categories (from 4/24- 4/25)')
plt.xlabel('Category')
plt.ylabel('Total Expenses(€)')
plt.xticks(rotation=45)
plt.grid(axis='y')

# Add values on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.tight_layout()
plt.show()

# Group expenses by month
monthly_expenses = expenses_only.groupby('Month')['Clean_Amount'].sum().sort_index()

# Create bar chart with values above each bar
plt.figure(figsize=(10, 6))
bars = plt.bar(monthly_expenses.index, monthly_expenses.values)

plt.title('Total Expenses Per Month')
plt.xlabel('Month')
plt.ylabel('Total Expenses(€)')
plt.xticks(ticks=range(1, 13))
plt.grid(axis='y')

# Add values on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Filter only 2024 records with Type == 'Expense'
expenses_2024 = df_clean[(df_clean['Type'] == 'Expense') & (df_clean['Year'] == 2024)]

# 1. Top 5 Expense Categories for 2024
top_expense_2024 = expenses_2024.groupby('Category name')['Clean_Amount'].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(10, 6))
bars1 = plt.bar(top_expense_2024.index, top_expense_2024.values)
plt.title('Top 5 Expense Categories (2024)')
plt.xlabel('Category')
plt.ylabel('Total Expenses (€)')
plt.xticks(rotation=45)
plt.grid(axis='y')
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Total Expenses per Month for 2024
monthly_expenses_2024 = expenses_2024.groupby('Month')['Clean_Amount'].sum().sort_index()

plt.figure(figsize=(10, 6))
bars2 = plt.bar(monthly_expenses_2024.index, monthly_expenses_2024.values)
plt.title('Total Expenses Per Month (2024)')
plt.xlabel('Month')
plt.ylabel('Total Expenses (€)')
plt.xticks(ticks=range(1, 13))
plt.grid(axis='y')
for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.show()

# For each month in 2024, find the category with the highest expenses
monthly_dominant_categories = (
    expenses_2024.groupby(['Month', 'Category name'])['Clean_Amount']
    .sum()
    .reset_index()
    .sort_values(['Month', 'Clean_Amount'], ascending=[True, False])
)

# Keep only the dominant category for each month
top_categories_per_month = monthly_dominant_categories.groupby('Month').first().reset_index()

# Create a dictionary with the frequency of each category appearing as "dominant"
dominant_counts = top_categories_per_month['Category name'].value_counts()

# Pie chart showing how often each category was "dominant" in 2024 months
plt.figure(figsize=(8, 8))
plt.pie(dominant_counts.values, labels=dominant_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Monthly Category Dominance Frequency (2024)')
plt.tight_layout()
plt.show()

# Group all 2024 expenses by category and sum them
category_totals_2024 = expenses_2024.groupby('Category name')['Clean_Amount'].sum().sort_values(ascending=False)

# Create bar chart with total expenses per category
plt.figure(figsize=(12, 7))
bars = plt.bar(category_totals_2024.index, category_totals_2024.values)

plt.title('Total Expenses by Category (2024)')
plt.xlabel('Category')
plt.ylabel('Total Expenses (€)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')

# Add values on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

df_tableau = df_clean[['Date', 'Type', 'Category name', 'Clean_Amount', 'Month', 'Weekday', 'Year']]
output_path = "C:\\Users\\nioan\Downloads\\Expense_Tracker_Cleaned_2024.csv"
df_tableau.to_csv(output_path, index=False)

output_path