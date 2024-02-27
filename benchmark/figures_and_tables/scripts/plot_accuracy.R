library(ggpubr)

data <- read.csv("sensitivity.csv", header=T, sep=",")

ggdotchart(data, x = "Method", y = "TPR",
           color = "Group",                              # Color by groups
           palette = c("#001219", "#005F73", "#EE9B00", "#CA6702", "#9B2226"), # Custom color palette
           sorting = "descending",                       # Sort value in descending order
           add = "segments",                             # Add segments from y = 0 to dots
           rotate = TRUE,                                # Rotate vertically
           group = "Group",                              # Order by groups
           dot.size = 6.5,                               # Large dot size
           label = data$TPR,                             # Add mpg values as dot labels
           font.label = list(color = "white", size = 7,
                             vjust = 0.5),               # Adjust label parameters
           # ggplot2 theme
           ggtheme = theme_pubr(
             base_family = "Helvetica"
           )
) +
  labs(y = "True Positive Rate", x = "", color="") +
  ggtitle("Highest true positive rates") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold")) +
  scale_y_continuous(labels = c("0" = "0%", "25" = "25%", "50" = "50%", "75" = "75%", "100" = "100%"))
  # scale_x_discrete(
  #   labels = rev(data$Label)
  # )

ggsave(
  "tpr.pdf",
  plot = last_plot(),
  device = "pdf",
  path = "results/images",
  scale = 1,
  width = NA,
  height = NA,
  units = c("in", "cm", "mm", "px"),
  dpi = 600,
  limitsize = TRUE,
  bg = NULL
)
