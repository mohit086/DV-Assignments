import sys
import squarify
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('../data/base.csv')

# -----------------------------------------------------------------------------------------------

utilization_quantiles = df['CreditCardUtilizationRate'].quantile([0.10, 0.30, 0.60, 0.80])
dti_quantiles = df['DebtToIncomeRatio'].quantile([0.10, 0.30, 0.60, 0.80])
df['CreditCardUtilizationCategory'] = pd.cut(df['CreditCardUtilizationRate'],
                                             bins=[-np.inf, utilization_quantiles[0.10], utilization_quantiles[0.30],
                                                   utilization_quantiles[0.60], utilization_quantiles[0.80], np.inf],
                                             labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High'])

df['DebtToIncomeCategory'] = pd.cut(df['DebtToIncomeRatio'],
                                    bins=[-np.inf, dti_quantiles[0.10], dti_quantiles[0.30],
                                          dti_quantiles[0.60], dti_quantiles[0.80], np.inf],
                                    labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High'])
summary = df.groupby(['CreditCardUtilizationCategory', 'DebtToIncomeCategory'], observed=False).size().reset_index(name='Count')
summary['CreditCardUtilizationCategory'] = summary['CreditCardUtilizationCategory'].astype(str)
summary['DebtToIncomeCategory'] = summary['DebtToIncomeCategory'].astype(str)
labels = summary['CreditCardUtilizationCategory'] + ',' + summary['DebtToIncomeCategory'] + '\n' + summary['Count'].astype(str)
sizes = summary['Count']
norm = plt.Normalize(vmin=0, vmax=len(sizes)-1)
cmap = cm.viridis
colors = [cmap(norm(i)) for i in range(len(sizes))]
plt.figure(figsize=(12, 8))
ax = plt.gca()
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, edgecolor='white', linewidth=3)
plt.axis('off')
plt.savefig('../images/fig25.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------

loan_amount_quantiles = df['LoanAmount'].quantile([0.30, 0.70])
df['AgeCategory'] = pd.cut(df['Age'], bins=[-np.inf, 30, 60, np.inf], labels=['Youth', 'Middle Age', 'Senior'])
df['LoanAmountCategory'] = pd.cut(df['LoanAmount'], 
                                  bins=[-np.inf, loan_amount_quantiles[0.30], loan_amount_quantiles[0.70], np.inf], 
                                  labels=['Low', 'Moderate', 'High'])
summary = df.groupby(['AgeCategory', 'LoanAmountCategory'], observed=False).size().reset_index(name='Count')
summary['AgeCategory'] = summary['AgeCategory'].astype(str)
summary['LoanAmountCategory'] = summary['LoanAmountCategory'].astype(str)
labels = summary['AgeCategory'] + ' & ' + summary['LoanAmountCategory'] + '\n' + summary['Count'].astype(str)
sizes = summary['Count']
norm = plt.Normalize(vmin=0, vmax=len(sizes)-1)
cmap = cm.viridis
colors = [cmap(norm(i)) for i in range(len(sizes))]
plt.figure(figsize=(12, 8))
ax = plt.gca()
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, edgecolor='white', linewidth=3)
plt.axis('off')
plt.savefig('../images/fig26.png', bbox_inches='tight')
plt.close()

# ---------------------------------------------------------------------------------------------------------------

denied_loans_df = df[df['LoanApproved'] == 0].copy()
savings_to_income_ratio = denied_loans_df['SavingsAccountBalance'] / denied_loans_df['AnnualIncome']
savings_bins = [0, 0.1, 0.2, 0.3, 0.4, 1.0]
savings_labels = ['0-0.1', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-1']
savings_ratio_category = pd.cut(savings_to_income_ratio, bins=savings_bins, labels=savings_labels, right=False)
savings_ratio_counts = savings_ratio_category.value_counts().sort_index()
credit_bins = [0, 3, 6, 9, 12, np.inf]
credit_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
credit_lines_category = pd.cut(denied_loans_df['NumberOfOpenCreditLines'], bins=credit_bins, labels=credit_labels, right=False)
credit_lines_counts = credit_lines_category.value_counts().sort_index()
liabilities_to_assets_ratio = denied_loans_df['TotalLiabilities'] / denied_loans_df['TotalAssets']
liabilities_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
liabilities_labels = ['0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']
liabilities_ratio_category = pd.cut(liabilities_to_assets_ratio, bins=liabilities_bins, labels=liabilities_labels, right=False)
liabilities_ratio_counts = liabilities_ratio_category.value_counts().sort_index()

plt.figure(figsize=(6, 6))
plt.pie(savings_ratio_counts, labels=savings_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.savefig('../images/fig27.png', bbox_inches='tight')
plt.figure(figsize=(6, 6))
plt.pie(credit_lines_counts, labels=credit_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.savefig('../images/fig28.png', bbox_inches='tight')
plt.figure(figsize=(6, 6))
plt.pie(liabilities_ratio_counts, labels=liabilities_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.savefig('../images/fig29.png', bbox_inches='tight')
plt.close()

# --------------------------------------------------------------------------------------------------------------------

feature_to_label = {  
    'EducationLevel': 'Education',
    'LoanPurpose': 'Purpose',
    'DebtToIncomeCategory': 'Debt-to-Income',
    'AgeCategory': 'Age',
    'LoanApproved': 'Approval Status'
}
source_features = ['EducationLevel', 'LoanPurpose', 'DebtToIncomeCategory', 'AgeCategory']
all_categories = {}
index = 0
for col in source_features + ['LoanApproved']:
    for value in df[col].unique():
        if value not in all_categories:
            all_categories[value] = index
            index += 1

source = []
target = []
value = []
colors = []
color_palette = plt.cm.Pastel2(np.linspace(0, 1, len(all_categories)))
for i in range(len(source_features)):
    col1 = source_features[i]
    col2 = source_features[i + 1] if i + 1 < len(source_features) else 'LoanApproved'
    for group, sub_df in df.groupby([col1, col2], observed=True):
        source.append(all_categories[group[0]])
        target.append(all_categories[group[1]])
        value.append(len(sub_df))
        colors.append(color_palette[all_categories[group[0]]])
flow_colors = [f"rgba({int(c[0] * 255)}, {int(c[1] * 255)}, {int(c[2] * 255)}, 0.8)" for c in colors]
labels = [key for key, val in sorted(all_categories.items(), key=lambda x: x[1])]
x_positions = np.linspace(0.1, 0.9, len(source_features) + 1)
x_positions[-1] += 0.08
x_positions[-2] += 0.05
x_positions[0] -= 0.1
x_positions[1] -= 0.08
annotations = []
for i, feature in enumerate(source_features + ['LoanApproved']):
    annotations.append(
        dict(
            x=x_positions[i], 
            y=1.1,
            text=feature_to_label[feature],
            showarrow=False,
            font=dict(size=14, color="black"),
            align="center"
        )
    )

fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=flow_colors,
    )
))

fig.update_layout(
    paper_bgcolor="white",
    annotations=annotations
)

fig.write_image("../images/fig30.png")

# ------------------------------------------------------------------------------------------------------------

ccur_bins = pd.cut(df['CreditCardUtilizationRate'], bins=10, labels=False)
dti_bins = pd.cut(df['DebtToIncomeRatio'], bins=10, labels=False)
features_binned = np.column_stack([ccur_bins, dti_bins])
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(features_binned)
cluster_labels = {
    0: "High CCUR, Low DTI",
    1: "Low CCUR, High DTI",
    2: "High CCUR, High DTI",
    3: "Low CCUR, Low DTI"
}

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

for cluster in range(4):
    cluster_data = df.iloc[clusters == cluster]
    approval_counts = cluster_data['LoanApproved'].value_counts()
    labels = ['Loan Approved', 'Loan Denied']
    approval_counts = approval_counts.reindex([1, 0], fill_value=0)
    
    axes[cluster].pie(
        approval_counts, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#66b3ff', '#ff6666']
    )
    axes[cluster].text(
        0.5, 
        1.2, 
        cluster_labels[cluster], 
        ha='center', 
        va='center', 
        transform=axes[cluster].transAxes, 
        fontsize=12, 
        fontweight='bold'
    )

plt.tight_layout()
plt.savefig('../images/fig31.png', bbox_inches='tight')

fig, ax_scatter = plt.subplots(figsize=(6, 6))
random_points = df.sample(50, random_state=42)
random_clusters = clusters[random_points.index]

x = random_points['CreditCardUtilizationRate']
y = random_points['DebtToIncomeRatio']
colors = ['#66b3ff', '#ff6666', '#99ff99', '#ffcc99']

for cluster in range(4):
    cluster_points = random_points[random_clusters == cluster]
    ax_scatter.scatter(
        cluster_points['CreditCardUtilizationRate'], 
        cluster_points['DebtToIncomeRatio'], 
        label=f'{cluster_labels[cluster]}', 
        color=colors[cluster], 
        s=20, 
        alpha=1
    )

ax_scatter.set_xlabel("Credit Card Utilization Rate")
ax_scatter.set_ylabel("Debt to Income Ratio")
ax_scatter.legend()
plt.tight_layout()
plt.savefig('../images/fig32.png', bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------------------------------------------------

total_assets_bins = pd.cut(df['TotalAssets'], bins=10, labels=False)
total_liabilities_bins = pd.cut(df['TotalLiabilities'], bins=10, labels=False)
features_binned = np.column_stack([total_assets_bins, total_liabilities_bins])
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(features_binned)
df['Cluster'] = clusters
cluster_labels = {
    0: "Low Assets, Low Liabilities", 
    1: "High Assets, Low Liabilities", 
    2: "Low Assets, High Liabilities", 
    3: "High Assets, High Liabilities"
}
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

for cluster in range(4):
    cluster_data = df[df['Cluster'] == cluster]
    approval_counts = cluster_data['LoanApproved'].value_counts()
    approval_counts = approval_counts.reindex([1, 0], fill_value=0)
    axes[cluster].bar(
        ['Loan Approved', 'Loan Denied'], 
        approval_counts, 
        color=['#66b3ff', '#ff6666']
    )
    axes[cluster].text(
        0.5, 
        max(approval_counts) + 0.5, 
        cluster_labels[cluster], 
        ha='center', 
        va='bottom', 
        fontsize=12,
    )
    axes[cluster].set_ylim(0, max(approval_counts) + 2)
plt.tight_layout()
plt.savefig('../images/fig33.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------------

savings_income_ratio = df['SavingsAccountBalance'] / df['AnnualIncome']
savings_income_ratio_bin = pd.qcut(savings_income_ratio, q=10, labels=False)
features_binned = savings_income_ratio_bin.values.reshape(-1, 1)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(features_binned)
df['Cluster'] = clusters
cluster_labels = {
    0: "Low Savings,\n Low Income",
    1: "High Savings,\n Low Income",
    2: "Low Savings,\n High Income",
    3: "High Savings,\n High Income"
}
fig, ax = plt.subplots(figsize=(10, 6))
approval_counts = df.groupby(['Cluster', 'LoanApproved']).size().unstack(fill_value=0)
approval_counts.plot(kind='bar', stacked=True, color=['#ff6666', '#66b3ff'], ax=ax)
for cluster in range(4):
    ax.text(cluster, approval_counts.iloc[cluster].sum() + 5, cluster_labels[cluster], ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_xlabel('Cluster', fontsize=12)
ax.set_ylabel('Number of Loans', fontsize=12)
ax.legend(['Loan Denied', 'Loan Approved'], title='Loan Status')
plt.tight_layout()
plt.savefig('../images/fig34.png', bbox_inches='tight')
plt.close()


# ----------------------------------------------------------------------------------------------------------------------------

age_bins = pd.cut(df['Age'], bins=[0, 30, 50, 70, 100], labels=['Young', 'Middle-aged', 'Senior', 'Elderly'])
label_encoder = LabelEncoder()
age_bin_encoded = label_encoder.fit_transform(age_bins)
features_binned = np.column_stack([age_bin_encoded, df['LoanAmount']])
kmeans = KMeans(n_clusters=6, random_state=42)
clusters = kmeans.fit_predict(features_binned)
cluster_labels = {
    0: "Young, Low LoanAmount",
    1: "Senior, Low LoanAmount",
    2: "Middle-Aged, Low LoanAmount",
    3: "Young, High LoanAmount",
    4: "Senior, High LoanAmount",
    5: "Middle-Aged, High LoanAmount"
}
fig, ax = plt.subplots(figsize=(16, 10))
approval_counts = df.groupby([clusters, 'LoanApproved']).size().unstack(fill_value=0)
scaled_approval_counts = approval_counts.copy()
scaled_approval_counts[0] = approval_counts[0] * 0.5
scaled_approval_counts.plot(kind='barh', stacked=True, color=['#ff6666', '#66b3ff'], ax=ax, alpha=1)
for cluster in range(6):
    ax.text(scaled_approval_counts.iloc[cluster].sum() + 5, cluster, cluster_labels[cluster], ha='left', va='center', fontsize=12, fontweight='bold')
ax.set_title('Loan Approval Breakdown by Cluster - Age vs LoanAmount', fontsize=16)
ax.set_xlabel('Number of Loans', fontsize=14)
ax.set_ylabel('Cluster', fontsize=14)
ax.legend(['Loan Denied', 'Loan Approved'])
plt.tight_layout()
plt.savefig('../images/fig35.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

savings_income_ratio = df['SavingsAccountBalance'] / df['AnnualIncome']
liability_asset_ratio = df['TotalLiabilities'] / df['TotalAssets']
credit_card_utilization_normalized = df['CreditCardUtilizationRate'] / df['CreditCardUtilizationRate'].max()
debt_to_income_normalized = df['DebtToIncomeRatio'] / df['DebtToIncomeRatio'].max()
liability_asset_normalized = liability_asset_ratio / liability_asset_ratio.max()
loan_duration_normalized = df['LoanDuration'] / df['LoanDuration'].max()
age_normalized = df['Age'] / df['Age'].max()
w1, w2, w3, w4, w5 = 0.3,0.3,0.1,0.1,0.2
behavioural_risk = (
    w1 * credit_card_utilization_normalized +
    w2 * debt_to_income_normalized +
    w3 * liability_asset_normalized +
    w4 * age_normalized +
    w5 * loan_duration_normalized
)
behavioural_risk = (behavioural_risk - behavioural_risk.min()) / (behavioural_risk.max() - behavioural_risk.min())
df['BehaviouralRisk'] = behavioural_risk
threshold = 0.7
threshold2 = 0.4
risky_loans = df[df['BehaviouralRisk'] >= threshold]
good_loans = df[df['BehaviouralRisk'] <= threshold2]
denied_percentage = (risky_loans['LoanApproved'].value_counts(normalize=True).get(0) * 100)
allowed_percentage = (good_loans['LoanApproved'].value_counts(normalize=True).get(1) * 100)

# -------------------------------------------------------------------------------------------------------------------------

df_sorted = df.sort_values('CreditScore')
bins = np.linspace(300, 850, 15)
df_sorted['CreditScoreBin'] = pd.cut(df_sorted['CreditScore'], bins=bins)
bin_avg = df_sorted.groupby('CreditScoreBin',observed=True).agg({
    'BehaviouralRisk': 'mean'
}).reset_index()
bin_avg['CreditScore'] = bin_avg['CreditScoreBin'].apply(lambda x: x.mid)
plt.figure(figsize=(10, 6))
plt.plot(bin_avg['CreditScore'], bin_avg['BehaviouralRisk'], color='#007acc', marker='o', linewidth=2, markersize=6)
plt.title('BehaviouralRisk vs CreditScore', fontsize=16)
plt.xlabel('CreditScore', fontsize=14)
plt.ylabel('BehaviouralRisk', fontsize=14)
plt.tight_layout()
plt.savefig('../images/fig36.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

df_sorted = df.sort_values('CreditScore')
bins = np.linspace(300, 850, 15)
df_sorted['CreditScoreBin'] = pd.cut(df_sorted['CreditScore'], bins=bins, labels=False)
bin_avg = df_sorted.groupby('CreditScoreBin').agg({
    'CreditScore': 'mean',
    'BehaviouralRisk': 'max'
}).reset_index()
plt.figure(figsize=(10, 6))
plt.plot(bin_avg['CreditScore'], bin_avg['BehaviouralRisk'], color='#007acc', marker='o', linewidth=2, markersize=6)
plt.title('BehaviouralRisk vs CreditScore', fontsize=16)
plt.xlabel('CreditScore', fontsize=14)
plt.ylabel('BehaviouralRisk', fontsize=14)
plt.tight_layout()
plt.savefig('../images/fig37.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

df_sorted = df.sort_values('PaymentHistory')
bins = np.linspace(df_sorted['PaymentHistory'].min(), 40, 15)
df_sorted['PaymentHistoryBin'] = pd.cut(df_sorted['PaymentHistory'], bins=bins, labels=False)
bin_avg_payment_history = df_sorted.groupby('PaymentHistoryBin').agg({
    'PaymentHistory': 'mean',
    'BehaviouralRisk': 'mean'
}).reset_index()
plt.figure(figsize=(10, 6))
plt.plot(bin_avg_payment_history['PaymentHistory'], bin_avg_payment_history['BehaviouralRisk'], color='#007acc', marker='o', linewidth=2, markersize=6)
plt.title('BehaviouralRisk vs PaymentHistory', fontsize=16)
plt.xlabel('PaymentHistory', fontsize=14)
plt.ylabel('BehaviouralRisk', fontsize=14)
plt.tight_layout()
plt.savefig('../images/fig38.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

bin_avg_credit_lines = df.groupby('NumberOfOpenCreditLines')['BehaviouralRisk'].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(bin_avg_credit_lines['NumberOfOpenCreditLines'], bin_avg_credit_lines['BehaviouralRisk'], color='#007acc', marker='o', linewidth=2, markersize=6)
plt.title('BehaviouralRisk vs Number of Open Credit Lines', fontsize=16)
plt.xlabel('Number of Open Credit Lines', fontsize=14)
plt.ylabel('BehaviouralRisk', fontsize=14)
plt.tight_layout()
plt.savefig('../images/fig39.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

df_copy = df.copy()
columns_to_drop = [
    'CreditCardUtilizationRate', 'DebtToIncomeRatio', 'LoanDuration','TotalAssets', 'Age',
    'BehaviouralRisk','TotalLiabilities'
]
df_copy.drop(columns=columns_to_drop, inplace=True)
X = df_copy
y = df['BehaviouralRisk']
le = LabelEncoder()
for col in X.select_dtypes(include=['object', 'category']).columns:
    X[col] = le.fit_transform(X[col])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
accuracy_percentage = r2 * 100
print("Accuracy of predicting BehaviouralRisk: ",accuracy_percentage)
importances = rf.feature_importances_

features = X.columns
non_category_features = [feature for feature in features if not feature.endswith('Category')]
non_category_importances = importances[[features.get_loc(feature) for feature in non_category_features]]
indices = np.argsort(non_category_importances)[::-1]
non_category_features = np.array(non_category_features)
top_5_features = non_category_features[indices][:5]
top_5_importances = non_category_importances[indices][:5]
plt.figure(figsize=(10, 6))
plt.barh(range(len(top_5_importances)), top_5_importances, align="center")
plt.yticks(range(len(top_5_importances)), top_5_features)
plt.xlabel("Relative Importance")
plt.tight_layout()
plt.savefig('../images/fig40.png', bbox_inches='tight')
plt.close()

# ----------------------------------------------------------------------------------------------------------------

combinations = pd.crosstab(df['BehaviouralRisk'] > 0.7, df['LoanApproved'] == 1)
labels = [
    'BehaviouralRisk > 0.7 & Loan Approved',
    'BehaviouralRisk < 0.7 & Loan Denied',
    'BehaviouralRisk <= 0.7 & Loan Approved',
    'BehaviouralRisk > 0.7 & Loan Denied'
]
sizes = [
    combinations.loc[True, True] if True in combinations.index and True in combinations.columns else 0,
    combinations.loc[True, False] if True in combinations.index and False in combinations.columns else 0,
    combinations.loc[False, True] if False in combinations.index and True in combinations.columns else 0,
    combinations.loc[False, False] if False in combinations.index and False in combinations.columns else 0
]

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666', '#99ff99', '#ffcc99'])
plt.axis('equal')
plt.savefig('../images/fig41.png', bbox_inches='tight')
plt.close('all')

# ---------------------------------------------------------------------------------------------------------------

bins = [0, 10, 25, np.inf]
labels = ['Short-term', 'Mid-term', 'Long-term']
df['LoanDurationCategory'] = pd.cut(df['LoanDuration'], bins=bins, labels=labels, right=True)

bins_jobs = [0, 5, 12, np.inf]
labels_jobs = ['Short', 'Mid', 'Long']
df['JobTenureCategory'] = pd.cut(df['JobTenure'], bins=bins_jobs, labels=labels_jobs, right=True)

bins_net_worth = [-np.inf, 30000, 80000, np.inf]
labels_net_worth = ['Small', 'Medium', 'Large']
df['NetWorthCategory'] = pd.cut(df['NetWorth'], bins=bins_net_worth, labels=labels_net_worth, right=True)

bins_bv_risk = [0, 0.6, 0.7, 1]
labels_bv_risk = ['Good', 'Okay', 'Poor']
df['BehaviouralRiskCategory'] = pd.cut(df['BehaviouralRisk'], bins=bins_bv_risk, labels=labels_bv_risk, right=True)

feature_to_label = {  
    'LoanDurationCategory': 'Loan Duration',
    'JobTenureCategory': 'Job Tenure',
    'NetWorthCategory': 'Net Worth',
    'BehaviouralRiskCategory': 'Behavioural Risk',
    'LoanApproved': 'Approval Status'
}
source_features = ['LoanDurationCategory', 'JobTenureCategory', 'NetWorthCategory', 'BehaviouralRiskCategory']
all_categories = {}
index = 0
for col in source_features + ['LoanApproved']:
    for value in df[col].unique():
        if value not in all_categories:
            all_categories[value] = index
            index += 1

source = []
target = []
value = []
colors = []
color_palette = plt.cm.Pastel2(np.linspace(0, 1, len(all_categories)))
for i in range(len(source_features)):
    col1 = source_features[i]
    col2 = source_features[i + 1] if i + 1 < len(source_features) else 'LoanApproved'
    for group, sub_df in df.groupby([col1, col2], observed=True):
        source.append(all_categories[group[0]])
        target.append(all_categories[group[1]])
        value.append(len(sub_df))
        colors.append(color_palette[all_categories[group[0]]])
flow_colors = [f"rgba({int(c[0] * 255)}, {int(c[1] * 255)}, {int(c[2] * 255)}, 0.8)" for c in colors]
labels = [key for key, val in sorted(all_categories.items(), key=lambda x: x[1])]
x_positions = np.linspace(0.1, 0.9, len(source_features) + 1)
x_positions[0] -= 0.15
x_positions[1] -= 0.1
x_positions[2] -= 0.02
x_positions[3] += 0.1
x_positions[4] += 0.15
annotations = []
for i, feature in enumerate(source_features + ['LoanApproved']):
    annotations.append(
        dict(
            x=x_positions[i], 
            y=1.1,
            text=feature_to_label[feature],
            showarrow=False,
            font=dict(size=14, color="black"),
            align="center"
        )
    )

fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=flow_colors,
    )
))

fig.update_layout(
    paper_bgcolor="white",
    annotations=annotations
)
fig.write_image("../images/fig42.png")
sys.exit(0)

# --------------------------------------------------------------------------------------------------------------