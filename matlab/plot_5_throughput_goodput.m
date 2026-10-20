%% =========================================================================
%% GRAPH 5: THROUGHPUT VS ADVERSARIAL DROP RATE & GOODPUT EFFICIENCY
%% =========================================================================

function fig = plot_5_throughput_goodput(outputDir)
    adv_ratios = 0:5:35; % Malicious adversary ratio (%)

    % Goodput (delivered kbps)
    tp_leach     = [480, 420, 350, 275, 205, 140, 95, 60];
    tp_leach_pso = [510, 465, 410, 345, 275, 210, 155, 105];
    tp_proposed  = [540, 505, 465, 415, 360, 305, 250, 190];
    tp_q_insp    = [565, 540, 510, 475, 435, 390, 345, 295];
    tp_quantum   = [585, 572, 555, 535, 510, 485, 455, 420];

    % Drop rates (%)
    drop_leach   = [5.2, 11.5, 18.2, 26.5, 36.8, 48.2, 61.5, 74.0];
    drop_quantum = [1.2,  2.1,  3.4,  5.1,  7.2,  9.8, 12.5, 15.6];

    fig = figure('Name', 'Graph 5: Throughput & Goodput vs Attack Ratio', 'Position', [150, 150, 950, 520], 'Color', 'w');
    
    % Dual Y-axis
    yyaxis left;
    hold on; box on; grid on;
    set(gca, 'GridLineStyle', '--', 'GridAlpha', 0.4);

    plot(adv_ratios, tp_leach, 'o--', 'Color', [0.91, 0.3, 0.24], 'LineWidth', 1.8, 'MarkerSize', 6, 'DisplayName', 'Throughput: LEACH');
    plot(adv_ratios, tp_leach_pso, 's--', 'Color', [0.90, 0.49, 0.13], 'LineWidth', 1.8, 'MarkerSize', 6, 'DisplayName', 'Throughput: LEACH+PSO');
    plot(adv_ratios, tp_proposed, 'd-', 'Color', [0.20, 0.60, 0.86], 'LineWidth', 1.8, 'MarkerSize', 6, 'DisplayName', 'Throughput: Proposed Classical');
    plot(adv_ratios, tp_q_insp, '^-', 'Color', [0.61, 0.35, 0.71], 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Throughput: Quantum-Inspired');
    plot(adv_ratios, tp_quantum, 'p-', 'Color', [0.18, 0.8, 0.44], 'LineWidth', 2.6, 'MarkerSize', 8, 'DisplayName', 'Throughput: Full Quantum QSE-FCM');

    ylabel('Effective Network Goodput (kbps)', 'FontSize', 10.5, 'FontWeight', 'bold');
    ylim([0, 650]);

    yyaxis right;
    plot(adv_ratios, drop_leach, 'x:', 'Color', [0.7, 0.1, 0.1], 'LineWidth', 1.8, 'MarkerSize', 7, 'DisplayName', 'Drop Rate: LEACH (%)');
    plot(adv_ratios, drop_quantum, '+:', 'Color', [0.1, 0.6, 0.2], 'LineWidth', 2.0, 'MarkerSize', 7, 'DisplayName', 'Drop Rate: Quantum (%)');
    ylabel('Packet Loss Ratio (%)', 'FontSize', 10.5, 'FontWeight', 'bold');
    ylim([0, 100]);

    xlabel('Adversary Malicious Node Injection Ratio (%)', 'FontSize', 11, 'FontWeight', 'bold');
    title({'Graph 5: Effective Network Goodput vs Adversarial Injection Stress Test', ...
           'Resilience Under High Malicious Adversary Density (0% to 35%)'}, 'FontSize', 12, 'FontWeight', 'bold');
    xlim([0, 35]);
    legend('Location', 'southwest', 'FontSize', 8.5);

    if nargin > 0 && ~isempty(outputDir)
        saveas(fig, fullfile(outputDir, '5_packet_loss_matlab.png'));
        saveas(fig, fullfile(outputDir, '5_packet_loss_throughput.fig'));
    end
end
