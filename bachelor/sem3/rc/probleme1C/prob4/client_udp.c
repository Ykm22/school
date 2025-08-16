#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char**argv){
    int32_t client_fd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in server;
    int32_t server_len = sizeof(server);
    server.sin_family = AF_INET;
    server.sin_port = htons(2222);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    sendto(client_fd, 0, 0, 0, (struct sockaddr*)&server, server_len);

    int32_t n_new_port;
    recvfrom(client_fd, &n_new_port, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t new_port = ntohl(n_new_port);
    server.sin_port = htons(new_port);

    //start

    char string[105];
    printf("String = ");
    fgets(string, 105, stdin);
    int32_t string_len = strlen(string) - 1;
    int32_t n_string_len = htonl(string_len);
    sendto(client_fd, &n_string_len, 4, 0, (struct sockaddr*)&server, server_len);
    sendto(client_fd, string, string_len, 0, (struct sockaddr*)&server, server_len);

    char reversed_string[105];
    recvfrom(client_fd, reversed_string, string_len, 0, (struct sockaddr*)&server, &server_len);
    printf("Received from server : %s\n", reversed_string);
    close(client_fd);
    return 0;
}