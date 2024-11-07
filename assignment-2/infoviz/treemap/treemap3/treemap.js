// const DYNASTY_TRANSLATIONS = {
//   清: "Qing (清)",
//   唐: "Tang (唐)",
//   北宋: "Northern Song (北宋)",
//   明: "Ming (明)",
//   南宋: "Southern Song (南宋)",
//   五代十國: "Five Dynasties and Ten Kingdoms (五代十國)",
//   "明 清": "Ming-Qing (明清)",
//   元: "Yuan (元)",
//   隋: "Sui (隋)",
//   劉宋: "Liu Song (劉宋)",
//   南梁: "Southern Liang (南梁)",
//   南齊: "Southern Qi (南齊)",
//   東晉: "Eastern Jin (東晉)",
//   宋: "Song (宋)",
//   陳: "Chen (陳)",
// };

// const DYNASTY_COLORS = {
//   "Qing (清)": "#FF0000",
//   "Tang (唐)": "#0002B0",
//   "Northern Song (北宋)": "#43FF00",
//   "Ming (明)": "#FFC90E",
//   "Southern Song (南宋)": "#650091",
//   "Five Dynasties and Ten Kingdoms (五代十國)": "#72B300",
//   "Ming-Qing (明清)": "#5E3500",
//   "Yuan (元)": "#FFB077",
//   "Sui (隋)": "#007061",
//   "Liu Song (劉宋)": "#F354FF",
//   "Southern Liang (南梁)": "#97FFDB",
//   "Southern Qi (南齊)": "#46611B",
//   "Eastern Jin (東晉)": "#5C79FF",
//   "Song (宋)": "#AD1F78",
//   "Chen (陳)": "#FFFA88",
// };

const DYNASTY_TRANSLATIONS = {
  '清': 'Qing',
  '明': 'Ming',
  '唐': 'Tang',
  '南宋': 'Southern Song',
  '明 清': 'Ming-Qing',
  '元': 'Yuan',
  '北宋': 'Northern Song',
  '宋': 'Song',
  '五代十國': 'Five Dynasties and Ten Kingdoms',
  '隋': 'Sui',
  '陳': 'Chen',
  '東晉': 'Eastern Jin',
  '南梁': 'Southern Liang',
  '劉宋': 'Liu Song',
  '南齊': 'Southern Qi'
};


const DYNASTY_COLORS = {
  "Qing": "#FF0000",
  "Tang": "#0002B0",
  "Northern Song": "#43FF00", 
  "Ming": "#FFC90E",
  "Southern Song": "#650091",
  "Five Dynasties and Ten Kingdoms": "#72B300",
  "Ming-Qing": "#5E3500",
  "Yuan": "#FFB077",
  "Sui": "#007061",
  "Liu Song": "#F354FF",
  "Southern Liang": "#97FFDB",
  "Southern Qi": "#46611B",
  "Eastern Jin": "#5C79FF",
  "Song": "#AD1F78",
  "Chen": "#FFFA88",
};

let currentView = "dynasty";
let selectedDynasty = null;
let globalEdgesData = null;
let currentAlgorithm = "squarify";

// Create the layout object for the Plotly chart
const layout = {
  title: {
    text: "Chinese Buddhist Figures - Dynasty Interactions",
    font: {
      size: 18,
    },
  },
  margin: {
    t: 40,
    b: 40,
    l: 40,
    r: 40,
  },
  height: 700,
  width: "100%",
  showlegend: false,
  hovermode: "closest",
};

