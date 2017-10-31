#Karissa Bowser
#Summoner name == pashmak
#CS 353-01 Fall 2017 Project 1
#Python 3.4.3

from PIL import Image #Pillow documentation: https://pillow.readthedocs.io/en/latest/reference/index.html
import argparse #argparse documentation: https://docs.python.org/3/library/argparse.html

        
"Encode the image and export it as a .png (called by def main)" #encoding should be improved in a future version, currently it is *very* slow & inefficient
def encode_image(input_img_file, text_to_encode, encoded_img_file): 
    
    text_to_encode_len = len(text_to_encode) #Set text length
    binary_text_num_bits = convert_num_bits_to_binary(text_to_encode_len) #binary_text_num_bits = number of bits of text length in binary (reversed)
    text = convert_text_to_binary(text_to_encode_len, text_to_encode) #text = text_to_encode in binary (reversed)
    image_to_encode = Image.open(input_img_file) #Open and identify given file 
    image_to_encode = image_to_encode.rotate(180) #Rotate image upside down so we can just encode message starting from upper left corner of image
    img_pixels = list(image_to_encode.getdata()) #Convert .getdata() to ordinary sequence of pixels using list()
    text_length_encoded_pixels = encode_text_length(binary_text_num_bits, img_pixels) #text_length_encoded_pixels = pixels embedded with number of bits of text length 
    encoded_pixel_tuples = encode_text(text, img_pixels, text_length_encoded_pixels) #encoded_pixel_tuples = pixel tuples embedded with both the number of bits of text length + binary text
    image_to_encode.putdata(encoded_pixel_tuples) #Embed text into the image
    image_to_encode = image_to_encode.rotate(180) #Done with image, turn it back to original position
    image_to_encode.filename = encoded_img_file #Set filename according to args.output_img_filename
    image_to_encode.format_description = 'Portable network graphics' #Image will be exported as .png
    image_to_encode.save(encoded_img_file) #Save image as argument given for args.output_img_filename
    image_to_encode.close() #Close file pointer


"Convert the number of bits in text to binary (called by def encode_image)"
def convert_num_bits_to_binary(text_length):
    
    text_num_bits = text_length * 8 #Set text_num_bits to number of bits in the text that will be encoded (text_length * 8)
    binary_num_bits = bin(text_num_bits) #Set binary_num_bits = text_num_bits in binary
    binary_num_bits = binary_num_bits[2:] #Remove the 0b at start of string
    binary_num_bits = "".join(reversed(binary_num_bits)) #Reverse string
    return binary_num_bits


"Convert text to binary (called by def encode_image)"
def convert_text_to_binary(text_len, text): 
    
    binary_text = "" #Will contain binary version of text that we want to embed in image
    for i in range (0,text_len):
        char_to_encode = text[i] #char_to_encode = char in text[i]
        ascii_char = ord(char_to_encode) #Set ascii_char to integer value for each char (ie ord('a') returns the integer 97)
        binary_char = bin(ascii_char) #Set binary_char to the binary representation of each ascii_char 
        binary_char = binary_char[0:1] + binary_char[2:] #Remove the b from '0b' in the string (*leaves the 0, just removes the b)
        while (len(binary_char) < 8): 
            #Add a zero to binary_char (using slice that has the zero value [0:1] that we left in above to add a new zero in each loop)
            binary_char = binary_char[0:1] + binary_char 
        binary_text += binary_char #Add the binary char to the binary text
    binary_text = "".join(reversed(binary_text)) #Reverse string
    return binary_text


