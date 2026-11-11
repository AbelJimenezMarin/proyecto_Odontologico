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