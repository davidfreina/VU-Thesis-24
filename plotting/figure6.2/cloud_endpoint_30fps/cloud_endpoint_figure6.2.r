library(ggplot2)
library(dplyr)
library(reshape2)
library(scales)
setwd(getSrcDirectory(function(){})[1])

process_data <- function(file_path) {
  data <- read.csv(file_path, check.names=FALSE)

  data$Timestamp <- data$Timestamp - min(data$Timestamp)
  if ("intel-rapl:0:0 (W)" %in% names(data)) {
    if ("intel-rapl:1:0 (W)" %in% names(data)) {
      data$'Memory (W)' <- data$'intel-rapl:0:0 (W)' + data$'intel-rapl:1:0 (W)'
      data = subset(data, select = -c(`intel-rapl:0:0 (W)`, `intel-rapl:1:0 (W)`))
    } else {
      data$'Memory (W)' <- data$'intel-rapl:0:0 (W)'
      data = subset(data, select = -c(`intel-rapl:0:0 (W)`))
    }
  }

  columns_with_units <- grep("\\(.*\\)", names(data), value = TRUE)
  data <- data %>% select(Timestamp, all_of(columns_with_units))

  if ("CPUMaxIdleModel Utilization (%)" %in% names(data)) {
    data$`CPUMaxIdleModel Utilization (%)` <- sapply(data$`CPUMaxIdleModel Utilization (%)`, function(x) {
      sum(as.numeric(unlist(strsplit(gsub("\\[|\\]", "", x), ","))))
    })
  }

  melted_data <- melt(data, id.vars = 'Timestamp')

  if ("CameraModel (W)" %in% names(data)) {
    variable_labels <- c(
      `eno1 (W)` = 'NIC (W)',
      `eno1 Utilization (pps)` = 'NIC (pps)',
      `Memory (W)` = 'Memory (W)',
      `CameraModel (W)` = 'Camera (W)',
      `ens2 (W)` = 'WiFi (W)',
      `ens2 Utilization (pps)` = 'WiFi (pps)',
      `CPUMaxIdleModel (W)` = 'CPU (W)',
      `CPUMaxIdleModel Utilization (%)` = 'CPU (%)'
    )
  } else {
    variable_labels <- c(
      `intel-rapl:0 (W)` = 'CPU (W)',
      `intel-rapl:0 Utilization (%)` = 'CPU (%)',
      `intel-rapl:0:0 (W)` = 'Memory Socket 0 (W)',
      `intel-rapl:1:0 (W)` = 'Memory Socket 1 (W)',
      `eno1 (W)` = 'NIC (W)',
      `eno1 Utilization (pps)` = 'NIC (pps)',
      `Memory (W)` = 'Memory (W)',
      `CameraModel (W)` = 'Camera (W)',
      `ens2 (W)` = 'NIC (W)',
      `ens2 Utilization (pps)` = 'NIC (Mbps)',
      `CPUMaxIdleModel (W)` = 'CPU (W)',
      `CPUMaxIdleModel Utilization (%)` = 'CPU (%)'
    )
  }

  melted_data$variable <- factor(melted_data$variable, levels = names(variable_labels), labels = variable_labels)

  return(melted_data)
}

endpoint_data <- process_data('endpoint.csv')
cloud_data <- process_data('cloud.csv')

plot_data <- function(data, title) {
  custom_colors <- c(
    'NIC (W)' = '#1f77b4',
    'NIC (pps)' = '#ff7f0e',
    'Memory (W)' = '#2ca02c',
    'Camera (W)' = '#d62728',
    'WiFi (W)' = '#1f77b4',
    'WiFi (pps)' = '#ff7f0e',
    'CPU (W)' = '#e377c2',
    'CPU (%)' = '#7f7f7f'
  )
  return (ggplot(data, aes(x = Timestamp, y = value, color = variable)) +
    geom_line(size=2) +
    scale_color_manual(values = custom_colors) +
    scale_x_continuous(labels = comma) +
    scale_y_log10(labels = scales::trans_format("log10", scales::math_format(10^.x)), limits = c(10^-4, 10^4)) +
    labs(title = title, x = 'Time (seconds)', y = '') +
    theme_minimal() +
    theme(axis.text = element_text(size = 42),
          axis.title.y.left = element_text(margin = margin(0, 10, 0, 0)),
          axis.title.y.right = element_text(margin = margin(0, 0, 0, 30)),
          axis.title.x.bottom = element_text(margin = margin(10, 0, 0, 0)),
          axis.title = element_text(size = 44),
          plot.title = element_text(size = 44),
          axis.line = element_line(color= "gray"),
          panel.grid.major = element_line(color = "gray", linewidth = 0.25, linetype = 1),
          panel.grid.minor = element_line(color = "gray", linewidth = 0.5, linetype = 2),
          panel.background = element_rect(fill = "white"),
          plot.margin = grid::unit(c(10, 0, 0, 0), "mm"),
          #legend.justification = c(1, 0.85),
          legend.position = "bottom",
          legend.text = element_text(size = 40),
          legend.title = element_blank()) +
      guides(color = guide_legend(override.aes = list(linewidth = 12), nrow=2)))
}

endpoint_plot <- plot_data(endpoint_data, '')
cloud_plot <- plot_data(cloud_data, '')

ggsave(file="cloud.pdf", plot = cloud_plot, width = 15, height = 9)
ggsave(file="endpoint.pdf", plot = endpoint_plot, width = 15, height = 9)

print(cloud_plot)
