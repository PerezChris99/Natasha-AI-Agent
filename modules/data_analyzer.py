import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class DataAnalyzer:
    def __init__(self):
        self.current_dataset = None
        self.analysis_history = []

    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                self.current_dataset = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.current_dataset = pd.read_excel(file_path)
            return "Data loaded successfully"
        except Exception as e:
            return f"Error loading data: {str(e)}"

    def analyze_data(self, analysis_type):
        if self.current_dataset is None:
            return "No dataset loaded"

        if analysis_type == "summary":
            return self._get_summary_stats()
        elif analysis_type == "correlation":
            return self._analyze_correlations()
        elif analysis_type == "patterns":
            return self._find_patterns()
        elif analysis_type == "visualization":
            return self._create_visualization()

    def _get_summary_stats(self):
        summary = {
            "basic_stats": self.current_dataset.describe().to_dict(),
            "missing_values": self.current_dataset.isnull().sum().to_dict(),
            "data_types": self.current_dataset.dtypes.to_dict()
        }
        return summary

    def _analyze_correlations(self):
        numeric_data = self.current_dataset.select_dtypes(include=[np.number])
        correlations = numeric_data.corr()
        return correlations.to_dict()

    def _find_patterns(self):
        numeric_data = self.current_dataset.select_dtypes(include=[np.number])
        if len(numeric_data.columns) < 2:
            return "Not enough numeric columns for pattern analysis"

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        kmeans = KMeans(n_clusters=3)
        clusters = kmeans.fit_predict(scaled_data)
        
        return {
            "clusters": clusters.tolist(),
            "cluster_centers": kmeans.cluster_centers_.tolist()
        }

    def _create_visualization(self):
        plt.figure(figsize=(10, 6))
        numeric_data = self.current_dataset.select_dtypes(include=[np.number])
        numeric_data.boxplot()
        plt.title("Distribution of Numeric Variables")
        plt.xticks(rotation=45)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode()
