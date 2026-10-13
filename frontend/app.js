fetch("../contract/sample.json")
  .then(response => response.json())
  .then(data => {
    renderTable(data);
    renderChart(data);
  });


function renderTable(data) {
  const latest = data.weeks[data.weeks.length - 1];
  const tbody = document.getElementById("reservoir-rows");

  for (const reservoir of latest.reservoirs) {
    const row = document.createElement("tr");

    const nameCell = document.createElement("td");
    nameCell.textContent = reservoir.name;
    row.appendChild(nameCell);

    const stockCell = document.createElement("td");
    stockCell.textContent = `${reservoir.actualStock}%`;
    row.appendChild(stockCell);

    tbody.appendChild(row);
  }

  document.getElementById("week-date").textContent = `Week ending ${latest.date}`;
}

  function renderChart(data) {

  }