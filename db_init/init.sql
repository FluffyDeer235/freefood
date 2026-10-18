CREATE TABLE IF NOT EXISTS events (
    id VARCHAR PRIMARY KEY,
    title TEXT,
    link TEXT,
    has_food BOOLEAN,
    is_free BOOLEAN,
    start_datetime TIMESTAMP WITH TIME ZONE,
    end_datetime TIMESTAMP WITH TIME ZONE
);
