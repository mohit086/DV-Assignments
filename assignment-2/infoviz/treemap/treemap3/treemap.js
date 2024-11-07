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

let currentView = "dynasty";
let selectedDynasty = null;
let globalEdgesData = null;
let currentAlgorithm = "squarify";

function createTreemap(edgesData, view = "dynasty", selectedDynasty = null) {
  // Group data by dynasty
  const groupedByDynasty = new Map();
  edgesData.forEach((edge) => {
    const sourceDynasty = edgesData.find((node) => node.id === edge.source).nationality;
    const targetDynasty = edgesData.find((node) => node.id === edge.target).nationality;

    if (!groupedByDynasty.has(sourceDynasty)) {
      groupedByDynasty.set(sourceDynasty, new Map());
    }
    if (!groupedByDynasty.get(sourceDynasty).has(targetDynasty)) {
      groupedByDynasty.get(sourceDynasty).set(targetDynasty, 0);
    }
    groupedByDynasty.get(sourceDynasty).set(targetDynasty, groupedByDynasty.get(sourceDynasty).get(targetDynasty) + 1);
  });

  // Create different hierarchy based on view
  let hierarchyData;
  if (view === "dynasty") {
    hierarchyData = {
      name: "Chinese Buddhist Figures",
      children: Array.from(groupedByDynasty, ([dynasty, interactions]) => ({
        name: dynasty,
        displayName: DYNASTY_TRANSLATIONS[dynasty] || dynasty,
        value: Array.from(interactions.values()).reduce((sum, count) => sum + count, 0),
        children: Array.from(interactions, ([targetDynasty, count]) => ({
          name: targetDynasty,
          displayName: DYNASTY_TRANSLATIONS[targetDynasty] || targetDynasty,
          value: count,
        })),
      })),
    };
  } else if (view === "interactions" && selectedDynasty) {
    const selectedDynastyInteractions = groupedByDynasty.get(selectedDynasty);
    hierarchyData = {
      name: DYNASTY_TRANSLATIONS[selectedDynasty] || selectedDynasty,
      children: Array.from(selectedDynastyInteractions, ([targetDynasty, count]) => ({
        name: targetDynasty,
        displayName: DYNASTY_TRANSLATIONS[targetDynasty] || targetDynasty,
        value: count,
      })),
    };
  }

  const plotlyData = [
    {
      type: "treemap",
      labels: [],
      parents: [],
      values: [],
      textinfo: "label+value+percent parent",
      hovertemplate:
        view === "dynasty"
          ? "Dynasty: %{label}<br>Interactions: %{value}<br>Percentage: %{percentRoot:.1%}<extra></extra>"
          : "Interaction with: %{label}<br>Count: %{value}<br>Percentage: %{percentParent:.1%}<extra></extra>",
      texttemplate:
        view === "dynasty"
          ? "%{label}<br>%{value}<br>%{percentRoot:.1%}"
          : "%{label}<br>%{value}<br>%{percentParent:.1%}",
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
    if (parent === "") return "#ffffff";
    if (view === "dynasty") {
      const originalKey =
        Object.keys(DYNASTY_TRANSLATIONS).find(
          (key) => DYNASTY_TRANSLATIONS[key] === label
        ) || label;
      return DYNASTY_COLORS[DYNASTY_TRANSLATIONS[originalKey]] || "#bdbdbd";
    }
    return DYNASTY_COLORS[DYNASTY_TRANSLATIONS[label]] || "#bdbdbd";
  });

  return plotlyData;
}

const layout = {
  width: 20,
  height: 600,
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

function handleClick(eventData) {
  if (!eventData || !eventData.points || eventData.points.length === 0) return;

  const point = eventData.points[0];

  if (
    currentView === "dynasty" &&
    point.parent === "Chinese Buddhist Figures"
  ) {
    const dynastyKey = point.label;
    selectedDynasty = dynastyKey;
    currentView = "interactions";
    layout.title.text = `Interactions of ${point.label} Dynasty`;

    const plotlyData = createTreemap(globalEdgesData, "interactions", dynastyKey);
    Plotly.react("treemap", plotlyData, layout);
    addBackButton();
  }
}

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
      currentView = "dynasty";
      selectedDynasty = null;
      layout.title.text = "Chinese Buddhist Figures by Dynasty";

      const plotlyData = createTreemap(globalEdgesData, "dynasty");
      Plotly.react("treemap", plotlyData, layout);
      backButton.remove();
    });

    container.appendChild(backButton);
  }
}

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
        globalEdgesData,
        currentView,
        selectedDynasty
      );
      Plotly.react("treemap", plotlyData, layout);
    });

    container.appendChild(selector);
  }
}

function initVisualization() {
  Promise.all([d3.csv("nodes.csv"), d3.csv("edges.csv")])
    .then(([nodesData, edgesData]) => {
      globalEdgesData = edgesData;
      const plotlyData = createTreemap(edgesData, "dynasty");

      Plotly.newPlot("treemap", plotlyData, layout).then((gd) => {
        gd.on("plotly_click", handleClick);
        resizeVisualization();
        addAlgorithmSelector();
      });
    })
    .catch((error) => console.error("Error loading data:", error));
}

const style = document.createElement("style");
style.textContent = `
  #algoSelector {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 4px 8px;
    border-radius: 4px;
  }
`;
document.head.appendChild(style);

document.addEventListener("DOMContentLoaded", initVisualization);