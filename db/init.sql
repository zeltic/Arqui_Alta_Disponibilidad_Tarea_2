CREATE TABLE sismos (
    id INT PRIMARY KEY,
    fecha_hora TIMESTAMP,
    ubicacion VARCHAR(255),
    profundidad INTEGER,
    magnitud DECIMAL
);