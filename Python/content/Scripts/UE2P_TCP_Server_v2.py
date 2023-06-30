# Python 3.9
# Made by: Fortbonnitar
# This works as a bridge between Unreal Engine and Python by allowing the exchanging of data through a local TCP socket connection.




# # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # ################                                 ##############        ########################
# XXX XXX XXX XXX XXX XXX XXX XXX ## XXX XXX XXX XXX XXX XXX XXX XXX ################         ############            ################      ########################
# XXX XXX# # # # # # # # #XXX XXX ## XXX XXX# # # # # # # # #XXX XXX ###                    ####        ####          ###           ###                ### 
# XXX #         ###         # XXX ## XXX #         ###         # XXX ###                  ###              ###        ###            ###               ### 
# XXX #       ### ###       # XXX ## XXX #       ### ###       # XXX ###                ###                  ###      ###            ###               ### 
# XXX #      ###   ###      # XXX ## XXX #      ###   ###      # XXX ############      ###                    ###     ###           ###                ### 
# XXX #     ###  X  ###     # XXX ## XXX #     ###  X  ###     # XXX ############      ###                    ###     ###         ###                  ### 
# XXX #      ###   ###      # XXX ## XXX #      ###   ###      # XXX ###               ###                    ###     #############                    ### 
# XXX #       ### ###       # XXX ## XXX #       ### ###       # XXX ###                ###                  ###      ###         ###                  ### 
# XXX #         ###         # XXX ## XXX #         ###         # XXX ###                 ###                ###       ###           ###                ### 
# XXX XXX# # # # # # # # #XXX XXX ## XXX XXX# # # # # # # # #XXX XXX ###                  ###              ###        ###             ###              ### 
# XXX XXX XXX XXX XXX XXX XXX XXX ## XXX XXX XXX XXX XXX XXX XXX XXX ###                   ###            ###         ###              ###             ### 
# # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # ###                     ##############           ###               ###            ###                                
                  #################################
                  #  |_|_|_|_|_|_|_|_|_|_|_|_|_|  #                  #####################################################################################################
                  #  | | | | | | | | | | | | | |  #
                  #################################







import socket
import numpy
import csv
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
import numpy as np



debug: bool= False 
csv_data_in = []
csv_save_filename = 'player_mimic.csv'
csv_header = ['throttle','left','right','speed','input_steering','input_throttle']

# run_type = input("Are you wanting to teach or load model? Enter 'teach' or 'load'     ")
# while run_type != 'teach' and run_type != 'load':
#     print('Error incorrect entry, please try again... ')
#     run_type = input("Are you wanting to teach or load model? Enter 'teach' or 'load'     ")


##########################################################################################
# BASIC FUNCTIONS
###########################################################################################


def change_type(current_data, new_type: str):
    '''
    Currently can convert a variable to types, [float, int, str, bool]
    
    '''
    try:

        if new_type == 'float':
            result = float(current_data)
        if new_type == 'int':
            result = int(current_data)
        if new_type == 'string' or new_type == 'str':
            result = str(current_data)
        if new_type == 'boolean' or new_type == 'bool':
            result = bool(current_data)
        return result
    except Exception as conv_error:
        print(conv_error)
        return current_data


class driver_agent:

    def __init__(self, throttle_model_path, steering_model_path):
        self.throttling_model = tf.keras.models.load_model(throttle_model_path)
        self.steering_model = tf.keras.models.load_model(steering_model_path)

    def get_steer_direction(self, front_trace, left_trace, right_trace, current_speed):
        vehicle_inputs = np.array([[front_trace, left_trace, right_trace, current_speed]])
        steer =self.steering_model.predict(vehicle_inputs)

        pred_dir = np.argmax(steer)

        if pred_dir == 0:
            dir = -1
            
        if pred_dir == 1:
            dir = 0
            
        if pred_dir == 2:
            dir = 1

        return dir

    def get_throttle(self, front_trace, left_trace, right_trace, current_speed):

        vehicle_inputs = np.array([[front_trace, left_trace, right_trace, current_speed]])
        throttle =self.throttling_model.predict(x_test)

        return np.ravel(throttle).item()

    def use_models(self, data_string):

        data_split1 = data_string.split('A')  #    [0.614246]  [0.100674B0.113973C0.10119D0.000E0.000]
                                                    #        0                             1
        throttle = float(data_split1[0])

        data_split2 = data_split1[1].split('B')  #    [0.100674]  [0.113973C0.10119D0.000E0.000] 
                                                    #         0                     1
        left = float(data_split2[0])
            
        data_split3 = data_split2[1].split('C')  #     [0.113973]  [0.10119D0.000E0.000]
                                                    #           0                1

        right = float(data_split3[0])

        data_split4 = data_split3[1].split('D') #         [0.10119]   [0.000E0.000]
                                                    #             0            1

        speed = float(data_split4[0])


        steering = self.get_steer_direction(throttle, left, right, speed)
        throttle = self.get_throttle(throttle, left, right, speed)

        return steering, throttle




