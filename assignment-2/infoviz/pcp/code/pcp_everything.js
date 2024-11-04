console.log('hello world everything');



Promise.all([
    d3.csv('../../data/nodes.csv'),
    d3.csv('../../data/edges.csv')
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
            crossinteractionCounts[v_nationality] = (crossinteractionCounts[v_nationality] || 0) + 1; // here nationality is a chinese string
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

    // console.log('nationalityStats is', nationalityStats)
    // Calculate averages
    const nationalityAverages = Object.entries(nationalityStats).map(([nationality, stats]) => {
        // console.log(nationality, stats);
        //the nationality here is still in chinese
        return {
            nationality: nationality,
            // nationality_chinese_text: nationality,
            midBirthY: (stats.minBirthYear + stats.maxBirthYear) / 2,
            maxBirthY: stats.maxBirthYear,
            meanBirthY: stats.meanBirthYear,
            totalInteractionsRatio: stats.totalInteractions / stats.count,
            selfinteractionRatio: 2*stats.selfInteractions / stats.count, //each self contributes twice to the nationality
            crossinteractionRatio: stats.crossInteractions / stats.count,
        };
    });

    // console.log(nationalityAverages)

    // Sort by median birth year
    nationalityAverages.sort((a, b) => d3.ascending(a.meanBirthY, b.meanBirthY));

    // console.log('nationalityAverages.length is ', nationalityAverages.length)

    function generate_color_scale(){
        let reverseMap = {}
        let len1 = 0
        //nationalityAverages is an array
        nationalityAverages.map((val, idx) => {
            reverseMap[idx] = val;
            // console.log(reverseMap[idx].nationality)
            len1 += 1
        });
        
        len1-=1
        const ans = [];
        const step = 1 / len1;
        let j = 0
         let i=0
        nationalityAverages.map((val, idx)=>{
            //using idx obtain req_str
            req_obj= reverseMap[idx]
            req_str = req_obj.nationality
            let arr = []
            arr = [j.toFixed(2), DYNASTY_COLORS[dynasty_translations[req_str] || 'black']]
            j += step
            ans.push(arr)
             i+=1;
        })
        return ans;

    }

    const data = [{
        type: 'parcoords',
        line: {
            color: nationalityAverages.map((val, idx) => idx),
            colorscale: generate_color_scale()
        },
        dimensions: [
            {
                label: 'Nationality',
                values: nationalityAverages.map(nat => nationalityAverages.indexOf(nat)),
                tickvals: nationalityAverages.map((nat, idx) => idx),
                ticktext: nationalityAverages.map(nat => dynasty_translations[nat.nationality] + " " + nat.nationality)
            },
            { label: 'Mean Birth Year', values: nationalityAverages.map(nat => nat.meanBirthY) , tickvals: new Range(0, 1900, 300)},
            { label: 'Self-Interaction Ratio', values: nationalityAverages.map(nat => nat.selfinteractionRatio) },
            { label: 'Cross-Interaction Ratio', values: nationalityAverages.map(nat => nat.crossinteractionRatio) },
            { label: 'Total-Interaction Ratio', values: nationalityAverages.map(nat => nat.totalInteractionsRatio) },
        ],
    }];

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

    Plotly.newPlot('everything', data, layout);
}).catch(error => console.error('Error loading data:', error));

