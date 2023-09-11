//Selecciona todas las clases btn-delete
const btnDelete = document.querySelectorAll('.btn-delete')

//Aqui se crea el arreglo para que recorra todos los botones de eliminar
if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        //Aqui se toma la información del evento click
        btn.addEventListener('click', (e) => {
            //Esto es una ventana para que el usuario ingrese si cancela o no la eliminación
            if(!confirm('¿Estas seguro de querer eliminarlo?')){
                //Si da click en cancelar pues así mismo se cancelara el evento
                //Si da clik en aceptar, así mismo seguira con su proceso normal
                e.preventDefault();
            }
        });
    });
}