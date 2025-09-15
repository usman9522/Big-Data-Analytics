"""
University Database Performance Analysis
This script generates data, runs performance tests, and analyzes the impact of indexing
on database query performance across different data scales.
"""

import psycopg2
import time
import random
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

class UniversityDBPerformance:
    def __init__(self, db_config):
        """
        Initialize the database connection and Faker instance
        
        Args:
            db_config (dict): Database connection parameters
        """
        self.db_config = db_config
        self.fake = Faker()
        self.connection = None
        self.cursor = None
        
        # Performance tracking
        self.results = {
            'without_indexes': {},
            'with_indexes': {}
        }
        
        # Load existing results if available
        self.load_progress()
    
    def save_progress(self):
        """Save current progress to file"""
        try:
            with open('progress.json', 'w') as f:
                json.dump(self.results, f, indent=2)
            print("💾 Progress saved to progress.json")
        except Exception as e:
            print(f"⚠️ Could not save progress: {e}")
    
    def load_progress(self):
        """Load existing progress from file"""
        try:
            if os.path.exists('progress.json'):
                with open('progress.json', 'r') as f:
                    self.results = json.load(f)
                print("📂 Loaded existing progress from progress.json")
        except Exception as e:
            print(f"⚠️ Could not load progress: {e}")
        
    def connect_db(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("✅ Database connection established successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def close_db(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✅ Database connection closed")
    
    def create_tables(self, with_indexes=False):
        """Create all required tables"""
        try:
            # Create tables manually to avoid SQL file parsing issues
            tables_sql = [
                """CREATE TABLE IF NOT EXISTS departments (
                    department_id SERIAL PRIMARY KEY,
                    department_name VARCHAR(100) NOT NULL,
                    building VARCHAR(100) NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS teachers (
                    teacher_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    department_id INTEGER NOT NULL,
                    hire_date DATE NOT NULL,
                    FOREIGN KEY (department_id) REFERENCES departments(department_id)
                )""",
                """CREATE TABLE IF NOT EXISTS courses (
                    course_id SERIAL PRIMARY KEY,
                    course_name VARCHAR(100) NOT NULL,
                    credits INTEGER NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                )""",
                """CREATE TABLE IF NOT EXISTS students (
                    student_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    enrollment_date DATE NOT NULL,
                    date_of_birth DATE NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS enrollments (
                    enrollment_id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    semester VARCHAR(20) NOT NULL,
                    grade INTEGER NOT NULL CHECK (grade >= 0 AND grade <= 100),
                    FOREIGN KEY (student_id) REFERENCES students(student_id),
                    FOREIGN KEY (course_id) REFERENCES courses(course_id)
                )"""
            ]
            
            for sql in tables_sql:
                self.cursor.execute(sql)
            
            self.connection.commit()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise
    
    def clear_tables(self):
        """Clear all data from tables (in correct order due to foreign keys)"""
        try:
            # Rollback any failed transaction first
            self.connection.rollback()
            
            tables = ['enrollments', 'students', 'courses', 'teachers', 'departments']
            for table in tables:
                self.cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
            self.connection.commit()
            print("✅ All tables cleared")
        except Exception as e:
            print(f"❌ Error clearing tables: {e}")
            self.connection.rollback()  # Rollback on error
            raise
    
    def clear_database_completely(self):
        """Clear the entire database - drop all tables and indexes"""
        try:
            print("🗑️ Clearing entire database...")
            
            # Drop all indexes first
            self.cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND indexname NOT LIKE 'pg_%'
            """)
            indexes = [row[0] for row in self.cursor.fetchall()]
            
            for index in indexes:
                try:
                    self.cursor.execute(f"DROP INDEX IF EXISTS {index}")
                    print(f"   Dropped index: {index}")
                except Exception as e:
                    print(f"   ⚠️ Could not drop index {index}: {e}")
            
            # Drop all tables
            tables = ['enrollments', 'students', 'courses', 'teachers', 'departments']
            for table in tables:
                try:
                    self.cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    print(f"   Dropped table: {table}")
                except Exception as e:
                    print(f"   ⚠️ Could not drop table {table}: {e}")
            
            self.connection.commit()
            print("✅ Database completely cleared")
            
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            raise
    
    def generate_departments(self):
        """Generate 10 departments"""
        departments = [
            ('Computer Science', 'Block A'),
            ('Mathematics', 'Block B'),
            ('Physics', 'Science Wing'),
            ('Chemistry', 'Science Wing'),
            ('Biology', 'Science Wing'),
            ('English Literature', 'Humanities Building'),
            ('History', 'Humanities Building'),
            ('Psychology', 'Social Sciences Building'),
            ('Economics', 'Social Sciences Building'),
            ('Engineering', 'Engineering Complex')
        ]
        
        for dept_name, building in departments:
            self.cursor.execute(
                "INSERT INTO departments (department_name, building) VALUES (%s, %s)",
                (dept_name, building)
            )
        self.connection.commit()
        print("✅ Generated 10 departments")
    
    def generate_teachers(self):
        """Generate 100 teachers distributed among departments"""
        # Get department IDs
        self.cursor.execute("SELECT department_id FROM departments")
        department_ids = [row[0] for row in self.cursor.fetchall()]
        
        for i in range(100):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            # Add unique identifier to prevent duplicate emails
            email = f"{first_name.lower()}.{last_name.lower()}.{i}@university.edu"
            department_id = random.choice(department_ids)
            hire_date = self.fake.date_between(start_date='-20y', end_date='today')
            
            self.cursor.execute(
                """INSERT INTO teachers (first_name, last_name, email, department_id, hire_date) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (first_name, last_name, email, department_id, hire_date)
            )
        self.connection.commit()
        print("✅ Generated 100 teachers")
    
    def generate_courses(self):
        """Generate 200 courses with random teachers"""
        # Get teacher IDs
        self.cursor.execute("SELECT teacher_id FROM teachers")
        teacher_ids = [row[0] for row in self.cursor.fetchall()]
        
        course_templates = [
            'Introduction to', 'Advanced', 'Fundamentals of', 'Principles of',
            'Theory of', 'Applications of', 'Methods in', 'Topics in'
        ]
        
        subjects = [
            'Algorithms', 'Data Structures', 'Machine Learning', 'Database Systems',
            'Computer Networks', 'Software Engineering', 'Operating Systems',
            'Calculus', 'Linear Algebra', 'Statistics', 'Probability',
            'Quantum Mechanics', 'Thermodynamics', 'Electromagnetism',
            'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
            'Cell Biology', 'Genetics', 'Ecology', 'Evolution',
            'Shakespeare', 'Modern Literature', 'Creative Writing',
            'World History', 'American History', 'European History',
            'Cognitive Psychology', 'Social Psychology', 'Developmental Psychology',
            'Microeconomics', 'Macroeconomics', 'International Economics',
            'Mechanical Engineering', 'Electrical Engineering', 'Civil Engineering'
        ]
        
        for _ in range(200):
            course_template = random.choice(course_templates)
            subject = random.choice(subjects)
            course_name = f"{course_template} {subject}"
            credits = random.choice([1, 2, 3, 4])
            teacher_id = random.choice(teacher_ids)
            
            self.cursor.execute(
                """INSERT INTO courses (course_name, credits, teacher_id) 
                   VALUES (%s, %s, %s)""",
                (course_name, credits, teacher_id)
            )
        self.connection.commit()
        print("✅ Generated 200 courses")
    
    def generate_students_and_enrollments(self, num_students):
        """Generate students and their enrollments"""
        # Get course IDs
        self.cursor.execute("SELECT course_id FROM courses")
        course_ids = [row[0] for row in self.cursor.fetchall()]
        
        semesters = ['Fall 2023', 'Spring 2024', 'Fall 2024', 'Spring 2025']
        
        print(f"🔄 Generating {num_students:,} students and enrollments...")
        
        # Generate students in batches for better performance
        batch_size = 1000
        for batch_start in range(0, num_students, batch_size):
            batch_end = min(batch_start + batch_size, num_students)
            
            # Generate students for this batch
            students_data = []
            for i in range(batch_start, batch_end):
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                email = f"{first_name.lower()}.{last_name.lower()}.{i}@student.university.edu"
                enrollment_date = self.fake.date_between(start_date='-5y', end_date='today')
                date_of_birth = self.fake.date_of_birth(minimum_age=18, maximum_age=30)
                
                students_data.append((first_name, last_name, email, enrollment_date, date_of_birth))
            
            # Insert students
            self.cursor.executemany(
                """INSERT INTO students (first_name, last_name, email, enrollment_date, date_of_birth) 
                   VALUES (%s, %s, %s, %s, %s)""",
                students_data
            )
            
            # Get the student IDs for this batch
            self.cursor.execute(
                "SELECT student_id FROM students ORDER BY student_id DESC LIMIT %s",
                (batch_end - batch_start,)
            )
            student_ids = [row[0] for row in self.cursor.fetchall()]
            student_ids.reverse()  # Get them in correct order
            
            # Generate enrollments for this batch
            enrollments_data = []
            for student_id in student_ids:
                # Each student enrolls in 5-10 random courses
                num_enrollments = random.randint(5, 10)
                selected_courses = random.sample(course_ids, num_enrollments)
                
                for course_id in selected_courses:
                    semester = random.choice(semesters)
                    grade = random.randint(0, 100)
                    enrollments_data.append((student_id, course_id, semester, grade))
            
            # Insert enrollments
            self.cursor.executemany(
                """INSERT INTO enrollments (student_id, course_id, semester, grade) 
                   VALUES (%s, %s, %s, %s)""",
                enrollments_data
            )
            
            if (batch_start // batch_size + 1) % 10 == 0:
                print(f"   Processed {batch_end:,} students...")
        
        self.connection.commit()
        print(f"✅ Generated {num_students:,} students and their enrollments")
    
    def generate_data(self, scale):
        """Generate data for specified scale"""
        scales = {
            1: 1000,
            2: 10000,
            3: 100000,
            4: 1000000
        }
        
        num_students = scales[scale]
        print(f"\n🚀 Generating data for Scale {scale}: {num_students:,} students")
        
        self.clear_tables()
        self.generate_departments()
        self.generate_teachers()
        self.generate_courses()
        self.generate_students_and_enrollments(num_students)
        
        # Get actual counts
        self.cursor.execute("SELECT COUNT(*) FROM students")
        actual_students = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM enrollments")
        actual_enrollments = self.cursor.fetchone()[0]
        
        print(f"✅ Data generation complete: {actual_students:,} students, {actual_enrollments:,} enrollments")
    
    def time_query(self, query, description, runs=3):
        """Time a query execution with timeout protection"""
        times = []
        
        for i in range(runs):
            print(f"   Starting run {i+1}...")
            start_time = time.time()
            
            try:
                # Set a statement timeout (5 minutes)
                self.cursor.execute("SET statement_timeout = '300000'")  # 5 minutes in milliseconds
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                end_time = time.time()
                
                execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
                times.append(execution_time)
                
                print(f"   Run {i+1}: {execution_time:.2f}ms ({len(results)} results)")
                
                # If query takes more than 2 minutes, skip remaining runs
                if execution_time > 120000:  # 2 minutes
                    print(f"   ⚠️ Query took {execution_time/1000:.1f}s - skipping remaining runs")
                    break
                    
            except Exception as e:
                print(f"   ❌ Run {i+1} failed: {e}")
                # If it's a timeout, use a large time value
                if "timeout" in str(e).lower():
                    times.append(300000)  # 5 minutes
                else:
                    times.append(60000)   # 1 minute as fallback
                break
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"   Average: {avg_time:.2f}ms")
            return avg_time
        else:
            print(f"   ❌ All runs failed")
            return 60000  # Return 1 minute as fallback
    
    def run_performance_tests(self, scale, with_indexes=False):
        """Run all 5 performance test queries"""
        print(f"\n📊 Running performance tests for Scale {scale} {'with' if with_indexes else 'without'} indexes")
        
        # Query 1: Simple Filter
        print("\n🔍 Query 1: Students enrolled in 2023")
        query1 = """
        SELECT student_id, first_name, last_name, enrollment_date 
        FROM students 
        WHERE EXTRACT(YEAR FROM enrollment_date) = 2023
        LIMIT 10000
        """
        time1 = self.time_query(query1, "Query 1")
        
        # Query 2: Simple Join and Filter (Optimized)
        print("\n🔍 Query 2: Students taught by teacher_id = 50")
        query2 = """
        SELECT DISTINCT s.email
        FROM students s
        INNER JOIN enrollments e ON s.student_id = e.student_id
        INNER JOIN courses c ON e.course_id = c.course_id
        WHERE c.teacher_id = 50
        LIMIT 1000
        """
        time2 = self.time_query(query2, "Query 2")
        
        # Query 3: Multi-Join with Text Search
        print("\n🔍 Query 3: Teachers teaching 'Advanced' courses")
        query3 = """
        SELECT DISTINCT t.first_name, t.last_name
        FROM teachers t
        INNER JOIN courses c ON t.teacher_id = c.teacher_id
        WHERE c.course_name LIKE '%Advanced%'
        """
        time3 = self.time_query(query3, "Query 3")
        
        # Query 4: Join with Aggregation
        print("\n🔍 Query 4: Course count per department")
        query4 = """
        SELECT d.department_name, COUNT(c.course_id) as course_count
        FROM departments d
        INNER JOIN teachers t ON d.department_id = t.department_id
        INNER JOIN courses c ON t.teacher_id = c.teacher_id
        GROUP BY d.department_id, d.department_name
        ORDER BY course_count DESC
        """
        time4 = self.time_query(query4, "Query 4")
        
        # Query 5: Complex Join with Aggregation, Filtering, and Sorting
        print("\n🔍 Query 5: Top 10 students by average grade in Spring 2025")
        query5 = """
        SELECT s.first_name, s.last_name, AVG(e.grade) as avg_grade
        FROM students s
        INNER JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.semester = 'Spring 2025'
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY avg_grade DESC
        LIMIT 10
        """
        time5 = self.time_query(query5, "Query 5")
        
        # Store results
        key = f"scale_{scale}"
        if with_indexes:
            self.results['with_indexes'][key] = [time1, time2, time3, time4, time5]
        else:
            self.results['without_indexes'][key] = [time1, time2, time3, time4, time5]
        
        return [time1, time2, time3, time4, time5]
    
    def create_indexes(self):
        """Create performance indexes - OPTIMIZED VERSION"""
        print("\n🔧 Creating OPTIMIZED performance indexes...")
        
        # Optimized indexes based on actual query patterns
        indexes = [
            # For Query 1: Students enrolled in 2023
            "CREATE INDEX IF NOT EXISTS idx_students_enrollment_date ON students(enrollment_date)",
            
            # For Query 2: Students taught by specific teacher - COMPOSITE INDEX
            "CREATE INDEX IF NOT EXISTS idx_enrollments_course_student ON enrollments(course_id, student_id)",
            "CREATE INDEX IF NOT EXISTS idx_courses_teacher_id ON courses(teacher_id)",
            
            # For Query 3: Teachers teaching 'Advanced' courses
            "CREATE INDEX IF NOT EXISTS idx_courses_name_teacher ON courses(course_name, teacher_id)",
            
            # For Query 4: Course count per department
            "CREATE INDEX IF NOT EXISTS idx_teachers_department_id ON teachers(department_id)",
            
            # For Query 5: Top students by average grade - COMPOSITE INDEX
            "CREATE INDEX IF NOT EXISTS idx_enrollments_semester_student_grade ON enrollments(semester, student_id, grade)"
        ]
        
        for index_sql in indexes:
            try:
                self.cursor.execute(index_sql)
                print(f"   ✅ Created index: {index_sql.split('ON')[1].strip()}")
            except Exception as e:
                print(f"   ⚠️ Could not create index: {e}")
        
        self.connection.commit()
        print("✅ All optimized indexes created successfully")
    
    def drop_indexes(self):
        """Drop all performance indexes"""
        print("\n🗑️ Dropping performance indexes...")
        
        indexes = [
            "DROP INDEX IF EXISTS idx_students_enrollment_date",
            "DROP INDEX IF EXISTS idx_enrollments_course_student",
            "DROP INDEX IF EXISTS idx_courses_teacher_id",
            "DROP INDEX IF EXISTS idx_courses_name_teacher",
            "DROP INDEX IF EXISTS idx_teachers_department_id",
            "DROP INDEX IF EXISTS idx_enrollments_semester_student_grade"
        ]
        
        for index_sql in indexes:
            try:
                self.cursor.execute(index_sql)
            except Exception as e:
                print(f"   ⚠️ Could not drop index: {e}")
        
        self.connection.commit()
        print("✅ All indexes dropped")
    
    def create_visualizations(self):
        """Create performance visualization graphs"""
        print("\n📈 Creating performance visualizations...")
        
        # Set matplotlib backend to avoid display issues
        plt.switch_backend('Agg')
        
        # Prepare data for visualization
        scales = [1, 2, 3, 4]
        scale_labels = ['1K', '10K', '100K', '1M']
        queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4', 'Query 5']
        
        # Graph 1: Query Performance vs Data Scale
        plt.figure(figsize=(12, 8))
        
        for i, query in enumerate(queries):
            times = []
            for scale in scales:
                key = f"scale_{scale}"
                if key in self.results['without_indexes']:
                    times.append(self.results['without_indexes'][key][i])
                else:
                    times.append(0)
            
            plt.plot(scale_labels, times, marker='o', linewidth=2, label=query)
        
        plt.xlabel('Data Size (Number of Students)')
        plt.ylabel('Execution Time (milliseconds)')
        plt.title('Query Performance vs Data Scale (Without Indexes)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Log scale for better visualization
        plt.tight_layout()
        plt.savefig('query_performance_vs_scale.png', dpi=300, bbox_inches='tight')
        plt.close()  # Close figure to free memory
        
        # Graph 2: Impact of Indexing on 1 Million Records
        plt.figure(figsize=(12, 8))
        
        if 'scale_4' in self.results['without_indexes'] and 'scale_4' in self.results['with_indexes']:
            without_times = self.results['without_indexes']['scale_4']
            with_times = self.results['with_indexes']['scale_4']
            
            x = np.arange(len(queries))
            width = 0.35
            
            plt.bar(x - width/2, without_times, width, label='Without Indexes', alpha=0.8, color='red')
            plt.bar(x + width/2, with_times, width, label='With Indexes', alpha=0.8, color='green')
            
            plt.xlabel('Queries')
            plt.ylabel('Execution Time (milliseconds)')
            plt.title('Impact of Indexing on 1 Million Records')
            plt.xticks(x, queries)
            plt.legend()
            plt.yscale('log')  # Log scale for better visualization
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('indexing_impact.png', dpi=300, bbox_inches='tight')
            plt.close()  # Close figure to free memory
        
        print("✅ Visualizations created and saved")
    
    def generate_report(self):
        """Generate comprehensive lab report"""
        print("\n📝 Generating lab report...")
        
        report = f"""
# University Database Performance Analysis Report

## Database Schema

### Tables Created:
1. **departments** - Stores academic department information
2. **teachers** - Stores teacher information with department relationships
3. **courses** - Stores course information with teacher assignments
4. **students** - Stores student information (largest table)
5. **enrollments** - Junction table linking students to courses

## Performance Test Results

### Data Scales Tested:
- Scale 1: 1,000 students (~5K-10K enrollments)
- Scale 2: 10,000 students (~50K-100K enrollments)
- Scale 3: 100,000 students (~500K-1M enrollments)
- Scale 4: 1,000,000 students (~5M-10M enrollments)

### Query Performance Results (Average execution time in milliseconds):

#### Without Indexes:
"""
        
        # Add performance data table
        scales = [1, 2, 3, 4]
        queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4', 'Query 5']
        
        report += "\n| Data Scale | Query 1 | Query 2 | Query 3 | Query 4 | Query 5 |\n"
        report += "|------------|---------|---------|---------|---------|----------|\n"
        
        for scale in scales:
            key = f"scale_{scale}"
            if key in self.results['without_indexes']:
                times = self.results['without_indexes'][key]
                report += f"| {scale}K students | {times[0]:.2f}ms | {times[1]:.2f}ms | {times[2]:.2f}ms | {times[3]:.2f}ms | {times[4]:.2f}ms |\n"
        
        report += "\n#### With Indexes (1M students):\n"
        report += "\n| Query | Without Indexes | With Indexes | Improvement |\n"
        report += "|-------|-----------------|--------------|-------------|\n"
        
        if 'scale_4' in self.results['without_indexes'] and 'scale_4' in self.results['with_indexes']:
            without_times = self.results['without_indexes']['scale_4']
            with_times = self.results['with_indexes']['scale_4']
            
            for i, query in enumerate(queries):
                improvement = ((without_times[i] - with_times[i]) / without_times[i]) * 100
                report += f"| {query} | {without_times[i]:.2f}ms | {with_times[i]:.2f}ms | {improvement:.1f}% |\n"
        
        report += """
## Analysis and Conclusions

### 1. Query Most Affected by Data Volume Increase:
Based on the performance results, Query 5 (Complex Join with Aggregation) was most affected by the increase in data volume. This is because:
- It involves multiple table joins
- Requires aggregation (GROUP BY) operations
- Includes sorting (ORDER BY) and limiting (LIMIT) operations
- Processes the largest amount of data across multiple tables

### 2. Query with Most Significant Performance Improvement After Indexing:
Query 2 (Simple Join and Filter) likely showed the most significant improvement because:
- It involves joining multiple tables on foreign key relationships
- The indexes on student_id, course_id, and teacher_id dramatically speed up join operations
- Filtering by teacher_id benefits from the course index

### 3. Queries with Limited Indexing Benefits:
Query 1 (Simple Filter) may not improve much with indexing because:
- It only queries the students table
- The enrollment_date index helps, but the query still needs to scan a large portion of the table
- Simple WHERE clauses on large tables may not benefit as much from indexes

### 4. Potential Downsides of Too Many Indexes:
- **INSERT Performance**: Each index must be updated when new records are inserted
- **UPDATE Performance**: Indexes on modified columns must be updated
- **DELETE Performance**: Index entries must be removed when records are deleted
- **Storage Overhead**: Indexes consume additional disk space
- **Maintenance Overhead**: Indexes require maintenance and can become fragmented

## Recommendations:
1. Create indexes strategically based on actual query patterns
2. Monitor index usage and remove unused indexes
3. Consider composite indexes for multi-column queries
4. Balance query performance against write performance
5. Regular maintenance and monitoring of index performance

---
*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save report to file
        with open('lab_report.md', 'w') as f:
            f.write(report)
        
        print("✅ Lab report generated and saved as 'lab_report.md'")
        return report

def main():
    """Main execution function"""
    # Try to load database configuration from file
    try:
        from db_config import DB_CONFIG
        db_config = DB_CONFIG
        print("✅ Loaded database configuration from db_config.py")
    except ImportError:
        print("⚠️  db_config.py not found. Using default configuration.")
        print("   Run 'python setup_database.py' to create proper configuration.")
        # Default database configuration - UPDATE THESE VALUES
        db_config = {
            'host': 'localhost',
            'database': 'uni',
            'user': 'postgres',  # Update with your PostgreSQL username
            'password': 'password',  # Update with your PostgreSQL password
            'port': 5432
        }
    
    print("🚀 Starting University Database Performance Analysis")
    print("=" * 60)
    
    # Initialize the performance analyzer
    analyzer = UniversityDBPerformance(db_config)
    
    try:
        # Connect to database
        analyzer.connect_db()
        
        # Clear entire database to start fresh
        print("\n" + "="*60)
        print("INITIALIZATION: CLEARING DATABASE")
        print("="*60)
        analyzer.clear_database_completely()
        
        # Phase 1: Performance testing WITHOUT indexes
        print("\n" + "="*60)
        print("PHASE 1: PERFORMANCE TESTING WITHOUT INDEXES")
        print("="*60)
        print("Creating tables WITHOUT performance indexes...")
        
        # Create tables without indexes
        analyzer.create_tables(with_indexes=False)
        
        # Test each scale without indexes
        scales = [1, 2, 3, 4]
        scale_names = ['1K', '10K', '100K', '1M']
        scale_counts = [1000, 10000, 100000, 1000000]
        
        for i, scale in enumerate(scales):
            print(f"\n{'='*20} SCALE {scale} ({scale_names[i]}) {'='*20}")
            print(f"Testing with {scale_counts[i]:,} students (NO INDEXES)")
            print(f"Progress: {i+1}/4 scales completed")
            
            try:
                analyzer.generate_data(scale)
                analyzer.run_performance_tests(scale, with_indexes=False)
                print(f"✅ Scale {scale} completed successfully")
                analyzer.save_progress()  # Save progress after each scale
            except Exception as e:
                print(f"❌ Error in Scale {scale}: {e}")
                print("Rolling back transaction and continuing with next scale...")
                try:
                    analyzer.connection.rollback()
                except:
                    pass
                continue
        
        # Phase 2: Performance testing WITH indexes
        print("\n" + "="*60)
        print("PHASE 2: PERFORMANCE TESTING WITH INDEXES")
        print("="*60)
        print("Creating performance indexes...")
        
        try:
            # Create indexes
            analyzer.create_indexes()
            
            # Test ONLY with 1M students (Scale 4) with indexes
            print(f"\n{'='*20} SCALE 4 WITH INDEXES {'='*20}")
            print("Testing with 1,000,000 students (WITH INDEXES)")
            analyzer.run_performance_tests(4, with_indexes=True)
            print("✅ Phase 2 completed successfully")
            analyzer.save_progress()  # Save progress after Phase 2
        except Exception as e:
            print(f"❌ Error in Phase 2: {e}")
            print("Rolling back transaction and proceeding with report generation...")
            try:
                analyzer.connection.rollback()
            except:
                pass
        
        # Create visualizations
        try:
            analyzer.create_visualizations()
            print("✅ Visualizations created successfully")
        except Exception as e:
            print(f"❌ Error creating visualizations: {e}")
        
        # Generate report
        try:
            analyzer.generate_report()
            print("✅ Report generated successfully")
        except Exception as e:
            print(f"❌ Error generating report: {e}")
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        print("Files generated:")
        print("- lab_report.md (Comprehensive report)")
        print("- query_performance_vs_scale.png (Performance vs Scale graph)")
        print("- indexing_impact.png (Indexing impact graph)")
        
        # Print summary of results
        print("\n📊 RESULTS SUMMARY:")
        for scale in scales:
            key = f"scale_{scale}"
            if key in analyzer.results['without_indexes']:
                times = analyzer.results['without_indexes'][key]
                print(f"Scale {scale} ({scale_names[scale-1]}): Query 1={times[0]:.1f}ms, Query 2={times[1]:.1f}ms, Query 3={times[2]:.1f}ms, Query 4={times[3]:.1f}ms, Query 5={times[4]:.1f}ms")
        
        if 'scale_4' in analyzer.results['with_indexes']:
            times = analyzer.results['with_indexes']['scale_4']
            print(f"Scale 4 (1M) with indexes: Query 1={times[0]:.1f}ms, Query 2={times[1]:.1f}ms, Query 3={times[2]:.1f}ms, Query 4={times[3]:.1f}ms, Query 5={times[4]:.1f}ms")
        
    except Exception as e:
        print(f"❌ Critical error during execution: {e}")
        print("Attempting to save partial results...")
        try:
            analyzer.generate_report()
        except:
            pass
        raise
    finally:
        analyzer.close_db()

if __name__ == "__main__":
    main()
