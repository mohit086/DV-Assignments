// Dynasty translations mapping for display
const DYNASTY_TRANSLATIONS = {
  清: "Qing",
  明: "Ming",
  唐: "Tang",
  南宋: "Southern Song",
  "明 清": "Ming-Qing",
  元: "Yuan",
  北宋: "Northern Song",
  宋: "Song",
  五代十國: "Five Dynasties and Ten Kingdoms",
  隋: "Sui",
  陳: "Chen",
  東晉: "Eastern Jin",
  南梁: "Southern Liang",
  劉宋: "Liu Song",
  南齊: "Southern Qi",
};

const DYNASTY_COLORS = {
<<<<<<< HEAD
  "Qing": "#FF7540",                         // 清
  "Tang": "#B0FF50",                         // 唐
  "Northern Song": "#749AFF",                // 北宋
  "Song": "#FF73F8",                         // 宋
  "Southern Song": "#FFE747",                // 南宋
  "Five Dynasties and Ten Kingdoms": "#0FF200", // 五代十國
  "Ming Qing": "#78F2EA",                    // 明 清
  "Yuan": "#9500FF",                         // 元
  "Sui": "#A3A651",                          // 隋
  "Liu Song": "#BA713D",                     // 劉宋
  "Southern Liang": "#FF0013",               // 南梁
  "Southern Qi": "#0300FF",                  // 南齊
  "Eastern Jin": "#F5D1AE",                  // 東晉
  "Song (duplicate color)": "#0FA600",       // 南宋 (duplicate)
  "Chen": "#CDB3FF"                          // 陳
=======
  "Qing": "#FF7540",
  "Ming": "#FF73F8",
  "Tang": "#B0FF50",
  "Southern Song": "#FFE847",
  "Ming-Qing": "#78F2EA",
  "Yuan": "#9500FF",
  "Northern Song": "#749AFF",
  "Song": "#0FA600",
  "Five Dynasties and Ten Kingdoms": "#0FF200",
  "Sui": "#A3A651",
  "Chen": "#CDB3FF",
  "Eastern Jin": "#F5D1AE",
  "Southern Liang": "#FF0013",
  "Liu Song": "#BA713D",
  "Southern Qi": "#0300FF",
>>>>>>> 1ba6b1170130886c2bddaf3c002afdc449199c59
};

// Gender color scheme
const GENDER_COLORS = {
  1: "#3339ff",
  2: "#ff77fb",
};

let currentView = "nationality"; // Track current view state
let selectedNationality = null; // Track selected nationality
let globalNodesData = null; // Store nodes data globally

