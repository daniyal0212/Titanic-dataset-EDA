import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


os.chdir('E:/python/practice')

data = pd.read_csv('titanic.csv')

#checking for null values
print(data.isnull().sum())
#cleaning the data
data['Age'].fillna(data['Age'].mean(), inplace=True)
data.drop('Cabin', axis=1, inplace=True)
# mapping categorical variables to numeric values for analysis
data['Embarked'] = data['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# adding new variables in the original dataset
data['Age Group'] = pd.cut(data['Age'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80,90], 
                                labels=['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90'])
data['Fare Group'] = pd.cut(data['Fare'], bins=[-1, 50, 100, 150, 200, 300, 400, 500, 600], 
                                labels=['0-50', '50-100', '100-150', '150-200', '200-300', '300-400', '400-500', '500-600'])
data['Title'] = data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
data['Family Size']=data['SibSp'] + data['Parch'] + 1
# displaying titles in front of name column in the dataset
name_idx = data.columns.get_loc('Name')
data.insert(name_idx, 'Title', data.pop('Title'))
#checking if the changes worked or not
print(data.head())

#checking for null values again after cleaning
print(data.isnull().sum())

# checking for variables and data types
print(data.info())
print(data.columns)
print(data.head())
#overall description of the data
print(data.describe())


# making 2 copy of the data to work on(one for numeric analysis and one for categorical analysis)
dataset= data.copy()
dataset_cat = data.copy()


# VISUALIZATION OF THE DATA
# count of people according to their age group
sns.histplot(dataset['Age'], kde=True)  # histogram + density curve
plt.savefig('E:/python/practice/plots/age_distribution.png', bbox_inches='tight')
plt.close()
# count of survivors
sns.countplot(x='Survived', data=dataset)
plt.title('Survival Count')
plt.savefig('E:/python/practice/plots/survival_count.png', bbox_inches='tight')
plt.close()
# age distribution of survivors and non-survivors(two types of charts)
sns.countplot(x='Age Group', hue='Survived', data=dataset)
plt.title('Age Distribution by Survival')
plt.xticks(rotation=45)
plt.savefig('E:/python/practice/plots/age_distribution_by_survival.png', bbox_inches='tight')
plt.close()
# boxplot
sns.boxplot(x='Survived', y='Age', data=dataset)    
plt.title('Age Distribution by Survival')
plt.savefig('E:/python/practice/plots/age_boxplot.png', bbox_inches='tight')
plt.close()
# gender distribution of survivors and non-survivors
sns.countplot(x='Survived', hue='Sex', data=dataset)
plt.title(' Survival Count by Gender')
plt.savefig('E:/python/practice/plots/survival_by_gender.png', bbox_inches='tight')
plt.close()
# distribution of survivors and non-survivors by passenger class
sns.countplot(x='Survived', hue='Pclass', data=dataset)
plt.title('Survival Count by Passenger Class')
plt.savefig('E:/python/practice/plots/survival_by_passenger_class.png', bbox_inches='tight')
plt.close()
# fare distribution wrt survival
sns.countplot(x='Fare Group', hue='Survived', data=dataset)
plt.title('Fare Distribution by Survival')
plt.xticks(rotation=45)
plt.savefig('E:/python/practice/plots/fare_distribution_by_survival.png', bbox_inches='tight')
plt.close()
# location of survivors and non-survivors by port of embarkation
sns.countplot(x='Survived', hue='Embarked', data=dataset)
handles, _ = plt.gca().get_legend_handles_labels()
plt.legend(handles, ['S - Southampton', 'C - Cherbourg', 'Q - Queenstown'], title='Embarked')
plt.title('Survival Count by Port of Embarkation')
plt.savefig('E:/python/practice/plots/survival_by_embarked.png', bbox_inches='tight')
plt.close()

# correlation between variables
# DROPPING and changing SOME VARIABLES FOR CORRELATION MATRIX
dataset.drop('Name', axis=1, inplace=True)
dataset.drop('Ticket', axis=1, inplace=True)
dataset.drop('Title', axis=1, inplace=True)
dataset.drop('Age Group', axis=1, inplace=True)
dataset.drop('Fare Group', axis=1, inplace=True)
dataset['Sex'] = dataset['Sex'].map({'male': 0, 'female': 1})
# calculating correlation matrix and visualizing it using heatmap
correlation_matrix = dataset.corr()
plt.figure(figsize=(12, 10))  
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.tight_layout()  # prevents cutoff
plt.savefig('E:/python/practice/plots/correlation_matrix.png', bbox_inches='tight')
plt.close()

print(data.info())
print(data.isnull().sum())

data.to_csv('titanic_cleaned.csv', index=False)
