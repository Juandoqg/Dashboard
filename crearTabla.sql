USE dashboard;

CREATE TABLE datos (
    codigo_institucion INT,
    ies_padre INT,
    institucion_educacion_superior VARCHAR(255),
    principal_o_seccional VARCHAR(50),
    sector_ies VARCHAR(50),
    caracter_ies VARCHAR(50),
    departamento_domicilio_ies VARCHAR(100),
    codigo_municipio INT,
    municipio_domicilio_ies VARCHAR(100),
    genero_docente VARCHAR(20),
    tipo_documento VARCHAR(20),
    maximo_nivel_formacion_docente VARCHAR(50),
    tiempo_dedicacion_docente VARCHAR(50),
    tipo_contrato_docente VARCHAR(50),
    año INT,
    semestre INT,
    numero_docentes INT
);
