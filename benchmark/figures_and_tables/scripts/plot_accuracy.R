library(ggpubr)
library(optparse)

option_list <- list(
  make_option(c("-i", "--input"), type="character", default=NULL, help="input file name", metavar="character"),
  make_option(c("-p", "--path"), type="character", default=NULL, help="output path", metavar="character"),
  make_option(c("-f", "--file"), type="character", default=NULL, help="output file name", metavar="character")
);

opt_parser <- OptionParser(option_list=option_list);
opt <- parse_args(opt_parser);

data <- read.csv(opt$input, header=T, sep=",")

ggdotchart(data, x = "Method", y = "Acc",
           color = "Group",                              # Color by groups
           palette = c("#001219", "#005F73", "#EE9B00", "#CA6702", "#9B2226"), # Custom color palette
           sorting = "descending",                       # Sort value in descending order
           add = "segments",                             # Add segments from y = 0 to dots
           rotate = TRUE,                                # Rotate vertically
           group = "Group",                              # Order by groups
           dot.size = 6.5,                               # Large dot size
           label = data$Acc,                             # Add mpg values as dot labels
           font.label = list(color = "white", size = 7,
                             vjust = 0.5),               # Adjust label parameters
           # ggplot2 theme
           ggtheme = theme_pubr(
             base_family = "Helvetica"
           )
) +
  labs(y = "Accuracy", x = "", color="") +
  ggtitle("Highest accuracies") +
  theme(plot.title = element_text(hjust = 0.5, face = "bold")) +
  scale_y_continuous(labels = c("0" = "0%", "25" = "25%", "50" = "50%", "75" = "75%", "100" = "100%")) +
  scale_x_discrete(
    labels = rev(data$Label)
  )

print(data$Label)

ggsave(
  opt$file,
  plot = last_plot(),
  device = "pdf",
  path = opt$path,
  scale = 1,
  width = NA,
  height = NA,
  units = c("in", "cm", "mm", "px"),
  dpi = 600,
  limitsize = TRUE,
  bg = NULL
)