"Encode number of bits of text length in bottom right 11 pixels that will be put into image (called by def encode_image)"
def encode_text_length(binary_num_bits, img_data):
    
    #Embed encoded_pixels with binary_num_bits (the binary representation of the text length in number of bits of the text_to_encode)
    pixel_tuples = () #Will be used to hold img_pixel values  in for j loop below
    encoded_pixels = list() #Will contain pixel values which contain encoded message in the least significant bit
    binary_num_bits_len=len(binary_num_bits) #Set length of number of bits in binary text
    pixel_count = 0 #Used to keep track of current pixel number for if statement
    k = 1 #Used to decrement index of binary_message_num_bits in the following for j loop
    #We only want the 11 pixels in bottom right corner to write the message size, but imaged was rotated upside down, so start at i = 0
    for i in range(0,11,1): #get first 11 pixels (ie pixels 0-10)
        for j in range(0,3,1): #B, G, R
            pixel_tuples = img_data[i]
            if  pixel_count <= 32 and pixel_count >= (32-binary_num_bits_len): #encode the message size in the portion of pixels between 32-binary_message_num_bits_len and 32
                if binary_num_bits[binary_num_bits_len-k] == '0':
                    temp_pixels = list(pixel_tuples[j:j+1])
                    if img_data[i][j] % 2 != 0:  #if value is not even, subtract 1 to make even(if it is even lsb is already 0)
                        temp_pixels = [x-1 for x in temp_pixels]
                    encoded_pixels += temp_pixels
                if binary_num_bits[binary_num_bits_len-k] == '1':
                    temp_pixels = list(pixel_tuples[j:j+1])
                    if img_data[i][j] % 2 == 0:  #if value is even, add 1 to make odd (if it is odd lsb is already 1)
                        temp_pixels = [x+1 for x in temp_pixels]
                    encoded_pixels += temp_pixels
                k+=1
            else:
                temp_pixels = list(pixel_tuples[j:j+1])
                if img_data[i][j] % 2 != 0:#if value is not even, subtract 1 to make even(if it is even lsb, then it is already 0) 
                    temp_pixels = [x-1 for x in temp_pixels]
                encoded_pixels += temp_pixels
            pixel_count+=1
    return encoded_pixels


"Encode binary representation of text in the remaining pixels that will be put into image, from bottom right to top left of the image (called by def encode_image)"
def encode_text(text_to_encode, img_data, encoded_pixels): 

    #At this point, encoded_pixels already contains the text length encoded pixels, now embed the binary text into encoded_pixels
    text_len = len(text_to_encode) #Set length of text to encode
    num_pixels = int(text_len/3) #the number of pixels needed to embed text (text may either wholly or partially span pixels)
    k = 1 #Used to decrement index of encoded_message in the following for j loop
    for i in range (11, num_pixels + 11 + 1, 1): # Stop at num_pixels + 11 + 1 to account for text that partially spans pixels 
        for j in range(0,3,1): #B, G, R
            pixel_tuples = img_data[i]
            if text_to_encode[text_len-k] == '0':
                temp_pixels = list(pixel_tuples[j:j+1])
                if img_data[i][j] % 2 != 0:  #If value is odd, subtract 1 to make even (then lsb = 0)
                    temp_pixels = [x-1 for x in temp_pixels]
                encoded_pixels += temp_pixels
            if text_to_encode[text_len-k] == '1':
                temp_pixels = list(pixel_tuples[j:j+1])
                if img_data[i][j] % 2 == 0:  #If value is even, add 1 to make odd (then lsb = 1)
                    temp_pixels = [x+1 for x in temp_pixels]
                encoded_pixels += temp_pixels
            k+=1
    embedded_pixel_tuples = [(encoded_pixels[i],encoded_pixels[i+1],encoded_pixels[i+2]) for i in range(0,len(encoded_pixels),3)] #Convert encoded_pixels into tuples
    return embedded_pixel_tuples  


"Decode the input .png image (called by def main)" #Decoding should be improved in a future version, it is simple, slow, & inefficient currently
def decode_image(input_img_file, decoded_file):
    
    encoded_image = Image.open(input_img_file)
    img_pixels = encoded_image.getdata() #.getdata() returns contents of image as a sequence object containing pixel values
    least_significant_bits = "" #least significant bit string
    num_bits_of_encoded_text = decode_text_num_bits(img_pixels, least_significant_bits) #num_bits_of_encoded_text = text length in number of bits
    decode_text(img_pixels, least_significant_bits, num_bits_of_encoded_text, decoded_file) #Decode text, print it to console (+ print to file if user gives output file argument)
    encoded_image.close() #Close file pointer


