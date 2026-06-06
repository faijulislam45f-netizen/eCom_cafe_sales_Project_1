import pandas as pd

df = pd.read_csv('raw_eco_india.csv')
print("=== SHAPE ===")
print(df.shape)

print("\n=== MISSING VALUES ===")
for col in df.columns:
    print(col, ':', df[col].isnull().sum())

print("\n=== DUPLICATES ===")
print('Total Duplicates Rows:', df.duplicated().sum())
print("\n=== NUMERIC OUTLIERS ===")
for col in ['quantity','unit_price','total_amount']:
    print(col, '| min:', df[col].min(), '| max:', df[col].max())


print("\n=== RANDOM CHARACTERS ===")
for col in ['order_id','customer_name','city','product_category','product_name']:
    mask = df[col].astype(str).str.contains(r'^a-zA-Z0-9\s&,._-]', regex=True, na=False)
    print(col, ':', mask.sum(), 'rows')

print("\n=== WHITESPACES ===")
for col in ['customer_name','city','state','product_category','product_name','payment_method','order_status']:
    mask = df[col].astype(str).str.contains(r'^\s|\s$', regex=True, na=False)
    print(col, ':', mask.sum(), 'rows')
