<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Reserva de Canchas</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Segoe UI', sans-serif;
      background-color: #f4f6f8;
      padding: 2rem;
      color: #333;
    }

    h2 {
      text-align: center;
      margin-bottom: 2rem;
      font-size: 2rem;
    }

    .tabs {
      display: flex;
      justify-content: center;
      margin-bottom: 1.5rem;
      border-bottom: 2px solid #ddd;
    }

    .tab {
      padding: 0.8rem 2rem;
      cursor: pointer;
      font-weight: 500;
      border-bottom: 3px solid transparent;
      transition: 0.3s;
    }

    .tab.active {
      border-bottom: 3px solid #007bff;
      color: #007bff;
    }

    .grid-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1.5rem;
      padding: 0 1rem;
    }

    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      overflow: hidden;
      transition: transform 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .card:hover {
      transform: translateY(-4px);
    }

    .card img {
      width: 100%;
      height: 150px;
      object-fit: cover;
    }

    .card-content {
      padding: 1rem;
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .card-content h3 {
      margin-bottom: 0.5rem;
      font-size: 1.1rem;
    }

    .card-content p {
      margin-bottom: 0.8rem;
      font-size: 0.95rem;
      color: #555;
    }

    .card-content button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      align-self: flex-start;
    }

    .card-content button:hover {
      background-color: #0056b3;
    }

    .content-section {
      display: none;
    }

    .content-section.active {
      display: block;
    }

    @media (max-width: 600px) {
      .grid-container {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>

  <h2>Nombre de Empresa</h2>

  <div class="tabs">
    <div class="tab active" data-tab="futbol">Canchas de Fútbol</div>
    <div class="tab" data-tab="padel">Canchas de Pádel</div>
  </div>

  <!-- Fútbol Section -->
  <div id="futbol" class="content-section active">
    <div class="grid-container" id="futbol-list">
      <!-- Aquí las canchas de fútbol se generarán con JS -->
    </div>
  </div>

  <!-- Pádel Section -->
  <div id="padel" class="content-section">
    <div class="grid-container" id="padel-list">
      <!-- Aquí las canchas de pádel se generarán con JS -->
    </div>
  </div>

  <!-- JS para Tabs y generación dinámica de canchas -->
  <script>
    // Datos de canchas con varias imágenes para cada una
    const futbolCanchas = [
      {
        nombre: "Cancha Fútbol 1",
        precio: 29,
        ubicacion: "Ciudad Deportiva",
        superficie: "Césped sintético",
        imagenes: [
          "/imagenes/OIP.webp",
          "/imagenes/OIP2.webp",
          "/imagenes/OIP3.webp"
        ]
      },
      {
        nombre: "Cancha Fútbol 2",
        precio: 230,
        ubicacion: "Complejo Norte",
        superficie: "Pasto natural",
        imagenes: [
          "/imagenes/download.webp",
          "/imagenes/download2.webp"
        ]
      },
      {
        nombre: "Cancha Fútbol 3",
        precio: 244,
        ubicacion: "Ciudad Deportiva",
        superficie: "Césped sintético",
        imagenes: [
          "/imagenes/OIP (1).webp"
        ]
      }
    ];

    const padelCanchas = [
      {
        nombre: "Cancha Pádel 1",
        precio: 20,
        ubicacion: "Club Pádel Central",
        superficie: "Césped azul",
        imagenes: [
          "/imagenes/download (1).webp",
          "/imagenes/download (2).webp"
        ]
      }
      // Puedes agregar más canchas de pádel aquí
    ];

    // Función para crear las tarjetas y agregarlas a un contenedor
    function renderCanchas(lista, contenedorId) {
      const contenedor = document.getElementById(contenedorId);
      lista.forEach(cancha => {
        const card = document.createElement("div");
        card.className = "card";

        // Imagen principal
        const img = document.createElement("img");
        img.src = cancha.imagenes[0]; 
        img.alt = cancha.nombre;
        card.appendChild(img);

        // Contenido
        const cardContent = document.createElement("div");
        cardContent.className = "card-content";

        cardContent.innerHTML = `
          <h3>${cancha.nombre}</h3>
          <p>Precio: $${cancha.precio}/hora</p>
        `;

        // Botón reservar
        const btn = document.createElement("button");
        btn.textContent = "Reservar";
        btn.onclick = () => {
          // Concatenar las imágenes codificadas por coma para la URL
          const imagenesStr = cancha.imagenes.map(url => encodeURIComponent(url)).join(",");
          const url = `reserva.html?nombre=${encodeURIComponent(cancha.nombre)}&precio=${encodeURIComponent(cancha.precio)}&imagenes=${imagenesStr}&ubicacion=${encodeURIComponent(cancha.ubicacion)}&superficie=${encodeURIComponent(cancha.superficie)}`;
          window.location.href = url;
        };

        cardContent.appendChild(btn);
        card.appendChild(cardContent);
        contenedor.appendChild(card);
      });
    }

    // Renderizar las canchas al cargar la página
    renderCanchas(futbolCanchas, "futbol-list");
    renderCanchas(padelCanchas, "padel-list");

    // Código de Tabs
    const tabs = document.querySelectorAll(".tab");
    const sections = document.querySelectorAll(".content-section");

    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        sections.forEach(s => s.classList.remove("active"));

        tab.classList.add("active");
        document.getElementById(tab.getAttribute("data-tab")).classList.add("active");
      });
    });
  </script>

</body>
</html>
