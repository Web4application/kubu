import pandas as pd
import matplotlib.pyplot as plt

# Load and clean the CSV log file
file_path = "chat_gpt-web4-l7k6oqluq-web4era_vercel_app_logs.csv"
logs_df = pd.read_csv(file_path, on_bad_lines='skip')
logs_df = logs_df.dropna(subset=["size"])

# Summary statistics
summary_stats = logs_df["size"].describe()
print("=== File Size Summary ===")
print(summary_stats)

# Top 10 largest files
top_largest = logs_df.sort_values(by="size", ascending=False).head(10)
print("\n=== Top 10 Largest Files ===")
print(top_largest[["path_name", "size"]])

# Error path analysis
error_paths = logs_df[logs_df["path_name"].isin(["/404", "/500"])]
print("\n=== Error Path Sizes ===")
print(error_paths[["path_name", "size"]])

# Group by file extension
logs_df["extension"] = logs_df["path_name"].str.extract(r'\.([a-zA-Z0-9]+)$')
ext_summary = logs_df.groupby("extension")["size"].sum().sort_values(ascending=False)

# Plotting file size by extension
plt.figure(figsize=(10, 6))
ext_summary.plot(kind='bar', color='teal')
plt.title("Total File Size by Extension")
plt.xlabel("File Extension")
plt.ylabel("Total Size (bytes)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')
plt.savefig("file_size_by_extension.png")
plt.show()
