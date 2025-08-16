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

    char string[50];
    printf("First array: ");
    fgets(string, 50, stdin);
    int32_t string_len = strlen(string) - 1;
    int32_t network_string_len = htonl(string_len);
    send(client_fd, &network_string_len, 4, 0);
    send(client_fd, string, string_len, 0);

    char ch;
    printf("Character: ");
    scanf(" %c", &ch);
    send(client_fd, &ch, 1, 0);

    int32_t network_cnt;
    recv(client_fd, &network_cnt, 4, 0);
    int32_t cnt = ntohl(network_cnt);
    printf("cnt = %d\n", cnt);

    char position_string[50];
    int32_t network_posstring_len;
    recv(client_fd, &network_posstring_len, 4, 0);
    int32_t posstring_len = ntohl(network_posstring_len);
    recv(client_fd, position_string, posstring_len, 0);
    printf("position string: %s\n", position_string);

    return 0;
}