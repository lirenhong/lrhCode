cat words.txt |tr -s ' ' '\n'|sort |uniq -c|awk '{print $2 " " $1}'

awk '{i=1;while(i<=NF){print $i;i++}}' words.txt |sort|uniq -c|sort -k1nr|awk '{print $2 " " $1}'
