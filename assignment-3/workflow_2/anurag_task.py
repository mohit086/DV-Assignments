import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score
import plotly.express as px
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


# Read the data into a dataframe
df = pd.read_csv('../data/base.csv')
os.makedirs('images',exist_ok=True)

# ---------------------------------------------------------------------------------------------------------------


bins = np.arange(300, 851, 50)
labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]

df['CreditScoreBin'] = pd.cut(df['CreditScore'], bins=bins, labels=labels, right=False)

score_counts = df['CreditScoreBin'].value_counts().sort_index()

colors = ['red' if int(label.split('-')[0]) < 500 else 
          'gold' if int(label.split('-')[0]) < 700 else 
          'green' for label in labels]
plt.figure(figsize=(10, 6))
plt.bar(score_counts.index, score_counts.values, color=colors)
plt.title('Credit Score Distribution')
plt.xlabel('Credit Score Range')
plt.ylabel('Number of People')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("../images/fig12.png")
#plt.show()
plt.close()
# ---------------------------------------------------------------------------------------------------------------


plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='CreditScore', hue='LoanApproved', common_norm=False)
plt.title('Distribution of Credit Scores by Loan Approval Status')
plt.xlabel('Credit Score')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig('../images/fig13.png')
#plt.show()
plt.close()
# ---------------------------------------------------------------------------------------------------------------



plt.figure(figsize=(10, 6))
approved = df[df['LoanApproved'] == 1]
rejected = df[df['LoanApproved'] == 0]

plt.scatter(approved['CreditScore'], approved['DebtToIncomeRatio'], 
           alpha=0.6, label='Approved', c='green')
plt.scatter(rejected['CreditScore'], rejected['DebtToIncomeRatio'], 
           alpha=0.6, label='Rejected', c='red')
plt.xlabel('Credit Score')
plt.ylabel('Debt-to-Income Ratio')
plt.title('Credit Score vs Debt-to-Income Ratio')
plt.legend()
plt.tight_layout()
plt.savefig('../images/fig14.png')
#plt.show()
plt.close()
# ---------------------------------------------------------------------------------------------------------------



tenure_inquiries = df.groupby('JobTenure')['NumberOfCreditInquiries'].sum().reset_index()


plt.figure(figsize=(12, 6))
plt.plot(tenure_inquiries['JobTenure'], 
         tenure_inquiries['NumberOfCreditInquiries'], 
         marker='o',  
         linewidth=2, 
         markersize=8,
         color='#2ecc71')  


plt.title('Total Number of Credit Inquiries by Job Tenure', fontsize=12, pad=15)
plt.xlabel('Job Tenure (Years)', fontsize=10)
plt.ylabel('Total Number of Credit Inquiries', fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7)

plt.xticks(rotation=45)


plt.tight_layout()
plt.savefig('../images/fig15.png')
#plt.show()
plt.close()
# ---------------------------------------------------------------------------------------------------------------




bins = [18, 25, 35, 45, 55, 66]
labels = ['18-24', '25-34', '35-44', '45-54', '55-65']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)


def categorize_credit_score(score):
    if score < 500:
        return 'Low'
    elif score < 700:
        return 'Medium'
    else:
        return 'High'

df['CreditScoreCategory'] = df['CreditScore'].apply(categorize_credit_score)


grouped_data = df.groupby(['AgeGroup', 'CreditScoreCategory'])['NumberOfCreditInquiries'].sum().unstack()

colors = {'Low': 'red', 'Medium': 'gold', 'High': 'green'}

grouped_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=[colors[col] for col in grouped_data.columns])

