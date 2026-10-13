for mode in r+ w+ a+; do
    printf OLD > sample.txt
    ./mode_probe "$mode" sample.txt X
    cat sample.txt
    printf '\n'
done
