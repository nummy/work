library(rvest)
library(tidyverse)
years <- c()
issues <- c()
titles <- c()
authors <- c()
for(year in 2015:2020){
  if(year==2020){
    arr <- 1:4
  }else{
    arr <- 1:6
  }
  for(issue in arr){
    url <- paste0("https://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=", year, "&issue=0", issue, "&pykm=LSYJ")
    page <- read_html(url)
    print(url)
    dd <- html_nodes(page, "dd")
    title <- dd %>% html_nodes("span.name") %>% html_nodes("a") %>% html_text() %>% trimws(whitespace = "[ \t\r\n;]")
    author <- dd %>% html_nodes("span.author") %>% html_text() %>% trimws(whitespace = "[ \t\r\n;]")
    years <- c(years, rep(year, length(title)))
    issues <- c(issues, rep(issue, length(title)))
    titles <- c(titles, title)
    authors <- c(authors, author)
  }
}
dat <- data.frame(title=titles, author=authors, year=years, issue=issues)
write.csv(dat, "data.csv", row.names = F)
