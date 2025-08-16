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
    recvfrom(client_fd, 0, 0, 0, (struct sockaddr*)&server, &server_len);
    
    //start

    char string[105];
    printf("String = ");
    fgets(string, 105, stdin);
    int32_t string_len = strlen(string) - 1;
    printf("read string = %s\n", string);
    int32_t n_string_len = htonl(string_len);
    sendto(client_fd, &n_string_len, 4, 0, (struct sockaddr*)&server, server_len);
    sendto(client_fd, string, string_len, 0, (struct sockaddr*)&server, server_len);
    
    char ch;
    printf("Character = ");
    scanf("%s", &ch);


    sendto(client_fd, &ch, 1, 0, (struct sockaddr*)&server, server_len);

    int32_t n_n;
    recvfrom(client_fd, &n_n, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t n = ntohl(n_n);
    int* v = (int*)malloc(4 * n);
    for(int i = 1; i <= n; i++){
        int32_t n_x;
        recvfrom(client_fd, &n_x, 4, 0, (struct sockaddr*)&server, &server_len);
        v[i] = ntohl(n_x);
    }

    printf("Position vector: ");
    for(int i = 1; i <= n; i++){
        printf("%d ", v[i]);
    }

    free(v);
    close(client_fd);
    return 0;
}