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
    int client_fd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in server;
    int server_len = sizeof(server);
    server.sin_family = AF_INET;
    server.sin_port = htons(7775);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    //connect(client_fd, (struct sockaddr *) &server, sizeof(server));

    sendto(client_fd, 0, 0, 0, (struct sockaddr*)&server, server_len);

    int32_t n_new_port;
    recvfrom(client_fd, &n_new_port, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t new_port = ntohl(n_new_port); 
    server.sin_port = htons(new_port);

    char string1[50];
    printf("Firstg sorted string: ");
    fgets(string1, 50, stdin);
    int32_t string1_len = strlen(string1) - 1;
    int32_t network_string1_len = htonl(string1_len);

    sendto(client_fd, &network_string1_len, 4, 0, (struct sockaddr*)&server, server_len);
    sendto(client_fd, string1, string1_len, 0, (struct sockaddr*)&server, server_len);

    char string2[50];
    printf("Second sorted string: ");
    fgets(string2, 50, stdin);
    int32_t string2_len = strlen(string2) - 1;
    int32_t network_string2_len = htons(string2_len);
    sendto(client_fd, &network_string2_len, 4, 0, (struct sockaddr*)&server, server_len);
    sendto(client_fd, string2, string2_len, 0, (struct sockaddr*)&server, server_len);

    char result_string[100];
    int32_t network_result_string_len;
    recvfrom(client_fd, &network_result_string_len, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t result_string_len = ntohl(network_result_string_len);
    
    recvfrom(client_fd, result_string, result_string_len, 0, (struct sockaddr*)&server, &server_len);
    printf("s = %s", result_string);
    close(client_fd);
    return 0;
}