if DB_ID('BD_NADINNE') is null
	create database BD_NADINNE;
go

use bd_nadinne;
go

/* ----- Tabla USUARIO ----- */
create table dbo.Usuario (
id_usuario int identity(1,1) not null,
nombre_completo nvarchar(100) not null,
correo nvarchar(100) not null,
clave_hash nvarchar(255) not null,   --para que nunca se guarde la contraseña en texto plano
rol nvarchar(20) not null constraint DF_Usuario_rol default 'Administrador',
activo bit not null constraint DF_Usuario_activo default 1,
fecha_creacion datetime2(0) not null constraint DF_Usuario_fecha default sysdatetime(),
constraint PK_Usuario primary key (id_usuario),
constraint UQ_Usuario_correo unique (correo)
);
go

/* ----- Tabla PACIENTE ----- */
create table dbo.Paciente (
id_paciente int identity(1,1) not null,
dni char(8) not null, 
nombres nvarchar(80) not null, 
apellidos nvarchar(80) not null,
fecha_nacimiento date not null,
sexo char(1) not null,
telefono nvarchar(15) not null,
correo nvarchar(100) null,
direccion nvarchar(150) null,
antecedentes nvarchar(max) null,
activo bit not null constraint DF_Paciente_activo default 1,  --se desactiva, no se elimina
fecha_registro datetime2(0) not null constraint DF_Paciente_fecha default sysdatetime(),
constraint PK_Paciente primary key (id_paciente),
constraint UQ_Paciente_dni unique (dni),
constraint CK_Paciente_sexo check (sexo in('M', 'F')),
constraint CK_Paciente_dni check (dni not like '%[^0-9]%')
);
go

/* ----- Tabla CITA ----- */
create table dbo.Cita (
id_cita int identity(1, 1) not null,
id_paciente int not null,
id_usuario int not null,
fecha_cita date not null,
hora_cita time(0) not null,
estado nvarchar(15) not null constraint DF_Cita_estado default 'Programada',
motivo nvarchar(200) null,
recordatorio_enviado bit not null constraint DF_Cita_recordatorio default 0,
fecha_registro datetime2(0) not null constraint DF_Cita_fecha default sysdatetime(),
constraint PK_Cita primary key (id_cita),
constraint FK_Cita_Paciente foreign key (id_paciente) references dbo.Paciente (id_paciente),
constraint CK_Cita_estado check (estado in('Programada', 'Confirmada', 'Reprogramada', 'Cancelada', 'Atendida'))
);
go

-- No se puede registrar dos citas vigentes para la misma fecha y hora
create unique index UX_Cita_fecha_hora_vigente
	ON dbo.Cita (fecha_cita, hora_cita)
	where estado in ('Programada', 'Confirmada', 'Reprogramada');
create index IX_Cita_paciente ON dbo.Cita (id_paciente);
create index IX_Cita_fecha ON dbo.Cita (fecha_cita) include (hora_cita, estado);
go

/* ----- Tabla TRATAMIENTO ----- */
create table dbo.Tratamiento (
id_tratamiento int identity(1, 1) not null, 
id_paciente int not null,
tipo nvarchar(100) not null,
descripcion nvarchar(300) null,
costo_total decimal(10,2) not null,
num_sesiones int not null,
estado nvarchar(15) not null constraint DF_Tratamiento_estado default 'En curso',
fecha_inicio date not null constraint DF_Tratamiento_inicio default cast(sysdatetime() as date),
constraint PK_Tratamiento primary key (id_tratamiento),
constraint FK_Tratamiento_Paciente foreign key (id_paciente) references dbo.Paciente(id_paciente),
constraint CK_Tratamiento_costo check (costo_total >= 0),
constraint CK_Tratamiento_sesion check (num_sesiones > 0),
constraint CK_Tratamiento_estado check (estado in ('En curso', 'Concluido', 'Cancelado'))
);
go

create index IX_Tratamiento_paciente ON dbo.Tratamiento (id_paciente);
go

/* ------ Tabla SESIONTRATAMIENTO ------ */
create table dboSesionTratamiento (
id_sesion int identity(1, 1) not null,
id_tratamiento int not null,
numero_sesion int not null,
fecha_sesion date not null,
observaciones nvarchar(500) null,
estado nvarchar(15) not null constraint FD_Sesion_estado default 'Realizada',
constraint PK_SesionTratamiento primary key (id_sesion),
constraint FK_Sesion_Tratamiento foreign key (id_tratamiento) references dbo.Tratamiento(id_tratamiento),
constraint UQ_Sesion_numero unique (id_tratamiento, numero_sesion),
constraint CK_Sesion_numero check (numero_sesion > 0),
constraint CK_Sesion_estado check (estado in ('Pendiente', 'Realizada'))
);
go

/* ------ Tabla PAGO ------ */
create table dbo.Pago (
id_pago int identity(1, 1) not null,
id_tratamiento int not null, 
monto decimal(10,2) not null, 
fecha_pago date not null constraint DF_Pago_fecha default cast(sysdatetime() as date),
metodo_pago nvarchar(20) not null, 
constraint PK_Pago primary key (id_pago),
constraint FK_Pago_Tratamiento foreign key (id_tratamiento) references dbo.Tratamiento(id_tratamiento), 
constraint CK_Pago_monto check (monto > 0),
constraint CK_Pago_metodo check (metodo_pago in ('Efectivo', 'Yape', 'Plin', 'Transferencia', 'Tarjeta'))
);
go

create index IX_Pago_tratamiento ON dbo.Pago (id_tratamiento);

/* ----- VISTA: Saldo pendiente por tratamiento ----- */
create view dbo.vw_SaldoTratamiento AS
select t.id_tratamiento,
    t.id_paciente,
	t.tipo,
	t.costo_total,
	isnull(sum(p.monto), 0) as total_pagado,
	t.costo_total - isnull(sum(p.monto), 0) as saldo_pendiente from dbo.Tratamiento t
	left join dbo.Pago p ON p.id_tratamiento = t.id_tratamiento
	group by t.id_tratamiento, t.id_paciente, t.tipo, t.costo_total;
	go

	select * from Usuario;
