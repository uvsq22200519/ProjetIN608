# plot pour voir évolution de la modularite avec une courbe par lignes executées
df <- read.delim("evolution_modularite.txt", header = FALSE, sep = "\t", skip = 1, fill = TRUE)
x <- 1:ncol(df)

plot(x, xlim = c(1, ncol(df)), ylim = c(0.32,0.57),
     xlab = "Générations", ylab = "Valeurs de la modularité", main = "Évolution de la modularité")

colors <- rainbow(nrow(df))
for (i in 1:nrow(df)) {
  y <- as.numeric(df[i, ])
  lines(x, y, col = colors[i])
}

#boxplot pour voir la moyenne de la modularité par génération
library(tidyverse)

df <- read.delim("evolution_modularite.txt", header = FALSE, sep = "\t", skip = 1, fill = TRUE)
df_clean <- na.omit(df)
df_clean <- df_clean[, 1:200]
colnames(df_clean) <- paste0("Gen", 1:ncol(df_clean))


df_long <- df_clean %>%
  pivot_longer(cols = everything(), names_to = "Generation", values_to = "Value") %>%
  mutate(
    GenNum = as.numeric(gsub("Gen", "", Generation)),
    FacetGroup = ceiling(GenNum / 8)
  )


df_long <- df_long %>%
  mutate(GenLabel = factor(GenNum, levels = sort(unique(GenNum))))


ggplot(df_long, aes(x = GenLabel, y = Value)) +
  geom_boxplot(outlier.colour = "red",alpha = 5, outlier.size = 1.3) +
  facet_wrap(~FacetGroup, scales = "free_x", ncol = 5) +
  labs(x = "Génération", y = "Valeurs de la modularité", title = "Evolution de la modularité") +
  theme_minimal() +
  theme(strip.background = element_rect(fill = "grey20"),
        strip.text = element_text(color = "white"),
        panel.background = element_rect(fill = "black",size = 1, linetype = "solid"),
        plot.background = element_rect(fill = "black"),
        plot.title = element_text(color = "white",hjust = 0.5, size=14, face="bold"),
        axis.text = element_text(color = "white", size = 6),
        axis.title = element_text(color = "white"),
        panel.grid = element_line(color = "grey30"))