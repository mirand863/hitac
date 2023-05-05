# library(ggpubr)
# # Load data
# data("ToothGrowth")
# df <- ToothGrowth
# head(df, 4)
# #>    len supp dose
# #> 1  4.2   VC  0.5
# #> 2 11.5   VC  0.5
# #> 3  7.3   VC  0.5
# #> 4  5.8   VC  0.5
#
# # Box plots with jittered points
# # :::::::::::::::::::::::::::::::::::::::::::::::::::
# # Change outline colors by groups: dose
# # Use custom color palette
# # Add jitter points and change the shape by groups
# p <- ggboxplot(df, x = "dose", y = "len",
#                color = "dose", palette =c("#00AFBB", "#E7B800", "#FC4E07"),
#                add = "jitter", shape = "dose")
# p

# https://z3tt.github.io/beyond-bar-and-box-plots/
library(tidyverse)     ## data wrangling + ggplot2
library(colorspace)    ## adjust colors
library(rcartocolor)   ## Carto palettes
library(ggforce)       ## sina plots
library(ggdist)        ## halfeye plots
library(ggridges)      ## ridgeline plots
library(ggbeeswarm)    ## beeswarm plots
library(gghalves)      ## off-set jitter
library(systemfonts)   ## custom fonts
library(extrafont)

# url <- "https://raw.githubusercontent.com/z3tt/DataViz-Teaching/master/data/weissgerber-data.csv"
# data <- read_csv(url)

data <- read_csv("results/images/sp_rdp_its_sensitivity.csv")
data$group <- factor(data$group, c("HiTaC", "BTOP", "TOP", "Microclass", "KTOP", "HiTaC_Filter", "SINTAX50", "SPINGO"))

# font_import(paths = "/usr/share/fonts/TTF/", prompt=FALSE)

## general theme
theme_set(theme_void(base_family = "Roboto"))

theme_update(
  axis.text.x = element_text(color = "black", face = "bold", size = 26,
                             margin = margin(t = 6), angle = 60, vjust = 1, hjust = 1),
  axis.text.y = element_text(color = "black", size = 22, hjust = 1,
                             margin = margin(r = 6), family = "Roboto Mono"),
  axis.line.x = element_line(color = "black", size = 1),
  panel.grid.major.y = element_line(color = "grey90", size = .6),
  plot.background = element_rect(fill = "white", color = "white"),
  plot.margin = margin(rep(20, 4))
)

## theme for horizontal charts
theme_flip <-
  theme(
    axis.text.x = element_text(face = "plain", family = "Roboto Mono", size = 22),
    axis.text.y = element_text(face = "bold", family = "Roboto", size = 26),
    panel.grid.major.x = element_line(color = "grey90", size = .6),
    panel.grid.major.y = element_blank(),
    legend.position = "top",
    legend.text = element_text(family = "Roboto Mono", size = 18),
    legend.title = element_text(face = "bold", size = 18, margin = margin(b = 25))
  )

## custom colors
# my_pal <- rcartocolor::carto_pal(n = 8, name = "Bold")[c(1, 3, 7, 2)]
my_pal <- rcartocolor::carto_pal(n = 8, name = "Bold")[c(1, 2, 3, 4, 5, 6, 7, 8)]


# barplot
# ggplot(data, aes(x = group, y = value, fill = group)) +
#   geom_bar(stat = "summary", width = .8) +
#   scale_y_continuous(expand = c(0, 0), breaks = 0:4) +
#   scale_fill_manual(values = my_pal, guide = "none")

# ggplot(data, aes(x = group, fill = group)) +
#   geom_bar(width = .8) +
#   scale_y_continuous(expand = c(0, 0)) +
#   scale_fill_manual(values = my_pal, guide = "none")

# dynamite plot
# ggplot(data, aes(x = group, y = value, color = group, fill = group)) +
#   stat_summary(
#     geom = "errorbar",
#     fun.max = function(x) mean(x) + sd(x),
#     fun.min = function(x) mean(x) - sd(x),
#     width = .3, size = 1.2
#   ) +
#   geom_bar(stat = "summary", width = .8, size = .8) +
#   scale_y_continuous(expand = c(0, 0), breaks = 1:9) +
#   scale_fill_manual(values = my_pal, guide = "none") +
#   scale_color_manual(values = my_pal, guide = "none")

# boxplot
g <- ggplot(data, aes(x = group, y = value, color = group, fill = group)) +
  scale_y_continuous(breaks = seq(50,100,25)) +
  scale_color_manual(values = my_pal, guide = "none") +
  scale_fill_manual(values = my_pal, guide = "none")

g +
  geom_boxplot(
    aes(fill = group, fill = after_scale(colorspace::lighten(fill, .7))),
    size = 1.5, outlier.shape = NA
  ) +
  geom_jitter(width = .1, size = 7, alpha = .5)
