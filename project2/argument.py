def add_arguments(parser):
    # Sender:   IP, Port, path of source file,... etc.
    # Receiver: IP, port ,path of destination file, ... etc.
    # Agent:    IP, port, loss rate, ... etc.
    parser.add_argument('--IP', type=str, default='127.0.0.1')
    parser.add_argument('--Port', type=int, default=6666)
    parser.add_argument('--packet_size', type=int, default=1024)
    parser.add_argument('--time_out', type=float, default=1)
    parser.add_argument('--threshold', type=int, default=16)
    return parser
