USE dashboard;

CREATE TABLE datos (
    codigo_institucion VARCHAR(50) NOT NULL,
    ies_padre VARCHAR(50),
    institucion_educacion_superior VARCHAR(255),
    principal_o_seccional VARCHAR(50),
    id_sector_ies INT,
    sector_ies VARCHAR(100),
    id_caracter_ies INT,
    caracter_ies VARCHAR(100),
    id_departamento_domicilio_ies INT,
    departamento_domicilio_ies VARCHAR(100),
    codigo_municipio VARCHAR(10),
    municipio_domicilio_ies VARCHAR(100),
    id_genero INT,
    genero_docente VARCHAR(50),
    id_maximo_nivel_formacion_docente INT,
    maximo_nivel_formacion_docente VARCHAR(100),
    id_tiempo_dedicacion_docente INT,
    tiempo_dedicacion_docente VARCHAR(100),
    id_tipo_contrato_docente INT,
    tipo_contrato_docente VARCHAR(100),
    año INT,
    semestre INT,
    numero_docentes INT
);
