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
    server.sin_port = htons(5555);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(client_fd, (struct sockaddr*)&server, sizeof(server));

    int32_t n1, n2;
    printf("Lungime primul sir = ");
    scanf("%d\n", &n1);
    int32_t* v1 = malloc(sizeof(int32_t) * n1);
    for(int i = 1; i <= n1; i++){
        scanf("%d", &v1[i]);
    }

    printf("Lungime al doilea sir = ");
    scanf("%d\n", &n2);
    int32_t* v2 = malloc(sizeof(int32_t) * n2);
    for(int i = 1; i <= n2; i++){
        scanf("%d", &v2[i]);
    }

    int32_t n_n1, n_n2;
    n_n1 = htonl(n1);
    send(client_fd, &n_n1, 4, 0);
    for(int i = 1; i <= n1; i++){
        int32_t aux = htonl(v1[i]);
        send(client_fd, &aux, 4, 0);
    }

    n_n2 = htonl(n2);
    send(client_fd, &n_n2, 4, 0);
    for(int i = 1; i <= n2; i++){
        int32_t aux = htonl(v2[i]);
        send(client_fd, &aux, 4, 0);
    }

    int32_t n_n3;
    recv(client_fd, &n_n3, 4, 0);
    int32_t n3 = ntohl(n_n3);

    int32_t* v3 = malloc(sizeof(int32_t) * n3);
    for(int i = 1; i <= n3; i++){
        int32_t aux;
        recv(client_fd, &aux, 4, 0);
        v3[i] = ntohl(aux);
    }

    printf("Array: ");
    for(int i = 1; i <= n3; i++){
        printf("%d", v3[i]);
    }

    free(v1);
    free(v2);
    free(v3);
    return 0;
}