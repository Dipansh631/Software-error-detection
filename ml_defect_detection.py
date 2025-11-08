"""
Complete Machine Learning Pipeline for Software Defect Detection

This program:
- Loads software defect datasets
- Preprocesses data (handles missing values, normalizes, encodes)
- Trains 8 different ML models
- Evaluates all models with comprehensive metrics
- Saves the best-performing model
- Visualizes model performance
"""

import os
import warnings
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# Try to import XGBoost, but make it optional
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Warning: XGBoost not available. Install with: pip install xgboost")

warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class SoftwareDefectDetector:
    """Main class for software defect detection using multiple ML models."""
    
    def __init__(self, dataset_path: str, target_column: str = None):
        """
        Initialize the detector.
        
        Args:
            dataset_path: Path to the CSV dataset
            target_column: Name of the target column (auto-detected if None)
        """
        self.dataset_path = dataset_path
        self.target_column = target_column
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.best_score = 0
        
    def load_data(self) -> pd.DataFrame:
        """Load the dataset from CSV file."""
        print(f"\n{'='*60}")
        print(f"Loading dataset: {self.dataset_path}")
        print(f"{'='*60}")
        
        try:
            df = pd.read_csv(self.dataset_path)
            print(f"Dataset loaded successfully!")
            print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"\nFirst few rows:")
            print(df.head())
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found at: {self.dataset_path}")
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")
    
    def detect_target_column(self, df: pd.DataFrame) -> str:
        """Auto-detect the target column name."""
        # Common target column names
        possible_targets = ['label', 'defects', 'defect', 'target', 'class', 'bug']
        
        for col in possible_targets:
            if col in df.columns:
                return col
        
        # If not found, check last column
        if self.target_column is None:
            print(f"\nWarning: Could not auto-detect target column.")
            print(f"Available columns: {list(df.columns)}")
            print(f"Using last column as target: {df.columns[-1]}")
            return df.columns[-1]
        
        return self.target_column
    
    def preprocess_data(self, df: pd.DataFrame) -> tuple:
        """
        Preprocess the dataset.
        
        Returns:
            X: Features (numpy array)
            y: Target labels (numpy array)
            feature_names: List of feature names
        """
        print(f"\n{'='*60}")
        print("PREPROCESSING DATA")
        print(f"{'='*60}")
        
        # Detect target column
        target_col = self.detect_target_column(df)
        print(f"Target column: {target_col}")
        
        # Separate features and target
        X = df.drop(columns=[target_col]).copy()
        y = df[target_col].copy()
        
        print(f"\nOriginal data shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        
        # Handle missing values
        print(f"\n1. Handling missing values...")
        missing_before = X.isnull().sum().sum()
        if missing_before > 0:
            print(f"   Found {missing_before} missing values")
            # Fill numeric columns with median
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                X[col].fillna(X[col].median(), inplace=True)
            # Fill categorical columns with mode
            categorical_cols = X.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                X[col].fillna(X[col].mode()[0] if len(X[col].mode()) > 0 else 'unknown', inplace=True)
            print(f"   Missing values filled")
        else:
            print(f"   No missing values found")
        
        # Encode categorical features
        print(f"\n2. Encoding categorical features...")
        categorical_cols = X.select_dtypes(include=['object', 'bool']).columns.tolist()
        feature_names = []
        
        for col in X.columns:
            if col in categorical_cols:
                # One-hot encode categorical columns
                dummies = pd.get_dummies(X[col], prefix=col, drop_first=True)
                X = pd.concat([X.drop(columns=[col]), dummies], axis=1)
                feature_names.extend(dummies.columns.tolist())
                print(f"   Encoded '{col}' -> {len(dummies.columns)} binary features")
            else:
                feature_names.append(col)
        
        # Encode target variable if needed
        print(f"\n3. Encoding target variable...")
        if y.dtype == 'object' or y.dtype == 'bool':
            # Convert boolean/string to numeric
            if y.dtype == 'bool':
                y = y.astype(int)
            else:
                # Handle string booleans (true/false, True/False)
                y_str = y.astype(str).str.lower()
                if set(y_str.unique()).issubset({'true', 'false', '1', '0', 'yes', 'no'}):
                    # Map common boolean strings
                    y = y_str.map({'true': 1, 'false': 0, '1': 1, '0': 0, 'yes': 1, 'no': 0}).astype(int)
                else:
                    # Use label encoder for other categorical values
                    y = self.label_encoder.fit_transform(y)
            print(f"   Target encoded: {np.unique(y)}")
        else:
            y = y.astype(int)
            print(f"   Target already numeric: {np.unique(y)}")
        
        # Normalize/scale numeric features
        print(f"\n4. Normalizing numeric features...")
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=feature_names)
        
        print(f"   Features normalized using StandardScaler")
        print(f"   Final feature shape: {X_scaled.shape}")
        
        return X_scaled.values, y.values, feature_names
    
    def initialize_models(self):
        """Initialize all ML models."""
        print(f"\n{'='*60}")
        print("INITIALIZING MODELS")
        print(f"{'='*60}")
        
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Naive Bayes': GaussianNB(),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42, kernel='rbf')
        }
        
        # Add XGBoost if available
        if XGBOOST_AVAILABLE:
            self.models['XGBoost'] = xgb.XGBClassifier(
                n_estimators=100,
                random_state=42,
                eval_metric='logloss',
                use_label_encoder=False
            )
        else:
            print("   XGBoost skipped (not installed)")
        
        print(f"\nInitialized {len(self.models)} models:")
        for name in self.models.keys():
            print(f"   - {name}")
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """Train all models and evaluate their performance."""
        print(f"\n{'='*60}")
        print("TRAINING AND EVALUATING MODELS")
        print(f"{'='*60}")
        
        self.results = {}
        
        for name, model in self.models.items():
            print(f"\n{'─'*60}")
            print(f"Training: {name}")
            print(f"{'─'*60}")
            
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Predictions
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                
                # ROC-AUC (only if binary classification and probabilities available)
                try:
                    if y_pred_proba is not None and len(np.unique(y_test)) == 2:
                        roc_auc = roc_auc_score(y_test, y_pred_proba)
                    else:
                        roc_auc = None
                except:
                    roc_auc = None
                
                # Confusion matrix
                cm = confusion_matrix(y_test, y_pred)
                
                # Store results
                self.results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'roc_auc': roc_auc,
                    'confusion_matrix': cm,
                    'predictions': y_pred
                }
                
                # Update best model (based on F1 score)
                if f1 > self.best_score:
                    self.best_score = f1
                    self.best_model = model
                    self.best_model_name = name
                
                print(f"   [OK] Accuracy:  {accuracy:.4f}")
                print(f"   [OK] Precision: {precision:.4f}")
                print(f"   [OK] Recall:    {recall:.4f}")
                print(f"   [OK] F1 Score:  {f1:.4f}")
                if roc_auc is not None:
                    print(f"   [OK] ROC-AUC:   {roc_auc:.4f}")
                
            except Exception as e:
                print(f"   [ERROR] Error training {name}: {str(e)}")
                continue
        
        print(f"\n{'='*60}")
        print("TRAINING COMPLETE")
        print(f"{'='*60}")
    
    def print_results_table(self):
        """Print all results in a tabular format."""
        print(f"\n{'='*80}")
        print("MODEL PERFORMANCE COMPARISON")
        print(f"{'='*80}")
        
        # Create results DataFrame
        data = []
        for name, metrics in self.results.items():
            row = {
                'Model': name,
                'Accuracy': f"{metrics['accuracy']:.4f}",
                'Precision': f"{metrics['precision']:.4f}",
                'Recall': f"{metrics['recall']:.4f}",
                'F1 Score': f"{metrics['f1_score']:.4f}",
                'ROC-AUC': f"{metrics['roc_auc']:.4f}" if metrics['roc_auc'] is not None else "N/A"
            }
            data.append(row)
        
        df_results = pd.DataFrame(data)
        print("\n" + df_results.to_string(index=False))
        
        # Print confusion matrices
        print(f"\n{'='*80}")
        print("CONFUSION MATRICES")
        print(f"{'='*80}")
        
        for name, metrics in self.results.items():
            print(f"\n{name}:")
            print(metrics['confusion_matrix'])
    
    def visualize_results(self, save_path: str = None):
        """Create visualizations of model performance."""
        print(f"\n{'='*60}")
        print("CREATING VISUALIZATIONS")
        print(f"{'='*60}")
        
        if not self.results:
            print("No results to visualize.")
            return
        
        # Prepare data for plotting
        models = list(self.results.keys())
        accuracies = [self.results[m]['accuracy'] for m in models]
        f1_scores = [self.results[m]['f1_score'] for m in models]
        precisions = [self.results[m]['precision'] for m in models]
        recalls = [self.results[m]['recall'] for m in models]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        # Accuracy comparison
        axes[0, 0].barh(models, accuracies, color='steelblue')
        axes[0, 0].set_xlabel('Accuracy', fontsize=12)
        axes[0, 0].set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlim([0, 1])
        axes[0, 0].grid(axis='x', alpha=0.3)
        
        # F1 Score comparison
        axes[0, 1].barh(models, f1_scores, color='coral')
        axes[0, 1].set_xlabel('F1 Score', fontsize=12)
        axes[0, 1].set_title('F1 Score Comparison', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlim([0, 1])
        axes[0, 1].grid(axis='x', alpha=0.3)
        
        # Precision comparison
        axes[1, 0].barh(models, precisions, color='mediumseagreen')
        axes[1, 0].set_xlabel('Precision', fontsize=12)
        axes[1, 0].set_title('Precision Comparison', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlim([0, 1])
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # Recall comparison
        axes[1, 1].barh(models, recalls, color='gold')
        axes[1, 1].set_xlabel('Recall', fontsize=12)
        axes[1, 1].set_title('Recall Comparison', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlim([0, 1])
        axes[1, 1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"   Visualization saved to: {save_path}")
        else:
            plt.savefig('model_performance.png', dpi=300, bbox_inches='tight')
            print(f"   Visualization saved to: model_performance.png")
        
        plt.close()
        print("   [OK] Visualizations created successfully")
    
    def save_best_model(self, save_path: str = None):
        """Save the best-performing model."""
        if self.best_model is None:
            print("No model to save.")
            return
        
        if save_path is None:
            save_path = 'best_defect_model.joblib'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        
        # Save model, scaler, and metadata
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'model_name': self.best_model_name,
            'metrics': self.results[self.best_model_name]
        }
        
        joblib.dump(model_data, save_path)
        print(f"\n{'='*60}")
        print(f"BEST MODEL SAVED")
        print(f"{'='*60}")
        print(f"Model: {self.best_model_name}")
        print(f"Path: {save_path}")
        print(f"F1 Score: {self.best_score:.4f}")
        print(f"Accuracy: {self.results[self.best_model_name]['accuracy']:.4f}")
    
    def print_best_model_summary(self):
        """Print summary of the best-performing model."""
        if self.best_model_name is None:
            return
        
        print(f"\n{'='*80}")
        print("BEST MODEL SUMMARY")
        print(f"{'='*80}")
        print(f"\n[WINNER] Best Model: {self.best_model_name}")
        print(f"\nPerformance Metrics:")
        metrics = self.results[self.best_model_name]
        print(f"   • Accuracy:  {metrics['accuracy']:.4f}")
        print(f"   • Precision: {metrics['precision']:.4f}")
        print(f"   • Recall:    {metrics['recall']:.4f}")
        print(f"   • F1 Score:  {metrics['f1_score']:.4f}")
        if metrics['roc_auc'] is not None:
            print(f"   • ROC-AUC:   {metrics['roc_auc']:.4f}")
        
        print(f"\nConfusion Matrix:")
        print(metrics['confusion_matrix'])
        print(f"\n{'='*80}\n")


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("SOFTWARE DEFECT DETECTION - MACHINE LEARNING PIPELINE")
    print("="*80)
    
    # Configuration
    # You can change this to any dataset in the datasets folder
    dataset_path = os.path.join('datasets', 'sample.csv')
    
    # Check if dataset exists, if not try other datasets
    if not os.path.exists(dataset_path):
        # Try to find any CSV in datasets folder
        datasets_dir = 'datasets'
        if os.path.exists(datasets_dir):
            csv_files = [f for f in os.listdir(datasets_dir) if f.endswith('.csv')]
            if csv_files:
                dataset_path = os.path.join(datasets_dir, csv_files[0])
                print(f"Using dataset: {dataset_path}")
            else:
                raise FileNotFoundError("No CSV files found in datasets folder")
        else:
            raise FileNotFoundError("Datasets folder not found")
    
    # Initialize detector
    detector = SoftwareDefectDetector(dataset_path)
    
    # Load data
    df = detector.load_data()
    
    # Preprocess data
    X, y, feature_names = detector.preprocess_data(df)
    
    # Split data (80/20)
    print(f"\n{'='*60}")
    print("SPLITTING DATA")
    print(f"{'='*60}")
    
    # Use stratify only if we have enough samples per class
    unique_labels = np.unique(y)
    if len(unique_labels) >= 2:
        value_counts = pd.Series(y).value_counts()
        can_stratify = len(y) >= 20 and len(value_counts) >= 2 and all(value_counts >= 2)
        stratify_param = y if can_stratify else None
        if stratify_param is None:
            print("Warning: Using non-stratified split (dataset too small or imbalanced)")
    else:
        stratify_param = None
        print("Warning: Using non-stratified split (only one class found)")
    
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=stratify_param
        )
    except ValueError as e:
        # If stratify fails, try without it
        print(f"Warning: Stratified split failed: {e}. Using non-stratified split.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=None
        )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Initialize models
    detector.initialize_models()
    
    # Train and evaluate
    detector.train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Print results
    detector.print_results_table()
    
    # Create visualizations
    detector.visualize_results('model_performance.png')
    
    # Save best model
    model_dir = 'model'
    os.makedirs(model_dir, exist_ok=True)
    detector.save_best_model(os.path.join(model_dir, 'best_defect_model.joblib'))
    
    # Print best model summary
    detector.print_best_model_summary()
    
    print("\n" + "="*80)
    print("PIPELINE COMPLETE!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

