import pandas as pd
import numpy as np
import re

#step1 ----load dataset
df = pd.read_csv('raw_eco_india.csv')
print("Data Is Loaded Successfully", df.shape)


#step2 ----duplicates
df = df.drop_duplicates()
df = df.drop_duplicates(subset=['order_id'])
print("After Duplicates:", df.shape)


#step3 ----whitespaces and random chars
text_cols = ['order_id', 'customer_name', 'city', 'state', 'product_category', 
             'product_name', 'payment_method', 'order_status']
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s&,._-]', '', str(x)) if pd.notna(x) else x)
    df[col] = df[col].replace('nan', np.nan)
print("Spaces and Chars Cleaned")


#step4 ----standardize text(city wise)
city_map = {
    'mumbai':'Mumbai','MUMBAI':'Mumbai','mombai':'Mumbai','Mombai':'Mumbai',
    'delhi':'Delhi','new delhi':'Delhi','NEW DELHI':'Delhi','New Delhi':'Delhi',
    'bangalore':'Bangalore','Bengaluru':'Bangalore','bengaluru':'Bangalore','BANGALORE':'Bangalore','Banglore':'Bangalore',
    'chennai':'Chennai','chenai':'Chennai','Chenai':'Chennai',
    'hyderabad':'Hyderabad','hydrabad':'Hyderabad','Hydrabad':'Hyderabad',
    'pune':'Pune','PUNE':'Pune',
    'kolkata':'Kolkata','calcutta':'Kolkata','Calcutta':'Kolkata',
    'ahmedabad':'Ahmedabad','ahemdabad':'Ahmedabad','Ahemdabad':'Ahmedabad',
    'jaipur':'Jaipur'
}
df['city'] = df['city'].str.strip().replace(city_map)


#step5 ----category standardize(product wise)
cat_map = { 
    'electronics':'Electronics','ELECTRONICS':'Electronics','electroncis':'Electronics','electr0nics':'Electronics',
    'clothing':'Clothing','CLOTHING':'Clothing','clothng':'Clothing',
    'home and kitchen':'Home & Kitchen','home & kitchen':'Home & Kitchen',
    'homekitchen':'Home & Kitchen','home&kitchen':'Home & Kitchen',
    'books':'Books','BOOKS':'Books',
    'sports':'Sports','SPORTS':'Sports','sport':'Sports',
    'beauty':'Beauty','BEAUTY':'Beauty','beuty':'Beauty'}
df['product_category'] = df['product_category'].str.strip().str.lower().map( 
    lambda x: cat_map.get(x, x.title() if isinstance(x, str) else x))

#step6 ----payment method standardize
pay_map = { 
    'credit card':'Credit Card','cc':'Credit Card','creditcard':'Credit Card',
    'upi':'UPI','Upi':'UPI',
    'debit card':'Debit Card','dc':'Debit Card',
    'net banking':'Net Banking','netbanking':'Net Banking','net banking':'Net Banking',
    'cod':'COD','cash on delivery':'COD'}
df['payment_method'] = df['payment_method'].str.strip().str.lower().map( 
    lambda x: pay_map.get(x, x) if isinstance(x, str) else x)

#step7 ----order status standardize
status_map = { 
    'delivered':'Delivered','DELIVERED':'Delivered',
    'pending':'Pending','PENDING':'Pending',
    'cancelled':'Cancelled','cancelled':'Cancelled','Cancled':'Cancelled','cancled':'Cancelled','cancled':'Cancelled','cancled':'Cancelled', 
    'shipped':'Shipped','shipped':'Shipped','Shpped':'Shipped','shpped':'Shipped','shpped':'Shipped','shpped':'Shipped',
    'returned':'Returned','RETURNED':'Returned'}
df['order_status'] = df['order_status'].str.strip().replace(status_map)

#step8 ----numeric fixes(negative quantity and outliers)
df['quantity'] = df['quantity'].abs()
df.loc[df['quantity'] > 100, 'quantity'] = np.nan
df.loc[df['quantity']==0, 'quantity'] = np.nan
df.loc[df['unit_price'] <= 0, 'unit_price'] = np.nan
df.loc[df['unit_price'] > 50000, 'unit_price'] = np.nan

df['total_amount'] = (df['quantity'] * df['unit_price']).round(2)
print("Negative Numeric Fixed")


# 1. Datetime objects mein convert karein
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True, errors='coerce')
df['delivery_date'] = pd.to_datetime(df['delivery_date'], dayfirst=True, errors='coerce')

# 2. Sirf tabhi drop karein jab DONO dates missing hon (truly corrupt rows)
df = df.dropna(subset=['order_date', 'delivery_date'], how='all')

# 3. Format apply karein aur missing values ko gracefully fill karein
df['order_date'] = df['order_date'].dt.strftime('%d/%m/%Y').fillna("Not Recorded")
df['delivery_date'] = df['delivery_date'].dt.strftime('%d/%m/%Y').fillna("Pending Delivery")


#step11 ----missing values 
state_fill = {
    'Mumbai':'Maharashtra',
    'Delhi':'Delhi',
    'Bangalore':'Karnataka',
    'Chennai':'Tamil Nadu',
    'Hyderabad':'Telangana',
    'Pune':'Maharashtra',
    'Kolkata':'West Bengal',
    'Ahmedabad':'Gujarat',
    'Jaipur':'Rajasthan'
}
df['state'] = df.apply(
    lambda row: state_fill.get(row['city'], row['state'])
    if pd.isnull(row['state']) else row['state'], axis=1)
df['state'] = df['state'].str.title()
df['payment_method'] = df['payment_method'].fillna(df['payment_method'].mode()[0])
df['order_status'] = df['order_status'].fillna('Unknown')
df['product_name'] = df['product_name'].fillna('Unknown')
print("Missing values fixed")


#step12 ----final_result.csv file
df.to_csv('final_result.csv', index=False)
print("\nDone File Saved")
