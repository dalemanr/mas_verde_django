(function () {

    const btnEliminar = document.querySelectorAll(".btnEliminar");

btnEliminar.forEach(btn => {
    btn.addEventListener('click', (e) =>{
        const confirmacion = confirm('¿Estas seguro de elminar el registro?');
        if (!confirmacion) {
            e.preventDefault();
        }
    });
});

})();