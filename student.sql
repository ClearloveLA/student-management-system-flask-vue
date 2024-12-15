CREATE DATABASE student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use student_db;
-- 用户表(管理员/普通用户)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 学生信息表
CREATE TABLE students (
    id VARCHAR(20) PRIMARY KEY,  -- 学号
    name VARCHAR(50) NOT NULL,
    gender ENUM('男','女') NOT NULL,
    age INT,
    class_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    enrollment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 操作日志表
CREATE TABLE operation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    operation_type VARCHAR(20),
    operation_desc TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from users;
select * from students;
select * from operation_logs;