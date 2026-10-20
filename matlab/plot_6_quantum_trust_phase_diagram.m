%% =========================================================================
%% GRAPH 6: QUANTUM DENSITY MATRIX PURITY PHASE DIAGRAM & SURFACE
%% =========================================================================

function fig = plot_6_quantum_trust_phase_diagram(nodesData, outputDir)
    fig = figure('Name', 'Graph 6: Quantum Density Trust Phase Diagram', 'Position', [150, 150, 950, 520], 'Color', 'w');

    % Analytical 2D Grid for Phase Space Manifold
    [Ps, Gamma] = meshgrid(linspace(0, 1, 100), linspace(0.5, 1, 100));
    beta = 0.2;
    D_tr = 1 - Ps;
    TQ_surface = Ps .* sqrt(Gamma) .* (1 - beta * D_tr);

    % Subplot 1: Contour Phase Manifold
    subplot(1, 2, 1);
    hold on; box on;
    contourf(Ps, Gamma, TQ_surface, 25, 'LineColor', 'none');
    colormap(gca, parula);
    c = colorbar;
    c.Label.String = 'Quantum Trust Metric T_Q';
    c.Label.FontSize = 9.5;

    % Decision Boundaries
    yline(0.85, 'w--', 'LineWidth', 1.5);
    xline(0.75, 'w--', 'LineWidth', 1.5);
    text(0.1, 0.95, '\bf Malicious Zone', 'Color', 'w', 'FontSize', 9.5);
    text(0.78, 0.95, '\bf Trusted Pure State', 'Color', 'w', 'FontSize', 9.5);

    xlabel('Forwarding Probability p_s = forwarded / sent', 'FontSize', 10, 'FontWeight', 'bold');
    ylabel('Density Matrix Purity \gamma = Tr(\rho^2)', 'FontSize', 10, 'FontWeight', 'bold');
    title('(a) Analytical Quantum Trust Phase Space', 'FontSize', 11, 'FontWeight', 'bold');
    xlim([0, 1]); ylim([0.5, 1.0]);

    % Subplot 2: Empirical Node State Scatter
    subplot(1, 2, 2);
    hold on; box on; grid on;
    set(gca, 'GridLineStyle', '--', 'GridAlpha', 0.4);

    trust = nodesData.trust;
    is_mal = logical(nodesData.is_malicious);
    purity = (1 - trust).^2 + trust.^2;

    scatter(trust(~is_mal), purity(~is_mal), 45, [0.18, 0.8, 0.44], 'filled', ...
        'MarkerFaceAlpha', 0.7, 'DisplayName', 'Authentic Nodes (\gamma \approx 1.0)');
    scatter(trust(is_mal), purity(is_mal), 85, [0.91, 0.3, 0.24], 'x', 'LineWidth', 1.8, ...
        'DisplayName', 'Detected Threat Nodes (\gamma < 0.75)');

    xline(0.75, 'Color', [0.95, 0.6, 0.07], 'LineWidth', 1.5, 'LineStyle', '--', 'DisplayName', 'Trusted Threshold (T_Q \ge 0.75)');
    xline(0.45, 'Color', [0.9, 0.1, 0.1], 'LineWidth', 1.5, 'LineStyle', ':', 'DisplayName', 'Malicious Threshold (T_Q < 0.45)');

    xlabel('Calculated Quantum Trust Score (T_Q)', 'FontSize', 10, 'FontWeight', 'bold');
    ylabel('Quantum State Purity \gamma = Tr(\rho^2)', 'FontSize', 10, 'FontWeight', 'bold');
    title('(b) Empirical IoT Node Classification', 'FontSize', 11, 'FontWeight', 'bold');
    xlim([0, 1]); ylim([0.48, 1.02]);
    legend('Location', 'northwest', 'FontSize', 8.5);

    sgtitle('Graph 6: Quantum Density Matrix Trace Fidelity Trust & State Purity Manifold', 'FontSize', 13, 'FontWeight', 'bold');

    if nargin > 1 && ~isempty(outputDir)
        saveas(fig, fullfile(outputDir, '6_quantum_trust_matlab.png'));
        saveas(fig, fullfile(outputDir, '6_quantum_trust_purity_scatter.fig'));
    end
end
