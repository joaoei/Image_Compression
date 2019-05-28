# Image_Compression
Encoder/decoder for image compression. A program encodes the image, resulting in a compressed image file. The program that decodes writes to another file in a known extension.

## Description
The methods used for image compression were the Discrete Cosine Transform (DCT) with quantization, and Run-length encoding (RLE) to encode the file.

## How to run
To run Image_Compression use:
```
python3 main.py [-e (for encode) | -d (for decode)] -i <inputfile> -o <outputpath>
```
## Features:
* [x] DCT 
* [x] QUANTIZATION
* [x] RLE
* [] ZIGZAG
* [] HUFFMAN

## References
- [http://computacaografica.ic.uff.br/transparenciasvol2cap8.pdf](http://computacaografica.ic.uff.br/transparenciasvol2cap8.pdf)
- [https://www.youtube.com/watch?v=sckLJpjH5p8](https://www.youtube.com/watch?v=sckLJpjH5p8)
- [https://github.com/amzhang1/simple-JPEG-compression](https://github.com/amzhang1/simple-JPEG-compression)
- [https://github.com/getsanjeev/compression-DCT](https://github.com/getsanjeev/compression-DCT)