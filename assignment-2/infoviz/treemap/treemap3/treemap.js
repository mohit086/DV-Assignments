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
let globalNodesData = null;
let currentAlgorithm = "dice";

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
  height: 600,
  width: 1500,
  showlegend: false,
  hovermode: "closest",
};

function createTreemap(edgesData, view = "dynasty", selectedDynasty = null) {
  const interactionCounts = {};

  // Count both source and target interactions
  edgesData.forEach((edge) => {
    const sourceNode = globalNodesData.find((node) => node.id === edge.source);
    const targetNode = globalNodesData.find((node) => node.id === edge.target);
    if (!sourceNode || !targetNode) return;

    const sourceDynasty = sourceNode.nationality;
    const targetDynasty = targetNode.nationality;

    if (!interactionCounts[sourceDynasty])
      interactionCounts[sourceDynasty] = {};
    if (!interactionCounts[targetDynasty])
      interactionCounts[targetDynasty] = {};

    if (!interactionCounts[sourceDynasty][targetDynasty]) {
      interactionCounts[sourceDynasty][targetDynasty] = 0;
    }
    if (!interactionCounts[targetDynasty][sourceDynasty]) {
      interactionCounts[targetDynasty][sourceDynasty] = 0;
    }

    interactionCounts[sourceDynasty][targetDynasty]++;
    if (sourceDynasty !== targetDynasty) {
      interactionCounts[targetDynasty][sourceDynasty]++;
    }
  });

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

  if (view === "dynasty") {
    // Add root without value display
    plotlyData[0].labels.push("Chinese Buddhist Figures");
    plotlyData[0].parents.push("");
    plotlyData[0].values.push(0);
    plotlyData[0].marker.colors.push("#FFFFFF");

    // Add dynasty-level data
    Object.keys(interactionCounts).forEach((dynasty) => {
      const totalInteractions = Object.values(
        interactionCounts[dynasty]
      ).reduce((sum, count) => sum + count, 0);
      const displayName = DYNASTY_TRANSLATIONS[dynasty] || dynasty;

      plotlyData[0].labels.push(displayName);
      plotlyData[0].parents.push("Chinese Buddhist Figures");
      plotlyData[0].values.push(totalInteractions);
      plotlyData[0].marker.colors.push(
        DYNASTY_COLORS[displayName] || "#808080"
      );
    });
  } else if (view === "interactions" && selectedDynasty) {
    const selectedDisplayName = selectedDynasty;

    // Collect all interactions where the selected dynasty is either source or target
    const allInteractions = {};
    Object.keys(interactionCounts).forEach((dynasty) => {
      if (dynasty === selectedDynasty) {
        // Add interactions where selected dynasty is the source
        Object.entries(interactionCounts[dynasty]).forEach(
          ([targetDynasty, count]) => {
            allInteractions[targetDynasty] =
              (allInteractions[targetDynasty] || 0) + count;
          }
        );
      } else if (interactionCounts[dynasty][selectedDynasty]) {
        // Add interactions where selected dynasty is the target
        allInteractions[dynasty] =
          (allInteractions[dynasty] || 0) +
          interactionCounts[dynasty][selectedDynasty];
      }
    });

    // Add root level for selected dynasty
    plotlyData[0].labels.push(selectedDisplayName);
    plotlyData[0].parents.push("");
    plotlyData[0].values.push(0);
    plotlyData[0].marker.colors.push(
      DYNASTY_COLORS[selectedDisplayName] || "#808080"
    );

    // Add interaction data
    Object.entries(allInteractions).forEach(([dynasty, count]) => {
      const displayName = DYNASTY_TRANSLATIONS[dynasty] || dynasty;

      plotlyData[0].labels.push(displayName);
      plotlyData[0].parents.push(selectedDisplayName);
      plotlyData[0].values.push(count);
      plotlyData[0].marker.colors.push(
        DYNASTY_COLORS[displayName] || "#808080"
      );
    });
  }

  return plotlyData;
}

function addAlgorithmSelector() {
  // Create a container for the dropdown
  const container = document.createElement("div");
  container.style.marginBottom = "10px";

  // Create a label for the dropdown
  const label = document.createElement("label");
  label.textContent = "";
  label.style.marginRight = "10px";

  // Create the dropdown select element
  const select = document.createElement("select");
  select.id = "algorithm-selector";

  // Define the list of algorithms
  const algorithms = ["squarify", "binary", "slice", "dice"];

  // Populate the dropdown with options
  algorithms.forEach((algo) => {
    const option = document.createElement("option");
    option.value = algo;
    option.textContent = algo.charAt(0).toUpperCase() + algo.slice(1);
    if (algo === currentAlgorithm) option.selected = true;
    select.appendChild(option);
  });

  // Handle changes to the selected algorithm
  select.onchange = (e) => {
    currentAlgorithm = e.target.value;
    const plotlyData = createTreemap(
      globalEdgesData,
      currentView,
      selectedDynasty
    );
    Plotly.react("treemap", plotlyData, layout);
  };

  // Add label and select dropdown to the container
  container.appendChild(label);
  container.appendChild(select);

  // Insert the container before the treemap element
  document.body.insertBefore(container, document.getElementById("treemap"));
}

function addBackButton() {
  const existingButton = document.getElementById("back-button");
  if (existingButton) existingButton.remove();

  const backButton = document.createElement("button");
  backButton.id = "back-button";
  backButton.textContent = "Back to All Dynasties";
  backButton.style.marginRight = "10px";
  backButton.onclick = () => {
    currentView = "dynasty";
    selectedDynasty = null;
    layout.title.text = "Chinese Buddhist Figures - Dynasty Interactions";
    const plotlyData = createTreemap(globalEdgesData, "dynasty");
    Plotly.react("treemap", plotlyData, layout);
    backButton.remove();
  };
  document.body.insertBefore(backButton, document.getElementById("treemap"));
}

function handleClick(eventData) {
  if (!eventData || !eventData.points || eventData.points.length === 0) return;

  const point = eventData.points[0];
  const parentName = point.parent;
  const dynastyName = point.label;

  // Only handle clicks on first-level dynasty nodes
  if (currentView === "dynasty" && parentName === "Chinese Buddhist Figures") {
    selectedDynasty = Object.keys(DYNASTY_TRANSLATIONS).find(
      (key) => DYNASTY_TRANSLATIONS[key] === dynastyName
    );

    if (selectedDynasty) {
      currentView = "interactions";
      layout.title.text = `Interactions of ${dynastyName}`;
      const plotlyData = createTreemap(
        globalEdgesData,
        "interactions",
        selectedDynasty
      );
      Plotly.react("treemap", plotlyData, layout);
      addBackButton();
    }
  }
}

function initVisualization() {
  Promise.all([d3.csv("../../data/nodes.csv"), d3.csv("../../data/edges.csv")])
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

initVisualization();
