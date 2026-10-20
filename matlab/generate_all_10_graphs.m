%% =========================================================================
%% ⚛️ QUANTUM-ENHANCED SECURE IoT ROUTING - MASTER MATLAB GRAPH GENERATOR
%% =========================================================================
%% Generates 10 Publication-Quality (IEEE / Elsevier format) MATLAB Figures
%% for Quantum State Amplitude Hilbert Embedding, QSE-FCM Clustering,
%% Parameterized VQC Cluster-Head Election, and Q-PSO Multi-Objective Routing.
%% =========================================================================

function generate_all_10_graphs()
    fprintf('\n===============================================================\n');
    fprintf('⚛️  QUANTUM SECURE IoT ROUTING - MATLAB 10-GRAPH SUITE GENERATOR\n');
    fprintf('===============================================================\n\n');

    % Setup paths
    scriptDir = fileparts(mfilename('fullpath'));
    projectDir = fullfile(scriptDir, '..');
    outputDir = fullfile(projectDir, 'results', 'output');
    dataDir = fullfile(projectDir, 'data');

    if ~exist(outputDir, 'dir')
        mkdir(outputDir);
    end

    % Check if dataset exists
    nodesFile = fullfile(dataDir, 'nodes.csv');
    if exist(nodesFile, 'file')
        nodesData = readtable(nodesFile);
        fprintf('[+] Loaded topology dataset: %d nodes from %s\n', height(nodesData), nodesFile);
    else
        fprintf('[!] nodes.csv not found. Synthesizing 1000 nodes dataset in MATLAB...\n');
        nodesData = synthesize_nodes(1000, 200);
    end

    % Set default graphical aesthetics
    set(0, 'DefaultFigureColor', 'w');
    set(0, 'DefaultAxesFontName', 'Helvetica');
    set(0, 'DefaultAxesFontSize', 10);
    set(0, 'DefaultAxesLineWidth', 1.1);
    set(0, 'DefaultLineLineWidth', 1.8);

    fprintf('\n[*] Generating 10 Complex Publication-Quality MATLAB Figures...\n');

    % 1. Network Topology
    fig1 = plot_1_network_topology(nodesData, outputDir);
    fprintf('  [1/10] ✓ Graph 1: Network Topology & Voronoi Quantum Tessellation\n');

    % 2. PDR Scalability
    fig2 = plot_2_pdr_scalability(outputDir);
    fprintf('  [2/10] ✓ Graph 2: Packet Delivery Ratio Scalability (200-1000 Nodes)\n');

    % 3. Latency CDF & Boxplot
    fig3 = plot_3_latency_cdf_boxplot(outputDir);
    fprintf('  [3/10] ✓ Graph 3: Cumulative Latency Distribution & Boxplot\n');

    % 4. Energy Lifetime
    fig4 = plot_4_energy_lifetime_survival(outputDir);
    fprintf('  [4/10] ✓ Graph 4: Energy Depletion Profile & FND/HND/LND Survival\n');

    % 5. Throughput & Drop Rate
    fig5 = plot_5_throughput_goodput(outputDir);
    fprintf('  [5/10] ✓ Graph 5: Throughput Efficiency vs Adversary Drop Rate\n');

    % 6. Quantum Trust Phase Diagram
    fig6 = plot_6_quantum_trust_phase_diagram(nodesData, outputDir);
    fprintf('  [6/10] ✓ Graph 6: Density Matrix Purity Phase Manifold\n');

    % 7. ROC & PR Curves
    fig7 = plot_7_roc_pr_security_curves(outputDir);
    fprintf('  [7/10] ✓ Graph 7: Security Detection ROC & PR Iso-Contours\n');

    % 8. Q-PSO vs PSO Convergence & Phase Space
    fig8 = plot_8_qpso_phase_space_convergence(outputDir);
    fprintf('  [8/10] ✓ Graph 8: Q-PSO Hamiltonian Trajectory & Tunneling\n');

    % 9. Clustering Radar & Scorecard
    fig9 = plot_9_clustering_radar_metrics(outputDir);
    fprintf('  [9/10] ✓ Graph 9: 4-Way Quantum Clustering Radar Benchmark\n');

    % 10. 3D Pareto Front
    fig10 = plot_10_pareto_3d_front(outputDir);
    fprintf('  [10/10] ✓ Graph 10: 3D Multi-Objective Routing Pareto Optimal Front\n');

    fprintf('\n===============================================================\n');
    fprintf('[+] ALL 10 MATLAB FIGURES SUCCESSFULLY COMPILED & EXPORTED!\n');
    fprintf('    Saved to directory: %s\n', outputDir);
    fprintf('===============================================================\n\n');
end

function df = synthesize_nodes(N, area)
    rng(42);
    x = rand(N, 1) * area;
    y = rand(N, 1) * area;
    energy = 70 + rand(N, 1) * 30;
    trust = ones(N, 1);
    packet_rate = randi([5, 25], N, 1);
    cluster_id = randi([0, 7], N, 1);
    is_ch = false(N, 1);
    for c = 0:7
        c_idx = find(cluster_id == c);
        if ~isempty(c_idx)
            is_ch(c_idx(1)) = true;
        end
    end
    is_malicious = rand(N, 1) < 0.10;
    trust(is_malicious) = 0.2 + rand(sum(is_malicious), 1) * 0.35;
    dist_to_bs = sqrt((x - area/2).^2 + (y - area/2).^2);
    
    df = table((0:N-1)', x, y, energy, trust, packet_rate, cluster_id, is_ch, is_malicious, dist_to_bs, ...
        'VariableNames', {'node_id', 'x', 'y', 'energy', 'trust', 'packet_rate', 'cluster_id', 'is_ch', 'is_malicious', 'distance_to_bs'});
end
