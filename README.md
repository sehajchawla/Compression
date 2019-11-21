# Compression

This repository has my implementation of compression schemes I learnt during the Information Theory module of my engineering course at Cambridge.

The file titled 'vl_codes' has the implementation of Shanon Fano and Huffman coding. It also calculates the entropy levels achieved and is decriptive in suggesting that Shanon Fano is largely an academic coding method, rather than a practical one. This is because, the entropy level achieved is not close to optimal. Huffman coding, on the other hand, works well to correct errors and gets close to ideal entropy, however it gets very complicated for multiple symbols.

The file titled 'arithmetic' has the arithmetic coding implementation and is illustrative in showing us that although arithmetic is extremely practical, and very close to ideal entropy, it is very bad with error handling.

To demonstrate the working of the algorithms, hamlet.txt (a complete copy of Shakespeare's Hamlet) is used. Hamlet.txt.czs is the shannon-fano encoded file, Hamlet.txt.czh is huffman encoded, and Hamlet.txt.cza is arithmetic encoded. 

The decoded and recovered file is titled Hamlet.txt.cuz.
