#!/usr/bin/env python3
"""
Script to extend the ML technologies database with equipment and technologies
like PX4/ArduPilot and CUBE+ systems
"""

import sqlite3
import secrets
import string
from datetime import datetime

def generate_secure_password(length=20):
    """Generate a secure password with mixed characters"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def extend_database():
    """Extend the existing database with equipment and flight control technologies"""
    conn = sqlite3.connect('/home/vovkes/DATADOG/ml_technologies.db')
    cursor = conn.cursor()
    
    # Create equipment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manufacturer TEXT,
            category TEXT,
            description TEXT,
            specifications TEXT,
            supported_software TEXT,
            price_range TEXT,
            availability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create flight_control_systems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_control_systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            description TEXT,
            features TEXT,
            supported_hardware TEXT,
            open_source BOOLEAN,
            community_support TEXT,
            documentation_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sensors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            manufacturer TEXT,
            specifications TEXT,
            accuracy TEXT,
            range TEXT,
            power_consumption TEXT,
            interface TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create companies for equipment manufacturers
    equipment_companies = [
        ('3D Robotics', 'Drone Manufacturing', 'USA', 2009, 'Drone and autopilot hardware manufacturer'),
        ('Hex Technology', 'Flight Controllers', 'USA', 2015, 'Advanced flight controller manufacturer'),
        ('CUAV', 'Flight Controllers', 'China', 2012, 'Professional flight controller and sensor manufacturer'),
        ('Pixhawk', 'Open Source Hardware', 'International', 2011, 'Open source autopilot hardware platform'),
        ('ArduPilot Community', 'Open Source Software', 'International', 2007, 'Open source autopilot software community'),
        ('PX4 Foundation', 'Open Source Software', 'International', 2014, 'Open source autopilot software foundation'),
        ('U-Blox', 'GNSS Technology', 'Switzerland', 1997, 'GNSS positioning and wireless communication solutions'),
        ('Bosch Sensortec', 'Sensor Technology', 'Germany', 2005, 'MEMS sensor solutions for consumer electronics'),
        ('Invensense', 'Sensor Technology', 'USA', 2003, 'MEMS sensor and actuator solutions')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO companies (company_name, industry, country, founded_year, description)
        VALUES (?, ?, ?, ?, ?)
    ''', equipment_companies)
    
    conn.commit()
    return conn

def populate_equipment_data(conn):
    """Populate equipment table with flight controllers and related hardware"""
    cursor = conn.cursor()
    
    equipment_data = [
        # Flight Controllers
        ('Pixhawk 2.4.8', '3D Robotics', 'Flight Controller', 
         'Open source autopilot hardware supporting ArduPilot and PX4',
         'STM32F427 processor, 168MHz, 2MB Flash, 256KB RAM, 14 PWM outputs',
         'ArduPilot, PX4, QGroundControl', '$200-300', 'Available'),
        
        ('Cube Orange+', 'Hex Technology', 'Flight Controller',
         'Advanced flight controller with triple sensor redundancy and built-in ADS-B receiver',
         'STM32H7 dual processor, 400MHz, 2MB Flash, 1MB RAM, 20 PWM outputs, ADS-B receiver',
         'ArduPilot, PX4, Mission Planner', '$400-500', 'Available'),
        
        ('CUAV X7+ Pro', 'CUAV', 'Flight Controller',
         'High-performance flight controller with aerospace-grade sensors',
         'STM32H7 processor, 400MHz, 2MB Flash, 1MB RAM, 16 PWM outputs, triple redundancy',
         'ArduPilot, PX4, QGroundControl', '$300-400', 'Available'),
        
        ('Pixhawk 4', 'Pixhawk', 'Flight Controller',
         'Latest generation open source autopilot with improved performance',
         'STM32F765 processor, 216MHz, 2MB Flash, 512KB RAM, 14 PWM outputs',
         'ArduPilot, PX4, QGroundControl', '$150-250', 'Available'),
        
        ('Cube Black+', 'Hex Technology', 'Flight Controller',
         'Professional flight controller with advanced sensor fusion',
         'STM32F7 processor, 216MHz, 2MB Flash, 512KB RAM, 20 PWM outputs',
         'ArduPilot, PX4, Mission Planner', '$300-400', 'Available'),
        
        # Power Management
        ('CUAV CAN PMU', 'CUAV', 'Power Management',
         'Power management unit supporting CAN UAV standard protocol',
         'Input: 6-60V, Output: 5V/3A, 12V/2A, CAN bus communication',
         'ArduPilot, PX4', '$50-80', 'Available'),
        
        ('Pixhawk Power Module', 'Pixhawk', 'Power Management',
         'Power module with current and voltage sensing for Pixhawk',
         'Input: 2-6S LiPo, Output: 5.1V/2.5A, Current sensing: 90A',
         'ArduPilot, PX4', '$30-50', 'Available'),
        
        # GPS Modules
        ('CUAV NEO 3 U-Blox GNSS', 'CUAV', 'GPS Module',
         'High-precision GNSS module with RTK capability',
         'U-Blox ZED-F9P, RTK accuracy: 1cm, Update rate: 20Hz',
         'ArduPilot, PX4', '$200-300', 'Available'),
        
        ('Pixhawk GPS Module', 'Pixhawk', 'GPS Module',
         'Standard GPS module for Pixhawk autopilots',
         'U-Blox M8N, Accuracy: 2.5m CEP, Update rate: 10Hz',
         'ArduPilot, PX4', '$50-80', 'Available'),
        
        # Telemetry
        ('CUAV Radio V2', 'CUAV', 'Telemetry Radio',
         'Long-range telemetry radio for ground control communication',
         '433MHz/915MHz, Range: 40km, Power: 1W, Encryption support',
         'ArduPilot, PX4, QGroundControl', '$100-150', 'Available'),
        
        ('Pixhawk Telemetry Radio', 'Pixhawk', 'Telemetry Radio',
         'Standard telemetry radio for Pixhawk systems',
         '433MHz/915MHz, Range: 20km, Power: 500mW',
         'ArduPilot, PX4, Mission Planner', '$60-100', 'Available')
    ]
    
    cursor.executemany('''
        INSERT INTO equipment (name, manufacturer, category, description, 
                              specifications, supported_software, price_range, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', equipment_data)
    
    conn.commit()

def populate_flight_control_systems(conn):
    """Populate flight control systems table"""
    cursor = conn.cursor()
    
    flight_systems_data = [
        ('PX4', 'Autopilot Software', 
         'Open source autopilot software for drones, rovers, and other autonomous vehicles',
         'Multi-vehicle support, Advanced flight modes, Mission planning, Simulation support',
         'Pixhawk, Cube, CUAV X7+, Holybro, and other compatible hardware',
         True, 'Large community, active development', 'https://docs.px4.io/'),
        
        ('ArduPilot', 'Autopilot Software',
         'Open source autopilot software supporting various vehicle types',
         'Copter, Plane, Rover, Submarine support, Advanced flight modes, Mission planning',
         'Pixhawk, Cube, CUAV, Holybro, and other compatible hardware',
         True, 'Large community, extensive documentation', 'https://ardupilot.org/'),
        
        ('QGroundControl', 'Ground Control Station',
         'Cross-platform ground control station for PX4 and ArduPilot',
         'Mission planning, Real-time telemetry, Log analysis, Parameter tuning',
         'All PX4 and ArduPilot compatible hardware',
         True, 'Active development, regular updates', 'https://qgroundcontrol.com/'),
        
        ('Mission Planner', 'Ground Control Station',
         'Windows-based ground control station for ArduPilot',
         'Mission planning, Real-time telemetry, Log analysis, Parameter tuning',
         'All ArduPilot compatible hardware',
         True, 'Large community, extensive features', 'https://ardupilot.org/planner/'),
        
        ('MAVLink', 'Communication Protocol',
         'Lightweight message marshalling library for micro air vehicles',
         'Bidirectional communication, Message routing, Telemetry, Command interface',
         'All PX4 and ArduPilot compatible systems',
         True, 'Standard protocol, wide adoption', 'https://mavlink.io/'),
        
        ('MAVSDK', 'Software Development Kit',
         'Cross-platform SDK for drone programming and automation',
         'Python, C++, Swift, Java support, Mission automation, Telemetry access',
         'PX4 and ArduPilot compatible systems',
         True, 'Active development, comprehensive documentation', 'https://mavsdk.mavlink.io/')
    ]
    
    cursor.executemany('''
        INSERT INTO flight_control_systems (name, type, description, features,
                                           supported_hardware, open_source, 
                                           community_support, documentation_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', flight_systems_data)
    
    conn.commit()

def populate_sensors_data(conn):
    """Populate sensors table with various sensor types"""
    cursor = conn.cursor()
    
    sensors_data = [
        # IMU Sensors
        ('MPU-9250', 'IMU', 'Invensense', 
         '9-axis motion sensor with 3-axis gyroscope, 3-axis accelerometer, 3-axis magnetometer',
         'Gyro: ±250/500/1000/2000°/s, Accel: ±2/4/8/16g, Mag: ±4800μT',
         '±0.1°C', 'Gyro: ±250°/s, Accel: ±2g, Mag: ±4800μT', '3.3V, 3.9mA', 'I2C/SPI'),
        
        ('BMI088', 'IMU', 'Bosch Sensortec',
         'High-performance 6-axis IMU with gyroscope and accelerometer',
         'Gyro: ±125/250/500/1000/2000°/s, Accel: ±3/6/12/24g',
         '±0.1°C', 'Gyro: ±125°/s, Accel: ±3g', '3.3V, 1.2mA', 'SPI'),
        
        # Barometric Pressure Sensors
        ('MS5611', 'Barometer', 'TE Connectivity',
         'High-resolution digital barometric pressure sensor',
         'Pressure: 10-1200 mbar, Temperature: -40°C to +85°C',
         '±0.012 mbar', '10-1200 mbar', '3.3V, 1.2mA', 'I2C/SPI'),
        
        ('BMP388', 'Barometer', 'Bosch Sensortec',
         'Low-power digital barometric pressure sensor',
         'Pressure: 300-1250 hPa, Temperature: -40°C to +85°C',
         '±0.08 hPa', '300-1250 hPa', '3.3V, 3.4μA', 'I2C/SPI'),
        
        # Magnetometers
        ('HMC5883L', 'Magnetometer', 'Honeywell',
         '3-axis digital magnetometer with I2C interface',
         'Magnetic field: ±8 Gauss, Resolution: 0.73 mGauss',
         '±1°', '±8 Gauss', '3.3V, 100μA', 'I2C'),
        
        ('QMC5883L', 'Magnetometer', 'QST',
         '3-axis digital magnetometer with I2C interface',
         'Magnetic field: ±8 Gauss, Resolution: 0.73 mGauss',
         '±1°', '±8 Gauss', '3.3V, 100μA', 'I2C'),
        
        # GNSS/GPS
        ('U-Blox ZED-F9P', 'GNSS', 'U-Blox',
         'High-precision GNSS module with RTK capability',
         'Multi-constellation: GPS, GLONASS, Galileo, BeiDou, QZSS',
         'RTK: 1cm, Standard: 2.5m', 'Global', '3.3V, 200mA', 'UART'),
        
        ('U-Blox M8N', 'GNSS', 'U-Blox',
         'Multi-constellation GNSS module',
         'Multi-constellation: GPS, GLONASS, Galileo, BeiDou',
         '2.5m CEP', 'Global', '3.3V, 100mA', 'UART'),
        
        # Optical Flow
        ('PX4Flow', 'Optical Flow', 'PX4',
         'Optical flow sensor for position estimation',
         'Resolution: 752x480, Frame rate: 60fps, Range: 0.3-3m',
         '±5%', '0.3-3m', '5V, 200mA', 'I2C'),
        
        ('PMW3901', 'Optical Flow', 'Pixart',
         'Compact optical flow sensor for indoor navigation',
         'Resolution: 30x30 pixels, Frame rate: 120fps',
         '±5%', '0.1-2m', '3.3V, 50mA', 'SPI')
    ]
    
    cursor.executemany('''
        INSERT INTO sensors (name, type, manufacturer, specifications, accuracy,
                            range, power_consumption, interface)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sensors_data)
    
    conn.commit()

def add_ml_technologies_for_autonomous_systems(conn):
    """Add ML technologies specifically for autonomous systems and drones"""
    cursor = conn.cursor()
    
    autonomous_ml_data = [
        # Add to existing ml_technologies table
        ('Shield AI', 'Autonomous Navigation AI', 'Deep Learning', 'Autonomous Flight',
         'AI-powered autonomous navigation for drones and UAVs', '2024-01-01',
         'https://www.shield.ai/technology/'),
        
        ('Shield AI', 'Computer Vision for Obstacle Avoidance', 'Computer Vision', 'Safety Systems',
         'Real-time computer vision for obstacle detection and avoidance', '2024-01-01',
         'https://www.shield.ai/technology/'),
        
        ('PX4 Foundation', 'PX4 Vision AI', 'Computer Vision', 'Autonomous Flight',
         'AI-powered computer vision for autonomous drone operations', '2024-01-01',
         'https://px4.io/vision/'),
        
        ('ArduPilot Community', 'ArduPilot Machine Learning', 'Deep Learning', 'Flight Control',
         'Machine learning integration for advanced flight control algorithms', '2024-01-01',
         'https://ardupilot.org/dev/docs/machine-learning.html'),
        
        ('CUAV', 'Intelligent Flight Control', 'Deep Learning', 'Flight Management',
         'AI-enhanced flight control systems for commercial drones', '2024-01-01',
         'https://cuav.net/technology/'),
        
        ('3D Robotics', 'Autonomous Mission Planning', 'Predictive Analytics', 'Mission Management',
         'AI-powered mission planning and optimization for drone operations', '2024-01-01',
         'https://3dr.com/technology/')
    ]
    
    cursor.executemany('''
        INSERT INTO ml_technologies (company_name, technology_name, technology_type,
                                   application_area, description, implementation_date, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', autonomous_ml_data)
    
    conn.commit()

def update_env_file():
    """Update the environment file with additional secure passwords"""
    additional_passwords = {
        'EQUIPMENT_DB_PASSWORD': generate_secure_password(24),
        'FLIGHT_CONTROL_API_KEY': generate_secure_password(32),
        'SENSOR_DATA_SECRET': generate_secure_password(32),
        'AUTOPILOT_ENCRYPTION_KEY': generate_secure_password(32),
        'DRONE_COMMUNICATION_KEY': generate_secure_password(32)
    }
    
    with open('/home/vovkes/DATADOG/env.main', 'a') as f:
        f.write("\n# Additional passwords for equipment and flight control systems\n")
        f.write(f"# Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, value in additional_passwords.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Environment file updated with additional secure passwords")

def main():
    """Main function to extend the database with equipment and technologies"""
    print("🚀 Extending ML Technologies Database with Equipment and Flight Control Systems...")
    
    # Extend database
    conn = extend_database()
    print("✅ Database schema extended with equipment tables")
    
    # Populate equipment data
    populate_equipment_data(conn)
    print("✅ Equipment data populated")
    
    # Populate flight control systems
    populate_flight_control_systems(conn)
    print("✅ Flight control systems data populated")
    
    # Populate sensors data
    populate_sensors_data(conn)
    print("✅ Sensors data populated")
    
    # Add ML technologies for autonomous systems
    add_ml_technologies_for_autonomous_systems(conn)
    print("✅ ML technologies for autonomous systems added")
    
    # Update environment file
    update_env_file()
    print("✅ Environment file updated")
    
    # Display summary
    cursor = conn.cursor()
    
    # Count records in each table
    tables = ['equipment', 'flight_control_systems', 'sensors', 'ml_technologies', 'companies']
    counts = {}
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cursor.fetchone()[0]
    
    print(f"\n📊 Extended Database Summary:")
    print(f"   • Companies: {counts['companies']}")
    print(f"   • ML Technologies: {counts['ml_technologies']}")
    print(f"   • Equipment: {counts['equipment']}")
    print(f"   • Flight Control Systems: {counts['flight_control_systems']}")
    print(f"   • Sensors: {counts['sensors']}")
    print(f"   • Database file: /home/vovkes/DATADOG/ml_technologies.db")
    print(f"   • Environment file: /home/vovkes/DATADOG/env.main")
    
    conn.close()
    print("\n🎉 Database extension completed successfully!")

if __name__ == "__main__":
    main()
