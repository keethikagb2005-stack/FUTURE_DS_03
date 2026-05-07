# =========================================
# MARKETING FUNNEL & CONVERSION PERFORMANCE ANALYSIS
# Internship Project - Python Flask Backend
# =========================================

from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# =========================================
# SAMPLE MARKETING FUNNEL DATA
# =========================================

marketing_data = {
    'Channel': [
        'Facebook Ads', 'Instagram Ads', 'Google Ads',
        'LinkedIn Campaign', 'Email Marketing',
        'YouTube Ads', 'Organic Search', 'Referral'
    ],

    'Visitors': [12000, 15000, 18000, 8000, 6000, 9000, 11000, 5000],

    'Leads': [3200, 4100, 5300, 2100, 1700, 2500, 3700, 1800],

    'Qualified_Leads': [2100, 2800, 3900, 1500, 1200, 1700, 2900, 1300],

    'Opportunities': [1200, 1700, 2500, 1000, 800, 1100, 1800, 900],

    'Customers': [650, 920, 1500, 610, 450, 580, 1200, 550],

    'Marketing_Spend': [150000, 180000, 250000, 100000, 70000, 120000, 90000, 50000]
}

# =========================================
# CREATE DATAFRAME
# =========================================

df = pd.DataFrame(marketing_data)

# =========================================
# CALCULATE CONVERSION METRICS
# =========================================

df['Visitor_to_Lead_%'] = round((df['Leads'] / df['Visitors']) * 100, 2)

df['Lead_to_Qualified_%'] = round((df['Qualified_Leads'] / df['Leads']) * 100, 2)

df['Qualified_to_Opportunity_%'] = round((df['Opportunities'] / df['Qualified_Leads']) * 100, 2)

df['Opportunity_to_Customer_%'] = round((df['Customers'] / df['Opportunities']) * 100, 2)

df['Overall_Conversion_%'] = round((df['Customers'] / df['Visitors']) * 100, 2)

df['Cost_Per_Lead'] = round(df['Marketing_Spend'] / df['Leads'], 2)

df['Customer_Acquisition_Cost'] = round(df['Marketing_Spend'] / df['Customers'], 2)

# =========================================
# TOTAL FUNNEL CALCULATIONS
# =========================================

total_visitors = df['Visitors'].sum()
total_leads = df['Leads'].sum()
total_qualified = df['Qualified_Leads'].sum()
total_opportunities = df['Opportunities'].sum()
total_customers = df['Customers'].sum()

overall_conversion = round((total_customers / total_visitors) * 100, 2)

# =========================================
# IDENTIFY DROP-OFFS
# =========================================

drop_visitor_lead = total_visitors - total_leads
drop_lead_qualified = total_leads - total_qualified
drop_qualified_opportunity = total_qualified - total_opportunities
drop_opportunity_customer = total_opportunities - total_customers

# =========================================
# CREATE CHARTS
# =========================================

if not os.path.exists('static'):
    os.makedirs('static')

# Funnel Chart
funnel_stages = ['Visitors', 'Leads', 'Qualified Leads', 'Opportunities', 'Customers']
funnel_values = [
    total_visitors,
    total_leads,
    total_qualified,
    total_opportunities,
    total_customers
]

plt.figure(figsize=(10, 6))
sns.barplot(x=funnel_stages, y=funnel_values)
plt.title('Marketing Funnel Performance')
plt.xlabel('Funnel Stages')
plt.ylabel('Count')
plt.savefig('static/funnel_chart.png')
plt.close()

# Channel Performance Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=df['Channel'], y=df['Customers'])
plt.xticks(rotation=20)
plt.title('Customers Acquired by Marketing Channel')
plt.xlabel('Marketing Channels')
plt.ylabel('Customers')
plt.savefig('static/channel_performance.png')
plt.close()

# Conversion Rate Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=df['Channel'], y=df['Overall_Conversion_%'])
plt.xticks(rotation=20)
plt.title('Overall Conversion Rate by Channel')
plt.xlabel('Channels')
plt.ylabel('Conversion Rate %')
plt.savefig('static/conversion_rate.png')
plt.close()

# CAC Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=df['Channel'], y=df['Customer_Acquisition_Cost'])
plt.xticks(rotation=20)
plt.title('Customer Acquisition Cost by Channel')
plt.xlabel('Channels')
plt.ylabel('CAC')
plt.savefig('static/cac_chart.png')
plt.close()

# =========================================
# BEST & WORST CHANNEL ANALYSIS
# =========================================

best_channel = df.loc[df['Overall_Conversion_%'].idxmax()]

worst_channel = df.loc[df['Overall_Conversion_%'].idxmin()]

# =========================================
# HOME ROUTE
# =========================================

@app.route('/')
def dashboard():

    recommendations = [
        "Improve landing page optimization to reduce visitor drop-offs.",
        "Increase retargeting campaigns for unqualified leads.",
        "Focus more budget on high-performing Google Ads and Organic Search.",
        "Enhance email personalization to improve engagement.",
        "Implement AI-based lead scoring for better qualification.",
        "Improve customer onboarding process to increase final conversions.",
        "Use A/B testing for ad creatives and CTA buttons.",
        "Optimize mobile responsiveness of landing pages."
    ]

    return render_template(
        'index.html',
        tables=[df.to_html(classes='data', index=False)],

        total_visitors=total_visitors,
        total_leads=total_leads,
        total_qualified=total_qualified,
        total_opportunities=total_opportunities,
        total_customers=total_customers,

        overall_conversion=overall_conversion,

        drop_visitor_lead=drop_visitor_lead,
        drop_lead_qualified=drop_lead_qualified,
        drop_qualified_opportunity=drop_qualified_opportunity,
        drop_opportunity_customer=drop_opportunity_customer,

        best_channel=best_channel['Channel'],
        best_conversion=best_channel['Overall_Conversion_%'],

        worst_channel=worst_channel['Channel'],
        worst_conversion=worst_channel['Overall_Conversion_%'],

        recommendations=recommendations
    )

# =========================================
# MAIN FUNCTION
# =========================================

if __name__ == '__main__':
    app.run(debug=True)