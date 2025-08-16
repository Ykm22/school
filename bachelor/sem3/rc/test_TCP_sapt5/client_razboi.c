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
    server.sin_port = htons(2222);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(client_fd, (struct sockaddr*)&server, sizeof(server));

    printf("Give n, 4 <= n <= 9: ");
    int32_t n;
    scanf("%d", &n);
    int32_t n_n = htonl(n);
    send(client_fd, &n_n, 4, 0);

    char start_msg[5000];
    // int32_t n_start_msg_len;
    // recv(client_fd, &n_start_msg_len, 4, 0);
    // int32_t start_msg_len = ntohl(n_start_msg_len);
    recv(client_fd, start_msg, 12, 0);
    printf("%s\n", start_msg);

    int mistakes = 0, planes_alive = n;
    printf("Lines and columns between 0 and %d\n", n - 1);
    int32_t guessing_line, guessing_column;
    int32_t n_guessing_line, n_guessing_column;
    while(1){
        printf("Guess line: ");
        scanf("%d", &guessing_line);
        printf("Guess column: ");
        scanf("%d", &guessing_column);

        n_guessing_line = htonl(guessing_line);
        n_guessing_column = htonl(guessing_column);

        send(client_fd, &n_guessing_line, 4, 0);
        send(client_fd, &n_guessing_column, 4, 0);

        char hit[500];
        // int32_t n_hit_len;
        // recv(client_fd, &n_hit_len, 4, 0);
        // int32_t hit_len = ntohl(n_hit_len);
        recv(client_fd, hit, 2, 0);
        printf("Hit? %s\n", hit);

        int32_t n_mistakes;
        recv(client_fd, &n_mistakes, 4, 0);
        int32_t mistakes = ntohl(n_mistakes); 
        printf("Mistakes : %d\n", mistakes);

        if(mistakes == 5){
            break;
        }   

        int32_t n_planes_alive;
        recv(client_fd, &n_planes_alive, 4, 0);
        int32_t planes_alive = ntohl(n_planes_alive);
        printf("Planes alive: %d\n", planes_alive);
        if(planes_alive == 0){
            break;
        }
    }
    int32_t n_result_len;
    recv(client_fd, &n_result_len, 4, 0);
    int32_t result_len = ntohl(n_result_len);
    char result[1000];
    recv(client_fd, result, result_len, 0);

    printf("Result: %s\n", result);


    return 0;
}