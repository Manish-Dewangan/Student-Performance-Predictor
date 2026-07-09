import joblib
import pandas as pd
import sys

print("Loading model...")
model = joblib.load("models/model.pkl")
print("Model loaded successfully.")

# Mock student data based on typical student performance features
# I'll need to know the features, let's just inspect the model's feature names
try:
    if hasattr(model, "feature_names_in_"):
        print("Expected features:", model.feature_names_in_)
        # Create a dummy dataframe with these features
        dummy_data = {col: [0] for col in model.feature_names_in_}
        df = pd.DataFrame(dummy_data)
        
        print("Testing predict...")
        prediction = model.predict(df)
        print("Prediction:", prediction)
    else:
        print("No feature_names_in_ attribute.")
except Exception as e:
    print("Error:", e)
    sys.exit(1)
