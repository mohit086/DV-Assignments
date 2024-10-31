console.log('hello world all');

const dynasty_translations = {
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

Promise.all([
    d3.csv('../nodes.csv'),
    d3.csv('../edges.csv')
]).then(([nodesData, edgesData]) => {
    // Calculate interaction counts
    const selfinteractionCounts = {};
    const crossinteractionCounts = {};
    const interactionCounts = {};
    
    edgesData.forEach(edge => {
        interactionCounts[edge.source] = (interactionCounts[edge.source] || 0) + 1;

        const u_nationality = nodesData.find(node => edge.source == node.id)?.nationality;
        const v_nationality = nodesData.find(node => edge.target == node.id)?.nationality;

        if (u_nationality == null || v_nationality == null) {
            console.log('Invalid nationality found');
        }

        if (u_nationality === v_nationality) {
            selfinteractionCounts[u_nationality] = (selfinteractionCounts[u_nationality] || 0) + 1;
        } else {
            crossinteractionCounts[u_nationality] = (crossinteractionCounts[u_nationality] || 0) + 1;
            crossinteractionCounts[v_nationality] = (crossinteractionCounts[v_nationality] || 0) + 1;
        }
    });

    // Calculate nationality stats
    const nationalityStats = {};

    nodesData.forEach(node => {
        const nationality = node.nationality;
        node.interactions = interactionCounts[node.id] || 0;
        const self_nationality_interactions = selfinteractionCounts[nationality] || 0;
        const cross_nationality_interactions = crossinteractionCounts[nationality] || 0;

        if (!nationalityStats[nationality]) {
            nationalityStats[nationality] = { maxBirthYear: 0, count: 0, totalInteractions: 0, selfInteractions: 0, crossInteractions: 0, minBirthYear: Infinity };
        }

        nationalityStats[nationality].maxBirthYear = Math.max(node.birthY, nationalityStats[nationality].maxBirthYear);
        nationalityStats[nationality].minBirthYear = Math.min(node.birthY, nationalityStats[nationality].minBirthYear);
        if(nationalityStats[nationality].count == 0)
            nationalityStats[nationality].meanBirthYear = node.birthY
        else
            nationalityStats[nationality].meanBirthYear = (nationalityStats[nationality].meanBirthYear * (nationalityStats[nationality].count) / (nationalityStats[nationality].count+1)) + (node.birthY/(nationalityStats[nationality].count+1))
        nationalityStats[nationality].count += 1;
        nationalityStats[nationality].totalInteractions = self_nationality_interactions + cross_nationality_interactions;
        nationalityStats[nationality].selfInteractions = self_nationality_interactions;
        nationalityStats[nationality].crossInteractions = cross_nationality_interactions;
    });

    // Calculate averages
    const nationalityAverages = Object.entries(nationalityStats).map(([nationality, stats]) => {
        return {
            nationality: nationality,
            midBirthY: (stats.minBirthYear + stats.maxBirthYear) / 2,
            maxBirthY: stats.maxBirthYear,
            meanBirthY: stats.meanBirthYear,
            totalInteractionsRatio: stats.totalInteractions / stats.count,
            selfinteractionRatio: 2*stats.selfInteractions / stats.count, //each self contributes twice to the nationality
            crossinteractionRatio: stats.crossInteractions / stats.count,
        };
    });

    // Sort by median birth year
    nationalityAverages.sort((a, b) => d3.ascending(a.meanBirthY, b.meanBirthY));

    // Prepare data for the plots
    const baseTrace = {
        type: 'parcoords',
        line: {
            color: nationalityAverages.map((_, idx) => idx),
            colorscale: [
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
            ],
        },
    };

    const createTrace = (label, values) => ({
        ...baseTrace,
        dimensions: [
            {
                label: 'Nationality',
                values: nationalityAverages.map(nat => nationalityAverages.indexOf(nat)),
                tickvals: nationalityAverages.map((nat, idx) => idx),
                ticktext: nationalityAverages.map(nat => dynasty_translations[nat.nationality] + " \n" + nat.nationality)
            },
            { label: 'Mean Birth Year', values: nationalityAverages.map(nat => nat.meanBirthY) , tickvals: new Range(0, 1900, 300)},
            { label: label, values: values },
        ],
    });

    const data = [createTrace('Total Interaction Ratio', nationalityAverages.map(nat => nat.totalInteractionsRatio))];
    const data2 = [createTrace('Self-Interaction Ratio', nationalityAverages.map(nat => nat.selfinteractionRatio))];
    const data3 = [createTrace('Cross-Interaction Ratio', nationalityAverages.map(nat => nat.crossinteractionRatio))];

    const layout = {
        title: 'Parallel Coordinates Plot',
        width: 1000,
        height: 600,
        margin: {
            l: 250,
            r: 80,
            t: 100,
            b: 50
        },
    };

    Plotly.newPlot('plotall', data, layout);
    Plotly.newPlot('selfplot', data2, layout);
    Plotly.newPlot('crossplot', data3, layout);
}).catch(error => console.error('Error loading data:', error));
