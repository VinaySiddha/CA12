"""
Data utilities for processing and transforming data
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)


class DataUtils:
    @staticmethod
    def normalize_scores(scores: List[float], min_val: float = 0.0, max_val: float = 1.0) -> List[float]:
        """Normalize scores to a specified range"""
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if min_score == max_score:
            return [0.5] * len(scores)  # All scores are the same
        
        normalized = []
        for score in scores:
            normalized_score = (score - min_score) / (max_score - min_score)
            scaled_score = min_val + normalized_score * (max_val - min_val)
            normalized.append(scaled_score)
        
        return normalized
    
    @staticmethod
    def calculate_weighted_average(values: List[float], weights: List[float]) -> float:
        """Calculate weighted average of values"""
        if not values or not weights or len(values) != len(weights):
            return 0.0
        
        if sum(weights) == 0:
            return sum(values) / len(values)  # Simple average if no weights
        
        weighted_sum = sum(v * w for v, w in zip(values, weights))
        return weighted_sum / sum(weights)
    
    @staticmethod
    def calculate_similarity_matrix(data: List[List[float]]) -> List[List[float]]:
        """Calculate similarity matrix using cosine similarity"""
        if not data:
            return []
        
        from sklearn.metrics.pairwise import cosine_similarity
        
        try:
            similarity_matrix = cosine_similarity(data)
            return similarity_matrix.tolist()
        except Exception as e:
            logger.error(f"Error calculating similarity matrix: {e}")
            return []
    
    @staticmethod
    def group_by_field(data: List[Dict], field: str) -> Dict[Any, List[Dict]]:
        """Group data by a specific field"""
        grouped = {}
        
        for item in data:
            key = item.get(field)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        
        return grouped
    
    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0
        
        return np.percentile(values, percentile)
    
    @staticmethod
    def detect_outliers(values: List[float], method: str = "iqr") -> List[int]:
        """Detect outliers in data and return their indices"""
        if not values:
            return []
        
        values_array = np.array(values)
        outlier_indices = []
        
        if method == "iqr":
            Q1 = np.percentile(values_array, 25)
            Q3 = np.percentile(values_array, 75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_indices = [
                i for i, val in enumerate(values) 
                if val < lower_bound or val > upper_bound
            ]
        
        elif method == "zscore":
            mean_val = np.mean(values_array)
            std_val = np.std(values_array)
            
            if std_val > 0:
                z_scores = np.abs((values_array - mean_val) / std_val)
                outlier_indices = [i for i, z in enumerate(z_scores) if z > 3]
        
        return outlier_indices
    
    @staticmethod
    def smooth_time_series(values: List[float], window_size: int = 3) -> List[float]:
        """Apply moving average smoothing to time series data"""
        if not values or window_size <= 0:
            return values
        
        smoothed = []
        for i in range(len(values)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(values), i + window_size // 2 + 1)
            window_values = values[start_idx:end_idx]
            smoothed.append(sum(window_values) / len(window_values))
        
        return smoothed
    
    @staticmethod
    def calculate_trend(values: List[float]) -> Dict[str, Any]:
        """Calculate trend information for a series of values"""
        if len(values) < 2:
            return {"trend": "insufficient_data", "slope": 0, "correlation": 0}
        
        x = list(range(len(values)))
        
        # Calculate correlation coefficient
        correlation = np.corrcoef(x, values)[0, 1] if len(values) > 1 else 0
        
        # Calculate slope using linear regression
        if len(values) > 1:
            slope = np.polyfit(x, values, 1)[0]
        else:
            slope = 0
        
        # Determine trend direction
        if abs(correlation) < 0.1:
            trend = "stable"
        elif correlation > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        return {
            "trend": trend,
            "slope": float(slope),
            "correlation": float(correlation) if not np.isnan(correlation) else 0,
            "strength": "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.3 else "weak"
        }
    
    @staticmethod
    def aggregate_by_time_period(data: List[Dict], date_field: str, period: str = "day") -> Dict[str, List[Dict]]:
        """Aggregate data by time period"""
        aggregated = {}
        
        for item in data:
            date_value = item.get(date_field)
            if not date_value:
                continue
            
            # Convert to datetime if it's a string
            if isinstance(date_value, str):
                try:
                    date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                except:
                    continue
            
            # Create period key
            if period == "day":
                period_key = date_value.strftime("%Y-%m-%d")
            elif period == "week":
                period_key = date_value.strftime("%Y-W%U")
            elif period == "month":
                period_key = date_value.strftime("%Y-%m")
            elif period == "year":
                period_key = date_value.strftime("%Y")
            else:
                period_key = date_value.strftime("%Y-%m-%d")
            
            if period_key not in aggregated:
                aggregated[period_key] = []
            aggregated[period_key].append(item)
        
        return aggregated
    
    @staticmethod
    def calculate_statistics(values: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of values"""
        if not values:
            return {}
        
        values_array = np.array(values)
        
        return {
            "count": len(values),
            "mean": float(np.mean(values_array)),
            "median": float(np.median(values_array)),
            "std": float(np.std(values_array)),
            "min": float(np.min(values_array)),
            "max": float(np.max(values_array)),
            "q25": float(np.percentile(values_array, 25)),
            "q75": float(np.percentile(values_array, 75))
        }
    
    @staticmethod
    def encode_categorical_variables(data: List[Dict], categorical_fields: List[str]) -> Tuple[List[Dict], Dict[str, Dict]]:
        """Encode categorical variables to numerical values"""
        encoded_data = []
        encoding_mappings = {}
        
        # Create mappings for each categorical field
        for field in categorical_fields:
            unique_values = list(set(item.get(field) for item in data if item.get(field) is not None))
            encoding_mappings[field] = {val: idx for idx, val in enumerate(unique_values)}
        
        # Apply encodings
        for item in data:
            encoded_item = item.copy()
            for field in categorical_fields:
                if field in encoded_item and encoded_item[field] is not None:
                    encoded_item[field + "_encoded"] = encoding_mappings[field].get(encoded_item[field], -1)
            encoded_data.append(encoded_item)
        
        return encoded_data, encoding_mappings
    
    @staticmethod
    def fill_missing_values(data: List[Dict], field: str, method: str = "mean") -> List[Dict]:
        """Fill missing values in a specific field"""
        # Get non-null values
        non_null_values = [item[field] for item in data if field in item and item[field] is not None]
        
        if not non_null_values:
            return data
        
        # Calculate fill value
        if method == "mean":
            fill_value = sum(non_null_values) / len(non_null_values)
        elif method == "median":
            fill_value = np.median(non_null_values)
        elif method == "mode":
            from collections import Counter
            fill_value = Counter(non_null_values).most_common(1)[0][0]
        else:
            fill_value = 0
        
        # Fill missing values
        filled_data = []
        for item in data:
            filled_item = item.copy()
            if field not in filled_item or filled_item[field] is None:
                filled_item[field] = fill_value
            filled_data.append(filled_item)
        
        return filled_data
    
    @staticmethod
    def create_feature_matrix(data: List[Dict], feature_fields: List[str]) -> Tuple[np.ndarray, List[str]]:
        """Create feature matrix from data"""
        features = []
        valid_indices = []
        
        for i, item in enumerate(data):
            feature_vector = []
            valid = True
            
            for field in feature_fields:
                value = item.get(field)
                if value is None:
                    valid = False
                    break
                
                # Convert to float if possible
                try:
                    feature_vector.append(float(value))
                except:
                    valid = False
                    break
            
            if valid:
                features.append(feature_vector)
                valid_indices.append(i)
        
        return np.array(features), valid_indices
    
    @staticmethod
    def calculate_distance_matrix(points: List[List[float]], metric: str = "euclidean") -> List[List[float]]:
        """Calculate distance matrix between points"""
        if not points:
            return []
        
        from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_distances
        
        points_array = np.array(points)
        
        if metric == "euclidean":
            distances = euclidean_distances(points_array)
        elif metric == "manhattan":
            distances = manhattan_distances(points_array)
        elif metric == "cosine":
            distances = cosine_distances(points_array)
        else:
            distances = euclidean_distances(points_array)
        
        return distances.tolist()
    
    @staticmethod
    def sample_data(data: List[Dict], sample_size: int, method: str = "random") -> List[Dict]:
        """Sample data using specified method"""
        if sample_size >= len(data):
            return data
        
        if method == "random":
            import random
            return random.sample(data, sample_size)
        elif method == "systematic":
            step = len(data) // sample_size
            return [data[i * step] for i in range(sample_size)]
        else:
            return data[:sample_size]
    
    @staticmethod
    def validate_data_schema(data: List[Dict], required_fields: List[str]) -> Dict[str, Any]:
        """Validate data against required schema"""
        validation_results = {
            "valid": True,
            "errors": [],
            "missing_fields": [],
            "invalid_records": []
        }
        
        for i, record in enumerate(data):
            missing_in_record = [field for field in required_fields if field not in record]
            
            if missing_in_record:
                validation_results["valid"] = False
                validation_results["invalid_records"].append(i)
                validation_results["missing_fields"].extend(missing_in_record)
        
        # Remove duplicates
        validation_results["missing_fields"] = list(set(validation_results["missing_fields"]))
        
        if validation_results["missing_fields"]:
            validation_results["errors"].append(f"Missing required fields: {validation_results['missing_fields']}")
        
        return validation_results


# Global instance
data_utils = DataUtils()