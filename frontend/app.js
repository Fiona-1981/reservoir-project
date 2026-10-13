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
  const canvas = document.getElementById("reservoir-chart");

  // x-axis: one label per week
  const labels = data.weeks.map(week => week.date);

  // reservoir names, taken from the latest week
  const latest = data.weeks[data.weeks.length - 1];
  const names = latest.reservoirs.map(reservoir => reservoir.name);

  // one line (dataset) per reservoir
  const datasets = names.map(name => ({
    label: name,
    data: data.weeks.map(week =>
      week.reservoirs.find(reservoir => reservoir.name === name)?.actualStock ?? null
    ),
  }));

  new Chart(canvas, {
    type: "line",
    data: { labels, datasets },
    options: {
      scales: {
        y: { min: 0, max: 100, title: { display: true, text: "% full" } },
      },
    },
  });
}