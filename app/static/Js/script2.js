// Encuentra el formulario de comentarios y la sección de comentarios
const commentForm = document.getElementById('commentForm');
const commentsSection = document.querySelector('.comments');

// Manejar el envío de comentarios
commentForm.addEventListener('submit', function (e) {
    e.preventDefault();

    // Obtener los valores del formulario
    const name = document.getElementById('name').value;
    const comment = document.getElementById('comment').value;
    const rating = document.querySelector('input[name="rating"]:checked').value;

    // Crear un nuevo elemento de comentario
    const newComment = document.createElement('div');
    newComment.classList.add('comment');
    newComment.innerHTML = `<strong>${name}:</strong> ${comment} - Calificación: ${rating} estrella(s)`;

    // Agregar el nuevo comentario a la sección de comentarios
    commentsSection.appendChild(newComment);

    // Limpiar el formulario
    commentForm.reset();
});
