# test scrpt
args <- commandArgs(trailingOnly = TRUE)
library(tidyverse)
library(coda)

growth <- read_rds("growth.rds")

taxa <-  c('B_caccae',
           'B_cellulosilyticus_WH2',
           'B_ovatus',
           'B_thetaiotaomicron',
           'B_uniformis',
           'B_vulgatus',
           'C_aerofaciens',
           'C_scindens',
           'C_spiroforme',
           'D_longicatena',
           'P_distasonis',
           'R_obeum')

sopa <- cbind(growth[1, 1:24000, 1],  growth[1, 1:24000, 2], growth[1, 1:24000, 3], growth[1, 1:24000, 4], growth[1, 1:24000, 5], growth[1, 1:24000, 6], growth[1, 1:24000, 7], growth[1, 1:24000, 8], growth[1, 1:24000, 9], growth[1, 1:24000, 10], growth[1, 1:24000, 11], growth[1, 1:24000, 12])
colnames(sopa) <- taxa
lima <- cbind(growth[2, 1:24000, 1],  growth[2, 1:24000, 2], growth[2, 1:24000, 3], growth[2, 1:24000, 4], growth[2, 1:24000, 5], growth[2, 1:24000, 6], growth[2, 1:24000, 7], growth[2, 1:24000, 8], growth[2, 1:24000, 9], growth[2, 1:24000, 10], growth[2, 1:24000, 11], growth[2, 1:24000, 12])
colnames(lima) <- taxa

yuca <- mcmc(data = sopa)

pera <- mcmc(data = lima)

chipi <- mcmc.list(yuca, pera)

# gelman.plot(chipi, autoburnin = FALSE)
gelman.diag(chipi)
heidel.diag(yuca)
geweke.diag(yuca)

gelman.plot(chipi)