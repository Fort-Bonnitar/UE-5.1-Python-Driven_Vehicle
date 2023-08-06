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


debug = False



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
    data = client_socket.recv(4096)
    # print(f'data_oring = {data}')

    if data == '':
        running = False
    

    # Data is firstly decoded from bytes to a string
    data_string = data.decode()
    if debug == True:
        print(f'data as string = {data_string}')



    result_data_string = 'Hello World!'

    # Converting the sending data from string to bytes 
    reply_data = bytes(result_data_string, 'utf-8')


    # Sending back to Unreal Engine
    send = client_socket.send(reply_data)
    
