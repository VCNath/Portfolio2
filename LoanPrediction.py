#import libraires
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import numpy as np
#load data
data = pd.read_csv('/Users/nathanielvc/Downloads/Loan payments data.csv')
#check for null values
print(data.isnull().sum())
#dealing with null values (handle missing values and numerical columns)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

num_cols = ['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']

for col in num_cols:
    data[col] = imputer.fit_transform(data[col].values.reshape(-1,1))
#econding numbers for the modeling process    
encoder = LabelEncoder()

cat_cols = ['Gender','Married','Dependents','Education','Self_Employed','Property_Area','Loan_Status']

for col in cat_cols:
    data[col] = encoder.fit_transform(data[col])
    
#training

X = data.drop(columns=['Loan_ID','Loan_Status'],axis=1)
Y = data['Loan_Status']
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

model = LogisticRegression()
model.fit(X_train,Y_train)

#model evaluation
predictions = model.predict(X_test)
print('Model Accuracy:', accuracy_score(Y_test,predictions))

#predicting for new data
new_data = [[1,0,0,1,0,0,1,0,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1]]
predictions = model.predict(new_data)
predictions('Loan Status for new application:', predictions)
