-- CONFIGURACIÓN INICIAL Y CREACIÓN DE BASE DE DATOS PARA SISTEMA DE INVENTARIO DE EQUIPOS

SET NAMES utf8mb4;
SET sql_safe_updates
= 0;

-- Crear Base de Datos
CREATE DATABASE
IF NOT EXISTS inventario
DEFAULT CHARACTER
SET utf8mb4
DEFAULT
COLLATE utf8mb4_0900_ai_ci;
USE inventario;

--  CREACIÓN DE TABLAS
-- ORDEN: Tablas Padre (Sin FK) -> Tablas con Claves Foráneas


-- Departamentos (Padre 1)
CREATE TABLE
IF NOT EXISTS departamento
(
  id_dpto     INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR
(100) NOT NULL UNIQUE,
  ubicacion   VARCHAR
(150)
) ENGINE=InnoDB;

-- Categorías de equipo (Padre 2)

CREATE TABLE
IF NOT EXISTS categoria_equipo
(
  id_categoria  INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR
(100) NOT NULL UNIQUE,
  descripcion   TEXT,
  vida_util     SMALLINT,
  CONSTRAINT ck_categoria_vida_util CHECK
(vida_util IS NULL OR vida_util >= 0)
) ENGINE=InnoDB;

--  Técnicos (Padre 3)

CREATE TABLE
IF NOT EXISTS tecnico
(
  id_tecnico    INT AUTO_INCREMENT PRIMARY KEY,
  doc_iden      VARCHAR
(40) NOT NULL UNIQUE,
  nombre        VARCHAR
(120) NOT NULL,
  especialidad  VARCHAR
(120),
  telefono      VARCHAR
(30),
  email         VARCHAR
(120) UNIQUE
) ENGINE=InnoDB;

--  Usuarios (Depende de departamento)

CREATE TABLE
IF NOT EXISTS usuario
(
  id_usuario   INT AUTO_INCREMENT PRIMARY KEY,
  doc_ident    VARCHAR
(40) NOT NULL UNIQUE,
  nombre       VARCHAR
(120) NOT NULL,
  rol          VARCHAR
(60),
  email        VARCHAR
(120) UNIQUE,
  id_dpto      INT,
  CONSTRAINT fk_usuario_dpto
    FOREIGN KEY
(id_dpto) REFERENCES departamento
(id_dpto)
    ON
UPDATE CASCADE ON DELETE SET NULL
-- SET NULL porque id_dpto en usuario es opcional
) ENGINE=InnoDB;

--  Equipos (Depende de categoria_equipo y departamento)

