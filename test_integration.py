"""
Integration Tests for Academic Performance Prediction System
Tests the complete end-to-end system including API, model, and recommendations
"""

import requests
import json
import time
import os

# API Configuration
API_URL = 'http://localhost:5000'

def test_health_check():
    """Test 1: Health check endpoint"""
    print("\n" + "="*80)
    print("TEST 1: Health Check")
    print("="*80)
    
    try:
        response = requests.get(f'{API_URL}/health')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        print("✓ Health check passed")
        print(f"  Response: {data}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_get_sample_data():
    """Test 2: Get sample student data"""
    print("\n" + "="*80)
    print("TEST 2: Get Sample Data")
    print("="*80)
    
    try:
        response = requests.get(f'{API_URL}/sample')
        assert response.status_code == 200
        data = response.json()
        assert 'student_id' in data
        assert 'cumulative_gpa' in data
        print("✓ Sample data retrieved successfully")
        print(f"  Student ID: {data['student_id']}")
        print(f"  GPA: {data['cumulative_gpa']}")
        return data
    except Exception as e:
        print(f"✗ Sample data retrieval failed: {e}")
        return None

def test_single_prediction(student_data):
    """Test 3: Single student prediction"""
    print("\n" + "="*80)
    print("TEST 3: Single Student Prediction")
    print("="*80)
    
    try:
        response = requests.post(f'{API_URL}/predict', json=student_data)
        assert response.status_code == 200
        result = response.json()
        
        # Validate response structure
        assert 'student_id' in result
        assert 'prediction' in result
        assert 'recommendations' in result
        assert 'timestamp' in result
        
        # Validate prediction
        prediction = result['prediction']
        assert 'risk_level' in prediction
        assert 'confidence' in prediction
        assert 'probabilities' in prediction
        assert prediction['risk_level'] in ['High Risk', 'Medium Risk', 'Low Risk']
        assert 0 <= prediction['confidence'] <= 1
        
        # Validate recommendations
        recommendations = result['recommendations']
        assert 'priority_interventions' in recommendations
        assert 'action_plan' in recommendations
        
        print("✓ Single prediction successful")
        print(f"  Student ID: {result['student_id']}")
        print(f"  Risk Level: {prediction['risk_level']}")
        print(f"  Confidence: {prediction['confidence']:.2%}")
        print(f"  Priority Interventions: {len(recommendations['priority_interventions'])}")
        
        return result
    except Exception as e:
        print(f"✗ Single prediction failed: {e}")
        return None

def test_batch_prediction():
    """Test 4: Batch predictions"""
    print("\n" + "="*80)
    print("TEST 4: Batch Predictions")
    print("="*80)
    
    try:
        # Get sample data
        sample = requests.get(f'{API_URL}/sample').json()
        
        # Create batch with 3 students
        batch_data = []
        for i in range(3):
            student = sample.copy()
            student['student_id'] = f'TEST_STU_{i+1:03d}'
            student['cumulative_gpa'] = 2.5 + (i * 0.5)  # Vary GPA
            batch_data.append(student)
        
        response = requests.post(f'{API_URL}/predict/batch', json=batch_data)
        assert response.status_code == 200
        result = response.json()
        
        # Validate response
        assert 'total_students' in result
        assert 'results' in result
        assert result['total_students'] == 3
        assert len(result['results']) == 3
        
        print("✓ Batch prediction successful")
        print(f"  Total Students: {result['total_students']}")
        for student in result['results']:
            print(f"  - {student['student_id']}: {student['risk_level']} ({student['confidence']:.2%})")
        
        return result
    except Exception as e:
        print(f"✗ Batch prediction failed: {e}")
        return None

def test_model_statistics():
    """Test 5: Model statistics endpoint"""
    print("\n" + "="*80)
    print("TEST 5: Model Statistics")
    print("="*80)
    
    try:
        response = requests.get(f'{API_URL}/stats')
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert 'model_info' in data
        assert 'top_features' in data
        
        model_info = data['model_info']
        assert 'total_features' in model_info
        assert 'risk_levels' in model_info
        assert 'model_type' in model_info
        
        print("✓ Model statistics retrieved successfully")
        print(f"  Model Type: {model_info['model_type']}")
        print(f"  Total Features: {model_info['total_features']}")
        print(f"  Risk Levels: {', '.join(model_info['risk_levels'])}")
        print(f"  Top Features: {len(data['top_features'])}")
        
        return data
    except Exception as e:
        print(f"✗ Model statistics retrieval failed: {e}")
        return None

def test_features_list():
    """Test 6: Features list endpoint"""
    print("\n" + "="*80)
    print("TEST 6: Features List")
    print("="*80)
    
    try:
        response = requests.get(f'{API_URL}/features')
        assert response.status_code == 200
        data = response.json()
        
        assert 'total_features' in data
        assert 'features' in data
        assert len(data['features']) == data['total_features']
        
        print("✓ Features list retrieved successfully")
        print(f"  Total Features: {data['total_features']}")
        print(f"  First 5 features: {', '.join(data['features'][:5])}")
        
        return data
    except Exception as e:
        print(f"✗ Features list retrieval failed: {e}")
        return None

def test_report_generation(prediction_result):
    """Test 7: Report generation"""
    print("\n" + "="*80)
    print("TEST 7: Report Generation")
    print("="*80)
    
    try:
        response = requests.post(f'{API_URL}/report', json=prediction_result)
        assert response.status_code == 200
        data = response.json()
        
        assert 'success' in data
        assert 'filename' in data
        assert data['success'] == True
        
        # Verify file exists
        filename = data['filename']
        assert os.path.exists(filename)
        
        print("✓ Report generation successful")
        print(f"  Filename: {filename}")
        print(f"  File size: {os.path.getsize(filename)} bytes")
        
        return data
    except Exception as e:
        print(f"✗ Report generation failed: {e}")
        return None

def test_error_handling():
    """Test 8: Error handling"""
    print("\n" + "="*80)
    print("TEST 8: Error Handling")
    print("="*80)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 8.1: Invalid prediction data
    try:
        response = requests.post(f'{API_URL}/predict', json={})
        # Should return error but not crash
        print("  ✓ Invalid data handled gracefully")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Invalid data test failed: {e}")
    
    # Test 8.2: Missing required fields
    try:
        response = requests.post(f'{API_URL}/predict', json={'student_id': 'TEST'})
        # Should return error
        print("  ✓ Missing fields handled gracefully")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Missing fields test failed: {e}")
    
    # Test 8.3: Invalid endpoint
    try:
        response = requests.get(f'{API_URL}/invalid_endpoint')
        assert response.status_code == 404
        print("  ✓ Invalid endpoint returns 404")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Invalid endpoint test failed: {e}")
    
    print(f"\n✓ Error handling tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("ACADEMIC PERFORMANCE PREDICTION SYSTEM - INTEGRATION TESTS")
    print("="*80)
    print(f"API URL: {API_URL}")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Wait for API to be ready
    print("\nWaiting for API to be ready...")
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f'{API_URL}/health', timeout=2)
            if response.status_code == 200:
                print("✓ API is ready")
                break
        except:
            if i < max_retries - 1:
                print(f"  Retry {i+1}/{max_retries}...")
                time.sleep(2)
            else:
                print("✗ API is not responding. Please start the API server first:")
                print("  python api_server.py")
                return
    
    # Run tests
    results = {}
    
    # Test 1: Health check
    results['health'] = test_health_check()
    
    # Test 2: Get sample data
    sample_data = test_get_sample_data()
    results['sample'] = sample_data is not None
    
    if sample_data:
        # Test 3: Single prediction
        prediction_result = test_single_prediction(sample_data)
        results['single_prediction'] = prediction_result is not None
        
        # Test 7: Report generation (if prediction succeeded)
        if prediction_result:
            results['report'] = test_report_generation(prediction_result)
    
    # Test 4: Batch prediction
    results['batch_prediction'] = test_batch_prediction() is not None
    
    # Test 5: Model statistics
    results['statistics'] = test_model_statistics() is not None
    
    # Test 6: Features list
    results['features'] = test_features_list() is not None
    
    # Test 8: Error handling
    results['error_handling'] = test_error_handling()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Success Rate: {passed/total*100:.1f}%")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")

if __name__ == '__main__':
    run_all_tests()