function createTreemap(edgesData, view = "dynasty", selectedDynasty = null) {
  const interactionCounts = {};
  
  edgesData.forEach((edge) => {
    const sourceNode = globalNodesData.find((node) => node.id === edge.source);
    const targetNode = globalNodesData.find((node) => node.id === edge.target);
    if (!sourceNode || !targetNode) return;

    const sourceDynasty = sourceNode.nationality;
    const targetDynasty = targetNode.nationality;
    
    // Initialize if not already done
    if (!interactionCounts[sourceDynasty]) interactionCounts[sourceDynasty] = {};
    if (!interactionCounts[sourceDynasty][targetDynasty]) interactionCounts[sourceDynasty][targetDynasty] = 0;

    // Increment interaction count
    interactionCounts[sourceDynasty][targetDynasty]++;
  });

  let hierarchyData;

  if (view === "dynasty") {
    hierarchyData = {
      name: "Chinese Buddhist Figures",
      children: Object.keys(interactionCounts).map((dynasty) => {
        const totalInteractions = Object.values(interactionCounts[dynasty]).reduce((sum, count) => sum + count, 0);
        return {
          name: dynasty,
          displayName: DYNASTY_TRANSLATIONS[dynasty] || dynasty,
          value: totalInteractions,
          children: Object.entries(interactionCounts[dynasty]).map(([targetDynasty, count]) => ({
            name: targetDynasty,
            displayName: DYNASTY_TRANSLATIONS[targetDynasty] || targetDynasty,
            value: count,
          })),
        };
      }),
    };
  } else if (view === "interactions" && selectedDynasty) {
    const selectedInteractions = interactionCounts[selectedDynasty];
    hierarchyData = {
      name: DYNASTY_TRANSLATIONS[selectedDynasty] || selectedDynasty,
      children: Object.entries(selectedInteractions).map(([targetDynasty, count]) => ({
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
      hovertemplate: view === "dynasty"
        ? "Dynasty: %{label}<br>Interactions: %{value}<br>Percentage: %{percentRoot:.1%}<extra></extra>"
        : "Interaction with: %{label}<br>Count: %{value}<br>Percentage: %{percentParent:.1%}<extra></extra>",
      texttemplate: view === "dynasty"
        ? "%{label}<br>%{value}<br>%{percentRoot:.1%}"
        : "%{label}<br>%{value}<br>%{percentParent:.1%}",
      marker: {
        colors: [], // We'll populate this in the processNode function
        line: { width: 2 },
      },
      tiling: {
        packing: currentAlgorithm,
      },
    },
  ];

  function processNode(node, parent = "") {
    const displayName = node.displayName || node.name;
    const uniqueLabel = `${displayName} (${node.value || 0})`;
    console.log(`Adding node: label=${uniqueLabel}, parent=${parent}`);
    plotlyData[0].labels.push(uniqueLabel);
    plotlyData[0].parents.push(parent);
    plotlyData[0].values.push(node.value || 0);

    if (node.children) {
        node.children.forEach((child) => processNode(child, uniqueLabel));
    }
}


  processNode(hierarchyData);

  return plotlyData;
}

function handleClick(eventData) {
  if (!eventData || !eventData.points || eventData.points.length === 0) return;

  const point = eventData.points[0];
  if (currentView === "dynasty" && point.parent === "Chinese Buddhist Figures") {
    selectedDynasty = Object.keys(DYNASTY_TRANSLATIONS).find(
      (key) => DYNASTY_TRANSLATIONS[key] === point.label
    ) || point.label;

    currentView = "interactions";
    layout.title.text = `Interactions of ${point.label} Dynasty`;

    const plotlyData = createTreemap(globalEdgesData, "interactions", selectedDynasty);
    Plotly.react("treemap", plotlyData, layout);
    addBackButton();
  }
}

function initVisualization() {
  Promise.all([d3.csv("./nodes.csv"), d3.csv("./edges.csv")])
    .then(([nodesData, edgesData]) => {
      globalEdgesData = edgesData;
      globalNodesData = nodesData;
      const plotlyData = createTreemap(edgesData, "dynasty");

      Plotly.newPlot("treemap", plotlyData, layout).then((gd) => {
        gd.on("plotly_click", handleClick);
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

function resizeVisualization() {
  const container = document.getElementById("treemap").parentElement;
  Plotly.relayout("treemap", {
    width: container.offsetWidth,
    height: container.offsetHeight,
  });
}

window.addEventListener("resize", resizeVisualization);
