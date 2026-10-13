for mode in r r+ w w+ a a+; do
    printf OLD > sample.txt
    ./mode_probe "$mode" sample.txt
done
