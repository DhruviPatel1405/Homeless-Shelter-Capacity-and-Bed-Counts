#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import zipfile
import io


# In[2]:


# URL to the dataset
url = "https://www150.statcan.gc.ca/n1/tbl/csv/14100353-eng.zip"

# Download and extract the dataset
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
    zip_file.extractall("data")  # Extract the contents to the "data" folder

# Load data from CSV file
file_path = "data/14100353.csv"
df = pd.read_csv(file_path)


# In[3]:


df.shape


# In[4]:


df.info()


# In[7]:


df.drop(['STATUS','SYMBOL','TERMINATED'],axis=1,inplace=True)


# In[8]:


pd.isnull(df).sum()


# In[9]:


df.dropna(inplace=True)


# In[10]:


df.shape


# In[11]:


df.info()


# In[12]:


pd.isnull(df).sum()


# In[13]:


df.columns


# In[50]:


df.describe(include='object')


# In[14]:


df.drop(['DECIMALS','SCALAR_ID'],axis=1,inplace=True)


# In[16]:


df.rename(columns={'GEO': 'Region', 'REF_DATE': 'Year', 'VALUE': 'Count'}, inplace=True)


# In[17]:


df['Year'] = pd.to_datetime(df['Year'])


# In[18]:


df['Year'] = pd.to_datetime(df['Year'])


# In[19]:


df['Occupancy_Rate'] = df['Count'] / df.groupby(['Year', 'Type of shelter'])['Count'].transform('sum') * 100


# In[20]:


df['Count'].fillna(method='ffill', inplace=True)


# In[21]:


print(df.duplicated().sum())


# In[22]:


df['Count'] = df['Count'].astype(int)


# In[23]:


print(df['Type of shelter'].unique())


# In[24]:


from scipy.stats import zscore

z_scores = zscore(df['Count'])
df = df[(z_scores < 3)]  # Remove rows with extreme values (z-score > 3)


# In[25]:


df.rename(columns={'Type of shelter': 'Shelter_type'}, inplace=True)


# In[26]:


df.info()


# In[27]:


print(df.describe())


# In[28]:


import numpy as ny 
import matplotlib.pyplot as plt
import seaborn as sns


# In[29]:


# Explore shelter capacity and bed counts for Canada
plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='Count', hue='Statistics', data=df[df['Region'] == 'Canada'])
plt.title('Shelter Capacity and Bed Counts in Canada')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


# In[30]:


# Explore shelter capacity and bed counts by province
plt.figure(figsize=(12, 6))
sns.barplot(x='Region', y='Count', hue='Statistics', data=df[df['Region'] != 'Canada'])
plt.title('Shelter Capacity and Bed Counts by Province')
plt.xlabel('Province')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Statistics')
plt.show()


# In[32]:


print(df['Shelter_type'].unique())


# In[33]:


df.head()


# In[35]:


df['Occupancy_Rate'] = df['Count'] / df.groupby(['Year', 'Shelter_type'])['Count'].transform('sum') * 100


# In[36]:


print(df['Occupancy_Rate'])


# In[37]:





# In[38]:


# Time Series Analysis - Shelter Capacity and Bed Counts in Canada
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Count', hue='Statistics', data=df[df['Region'] == 'Canada'])
plt.title('Time Series Analysis - Shelter Capacity and Bed Counts in Canada')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


# In[40]:


# Time Series Analysis - Shelter Occupancy Rates in Canada
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Occupancy_Rate', hue='Shelter_type', data=df[df['Region'] == 'Canada'])
plt.title('Time Series Analysis - Shelter Occupancy Rates in Canada')
plt.xlabel('Year')
plt.ylabel('Occupancy Rate (%)')
plt.xticks(rotation=45)
plt.show()


# In[44]:


plt.figure(figsize=(14, 8))
sns.barplot(x='Region', y='Count', hue='Shelter_type', data=df[df['Region'] != 'Canada'])
plt.title('Comparative Analysis - Shelter Capacity and Bed Counts by Province and Shelter Type')
plt.xlabel('Province')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Shelter_type')
plt.show()


# In[45]:


plt.figure(figsize=(14, 8))
sns.barplot(x='Region', y='Count', hue='Shelter_type', data=df[df['Region'] != 'Canada'])
plt.title('Comparative Analysis - Shelter Capacity and Bed Counts by Province and Shelter Type')
plt.xlabel('Province')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Shelter_type')
plt.show()


# In[49]:


plt.figure(figsize=(14, 8))
sns.barplot(x='Region', y='Occupancy_Rate', hue='Shelter_type', data=df[df['Region'] != 'Canada'])
plt.title('Comparative Analysis - Shelter Occupancy Rates by Province and Shelter Type')
plt.xlabel('Province')
plt.ylabel('Occupancy Rate (%)')
plt.xticks(rotation=45)
plt.legend(title='Shelter_type')
plt.show()


# In[ ]:




