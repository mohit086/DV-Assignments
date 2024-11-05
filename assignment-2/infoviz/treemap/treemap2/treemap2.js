// Dynasty translations mapping for display
const DYNASTY_TRANSLATIONS = {
  清: "Qing (清)",
  唐: "Tang (唐)",
  北宋: "Northern Song (北宋)",
  明: "Ming (明)",
  南宋: "Southern Song (南宋)",
  五代十國: "Five Dynasties and Ten Kingdoms (五代十國)",
  "明 清": "Ming-Qing (明清)",
  元: "Yuan (元)",
  隋: "Sui (隋)",
  劉宋: "Liu Song (劉宋)",
  南梁: "Southern Liang (南梁)",
  南齊: "Southern Qi (南齊)",
  東晉: "Eastern Jin (東晉)",
  宋: "Song (宋)",
  陳: "Chen (陳)",
};

const DYNASTY_COLORS = {
  "Qing (清)": "#FF0000",
  "Tang (唐)": "#0002B0",
  "Northern Song (北宋)": "#43FF00",
  "Ming (明)": "#FFC90E",
  "Southern Song (南宋)": "#650091",
  "Five Dynasties and Ten Kingdoms (五代十國)": "#72B300",
  "Ming-Qing (明清)": "#5E3500",
  "Yuan (元)": "#FFB077",
  "Sui (隋)": "#007061",
  "Liu Song (劉宋)": "#F354FF",
  "Southern Liang (南梁)": "#97FFDB",
  "Southern Qi (南齊)": "#46611B",
  "Eastern Jin (東晉)": "#5C79FF",
  "Song (宋)": "#AD1F78",
  "Chen (陳)": "#FFFA88",
};

const periodColors = {
  "0 - 800": "#fc03b6",
  "801 - 1400": "#030ffc",
  "1401 - 2000": "#09ad3a"
};
// Gender color scheme
const GENDER_COLORS = {
  1: "#3339ff",
  2: "#ff77fb",
};

let currentView = "time_period"; // Changed default view to time_period
let selectedPeriod = null; // Track selected time period
let globalNodesData = null;
let currentAlgorithm = "squarify";

// Create the visualization
function createTreemap(nodesData, view = "time_period", selectedPeriod = null) {
  // Group data by time period first
  const groupedByPeriod = d3.group(nodesData, (d) => d.time_period);

  let hierarchyData;
  if (view === "time_period") {
    hierarchyData = {
      name: "Chinese Buddhist Figures",
      children: Array.from(groupedByPeriod, ([period, nodes]) => ({
        name: period,
        value: nodes.length,
      })),
    };
  } else if (view === "nationality" && selectedPeriod) {
    // Get data for selected time period
    const periodData = groupedByPeriod.get(selectedPeriod);
    const nationalityGroups = d3.group(periodData, (d) => d.nationality);

    hierarchyData = {
      name: selectedPeriod,
      children: Array.from(nationalityGroups, ([nationality, nodes]) => ({
        name: nationality,
        displayName: DYNASTY_TRANSLATIONS[nationality] || nationality,
        value: nodes.length,
      })),
    };
  }

  // Create treemap data structure
  const plotlyData = [
    {
      type: "treemap",
      labels: [],
      parents: [],
      values: [],
      textinfo: "label+value+percent parent",
      hovertemplate:
      view === "time_period"
        ? "Time Period: %{label}<br>Count: %{value:.1f}<br>Percentage: %{percentRoot:.1%}<extra></extra>"
        : "Dynasty: %{label}<br>Count: %{value:.1f}<br>Percentage: %{percentParent:.1%}<extra></extra>",
      texttemplate:
      view === "time_period"
        ? "%{label}<br>%{value:.1f}<br>%{percentRoot:.1%}"
        : "%{label}<br>%{value:.1f}<br>%{percentParent:.1%}",
      marker: {
        colors: [],
        line: { width: 2 },
      },
      tiling: {
        packing: currentAlgorithm,
      },
    },
  ];

  function processNode(node, parent = "") {
    const displayName = node.displayName || node.name;
    plotlyData[0].labels.push(displayName);
    plotlyData[0].parents.push(parent);
    plotlyData[0].values.push(node.value || 0);

    if (node.children) {
      node.children.forEach((child) => processNode(child, displayName));
    }
  }

  processNode(hierarchyData);

  plotlyData[0].marker.colors = plotlyData[0].labels.map((label, i) => {
    const parent = plotlyData[0].parents[i];
    if (parent === "") return "#ffffff"; // root
    if (view === "nationality") {
      const originalKey =
        Object.keys(DYNASTY_TRANSLATIONS).find(
          (key) => DYNASTY_TRANSLATIONS[key] === label
        ) || label;
      return DYNASTY_COLORS[DYNASTY_TRANSLATIONS[originalKey]] || "#bdbdbd";
    }
    // Add different colors for time periods
    return (
      periodColors[label] || "#bdbdbd"
    );
  });

  return plotlyData;
}

const layout = {
  width: "70%",
  height: "100%",
  margin: { l: 10, r: 20, t: 40, b: 10 },
  title: {
    text: "Chinese Buddhist Figures by Dynasty",
    x: 0.5,
    y: 0.98,
  },
  hoverlabel: {
    bgcolor: "white",
    bordercolor: "#000000",
    font: { family: "Arial", size: 12 },
  },
  autosize: true,
};

function resizeVisualization() {
  const container = document.getElementById("treemap").parentElement;
  Plotly.relayout("treemap", {
    width: container.offsetWidth,
    height: container.offsetHeight,
  });
}

