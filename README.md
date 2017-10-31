<b>K Bowser</b>

<b>CPSC 353-01 Fall 2017</b>
 
<b>Summoner name == pashmak</b>

<b>Python 3.4.3</b>



<b>----------Brief description of application architecture----------</b>

Important notes: 
-Application is not currently optimized. 
-Use an input .jpeg with dimensions less than or equal to 1000x1000.

Application uses Python's Pillow (documentation @ https://pillow.readthedocs.io/en/latest/reference/index.html)
as well as argparse (documentation @ https://docs.python.org/3/library/argparse.html).

The input image used to encode a message should be a .jpeg image, and the application will export a .png image that is imbedded with the message bit length and message. 
The message bit length and message are stored inside inside each RGB value of each pixel in the least significant bit of the RGB values. 
The application uses the first 11 pixels on the bottom right corner of the image to embed the message length. 
The message itself is embedded in each pixel after the message length, from the bottom right to the top left.



<b>----------Instructions on how to execute application----------</b>

1. Download textInImage.py and save it in desired location, for example in C:\Python34

2. Open command prompt and use as outlined below:

<b>-Encode text from a file into a .jpeg image (exports encoded .png image):</b>

C:\Python34\python.exe C:\Python34\textInImage.py -opt encode -inputImg C:\Python34\input_image.jpg -inputFile C:\Python34\input_file.txt -outputImg C:\Python34\encoded_image.png

<b>-Encode text from command prompt into a .jpeg image (exports encoded .png image):</b>

C:\Python34\python.exe C:\Python34\textInImage.py -opt encode -inputImg C:\Python34\input_image.jpg -txt "security is fun" -outputImg C:\Python34\encoded_image.png

<b>-Decode a .png image, print to console + file:</b>

C:\Python34\python.exe C:\Python34\textInImage.py -opt decode -inputImg C:\Python34\encoded_image.png -outputFile C:\Python34\decoded_message.txt

<b>-Decode a .png image, print to console only:</b>

C:\Python34\python.exe C:\Python34\textInImage.py -opt decode -inputImg C:\Python34\encoded_image.png
