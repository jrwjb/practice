options(warn =-1)
if (!require("pacman")){
  install.packages("pacman",dep=TRUE, repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')
  if(!require("pacman")){
  stop("安装失败")
  }
}

p_load(dplyr, foreach, doSNOW, xml2, openxlsx, doParallel)

# suppressMessages(library(dplyr))
# suppressMessages(library(foreach))
# suppressMessages(library(doSNOW))
# # library(XML)
# library(xml2)
# library(openxlsx)
# suppressMessages(library(doParallel))

args <- commandArgs(T)
path <- as.character(args[1])
thread <- as.numeric(args[2])
setwd(path)


################# FUNCTION ######################
# proid <- "aaabbb"
# proid <- "A0A0G2JGX4"
# proid <- "A0A087WUF0"

# library(RCurl)
# library(xml2)
# library(dplyr)

get_info <- function(proid){
  library(xml2)
  library(dplyr)
  name <- paste0("http://www.uniprot.org/uniprot/", proid, ".xml")
  # result <- try(xmlTreeParse(name, useInternalNodes = TRUE), silent = T)
  result <- try(read_xml(name), silent = T)
  
  # res <- as_list(result)
  
  error <- 1
  if (!class(result)[1] == "xml_document"){
    while(any(class(result) == "try-error"& error == 1)){
      cat(paste0("The error protein ID is ", proid, ". If this error happens again, please check your network or protein ID !!!\n"))
      if (grepl("Failed to parse text", result[1])){
        error <- 0
      }else{
        result <- try(read_xml(name), silent = T)
      }
    }
  }
  
  if (any(class(result) == "try-error")){
    out <- c(ProteinID = proid, ProteinName = "-", BP = "-", MF = "-", CC = "-", GO_Term = "-")
  }else{
    # goid <- xpathSApply(result, "//g:dbReference[@type='GO']", xmlGetAttr, "id", namespaces = "g")
    # tmp <- xpathSApply(result, "//j:property [@type='term']", xmlGetAttr, "value", namespaces = "j")
    # category <- unlist(lapply(tmp, function(x){strsplit(x, ":")[[1]][1]}))
    # goterm <- unlist(lapply(tmp, function(x){strsplit(x, ":")[[1]][2]}))
    # proname <- xpathSApply(result, "//j:fullName", fun = xmlValue, namespaces = "j")[1]
    
    goid <- xml_find_all(result, ".//d1:dbReference[@type='GO']", ns = xml_ns(result)) %>% xml_attr("id")
    tmp <- xml_find_all(result, ".//d1:property[@type='term']", ns = xml_ns(result)) %>% xml_attr("value")
    category <- unlist(lapply(tmp, function(x){strsplit(x, ":")[[1]][1]}))
    goterm <- unlist(lapply(tmp, function(x){strsplit(x, ":")[[1]][2]}))
    proname <- xml_find_all(result, ".//d1:fullName", ns = xml_ns(result)) %>% xml_text() %>% head(1)
    
    if ("P" %in% category){
      bp <- paste0(paste(goterm[which(category == "P")], paste0("[", goid[which(category == "P")], "]")), collapse = ";")
    }else{
      bp <- "-"
    }
    
    if ("F" %in% category){
      mf <- paste0(paste(goterm[which(category == "F")], paste0("[", goid[which(category == "F")], "]")), collapse = ";")
    }else{
      mf <- "-"
    }
    
    if ("C" %in% category){
      cc <- paste0(paste(goterm[which(category == "C")], paste0("[", goid[which(category == "C")], "]")), collapse = ";")
    }else{
      cc <- "-"
    }
    
    all_go <- paste(c(bp[!is.na(bp)], mf[!is.na(mf)], cc[!is.na(cc)]), collapse = ";")
    
    if (length(goid) == 0){
      out <- c(ProteinID = proid, ProteinName = proname, BP = "-", MF = "-", CC = "-", GO_Term = "-")
    }else{
      out <- c(ProteinID = proid, ProteinName = proname, BP = bp, MF = mf, CC = cc, GO_Term = all_go)
    }
  }
  return(out)
}


dirs <- dir()
dirs <- dirs[!grepl("\\.", dirs)]

wb <- createWorkbook()
modifyBaseFont(wb, fontName = "Arial", fontSize = 10)

project_number <- 1

for(i in dirs){
  folder <- i
  file <- paste0(folder, "/diff_list.txt")
  
  uniprot_id <- read.table(file = file, header = F, stringsAsFactors = F) %>% as.matrix() %>% as.character()
  # 
  cl.cores <- detectCores()
  if (is.na(thread)){
    core <- 10
  }else{
    core <- thread
  }
  
  #  core <- 10
  cl <- makeCluster(core)
  registerDoSNOW(cl)
  pb <- txtProgressBar(min = 0, max = length(uniprot_id), style = 3)
  progress <- function(n) setTxtProgressBar(pb, n)
  opts <- list(progress = progress)
  
  system.time({
    result_df <- foreach(i = 1:length(uniprot_id), .combine = rbind, .options.snow = opts) %dopar% {
      df <- get_info(proid = uniprot_id[i])
      
      Sys.sleep(0.2)
      return(df)
    }
    close(pb)
    stopCluster(cl)
  })
  
  # for(i in 1:length(uniprot_id)){
  #   df <- get_info(proid = uniprot_id[i])
  #   result_df <- rbind(result_df, df)
  #   
  #   Sys.sleep(0.5)
  #   setTxtProgressBar(pb, i)
  # }
  
  print(paste0("The processs of ", i, " is finished !!!"))
  
  addWorksheet(wb, sheetName = folder)
  header_style <- createStyle(textDecoration = "bold", halign = "left")
  addStyle(wb, sheet = folder, rows = 1, cols = 1:ncol(result_df), style = header_style)
  
  setColWidths(wb, sheet = folder, cols = 2, widths = 15)
  writeData(wb, sheet = folder, x = result_df)
}

saveWorkbook(wb, "GO.xlsx", overwrite = T)


