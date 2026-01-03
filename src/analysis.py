
import pandas as pd 
import seaborn as sns
from matplotlib import pyplot as plt
import pandasgui as pdg
from scipy import stats

data = pd.read_csv('research\data.csv')
#Is there more male or female gamers?
Count_of_gender = data['Gender'].value_counts()
Gender_avg_time = data.groupby('Gender')['The average time you spend playing games'].mean()

Gender_median = data.groupby('Gender')['The average time you spend playing games'].median()
male_rows = data[data['Gender']=='Male']['The average time you spend playing games']
female_rows = data[data['Gender']=='Female']['The average time you spend playing games']
t_stat, p_val = stats.ttest_ind(male_rows,female_rows,equal_var = False)


# does longer hours of game time effect the social interaction of an individual
gametime_social = data.groupby('The average time you spend playing games')['How much time do you spend with family and friend'].mean().reset_index()
# print(gametime_social)
# sns.barplot(x = 'The average time you spend playing games',y ='How much time do you spend with family and friend',data = gametime_social)
x = data['The average time you spend playing games']
y = data['How much time do you spend with family and friend']
r , p = stats.pearsonr(x, y)
rho, p_s = stats.spearmanr(x,y)
# print('r =',r,'p = ',p )
# print('rho=',rho,'p_s=',p_s)
# scatter_plot = sns.regplot(
#     x="The average time you spend playing games", 
#     y="How much time do you spend with family and friend", 
#     data=data
# )

# plt.title("Regression Line: Gaming vs Social Interaction")
# plt.show()

# Does games affect their sleep schedule?
sleep_hour = data['When you go to sleep'].mean()
# print(sleep_hour)
sleep_hrs = data['When you go to sleep'].value_counts()
# print(sleep_hrs)
# print(data['When you go to sleep'].median())
morning_class = data.groupby('When you go to sleep')['Do you attend your morning class regularly'].value_counts()
# print(morning_class)
# sns.histplot(data["When you go to sleep"], bins=24, kde=False)
# plt.title("Distribution of Sleep Times")
# plt.xlabel("Hour of Day (24h format)")
# plt.ylabel("Number of Students")
# plt.xticks(range(0,24))  # show all hours on x-axis
# plt.show()

# Does playing longer hours of games affect their CGPA 
avg_cgpa = data.groupby('The average time you spend playing games')['Your  current CGPA'].mean()
highest_cgpa= data.groupby('The average time you spend playing games')['Your  current CGPA'].max()
# print(avg_cgpa)
# print(highest_cgpa)
# print(data['The average time you spend playing games'].value_counts())

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

fig, ax1 = plt.subplots(figsize=(8,5))

sns.lineplot(data=cgpa_graph, x="GamingHours", y="AvgCGPA", marker="o", ax=ax1, color="blue")
ax1.set_ylabel("Average CGPA", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()
sns.barplot(data=cgpa_graph, x="GamingHours", y="Count", alpha=0.4, ax=ax2, color="orange")
ax2.set_ylabel("Number of Students", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")

plt.title("Average CGPA vs Gaming Hours with Student Counts")
# plt.show()

# Do people who play games from a very young age have the tendency to play more? and what was their HSC results 
data['At what age you had started playing games'] = data['At what age you had started playing games'].astype(str).str.strip().astype(int)
counts = data['At what age you had started playing games'].value_counts() 
valid_group = counts[counts>=5].index
tendency = data[data['At what age you had started playing games'].isin(valid_group)] \
    .groupby('At what age you had started playing games')['The average time you spend playing games'].mean()
# print(tendency)
hsc_result= data[data['At what age you had started playing games'].isin(valid_group)] \
    .groupby('At what age you had started playing games')['Your Higher Secondary School(H. SC) or A level or equivalent result'].mean()
# print(data['At what age you had started playing games'].value_counts())
# print(hsc_result)
# print(hsc_result.max())




hsc_results = {
    12: 4.613636,
    14: 4.813000,
    15: 4.482222,
    16: 4.065000,
    17: 4.223684,
    18: 4.109111,
    19: 4.230696,
    20: 4.177965,
    21: 4.030057,
    22: 4.013409,
    23: 4.202326,
    24: 4.240800
}

gaming_hours = {
    12: 3.090909,
    14: 2.900000,
    15: 2.222222,
    16: 3.409091,
    17: 3.236842,
    18: 3.766667,
    19: 3.924051,
    20: 3.901163,
    21: 3.764368,
    22: 3.602273,
    23: 4.302326,
    24: 4.260000
}


summary = pd.DataFrame({
    "StartingAge": list(hsc_results.keys()),
    "AvgHSCGPA": list(hsc_results.values()),
    "AvgGamingHours": [gaming_hours[age] for age in hsc_results.keys()]
})


fg, axx1 = plt.subplots(figsize = (8,5))
sns.lineplot(data=summary, x="StartingAge", y="AvgGamingHours", marker="o", ax=axx1, color="blue", label="Avg Gaming Hours")
axx1.set_ylabel("Average Gaming Hours", color="blue")
axx1.tick_params(axis="y", labelcolor="blue")

axx2 = axx1.twinx()
sns.lineplot(data=summary, x="StartingAge", y="AvgHSCGPA", marker="s", ax=axx2, color="green", label="Avg HSC GPA")
axx2.set_ylabel("Average HSC GPA", color="green")
axx2.tick_params(axis="y", labelcolor="green")

plt.title("Starting Age vs Gaming Hours and HSC GPA")
# plt.show()


# does games play a mentally soothing effect on peoples mind?
stress_relief = data['Do you play games for stress relief'].value_counts()
fatigue = data['Do you feel Fatigue'].value_counts()
stress_relief_gametime = data.groupby('Do you play games for stress relief')['The average time you spend playing games'].mean()
fatigue_gametime = data.groupby('Do you feel Fatigue')['The average time you spend playing games'].mean()
# print(stress_relief_gametime)
# print(fatigue_gametime)

# does certain games have higher playtime than others?

popular_games = data['Which type of game  addicts more'].value_counts()
time_games= data.groupby('Which type of game  addicts more')['The average time you spend playing games'].mean()
# print(popular_games)
# print(time_games)

# Has games become a daily part of their lives and do people feel more irritated when not being able to play it?

feeling = data['How do you feel when you can not play game in whole day'].value_counts()
time_feeling = data.groupby('How do you feel when you can not play game in whole day')['The average time you spend playing games'].mean()
# print(feeling)
# print(time_feeling)


counts = {
    "negative": 723,
    "positive": 259,
    "neutral": 7
}

avg_hours = {
    "negative": 3.845090,
    "positive": 3.606178,
    "neutral": 2.714286
}
feeling_graph= pd.DataFrame({
    "Feeling": list(counts.keys()),
    "Count": list(counts.values()),
    "AvgGamingHours": [avg_hours[f] for f in counts.keys()]
})
fgg, bx1 = plt.subplots(figsize = (8,5))
sns.barplot(data=feeling_graph, x="Feeling", y="Count", ax=bx1, color="skyblue", alpha=0.7)
bx1.set_ylabel("Number of Students", color="blue")
bx1.tick_params(axis="y", labelcolor="blue")

bx2 = bx1.twinx()
sns.lineplot(data=feeling_graph, x="Feeling", y="AvgGamingHours", marker="o", ax=bx2, color="red", linewidth=2)
bx2.set_ylabel("Average Gaming Hours", color="red")
bx2.tick_params(axis="y", labelcolor="red")

plt.title("Feelings When Unable to Play Games vs Gaming Hours")
plt.show()




