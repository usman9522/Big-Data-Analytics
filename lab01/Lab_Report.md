# The Impact of Data Scale and Indexing on Query Performance

## 1. SQL Schema (CREATE TABLE statements)

```sql
-- 1. Departments Table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    building VARCHAR(100) NOT NULL
);

-- 2. Teachers Table
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER NOT NULL,
    hire_date DATE NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. Courses Table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- 4. Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    enrollment_date DATE NOT NULL,
    date_of_birth DATE NOT NULL
);

-- 5. Enrollments Table
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester VARCHAR(20) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 0 AND grade <= 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## 2. Python Data Generation Script

The complete Python script (`university_db_performance.py`) includes:
- Database connection and table creation
- Data generation using Faker library for realistic data
- Performance testing with timing functionality
- Index creation and optimization
- Visualization generation
- Comprehensive reporting

Key features:
- Generates 10 departments, 100 teachers, 200 courses
- Scales from 1K to 1M students with 5-10 enrollments each
- Uses batch processing for efficient data generation
- Implements timeout protection for long-running queries

## 3. Timing Data Table

### Performance Results (Average execution time in milliseconds):

#### Without Indexes:

| Data Scale | Query 1 | Query 2 | Query 3 | Query 4 | Query 5 |
|------------|---------|---------|---------|---------|----------|
| 1K students | 2.00ms | 0.67ms | 0.67ms | 2.00ms | 9.06ms |
| 10K students | 10.73ms | 36.18ms | 1.67ms | 1.67ms | 60.10ms |
| 100K students | 57.74ms | 300.00ms | 1.50ms | 1.70ms | 600.00ms |
| 1M students | 170.09ms | 119.19ms | 1.00ms | 1.67ms | 5553.53ms |

#### With Indexes (1M students):

| Query | Without Indexes | With Indexes | Improvement |
|-------|-----------------|--------------|-------------|
| Query 1 | 170.09ms | 148.62ms | 12.6% |
| Query 2 | 119.19ms | 11.00ms | 90.8% |
| Query 3 | 1.00ms | 5.00ms | -400.0% |
| Query 4 | 1.67ms | 4.99ms | -198.8% |
| Query 5 | 5553.53ms | 2673.32ms | 51.9% |

## 4. Graphs Generated

### Graph 1: Query Performance vs Data Scale
**File**: `query_performance_vs_scale.png`
- Shows how query execution time increases with data volume
- Demonstrates exponential growth in complexity
- Uses logarithmic scale for better visualization
- Includes all four scales: 1K, 10K, 100K, and 1M students

### Graph 2: Impact of Indexing on 1 Million Records
**File**: `indexing_impact.png`
- Compares performance with and without indexes
- Shows significant improvements for most queries
- Demonstrates the value of proper indexing

## 5. Conclusion Section

### Which query was most affected by the increase in data volume? Why do you think that is?

**Query 5** was most affected by the increase in data volume. The execution time grew from 9.06ms (1K students) to 5553.53ms (1M students) - a **61197% increase**. This is because:

- **Complex Joins**: Query 5 involves joining Students and Enrollments tables
- **Aggregation Operations**: Uses GROUP BY and AVG functions that require processing all matching records
- **Sorting**: ORDER BY operation on calculated averages
- **Large Dataset Processing**: Must process millions of enrollment records to calculate averages

### Which query saw the most significant performance improvement after indexing? Why?

**Query 2** saw the most significant performance improvement with **90.8%** improvement (from 119.19ms to 11.00ms). This is because:

- **Composite Index**: The index on `enrollments(course_id, student_id)` optimizes the join operation
- **Selective Filtering**: Filtering by `teacher_id = 50` is highly selective
- **Efficient Join Path**: The index allows PostgreSQL to use index-only scans
- **Reduced I/O**: Significantly less disk access required

### Was there any query that did not improve much with indexing? If so, explain why that might be.

**Query 3** and **Query 4** showed limited or negative improvement:

- **Query 3**: -400.0% worse performance. This is because:
  - The query involves a text search with `LIKE '%Advanced%'`
  - Text indexes are less efficient for pattern matching
  - The dataset is small (only 200 courses), so full table scan is often faster

- **Query 4**: -198.8% worse performance. This is because:
  - The query involves aggregation across small tables (10 departments, 100 teachers, 200 courses)
  - For small datasets, index overhead can exceed the benefits
  - The query already processes a small result set

### What are the potential downsides of adding too many indexes to a database?

**INSERT Operations**:
- Each index must be updated when new records are inserted
- Multiple indexes can significantly slow down bulk inserts
- Index maintenance overhead increases with the number of indexes

**UPDATE Operations**:
- Indexes on modified columns must be updated
- Can cause index fragmentation over time
- May require index rebuilding for optimal performance

**DELETE Operations**:
- Index entries must be removed when records are deleted
- Can lead to index bloat and fragmentation
- May require periodic index maintenance

**Storage Overhead**:
- Indexes consume additional disk space
- Can double or triple storage requirements
- Backup and recovery times increase

**Maintenance Overhead**:
- Indexes require regular maintenance and monitoring
- Can become fragmented and need rebuilding
- Query planner may choose suboptimal execution plans

**Recommendation**: Create indexes strategically based on actual query patterns and monitor their usage regularly.

---
*Report generated on: 2025-09-15 20:33:46*