window.addEventListener("resize", resizeVisualization);

// Create legend
// function createLegend(nodesData) {
//   const legendDiv = document.getElementById("nationalityLegend");
//   legendDiv.innerHTML = ""; // Clear existing legend

//   if (currentView === "nationality") {
//     [...new Set(nodesData.map((d) => d.nationality))].forEach((nationality) => {
//       const legendItem = document.createElement("div");
//       legendItem.className = "legend-item";

//       const colorBox = document.createElement("div");
//       colorBox.className = "legend-color";
//       colorBox.style.backgroundColor =
//         DYNASTY_COLORS[DYNASTY_TRANSLATIONS[nationality]] || "#bdbdbd";

//       const label = document.createElement("span");
//       label.textContent = DYNASTY_TRANSLATIONS[nationality] || nationality;

//       legendItem.appendChild(colorBox);
//       legendItem.appendChild(label);
//       legendDiv.appendChild(legendItem);
//     });
//   } else {
//     // Gender legend
//     Object.entries(GENDER_COLORS).forEach(([gender, color]) => {
//       const legendItem = document.createElement("div");
//       legendItem.className = "legend-item";

//       const colorBox = document.createElement("div");
//       colorBox.className = "legend-color";
//       colorBox.style.backgroundColor = color;

//       const label = document.createElement("span");
//       label.textContent = gender === "1" ? "Male" : "Female";

//       legendItem.appendChild(colorBox);
//       legendItem.appendChild(label);
//       legendDiv.appendChild(legendItem);
//     });
//   }
// }

// Update click handler
function handleClick(eventData) {
  if (!eventData || !eventData.points || eventData.points.length === 0) return;

  const point = eventData.points[0];

  if (
    currentView === "time_period" &&
    point.parent === "Chinese Buddhist Figures"
  ) {
    selectedPeriod = point.label;
    currentView = "nationality";

    layout.title.text = `Dynasty Distribution in ${point.label}`;

    const plotlyData = createTreemap(
      globalNodesData,
      "nationality",
      selectedPeriod
    );
    Plotly.react("treemap", plotlyData, layout);

    addBackButton();
  }
}

// Update back button functionality
function addBackButton() {
  const container = document.getElementById("treemap").parentElement;

  if (!document.getElementById("backButton")) {
    const backButton = document.createElement("button");
    backButton.id = "backButton";
    backButton.textContent = "← Back to Time Periods";
    backButton.style.cssText = `
      position: absolute;
      top: 10px;
      left: 10px;
      padding: 8px 16px;
      background-color: #f0f0f0;
      border: 1px solid #ddd;
      border-radius: 4px;
      cursor: pointer;
    `;

    backButton.addEventListener("click", () => {
      currentView = "time_period";
      selectedPeriod = null;
      layout.title.text = "Chinese Buddhist Figures by Time Period";

      const plotlyData = createTreemap(globalNodesData, "time_period");
      Plotly.react("treemap", plotlyData, layout);

      backButton.remove();
    });

    container.appendChild(backButton);
  }
}

// Add this function after your other functions
function addAlgorithmSelector() {
  const container = document.getElementById("treemap").parentElement;

  if (!document.getElementById("algoSelector")) {
    const selector = document.createElement("select");
    selector.id = "algoSelector";
    selector.style.cssText = `
      position: absolute;
      top: 10px;
      right: 10px;
      padding: 4px 8px;
      border-radius: 4px;
    `;

    const algorithms = [
      { value: "squarify", text: "Squarify" },
      { value: "binary", text: "Binary" },
      { value: "slice", text: "Slice" },
      { value: "dice", text: "Dice" },
    ];

    algorithms.forEach((algo) => {
      const option = document.createElement("option");
      option.value = algo.value;
      option.textContent = algo.text;
      selector.appendChild(option);
    });

    selector.addEventListener("change", (e) => {
      currentAlgorithm = e.target.value;
      const plotlyData = createTreemap(
        globalNodesData,
        currentView,
        selectedPeriod
      );
      Plotly.react("treemap", plotlyData, layout);
    });

    container.appendChild(selector);
  }
}

// Main initialization function
function initVisualization() {
  Promise.all([
    d3.csv("../../data/nodes1.csv"),
    d3.csv("../../data/nodes2.csv"),
    d3.csv("../../data/nodes3.csv"),
  ])
    .then(([nodes1, nodes2, nodes3]) => {
      // Combine all nodes and add time_period property
      globalNodesData = [
        ...nodes1.map((n) => ({ ...n, time_period: "0 - 800" })),
        ...nodes2.map((n) => ({ ...n, time_period: "801 - 1400" })),
        ...nodes3.map((n) => ({ ...n, time_period: "1401 - 2000" })),
      ];

      const plotlyData = createTreemap(globalNodesData, "time_period");

      layout.title.text = "Chinese Buddhist Figures by Time Period";

      Plotly.newPlot("treemap", plotlyData, layout).then((gd) => {
        gd.on("plotly_click", handleClick);
        resizeVisualization();
        addAlgorithmSelector();
      });
    })
    .catch((error) => console.error("Error loading data:", error));
}

// Add necessary CSS
const style = document.createElement("style");
style.textContent = `
  #nationalityLegend {
    position: absolute;
    top: 50px;
    right: 10px;
    padding: 10px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    margin: 5px;
  }
  .legend-color {
    width: 20px;
    height: 20px;
    margin-right: 8px;
    border: 1px solid #ddd;
  }
`;
document.head.appendChild(style);

// Initialize visualization when DOM is ready
document.addEventListener("DOMContentLoaded", initVisualization);
