// Dynasty translations mapping for display
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
  
  // Gender color scheme
  const GENDER_COLORS = {
    'Male': '#2171b5',
    'Female': '#6baed6',
    'Unknown': '#bdbdbd'
  };
  
  // Create the visualization
  function createTreemap(nodesData) {
    // Group data by nationality and gender
    const groupedData = d3.group(nodesData,
      d => d.nationality,
      d => d.gender || 'Unknown'
    );
  
    // Transform data for treemap
    const hierarchyData = {
      name: "Buddhist Figures",
      children: Array.from(groupedData, ([nationality, genderGroups]) => ({
        name: nationality,
        displayName: DYNASTY_TRANSLATIONS[nationality] || nationality,
        children: Array.from(genderGroups, ([gender, nodes]) => ({
          name: gender,
          value: nodes.length,
          nationality: nationality
        }))
      }))
    };
  
    // Create treemap data structure
    const plotlyData = [{
      type: "treemap",
      labels: [],
      parents: [],
      values: [],
      textinfo: "label+value+percent parent",
      hovertemplate: `
        Nationality: %{parent}
        Gender: %{label}
        Count: %{value}
        Percentage: %{percentParent:.1%}
      `,
      marker: {
        colors: [],
        line: { width: 2 }
      }
    }];
  
    // Process hierarchy for Plotly
    function processNode(node, parent = "") {
      const displayName = node.displayName || node.name;
      plotlyData[0].labels.push(displayName);
      plotlyData[0].parents.push(parent);
      plotlyData[0].values.push(node.value || 0);
  
      if (node.children) {
        node.children.forEach(child => processNode(child, displayName));
      }
    }
  
    processNode(hierarchyData);
  
    // Create color scheme
    const nationalityColors = d3.scaleOrdinal()
      .domain([...new Set(nodesData.map(d => d.nationality))])
      .range(d3.schemeSet3);
  
    // Apply colors
    plotlyData[0].marker.colors = plotlyData[0].labels.map((label, i) => {
      const parent = plotlyData[0].parents[i];
      if (parent === "") return '#ffffff';  // root
      if (parent === "Buddhist Figures") return nationalityColors(label);  // nationality level
      return GENDER_COLORS[label] || '#bdbdbd';  // gender level
    });
  
    return plotlyData;
  }
  
  // Layout configuration
  const layout = {
    width: 1100,
    height: 700,
    margin: { l: 0, r: 0, t: 0, b: 0 },
    hoverlabel: {
      bgcolor: 'white',
      bordercolor: '#ddd',
      font: { family: 'Arial', size: 12 }
    }
  };
  
  // Create legend
  function createLegend(nodesData) {
    const legendDiv = document.getElementById('nationalityLegend');
    legendDiv.innerHTML = ''; // Clear existing legend
  
    const nationalityColors = d3.scaleOrdinal()
      .domain([...new Set(nodesData.map(d => d.nationality))])
      .range(d3.schemeSet3);
  
    [...new Set(nodesData.map(d => d.nationality))].forEach(nationality => {
      const legendItem = document.createElement('div');
      legendItem.className = 'legend-item';
      
      const colorBox = document.createElement('div');
      colorBox.className = 'legend-color';
      colorBox.style.backgroundColor = nationalityColors(nationality);
      
      const label = document.createElement('span');
      label.textContent = DYNASTY_TRANSLATIONS[nationality] || nationality;
      
      legendItem.appendChild(colorBox);
      legendItem.appendChild(label);
      legendDiv.appendChild(legendItem);
    });
  }
  
  // Main initialization function
  function initVisualization() {
    // Load data
    Promise.all([
      d3.csv('nodes.csv'),
      d3.csv('edges.csv')
    ]).then(([nodesData, edgesData]) => {
      const plotlyData = createTreemap(nodesData);
      createLegend(nodesData);
      
      // Create treemap
      Plotly.newPlot('treemap', plotlyData, layout);
    }).catch(error => console.error('Error loading data:', error));
  }
  
  // Add necessary CSS
  const style = document.createElement('style');
  style.textContent = `
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
  document.addEventListener('DOMContentLoaded', initVisualization);