-- Drop tables if exists (development)
DROP TABLE IF EXISTS task_logs CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Table: users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'project_manager',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    assigned_to VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Not_Started',
    priority VARCHAR(20) DEFAULT 'Medium',
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraint status
    CONSTRAINT chk_status CHECK (status IN ('Not_Started', 'In_Progress', 'Completed')),
    
    -- Constraint priority
    CONSTRAINT chk_priority CHECK (priority IN ('Low', 'Medium', 'High'))
);

-- Table: task_logs
CREATE TABLE task_logs (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    change_reason TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraint status
    CONSTRAINT chk_log_old_status CHECK (old_status IN ('Not_Started', 'In_Progress', 'Completed')),
    CONSTRAINT chk_log_new_status CHECK (new_status IN ('Not_Started', 'In_Progress', 'Completed'))
);

-- Indexes query
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_created_by ON tasks(created_by);
CREATE INDEX idx_task_logs_task_id ON task_logs(task_id);
CREATE INDEX idx_task_logs_changed_at ON task_logs(changed_at);

-- Function auto-update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger auto-update updated_at for table users
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger auto-update updated_at for table tasks
CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default user (Project Manager)
INSERT INTO users (username, email, password_hash, full_name, role) 
VALUES (
    'admin',
    'admin@herobusana.com',
    'pbkdf2:sha256:260000$placeholder',
    'Project Manager',
    'project_manager'
);

-- Sample tasks
INSERT INTO TASKS (title, description, assigned_to, status, priority, start_date, due_date, created_by) 
VALUES 
    ('Desain Landing Page', 'Membuat desain landing page untuk website baru', 'Budi Santoso', 'In_Progress', 'High', '2025-10-01', '2025-10-20', 1),
    ('Setup Database', 'Konfigurasi database PostgreSQL untuk production', 'Ani Wijaya', 'Completed', 'High', '2025-09-25', '2025-10-05', 1),
    ('Testing API', 'Testing semua endpoint REST API', 'Citra Dewi', 'Not_Started', 'Medium', '2025-10-15', '2025-10-25', 1),
    ('Dokumentasi Project', 'Membuat dokumentasi lengkap untuk project', 'Doni Pratama', 'In_Progress', 'Low', '2025-10-10', '2025-10-30', 1);

-- Insert sample task logs
INSERT INTO TASK_LOGS (task_id, old_status, new_status, changed_by, change_reason) 
VALUES 
    (1, 'Not_Started', 'In_Progress', 1, 'Task dimulai oleh Budi'),
    (2, 'Not_Started', 'In_Progress', 1, 'Database setup dimulai'),
    (2, 'In_Progress', 'Completed', 1, 'Database berhasil dikonfigurasi'),
    (4, 'Not_Started', 'In_Progress', 1, 'Dokumentasi dimulai');

-- View for dashboard statistics
CREATE OR REPLACE VIEW task_statistics AS
SELECT 
    COUNT(*) as total_tasks,
    COUNT(CASE WHEN status = 'Not_Started' THEN 1 END) as not_started,
    COUNT(CASE WHEN status = 'In_Progress' THEN 1 END) as in_progress,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed,
    COUNT(CASE WHEN due_date < CURRENT_DATE AND status != 'Completed' THEN 1 END) as overdue
FROM tasks;

-- View for team member activity
CREATE OR REPLACE VIEW team_activity AS
SELECT 
    assigned_to,
    COUNT(*) as total_tasks,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN status = 'In_Progress' THEN 1 END) as ongoing_tasks,
    ROUND(
        (COUNT(CASE WHEN status = 'Completed' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(*), 0)) * 100, 2
    ) as completion_rate
FROM tasks
GROUP BY assigned_to
ORDER BY completed_tasks DESC;