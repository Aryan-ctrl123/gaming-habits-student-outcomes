# analysis.py
# Independent research on gaming habits and student outcomes
# Author: Aryan

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Load dataset
data = pd.read_csv("data/data.csv")


# 1. Gender and Gaming Time

gender_counts = data['Gender'].value_counts()
gender_avg_time = data.groupby('Gender')['The average time you spend playing games'].mean()
gender_median_time = data.groupby('Gender')['The average time you spend playing games'].median()

# T-test: Male vs Female gaming time
male_time = data[data['Gender'] == 'Male']['The average time you spend playing games']
female_time = data[data['Gender'] == 'Female']['The average time you spend playing games']
t_stat, p_val = stats.ttest_ind(male_time, female_time, equal_var=False)

print("Gender Counts:\n", gender_counts)
print("Average Gaming Time by Gender:\n", gender_avg_time)
print("T-test result: t =", t_stat, "p =", p_val)


# 2. Gaming Time vs Social Interaction
gametime_social = data.groupby('The average time you spend playing games')['How much time do you spend with family and friend'].mean().reset_index()
sns.barplot(x='The average time you spend playing games', y='How much time do you spend with family and friend', data=gametime_social)
plt.title("Gaming Time vs Social Interaction")
plt.show()

# Correlation analysis
x = data['The average time you spend playing games']
y = data['How much time do you spend with family and friend']
r, p = stats.pearsonr(x, y)
rho, p_s = stats.spearmanr(x, y)
print(f"Pearson r = {r:.3f}, p = {p:.3f}")
print(f"Spearman rho = {rho:.3f}, p_s = {p_s:.3f}")

sns.regplot(x=x, y=y, data=data)
plt.title("Regression: Gaming vs Social Interaction")
plt.show()


# 3. Sleep Schedule Analysis

print("Average Sleep Hour:", data['When you go to sleep'].mean())
print("Median Sleep Hour:", data['When you go to sleep'].median())
print("Sleep Hour Distribution:\n", data['When you go to sleep'].value_counts())

sns.histplot(data["When you go to sleep"], bins=24)
plt.title("Distribution of Sleep Times")
plt.xlabel("Hour of Day (24h format)")
plt.ylabel("Number of Students")
plt.xticks(range(0, 24))
plt.show()


# 4. Gaming Hours vs CGPPA
avg_cgpa = {
    0: 3.225, 1: 3.332, 2: 3.169, 3: 3.129,
    4: 3.163, 5: 3.071, 6: 3.064, 7: 2.860, 8: 2.665
}
counts = {
    0: 4, 1: 49, 2: 214, 3: 198,
    4: 168, 5: 152, 6: 200, 7: 2, 8: 2
}

cgpa_graph = pd.DataFrame({
    "GamingHours": list(avg_cgpa.keys()),
    "AvgCGPA": list(avg_cgpa.values()),
    "Count": [counts[h] for h in avg_cgpa.keys()]
})

fig, ax1 = plt.subplots(figsize=(8, 5))
sns.lineplot(data=cgpa_graph, x="GamingHours", y="AvgCGPA", marker="o", ax=ax1, color="blue")
ax1.set_ylabel("Average CGPA", color="blue")
ax2 = ax1.twinx()
sns.barplot(data=cgpa_graph, x="GamingHours", y="Count", alpha=0.4, ax=ax2, color="orange")
ax2.set_ylabel("Number of Students", color="orange")
plt.title("Average CGPA vs Gaming Hours")
plt.show()


# 5. Starting Age vs Gaming & HSC GPA

data['At what age you had started playing games'] = data['At what age you had started playing games'].astype(str).str.strip().astype(int)
valid_group = data['At what age you had started playing games'].value_counts()[lambda x: x >= 5].index

hsc_results = {
    12: 4.613636, 14: 4.813000, 15: 4.482222, 16: 4.065000,
    17: 4.223684, 18: 4.109111, 19: 4.230696, 20: 4.177965,
    21: 4.030057, 22: 4.013409, 23: 4.202326, 24: 4.240800
}
gaming_hours = {
    12: 3.090909, 14: 2.900000, 15: 2.222222, 16: 3.409091,
    17: 3.236842, 18: 3.766667, 19: 3.924051, 20: 3.901163,
    21: 3.764368, 22: 3.602273, 23: 4.302326, 24: 4.260000
}

summary = pd.DataFrame({
    "StartingAge": list(hsc_results.keys()),
    "AvgHSCGPA": list(hsc_results.values()),
    "AvgGamingHours": [gaming_hours[age] for age in hsc_results.keys()]
})

fg, axx1 = plt.subplots(figsize=(8, 5))
sns.lineplot(data=summary, x="StartingAge", y="AvgGamingHours", marker="o", ax=axx1, color="blue")
axx2 = axx1.twinx()
sns.lineplot(data=summary, x="StartingAge", y="AvgHSCGPA", marker="s", ax=axx2, color="green")
plt.title("Starting Age vs Gaming Hours and HSC GPA")
plt.show()


# 6. Gaming for Stress Relief & Fatigue

stress_relief_gametime = data.groupby('Do you play games for stress relief')['The average time you spend playing games'].mean()
fatigue_gametime = data.groupby('Do you feel Fatigue')['The average time you spend playing games'].mean()
print("Stress Relief Gaming Time:\n", stress_relief_gametime)
print("Fatigue Gaming Time:\n", fatigue_gametime)


# 7. Game Type vs Playtime

popular_games = data['Which type of game  addicts more'].value_counts()
time_games = data.groupby('Which type of game  addicts more')['The average time you spend playing games'].mean()
print("Popular Game Types:\n", popular_games)
print("Average Time by Game Type:\n", time_games)


# 8. Emotional Impact of Not Playing

feeling_graph = pd.DataFrame({
    "Feeling": ["negative", "positive", "neutral"],
    "Count": [723, 259, 7],
    "AvgGamingHours": [3.845090, 3.606178, 2.714286]
})

fgg, bx1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=feeling_graph, x="Feeling", y="Count", ax=bx1, color="skyblue", alpha=0.7)
bx2 = bx1.twinx()
sns.lineplot(data=feeling_graph, x="Feeling", y="AvgGamingHours", marker="o", ax=bx2, color="red", linewidth=2)
plt.title("Feelings When Unable to Play Games vs Gaming Hours")
plt.show()




