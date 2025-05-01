# ÉVOLUTION MODULARITÉ AVEC PROBA À 0.1
# plot pour voir évolution de la modularite avec une courbe par lignes executées
df <- read.delim("evolution_modularite.txt", header = FALSE, sep = "\t", skip = 1, fill = TRUE)
x <- 1:ncol(df)
png("evolution_modularite_P0.1.png", width = 800, height = 600, bg = "white")
plot(x, xlim = c(1, ncol(df)), ylim = c(0.32,0.57),
     xlab = "Génération", ylab = "Valeurs de la modularité",cex.lab=1.4)

colors <- rainbow(nrow(df))
for (i in 1:nrow(df)) {
  y <- as.numeric(df[i, ])
  lines(x, y, col = colors[i])
}

title(main = "Évolution de la modularité", cex.main = 2, font.main= 2)
dev.off()

#boxplot pour voir la moyenne de la modularité par génération
library(tidyverse)

df <- read.delim("evolution_modularite.txt", header = FALSE, sep = "\t", skip = 1, fill = TRUE)
df_clean <- na.omit(df)
df_clean <- df_clean[, 1:200]
colnames(df_clean) <- paste0("Gen", 1:ncol(df_clean))

png("evolution_modularite_grilles_P0.1.png", width = 800, height = 600, bg = "white")
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
  theme(
  strip.background = element_rect(fill = "white"),
  strip.text = element_text(color = "black"),
  panel.background = element_rect(fill = "white", size = 1, linetype = "solid"),
  plot.background = element_rect(fill = "white"),
  plot.title = element_text(color = "black", hjust = 0.5, size = 14, face = "bold"),
  axis.text = element_text(color = "black", size = 6),
  axis.title = element_text(color = "black"),
  panel.grid = element_line(color = "grey70")
)

dev.off()

#ÉVOLUTION MODULARITÉ AVEC VARIATION PROBA
#boxplot qui visualise l'évolution de la modularité en variant proba
png("evolution_modularite_proba_variation.png", width = 800, height = 600, bg = "white")
probas <- scan("probas_variation_main", nlines = 1)
ds <- read.table("probas_variation_main", skip = 1)
boxplot(ds, names = probas, main = "Évolution modularité", xlab = "Variation probabilité", ylab = "Modularité", col = "lightblue",outcol="red", cex.main = 1.7,font.main = 2 )
dev.off()

#ÉVOLUTION F-SCORE AVEC VARIATION PROBA INIT
#proba init variation
png("évolution F score sans bruitage à P init ω = 2.png", width = 800, height = 600, bg = "white")
probas <- scan("f_score_données_graphe", nlines = 1)
ds <- read.table("f_score_données_graphe", skip = 1)
boxplot(ds, names = probas, main = "Évolution F score à P init = 0 et ω = 2", xlab = "Variation probabilité P clean", ylab = "F-score", col = "lightblue",outcol="red", cex.main = 1.2,font.main = 2 )
dev.off()
