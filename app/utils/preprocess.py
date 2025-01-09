import pandas as pd

def preprocess_products(filepath):
    """Preprocess the products dataset."""
    df = pd.read_csv(filepath)
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column].fillna(0, inplace=True)  
        else:
            df[column].fillna("", inplace=True) 

    # Prepare metadata
    metadata = df[["title", "price", "average_rating"]].to_dict(orient="records")
    return df, metadata

def preprocess_orders(filepath):
    """Preprocess the orders dataset."""
    df = pd.read_csv(filepath)
    for column in df.columns:
        if df[column].dtype == 'float64' or df[column].dtype == 'int64':
            df[column].fillna(0, inplace=True) 
        else:
            df[column].fillna("", inplace=True)  
    return df
