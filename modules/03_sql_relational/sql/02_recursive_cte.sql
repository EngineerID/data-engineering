-- Silberschatz — WITH RECURSIVE for hierarchical queries.
DROP TABLE IF EXISTS retail.product_hierarchy CASCADE;
CREATE TABLE retail.product_hierarchy (
    product_key INT PRIMARY KEY,
    parent_key INT,
    level INT NOT NULL
);

INSERT INTO retail.product_hierarchy (product_key, parent_key, level)
SELECT
    product_key,
    NULL::INT,
    1
FROM retail.dim_product
WHERE product_key <= 50;

INSERT INTO retail.product_hierarchy (product_key, parent_key, level)
SELECT
    p.product_key,
    (p.product_key - 1) / 10,
    2
FROM retail.dim_product AS p
WHERE p.product_key > 50 AND p.product_key <= 200;

INSERT INTO retail.product_hierarchy (product_key, parent_key, level)
SELECT
    p.product_key,
    (p.product_key - 1) / 10,
    3
FROM retail.dim_product AS p
WHERE p.product_key > 200;

DROP VIEW IF EXISTS retail.v_category_tree;
CREATE VIEW retail.v_category_tree AS
WITH RECURSIVE tree AS (
    SELECT product_key, parent_key, level, product_key AS root_key
    FROM retail.product_hierarchy
    WHERE parent_key IS NULL
    UNION ALL
    SELECT h.product_key, h.parent_key, h.level, t.root_key
    FROM retail.product_hierarchy AS h
    JOIN tree AS t ON h.parent_key = t.product_key
)
SELECT * FROM tree;
