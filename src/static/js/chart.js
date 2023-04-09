// Gráfico de precios 
var precioChart = document.getElementById('precioChart').getContext('2d');
var precioChart = new Chart(precioChart, {
  // ...
  data: {
      labels: labels,
      datasets: [{ 
          data: datosPrecio
      }]
  }
});

// Más gráficos...

// Gráfico de cantidad por modelo
var modeloChart = document.getElementById('modeloChart').getContext('2d');
var modeloChart = new Chart(modeloChart, {
  type: 'bar',
  data: {
      labels: labels,
      datasets: [{ 
          data: cantidadPorModelo
      }]  
  }
});

// Gráfico de top 3 modelos
var topModelosChart = document.getElementById('topModelosChart').getContext('2d'); 
var topModelosChart = new Chart(topModelosChart, {
  type: 'horizontalBar',
  data: {
      labels: ['Modelo 1', 'Modelo 2', 'Modelo 3'],
      datasets: [{    
          data: topModelos,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(255, 205, 86)'
          ]
      }]
  }
});

// Promedio de kilometraje por modelo
var promKilometrajeChart = document.getElementById('promKilometrajeChart').getContext('2d');
var promKilometrajeChart = new Chart(promKilometrajeChart, {
  type: 'bar',
  data: {
      labels: labels,
      datasets: [{    
          data: promKilometraje
      }]
  } 
});