import pandas as pd
import numpy as np

def compute_final_grade(df):
    return df["grade"].dot(df["LP"]) / df["LP"].sum()

def hypothetical_master_thesis_grades():
    return np.array([1.0, 1.3, 1.7, 2.0])

total_budget = 120
thesis_budget = 30
except_thesis_budget = total_budget - thesis_budget

df = pd.read_csv("master_notes.csv")
assert df["LP"].sum() == except_thesis_budget, "Expected {} LPs, but found {}".format(except_thesis_budget, df["LP"].sum())

free_wahl_budget_range = [12, 30]

snapshots_of_different_combinations = []
df_graded, df_ungraded = df[df["grade"] != "*"], df[df["grade"] == "*"]
df_graded["grade"] = df_graded["grade"].astype(float)
df_graded_sorted = df_graded.sort_values(["grade", "LP"], ascending=[True, False])

free_wahl_budget = df_ungraded["LP"].sum()
while free_wahl_budget <= free_wahl_budget_range[1]:
    currently_worst_row = df_graded_sorted.iloc[-1]
    df_graded_sorted = df_graded_sorted.iloc[:-1]
    free_wahl_budget += currently_worst_row["LP"]
    if free_wahl_budget_range[0] <= free_wahl_budget <= free_wahl_budget_range[1]:
        snapshots_of_different_combinations.append((free_wahl_budget, compute_final_grade(df_graded_sorted.copy())))

print("-" * 80)
for free_wahl_budget, final_grade in snapshots_of_different_combinations:
    wahlpflict_budget = except_thesis_budget - free_wahl_budget
    print("My current grade is {:<.1f} if I choose to free up {} LPs from my grades.".format(final_grade, free_wahl_budget))
    for hypothetical_grade in hypothetical_master_thesis_grades():
        hypothetical_final_grade = (final_grade * wahlpflict_budget + hypothetical_grade * thesis_budget) / (wahlpflict_budget + thesis_budget)
        print(f"- If I get {hypothetical_grade:<.1f} from my master thesis, my final grade will be {hypothetical_final_grade:<.1f})")