def record_user_driving(data: str):
        
    global csv_data_in

    # Splitting the data into 3 floats   raw_data_format-> '0.000A0.000B0.000C0.000D0.000E0.000
    # 1 is throttle distance
    # 2 is left sensor distance
    # 3 is right sensor distance
    # 4 is speed

    player_in_data = []
    data_split1 = data_string.split('A')  #    [0.614246]  [0.100674B0.113973C0.10119D0.000E0.000]
                                        #        0                             1
    throttle_in = float(data_split1[0])

    data_split2 = data_split1[1].split('B')  #    [0.100674]  [0.113973C0.10119D0.000E0.000] 
                                            #         0                     1
    left_in = float(data_split2[0])
    
    data_split3 = data_split2[1].split('C')  #     [0.113973]  [0.10119D0.000E0.000]
                                            #           0                1

    right_in = float(data_split3[0])

    data_split4 = data_split3[1].split('D') #         [0.10119]   [0.000E0.000]
                                            #             0            1

    speed_in = float(data_split4[0])

    data_split5 = data_split4[1].split('E') #             [0.000]  [0.000]
                                            #                0        1
    steering_in = float(data_split5[0])
    throttle_input = float(data_split5[1])

    player_in_data = [f'{throttle_in}',f'{left_in}',f'{right_in}',f'{speed_in}', f'{steering_in}',f'{throttle_input}']

    # Add to the csv data list
    csv_data_in.append(player_in_data)



        # Handling Throttle Calculations
    if throttle_in < 1.0:
        throttle_out = throttle_in * 0.5
    else:
        throttle_out = .5


    # Handling Steering Calculations
    if left_in >= 1.0 and right_in >= 1.0:
        steering_out = 0
    else:
        steering_out = (left_in + -right_in) * 2


    return [steering_out, throttle_out]
    






##########################################################################################
# Set this script as a TCP-Server and create the socket and listen for Unreal connection 
###########################################################################################


# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the server socket to a specific IP address and port
server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)


# Listen for incoming connections
server_socket.listen(1)
print("Server started. Waiting for connections...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Client connected: {client_address}")










##############################################################################
# After Connection established successfully, if data recieved set as variable
###############################################################################


running = True

# Main Loop
while running:
    try:
        data = client_socket.recv(4096)
        # print(f'data_oring = {data}')

        if data == '':
            running = False
        

        # Data is firstly decoded from bytes to a string
        data_string = data.decode()
        if debug == True:
            print(f'data as string = {data_string}')




#############################################################################################################
# Records the user driving and saves to a csv file for the Neural Network to train on later
##############################################################################################################

        # if run_type == 'teach':
        #     steering_out, throttle_out = record_user_driving(data_string) 

 
      

#############################################################################################################
# Uses Pretrained Models to process incoming data
##############################################################################################################

        # if run_type == 'load':

        driver = driver_agent('/content/drive/MyDrive/UE5_Drive/ue5_throttle_model.bak', '/content/drive/MyDrive/UE5_Drive/ue5_dir_model.bak')

        steering_out, throttle_out = driver.use_models(data_string)





###################################################################################################
# Formatting and converting data to string
###################################################################################################

        # converting processed data from float to string

        result_data_string = f'{throttle_out}:{steering_out}'
        print(f'throttle= {throttle_out}, steering= {steering_out}')

###################################################################################################
# Send the data back to Unreal Engine
###################################################################################################

        # Converting the sending data from string to bytes 
        reply_data = bytes(result_data_string, 'utf-8')
        # print(f'reply_data = {reply_data}')

        # Sending back to Unreal Engine
        send = client_socket.send(reply_data)
        # print(f'send = {send}')

    except Exception as error:
        print(error)
        input('Enter c to continue...   ')


###################################################################################################
# Save Player activity to csv
###################################################################################################


# with open(csv_save_filename, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(csv_header)  # Write the header
#     for entry in csv_data_in:
#          writer.writerow(entry)
#     # writer.writerows(player_in_data)   # Write the data rows

# print(f"Data has been written to {len(csv_data_in)} successfully.: {csv_data_in[0]}")




