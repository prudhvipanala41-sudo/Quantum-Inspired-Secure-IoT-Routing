%% =========================================================================
%% GRAPH 9: 4-WAY QUANTUM CLUSTERING RADAR BENCHMARK & QUALITY METRICS
%% =========================================================================

function fig = plot_9_clustering_radar_metrics(outputDir)
    fig = figure('Name', 'Graph 9: 4-Way Clustering Evaluation Benchmark', 'Position', [150, 150, 1000, 500], 'Color', 'w');

    % Metric names and scores
    % Metrics: [Silhouette (norm), 1/DB (norm), CH Index (norm), Quantum Coherence, Energy Balance]
    categories = {'Silhouette Score', '1 / Davies-Bouldin', 'Calinski-Harabasz', 'Quantum Coherence', 'Energy Uniformity'};
    num_vars = length(categories);

    kmeans_scores = [0.38, 0.42, 0.45, 0.71, 0.55];
    fcm_scores    = [0.42, 0.48, 0.52, 0.75, 0.62];
    qdf_scores    = [0.53, 0.68, 0.74, 0.88, 0.82];
    qse_scores    = [0.62, 0.85, 0.91, 0.97, 0.94];

    % -------------------------------------------------------------
    % Subplot 1: Bar Comparison Chart
    % -------------------------------------------------------------
    subplot(1, 2, 1);
    hold on; box on; grid on;
    set(gca, 'GridLineStyle', '--', 'GridAlpha', 0.4);

    bar_data = [0.382, 0.710;
                0.415, 0.745;
                0.528, 0.884;
                0.612, 0.965];
    
    b = bar(bar_data, 'grouped');
    b(1).FaceColor = [0.0, 0.85, 0.95];
    b(2).FaceColor = [0.48, 0.20, 0.80];

    set(gca, 'XTickLabel', {'K-Means', 'FCM', 'QDF-KMeans', 'QSE-FCM'}, 'FontWeight', 'bold');
    ylabel('Index Metric Score [0, 1]', 'FontSize', 10.5, 'FontWeight', 'bold');
    title('(a) Silhouette & Quantum Coherence', 'FontSize', 11.5, 'FontWeight', 'bold');
    ylim([0, 1.18]);
    legend({'Silhouette Score (↑)', 'Quantum Coherence (↑)'}, 'Location', 'northwest', 'FontSize', 8.5);

    % -------------------------------------------------------------
    % Subplot 2: Radar Spider Chart
    % -------------------------------------------------------------
    subplot(1, 2, 2);
    hold on; axis equal; axis off;

    angles = linspace(0, 2*pi, num_vars + 1);
    
    % Draw concentric grid rings
    for r = 0.2:0.2:1.0
        plot(r*cos(angles), r*sin(angles), 'Color', [0.85, 0.85, 0.85], 'LineWidth', 0.9);
        text(0.02, r, sprintf('%.1f', r), 'Color', [0.5, 0.5, 0.5], 'FontSize', 7.5);
    end

    % Draw spoke axes
    for i = 1:num_vars
        plot([0, cos(angles(i))], [0, sin(angles(i))], 'Color', [0.75, 0.75, 0.75], 'LineWidth', 1.0);
        text(1.15*cos(angles(i)), 1.15*sin(angles(i)), categories{i}, ...
            'HorizontalAlignment', 'center', 'FontSize', 8.5, 'FontWeight', 'bold');
    end

    % Plot radar polygons
    km_poly  = [kmeans_scores, kmeans_scores(1)];
    fcm_poly = [fcm_scores, fcm_scores(1)];
    qdf_poly = [qdf_scores, qdf_scores(1)];
    qse_poly = [qse_scores, qse_scores(1)];

    plot(km_poly.*cos(angles),  km_poly.*sin(angles),  'o--', 'Color', [0.90, 0.49, 0.13], 'LineWidth', 1.5, 'DisplayName', 'Classical K-Means');
    plot(fcm_poly.*cos(angles), fcm_poly.*sin(angles), 's--', 'Color', [0.20, 0.60, 0.86], 'LineWidth', 1.5, 'DisplayName', 'Classical FCM');
    plot(qdf_poly.*cos(angles), qdf_poly.*sin(angles), '^-',  'Color', [0.61, 0.35, 0.71], 'LineWidth', 1.8, 'DisplayName', 'Quantum Fidelity KMeans');
    plot(qse_poly.*cos(angles), qse_poly.*sin(angles), 'p-',  'Color', [0.18, 0.8, 0.44], 'LineWidth', 2.4, 'DisplayName', 'Quantum Superposition FCM');
    fill(qse_poly.*cos(angles), qse_poly.*sin(angles), [0.18, 0.8, 0.44], 'FaceAlpha', 0.15, 'EdgeColor', 'none', 'HandleVisibility', 'off');

    title('(b) Multi-Attribute Radar Benchmark', 'FontSize', 11.5, 'FontWeight', 'bold');
    legend('Location', 'southoutside', 'Orientation', 'horizontal', 'FontSize', 8.0);

    sgtitle('Graph 9: 4-Way Quantum vs Classical IoT Clustering Performance Benchmark', 'FontSize', 13, 'FontWeight', 'bold');

    if nargin > 0 && ~isempty(outputDir)
        saveas(fig, fullfile(outputDir, '9_clustering_metrics_matlab.png'));
        saveas(fig, fullfile(outputDir, '9_clustering_evaluation_metrics.fig'));
    end
end
