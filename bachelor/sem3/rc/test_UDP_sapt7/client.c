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
    int32_t port = atoi(argv[2]);
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(argv[1]);

    //start
    int32_t n;
    printf("Lungimea sirului: n = ");
    scanf("%d", &n);
    int32_t* v = (int32_t*)malloc(n * 4 + 4);
    printf("Sirul de nr de minim 2 cifre: ");
    for(int i = 1; i <= n; i++){
        scanf("%d", &v[i]);
    }
        int32_t n_n = htonl(n);
    sendto(client_fd, &n_n, 4, 0, (struct sockaddr*)&server, server_len);
    for(int32_t i = 1; i <= n; i++){
        int32_t x = htonl(v[i]);
        sendto(client_fd, &x, 4, 0, (struct sockaddr*)&server, server_len);
    }
    printf("a\n");
    char start_msg[10];
    int32_t n_len_msg;
    recvfrom(client_fd, &n_len_msg, 4, 0, (struct sockaddr*)&server, &server_len);
    printf("b\n");
    int32_t len_msg = ntohl(n_len_msg);
    recvfrom(client_fd, start_msg, len_msg, 0, (struct sockaddr*)&server, &server_len);
    start_msg[len_msg] = '\0';
    printf("%s\n", start_msg);
    server_len = sizeof(server);
    int tries = 0;
    int hit = 3;
    while(tries < 5 || hit > 0){
        printf("Tries: %d\n", tries);
        printf("Din primii 3 cei mai frecventi mai sunt %d", hit);
        int32_t guess;
        scanf("%d", &guess);
        int32_t n_guess = htonl(guess);
        sendto(client_fd, &n_guess, 4, 0, (struct sockaddr*)&server, server_len);
        
        int32_t n_len;
        recvfrom(client_fd, &n_len, 4, 0, (struct sockaddr*)&server, &server_len);
        int32_t len = ntohl(n_len);
        printf("len = %d\n", len);
        char answer[10];
        recvfrom(client_fd, answer, len, 0, (struct sockaddr*)&server, &server_len);

        answer[len] = '\0';
        if(strcmp(answer, "Corect") == 0){
            printf("Raspuns corect");
            hit--;
            tries++;
        } else{
            printf("Raspuns incorect");
            tries++;
        }

    }
    if(tries == 5){
        printf("Joc pierdut\n");
    } else {
        printf("Joc castigat\n");
    }
    free(v);
    close(client_fd);
    return 0;
}