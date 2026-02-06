# Database Schema Design Skill Specification

## Table of Contents
1. [Introduction](#introduction)
2. [Entity Relationship Identification](#entity-relationship-identification)
3. [Data Type Selection](#data-type-selection)
4. [Normalization Principles](#normalization-principles)
5. [Constraint Definitions](#constraint-definitions)
6. [Migration Strategies](#migration-strategies)
7. [Performance Optimization Techniques](#performance-optimization-techniques)
8. [Schema Creation Best Practices](#schema-creation-best-practices)
9. [Indexing Strategies](#indexing-strategies)
10. [Scalability Considerations](#scalability-considerations)
11. [Maintainability Guidelines](#maintainability-guidelines)
12. [Example SQL Structures](#example-sql-structures)

## Introduction

Database schema design is a critical skill for software developers and database administrators. A well-designed schema ensures data integrity, optimal performance, and maintainability. This specification outlines the essential competencies required for effective database schema design, covering everything from initial conceptual modeling to production deployment and optimization.

### Key Objectives
- Design normalized, efficient database schemas
- Implement proper constraints and relationships
- Plan and execute safe schema migrations
- Optimize for performance and scalability
- Maintain high standards of data integrity

## Entity Relationship Identification

### Core Concepts
Entity relationship identification involves recognizing the key entities in a business domain and defining how they relate to each other. This process forms the foundation of any database schema.

### Types of Relationships
- **One-to-One (1:1)**: Each record in Table A relates to exactly one record in Table B
- **One-to-Many (1:N)**: One record in Table A can relate to multiple records in Table B
- **Many-to-Many (N:M)**: Multiple records in Table A can relate to multiple records in Table B

### Identification Process
1. **Domain Analysis**: Understand the business requirements and identify core entities
2. **Attribute Discovery**: Determine the properties of each entity
3. **Relationship Mapping**: Define how entities interact with each other
4. **Cardinality Definition**: Specify the minimum and maximum number of relationships
5. **Dependency Analysis**: Identify which entities depend on others for existence

### Example Entity Relationship Model
```
Customer (1) ----< Order (N)
Order (1) ----< OrderItem (N)
Product (1) ----< OrderItem (N)
Category (1) ----< Product (N)
```

### Best Practices
- Use clear, consistent naming conventions for entities and relationships
- Document business rules that govern relationships
- Consider future growth when defining relationships
- Normalize relationships to reduce redundancy

## Data Type Selection

### Fundamental Principles
Selecting appropriate data types is crucial for storage efficiency, performance, and data integrity. The right choice impacts storage space, query performance, and validation capabilities.

### Common Data Types

#### String Types
- **VARCHAR(n)**: Variable-length character strings (recommended for most text)
- **CHAR(n)**: Fixed-length character strings (use when length is consistent)
- **TEXT**: Large text fields (for descriptions, content, etc.)

#### Numeric Types
- **INTEGER**: Whole numbers (use for IDs, counts, quantities)
- **DECIMAL(p,s)**: Precise decimal numbers (use for monetary values)
- **FLOAT/REAL**: Approximate numeric values (use for scientific calculations)

#### Date/Time Types
- **DATE**: Date values (YYYY-MM-DD)
- **TIME**: Time values (HH:MM:SS)
- **TIMESTAMP**: Date and time with timezone awareness
- **INTERVAL**: Time periods

#### Boolean Types
- **BOOLEAN**: True/false values (use for flags, statuses)

#### Binary Types
- **BLOB/BYTEA**: Binary large objects (images, files)
- **VARBINARY**: Variable-length binary data

### Selection Guidelines
- Choose the smallest data type that accommodates your data range
- Use appropriate precision for numeric types
- Consider storage implications for frequently accessed columns
- Account for internationalization requirements
- Plan for future data growth

### Example Data Type Selection
```sql
-- Good choices for common scenarios
customer_id INTEGER PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
balance DECIMAL(10,2),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
is_active BOOLEAN DEFAULT TRUE,
profile_image BYTEA,
description TEXT
```

## Normalization Principles

### Purpose of Normalization
Normalization reduces data redundancy and improves data integrity by organizing fields and tables according to specific rules.

### Normal Forms

#### First Normal Form (1NF)
- Eliminate repeating groups
- Each cell contains atomic (indivisible) values
- Each record is unique

#### Second Normal Form (2NF)
- Meet all 1NF requirements
- Remove partial dependencies (non-key attributes dependent on part of composite key)

#### Third Normal Form (3NF)
- Meet all 2NF requirements
- Remove transitive dependencies (non-key attributes dependent on other non-key attributes)

### Denormalization Considerations
While normalization is generally beneficial, consider denormalization for:
- Read-heavy applications
- Complex reporting requirements
- Performance optimization needs
- Careful balance between performance and data integrity

### Practical Normalization Example
```sql
-- Before normalization (denormalized)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_address TEXT,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2),
    quantity INTEGER,
    order_date DATE
);

-- After normalization
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(12,2)
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);
```

## Constraint Definitions

### Types of Constraints

#### Primary Key Constraints
- Uniquely identifies each record in a table
- Cannot contain NULL values
- Automatically creates an index

#### Foreign Key Constraints
- Maintains referential integrity between tables
- Ensures referenced records exist
- Can cascade updates/deletions

#### Unique Constraints
- Ensures column values are unique across the table
- Allows NULL values (unless combined with NOT NULL)

#### Check Constraints
- Validates data against specific conditions
- Enforces business rules at the database level

#### Not Null Constraints
- Prevents NULL values in specified columns
- Ensures data completeness

### Constraint Implementation Examples
```sql
-- Primary key constraint
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

-- Foreign key constraint with cascading actions
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Check constraint for business rule enforcement
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2) CHECK (salary > 0),
    department VARCHAR(50) CHECK (department IN ('IT', 'HR', 'Finance', 'Marketing')),
    hire_date DATE CHECK (hire_date <= CURRENT_DATE)
);

-- Composite unique constraint
CREATE TABLE user_profiles (
    user_id INTEGER REFERENCES users(id),
    profile_type VARCHAR(20),
    profile_data JSONB,
    UNIQUE(user_id, profile_type)
);
```

### Constraint Naming Conventions
- Use descriptive names that indicate purpose
- Follow consistent naming patterns
- Include table and constraint type in name
- Example: `fk_orders_customer_id`, `chk_products_price_positive`

## Migration Strategies

### Planning Phase
- Assess current schema and identify changes needed
- Evaluate impact on existing data and applications
- Plan rollback procedures
- Schedule maintenance windows

### Migration Approaches

#### Blue-Green Deployment
- Maintain two identical production environments
- Deploy schema changes to inactive environment
- Switch traffic to new environment after validation
- Provides zero-downtime capability

#### Canary Release
- Gradually roll out changes to subset of users
- Monitor performance and stability
- Expand rollout based on success metrics
- Minimizes risk of widespread issues

#### Feature Flags
- Use application-level flags to control schema usage
- Allow gradual transition between old and new schemas
- Enable quick rollback if issues arise

### Migration Best Practices
- Always backup data before migrations
- Test migrations thoroughly in staging environment
- Use version control for migration scripts
- Implement automated rollback procedures
- Monitor application performance post-migration
- Document all migration steps and decisions

### Example Migration Script Template
```sql
-- Migration: Add email verification to users table
-- Version: 2023.01.01.001
-- Author: Database Team

-- Pre-migration checks
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users') THEN
        RAISE NOTICE 'Users table exists, proceeding with migration';
    ELSE
        RAISE EXCEPTION 'Users table does not exist';
    END IF;
END $$;

-- Begin transaction
BEGIN;

-- Add new column with default value
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

-- Create index for performance
CREATE INDEX idx_users_email_verified ON users(email_verified);

-- Update existing records if needed
UPDATE users SET email_verified = TRUE WHERE email IS NOT NULL AND LENGTH(TRIM(email)) > 0;

-- Add constraint
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

-- Commit transaction
COMMIT;

-- Post-migration validation
DO $$
DECLARE
    count INTEGER;
BEGIN
    SELECT COUNT(*) INTO count FROM users WHERE email_verified = FALSE;
    RAISE NOTICE '% users have unverified emails', count;
END $$;
```

## Performance Optimization Techniques

### Query Optimization
- Use EXPLAIN/ANALYZE to understand query execution plans
- Optimize JOIN operations and subqueries
- Limit result sets with appropriate WHERE clauses
- Use appropriate indexing strategies

### Storage Optimization
- Choose appropriate data types to minimize storage
- Implement partitioning for large tables
- Use compression where beneficial
- Regularly analyze and vacuum tables

### Connection Management
- Implement connection pooling
- Optimize connection timeouts
- Monitor active connections
- Use appropriate isolation levels

### Performance Monitoring
- Track slow query logs
- Monitor database performance metrics
- Use database profiling tools
- Implement alerting for performance degradation

### Example Performance Optimization
```sql
-- Before optimization (inefficient query)
SELECT u.name, p.title, c.content
FROM users u, posts p, comments c
WHERE u.id = p.user_id AND p.id = c.post_id
AND u.status = 'active'
ORDER BY c.created_at DESC
LIMIT 10;

-- After optimization (optimized query with proper joins and indexes)
-- Indexes needed:
CREATE INDEX idx_posts_user_status ON posts USING btree (user_id) WHERE (SELECT status FROM users WHERE id = user_id) = 'active';
CREATE INDEX idx_comments_post_created ON comments (post_id, created_at DESC);

-- Optimized query
SELECT u.name, p.title, c.content
FROM users u
INNER JOIN posts p ON u.id = p.user_id
INNER JOIN comments c ON p.id = c.post_id
WHERE u.status = 'active'
ORDER BY c.created_at DESC
LIMIT 10;
```

## Schema Creation Best Practices

### Naming Conventions
- Use lowercase names with underscores (snake_case)
- Use plural names for tables (users, products)
- Prefix related tables consistently (user_sessions, user_preferences)
- Use descriptive names that reflect purpose

### Documentation Standards
- Include table and column descriptions
- Document business rules and constraints
- Maintain ERD diagrams
- Keep schema documentation in version control

### Security Considerations
- Implement proper access controls
- Use parameterized queries to prevent injection
- Encrypt sensitive data
- Regular security audits

### Version Control
- Store schema definitions in version control
- Use migration scripts for changes
- Tag schema versions with releases
- Maintain changelog for schema evolution

## Indexing Strategies

### Index Types

#### B-tree Indexes
- Default index type for most use cases
- Efficient for equality and range queries
- Good for sorting operations

#### Hash Indexes
- Fast for equality comparisons
- Not suitable for range queries
- Smaller than B-tree indexes

#### Partial Indexes
- Index only subset of rows meeting condition
- Reduces storage overhead
- Improves performance for targeted queries

#### Expression Indexes
- Index computed values from expressions
- Useful for complex queries
- Can improve performance significantly

### Index Selection Guidelines
- Index foreign keys used in JOINs
- Index columns frequently used in WHERE clauses
- Consider composite indexes for multi-column queries
- Monitor index usage and remove unused indexes
- Balance query performance with insert/update costs

### Example Indexing Strategy
```sql
-- Basic indexes for common queries
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_date ON orders (order_date);
CREATE INDEX idx_products_category ON products (category_id);

-- Composite index for multi-column queries
CREATE INDEX idx_orders_date_status ON orders (order_date, status);

-- Partial index for active records only
CREATE INDEX idx_users_active ON users (last_login) WHERE status = 'active';

-- Expression index for case-insensitive searches
CREATE INDEX idx_users_lower_email ON users (LOWER(email));

-- Covering index for frequently accessed columns
CREATE INDEX idx_orders_covering ON orders (customer_id, order_date, total_amount) 
INCLUDE (status, payment_method);
```

## Scalability Considerations

### Horizontal Scaling
- Database sharding strategies
- Read replicas for query distribution
- Caching layers integration
- Load balancing approaches

### Vertical Scaling
- Hardware optimization
- Memory allocation tuning
- Storage performance considerations
- CPU and I/O optimization

### Partitioning Strategies
- Range partitioning by date
- Hash partitioning for even distribution
- List partitioning for categorical data
- Subpartitioning for complex scenarios

### Cloud-Native Considerations
- Serverless database options
- Auto-scaling capabilities
- Multi-region deployment
- Cost optimization strategies

## Maintainability Guidelines

### Code Organization
- Group related tables logically
- Use consistent formatting
- Comment complex queries and constraints
- Separate DDL and DML operations

### Change Management
- Implement peer review for schema changes
- Use automated testing for migrations
- Maintain rollback procedures
- Document change rationale

### Monitoring and Maintenance
- Regular performance monitoring
- Automated backup procedures
- Schema evolution tracking
- Data quality validation

## Example SQL Structures

### Complete E-commerce Schema Example
```sql
-- Users and authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Addresses for users
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type VARCHAR(20) CHECK (type IN ('billing', 'shipping')) NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Categories for products
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id INTEGER,
    slug VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category_id INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    cost DECIMAL(10,2) CHECK (cost >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    weight DECIMAL(8,2),
    dimensions JSONB, -- Store length, width, height
    brand VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    tax_amount DECIMAL(10,2) DEFAULT 0 CHECK (tax_amount >= 0),
    shipping_cost DECIMAL(10,2) DEFAULT 0 CHECK (shipping_cost >= 0),
    discount_amount DECIMAL(10,2) DEFAULT 0 CHECK (discount_amount >= 0),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
    currency CHAR(3) DEFAULT 'USD',
    billing_address_id INTEGER,
    shipping_address_id INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (billing_address_id) REFERENCES addresses(id),
    FOREIGN KEY (shipping_address_id) REFERENCES addresses(id)
);

-- Order items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(12,2) NOT NULL CHECK (total_price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Inventory tracking
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE NOT NULL,
    reserved_quantity INTEGER DEFAULT 0 CHECK (reserved_quantity >= 0),
    available_quantity INTEGER GENERATED ALWAYS AS (stock_quantity - reserved_quantity) STORED,
    reorder_level INTEGER DEFAULT 10,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_products_category ON products (category_id);
CREATE INDEX idx_products_sku ON products (sku);
CREATE INDEX idx_order_items_order ON order_items (order_id);
CREATE INDEX idx_inventory_product ON inventory (product_id);

-- Triggers for maintaining data consistency
CREATE OR REPLACE FUNCTION update_inventory_on_order()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE inventory 
        SET reserved_quantity = reserved_quantity + NEW.quantity
        WHERE product_id = NEW.product_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE inventory 
        SET reserved_quantity = reserved_quantity - OLD.quantity
        WHERE product_id = OLD.product_id;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE inventory 
        SET reserved_quantity = reserved_quantity - OLD.quantity + NEW.quantity
        WHERE product_id = NEW.product_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_inventory
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW EXECUTE FUNCTION update_inventory_on_order();
```

### Sample Queries Demonstrating Best Practices
```sql
-- Efficient query with proper indexing
SELECT p.name, p.price, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = TRUE
  AND c.is_active = TRUE
  AND p.price BETWEEN 10 AND 100
ORDER BY p.price ASC
LIMIT 20;

-- Complex query with aggregation
SELECT 
    u.first_name,
    u.last_name,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.first_name, u.last_name
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC
LIMIT 10;

-- Safe update with proper constraints
UPDATE products 
SET stock_quantity = GREATEST(stock_quantity - 1, 0)
WHERE id = $1 
  AND stock_quantity > 0
RETURNING stock_quantity;

-- Transaction for complex operation
BEGIN;
UPDATE inventory 
SET reserved_quantity = reserved_quantity - 1
WHERE product_id = $1 AND reserved_quantity > 0;

UPDATE products 
SET stock_quantity = stock_quantity - 1
WHERE id = $1 AND stock_quantity > 0;

-- Verify both updates succeeded
GET DIAGNOSTICS affected_rows = ROW_COUNT;
IF affected_rows = 0 THEN
    ROLLBACK;
    RAISE EXCEPTION 'Insufficient stock or inventory reservation failed';
END IF;

COMMIT;
```

This comprehensive specification provides a solid foundation for database schema design skills, covering all essential aspects from initial design through implementation and optimization.