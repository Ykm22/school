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
    int client_fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(6666);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(client_fd, (struct sockaddr*)&server, sizeof(server));

    int32_t n;
    printf("n = ");
    scanf("%d", &n);
    int32_t network_n = htonl(n);
    send(client_fd, &network_n, 4, 0);

    int32_t network_dividers_len;
    recv(client_fd, &network_dividers_len, 4, 0);
    char dividers[10000];
    int32_t dividers_len = ntohl(network_dividers_len);
    recv(client_fd, dividers, dividers_len, 0);    

    printf("dividers: %s", dividers);

    return 0;
}