# Redis-Based Helpdesk Ticketing System 🎫

A comprehensive helpdesk ticketing system built with Redis Cloud, demonstrating advanced NoSQL database operations, real-time data management, and CRUD operations for enterprise-level applications.

## 🎯 Project Overview

This project implements a full-featured helpdesk ticketing system using Redis as the primary database. It showcases modern NoSQL database patterns, including document storage, indexing, querying, and real-time data operations commonly used in enterprise ticketing platforms.

### Key Features
- **User Management**: Customer and agent profiles with role-based access
- **Ticket Management**: Complete ticket lifecycle from creation to resolution
- **Queue System**: Efficient ticket routing and prioritization
- **Audit Logging**: Comprehensive activity tracking and history
- **Search & Indexing**: Fast ticket discovery and filtering
- **Data Integrity**: Validation and consistency checks

## 🛠️ Technology Stack

- **Database**: Redis Cloud (NoSQL)
- **Language**: Python 3.9+
- **Libraries**: 
  - `redis-py` - Redis client for Python
  - `python-dotenv` - Environment configuration management
- **Tools**: RedisInsight for database visualization and CLI operations

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.9 or higher installed
- Redis Cloud account and database instance
- RedisInsight installed for database management

### Installation

```bash
pip install redis python-dotenv
```

## ⚙️ Configuration

Create a `.env` file in the project root with your Redis Cloud credentials:

```env
REDIS_HOST=your_redis_cloud_host
REDIS_PORT=your_redis_port
REDIS_USERNAME=default
REDIS_PASSWORD=your_redis_password
REDIS_SSL=false
```

**Note**: Set `REDIS_SSL=false` for Redis Cloud connections to avoid SSL handshake issues.

## 📁 Project Structure

```
lab03/
├── helpdesk_conn.py              # Redis connection handler
├── seed_helpdesk.py              # Database initialization & sample data
├── read_tasks.py                 # READ operations & queries
├── update_tasks.py               # UPDATE operations & modifications
├── delete_tasks.py               # DELETE operations & cleanup
├── checks.py                     # Data validation & integrity checks
├── models.py                     # Data models & key patterns
├── redisinsight_cli_commands.txt # RedisInsight CLI commands
└── README.md                     # Project documentation
```

### File Descriptions

| File | Purpose | Functionality |
|------|---------|---------------|
| `helpdesk_conn.py` | Database Connection | Manages Redis connection with SSL/non-SSL support |
| `seed_helpdesk.py` | Data Initialization | Creates users, agents, tickets, queues, and indexes |
| `read_tasks.py` | Query Operations | Implements search, filtering, and data retrieval |
| `update_tasks.py` | Modification Operations | Handles ticket updates, status changes, assignments |
| `delete_tasks.py` | Cleanup Operations | Manages data deletion and cleanup procedures |
| `checks.py` | Data Validation | Ensures data integrity and consistency |
| `models.py` | Data Models | Defines key patterns and helper functions |

## 🚀 Getting Started

### Step 1: Test Connection
```bash
python helpdesk_conn.py
```
Expected output: `PING -> True`

### Step 2: Initialize Database
```bash
python seed_helpdesk.py
```
This creates sample users, agents, tickets, and sets up indexes.

### Step 3: Run Operations
Execute the following in order to see the complete system in action:

```bash
# Read operations - queries and data retrieval
python read_tasks.py

# Update operations - modify tickets and user data
python update_tasks.py

# Delete operations - cleanup and data removal
python delete_tasks.py

# Validation - check data integrity
python checks.py
```

## 🔍 Key Features Demonstrated

### 1. **Data Modeling**
- JSON document storage for complex objects
- Hash structures for user profiles
- List structures for queues and logs
- Set operations for categories and tags

### 2. **Indexing & Search**
- Secondary indexes for fast lookups
- Range queries for dates and priorities
- Text search capabilities
- Composite key patterns

### 3. **CRUD Operations**
- **Create**: Add new tickets, users, and agents
- **Read**: Query tickets by status, priority, agent
- **Update**: Modify ticket details, assign agents
- **Delete**: Remove resolved tickets, cleanup data

### 4. **Real-time Operations**
- Ticket queue management
- Status tracking and updates
- Activity logging and audit trails

## 🧪 Testing & Validation

The project includes comprehensive testing through:

- **Connection Testing**: Verify Redis connectivity
- **Data Integrity Checks**: Ensure referential integrity
- **Operation Validation**: Confirm CRUD operations work correctly
- **Performance Testing**: Measure query response times

## 🎓 Learning Outcomes

This project demonstrates:
- NoSQL database design patterns
- Redis data structures and operations
- Python Redis client usage
- Environment configuration management
- Database connection handling
- Error handling and debugging
- Real-world application architecture

## 🔧 Troubleshooting

### Common Issues

1. **SSL Connection Errors**: Set `REDIS_SSL=false` in `.env`
2. **Authentication Errors**: Verify username/password in Redis Cloud
3. **Connection Timeouts**: Check network connectivity and Redis Cloud status

### RedisInsight CLI

Use the commands in `redisinsight_cli_commands.txt` for direct database inspection and debugging.

## 🤝 Contributing

This project is part of a Big Data laboratory assignment. Feel free to fork and extend the functionality for your own learning purposes.

## 📄 License

This project is created for educational purposes as part of university coursework.

---

**Author**: Usman Ahmad </br>
**Course**: Big Data Analytics - Semester 7  
**Institution**: PUCIT, PU
