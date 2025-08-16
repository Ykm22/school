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
    // int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    int client_fd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in server;
    int server_len = sizeof(server);
    memset((char*)&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(8884);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    // connect(client_socket, (struct sockaddr *) &server, sizeof(server));

    int32_t n;
    printf("n = ");
    scanf("%d", &n);
    int32_t network_n = htonl(n);

    // send(client_socket, &network_n, 4, 0);
    sendto(client_fd, &network_n, 4, 0, (struct sockaddr*)&server, server_len);

    int32_t* v = (int32_t*)malloc(n * 4);

    for(int i = 1; i <= n; i++){
        scanf("%d", &v[i]);
        int network_x = htonl(v[i]);
        sendto(client_fd, &network_x, 4, 0, (struct sockaddr*)&server, server_len);
    }
    
    int32_t network_sum;
    recvfrom(client_fd, &network_sum, 4, 0, (struct sockaddr*)&server, &server_len);
    int32_t sum = ntohl(network_sum);
    printf("sum = %d", sum);
    
    free(v);
    close(client_fd);
    return 0;
}