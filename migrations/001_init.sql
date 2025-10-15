-- Enable UUIDs if needed
create extension if not exists "uuid-ossp";

-- Basic entities
create table if not exists users (
    id serial primary key,
    telegram_id bigint unique,
    name text,
    phone text,
    role text default 'user',
    created_at timestamptz default now()
);

create table if not exists categories (
    id serial primary key,
    name text not null unique
);

create table if not exists subcategories (
    id serial primary key,
    category_id int not null references categories(id) on delete cascade,
    name text not null,
    unique(category_id, name)
);

create table if not exists products (
    id serial primary key,
    name text not null,
    description text,
    price numeric(12,2) not null default 0,
    stock int not null default 0,
    category_id int references categories(id) on delete set null,
    subcategory_id int references subcategories(id) on delete set null,
    created_at timestamptz default now()
);

create table if not exists orders (
    id serial primary key,
    user_id int not null references users(id) on delete cascade,
    total numeric(12,2) not null default 0,
    status text not null default 'new',
    payment_status text not null default 'pending',
    created_at timestamptz default now()
);

create table if not exists order_items (
    id serial primary key,
    order_id int not null references orders(id) on delete cascade,
    product_id int not null references products(id),
    quantity int not null default 1,
    price numeric(12,2) not null default 0
);

create table if not exists user_roles (
    id serial primary key,
    user_id int not null references users(id) on delete cascade,
    role text not null,
    created_at timestamptz default now()
);

-- Minimal seed
insert into categories(name) values ('General')
on conflict (name) do nothing;
