<?php
$s = socket_create(AF_INET, SOCK_STREAM, 0);
socket_connect($s, "127.0.0.1", 3333);

$msg = readline("String for server: ");
socket_send($s, $msg, 100, 0);

$start_substring = readline("Start of wanted substring: ");
socket_send($s, $start_substring, 100, 0);

$substring_length = readline("Wanted substring length: ");
socket_send($s, $substring_length, 100, 0);

socket_recv($s, $substring_wanted, 100, 0);
echo "Received from server:: $substring_wanted\n"; 
?>
