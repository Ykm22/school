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
    server.sin_port = htons(3333);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(client_fd, (struct sockaddr*)&server, sizeof(server));

    printf("First char string: ");
    char first_string[100];
    fgets(first_string, 100, stdin);
    int32_t first_string_len = strlen(first_string) - 1;
    int32_t network_first_string_len = htonl(first_string_len);

    send(client_fd, &network_first_string_len, 4, 0);
    send(client_fd, first_string, first_string_len, 0);

    //a = start of string
    //b = length
    int32_t a, b;
    printf("start = ");
    scanf("%d", &a);
    printf("length = ");
    scanf("%d", &b);

    int32_t network_a = htonl(a);
    int32_t network_b = htonl(b);

    send(client_fd, &network_a, 4, 0);
    send(client_fd, &network_b, 4, 0);

    char wantedstring[100];
    int32_t network_wantedstring_len;
    recv(client_fd, &network_wantedstring_len, 4, 0);
    int32_t wantedstring_len = ntohl(network_wantedstring_len);
    recv(client_fd, wantedstring, wantedstring_len, 0);
    printf("wanted string: %s\n", wantedstring);



    return 0;
}