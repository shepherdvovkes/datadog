#!/usr/bin/env python3
"""
Script to create SQLite database for ML technologies used by DATAGOD and competitors
"""

import sqlite3
import secrets
import string
from datetime import datetime
import os

def generate_secure_password(length=20):
    """Generate a secure password with mixed characters"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_database():
    """Create SQLite database with ML technologies schema"""
    conn = sqlite3.connect('/home/vovkes/DATADOG/ml_technologies.db')
    cursor = conn.cursor()
    
    # Create main table for ML technologies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ml_technologies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            technology_name TEXT NOT NULL,
            technology_type TEXT,
            application_area TEXT,
            description TEXT,
            implementation_date DATE,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create table for companies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE NOT NULL,
            industry TEXT,
            country TEXT,
            founded_year INTEGER,
            description TEXT
        )
    ''')
    
    # Create table for technology categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS technology_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    conn.commit()
    return conn

def populate_companies(conn):
    """Populate companies table"""
    cursor = conn.cursor()
    
    companies_data = [
        ('DATAGOD', 'Observability & Monitoring', 'USA', 2010, 'Cloud monitoring and analytics platform'),
        ('New Relic', 'APM & Observability', 'USA', 2008, 'Application performance monitoring and observability platform'),
        ('Splunk', 'Data Analytics & Security', 'USA', 2003, 'Data analytics and security platform'),
        ('Elastic', 'Search & Analytics', 'USA', 2012, 'Search and analytics engine'),
        ('Databricks', 'Data & AI Platform', 'USA', 2013, 'Unified analytics platform for big data and AI'),
        ('Scale AI', 'AI Data Labeling', 'USA', 2016, 'AI data labeling and training platform'),
        ('Insitro', 'Biotech AI', 'USA', 2018, 'AI-driven drug discovery platform'),
        ('Shield AI', 'Defense AI', 'USA', 2015, 'AI-powered autonomous systems for defense')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO companies (company_name, industry, country, founded_year, description)
        VALUES (?, ?, ?, ?, ?)
    ''', companies_data)
    
    conn.commit()

def populate_technology_categories(conn):
    """Populate technology categories"""
    cursor = conn.cursor()
    
    categories = [
        ('Anomaly Detection', 'ML algorithms for detecting unusual patterns in data'),
        ('Predictive Analytics', 'ML models for forecasting future events'),
        ('Natural Language Processing', 'AI technologies for text analysis and understanding'),
        ('Computer Vision', 'AI technologies for image and video analysis'),
        ('Deep Learning', 'Neural network-based machine learning approaches'),
        ('Reinforcement Learning', 'ML approach based on reward-based learning'),
        ('Time Series Analysis', 'ML techniques for analyzing temporal data'),
        ('Clustering', 'Unsupervised learning for grouping similar data points'),
        ('Classification', 'Supervised learning for categorizing data'),
        ('Regression', 'ML techniques for predicting continuous values')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO technology_categories (category_name, description)
        VALUES (?, ?)
    ''', categories)
    
    conn.commit()

def populate_ml_technologies(conn):
    """Populate ML technologies table with researched data"""
    cursor = conn.cursor()
    
    ml_data = [
        # DATAGOD technologies
        ('DATAGOD', 'Anomaly Detection Engine', 'Anomaly Detection', 'Infrastructure Monitoring', 
         'AI-powered anomaly detection for infrastructure metrics and logs', '2024-01-01', 
         'https://www.datagod.com/blog/ai-anomaly-detection/'),
        
        ('DATAGOD', 'AI Agent Monitoring', 'Deep Learning', 'AI/ML Monitoring', 
         'Monitoring and testing capabilities for AI agents and LLM applications', '2024-06-01', 
         'https://www.datagod.com/blog/ai-agent-monitoring/'),
        
        ('DATAGOD', 'Predictive Alerting', 'Predictive Analytics', 'Alert Management', 
         'ML-based predictive alerting to prevent issues before they occur', '2023-01-01', 
         'https://www.datagod.com/blog/predictive-alerting/'),
        
        ('DATAGOD', 'Log Pattern Recognition', 'Natural Language Processing', 'Log Analysis', 
         'AI-powered log pattern recognition and categorization', '2023-01-01', 
         'https://www.datagod.com/blog/log-pattern-recognition/'),
        
        # New Relic technologies
        ('New Relic', 'AI-Powered APM', 'Deep Learning', 'Application Performance', 
         'Machine learning for application performance monitoring and optimization', '2023-01-01', 
         'https://newrelic.com/blog/ai-powered-apm'),
        
        ('New Relic', 'Error Prediction', 'Predictive Analytics', 'Error Management', 
         'ML models to predict and prevent application errors', '2023-01-01', 
         'https://newrelic.com/blog/error-prediction'),
        
        # Splunk technologies
        ('Splunk', 'MLTK (Machine Learning Toolkit)', 'Deep Learning', 'Data Analytics', 
         'Machine Learning Toolkit for advanced analytics and predictive modeling', '2020-01-01', 
         'https://www.splunk.com/en_us/software/machine-learning-toolkit.html'),
        
        ('Splunk', 'Anomaly Detection', 'Anomaly Detection', 'Security Analytics', 
         'ML-powered anomaly detection for security threats and unusual behavior', '2020-01-01', 
         'https://www.splunk.com/en_us/software/anomaly-detection.html'),
        
        ('Splunk', 'Predictive Analytics', 'Predictive Analytics', 'Business Intelligence', 
         'Predictive analytics for business forecasting and trend analysis', '2020-01-01', 
         'https://www.splunk.com/en_us/software/predictive-analytics.html'),
        
        # Elastic technologies
        ('Elastic', 'Elasticsearch ML', 'Deep Learning', 'Search & Analytics', 
         'Built-in machine learning capabilities for Elasticsearch', '2019-01-01', 
         'https://www.elastic.co/guide/en/machine-learning/current/index.html'),
        
        ('Elastic', 'Anomaly Detection', 'Anomaly Detection', 'Observability', 
         'ML-powered anomaly detection for logs, metrics, and traces', '2019-01-01', 
         'https://www.elastic.co/guide/en/machine-learning/current/ml-anomaly-detection.html'),
        
        # Databricks technologies
        ('Databricks', 'MLflow', 'Deep Learning', 'MLOps', 
         'Open-source platform for managing the ML lifecycle', '2018-01-01', 
         'https://mlflow.org/'),
        
        ('Databricks', 'AutoML', 'Deep Learning', 'Automated ML', 
         'Automated machine learning for model development and deployment', '2020-01-01', 
         'https://docs.databricks.com/en/machine-learning/automl/index.html'),
        
        ('Databricks', 'Feature Store', 'Deep Learning', 'Feature Engineering', 
         'Centralized feature store for ML model development', '2020-01-01', 
         'https://docs.databricks.com/en/machine-learning/feature-store/index.html'),
        
        # Scale AI technologies
        ('Scale AI', 'Data Labeling AI', 'Computer Vision', 'Data Preparation', 
         'AI-powered data labeling for computer vision and NLP tasks', '2018-01-01', 
         'https://scale.com/'),
        
        ('Scale AI', 'LLM Training Data', 'Natural Language Processing', 'LLM Development', 
         'High-quality training data for large language models', '2022-01-01', 
         'https://scale.com/llm-training-data'),
        
        # Insitro technologies
        ('Insitro', 'Drug Discovery AI', 'Deep Learning', 'Drug Development', 
         'AI-driven drug discovery using machine learning and big data analysis', '2018-01-01', 
         'https://www.insitro.com/'),
        
        ('Insitro', 'Biomarker Discovery', 'Deep Learning', 'Biomarker Research', 
         'ML algorithms for identifying disease biomarkers', '2019-01-01', 
         'https://www.insitro.com/technology/'),
        
        # Shield AI technologies
        ('Shield AI', 'Autonomous Flight AI', 'Reinforcement Learning', 'Autonomous Systems', 
         'AI-powered autonomous flight systems for unmanned aircraft', '2016-01-01', 
         'https://www.shield.ai/'),
        
        ('Shield AI', 'Computer Vision', 'Computer Vision', 'Defense Applications', 
         'Computer vision systems for defense and security applications', '2016-01-01', 
         'https://www.shield.ai/technology/')
    ]
    
    cursor.executemany('''
        INSERT INTO ml_technologies (company_name, technology_name, technology_type, 
                                   application_area, description, implementation_date, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ml_data)
    
    conn.commit()

def create_env_file():
    """Create env.main file with secure passwords"""
    passwords = {
        'DB_PASSWORD': generate_secure_password(24),
        'API_KEY': generate_secure_password(32),
        'SECRET_KEY': generate_secure_password(32),
        'JWT_SECRET': generate_secure_password(32),
        'ENCRYPTION_KEY': generate_secure_password(32),
        'DB_USERNAME': 'ml_analyst',
        'DB_NAME': 'ml_technologies.db',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432'
    }
    
    with open('/home/vovkes/DATADOG/env.main', 'w') as f:
        f.write("# ML Technologies Database Environment Variables\n")
        f.write("# Generated on: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("# WARNING: Keep this file secure and never commit to version control\n\n")
        
        for key, value in passwords.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Environment file 'env.main' created with secure passwords")
    print("🔐 Passwords generated and saved securely")

def main():
    """Main function to create database and populate with data"""
    print("🚀 Creating ML Technologies Database...")
    
    # Create database
    conn = create_database()
    print("✅ Database schema created")
    
    # Populate tables
    populate_companies(conn)
    print("✅ Companies data populated")
    
    populate_technology_categories(conn)
    print("✅ Technology categories populated")
    
    populate_ml_technologies(conn)
    print("✅ ML technologies data populated")
    
    # Create environment file
    create_env_file()
    
    # Display summary
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ml_technologies")
    tech_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM companies")
    company_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM technology_categories")
    category_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database Summary:")
    print(f"   • Companies: {company_count}")
    print(f"   • ML Technologies: {tech_count}")
    print(f"   • Technology Categories: {category_count}")
    print(f"   • Database file: /home/vovkes/DATADOG/ml_technologies.db")
    print(f"   • Environment file: /home/vovkes/DATADOG/env.main")
    
    conn.close()
    print("\n🎉 Database creation completed successfully!")

if __name__ == "__main__":
    main()
