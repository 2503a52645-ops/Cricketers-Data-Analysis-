import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. LOAD ----------
df = pd.read_excel("cleaned_odi_batting.xlsx")
print("Shape:", df.shape)
print("\n--- Summary statistics ---")
print(df.describe().round(2))

# ---------- 2. TOP 10 RUN SCORERS ----------
top_runs = df.nlargest(10, "Runs")[["Player_Name", "Country", "Matches", "Runs", "Average", "Strike_Rate"]]
print("\n--- Top 10 run scorers ---")
print(top_runs.to_string(index=False))

# ---------- 3. COUNTRY-WISE ANALYSIS ----------
country = df.groupby("Country").agg(
    Players=("Player_Name", "count"),
    Total_Runs=("Runs", "sum"),
    Avg_Average=("Average", "mean"),
    Avg_Strike_Rate=("Strike_Rate", "mean")
).round(2).sort_values("Total_Runs", ascending=False)
print("\n--- Country-wise analysis ---")
print(country)

# ---------- 4. BEST PLAYERS BY MEASURE ----------
veterans = df[df.Matches >= 100]

print("\n--- Most sixes ---")
print(df.nlargest(5, "Sixes")[["Player_Name", "Sixes"]].to_string(index=False))

print("\n--- Best average (min 100 matches) ---")
print(veterans.nlargest(5, "Average")[["Player_Name", "Average"]].to_string(index=False))

print("\n--- Highest strike rate (min 100 matches) ---")
print(veterans.nlargest(5, "Strike_Rate")[["Player_Name", "Strike_Rate"]].to_string(index=False))

# ---------- 5. NEW MEASURES ----------
df["Boundary_Pct"] = ((df.Fours * 4 + df.Sixes * 6) / df.Runs * 100).round(1)
df["Century_Rate"] = (df.Hundreds / df.Innings * 100).round(1)

print("\n--- Highest % of runs from boundaries ---")
print(df.nlargest(5, "Boundary_Pct")[["Player_Name", "Boundary_Pct"]].to_string(index=False))

# ---------- 6. CORRELATION ----------
print("\n--- Correlation ---")
print(df[["Runs", "Average", "Strike_Rate", "Matches", "Hundreds", "Sixes"]].corr().round(2))

# ---------- 7. CHARTS ----------
fig, ax = plt.subplots(2, 2, figsize=(16, 10))

t = df.nlargest(10, "Runs")
ax[0, 0].barh(t.Player_Name, t.Runs)
ax[0, 0].invert_yaxis()
ax[0, 0].set_title("Top 10 Run Scorers")

c = df.groupby("Country")["Runs"].sum().sort_values()
ax[0, 1].barh(c.index, c.values)
ax[0, 1].set_title("Total Runs by Country")

ax[1, 0].scatter(df.Average, df.Strike_Rate)
ax[1, 0].set_xlabel("Average")
ax[1, 0].set_ylabel("Strike Rate")
ax[1, 0].set_title("Average vs Strike Rate")

ax[1, 1].hist(df.Average, bins=15)
ax[1, 1].set_xlabel("Batting Average")
ax[1, 1].set_title("Distribution of Batting Average")

plt.tight_layout()
plt.savefig("charts.png")
plt.show()

# ---------- 8. SAVE RESULTS ----------
country.to_excel("country_analysis.xlsx")
top_runs.to_excel("top_10_run_scorers.xlsx", index=False)
print("\nDone! Files saved: charts.png, country_analysis.xlsx, top_10_run_scorers.xlsx")