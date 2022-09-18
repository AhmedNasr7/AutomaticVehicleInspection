/* Replace with your SQL commands */

CREATE TABLE vehicles (
    id SERIAL PRIMARY key,
    image text not null,
    name varchar(100) not null,
    model integer not null,
    driver_name varchar(100) not null,
    license_number varchar(100) unique not null
);

CREATE TABLE damagesinfo (
    id SERIAL PRIMARY KEY,
    damage_name varchar(100) NOT NULL,
    damage_cost numeric not null,
    healthy numeric not null
);

CREATE TABLE damages (
    id SERIAL PRIMARY KEY,
    damaged boolean not null,
    vehicle_id INTEGER REFERENCES vehicles(id)
);

CREATE TABLE vehicledamages (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id),
    damage_id INTEGER REFERENCES damagesinfo(id)
);