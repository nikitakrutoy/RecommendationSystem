# Desciption
Recomendation system for https://vc.ru.  
System could crawl, parse and save posts.  
Uses logistic regression model(SGD) to find intersting posts.  

## Crawler
Has a command line interface
Available commands:

  update [--from][--to][--print] Refresh list of pages to download  
  --from - sets from date  
  --to - sets for date  
  --print - prints new posts links  
  download [-all][url..] download pages  
  -all - download all pages  
  urls.. - download pages with specified urls  
  clean - Parses html pages  

## Classifier
ROC-AUC Score on ~200 samples: 0.78  
Article classification/marker.py - GUI for marking news posts
