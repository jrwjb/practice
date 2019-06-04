library(vegan)
library(RColorBrewer)

args <- commandArgs(T)
inpath <- as.character(args[1])
outpath <- as.character(args[2])

sample_info <- read.table(paste0(inpath, '/sample_info.txt'), row.names = 1, header = T, sep = '\t')
# otu_table <- read.table(paste0(inpath, '/01.OTU_Taxa/normalize/otu_table.xls'), row.names = 1, header = T, sep = '\t')
# otu_table <- otu_table[, rownames(sample_info)]


#####多组一起比较
## anosim
dm_unweight <- read.table(paste0(inpath, '/04.Beta/beta_diversity/unweighted_unifrac_otu_table.txt'), row.names = 1, header = T, sep = '\t')
dm_weight <- read.table(paste0(inpath, '/04.Beta/beta_diversity/weighted_unifrac_otu_table.txt'), row.names = 1, header = T, sep = '\t')
dm_bray <- read.table(paste0(inpath, '/04.Beta/beta_diversity/bray_curtis_otu_table.txt'), row.names = 1, header = T, sep = '\t')

# dm_bray <- vegdist(t(otu_table), method = 'bray')


dir.create(paste0(outpath, '/anosim'))

anosim_func <- function(dm, index){
  dir.create(paste0(outpath, '/anosim/', index))
  groupvs <- paste(unique(sample_info$Group), collapse = '_vs_')
  anosim <- anosim(dm, sample_info$Group, permutations = 999)
  group_num <- length(unique(sample_info$Group))
  cols <- brewer.pal(n=group_num + 1, name="Set1")
  R <- anosim$statistic
  p_value <- anosim$signif
  anosim_result <- data.frame(groupvs, R, p_value)
  write.table(anosim_result, paste0(outpath, '/anosim/', index, '/anosim_results.txt'), sep = '\t', row.names = F)
  png(filename = paste0(outpath, '/anosim/', index, '/anosim_results.png'), width = 26, height = 22, units = "cm", res = 300)
  plot(anosim, col=cols)
  dev.off()
  #pdf
  pdf(paste0(outpath, '/anosim/', index, '/anosim_results.pdf'))
  plot(anosim, col=cols)
  dev.off()
}

anosim_func(dm_bray, 'bray_curtis')
anosim_func(dm_weight, 'weighted_unifrac')
anosim_func(dm_unweight, 'unweighted_unifrac')

rm(list = ls())




