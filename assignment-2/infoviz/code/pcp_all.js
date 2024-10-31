console.log('hello world all');



dynasty_translations = {
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
}

Promise.all([
    d3.csv('../nodes.csv'),
    d3.csv('../edges.csv')
]).then(([nodesData, edgesData]) => {
    // calc the node degree using the edges which have node ids
    const selfinteractionCounts = {};
    const crossinteractionCounts = {}
    const interactionCounts = {}
    edgesData.forEach(edge => {
        interactionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;
        // selfinteractionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;
        // interactionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;

        const u_nationality = nodesData.find((node) => edge.source == node.id).nationality
        const v_nationality = nodesData.find((node) => edge.target == node.id).nationality;

        if(u_nationality == null || v_nationality == null)
            console.log('why')
        
        if(u_nationality == v_nationality){//self interaction
            selfinteractionCounts[u_nationality] = (selfinteractionCounts[u_nationality] || 0) + 1;
        }
        else{//cross interaction
            crossinteractionCounts[u_nationality] = (crossinteractionCounts[u_nationality] || 0) + 1;
            crossinteractionCounts[v_nationality] = (crossinteractionCounts[v_nationality] || 0) + 1;

        }
    });

    // Calculate total individuals and total birth years for each nationality
    const nationalityStats = {};

    nodesData.forEach(node => {
        node.interactions = interactionCounts[node.id] || 0;
        self_nationality_interactions = selfinteractionCounts[node.nationality] || 0;
        cross_nationality_interactions = crossinteractionCounts[node.nationality] || 0;

        if (!nationalityStats[node.nationality]) {
            nationalityStats[node.nationality] = { maxBirthYear: 0, count: 0, totalInteractions: 0 , selfInteractions: 0, crossInteractions: 0, minBirthYear:  0};
        }

        nationalityStats[node.nationality].maxBirthYear = Math.max(node.birthY, nationalityStats[node.nationality].maxBirthYear);
        nationalityStats[node.nationality].minBirthYear = Math.min(node.birthY, nationalityStats[node.nationality].minBirthYear);

        nationalityStats[node.nationality].count += 1;
        // nationalityStats[node.nationality].totalInteractions += node.interactions;
        nationalityStats[node.nationality].totalInteractions = self_nationality_interactions + cross_nationality_interactions
        nationalityStats[node.nationality].selfInteractions = self_nationality_interactions
        nationalityStats[node.nationality].crossInteractions = cross_nationality_interactions
    });
    console.log('nationalityStats is ', nationalityStats)

    // Calculate average birth year and interaction ratio for each nationality
    const nationalityAverages = Object.entries(nationalityStats).map(([nationality, stats]) => {
        return {
            nationality: nationality,
            midBirthY: (stats.minBirthYear+stats.maxBirthYear) / 2,
            maxBirthY: stats.maxBirthYear,
            totalInteractionsRatio: stats.totalInteractions / stats.count,
            selfinteractionRatio: stats.selfInteractions / stats.count,
            crossinteractionRatio: stats.crossInteractions / stats.count,
        };
    });

    // Sort by average birth year to get a cleaner graph and time ordered graph
    nationalityAverages.sort((a, b) => d3.ascending(a.maxBirthY, b.maxBirthY));


    console.log('nationality averages is', nationalityAverages)

    // Prepare data for the plot
    const trace = {
        type: 'parcoords',
        line: {
            color: nationalityAverages.map((_, idx) => idx), // Color by index for visualization
            colorscale: [
                // [
                    [0.0, 'red'],
                    [0.07, 'orange'],
                    [0.14, 'yellow'],
                    [0.21, 'lightgreen'],
                    [0.28, 'green'],
                    [0.35, 'cyan'],
                    [0.42, 'blue'],
                    [0.49, 'darkblue'],
                    [0.56, 'purple'],
                    [0.63, 'violet'],
                    [0.70, 'magenta'],
                    [0.77, 'pink'],
                    [0.84, 'lightgrey'],
                    [0.91, 'grey'],
                    [0.98, 'black']
                // ]
            ],
        },
        dimensions: [
            { label: 'Nationality', values: nationalityAverages.map(nat => nationalityAverages.indexOf(nat)), tickvals: nationalityAverages.map((nat, idx) => idx), ticktext: nationalityAverages.map(nat => dynasty_translations[nat.nationality] + " \n" + nat.nationality) },
            { label: 'Max Birth Year', values: nationalityAverages.map(nat => nat.maxBirthY) },
            { label: 'Interaction Ratio', values: nationalityAverages.map(nat => nat.totalInteractionsRatio) },
        ],
    };


    const data = [trace];

    const layout = {
        title: 'Parallel Coordinates Plot',
        width: 1000,
        height: 600,
        margin: {
            l: 250, // Left margin
            r: 80, // Right margin
            t: 100, // Top margin
            b: 50  // Bottom margin
        },
    };

    Plotly.newPlot('plotall', data, layout);
    Plotly.newPlot('selfplot', data, layout);
}).catch(error => console.error('Error loading data:', error));
