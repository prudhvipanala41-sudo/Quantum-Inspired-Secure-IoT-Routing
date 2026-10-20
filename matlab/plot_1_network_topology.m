%% =========================================================================
%% GRAPH 1: QUANTUM-CLUSTERED IoT TOPOLOGY & VORONOI TESSELLATION
%% =========================================================================

function fig = plot_1_network_topology(nodesData, outputDir)
    area = 200;
    x = nodesData.x;
    y = nodesData.y;
    cid = nodesData.cluster_id;
    is_ch = logical(nodesData.is_ch);
    is_mal = logical(nodesData.is_malicious);
    energy = nodesData.energy;

    fig = figure('Name', 'Graph 1: Quantum Network Topology', 'Position', [100, 100, 850, 750], 'Color', 'w');
    hold on; box on; grid on;
    set(gca, 'GridLineStyle', '--', 'GridAlpha', 0.4);

    % Color palette for clusters
    u_cid = unique(cid);
    k = length(u_cid);
    colors = lines(k);

    % 1. Voronoi cells of Cluster Heads if CHs exist
    ch_x = x(is_ch);
    ch_y = y(is_ch);
    if length(ch_x) >= 3
        try
            [vx, vy] = voronoi(ch_x, ch_y);
            plot(vx, vy, 'Color', [0.7, 0.7, 0.7], 'LineWidth', 1.2, 'LineStyle', ':', 'DisplayName', 'Quantum Cluster Boundaries');
        catch
        end
    end

    % 2. Scatter normal cluster nodes
    for i = 1:k
        c_val = u_cid(i);
        mask = (cid == c_val) & ~is_ch & ~is_mal;
        scatter(x(mask), y(mask), 35, colors(i,:), 'filled', 'MarkerFaceAlpha', 0.65, ...
            'DisplayName', sprintf('Cluster %d (n=%d)', c_val, sum(mask)));
    end

    % 3. Cluster Heads with Radio Range Rings
    Rc = 35;
    theta = linspace(0, 2*pi, 100);
    for idx = find(is_ch)'
        plot(x(idx) + Rc*cos(theta), y(idx) + Rc*sin(theta), 'Color', [0.95, 0.77, 0.05, 0.4], 'LineWidth', 1.0, 'HandleVisibility', 'off');
    end
    scatter(x(is_ch), y(is_ch), 220, [0.95, 0.77, 0.05], 'p', 'filled', 'MarkerEdgeColor', 'k', ...
        'LineWidth', 1.5, 'DisplayName', 'Quantum Cluster Head (VQC)');

    % 4. Malicious Nodes
    if any(is_mal)
        scatter(x(is_mal), y(is_mal), 75, [0.9, 0.1, 0.1], 'x', 'LineWidth', 2.0, ...
            'DisplayName', sprintf('Malicious Adversary (n=%d)', sum(is_mal)));
    end

    % 5. Base Station Gateway
    bs_x = area / 2;
    bs_y = area / 2;
    scatter(bs_x, bs_y, 250, [0.1, 0.5, 0.9], 's', 'filled', 'MarkerEdgeColor', 'k', ...
        'LineWidth', 2.0, 'DisplayName', 'Base Station Gateway (BS)');

    % Add Direct Transmission Links from CHs to BS
    for idx = find(is_ch)'
        plot([x(idx), bs_x], [y(idx), bs_y], 'Color', [0.16, 0.5, 0.72, 0.5], 'LineWidth', 1.1, 'LineStyle', '-.');
    end

    xlabel('Spatial X Coordinate (meters)', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('Spatial Y Coordinate (meters)', 'FontSize', 11, 'FontWeight', 'bold');
    title({'Graph 1: Quantum-Clustered IoT Network Topology & Voronoi Tessellation', ...
           sprintf('(N = %d Nodes, K = %d Quantum Clusters, Area = %dx%d m^2)', length(x), k, area, area)}, ...
           'FontSize', 12, 'FontWeight', 'bold');
    xlim([0, area]); ylim([0, area]);
    legend('Location', 'northeastoutside', 'FontSize', 8.5);

    if nargin > 1 && ~isempty(outputDir)
        saveas(fig, fullfile(outputDir, '1_network_topology_matlab.png'));
        saveas(fig, fullfile(outputDir, '1_network_topology.fig'));
    end
end
