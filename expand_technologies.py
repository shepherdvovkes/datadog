#!/usr/bin/env python3
"""
Script to expand the database with additional ML technologies, 
monitoring tools, and autonomous systems technologies
"""

import sqlite3
import secrets
import string
from datetime import datetime

def generate_secure_password(length=20):
    """Generate a secure password with mixed characters"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def add_more_companies(conn):
    """Add more companies in ML, monitoring, and autonomous systems"""
    cursor = conn.cursor()
    
    additional_companies = [
        # AI/ML Companies
        ('OpenAI', 'AI Research', 'USA', 2015, 'AI research company focused on AGI'),
        ('Anthropic', 'AI Safety', 'USA', 2021, 'AI safety and research company'),
        ('Hugging Face', 'AI Platform', 'USA', 2016, 'Open source AI platform and model hub'),
        ('Cohere', 'NLP AI', 'Canada', 2019, 'Enterprise AI platform for text understanding'),
        ('Stability AI', 'Generative AI', 'UK', 2020, 'Open source generative AI company'),
        
        # Monitoring & Observability
        ('Grafana Labs', 'Observability', 'USA', 2014, 'Open source analytics and monitoring platform'),
        ('Prometheus', 'Monitoring', 'International', 2012, 'Open source monitoring system'),
        ('Jaeger', 'Distributed Tracing', 'International', 2016, 'Open source distributed tracing system'),
        ('Zipkin', 'Distributed Tracing', 'International', 2012, 'Open source distributed tracing system'),
        ('Fluentd', 'Data Collection', 'International', 2011, 'Open source data collector'),
        
        # Cloud & Infrastructure
        ('AWS', 'Cloud Computing', 'USA', 2006, 'Amazon Web Services cloud platform'),
        ('Google Cloud', 'Cloud Computing', 'USA', 2008, 'Google Cloud Platform'),
        ('Microsoft Azure', 'Cloud Computing', 'USA', 2010, 'Microsoft cloud platform'),
        ('HashiCorp', 'Infrastructure', 'USA', 2012, 'Infrastructure automation software'),
        ('Docker', 'Containerization', 'USA', 2013, 'Container platform and tools'),
        
        # Autonomous Systems
        ('Tesla', 'Autonomous Vehicles', 'USA', 2003, 'Electric vehicles and autonomous driving'),
        ('Waymo', 'Autonomous Vehicles', 'USA', 2009, 'Self-driving technology company'),
        ('Cruise', 'Autonomous Vehicles', 'USA', 2013, 'Autonomous vehicle technology'),
        ('Aurora', 'Autonomous Vehicles', 'USA', 2017, 'Autonomous vehicle technology'),
        ('NVIDIA', 'AI Hardware', 'USA', 1993, 'GPU and AI computing solutions'),
        
        # Robotics
        ('Boston Dynamics', 'Robotics', 'USA', 1992, 'Advanced robotics and AI'),
        ('iRobot', 'Consumer Robotics', 'USA', 1990, 'Consumer and military robotics'),
        ('DJI', 'Drone Technology', 'China', 2006, 'Consumer and professional drone technology'),
        ('Skydio', 'Autonomous Drones', 'USA', 2014, 'Autonomous drone technology'),
        ('Zipline', 'Drone Delivery', 'USA', 2014, 'Medical drone delivery service'),
        
        # Edge Computing & IoT
        ('Edge Impulse', 'Edge AI', 'USA', 2019, 'Edge AI development platform'),
        ('Siemens', 'Industrial IoT', 'Germany', 1847, 'Industrial automation and digitalization'),
        ('Schneider Electric', 'Industrial IoT', 'France', 1836, 'Energy management and automation'),
        ('Rockwell Automation', 'Industrial IoT', 'USA', 1903, 'Industrial automation and information solutions'),
        ('Honeywell', 'Industrial IoT', 'USA', 1906, 'Industrial automation and control systems')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO companies (company_name, industry, country, founded_year, description)
        VALUES (?, ?, ?, ?, ?)
    ''', additional_companies)
    
    conn.commit()
    print(f"✅ Added {len(additional_companies)} new companies")

def add_more_ml_technologies(conn):
    """Add more ML technologies across different domains"""
    cursor = conn.cursor()
    
    additional_ml_technologies = [
        # OpenAI Technologies
        ('OpenAI', 'GPT-4', 'Deep Learning', 'Natural Language Processing',
         'Large language model for text generation and understanding', '2023-03-01',
         'https://openai.com/gpt-4'),
        
        ('OpenAI', 'DALL-E 3', 'Computer Vision', 'Image Generation',
         'AI system for generating images from text descriptions', '2023-09-01',
         'https://openai.com/dall-e-3'),
        
        ('OpenAI', 'Whisper', 'Deep Learning', 'Speech Recognition',
         'Automatic speech recognition and translation system', '2022-09-01',
         'https://openai.com/whisper'),
        
        # Anthropic Technologies
        ('Anthropic', 'Claude', 'Deep Learning', 'Natural Language Processing',
         'AI assistant focused on helpfulness, harmlessness, and honesty', '2023-03-01',
         'https://www.anthropic.com/claude'),
        
        # Hugging Face Technologies
        ('Hugging Face', 'Transformers Library', 'Deep Learning', 'NLP Framework',
         'Open source library for natural language processing', '2019-01-01',
         'https://huggingface.co/transformers'),
        
        ('Hugging Face', 'Model Hub', 'Deep Learning', 'Model Sharing',
         'Platform for sharing and discovering ML models', '2020-01-01',
         'https://huggingface.co/models'),
        
        # Monitoring & Observability ML
        ('Grafana Labs', 'Grafana ML', 'Deep Learning', 'Time Series Analysis',
         'Machine learning capabilities for time series data analysis', '2023-01-01',
         'https://grafana.com/grafana/machine-learning'),
        
        ('Prometheus', 'Prometheus ML', 'Deep Learning', 'Anomaly Detection',
         'ML-based anomaly detection for metrics and monitoring', '2022-01-01',
         'https://prometheus.io/docs/guides/ml'),
        
        # Cloud AI Services
        ('AWS', 'SageMaker', 'Deep Learning', 'ML Platform',
         'Fully managed machine learning platform', '2017-11-01',
         'https://aws.amazon.com/sagemaker'),
        
        ('AWS', 'Rekognition', 'Computer Vision', 'Image Analysis',
         'Deep learning-based image and video analysis service', '2016-11-01',
         'https://aws.amazon.com/rekognition'),
        
        ('Google Cloud', 'Vertex AI', 'Deep Learning', 'ML Platform',
         'Unified AI platform for building and deploying ML models', '2021-05-01',
         'https://cloud.google.com/vertex-ai'),
        
        ('Google Cloud', 'AutoML', 'Deep Learning', 'Automated ML',
         'Automated machine learning for structured data', '2018-01-01',
         'https://cloud.google.com/automl'),
        
        ('Microsoft Azure', 'Azure ML', 'Deep Learning', 'ML Platform',
         'Cloud-based machine learning platform', '2019-01-01',
         'https://azure.microsoft.com/en-us/products/machine-learning'),
        
        # Autonomous Vehicle Technologies
        ('Tesla', 'Autopilot', 'Deep Learning', 'Autonomous Driving',
         'AI-powered autonomous driving system', '2015-10-01',
         'https://www.tesla.com/autopilot'),
        
        ('Tesla', 'Full Self-Driving', 'Deep Learning', 'Autonomous Driving',
         'Advanced autonomous driving capabilities', '2020-10-01',
         'https://www.tesla.com/fsd'),
        
        ('Waymo', 'Waymo Driver', 'Deep Learning', 'Autonomous Driving',
         'Fully autonomous driving system', '2017-11-01',
         'https://waymo.com/technology'),
        
        ('NVIDIA', 'Drive Platform', 'Deep Learning', 'Autonomous Driving',
         'AI computing platform for autonomous vehicles', '2015-01-01',
         'https://www.nvidia.com/en-us/self-driving-cars'),
        
        # Robotics AI
        ('Boston Dynamics', 'Atlas AI', 'Deep Learning', 'Humanoid Robotics',
         'AI-powered humanoid robot with advanced mobility', '2013-01-01',
         'https://www.bostondynamics.com/atlas'),
        
        ('Boston Dynamics', 'Spot AI', 'Deep Learning', 'Quadruped Robotics',
         'AI-powered quadruped robot for various applications', '2019-06-01',
         'https://www.bostondynamics.com/spot'),
        
        # Drone AI Technologies
        ('DJI', 'ActiveTrack', 'Computer Vision', 'Drone Tracking',
         'AI-powered subject tracking for drones', '2016-01-01',
         'https://www.dji.com/activetrack'),
        
        ('DJI', 'Obstacle Avoidance', 'Computer Vision', 'Drone Safety',
         'AI-powered obstacle detection and avoidance', '2016-01-01',
         'https://www.dji.com/obstacle-avoidance'),
        
        ('Skydio', 'Autonomous Flight', 'Deep Learning', 'Drone Autonomy',
         'AI-powered autonomous drone flight system', '2018-01-01',
         'https://www.skydio.com/autonomy'),
        
        # Edge AI Technologies
        ('Edge Impulse', 'Edge ML', 'Deep Learning', 'Edge Computing',
         'Machine learning platform for edge devices', '2019-01-01',
         'https://www.edgeimpulse.com'),
        
        ('NVIDIA', 'Jetson Platform', 'Deep Learning', 'Edge AI',
         'AI computing platform for edge devices', '2014-01-01',
         'https://www.nvidia.com/en-us/autonomous-machines/embedded-systems'),
        
        # Industrial IoT AI
        ('Siemens', 'MindSphere AI', 'Deep Learning', 'Industrial IoT',
         'AI platform for industrial IoT applications', '2016-01-01',
         'https://siemens.com/mindsphere'),
        
        ('Honeywell', 'Forge AI', 'Deep Learning', 'Industrial Analytics',
         'AI-powered industrial analytics platform', '2018-01-01',
         'https://www.honeywellforge.ai'),
        
        # Additional Monitoring Technologies
        ('Jaeger', 'Distributed Tracing ML', 'Deep Learning', 'Performance Analysis',
         'ML-based analysis of distributed tracing data', '2021-01-01',
         'https://www.jaegertracing.io'),
        
        ('Fluentd', 'Log Analytics ML', 'Deep Learning', 'Log Analysis',
         'Machine learning for log data analysis', '2020-01-01',
         'https://www.fluentd.org'),
        
        # Container and DevOps AI
        ('Docker', 'Container AI', 'Deep Learning', 'Container Management',
         'AI-powered container optimization and management', '2022-01-01',
         'https://www.docker.com/products/ai-ml'),
        
        ('HashiCorp', 'Terraform AI', 'Deep Learning', 'Infrastructure as Code',
         'AI-powered infrastructure automation', '2021-01-01',
         'https://www.hashicorp.com/products/terraform')
    ]
    
    cursor.executemany('''
        INSERT INTO ml_technologies (company_name, technology_name, technology_type,
                                   application_area, description, implementation_date, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', additional_ml_technologies)
    
    conn.commit()
    print(f"✅ Added {len(additional_ml_technologies)} new ML technologies")

def add_more_equipment(conn):
    """Add more equipment for autonomous systems and monitoring"""
    cursor = conn.cursor()
    
    additional_equipment = [
        # AI Hardware
        ('NVIDIA A100', 'NVIDIA', 'AI GPU', 
         'High-performance GPU for AI and machine learning workloads',
         '80GB HBM2e memory, 312 TFLOPS FP16, PCIe and SXM form factors',
         'CUDA, TensorFlow, PyTorch, ONNX', '$10,000-15,000', 'Available'),
        
        ('NVIDIA H100', 'NVIDIA', 'AI GPU',
         'Latest generation AI GPU with advanced architecture',
         '80GB HBM3 memory, 1000 TFLOPS FP16, Transformer Engine',
         'CUDA, TensorFlow, PyTorch, ONNX', '$25,000-35,000', 'Available'),
        
        ('Google TPU v4', 'Google', 'AI Accelerator',
         'Tensor Processing Unit for large-scale machine learning',
         '4096 cores, 32GB HBM, 275 TFLOPS FP16',
         'TensorFlow, JAX, PyTorch', 'Cloud-based', 'Available'),
        
        # Edge AI Hardware
        ('NVIDIA Jetson AGX Orin', 'NVIDIA', 'Edge AI Computer',
         'High-performance edge AI computing platform',
         '2048-core NVIDIA Ampere GPU, 12-core ARM Cortex-A78AE CPU',
         'CUDA, TensorRT, DeepStream', '$2,000-3,000', 'Available'),
        
        ('Intel Neural Compute Stick 2', 'Intel', 'Edge AI Accelerator',
         'USB-based AI inference accelerator',
         'Intel Movidius Myriad X VPU, 1 TOPS performance',
         'OpenVINO, TensorFlow Lite', '$70-100', 'Available'),
        
        # Autonomous Vehicle Hardware
        ('Tesla FSD Computer', 'Tesla', 'Autonomous Vehicle Computer',
         'Custom AI computer for autonomous driving',
         'Dual SoC, 144 TOPS performance, 8 cameras, 12 ultrasonic sensors',
         'Tesla Autopilot, Neural Networks', '$7,000-10,000', 'Tesla Vehicles'),
        
        ('Mobileye EyeQ5', 'Mobileye', 'Autonomous Vehicle Chip',
         'AI chip for autonomous vehicle perception',
         '24 TOPS performance, 8 cameras, radar, lidar support',
         'Mobileye SDK, OpenCV', '$500-800', 'Available'),
        
        # Drone Hardware
        ('DJI Matrice 300 RTK', 'DJI', 'Professional Drone',
         'Enterprise drone with AI capabilities',
         '6-directional obstacle sensing, 55-minute flight time, RTK GPS',
         'DJI SDK, Mobile SDK', '$15,000-20,000', 'Available'),
        
        ('Skydio 2+', 'Skydio', 'Autonomous Drone',
         'AI-powered autonomous drone with obstacle avoidance',
         '6K video, 27-minute flight time, 360° obstacle avoidance',
         'Skydio SDK, Computer Vision', '$1,200-1,500', 'Available'),
        
        # Industrial IoT Sensors
        ('Siemens SIMATIC IOT2000', 'Siemens', 'Industrial IoT Gateway',
         'Industrial IoT gateway with AI capabilities',
         'ARM Cortex-A7, 512MB RAM, 4GB eMMC, multiple interfaces',
         'Siemens MindSphere, Node-RED', '$300-500', 'Available'),
        
        ('Honeywell Experion PKS', 'Honeywell', 'Process Control System',
         'AI-powered process control and optimization',
         'Distributed control system with ML algorithms',
         'Honeywell Forge, Advanced Process Control', '$50,000-100,000', 'Available'),
        
        # Monitoring Hardware
        ('Grafana Loki', 'Grafana Labs', 'Log Aggregation System',
         'Log aggregation system with ML analysis',
         'Distributed logging with machine learning capabilities',
         'Grafana, Prometheus, Kubernetes', 'Open Source', 'Available'),
        
        ('Prometheus Server', 'Prometheus', 'Monitoring System',
         'Time series monitoring with ML capabilities',
         'Time series database with anomaly detection',
         'PromQL, Grafana, AlertManager', 'Open Source', 'Available'),
        
        # Robotics Hardware
        ('Boston Dynamics Spot', 'Boston Dynamics', 'Quadruped Robot',
         'AI-powered quadruped robot for various applications',
         '360° cameras, LIDAR, autonomous navigation',
         'Boston Dynamics SDK, ROS', '$75,000-100,000', 'Available'),
        
        ('iRobot Roomba j7+', 'iRobot', 'Autonomous Vacuum',
         'AI-powered autonomous vacuum with obstacle avoidance',
         'Computer vision, smart mapping, self-emptying',
         'iRobot Home App, Smart Home Integration', '$800-1,200', 'Available'),
        
        # Edge Computing
        ('Raspberry Pi 4 Model B', 'Raspberry Pi Foundation', 'Single Board Computer',
         'Versatile single board computer for edge AI',
         'ARM Cortex-A72, 8GB RAM, 4K video, multiple interfaces',
         'Python, TensorFlow Lite, OpenCV', '$75-100', 'Available'),
        
        ('Jetson Nano', 'NVIDIA', 'Edge AI Computer',
         'Low-power edge AI computing platform',
         '128-core Maxwell GPU, 4GB RAM, multiple interfaces',
         'CUDA, TensorRT, DeepStream', '$100-150', 'Available')
    ]
    
    cursor.executemany('''
        INSERT INTO equipment (name, manufacturer, category, description, 
                              specifications, supported_software, price_range, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', additional_equipment)
    
    conn.commit()
    print(f"✅ Added {len(additional_equipment)} new equipment items")

def add_more_flight_control_systems(conn):
    """Add more flight control and autonomous systems"""
    cursor = conn.cursor()
    
    additional_flight_systems = [
        ('ROS (Robot Operating System)', 'Robotics Framework',
         'Open source robotics middleware framework',
         'Distributed computing, hardware abstraction, device drivers',
         'Various robots and autonomous systems',
         True, 'Large community, extensive packages', 'https://www.ros.org/'),
        
        ('ROS 2', 'Robotics Framework',
         'Next generation robot operating system',
         'Real-time capabilities, security, DDS communication',
         'Modern autonomous systems and robots',
         True, 'Active development, industry adoption', 'https://docs.ros.org/en/ros2/'),
        
        ('Gazebo', 'Robot Simulation',
         '3D robot simulator for autonomous systems',
         'Physics simulation, sensor simulation, multi-robot support',
         'Various robots and autonomous vehicles',
         True, 'Large community, extensive models', 'https://gazebosim.org/'),
        
        ('Webots', 'Robot Simulation',
         'Professional robot simulation software',
         '3D simulation, sensor simulation, robot programming',
         'Educational and research robotics',
         True, 'Academic and commercial support', 'https://cyberbotics.com/'),
        
        ('CARLA', 'Autonomous Driving Simulator',
         'Open source autonomous driving simulator',
         'Realistic urban simulation, sensor simulation, AI training',
         'Autonomous vehicles and robotics',
         True, 'Research community, active development', 'https://carla.org/'),
        
        ('AirSim', 'Drone Simulation',
         'Open source simulator for drones and autonomous vehicles',
         'Realistic physics, sensor simulation, AI training',
         'Drones, cars, and autonomous systems',
         True, 'Microsoft research, community support', 'https://microsoft.github.io/AirSim/'),
        
        ('Unity ML-Agents', 'AI Training Platform',
         'Unity plugin for training intelligent agents',
         'Reinforcement learning, imitation learning, curriculum learning',
         'Games, robotics, autonomous systems',
         True, 'Unity community, active development', 'https://unity.com/products/machine-learning-agents'),
        
        ('TensorFlow Lite', 'Edge AI Framework',
         'Lightweight machine learning framework for mobile and edge devices',
         'Model optimization, hardware acceleration, cross-platform',
         'Mobile devices, IoT, edge computing',
         True, 'Google support, large community', 'https://www.tensorflow.org/lite'),
        
        ('ONNX Runtime', 'AI Inference Engine',
         'Cross-platform inference engine for ML models',
         'Model interoperability, hardware acceleration, optimization',
         'Various AI applications and platforms',
         True, 'Microsoft support, industry adoption', 'https://onnxruntime.ai/'),
        
        ('OpenVINO', 'AI Inference Toolkit',
         'Intel toolkit for optimizing AI inference',
         'Model optimization, hardware acceleration, cross-platform',
         'Edge computing, IoT, computer vision',
         True, 'Intel support, performance optimization', 'https://docs.openvino.ai/')
    ]
    
    cursor.executemany('''
        INSERT INTO flight_control_systems (name, type, description, features,
                                           supported_hardware, open_source, 
                                           community_support, documentation_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', additional_flight_systems)
    
    conn.commit()
    print(f"✅ Added {len(additional_flight_systems)} new flight control systems")

def update_env_file():
    """Update the environment file with additional secure passwords"""
    additional_passwords = {
        'AI_HARDWARE_PASSWORD': generate_secure_password(24),
        'EDGE_AI_API_KEY': generate_secure_password(32),
        'ROBOTICS_SECRET': generate_secure_password(32),
        'SIMULATION_ENCRYPTION_KEY': generate_secure_password(32),
        'AUTONOMOUS_SYSTEMS_KEY': generate_secure_password(32)
    }
    
    with open('/home/vovkes/DATADOG/env.main', 'a') as f:
        f.write("\n# Additional passwords for expanded AI and autonomous systems\n")
        f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, value in additional_passwords.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Environment file updated with additional secure passwords")

def main():
    """Main function to expand the database with additional technologies"""
    print("🚀 Expanding Database with Additional ML and Autonomous Systems Technologies...")
    
    # Connect to database
    conn = sqlite3.connect('/home/vovkes/DATADOG/ml_technologies.db')
    
    # Add more companies
    add_more_companies(conn)
    
    # Add more ML technologies
    add_more_ml_technologies(conn)
    
    # Add more equipment
    add_more_equipment(conn)
    
    # Add more flight control systems
    add_more_flight_control_systems(conn)
    
    # Update environment file
    update_env_file()
    
    # Display final summary
    cursor = conn.cursor()
    
    # Count records in each table
    tables = ['companies', 'ml_technologies', 'equipment', 'flight_control_systems']
    counts = {}
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cursor.fetchone()[0]
    
    print(f"\n📊 Expanded Database Summary:")
    print(f"   • Companies: {counts['companies']}")
    print(f"   • ML Technologies: {counts['ml_technologies']}")
    print(f"   • Equipment: {counts['equipment']}")
    print(f"   • Flight Control Systems: {counts['flight_control_systems']}")
    print(f"   • Database file: /home/vovkes/DATADOG/ml_technologies.db")
    print(f"   • Environment file: /home/vovkes/DATADOG/env.main")
    
    conn.close()
    print("\n🎉 Database expansion completed successfully!")

if __name__ == "__main__":
    main()
