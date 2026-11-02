import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("cleaned_odi_batting.xlsx")
plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3,
                     "axes.spines.top": False, "axes.spines.right": False})

# 1. Top 10 run scorers
t = df.nlargest(10, "Runs")
plt.figure(figsize=(10, 6))
plt.barh(t.Player_Name, t.Runs, color="#1f77b4")
plt.gca().invert_yaxis()
for i, v in enumerate(t.Runs):
    plt.text(v + 100, i, f"{v:,}", va="center", fontsize=9)
plt.title("Top 10 Run Scorers in ODI Cricket")
plt.xlabel("Runs")
plt.tight_layout()
plt.savefig("viz1_top_run_scorers.png", dpi=150)
plt.show()

# 2. Total runs by country
c = df.groupby("Country")["Runs"].sum().sort_values()
plt.figure(figsize=(10, 6))
plt.barh(c.index, c.values, color="#2ca02c")
plt.title("Total Runs by Country (Top Batsmen in Dataset)")
plt.xlabel("Total Runs")
plt.tight_layout()
plt.savefig("viz2_runs_by_country.png", dpi=150)
plt.show()

# 3. Share of players by country (pie, top 6 + Others)
p = df["Country"].value_counts()
p = pd.concat([p.head(6), pd.Series({"Others": p.iloc[6:].sum()})])
plt.figure(figsize=(8, 8))
plt.pie(p.values, labels=p.index, autopct="%1.1f%%", startangle=90)
plt.title("Share of Players by Country")
plt.tight_layout()
plt.savefig("viz3_players_by_country.png", dpi=150)
plt.show()

# 4. Distribution of batting average
plt.figure(figsize=(10, 6))
plt.hist(df.Average, bins=15, color="#ff7f0e", edgecolor="white")
plt.axvline(df.Average.mean(), color="red", linestyle="--",
            label=f"Mean = {df.Average.mean():.1f}")
plt.title("Distribution of Batting Average")
plt.xlabel("Batting Average")
plt.ylabel("Number of Players")
plt.legend()
plt.tight_layout()
plt.savefig("viz4_average_distribution.png", dpi=150)
plt.show()

# 5. Average vs Strike Rate (top players labelled)
plt.figure(figsize=(10, 7))
plt.scatter(df.Average, df.Strike_Rate, s=df.Runs / 100, alpha=0.6, color="#9467bd")
for _, r in df.nlargest(6, "Runs").iterrows():
    plt.annotate(r.Player_Name, (r.Average, r.Strike_Rate),
                 fontsize=8, xytext=(4, 4), textcoords="offset points")
plt.title("Batting Average vs Strike Rate (bubble size = total runs)")
plt.xlabel("Average")
plt.ylabel("Strike Rate")
plt.tight_layout()
plt.savefig("viz5_average_vs_strike_rate.png", dpi=150)
plt.show()

# 6. Strike rate by country (boxplot, countries with 3+ players)
valid = df["Country"].value_counts()
valid = valid[valid >= 3].index
data = [df[df.Country == k].Strike_Rate for k in valid]
plt.figure(figsize=(11, 6))
plt.boxplot(data, tick_labels=valid)
plt.title("Strike Rate by Country (countries with 3+ players)")
plt.ylabel("Strike Rate")
plt.tight_layout()
plt.savefig("viz6_strike_rate_by_country.png", dpi=150)
plt.show()

# 7. Top 10 six hitters
s = df.nlargest(10, "Sixes")
plt.figure(figsize=(10, 6))
plt.bar(s.Player_Name, s.Sixes, color="#d62728")
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Six Hitters")
plt.ylabel("Sixes")
plt.tight_layout()
plt.savefig("viz7_top_sixes.png", dpi=150)
plt.show()

# 8. Hundreds vs Fifties (top 10 by hundreds)
h = df.nlargest(10, "Hundreds")
x = np.arange(len(h))
plt.figure(figsize=(11, 6))
plt.bar(x - 0.2, h.Hundreds, 0.4, label="Hundreds")
plt.bar(x + 0.2, h.Fifties, 0.4, label="Fifties")
plt.xticks(x, h.Player_Name, rotation=45, ha="right")
plt.title("Hundreds and Fifties: Top 10 by Centuries")
plt.legend()
plt.tight_layout()
plt.savefig("viz8_hundreds_fifties.png", dpi=150)
plt.show()

# 9. Runs vs Matches with trend line
plt.figure(figsize=(10, 6))
plt.scatter(df.Matches, df.Runs, alpha=0.6, color="#17becf")
m, b = np.polyfit(df.Matches, df.Runs, 1)
xs = np.linspace(df.Matches.min(), df.Matches.max(), 100)
plt.plot(xs, m * xs + b, color="red", label="Trend line")
plt.title("Runs vs Matches Played")
plt.xlabel("Matches")
plt.ylabel("Runs")
plt.legend()
plt.tight_layout()
plt.savefig("viz9_runs_vs_matches.png", dpi=150)
plt.show()

# 10. Correlation heatmap
cols = ["Runs", "Average", "Strike_Rate", "Matches", "Hundreds", "Fifties", "Sixes"]
corr = df[cols].corr()
plt.figure(figsize=(8, 7))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Correlation")
plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
plt.yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
plt.title("Correlation Heatmap")
plt.grid(False)
plt.tight_layout()
plt.savefig("viz10_correlation_heatmap.png", dpi=150)
plt.show()

print("Done! 10 charts saved as viz1_... to viz10_... PNG files.")