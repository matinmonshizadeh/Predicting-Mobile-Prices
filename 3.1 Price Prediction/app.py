import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import ttk

# Load dataset
mobile_df = pd.read_csv('cleaned_item_details.csv')

# Label encoding for categorical columns
label_encoders = {}
categorical_cols = ['Color', 'Brand Origin', 'Brand and Model', 'Status']
for col in categorical_cols:
    le = LabelEncoder()
    mobile_df[col] = le.fit_transform(mobile_df[col])
    label_encoders[col] = le

# Remove outliers based on Price(Toman)
Q1 = mobile_df['Price(Toman)'].quantile(0.25)
Q3 = mobile_df['Price(Toman)'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
mobile_df = mobile_df[(mobile_df['Price(Toman)'] >= lower_bound) & (mobile_df['Price(Toman)'] <= upper_bound)]

# Z-score normalization for numeric columns
numeric_cols = ['SIM Count', 'Internal Storage(GB)', 'RAM(GB)']
scaler = StandardScaler()
mobile_df[numeric_cols] = scaler.fit_transform(mobile_df[numeric_cols])

# Split into X and y
X = mobile_df.drop('Price(Toman)', axis=1)
y = mobile_df['Price(Toman)']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=519)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Create mapping dictionaries for categorical columns
mappings = {col: dict(zip(label_encoders[col].classes_, label_encoders[col].transform(label_encoders[col].classes_))) for col in categorical_cols}
reverse_mappings = {col: {v: k for k, v in mappings[col].items()} for col in categorical_cols}

# Tkinter App
class MobilePricePredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Price Predictor")
        
        # Create input fields
        self.create_widgets()

    def create_widgets(self):
        self.inputs = {}
        
        labels = ['Brand and Model', 'Status', 'SIM Count', 'Brand Origin', 'Internal Storage(GB)', 'RAM(GB)', 'Color']
        
        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            
            if label in categorical_cols:
                # Use dropdowns for categorical inputs
                self.inputs[label] = ttk.Combobox(self.root, values=list(mappings[label].keys()))
            else:
                self.inputs[label] = tk.Entry(self.root)
                
            self.inputs[label].grid(row=i, column=1, padx=10, pady=5)
        
        # Predict button
        self.predict_button = tk.Button(self.root, text="Predict Price", command=self.predict_price)
        self.predict_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        # Result label
        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    def predict_price(self):
        try:
            # Get input values
            input_values = {}
            for key, entry in self.inputs.items():
                value = entry.get()
                if key in categorical_cols:
                    if value in mappings[key]:
                        value = mappings[key][value]
                    else:
                        raise ValueError(f"Invalid input for {key}: {value}")
                input_values[key] = value

            # Extract numeric inputs and normalize them
            numeric_input = [float(input_values[key]) for key in numeric_cols]
            numeric_input_df = pd.DataFrame([numeric_input], columns=numeric_cols)
            normalized_numeric_input = scaler.transform(numeric_input_df)[0]

            # Reconstruct the input values list with normalized numeric inputs
            final_input_values = []
            for key in X.columns:
                if key in numeric_cols:
                    final_input_values.append(normalized_numeric_input[numeric_cols.index(key)])
                else:
                    final_input_values.append(input_values[key])
            
            # Predict price
            input_values_df = pd.DataFrame([final_input_values], columns=X.columns)
            predicted_price = model.predict(input_values_df)[0]
            
            # Display result
            self.result_label.config(text=f"Predicted Price: {predicted_price:.2f} Toman")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MobilePricePredictorApp(root)
    root.mainloop()
