# University Database Performance Analysis

This project analyzes the impact of data scale and indexing on database query performance using PostgreSQL.

## Overview

The lab demonstrates how database performance is affected by:
1. **Data Volume**: Testing queries across different scales (1K, 10K, 100K, 1M students)
2. **Indexing**: Comparing performance with and without database indexes

## Prerequisites

- PostgreSQL installed and running
- Python 3.7+
- Required Python packages (see requirements.txt)

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Database
```bash
python setup_database.py
```
This will:
- Create the `uni` database
- Generate a configuration file with your database credentials
- Test the connection

### 3. Run the Performance Analysis
```bash
python university_db_performance.py
```

## What the Analysis Does

### Database Schema
Creates 5 tables with realistic relationships:
- **departments**: 10 academic departments
- **teachers**: 100 teachers distributed across departments
- **courses**: 200 courses with random teacher assignments
- **students**: Variable number (1K to 1M) with realistic data
- **enrollments**: Junction table linking students to courses (5-10 enrollments per student)

### Performance Tests
Runs 5 different query types across 4 data scales:

1. **Query 1**: Simple filter on students table
2. **Query 2**: Multi-table join with filtering
3. **Query 3**: Text search with joins
4. **Query 4**: Aggregation with GROUP BY
5. **Query 5**: Complex query with joins, aggregation, filtering, and sorting

### Indexing Analysis
- Tests performance without indexes
- Creates strategic indexes based on query patterns
- Measures performance improvement with indexes

## Output Files

After running the analysis, you'll get:

1. **lab_report.md**: Comprehensive report with:
   - Database schema
   - Performance results tables
   - Analysis and conclusions
   - Recommendations

2. **query_performance_vs_scale.png**: Graph showing how query performance degrades with data volume

3. **indexing_impact.png**: Graph showing the performance improvement from indexing

## Expected Results

- **Query Performance Degradation**: Execution times increase significantly with data volume
- **Indexing Benefits**: Dramatic performance improvements, especially for join operations
- **Query Complexity Impact**: More complex queries show greater performance variations

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check your database credentials in `db_config.py`
- Verify the `uni` database exists

### Memory Issues with Large Datasets
- The 1M student dataset requires significant memory
- Consider running on a machine with at least 8GB RAM
- You can modify the scales in the script if needed

### Performance Issues
- Large data generation can take time (especially 1M students)
- Consider running overnight for the full analysis
- You can test with smaller scales first

## Customization

You can modify:
- **Data scales**: Change the number of students in each scale
- **Query complexity**: Add or modify the test queries
- **Index strategies**: Experiment with different indexing approaches
- **Visualization**: Customize the graphs and analysis

## Learning Objectives

After completing this lab, you should understand:
- How data volume affects query performance
- The importance of strategic database indexing
- Trade-offs between read and write performance
- Query optimization techniques
- Database performance monitoring and analysis

## Files Structure

```
├── university_db_performance.py  # Main analysis script
├── setup_database.py            # Database setup utility
├── database_schema.sql          # Database schema definition
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── db_config.py                 # Database configuration (generated)
├── lab_report.md                # Generated report
├── query_performance_vs_scale.png  # Generated graph 1
└── indexing_impact.png          # Generated graph 2
```
