#!/bin/sh
awk '
{
    for(i=1; i<=NF; i++){
        a[NR, i] = $i
    }
}
END{
    for(j=1; j<=NF; j++){
        str=a[1,j]
        for(i=2; i<=NR; i++){
            str = str" "a[i,j]
        }
        print str
    }
}
' file.txt
