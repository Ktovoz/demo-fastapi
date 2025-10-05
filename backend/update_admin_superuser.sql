-- 更新admin用户的is_superuser状态
UPDATE users
SET is_superuser = 1
WHERE email = 'admin@example.com' OR username = 'admin';

-- 检查更新结果
SELECT id, username, email, is_superuser FROM users
WHERE email = 'admin@example.com' OR username = 'admin';