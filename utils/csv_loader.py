"""
CSV Data Loader Utility
Loads and parses CSV test data for automated test generation.
"""

import csv
import os
from typing import List, Dict, Any


class CSVDataLoader:
    """Loads test data from CSV files."""

    @staticmethod
    def load_csv(filepath: str) -> List[Dict[str, Any]]:
        """
        Load CSV file and return list of dictionaries.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of dictionaries with CSV data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        data = []
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        
        return data

    @staticmethod
    def load_test_cases_by_module(filepath: str, module: str) -> List[Dict[str, Any]]:
        """
        Load test cases filtered by module.
        
        Args:
            filepath: Path to CSV file
            module: Module name to filter (e.g., 'Login')
            
        Returns:
            List of test cases for the specified module
        """
        all_data = CSVDataLoader.load_csv(filepath)
        return [row for row in all_data if row.get('Module') == module]

    @staticmethod
    def load_test_cases_by_priority(filepath: str, priority: str) -> List[Dict[str, Any]]:
        """
        Load test cases filtered by priority.
        
        Args:
            filepath: Path to CSV file
            priority: Priority level (e.g., 'High', 'Medium', 'Low')
            
        Returns:
            List of test cases with specified priority
        """
        all_data = CSVDataLoader.load_csv(filepath)
        return [row for row in all_data if row.get('Priority') == priority]

    @staticmethod
    def load_test_cases_by_type(filepath: str, test_type: str) -> List[Dict[str, Any]]:
        """
        Load test cases filtered by test type.
        
        Args:
            filepath: Path to CSV file
            test_type: Test type (e.g., 'Positive', 'Negative')
            
        Returns:
            List of test cases with specified type
        """
        all_data = CSVDataLoader.load_csv(filepath)
        return [row for row in all_data if row.get('Test Type') == test_type]

    @staticmethod
    def load_automatable_tests(filepath: str) -> List[Dict[str, Any]]:
        """
        Load only automatable test cases.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of automatable test cases
        """
        all_data = CSVDataLoader.load_csv(filepath)
        return [row for row in all_data if row.get('Automatable').lower() == 'yes']

    @staticmethod
    def get_test_data_by_id(filepath: str, tc_id: str) -> Dict[str, Any]:
        """
        Get specific test case by ID.
        
        Args:
            filepath: Path to CSV file
            tc_id: Test Case ID
            
        Returns:
            Test case data dictionary
            
        Raises:
            ValueError: If test case ID not found
        """
        all_data = CSVDataLoader.load_csv(filepath)
        for row in all_data:
            if row.get('TC_ID') == tc_id:
                return row
        raise ValueError(f"Test case {tc_id} not found in {filepath}")

    @staticmethod
    def get_statistics(filepath: str) -> Dict[str, Any]:
        """
        Get statistics about the CSV test data.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Dictionary with statistics
        """
        all_data = CSVDataLoader.load_csv(filepath)
        
        modules = {}
        priorities = {}
        test_types = {}
        automatable_count = 0
        
        for row in all_data:
            module = row.get('Module')
            priority = row.get('Priority')
            test_type = row.get('Test Type')
            automatable = row.get('Automatable', '').lower() == 'yes'
            
            modules[module] = modules.get(module, 0) + 1
            priorities[priority] = priorities.get(priority, 0) + 1
            test_types[test_type] = test_types.get(test_type, 0) + 1
            
            if automatable:
                automatable_count += 1
        
        return {
            'total_tests': len(all_data),
            'automatable': automatable_count,
            'by_module': modules,
            'by_priority': priorities,
            'by_type': test_types,
        }

    @staticmethod
    def print_statistics(filepath: str) -> None:
        """
        Print statistics about the CSV test data.
        
        Args:
            filepath: Path to CSV file
        """
        stats = CSVDataLoader.get_statistics(filepath)
        
        print("\n" + "="*50)
        print("CSV TEST DATA STATISTICS")
        print("="*50)
        print(f"Total Tests:        {stats['total_tests']}")
        print(f"Automatable:        {stats['automatable']}")
        print(f"\nBy Module:")
        for module, count in stats['by_module'].items():
            print(f"  {module}: {count}")
        print(f"\nBy Priority:")
        for priority, count in stats['by_priority'].items():
            print(f"  {priority}: {count}")
        print(f"\nBy Type:")
        for test_type, count in stats['by_type'].items():
            print(f"  {test_type}: {count}")
        print("="*50 + "\n")
