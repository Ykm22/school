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
    int32_t n;
    printf("n = ");
    scanf("%d", &n);
    int32_t n_n = htonl(n);
    sendto(client_fd, &n_n, 4, 0, (struct sockaddr*)&server, server_len);

    char answer[10];
    int32_t n_answer_len;
    recvfrom(client_fd, &n_answer_len, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t answer_len = ntohl(n_answer_len);
    
    recvfrom(client_fd, answer, answer_len, 0, (struct sockaddr*)&server, &server_len);
    answer[answer_len] = '\0';

    printf("Received from server %s\n", answer);
    if(strcmp(answer, "True") == 0){
        printf("%d is prime", n);
    } else {
        printf("%d is not prime", n);
    }

    close(client_fd);
    return 0;
}