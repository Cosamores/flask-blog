-- Insert users with avatars
INSERT INTO user (username, password, avatar)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'avatar1.png'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'avatar2.png');

-- Insert posts
INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2024-01-01 00:00:00'),
  ('another title', 'another' || x'0a' || 'body', 2, '2024-01-02 00:00:00');

-- Insert likes
INSERT INTO like (user_id, post_id)
VALUES
  (1, 1),  -- User 'test' likes their own post
  (2, 1);  -- User 'other' likes the post by 'test'