// Create the visualization
function createTreemap(nodesData, view = "nationality", selectedNat = null) {
  // Group data by nationality
  const groupedByNationality = d3.group(nodesData, (d) => d.nationality);

  // Create different hierarchy based on view
  let hierarchyData;
  if (view === "nationality") {
    hierarchyData = {
      name: "Chinese Buddhist Figures",
      children: Array.from(groupedByNationality, ([nationality, nodes]) => ({
        name: nationality,
        displayName: DYNASTY_TRANSLATIONS[nationality] || nationality,
        value: nodes.length,
      })),
    };
  } else if (view === "gender" && selectedNat) {
    const nationalityData = groupedByNationality.get(selectedNat);
    const genderGroups = d3.group(nationalityData, (d) => d.gender);

    hierarchyData = {
      name: DYNASTY_TRANSLATIONS[selectedNat] || selectedNat,
      children: Array.from(genderGroups, ([gender, nodes]) => ({
        name: gender,
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
        view === "nationality"
          ? "Dynasty: %{label}<br>Count: %{value}<br>Percentage: %{percentRoot:.1%}<extra></extra>"
          : "Gender: %{label}<br>Count: %{value}<br>Percentage: %{percentParent:.1%}<extra></extra>",
      marker: {
        colors: [],
        line: { width: 2 },
      },
    },
  ];

  // Process hierarchy for Plotly
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

  // Create color scheme
  // Apply colors
  plotlyData[0].marker.colors = plotlyData[0].labels.map((label, i) => {
    const parent = plotlyData[0].parents[i];
    if (parent === "") return "#ffffff"; // root
    if (view === "nationality") {
      // Find original key from translation
      const originalKey =
        Object.keys(DYNASTY_TRANSLATIONS).find(
          (key) => DYNASTY_TRANSLATIONS[key] === label
        ) || label;
      return DYNASTY_COLORS[DYNASTY_TRANSLATIONS[originalKey]] || "#bdbdbd";
    }
    return GENDER_COLORS[label] || "#bdbdbd"; // gender level
  });
  return plotlyData;
}

// Layout configuration
const layout = {
  width: 1100,
  height: 600,
  margin: { l: 0, r: 20, t: 30, b: 0 },
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
};

// Create legend
function createLegend(nodesData) {
  const legendDiv = document.getElementById("nationalityLegend");
  legendDiv.innerHTML = ""; // Clear existing legend

  if (currentView === "nationality") {
    [...new Set(nodesData.map((d) => d.nationality))].forEach((nationality) => {
      const legendItem = document.createElement("div");
      legendItem.className = "legend-item";

      const colorBox = document.createElement("div");
      colorBox.className = "legend-color";
      colorBox.style.backgroundColor =
        DYNASTY_COLORS[DYNASTY_TRANSLATIONS[nationality]] || "#bdbdbd";

      const label = document.createElement("span");
      label.textContent = DYNASTY_TRANSLATIONS[nationality] || nationality;

      legendItem.appendChild(colorBox);
      legendItem.appendChild(label);
      legendDiv.appendChild(legendItem);
    });
  } else {
    // Gender legend
    Object.entries(GENDER_COLORS).forEach(([gender, color]) => {
      const legendItem = document.createElement("div");
      legendItem.className = "legend-item";

      const colorBox = document.createElement("div");
      colorBox.className = "legend-color";
      colorBox.style.backgroundColor = color;

      const label = document.createElement("span");
      label.textContent = gender === "1" ? "Male" : "Female";

      legendItem.appendChild(colorBox);
      legendItem.appendChild(label);
      legendDiv.appendChild(legendItem);
    });
  }
}

// Handle click events
function handleClick(eventData) {
  if (!eventData || !eventData.points || eventData.points.length === 0) return;

  const point = eventData.points[0];

  if (
    currentView === "nationality" &&
    point.parent === "Chinese Buddhist Figures"
  ) {
    // Find the original nationality key
    const nationalityKey =
      Object.keys(DYNASTY_TRANSLATIONS).find(
        (key) => DYNASTY_TRANSLATIONS[key] === point.label
      ) || point.label;

    selectedNationality = nationalityKey;
    currentView = "gender";

    // Update title
    layout.title.text = `Gender Distribution in ${point.label} Dynasty`;

    // Update visualization
    const plotlyData = createTreemap(globalNodesData, "gender", nationalityKey);
    Plotly.react("treemap", plotlyData, layout);
    createLegend(globalNodesData);

    // Add back button
    addBackButton();
  }
}

// Add back button
function addBackButton() {
  const container = document.getElementById("treemap").parentElement;

  if (!document.getElementById("backButton")) {
    const backButton = document.createElement("button");
    backButton.id = "backButton";
    backButton.textContent = "← Back to Dynasties";
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
      currentView = "nationality";
      selectedNationality = null;
      layout.title.text = "Chinese Buddhist Figures by Dynasty";

      const plotlyData = createTreemap(globalNodesData, "nationality");
      Plotly.react("treemap", plotlyData, layout);
      createLegend(globalNodesData);

      backButton.remove();
    });

    container.appendChild(backButton);
  }
}

// Main initialization function
function initVisualization() {
  Promise.all([d3.csv("../../data/nodes.csv"), d3.csv("../../data/edges.csv")])
    .then(([nodesData, edgesData]) => {
      globalNodesData = nodesData;
      const plotlyData = createTreemap(nodesData, "nationality");
      createLegend(nodesData);

      // Create treemap with click handler
      Plotly.newPlot("treemap", plotlyData, layout).then((gd) => {
        gd.on("plotly_click", handleClick);
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
