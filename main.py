# Added stuff to put on github later 
# added a password strength check 
# loop until password meets the password strength requrements 
# added 3 attempts to password entries when extracting the message from the image 




# if not is_strong_password(password):
  #  print("Password must be at least 8 characters long, and include upper and lower case letters, digits, and special characters.")
   # password = input("Set a password: ")

def to_binary(data):  # Converts a string to its binary representation
    return ''.join(format(ord(char), '08b') for char in data)

def from_binary(binary_data):  # Converts binary data back to a string
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message = message + chr(int(byte, 2))
    return message

def encode_message(image_path, message):  # Encodes a message into an image
    with open(image_path, 'rb') as image_file:  # Opens the image file in binary read mode
        image_data = bytearray(image_file.read())

    binary_message = to_binary(message) + '00000000'  # Converts message to binary and adds an end marker

    if len(binary_message) > (len(image_data) - 54) * 8:  # Checks if the message fits into the image
        print("Error: Message too long for the image.")
        return

    index = 0
    for i in range(54, len(image_data)):  # Embeds the binary message using LSB method, skipping the header
        if index < len(binary_message):
            image_data[i] = (image_data[i] & 0xFE) | int(binary_message[index])
            index = index + 1

    encoded_image_path = 'd:\\encoded_image.bmp'  # Defines path for saving the encoded image
    with open(encoded_image_path, 'wb') as output_file:  # Saves the modified image data
        output_file.write(image_data)
    print(f"Encoded image saved as '{encoded_image_path}'")

def decode_message(image_path, password):  # Decodes a message from the image
    attempts = 3  # Number of attempts allowed
    while attempts > 0:
        input_password = input("Enter your password to decode and extract the message: ").strip()  # Asks user for password
        if input_password == password:  # Checks if the entered password matches the set password
            with open(image_path, 'rb') as image_file:  # Opens the image file in binary read mode again
                image_data = bytearray(image_file.read())

            binary_message = ""
            for i in range(54, len(image_data)):  # Extracts the binary message using LSB method, skipping the header
                binary_message = binary_message + str(image_data[i] & 1)

            end_marker_index = binary_message.find('00000000')  # Finds the end marker in the binary message
            if end_marker_index != -1:  # If end marker is found, converts binary message back to string
                binary_message = binary_message[:end_marker_index]
                decoded_message = from_binary(binary_message)
                print("Decoded message:", decoded_message)
            else:  # If no end marker is found, prints error
                print("Error: No hidden message found.")
            return
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Error: Incorrect password. You have {attempts} more attempts.")
            else:
                print("Error: Incorrect password. You have exhausted all attempts. Access denied.")
                return

def is_strong_password(password):   # Checks if the password meets strength criteria
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "!@#$%^&*(),.?\":{}|<>"

    for char in password:
        if 'A' <= char <= 'Z':
            has_upper = True
        elif 'a' <= char <= 'z':
            has_lower = True
        elif '0' <= char <= '9':
            has_digit = True
        elif char in special_characters:
            has_special = True

    return has_upper and has_lower and has_digit and has_special

# Get user input for encoding
image_path = input("Enter the image path: ")
password = input("Set a password: ")

while not is_strong_password(password): 
    print("Password must be at least 8 characters long, and include upper and lower case letters, digits, and special characters.")
    password = input("Set a password: ")

# if not is_strong_password(password):
  #  print("Password must be at least 8 characters long, and include upper and lower case letters, digits, and special characters.")
   # password = input("Set a password: ")

message = input("Enter the message to hide: ")
encode_message(image_path, message)

# Get user input for decoding
encoded_image_path = 'encoded_image.bmp'
decode_message("d:\\encoded_image.bmp", password)

