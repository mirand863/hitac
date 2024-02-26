#!/usr/bin/env Rscript

library(tidyverse)
library(optparse)

option_list <- list(
  make_option(c("-i", "--input"), type="character", default=NULL, help="input file name", metavar="character"),
  make_option(c("-p", "--path"), type="character", default=NULL, help="output path", metavar="character"),
  make_option(c("-f", "--file"), type="character", default=NULL, help="output file name", metavar="character")
);

opt_parser <- OptionParser(option_list=option_list);
opt <- parse_args(opt_parser);

data <- read.csv(opt$input, header=T, sep=",")

# Set a number of 'empty bar' to add at the end of each group
empty_bar <- 3
to_add <- data.frame( matrix(NA, empty_bar*nlevels(data$Group), ncol(data)) )
colnames(to_add) <- colnames(data)
to_add$Group <- rep(levels(data$Group), each=empty_bar)
data <- rbind(data, to_add)
data <- data %>% arrange(Group)
data$id <- seq(1, nrow(data))

# Get the name and the y position of each label
label_data <- data
number_of_bar <- nrow(label_data)
angle <- 90 - 360 * (label_data$id-0.5) /number_of_bar     # I substract 0.5 because the letter must have the angle of the center of the bars. Not extreme right(1) or extreme left (0)
label_data$hjust <- ifelse( angle < -90, 1, 0)
label_data$angle <- ifelse(angle < -90, angle+180, angle)
label_data$tpr_text_length <- nchar(as.character(label_data$TPR))
label_data$tpr_text_position <- label_data$TPR - 5 - label_data$tpr_text_length * 2
label_data$tpr_text <- ifelse(label_data$TPR > 11, label_data$TPR, "")

# prepare a data frame for base lines
base_data <- data %>%
  group_by(Group) %>%
  summarize(start=min(id) - 0.2, end=max(id)) %>%
  rowwise() %>%
  mutate(title=mean(c(start, end)))

# prepare a data frame for grid (scales)
grid_data <- base_data
grid_data$end <- grid_data$end[ c( nrow(grid_data), 1:nrow(grid_data)-1)] + 1
grid_data$start <- grid_data$start - 1
grid_data <- grid_data[-1,]

# Make the plot
p <- ggplot(data, aes(x=as.factor(id), y=TPR, fill=Group)) +       # Note that id is a factor. If x is numeric, there is some space between the first bar

  scale_fill_manual(values=c("#001219", "#005F73", "#EE9B00", "#CA6702", "#9B2226")) +

  geom_bar(aes(x=as.factor(id), y=TPR, fill=Group), stat="identity", alpha=1) +

  geom_bar(aes(x=as.factor(id), y=TPR, fill=Group), stat="identity", alpha=1) +
  ylim(-100,120) +
  theme_minimal() +
  theme(
    legend.position = "none",
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid = element_blank(),
    plot.margin = unit(rep(-1,4), "cm")
  ) +
  coord_polar() +
  geom_text(data=label_data, aes(x=id, y=TPR+1, label=Method, hjust=hjust), color="black", fontface="plain",alpha=1, size=2.5, angle= label_data$angle, inherit.aes = FALSE ) +
  geom_text(data=label_data, aes(x=id, y=tpr_text_position, label=tpr_text, hjust=hjust), color="white", fontface="plain",alpha=1, size=2.5, angle= label_data$angle, inherit.aes = FALSE ) +

  # Add base line information
  geom_segment(data=base_data, aes(x = start, y = -5, xend = end, yend = -5), colour = "black", alpha=1, size=0.6 , inherit.aes = FALSE )  +
  geom_text(data=base_data, aes(x = title, y = -18, label=Group), hjust=c(1,1,0,0,0), colour = "black", alpha=1, size=4, fontface="bold", inherit.aes = FALSE)

ggsave(
  opt$file,
  plot = last_plot(),
  device = "pdf",
  path = opt$path,
  scale = 1,
  width = 21,
  height = 29.7,
  units = "cm",
  dpi = 600,
  limitsize = FALSE,
  bg = NULL
)
