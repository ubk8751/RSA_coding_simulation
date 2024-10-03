from utils import (Alice, Bob, Code, argparser)
import os

def main(A:Alice, B:Bob, code:Code, message:int, **kwargs):
    message = A.send(m=message, code_order=code.code_order)

    B.receive(c=message)

def inverse_check(e, d, beta):
    print(f'Inverse check: {(e * d) % beta == 1}')

if __name__ == "__main__":
    code = None
    if os.path.exists('Code.pkl'):
        code = Code(code_order=-1)
        code.load()

    args = argparser(code_order=code.code_order if code is not None else -1)
    
    if args.gen_code > 0 :    
        if not os.path.exists('Code.pkl'):
            code = Code(code_order=args.gen_code)
        code.gen_code(code_order=args.gen_code,
                      min_distance=args.min_distance)
        code.save()
    
    B = Bob(p=args.p, q=args.q, additional_bits=args.additional_bits)


    A = Alice(pub_key=B.pub_key, additional_bits=B.additional_bits)
    
    print(f'P: {args.p}, Q: {args.q}\nAlpha: {B.alpha}, Beta: {B.beta}\ne: {B.e}, d: {B.d}')
    inverse_check(e=B.e, d=B.d, beta=B.beta)

    main(A=A, B=B, code=code, message=args.m)
    