plt.title('Number of Credit Inquiries Across Age Groups and Credit Score Categories')
plt.xlabel('Age Group')
plt.ylabel('Number of Credit Inquiries')
plt.xticks(rotation=45)
plt.legend(title='Credit Score Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('../images/fig16.png')

#plt.show()
plt.close()

# ---------------------------------------------------------------------------------------------------------------
features = ['NumberOfOpenCreditLines', 'LoanApproved', 'NumberOfCreditInquiries', 'DebtToIncomeRatio']
df_pcp = df[features].copy()
def categorize_credit_score(score):
    if score < 500:
        return 'Low'
    elif score < 700:
        return 'Medium'
    else:
        return 'High'

df_pcp['CreditScoreCategory'] = df['CreditScore'].apply(categorize_credit_score)
color_map = {'Low': 0, 'Medium': 0.5, 'High': 1}
df_pcp['CreditScoreNumeric'] = df_pcp['CreditScoreCategory'].map(color_map)
fig = px.parallel_coordinates(
    df_pcp,
    color='CreditScoreNumeric',
    dimensions=features,
    color_continuous_scale=[
        [0, 'red'],
        [0.5, 'gold'],
        [1, 'lightgreen']
    ],
    labels={
        'NumberOfOpenCreditLines': 'Open Credit Lines',
        'LoanApproved': 'Loan Approved',
        'NumberOfCreditInquiries': 'Credit Inquiries',
        'DebtToIncomeRatio': 'Debt-to-Income Ratio',
    },
    range_color=[0, 1]  
)
fig.update_traces(dimensions=[
    dict(range=[df_pcp['NumberOfOpenCreditLines'].min(), df_pcp['NumberOfOpenCreditLines'].max()], 
         values=(df_pcp['NumberOfOpenCreditLines']),
         label='Open Credit Lines'),
    dict(range=[0, 1], 
         values=df_pcp['LoanApproved'],
         label='Loan Approved'),
    dict(range=[df_pcp['NumberOfCreditInquiries'].min(), df_pcp['NumberOfCreditInquiries'].max()], 
         values=(df_pcp['NumberOfCreditInquiries']),
         label='Credit Inquiries'),
    dict(range=[0, 1], 
         values=df_pcp['DebtToIncomeRatio'],
         label='Debt-to-Income Ratio'),
])
fig.write_image("../images/fig17.png")

# fig.show()





# ---------------------------------------------------------------------------------------------------------------

def classify_credit_score(score):
    if score < 500:
        return "Low"
    elif score < 700:
        return "Medium"
    else:
        return "High"

df['CreditScoreCategory'] = df['CreditScore'].apply(classify_credit_score)
features = ['Age', 'JobTenure', 'NumberOfCreditInquiries', 'LoanApproved', 'DebtToIncomeRatio']
target = 'CreditScoreCategory'
X = df[features]
y = df[target]
# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=347)
naive_bayes_initial = GaussianNB()
naive_bayes_initial.fit(X_train, y_train)
y_pred_initial = naive_bayes_initial.predict(X_test)
# Evaluate Initial Model
print("Initial Naive Bayes Classification Report:")
print(classification_report(y_test, y_pred_initial))
accuracy_initial = accuracy_score(y_test, y_pred_initial)
print(f"Initial Naive Bayes Accuracy: {accuracy_initial}")



# ---------------------------------------------------------------------------------------------------------------


# Feature Engineering
# Creating a new feature based on domain logic
df['CreditUtilizationScore'] = (
    df['Age'] * -0.2 + 
    df['DebtToIncomeRatio'] * -0.35 + 
    df['LoanApproved'] * 0.25 + 
    df['NumberOfCreditInquiries'] * -0.35
)



# ---------------------------------------------------------------------------------------------------------------
custom_palette = {'Low': 'red', 'Medium': 'gold', 'High': 'green'}
sns.pairplot(df, vars=['CreditUtilizationScore', 'Age', 'DebtToIncomeRatio', 'LoanApproved', 'NumberOfCreditInquiries'], 
             hue='CreditScoreCategory', palette=custom_palette, diag_kind='kde')
plt.suptitle('Pairplot of CreditUtilizationScore and Related Features', y=1.02)
plt.savefig('../images/fig19.png')
#plt.show()
plt.close()

# ---------------------------------------------------------------------------------------------------------------


avg_scores = df.groupby('LoanApproved')['CreditUtilizationScore'].mean().reset_index()

fig, ax = plt.subplots()

# Barplot
sns.barplot(
    data=avg_scores, 
    x='LoanApproved', 
    y='CreditUtilizationScore', 
    hue='LoanApproved', 
    dodge=False, 
    palette='RdBu', 
    ax=ax,  
    legend=False
)


ax.set_title('Average CreditUtilizationScore by Loan Approval')
ax.set_xlabel('Loan Approved (0 = No, 1 = Yes)')
ax.set_ylabel('Average Credit Utilization Score')

# Save the figure
plt.tight_layout()
fig.savefig('../images/fig20.png')  
# plt.show()  
plt.close(fig)  


# ---------------------------------------------------------------------------------------------------------------

fig, ax = plt.subplots()

# Violin plot
sns.violinplot(
    data=df, 
    x='NumberOfCreditInquiries', 
    y='CreditUtilizationScore', 
    palette='muted', 
    cut=0, 
    ax=ax  
)


ax.set_title('CreditUtilizationScore by Number of Credit Inquiries')
ax.set_xlabel('Number of Credit Inquiries')
ax.set_ylabel('Credit Utilization Score')


plt.tight_layout()
fig.savefig('../images/fig21.png')  
# plt.show()  
plt.close(fig)  


# ---------------------------------------------------------------------------------------------------------------

sns.lineplot(data=df, x='JobTenure', y='CreditUtilizationScore', marker='o', color='blue', label='Credit Utilization Score')


slope, intercept, r_value, p_value, std_err = stats.linregress(df['JobTenure'], df['CreditUtilizationScore'])
plt.plot(df['JobTenure'], slope * df['JobTenure'] + intercept, color='red', label='Trend Line')


plt.title('CreditUtilizationScore vs Job Tenure with Trend Line')
plt.xlabel('Job Tenure (Years)')
plt.ylabel('Credit Utilization Score')

plt.legend()
plt.savefig("../images/fig22.png")

#plt.show()
plt.close()


# ---------------------------------------------------------------------------------------------------------------


# Use all original features plus the engineered feature
features_refined = features + ['CreditUtilizationScore']
X_refined = df[features_refined]

X_train_refined, X_test_refined, y_train_refined, y_test_refined = train_test_split(
    X_refined, y, test_size=0.2, random_state=808
)

naive_bayes_refined = GaussianNB()
naive_bayes_refined.fit(X_train_refined, y_train_refined)
y_pred_refined = naive_bayes_refined.predict(X_test_refined)

# Evaluate Refined Model
print("Refined Naive Bayes Classification Report:")
print(classification_report(y_test_refined, y_pred_refined))
accuracy_refined = accuracy_score(y_test_refined, y_pred_refined)

print(f"Initial Naive Bayes Accuracy: {accuracy_initial}")
print(f"Refined Naive Bayes Accuracy: {accuracy_refined}")

# ---------------------------------------------------------------------------------------------------------------




categories = ['Low', 'Medium', 'High', 'Overall']
model_1_f1_scores = [0.78, 0.60, 0.26, 0.682]  
model_2_f1_scores = [0.83, 0.64, 0.36, 0.748]  

x = np.arange(len(categories))

bar_width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))

bars_model_1 = ax.bar(x - bar_width/2, model_1_f1_scores, bar_width, label='Model 1', color='darkorange')
bars_model_2 = ax.bar(x + bar_width/2, model_2_f1_scores, bar_width, label='Model 2', color='blue')

for i, bar in enumerate(bars_model_1):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{model_1_f1_scores[i]:.2f}', 
            ha='center', va='bottom', fontsize=10)
for i, bar in enumerate(bars_model_2):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{model_2_f1_scores[i]:.2f}', 
            ha='center', va='bottom', fontsize=10)

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_xlabel('Credit Score Categories')
ax.set_ylabel('F1 Score')
ax.set_title('F1 Scores for Different Credit Score Categories (Model 1 vs Model 2)')


ax.legend()

plt.tight_layout()
plt.savefig('../images/fig23.png')
#plt.show()
plt.close()
# ---------------------------------------------------------------------------------------------------------------

