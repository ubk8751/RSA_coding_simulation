from argparse import ArgumentParser as argparser

def check_security_level(p:int,
                         q:int,
                         security_level:int,
                         code_order:int, **kwargs) -> tuple[bool, int]:
    '''
    Function to check if a provided number is a prime.
    
    :parameter int p: the first prime used to calculate the various parameters in the RSA method.
    :parameter int q: the second prime used to calculate the various parameters in the RSA method.
    :parameter int security_level: the security level required for the encryption.
    :parameter int code_order: the length of each code word in the code
    
    :return bool: returns `True` if p*q is large enough and `False` otherwise.
    :return int: returns -1 if p*q is large enough, the required_alpha if not. 
    '''
    required_alpha = code_order * 2**(security_level-1)

    if p * q < required_alpha:
        return False, required_alpha
    
    return True, -1

def gen_default_m(code_order:int, **kwargs) -> int:
    if code_order < 1:
        code_order = 1
    return int(''.join("1" for _ in range(code_order)), 2) // 2

def is_prime(n:int, **kwargs) -> bool:
    '''
    Function to check if a provided number is a prime.
    
    :parameter int n: the provided integer to evaluate. `n` needs to be nonnegative.
    
    :return bool: returns `True` if `n` is prime and `False` otherwise.

    Taken from [stackoverflow](https://stackoverflow.com/a/15285590).
    '''
    if n < 2: 
         return False;
    if n % 2 == 0:             
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def c_args(code_order:int,  **kwargs):
    parser = argparser(prog='Simple RSA and coding simulator',
                       description='''A program to simulate communication using the
                                      RSA method, and checking message validity using
                                      simple coding.''')
    parser.add_argument('-p',
                        type=int,
                        default=3,
                        dest='p',
                        help='''The first of two primes to calculate the various parameters.'''
                        )
    parser.add_argument('-q',
                        type=int,
                        default=5,
                        dest='q',
                        help='''The second of two primes to calculate the various parameters.'''
                        )
    parser.add_argument('--generate-code',
                        type=int,
                        default=-1,
                        dest='gen_code',
                        help='''Toggle if a new code should be generated. If toggled,
                        input the length of a keyword, so that it says --generate-code
                        [int]. Default value is -1, which means to not generate a new code.''')
    parser.add_argument('--security-level',
                        type=int,
                        default=1,
                        dest='security_level',
                        help='''Security level for the RSA method. Used to calculate the
                        required size of n. 1: Low, 2: Medium, 3: High.''')
    parser.add_argument('--min-distance',
                        type=int,
                        default=2,
                        dest='min_distance',
                        help='''The smallest Hamming distance between any two distinct codewords
                        in the code, determining its capacity to detect up to `d-1` errors and
                        correct up to `[(d-1)/2]` errors, where `d` is the minimum distance.''')
    parser.add_argument('-m',
                        type=int,
                        default=gen_default_m(code_order=code_order),
                        dest='m',
                        help='''The message A sends to B. Should be an integer. Default is the
                        maximum number a binary number of half the length code_order.''')
    parser.add_argument('--additional-bits',
                        type=int,
                        default=4,
                        dest='additional_bits',
                        help='''The extra bits that are to be added to further decrypt each
                        message.''')
    
    args = parser.parse_args()
    
    if code_order == -1 and args.gen_code < 0:
        print(f'There is no pre-generated code! Please generate a new one.')
        exit(1)

    if args.gen_code != -1:
        code_order = args.gen_code

    if not is_prime(args.p):
        print(f'ERROR: P should be a prime number. {args.p} is not a prime number.')
        exit(1)
    
    if not is_prime(args.q):
        print(f'ERROR: Q should be a prime number. {args.q} is not a prime number.')
        exit(1)
    
    if args.security_level not in [1,2,3]:
        print(f'{args.security_level} is not an accepted security level. It should be 1, 2, or 3.')
        exit(1)
    sufficient_security, required_product = check_security_level(p=args.p,
                                                                 q=args.q,
                                                                 security_level=args.security_level,
                                                                 code_order=code_order)
    if not sufficient_security:
        print(f'The provided p and q, {args.p} and {args.q}, does not provide a sufficient security level for your encoding. The product needs to be at least {required_product}!')
        exit(1)

    if args.gen_code > 0 and args.min_distance < 2:
        print(f'The min distance needs to be at least 2 to be able to detect any errors!')
        exit(1)

    if args.gen_code > 0 and args.min_distance > args.gen_code//2:
        print(f'The provided min distance will make the code too small! Please make it less than half the `code_order`!')
        exit(1)

    return args


    