CREATE TABLE
IF NOT EXISTS equipo
(
  id_equipo         INT AUTO_INCREMENT PRIMARY KEY,
  serial            VARCHAR
(80) NOT NULL UNIQUE,
  modelo            VARCHAR
(100),
  marca             VARCHAR
(100),
  estado_operativo  ENUM
('operativo','mantenimiento','baja','dañado','otro'),
  fecha_compra      DATE,
  espec_tecnicas    TEXT,
  id_categoria      INT,
  id_dpto           INT,
  CONSTRAINT fk_equipo_categoria
    FOREIGN KEY
(id_categoria) REFERENCES categoria_equipo
(id_categoria)
    ON
UPDATE CASCADE,
  CONSTRAINT fk_equipo_dpto
    FOREIGN KEY
(id_dpto) REFERENCES departamento
(id_dpto)
    ON
UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

--  Asignaciones (Depende de usuario y equipo)

CREATE TABLE
IF NOT EXISTS asignacion
(
  id_asignacion   INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario      INT NOT NULL,
  id_equipo       INT NOT NULL,
  fecha_asign     DATE NOT NULL,
  fecha_devol     DATE,
  observaciones   TEXT,
  CONSTRAINT uq_asign UNIQUE
(id_usuario, id_equipo, fecha_asign),
  CONSTRAINT ck_devolucion CHECK
(fecha_devol IS NULL OR fecha_devol >= fecha_asign),
  CONSTRAINT fk_asign_usuario
    FOREIGN KEY
(id_usuario) REFERENCES usuario
(id_usuario)
    ON
UPDATE CASCADE,
  CONSTRAINT fk_asign_equipo
    FOREIGN KEY
(id_equipo) REFERENCES equipo
(id_equipo)
    ON
UPDATE CASCADE
) ENGINE=InnoDB;

-- Mantenimientos (Depende de equipo y tecnico)

CREATE TABLE
IF NOT EXISTS mantenimiento
(
  id_mnto       INT AUTO_INCREMENT PRIMARY KEY,
  id_equipo     INT NOT NULL,
  id_tecnico    INT,
  fecha_mnto    DATE NOT NULL,
  tipo          VARCHAR
(60),
  descripcion   TEXT,
  CONSTRAINT fk_mnto_equipo
    FOREIGN KEY
(id_equipo) REFERENCES equipo
(id_equipo)
    ON
UPDATE CASCADE,
  CONSTRAINT fk_mnto_tecnico
    FOREIGN KEY
(id_tecnico) REFERENCES tecnico
(id_tecnico)
    ON
UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;


-- ÍNDICES 

CREATE INDEX idx_usuario_dpto ON usuario(id_dpto);
CREATE INDEX idx_equipo_categoria ON equipo(id_categoria);
CREATE INDEX idx_equipo_dpto ON equipo(id_dpto);
CREATE INDEX idx_equipo_estado_dpto ON equipo(estado_operativo, id_dpto);
CREATE INDEX idx_equipo_categoria_estado ON equipo(id_categoria, estado_operativo);
CREATE INDEX idx_asignacion_usuario ON asignacion(id_usuario);
CREATE INDEX idx_asignacion_equipo ON asignacion(id_equipo);
CREATE INDEX idx_asignacion_fechas ON asignacion(fecha_asign, fecha_devol);
CREATE INDEX idx_asign_equipo_fecha ON asignacion(id_equipo, fecha_asign);
CREATE INDEX idx_asign_usuario_fecha ON asignacion(id_usuario, fecha_asign);
CREATE INDEX idx_mantenimiento_equipo ON mantenimiento(id_equipo);
CREATE INDEX idx_mantenimiento_tecnico ON mantenimiento(id_tecnico);
CREATE INDEX idx_mantenimiento_fecha ON mantenimiento(fecha_mnto);
CREATE INDEX idx_mnto_equipo_fecha ON mantenimiento(id_equipo, fecha_mnto);


-- DATOS DE EJEMPLO


-- Departamentos

INSERT INTO departamento
    (nombre, ubicacion)
VALUES
    ('Sistemas', 'Edificio A - Piso 3'),
    ('Contabilidad', 'Edificio B - Piso 2'),
    ('Recursos Humanos', 'Edificio A - Piso 2'),
    ('Logística', 'Bodega Central');

-- Categorías

INSERT INTO categoria_equipo
    (nombre, descripcion, vida_util)
VALUES
    ('Laptop', 'Portátiles para uso de oficina', 36),
    ('Desktop', 'PCs de escritorio', 48),
    ('Impresora', 'Impresoras láser y de inyección', 60),
    ('Monitor', 'Monitores LCD/LED', 72);

-- Usuarios

INSERT INTO usuario
    (doc_ident, nombre, rol, email, id_dpto)
VALUES
    ('CC1001', 'Ana Gómez', 'Analista', 'ana.gomez@empresa.com', 1),
    ('CC1002', 'Luis Pérez', 'Auxiliar', 'luis.perez@empresa.com', 2),
    ('CC1003', 'María Ruiz', 'Coord. RRHH', 'maria.ruiz@empresa.com', 3),
    ('CC1004', 'Carlos Díaz', 'Operador', 'carlos.diaz@empresa.com', 4);

-- Técnicos

INSERT INTO tecnico
    (doc_iden, nombre, especialidad, telefono, email)
VALUES
    ('TC2001', 'Sofía Torres', 'Hardware', '3001234567', 'sofia.torres@empresa.com'),
    ('TC2002', 'Javier Mendoza', 'Impresoras', '3009876543', 'javier.mendoza@empresa.com');

-- Equipos

INSERT INTO equipo
    (serial, modelo, marca, estado_operativo, fecha_compra, espec_tecnicas, id_categoria, id_dpto)
VALUES
    ('LAP-001', 'Latitude 5420', 'Dell', 'operativo', '2023-01-15', 'i5, 16GB, 512GB SSD', 1, 1),
    ('LAP-002', 'ThinkPad T14', 'Lenovo', 'operativo', '2022-11-20', 'i7, 16GB, 1TB SSD', 1, 2),
    ('DES-001', 'OptiPlex 7090', 'Dell', 'mantenimiento', '2021-07-10', 'i5, 16GB, 512GB SSD', 2, 1),
    ('IMP-001', 'LaserJet Pro M404', 'HP', 'operativo', '2020-05-05', 'Láser B/N', 3, 4),
    ('MON-001', 'UltraSharp U2720Q', 'Dell', 'operativo', '2022-02-18', '27" 4K', 4, 1),
    ('LAP-003', 'MacBook Air M2', 'Apple', 'operativo', '2024-02-01', '8CPU, 16GB, 512GB', 1, 3),
    ('DES-002', 'EliteDesk 800', 'HP', 'baja', '2019-03-12', 'i5, 8GB, 256GB SSD', 2, 2);

-- Asignaciones (histórico)

INSERT INTO asignacion
    (id_usuario, id_equipo, fecha_asign, fecha_devol, observaciones)
VALUES
    (1, 1, '2023-02-01', NULL, 'Equipo de trabajo principal'),
    (2, 2, '2022-12-01', '2024-03-01', 'Cambio por renovación'),
    (2, 7, '2024-03-02', NULL, 'Equipo reemplazo por baja de desempeño'),
    (4, 4, '2020-06-01', NULL, 'Uso compartido en logística'),
    (3, 6, '2024-02-15', NULL, 'Asignación nuevo ingreso');

-- Mantenimientos

INSERT INTO mantenimiento
    (id_equipo, id_tecnico, fecha_mnto, tipo, descripcion)
VALUES
    (3, 1, '2023-08-10', 'preventivo', 'Limpieza interna y cambio de pasta térmica'),
    (4, 2, '2024-01-20', 'correctivo', 'Atasco de papel y cambio de rodillo'),
    (2, 1, '2023-06-05', 'preventivo', 'Actualización de BIOS y limpieza'),
    (3, 1, '2024-04-12', 'correctivo', 'Reemplazo de fuente de poder');

-- FUNCIONES

-- Función de apoyo: Revisa si un equipo tiene una asignación vigente
DROP FUNCTION IF EXISTS fn_equipo_asignado_actualmente;
DELIMITER $$
CREATE FUNCTION fn_equipo_asignado_actualmente(p_id_equipo INT)
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE v_asignado TINYINT DEFAULT 0;
    SELECT 1
    INTO v_asignado
    FROM asignacion a
    WHERE a.id_equipo = p_id_equipo
        AND a.fecha_devol IS NULL
    LIMIT 1;
RETURN IFNULL(v_asignado, 0);
END$$
DELIMITER ;

-- VISTAS

-- Vista de apoyo: Última asignación/estado por equipo

CREATE OR REPLACE VIEW v_equipo_estado_actual AS
SELECT
    e.id_equipo, e.serial, e.marca, e.modelo, e.estado_operativo,
    e.id_categoria, e.id_dpto,
    a.id_usuario, a.fecha_asign, a.fecha_devol
FROM equipo e
    LEFT JOIN (
  SELECT a.*,
        ROW_NUMBER() OVER (PARTITION BY a.id_equipo ORDER BY a.fecha_asign DESC) AS rn
    FROM asignacion a
) a ON a.id_equipo = e.id_equipo AND a.rn = 1;

-- Vista de apoyo alternativa: equipos asignados actualmente

CREATE OR REPLACE VIEW v_equipos_asignados_actualmente AS
SELECT
    e.id_equipo, e.serial, e.marca, e.modelo,
    u.id_usuario, u.nombre AS usuario, a.fecha_asign
FROM equipo e
    JOIN (
  SELECT a1.id_equipo, a1.id_usuario, a1.fecha_asign, a1.fecha_devol,
        ROW_NUMBER() OVER (PARTITION BY a1.id_equipo ORDER BY a1.fecha_asign DESC) AS rn
    FROM asignacion a1
) a ON a.id_equipo = e.id_equipo AND a.rn = 1
    JOIN usuario u ON u.id_usuario = a.id_usuario
WHERE a.fecha_devol IS NULL;

-- TRIGGERS

-- Trigger: Evitar fechas de compra futuras (INSERT)

DROP TRIGGER IF EXISTS trg_equipo_fecha_compra_ins;
DELIMITER $$
CREATE TRIGGER trg_equipo_fecha_compra_ins
BEFORE
INSERT ON
equipo
FOR
EACH
ROW
BEGIN
    IF NEW.fecha_compra IS NOT NULL AND NEW.fecha_compra > CURRENT_DATE() THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT
    = 'fecha_compra no puede ser futura';
END
IF;
END$$
DELIMITER ;

-- Trigger: Evitar fechas de compra futuras (UPDATE)

DROP TRIGGER IF EXISTS trg_equipo_fecha_compra_upd;
DELIMITER $$
CREATE TRIGGER trg_equipo_fecha_compra_upd
BEFORE
UPDATE ON equipo
FOR EACH ROW
BEGIN
    IF NEW.fecha_compra IS NOT NULL AND NEW.fecha_compra > CURRENT_DATE() THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT
    = 'fecha_compra no puede ser futura';
END
IF;
END$$
DELIMITER ;

-- PROCEDIMIENTOS ALMACENADOS

-- Procedimiento: ASIGNAR EQUIPO

DROP PROCEDURE IF EXISTS sp_asignar_equipo;
DELIMITER $$
CREATE PROCEDURE sp_asignar_equipo(
  IN p_id_usuario INT,
  IN p_id_equipo INT,
  IN p_fecha DATE,
  IN p_observaciones TEXT
)
BEGIN
    DECLARE v_estado VARCHAR
    (20);
DECLARE v_exists INT;

IF p_fecha IS NULL THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'La fecha de asignación es obligatoria';
END
IF;

  SELECT COUNT(*)
INTO v_exists
FROM usuario
WHERE id_usuario = p_id_usuario;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Usuario no existe';
END
IF;

  SELECT COUNT(*)
INTO v_exists
FROM equipo
WHERE id_equipo = p_id_equipo;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Equipo no existe';
END
IF;

  SELECT estado_operativo
INTO v_estado
FROM equipo
WHERE id_equipo = p_id_equipo;

IF v_estado = 'baja' THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'No se puede asignar un equipo en estado BAJA';
END
IF;

  IF fn_equipo_asignado_actualmente(p_id_equipo) = 1 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'El equipo ya se encuentra asignado';
END
IF;

  INSERT INTO asignacion
    (id_usuario, id_equipo, fecha_asign, fecha_devol, observaciones)
VALUES
    (p_id_usuario, p_id_equipo, p_fecha, NULL, p_observaciones);
END$$
DELIMITER ;

-- Procedimiento: DEVOLVER EQUIPO

DROP PROCEDURE IF EXISTS sp_devolver_equipo;
DELIMITER $$
CREATE PROCEDURE sp_devolver_equipo(
  IN p_id_equipo INT,
  IN p_fecha DATE
)
BEGIN
    DECLARE v_asign_id INT;

IF p_fecha IS NULL THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'La fecha de devolución es obligatoria';
END
IF;

  SELECT a.id_asignacion
INTO v_asign_id
FROM asignacion a
WHERE a.id_equipo = p_id_equipo
    AND a.fecha_devol IS NULL
ORDER BY a.fecha_asign DESC
  LIMIT 1;

  IF v_asign_id
IS NULL THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'El equipo no tiene asignación vigente';
END
IF;

  UPDATE asignacion
  SET fecha_devol = p_fecha
  WHERE id_asignacion = v_asign_id;
END$$
DELIMITER ;

-- Procedimiento: REGISTRAR MANTENIMIENTO

DROP PROCEDURE IF EXISTS sp_registrar_mantenimiento;
DELIMITER $$
CREATE PROCEDURE sp_registrar_mantenimiento(
  IN p_id_equipo INT,
  IN p_id_tecnico INT,
  IN p_fecha DATE,
  IN p_tipo VARCHAR
(60),
  IN p_descripcion TEXT,
  IN p_cambiar_estado_mant TINYINT
)
BEGIN
    DECLARE v_exists INT;

IF p_fecha IS NULL THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'La fecha de mantenimiento es obligatoria';
END
IF;

  SELECT COUNT(*)
INTO v_exists
FROM equipo
WHERE id_equipo = p_id_equipo;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Equipo no existe';
END
IF;

  IF p_id_tecnico IS NOT NULL THEN
SELECT COUNT(*)
INTO v_exists
FROM tecnico
WHERE id_tecnico = p_id_tecnico;
IF v_exists = 0 THEN
      SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Técnico no existe';
END
IF;
  END
IF;

  INSERT INTO mantenimiento
    (id_equipo, id_tecnico, fecha_mnto, tipo, descripcion)
VALUES
    (p_id_equipo, p_id_tecnico, p_fecha, p_tipo, p_descripcion);

IF p_cambiar_estado_mant = 1 THEN
UPDATE equipo SET estado_operativo = 'mantenimiento' WHERE id_equipo = p_id_equipo;
END
IF;
END$$
DELIMITER ;

-- Procedimiento: TRANSFERIR EQUIPO ENTRE DEPARTAMENTOS

DROP PROCEDURE IF EXISTS sp_transferir_equipo_departamento;
DELIMITER $$
CREATE PROCEDURE sp_transferir_equipo_departamento(
  IN p_id_equipo INT,
  IN p_id_dpto_dest INT
)
BEGIN
    DECLARE v_exists INT;

SELECT COUNT(*)
INTO v_exists
FROM equipo
WHERE id_equipo = p_id_equipo;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Equipo no existe';
END
IF;

  SELECT COUNT(*)
INTO v_exists
FROM departamento
WHERE id_dpto = p_id_dpto_dest;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Departamento destino no existe';
END
IF;

  UPDATE equipo SET id_dpto = p_id_dpto_dest WHERE id_equipo = p_id_equipo;
END$$
DELIMITER ;

-- Procedimiento: CAMBIAR ESTADO DEL EQUIPO

DROP PROCEDURE IF EXISTS sp_cambiar_estado_equipo;
DELIMITER $$
CREATE PROCEDURE sp_cambiar_estado_equipo(
  IN p_id_equipo INT,
  IN p_nuevo_estado VARCHAR
(20)
)
BEGIN
    DECLARE v_exists INT;
DECLARE v_valid TINYINT DEFAULT 0;

SELECT COUNT(*)
INTO v_exists
FROM equipo
WHERE id_equipo = p_id_equipo;
IF v_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Equipo no existe';
END
IF;

  IF p_nuevo_estado IN ('operativo','mantenimiento','baja','dañado','otro') THEN
SET v_valid
= 1;
END
IF;

  IF v_valid = 0 THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'Estado no permitido';
END
IF;

  UPDATE equipo SET estado_operativo = p_nuevo_estado WHERE id_equipo = p_id_equipo;
END$$
DELIMITER ;

-- Procedimiento: UPSERT CATEGORÍA (Insertar o Actualizar)

DROP PROCEDURE IF EXISTS sp_upsert_categoria;
DELIMITER $$
CREATE PROCEDURE sp_upsert_categoria(
  IN p_nombre VARCHAR
(100),
  IN p_descripcion TEXT,
  IN p_vida_util SMALLINT,
  OUT p_id_categoria INT
)
BEGIN
    DECLARE v_id INT;

IF p_nombre IS NULL OR p_nombre = '' THEN
    SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT
= 'El nombre de la categoría es obligatorio';
END
IF;

  SELECT id_categoria
INTO v_id
FROM categoria_equipo
WHERE nombre = p_nombre
LIMIT 1;

IF v_id IS NULL THEN
INSERT INTO categoria_equipo
    (nombre, descripcion, vida_util)
VALUES
    (p_nombre, p_descripcion, p_vida_util);
SET p_id_categoria
= LAST_INSERT_ID
();
  ELSE
UPDATE categoria_equipo
      SET descripcion = p_descripcion,
          vida_util = p_vida_util
    WHERE id_categoria = v_id;
SET p_id_categoria
= v_id;
END
IF;
END$$
DELIMITER ;

-- Procedimiento: BUSCAR EQUIPOS

DROP PROCEDURE IF EXISTS sp_buscar_equipos;
DELIMITER $$
CREATE PROCEDURE sp_buscar_equipos(
  IN p_texto VARCHAR
(100)
)
BEGIN
    SELECT e.id_equipo, e.serial, e.marca, e.modelo, e.estado_operativo,
        c.nombre AS categoria, d.nombre AS departamento
    FROM equipo e
        LEFT JOIN categoria_equipo c ON c.id_categoria = e.id_categoria
        LEFT JOIN departamento d ON d.id_dpto = e.id_dpto
    WHERE p_texto IS NULL
        OR p_texto = ''
        OR e.serial LIKE CONCAT('%', p_texto, '%')
        OR e.marca LIKE CONCAT('%', p_texto, '%')
        OR e.modelo LIKE CONCAT('%', p_texto, '%');
    END$$
DELIMITER
;

-- Procedimiento: REPORTE DE MANTENIMIENTOS EN RANGO

DROP PROCEDURE IF EXISTS sp_reporte_mantenimientos;
DELIMITER $$
CREATE PROCEDURE sp_reporte_mantenimientos(
  IN p_fini DATE,
  IN p_ffin DATE
)
BEGIN
    IF p_fini IS NULL OR p_ffin IS NULL THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT
    = 'Debe enviar fechas de inicio y fin';
END
IF;

  SELECT m.id_mnto, m.fecha_mnto, m.tipo, m.descripcion,
    e.serial, e.marca, e.modelo,
    t.nombre AS tecnico
FROM mantenimiento m
    JOIN equipo e ON e.id_equipo = m.id_equipo
    LEFT JOIN tecnico t ON t.id_tecnico = m.id_tecnico
WHERE m.fecha_mnto BETWEEN p_fini AND p_ffin
ORDER BY m.fecha_mnto DESC;
END$$
DELIMITER ;

-- Fin del script.