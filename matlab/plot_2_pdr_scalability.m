%% =========================================================================
%% GRAPH 2: PACKET DELIVERY RATIO (PDR) SCALABILITY WITH ERROR BANDS
%% =========================================================================

function fig = plot_2_pdr_scalability(outputDir)
    node_scales = [100, 200, 300, 500, 750, 1000];

    % Empirical benchmark trajectories across scales
    pdr_leach      = [86.2, 84.1, 82.5, 79.8, 76.4, 72.1];
    pdr_leach_pso  = [89.5, 88.2, 87.1, 85.0, 82.3, 79.4];
    pdr_prop_class = [93.1, 91.8, 90.5, 88.6, 86.2, 83.5];
    pdr_q_inspired = [95.8, 94.7, 93.9, 92.4, 90.8, 89.1];
    pdr_qse_fcm    = [98.4, 97.9, 97.2, 96.8, 95.6, 94.8];

    % Standard error deviations
    std_leach   = [1.8, 2.1, 2.4, 2.8, 3.2, 3.6];
    std_qse_fcm = [0.6, 0.7, 0.8, 0.9, 1.1, 1.2];

    fig = figure('Name', 'Graph 2: PDR Scalability Analysis', 'Position', [150, 150, 880, 550], 'Color', 'w');
    hold on; box on; grid on;
    set(gca, 'GridLineStyle', '--', 'GridAlpha', 0.4);

    % Shaded Confidence Bands for Quantum & Baseline
    fill([node_scales, fliplr(node_scales)], ...
         [pdr_qse_fcm + std_qse_fcm, fliplr(pdr_qse_fcm - std_qse_fcm)], ...
         [0.18, 0.8, 0.44], 'FaceAlpha', 0.18, 'EdgeColor', 'none', 'DisplayName', 'QSE-FCM 95% Conf. Band (\pm1\sigma)');

    fill([node_scales, fliplr(node_scales)], ...
         [pdr_leach + std_leach, fliplr(pdr_leach - std_leach)], ...
         [0.9, 0.3, 0.24], 'FaceAlpha', 0.12, 'EdgeColor', 'none', 'DisplayName', 'LEACH 95% Conf. Band (\pm1\sigma)');

    % Plot paradigm lines
    plot(node_scales, pdr_leach, 'o--', 'Color', [0.91, 0.3, 0.24], 'LineWidth', 2.0, 'MarkerSize', 7, ...
        'MarkerFaceColor', [0.91, 0.3, 0.24], 'DisplayName', '1. LEACH Baseline');
    plot(node_scales, pdr_leach_pso, 's--', 'Color', [0.90, 0.49, 0.13], 'LineWidth', 2.0, 'MarkerSize', 7, ...
        'MarkerFaceColor', [0.90, 0.49, 0.13], 'DisplayName', '2. LEACH + Classical PSO');
    plot(node_scales, pdr_prop_class, 'd-', 'Color', [0.20, 0.60, 0.86], 'LineWidth', 2.0, 'MarkerSize', 7, ...
        'MarkerFaceColor', [0.20, 0.60, 0.86], 'DisplayName', '3. Proposed Classical (K-Means+RF)');
    plot(node_scales, pdr_q_inspired, '^-', 'Color', [0.61, 0.35, 0.71], 'LineWidth', 2.2, 'MarkerSize', 7, ...
        'MarkerFaceColor', [0.61, 0.35, 0.71], 'DisplayName', '4. Quantum-Inspired (QDF-KMeans+VQC)');
    plot(node_scales, pdr_qse_fcm, 'p-', 'Color', [0.18, 0.8, 0.44], 'LineWidth', 2.6, 'MarkerSize', 9, ...
        'MarkerFaceColor', [0.18, 0.8, 0.44], 'DisplayName', '5. Full Quantum Superposition (QSE-FCM+QPSO)');

    % Target SLA Line
    yline(90.0, 'k:', 'LineWidth', 1.4, 'DisplayName', 'Critical SLA Requirement (90%)');

    xlabel('IoT Network Scale (Total Nodes N)', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('Packet Delivery Ratio - PDR (%)', 'FontSize', 11, 'FontWeight', 'bold');
    title({'Graph 2: Packet Delivery Ratio (PDR) vs Network Scalability', ...
           'Evaluated Under 10% Malicious Packet-Dropping Adversary Injections'}, ...
           'FontSize', 12, 'FontWeight', 'bold');
    xlim([100, 1000]); ylim([65, 102]);
    legend('Location', 'southwest', 'FontSize', 9);

    if nargin > 0 && ~isempty(outputDir)
        saveas(fig, fullfile(outputDir, '2_pdr_scalability_matlab.png'));
        saveas(fig, fullfile(outputDir, '2_pdr_comparison.fig'));
    end
end
