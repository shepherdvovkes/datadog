#!/usr/bin/env python3
"""
Script to query the ML technologies database
"""

import sqlite3

def connect_to_database():
    """Connect to the SQLite database"""
    return sqlite3.connect('/home/vovkes/DATADOG/ml_technologies.db')

def show_all_companies():
    """Display all companies in the database"""
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT company_name, industry, country, founded_year, description
    FROM companies
    ORDER BY company_name
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    print("\n🏢 COMPANIES IN DATABASE:")
    print("=" * 100)
    print(f"{'Company':<15} {'Industry':<25} {'Country':<10} {'Founded':<8} {'Description'}")
    print("-" * 100)
    for row in results:
        desc = row[4][:40] + "..." if len(row[4]) > 40 else row[4]
        print(f"{row[0]:<15} {row[1]:<25} {row[2]:<10} {row[3]:<8} {desc}")
    return results

def show_ml_technologies_by_company(company_name=None):
    """Display ML technologies by company"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    if company_name:
        query = """
        SELECT technology_name, technology_type, application_area, description, implementation_date
        FROM ml_technologies
        WHERE company_name = ?
        ORDER BY implementation_date DESC
        """
        cursor.execute(query, [company_name])
        print(f"\n🤖 ML TECHNOLOGIES FOR {company_name.upper()}:")
    else:
        query = """
        SELECT company_name, technology_name, technology_type, application_area, description
        FROM ml_technologies
        ORDER BY company_name, technology_name
        """
        cursor.execute(query)
        print(f"\n🤖 ALL ML TECHNOLOGIES:")
    
    results = cursor.fetchall()
    conn.close()
    
    print("=" * 120)
    if company_name:
        print(f"{'Technology':<25} {'Type':<20} {'Application':<20} {'Description':<40} {'Date'}")
        print("-" * 120)
        for row in results:
            desc = row[3][:35] + "..." if len(row[3]) > 35 else row[3]
            print(f"{row[0]:<25} {row[1]:<20} {row[2]:<20} {desc:<40} {row[4]}")
    else:
        print(f"{'Company':<15} {'Technology':<25} {'Type':<20} {'Application':<20} {'Description'}")
        print("-" * 120)
        for row in results:
            desc = row[4][:30] + "..." if len(row[4]) > 30 else row[4]
            print(f"{row[0]:<15} {row[1]:<25} {row[2]:<20} {row[3]:<20} {desc}")
    return results

def show_technology_categories():
    """Display technology categories"""
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT category_name, description
    FROM technology_categories
    ORDER BY category_name
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    print("\n📊 TECHNOLOGY CATEGORIES:")
    print("=" * 80)
    print(f"{'Category':<25} {'Description'}")
    print("-" * 80)
    for row in results:
        desc = row[1][:50] + "..." if len(row[1]) > 50 else row[1]
        print(f"{row[0]:<25} {desc}")
    return results

def get_company_stats():
    """Get statistics about companies and their ML technologies"""
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Count technologies per company
    query = """
    SELECT 
        c.company_name,
        c.industry,
        COUNT(mt.id) as technology_count
    FROM companies c
    LEFT JOIN ml_technologies mt ON c.company_name = mt.company_name
    GROUP BY c.company_name, c.industry
    ORDER BY technology_count DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n📈 COMPANY STATISTICS:")
    print("=" * 70)
    print(f"{'Company':<15} {'Industry':<25} {'Technologies':<12}")
    print("-" * 70)
    for row in results:
        print(f"{row[0]:<15} {row[1]:<25} {row[2]:<12}")
    
    # Technology type distribution
    query2 = """
    SELECT 
        technology_type,
        COUNT(*) as count
    FROM ml_technologies
    WHERE technology_type IS NOT NULL
    GROUP BY technology_type
    ORDER BY count DESC
    """
    cursor.execute(query2)
    results2 = cursor.fetchall()
    
    print("\n🔬 TECHNOLOGY TYPE DISTRIBUTION:")
    print("=" * 50)
    print(f"{'Technology Type':<25} {'Count':<8}")
    print("-" * 50)
    for row in results2:
        print(f"{row[0]:<25} {row[1]:<8}")
    
    conn.close()
    return results, results2

def search_technologies(keyword):
    """Search for technologies by keyword"""
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT company_name, technology_name, technology_type, application_area, description
    FROM ml_technologies
    WHERE technology_name LIKE ? OR description LIKE ? OR application_area LIKE ?
    ORDER BY company_name
    """
    search_term = f"%{keyword}%"
    cursor.execute(query, [search_term, search_term, search_term])
    results = cursor.fetchall()
    conn.close()
    
    print(f"\n🔍 SEARCH RESULTS FOR '{keyword.upper()}':")
    print("=" * 120)
    if len(results) > 0:
        print(f"{'Company':<15} {'Technology':<25} {'Type':<20} {'Application':<20} {'Description'}")
        print("-" * 120)
        for row in results:
            desc = row[4][:30] + "..." if len(row[4]) > 30 else row[4]
            print(f"{row[0]:<15} {row[1]:<25} {row[2]:<20} {row[3]:<20} {desc}")
    else:
        print("No results found.")
    return results

def show_datagod_technologies():
    """Show specific DATAGOD technologies"""
    print("\n🎯 DATAGOD SPECIFIC ML TECHNOLOGIES:")
    print("=" * 100)
    
    conn = connect_to_database()
    cursor = conn.cursor()
    query = """
    SELECT technology_name, technology_type, application_area, description, implementation_date
    FROM ml_technologies
    WHERE company_name = 'DATAGOD'
    ORDER BY implementation_date DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    for i, row in enumerate(results, 1):
        print(f"\n{i}. {row[0]}")
        print(f"   Type: {row[1]}")
        print(f"   Application: {row[2]}")
        print(f"   Description: {row[3]}")
        print(f"   Implemented: {row[4]}")
        print("-" * 80)

def main():
    """Main function to demonstrate database queries"""
    print("🚀 ML TECHNOLOGIES DATABASE QUERY TOOL")
    print("=" * 50)
    
    # Show all companies
    show_all_companies()
    
    # Show technology categories
    show_technology_categories()
    
    # Show all ML technologies
    show_ml_technologies_by_company()
    
    # Show statistics
    get_company_stats()
    
    # Show DATAGOD specific technologies
    show_datagod_technologies()
    
    # Search for anomaly detection technologies
    search_technologies("anomaly")
    
    print("\n✅ Database query completed successfully!")
    print(f"\n📁 Database location: /home/vovkes/DATADOG/ml_technologies.db")
    print(f"🔐 Environment file: /home/vovkes/DATADOG/env.main")

if __name__ == "__main__":
    main()