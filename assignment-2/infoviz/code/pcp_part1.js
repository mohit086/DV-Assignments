// Load data using D3
console.log('hello world1')



Promise.all([
    d3.csv('../nodes_0_800.csv'),
    d3.csv('../edges_0_800.csv')
]).then(([nodesData, edgesData]) => {
    // Preprocess the data
    const interactionCounts = {};
    edgesData.forEach(edge => {
        interactionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;
    });

    // Add interaction counts to nodes
    nodesData.forEach(node => {
        node.interactions = interactionCounts[node.id] || 0;
    });

    // Encode nationalities
    const nationalities = [...new Set(nodesData.map(node => node.nationality))];
    const nationalityMap = new Map(nationalities.map((nat, idx) => [nat, idx]));
    nodesData.forEach(node => {
        node.nationality = nationalityMap.get(node.nationality);
    });

    // Create the parallel coordinates plot
    const trace = {
        type: 'parcoords',
        line: {
            color: nodesData.map(node => node.nationality),
            colorscale: [
                [0, 'red'],
                [0.1, 'red'],
                [0.1, 'green'],
                [0.2, 'green'],
                [0.2, 'grey'],
                [0.3, 'grey'],
                [0.3, 'violet'],
                [0.4, 'violet'],
                [0.4, 'magenta'],
                [0.5, 'magenta'],
                [0.5, 'turquoise'],
                [0.6, 'turquoise'],
                [0.6, 'brown'],
                [0.7, 'brown'],
                [0.7, 'blue'],
                [0.8, 'blue'],
                [0.8, 'pink'],
                [0.9, 'pink'],
                [0.9, 'orange'],
                [1.0, 'orange'],
            ],
        },
        dimensions: [
            { label: 'Nationality', values: nodesData.map(node => node.nationality) },
            { label: 'Birth Year', values: nodesData.map(node => node.birthY) },
            { label: 'Interactions', values: nodesData.map(node => node.interactions) },
        ],
    };

    const data = [trace];

    const layout = {
        title: 'Parallel Coordinates Plot',
        width: 1000,
        height: 600,
    };

    Plotly.newPlot('plot1', data, layout);
}).catch(error => console.error('Error loading data:', error));