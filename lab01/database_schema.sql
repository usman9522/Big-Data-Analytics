-- University Database Schema
-- This script creates the university database and all required tables

-- Create database (run this separately if needed)
-- CREATE DATABASE university_db;

-- Connect to university_db and create tables
\c university_db;

-- 1. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    building VARCHAR(100) NOT NULL
);

-- 2. Teachers Table
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER NOT NULL,
    hire_date DATE NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- 4. Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    enrollment_date DATE NOT NULL,
    date_of_birth DATE NOT NULL
);

-- 5. Enrollments Table (Junction table)
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester VARCHAR(20) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 0 AND grade <= 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Create indexes for better performance (Phase 2)
-- These will be created after initial testing

-- Index on Students table for enrollment_date
CREATE INDEX IF NOT EXISTS idx_students_enrollment_date ON students(enrollment_date);

-- Indexes on Enrollments table
CREATE INDEX IF NOT EXISTS idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course_id ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_semester ON enrollments(semester);

-- Indexes on Courses table
CREATE INDEX IF NOT EXISTS idx_courses_teacher_id ON courses(teacher_id);
CREATE INDEX IF NOT EXISTS idx_courses_course_name ON courses(course_name);

-- Index on Teachers table
CREATE INDEX IF NOT EXISTS idx_teachers_department_id ON teachers(department_id);
