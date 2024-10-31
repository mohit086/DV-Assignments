console.log('hello world2');

Promise.all([
    d3.csv('../nodes_0_800.csv'),
    d3.csv('../edges_0_800.csv')
]).then(([nodesData, edgesData]) => {
    // calc the node degree using the edges which have node ids
    const selfinteractionCounts = {};
    const crossinteractionCounts = {}
    const interactionCounts = {}
    edgesData.forEach(edge => {
        interactionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;

        const u_nationality = nodesData.find((node) => edge.source == node.id).nationality
        const v_nationality = nodesData.find((node) => edge.source == node.id).nationality;

        if(u_nationality == null || v_nationality == null)
            console.log('why')
        
        if(u_nationality == v_nationality){
            if(u_nationality in selfinteractionCounts)
                selfinteractionCounts[u_nationality] += 1;
            else
                selfinteractionCounts[u_nationality] = 0

        }
        else{
            if(u_nationality in crossinteractionCounts)
                crossinteractionCounts[u_nationality] += 1;
            else
                crossinteractionCounts[u_nationality] = 0
        }
    });
    console.log(selfinteractionCounts)
    console.log(crossinteractionCounts)

    // Calculate total individuals and total birth years for each nationality
    const nationalityStats = {};

    nodesData.forEach(node => {
        node.interactions = interactionCounts[node.id] || 0;
        node.selfInteractions = interactionCounts[node.id] || 0;
        node.crossInteractions = interactionCounts[node.id] || 0;

        if (!nationalityStats[node.nationality]) {
            nationalityStats[node.nationality] = { totalBirthYear: 0, count: 0, totalInteractions: 0 , selfInteractions: 0, crossInteractions: 0};
        }

        nationalityStats[node.nationality].totalBirthYear += +node.birthY;
        nationalityStats[node.nationality].count += 1;
        nationalityStats[node.nationality].totalInteractions += node.interactions;
        nationalityStats[node.nationality].selfInteractions += node.selfInteractions;
        nationalityStats[node.nationality].crossInteractions += node.crossInteractions;
    });
    console.log('nationalityStats is ', nationalityStats)

    // Calculate average birth year and interaction ratio for each nationality
    const nationalityAverages = Object.entries(nationalityStats).map(([nationality, stats]) => {
        return {
            nationality: nationality,
            averageBirthY: stats.totalBirthYear / stats.count,
            totalInteractionsRatio: stats.selfInteractions / stats.count,
            selfinteractionRatio: stats.selfInteractions / stats.count,
            crossinteractionRatio: stats.crossInteractions / stats.count,
        };
    });

    // Sort by average birth year to get a cleaner graph?
    nationalityAverages.sort((a, b) => d3.ascending(a.averageBirthY, b.averageBirthY));

    // Prepare data for the plot
    const trace = {
        type: 'parcoords',
        line: {
            color: nationalityAverages.map((_, idx) => idx), // Color by index for visualization
            colorscale: [
                [0, 'red'],
                [0.1, 'green'],
                [0.2, 'grey'],
                [0.3, 'violet'],
                [0.4, 'magenta'],
                [0.5, 'turquoise'],
                [0.6, 'brown'],
                [0.7, 'blue'],
                [0.8, 'pink'],
                [0.9, 'orange'],
                [1.0, 'orange'],
            ],
        },
        dimensions: [
            { label: 'Nationality', values: nationalityAverages.map(nat => nationalityAverages.indexOf(nat)), tickvals: nationalityAverages.map((nat, idx) => idx), ticktext: nationalityAverages.map(nat => nat.nationality) },
            { label: 'Average Birth Year', values: nationalityAverages.map(nat => nat.averageBirthY) },
            { label: 'Interaction Ratio', values: nationalityAverages.map(nat => nat.totalInteractionsRatio) },
        ],
    };

    console.log(nationalityAverages)

    const data = [trace];

    const layout = {
        title: 'Parallel Coordinates Plot',
        width: 1000,
        height: 600,
    };

    Plotly.newPlot('plot2', data, layout);
}).catch(error => console.error('Error loading data:', error));
