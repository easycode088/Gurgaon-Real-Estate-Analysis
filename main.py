import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('row.csv')

# print(df.head())
# print(df.columns.tolist())

# find the costly flat and before we move forward we will clean the data
# print(df.info())  #to see the some information of data 

# data cleaning 

df.columns = df.columns.str.strip().str.lower().str.replace(" " ,"_")
print(df.columns.tolist())
df = df.drop_duplicates()

# Numerical columns cleaning

df['price'] = df["price"].astype(str).str.replace(",","_").astype(int)
df['area'] = df["area"].astype(str).str.replace(",","_").astype(int)
df['rate_per_sqft'] = df["rate_per_sqft"].astype(str).str.replace(",","_").astype(int)
# print(df['price'])
# print(df['area'])
# print(df['rate_per_sqft'])

# Categorical columns cleaning
df['status'] = df["status"].str.strip().str.lower()
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False })
df['flat_type'] = df['flat_type'].str.strip().str.lower()

df = df.drop_duplicates()
# print(df['rera_approval'])
# print(df)
# print(df.info())

# Q1 Which is the costlies flat in the dataset
costliest_flat = df.loc[df['price'].idxmax()]
# Lets write this output into sentence that Ai will do this and good for present
"""

price                                  1226300000
status                              ready to move
area                                        16500
rate_per_sqft                               74323
property_type    6 BHK Apartment in DLF Camellias
locality                                Sector 42
builder_name                    Provident Capital
rera_approval                               False
bhk_count                                       6
socity                              DLF Camellias
company_name                                  DLF
flat_type                               apartment

"""
print(f"The costliest flat is a {costliest_flat['bhk_count']} BHK flat located in {costliest_flat['locality']} priced at {costliest_flat['price']/10000000} crores in {costliest_flat['society']} society.")
# print(costliest_flat) 

# Q 2 Which locality has a highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
print(f"The locality with highest average price is {highest_avg_price_locality}.")

# Q3 Which locality has the highest rate per square foot?
highest_rate_per_sqft_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax()
print(f"The locality with highest rate per square is {highest_rate_per_sqft_locality}.")

# Q4 Do ready to move properties cost more tha under construction?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()

if ready_to_move_avg_price > under_construction_avg_price:
    print("Ready-to-move properties cost more on average than under-constructionproperties")
else:
   print("Under-construction properties cos more than average than ready-to-move properties")

# Q5 Do rera approved properties commnad a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price > rera_not_approved_avg_price:
    print("RERA-approved command a price premium")
else:
    print("RERA-approved properties do not command a price premium")

# Q6 How does area sqft impact price
# sns.scatterplot(data=df, x= 'area', y= 'price')
# plt.show()

# Q7 Which BHK configuration is most expensive 

most_expensive_bhk = df.groupby('bhk_count')['price'].mean().idxmax()
print(f"The most expensive BHK configuration on average is  {most_expensive_bhk} BHK.")
# based on rate_per_sqft it is showing 114 bhk might data is some issue

# Q8 Which property price is costliest

most_expensive_property_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"The most expensive property type is {most_expensive_property_type}.")

# Q9 Do certain builders price higher

# print(df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending = False).head(5))
# print name of top  builders

print("The top 5 builders that price higher are:", end=" ")
top_5_builders = df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending = False).head(5)
for builder in top_5_builders.index:
    print(builder, end=",")

# Q10 Are larger homes are expensive per sqft
sns.scatterplot(data= df, x = 'area', y ='rate_per_sqft')
plt.show()
