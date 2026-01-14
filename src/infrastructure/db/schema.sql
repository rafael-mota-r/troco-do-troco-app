CREATE TABLE IF NOT EXISTS ingredients (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    quantity TEXT NOT NULL,
    total_cost TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
    id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS recipe_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id TEXT NOT NULL,
    recipe_id TEXT NOT NULL,
    quantity TEXT NOT NULL,

    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE RESTRICT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    price TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    recipe_id TEXT NOT NULL,
    ratio TEXT NOT NULL,

    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE RESTRICT,
    UNIQUE (product_id, recipe_id)
);