"Extract text length from image (called by def decode_image)"
def decode_text_num_bits(img_data, bitstring):
    
    for i in range (len(img_data)-11, len(img_data)): #Only need 11 pixels in the bottom right corner of the image
        for j in range (2,-1,-1): #Get R first, then G, then B
            pixel_bits = (bin(img_data[i][j])) #pixel_bits holds the bits of the individual pixel @ img_pixels[i][j]
            bitstring += pixel_bits[-1] #Grab the lsb from the bits of pixel_bits and add it to bitstring    
    bitstring = "".join(reversed(bitstring)) #reverse bitstring
    num_bits = bitstring[:-1] #Remove the last/33rd bit (B at pixel 11), we don't need it
    num_bits = int(num_bits,2) #Convert num_bits to integer from binary
    print("Text length in number of bits:" , num_bits) #Print the number of bits of encoded text in integer format
    return num_bits


"Decode text, print it to console + print to file if user provides args.output_filename argument (called by def decode_image)"
def decode_text(img_data, bitstring, num_bits, out_file):
    
    num_pixels = int(num_bits/3) #num_pixels = number of pixels that the text spans (message could be either wholly or partially spanning these pixels)
    for i in range (len(img_data)-(num_pixels + 11 + 1), len(img_data)-11): # num_pixels + 11 + 1 to account for text that partially spans pixels 
        for j in range (2,-1,-1): #Get R first, then G, then B
            pixel_bits = (bin(img_data[i][j])) #pixel_bits holds the bits of the individual pixel @ img_pixels[i][j]
            bitstring += pixel_bits[-1] #Grab the lsb from the bits of pixel_bits and add it to temp_lsb string
            if pixel_bits == num_bits: #if we've reached an amount of pixel bits equal to the number of bits in text, break
                break;
    bitstring = "".join(reversed(bitstring)) #Reverse temp_lsb string
    encoded_byte =  "" #Will contain a byte from bitstring
    decoded_text = "" #Will contain the decoded message
    #Grab one byte at a time, convert it to character and it add to decoded_text
    for i in range(0,num_bits,8):
        for j  in range (0,8,1):
            encoded_byte += (str(bitstring[i]))
            i+=1
        encoded_ascii = int(encoded_byte,2) #Convert encoded_char to int from base 2
        decoded_char = chr(encoded_ascii) #Decoded character
        decoded_text += decoded_char #Add the char to the message
        encoded_byte =  "" #Reset encoded_byte for the next loop
    print("Decoded text  :\n") 
    print (decoded_text) #Print decoded text to console
    if (out_file):
        f = open(out_file, 'w', newline = '', encoding='utf8')
        f.write(decoded_text) #Write the decoded message to the file


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-opt", dest = 'option')
    parser.add_argument('-inputImg', dest = 'input_img_filename')
    parser.add_argument('-txt', dest = 'text')
    parser.add_argument('-inputFile', dest = 'input_filename')
    parser.add_argument('-outputFile', dest = 'output_filename')
    parser.add_argument('-outputImg', dest = 'output_img_filename', default='C:\Python34\encoded_image.png')
    args = parser.parse_args()

    #Encode .jpeg image with data from a file
    if (args.option == 'encode') and (args.input_filename):
        with open(args.input_filename, 'r', newline = '', encoding= 'utf8') as myfile:
            data = myfile.read()
        encode_image(args.input_img_filename, data, args.output_img_filename) 

    #Encode .jpeg image with console inputted text
    if (args.option == 'encode') and (args.text):
        encode_image(args.input_img_filename, args.text, args.output_img_filename) 

    #Decode a .png image, prints decoded message to the console as well as to a file specified by args.output_filename
    if (args.option == 'decode') and (args.output_filename):
        decode_image(args.input_img_filename, args.output_filename) 

    #Decode a .png image, just prints the decoded message to the console
    if (args.option == 'decode') and (args.output_filename==None) :
        decode_image(args.input_img_filename, args.output_filename)
        
        
if __name__ == '__main__':
    main()
