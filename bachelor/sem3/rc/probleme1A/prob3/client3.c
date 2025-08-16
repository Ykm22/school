#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char** argv){

    // int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    int client_socket = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in server;
    int server_len = sizeof(server);
    server.sin_family = AF_INET;
    server.sin_port = htons(7776);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    //connect(client_socket, (struct sockaddr *) &server, sizeof(server));

    printf("Give string: ");
    char string[50];
    fgets(string, 50, stdin);
    int32_t string_len = strlen(string) - 1;

    //send length of string as network type
    int32_t network_string_len = htonl(string_len);
    sendto(client_socket, &network_string_len, 4, 0, (struct sockaddr*)&server, server_len);

    //send string with string_len bytes
    sendto(client_socket, string, string_len, 0, (struct sockaddr*)&server, server_len);

    //recv string of string_len length
    char reversed_string[50];
    recvfrom(client_socket, reversed_string, string_len, 0, (struct sockaddr*)&server, &server_len);
    printf("%s", reversed_string);
    
    return 0;
}