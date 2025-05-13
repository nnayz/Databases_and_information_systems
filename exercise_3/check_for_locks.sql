SELECT
    relation::regclass,
    mode,
    granted
FROM
    pg_locks
WHERE
    relation::regclass = 'sheet3'::regclass;