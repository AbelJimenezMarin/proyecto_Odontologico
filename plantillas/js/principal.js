/* js/principal.js - Comportamiento de la aplicación */

/* ----- MENU MÓVIL (boton hamburguesa) ----- */
// Se busca en la página los tres elementos que intervienen en el menú.
var aplicacion = document.getElementById("aplicacion");      //contenedor general de la página
var botonMenu = document.getElementById("boton-menu");       //botón de las 3 rayitas (solo se ve en el movil)
var fondoMenu = document.getElementById("fondo-menu");       //capa oscura que aparece detrás del menú

// Abrel menú: la clase "menu-abierto" hace que el CSS deslice el menu a la vista.
function abrirMenu() {
    aplicacion.classList.add("menu-abierto");
    botonMenu.setAttribute("aria-expanded", "true");    //avisa a lectores de pantalla que esta abierto
}

// Cierra el menú: quita la clase y el CSS lo vuelve a esconder.
function cerrarMenu() {
    aplicacion.classList.remove("menu-abierto"); 
    if (botonMenu) {
        botonMenu.setAttribute("aria-expanded", "false");
    }
}

// Si esta abierto lo cierra, y si esta cerrado lo abre (un solo boton hace las dos cosas)
function alternarMenu() {
    if (aplicacion.classList.contains("menu-abierto")) {
        cerrarMenu();
    }
    else {
        abrirMenu();
    }
}

// Este bloque solo se ejecuta si la pagina tiene botón de menú (el inicio de sesión no lo tiene).
if (botonMenu) {
    botonMenu.addEventListener("click", alternarMenu);       // click en las 3 rayitas: abrir o cerrar
    fondoMenu.addEventListener("click", cerrarMenu);         // click en la capa oscura: cerrar
    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape") {
            cerrarMenu();
        }
    });       // Tecla Esc: cerrra
    window.addEventListener("resize", function () {
        if (window.innerWidth > 639) {
            cerrarMenu();
        }
    });        // Si la pantalla crece, el menu se cierra solo
}

/* ------ INICIO DE SESIÓN ------ */
var formularioInicioSesion = document.getElementById("formulario-inicio-sesion");
if (formularioInicioSesion) {        // "submit" ocurre cuando se pulsa el botón ingresar 
    formularioInicioSesion.addEventListener("submit", function (evento) {
        var usuario = document.getElementById("campo-usuario").value.trim();          // trim() quita espacios sobrantes
        var clave = document.getElementById("campo-clave").value;
        var mensaje = document.getElementById("mensaje-error");
        if (usuario === "" || clave === "") {         // Si falta alguno de los dos datos
            mensaje.textContent = "Ingrese su usuario y contraseña.";
            mensaje.className = "alerta alerta-peligro";         // ...se muestra la franja roja
            evento.preventDefault();                             // ...y se impide que la página avance
        }
    });
}

/* ------BUSCADOR DE LAS TABLAS ------ */
// Muestra solo las filas que contienen lo que se escribió en el buscador.
// Recibe tres ids: la caja de búsqueda, la tabla y el aviso "sin resultados".
function filtrarTabla(idEntrada, idTabla, idSinResultados) {
    var texto = document.getElementById(idEntrada).value.toLowerCase();           // minúsculas: no distingue mayúsculas
    var filas = document.getElementById(idTabla).getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    var visibles = 0;         // cuenta las filas que coinciden
    for (var i = 0; i < filas.length; i++) {       // revisa fila por fila 
        var coincide = filas[i].textContent.toLowerCase().indexOf(texto) !== -1;
        filas[i].style.display = coincide ? "" : "none";          // muestra u oculta la fila
        if (coincide) {
            visibles++;
        }
    }
    var aviso = document.getElementById(idSinResultados);
    if (aviso) {
        aviso.hidden = visibles !== 0;            // El aviso solo se ve si no coincidió ninguna fila
    }
}

/* ----- REGISTRO DE PACIENTES: VALIDACIÓN ----- */
// Muestra (o borra) el mensaje de error de un campo y lo marca en rojo.
// Devuelve true si el camppo está bien (sin mensaje).
function mostrarErrorCampo(idCampo, idMensaje, texto) {
    document.getElementById(idMensaje).textContent = texto;
    document.getElementById(idCampo).classList.toggle("campo-invalido", texto !== "");
    return texto === "";
}
var formularioPaciente = document.getElementById("formulario-paciente");
if (formularioPaciente) {                   // solo existe en pacientes.html
    formularioPaciente.addEventListener("submit", function (evento) {
        // /^[0-9]{8}$/ significa: exactamente 8 digitos del 0 al 9
        var dniValido = mostrarErrorCampo("campo-dni", "error-dni", /^[0-9]{8}$/ .test(document.getElementById("campo-dni").value) ? "" : "El DNI debe tener 8 dígitos.");
        // Teléfono: entre 9 y 15 caracteres entre dígitos y espacios.
        var telefonoValido = mostrarErrorCampo("campo-telefono", "error-telefono", /^[0-9]{9,15}$/ .test(document.getElementById("campo-telefono").value) ? "" : "Ingrese un teléfono válido (9 dígitos).");
        //Nombres: no puede quedar vacío,
        var nombresValido = mostrarErrorCampo("campo-nombres", "error-nombres", document.getElementById("campo-nombres").value.trim() !== "" ? "" : "Los nombres son abligatorios.");
        // Si algún campo falló, se impide enviar el formulario.
        if (!(dniValido && telefonoValido && nombresValido)) {
            evento.preventDefault();
        }
    });
}

/* ------ PARA LA DISPONIBILIDAD Y LA GESTIÓN DE LAS CITAS ------ */
// Horas que ya tienen cita (datos de prueba; luego vendrán de la base de datos).
var horasOcupadas = ["09:00", "10:30", "12:00", "15:00"];
// Comprueba la hora elegida: si está ocupada avisa y bloquea el botón Guadar cita.
function verificarDisponibilidad() {
    var hora = document.getElementById("campo-hora-cita").value;
    var mensaje = document.getElementById("mensaje-disponibilidad");
    var boton = document.getElementById("boton-guardar-cita");
    var libre = horasOcupadas.indexOf(hora) === -1;          // -1 significa "no esta en la lista"





    
}