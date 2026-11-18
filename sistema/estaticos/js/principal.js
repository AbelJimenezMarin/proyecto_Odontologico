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

/* ---------- 5. Pagos (CU-06): saldo pendiente (RN-04) ---------- */
// Regla RN-04: saldo = costo total - lo pagado (nunca menor que cero).
function calcularSaldo(costoTotal, totalPagado) {
    var saldo = costoTotal - totalPagado;
    return saldo < 0 ? 0 : saldo;
}

// Convierte 1200 en "S/ 1,200.00" (con coma de miles y 2 decimales).
function darFormatoSoles(numero) {
    return "S/ " + numero.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var campoMonto = document.getElementById("campo-monto");
if (campoMonto) {                                         // solo existe en la pantalla de pagos
// El servidor escribe el saldo pendiente real en el atributo data-saldo del campo.
    var saldoActual = parseFloat(campoMonto.getAttribute("data-saldo")) || 0;
    campoMonto.addEventListener("input", function () {      // se ejecuta cada vez que se escribe un monto
    var monto = parseFloat(campoMonto.value) || 0;        // texto a número (si está vacío, 0)
    var mensaje = document.getElementById("mensaje-monto");
    var valido = monto > 0 && monto <= saldoActual;       // debe ser mayor que 0 y no pasar del saldo
    mensaje.textContent = valido || campoMonto.value === "" ? "" : "El monto debe ser mayor que 0 y no superar el saldo pendiente.";
    campoMonto.classList.toggle("campo-invalido", !valido && campoMonto.value !== "");
    document.getElementById("boton-guardar-pago").disabled = !valido;   // bloquea el botón si no es válido
    // Muestra cuánto quedaría por pagar después de este pago.
    document.getElementById("valor-saldo-despues").textContent = darFormatoSoles(calcularSaldo(saldoActual, valido ? monto : 0));
});
    document.getElementById("boton-guardar-pago").disabled = true;      // al abrir la pantalla aún no hay monto
}


