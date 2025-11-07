"""
Intervention Recommendation Engine
Generates personalized intervention strategies based on risk predictions and SHAP analysis
"""

import pandas as pd
import numpy as np
import pickle
from typing import Dict, List, Tuple

class InterventionRecommendationEngine:
    """
    AI-powered recommendation engine that generates personalized intervention strategies
    based on student risk level and contributing factors identified through SHAP analysis
    """
    
    def __init__(self, feature_importance_path='outputs/feature_importance.csv'):
        """Initialize the recommendation engine"""
        # Load feature importance from SHAP analysis
        self.feature_importance = pd.read_csv(feature_importance_path)
        
        # Define intervention strategies for each risk factor
        self.intervention_strategies = self._define_intervention_strategies()
        
    def _define_intervention_strategies(self) -> Dict:
        """Define comprehensive intervention strategies for different risk factors"""
        return {
            # Academic Performance Factors
            'midterm_score': {
                'low': {
                    'title': 'Academic Performance Support',
                    'interventions': [
                        'Schedule immediate one-on-one tutoring sessions',
                        'Enroll in supplemental instruction programs',
                        'Provide access to past exam materials and practice tests',
                        'Connect with peer study groups',
                        'Arrange weekly check-ins with academic advisor'
                    ],
                    'priority': 'CRITICAL',
                    'timeline': 'Immediate (within 1 week)'
                },
                'medium': {
                    'title': 'Academic Enhancement',
                    'interventions': [
                        'Recommend office hours attendance',
                        'Provide study skills workshops',
                        'Share additional learning resources'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Short-term (1-2 weeks)'
                }
            },
            
            'cumulative_gpa': {
                'low': {
                    'title': 'GPA Recovery Plan',
                    'interventions': [
                        'Create personalized academic recovery plan',
                        'Consider course load reduction',
                        'Explore grade replacement options',
                        'Connect with academic success coach',
                        'Evaluate major/career fit'
                    ],
                    'priority': 'CRITICAL',
                    'timeline': 'Immediate'
                }
            },
            
            # Engagement Factors
            'lms_hours_per_week': {
                'low': {
                    'title': 'Digital Engagement Improvement',
                    'interventions': [
                        'Send personalized LMS engagement reminders',
                        'Provide LMS navigation tutorial',
                        'Highlight important course materials',
                        'Enable mobile app notifications',
                        'Schedule virtual office hours'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Immediate'
                }
            },
            
            'attendance_rate': {
                'low': {
                    'title': 'Attendance Intervention',
                    'interventions': [
                        'Investigate barriers to attendance (health, transportation, work)',
                        'Provide flexible attendance options if available',
                        'Connect with student support services',
                        'Implement attendance accountability system',
                        'Offer recorded lectures if possible'
                    ],
                    'priority': 'CRITICAL',
                    'timeline': 'Immediate'
                }
            },
            
            'total_absences': {
                'high': {
                    'title': 'Absence Reduction Strategy',
                    'interventions': [
                        'Meet with student to understand absence reasons',
                        'Connect with counseling services if needed',
                        'Provide catch-up materials and support',
                        'Create attendance improvement contract',
                        'Monitor weekly attendance progress'
                    ],
                    'priority': 'CRITICAL',
                    'timeline': 'Immediate'
                }
            },
            
            'assignments_on_time': {
                'low': {
                    'title': 'Time Management Support',
                    'interventions': [
                        'Provide time management workshop',
                        'Help create assignment calendar',
                        'Teach prioritization techniques',
                        'Offer deadline extension guidance',
                        'Connect with writing center for support'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Short-term (1-2 weeks)'
                }
            },
            
            # Wellness Factors
            'stress_level': {
                'high': {
                    'title': 'Stress Management Program',
                    'interventions': [
                        'Refer to counseling services',
                        'Provide stress management workshops',
                        'Teach mindfulness and relaxation techniques',
                        'Evaluate course load and commitments',
                        'Connect with wellness center resources'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Immediate'
                }
            },
            
            'avg_sleep_hours': {
                'low': {
                    'title': 'Sleep and Wellness Support',
                    'interventions': [
                        'Provide sleep hygiene education',
                        'Evaluate schedule for overcommitment',
                        'Refer to health services if needed',
                        'Discuss time management strategies',
                        'Share wellness resources'
                    ],
                    'priority': 'MEDIUM',
                    'timeline': 'Short-term (1-2 weeks)'
                }
            },
            
            # Resource Access
            'has_internet_at_home': {
                'no': {
                    'title': 'Technology Access Support',
                    'interventions': [
                        'Provide information on campus computer labs',
                        'Explore internet subsidy programs',
                        'Offer offline course materials',
                        'Arrange library study space access',
                        'Connect with technology lending programs'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Immediate'
                }
            },
            
            'has_study_space': {
                'no': {
                    'title': 'Study Environment Support',
                    'interventions': [
                        'Reserve dedicated library study space',
                        'Provide campus study room access',
                        'Share quiet study location information',
                        'Offer extended library hours information'
                    ],
                    'priority': 'MEDIUM',
                    'timeline': 'Immediate'
                }
            },
            
            # Financial Factors
            'work_hours_per_week': {
                'high': {
                    'title': 'Work-Life Balance Support',
                    'interventions': [
                        'Discuss financial aid options',
                        'Explore on-campus employment opportunities',
                        'Consider course load adjustment',
                        'Connect with financial aid office',
                        'Provide time management strategies for working students'
                    ],
                    'priority': 'MEDIUM',
                    'timeline': 'Short-term (2-4 weeks)'
                }
            },
            
            'financial_stress': {
                'high': {
                    'title': 'Financial Support Services',
                    'interventions': [
                        'Connect with financial aid counselor',
                        'Explore emergency grant programs',
                        'Provide information on food pantry/basic needs',
                        'Discuss scholarship opportunities',
                        'Refer to financial literacy workshops'
                    ],
                    'priority': 'HIGH',
                    'timeline': 'Immediate'
                }
            }
        }
    
    def generate_recommendations(self, 
                                student_data: Dict, 
                                risk_prediction: str,
                                risk_probabilities: np.ndarray,
                                top_n_factors: int = 5) -> Dict:
        """
        Generate personalized intervention recommendations
        
        Args:
            student_data: Dictionary of student features
            risk_prediction: Predicted risk level ('High Risk', 'Medium Risk', 'Low Risk')
            risk_probabilities: Array of probabilities for each risk level
            top_n_factors: Number of top contributing factors to address
            
        Returns:
            Dictionary containing recommendations and action plan
        """
        
        # Get top contributing factors from feature importance
        top_factors = self.feature_importance.head(top_n_factors)
        
        recommendations = {
            'student_id': student_data.get('student_id', 'Unknown'),
            'risk_level': risk_prediction,
            'risk_probability': float(max(risk_probabilities)),
            'confidence': self._calculate_confidence(risk_probabilities),
            'priority_interventions': [],
            'supporting_interventions': [],
            'action_plan': [],
            'follow_up_timeline': self._determine_follow_up(risk_prediction)
        }
        
        # Generate interventions based on top factors and student data
        for _, row in top_factors.iterrows():
            feature = row['feature']
            importance = row['importance']
            
            if feature in student_data:
                intervention = self._get_intervention_for_feature(
                    feature, 
                    student_data[feature],
                    importance
                )
                
                if intervention:
                    if intervention['priority'] in ['CRITICAL', 'HIGH']:
                        recommendations['priority_interventions'].append(intervention)
                    else:
                        recommendations['supporting_interventions'].append(intervention)
        
        # Create action plan
        recommendations['action_plan'] = self._create_action_plan(
            risk_prediction,
            recommendations['priority_interventions'],
            recommendations['supporting_interventions']
        )
        
        return recommendations
    
    def _get_intervention_for_feature(self, feature: str, value, importance: float) -> Dict:
        """Get appropriate intervention based on feature value"""
        
        if feature not in self.intervention_strategies:
            return None
        
        strategies = self.intervention_strategies[feature]
        
        # Determine which strategy to use based on value
        if isinstance(value, (int, float)):
            # Numeric features
            if 'low' in strategies and value < 50:  # Threshold for "low"
                strategy = strategies['low']
            elif 'high' in strategies and value > 75:  # Threshold for "high"
                strategy = strategies['high']
            elif 'medium' in strategies:
                strategy = strategies['medium']
            else:
                return None
        else:
            # Categorical features
            value_str = str(value).lower()
            if value_str in strategies:
                strategy = strategies[value_str]
            else:
                return None
        
        return {
            'factor': feature,
            'current_value': value,
            'importance_score': float(importance),
            **strategy
        }
    
    def _calculate_confidence(self, probabilities: np.ndarray) -> str:
        """Calculate confidence level based on probability distribution"""
        max_prob = max(probabilities)
        if max_prob > 0.8:
            return 'Very High'
        elif max_prob > 0.6:
            return 'High'
        elif max_prob > 0.4:
            return 'Medium'
        else:
            return 'Low'
    
    def _determine_follow_up(self, risk_level: str) -> str:
        """Determine follow-up timeline based on risk level"""
        if risk_level == 'High Risk':
            return 'Weekly check-ins for 4 weeks, then bi-weekly'
        elif risk_level == 'Medium Risk':
            return 'Bi-weekly check-ins for 6 weeks'
        else:
            return 'Monthly check-ins'
    
    def _create_action_plan(self, risk_level: str, priority_interventions: List, 
                           supporting_interventions: List) -> List[Dict]:
        """Create a structured action plan"""
        action_plan = []
        
        # Week 1 actions
        week1_actions = []
        for intervention in priority_interventions[:2]:  # Top 2 priority items
            week1_actions.extend(intervention['interventions'][:2])  # First 2 interventions
        
        if week1_actions:
            action_plan.append({
                'timeframe': 'Week 1 (Immediate)',
                'actions': week1_actions,
                'goal': 'Address most critical risk factors'
            })
        
        # Week 2-4 actions
        week2_4_actions = []
        for intervention in priority_interventions[2:] + supporting_interventions[:2]:
            if 'interventions' in intervention:
                week2_4_actions.extend(intervention['interventions'][:1])
        
        if week2_4_actions:
            action_plan.append({
                'timeframe': 'Weeks 2-4',
                'actions': week2_4_actions,
                'goal': 'Build sustainable support systems'
            })
        
        # Ongoing actions
        action_plan.append({
            'timeframe': 'Ongoing',
            'actions': [
                'Monitor academic progress weekly',
                'Track intervention effectiveness',
                'Adjust strategies as needed',
                'Maintain regular communication'
            ],
            'goal': 'Ensure continuous improvement'
        })
        
        return action_plan

