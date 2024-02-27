library(ggplot2)
library(ggpubr)
library(ggrepel)
library(optparse)

option_list <- list(
  make_option(c("-i", "--input"), type="character", default=NULL, help="input file name", metavar="character"),
  make_option(c("-p", "--path"), type="character", default=NULL, help="output path", metavar="character"),
  make_option(c("-d", "--dataset"), type="character", default=NULL, help="output file name", metavar="character")
);

opt_parser <- OptionParser(option_list=option_list);
opt <- parse_args(opt_parser);

datasets <- c(
  "sp_rdp_its.90" = "SP RDP ITS 90",
  "sp_rdp_its.95" = "SP RDP ITS 95",
  "sp_rdp_its.97" = "SP RDP ITS 97",
  "sp_rdp_its.99" = "SP RDP ITS 99",
  "sp_rdp_its.100" = "SP RDP ITS 100"
)

ranks <- c(
  "sp_rdp_its.90" = "genus",
  "sp_rdp_its.95" = "genus",
  "sp_rdp_its.97" = "genus",
  "sp_rdp_its.99" = "species",
  "sp_rdp_its.100" = "species"
)

theme_set(
  theme_pubr()
)

data <- read.csv(opt$input, header=T, sep=",")

shapes <- rep(15:18, 6)

colors <- rep(
  c(
    "#E9D8A6",
    "#EE9B00",
    "#CA6702",
    "#BB3E03",
    "#AE2012",
    "#9B2226",
    "#0A9396",
    "#001219",
    "#005F73",
    "#0A9396",
    "#94D2BD"
  ), 2)

plot <- ggplot(data, aes(x = UCR, y = OCR, group = Method, size = 9)) +
  geom_abline(intercept =0 , slope = 1) +
  geom_point(aes(shape = Method, color = Method), show.legend=FALSE) +
  scale_shape_manual(values = shapes) +
  scale_color_manual(values = colors) +
  scale_size(guide = "none") +
  geom_label_repel(
    aes(label = Method, color=Method), size = 3, show.legend=FALSE
  ) +
  xlab("Under-classification rate") +
  scale_x_continuous(limits = c(0, 100), breaks = c(0, 25, 50, 75, 100), label = c("0%", "25%", "50%", "75%", "100%")) +
  ylab("Over-classification rate") +
  scale_y_continuous(limits = c(0, 100), breaks = c(0, 25, 50, 75, 100), label = c("0%", "25%", "50%", "75%", "100%")) +
  guides(fill = "none") +
  ggtitle("Under-classification vs. over-classification rates", subtitle = paste(datasets[opt$dataset], "at", ranks[opt$dataset], "level")) +
  theme(plot.title = element_text(hjust = 0.5, face = "bold")) +
  theme(plot.subtitle = element_text(hjust = 0.5, face = "bold"))

plot + theme(
  panel.grid.major = element_line(colour = "gray", size = 0.2),
  panel.grid.minor = element_line(colour = "gray", size = 0.2)
)

ggsave(
  paste(opt$dataset, ".pdf", sep=""),
  plot = last_plot(),
  device = "pdf",
  path = opt$path,
  scale = 1,
  width = NA,
  height = NA,
  units = c("in", "cm", "mm", "px"),
  dpi = 300,
  limitsize = TRUE,
  bg = NULL
)
