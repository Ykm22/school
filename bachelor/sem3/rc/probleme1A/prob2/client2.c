#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char** agrv){
    //int client_socket = socket(AF_INET, SOCK_STREAM, 0); 
    int client_socket = socket(AF_INET, SOCK_DGRAM, 0); 

    struct sockaddr_in server;
    int server_len = sizeof(server);
    server.sin_family = AF_INET;
    server.sin_port = htons(7777);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    //connect(client_socket, (struct sockaddr*) &server, sizeof(server));

    char string[40];
    printf("String: ");
    //fgets ia si enter de la final => trebuie bagat '\0' la strlen(string) - 1
    fgets(string, 40, stdin);
    
    int32_t string_len = strlen(string) - 1;
    // string[string_len + 1] = '\0';
    int32_t network_string_len = htonl(string_len);

    sendto(client_socket, &network_string_len, 4, 0, (struct sockaddr*)&server, server_len);

    sendto(client_socket, string, string_len, 0, (struct sockaddr*)&server, server_len);
    
    int32_t network_cnt;
    recvfrom(client_socket, &network_cnt, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t cnt = ntohl(network_cnt);
    printf("cnt = %d", cnt);

    return 0;
}