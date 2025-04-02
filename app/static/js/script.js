let images = [];
let currentIndex = 0;

document.addEventListener("DOMContentLoaded", function () {
    flatpickr("#date-picker", {
        locale: flatpickr.l10ns.es, // Asegurar que usa español correctamente
        firstDayOfWeek: 1, // La semana empieza en lunes
        dateFormat: "Y-m-d",
        onChange: function(selectedDates, dateStr) {
            let [year, month, day] = dateStr.split("-");
            loadImages(year, month, day);
            contarImagenes(dateStr);
        }
    });
});

function contarImagenes(fecha) {
    fetch(`/contar_imagenes?fecha=${fecha}`)
        .then(response => response.json())
        .then(data => {
            const contador = document.getElementById("contador");
            contador.textContent = `Nº people: ${data.numero}`;
        })
        .catch(error => {
            console.error("Error al contar las personas:", error);
        });
}

function loadImages(year, month, day) {
    fetch(`/get_images/${year}/${month}/${day}`)
        .then(response => response.json())
        .then(data => {
            images = data;
            currentIndex = 0;
            updateImage(year, month, day);
            actualizarHoraDesdeImagen(year, month, day);
        });
}

function updateImage(year, month, day) {
    if (images.length > 0) {
        document.getElementById("current-image").src = `/static/images/${year}/${month}/${day}/${images[currentIndex]}`;
    } else {
        document.getElementById("current-image").src = "/static/image_00.png"; // Imagen por defecto
    }
}

function prevImage() {
    if (currentIndex > 0) {
        currentIndex--;
        let [year, month, day] = document.getElementById("date-picker").value.split("-");
        updateImage(year, month, day);
        actualizarHoraDesdeImagen(year, month, day);
    }
}

function nextImage() {
    if (currentIndex < images.length - 1) {
        currentIndex++;
        let [year, month, day] = document.getElementById("date-picker").value.split("-");
        updateImage(year, month, day);
        actualizarHoraDesdeImagen(year, month, day);
    }
}

function actualizarHoraDesdeImagen(year, month, day) {
    let nombreImagen = images[currentIndex];

    fetch('/get-hora', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nombreImagen: nombreImagen,
            year: year,
            month: month,
            day: day
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("hora").textContent = `Hour: ${data.hora}`;
        document.getElementById("id").textContent = `ID: ${data.id}`;
    })
    .catch(error => {
        console.error('Error al obtener la hora:', error);
        document.getElementById("hora").textContent = "Hora: --";
        document.getElementById("id").textContent = "ID: --";
    });
}

