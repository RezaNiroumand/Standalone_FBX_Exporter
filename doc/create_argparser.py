import argparse
import ast

def parse_list(string):
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError) as e:
        raise argparse.ArgumentTypeError(f"Invalid list format: {string}")

def some_parser():

    parser = argparse.ArgumentParser(description= 'Hello this is an argparser')

    parser.add_argument('-i',
                        '--input_dir',
                        help= 'User specify which maya file to open',
                        type = str,
                        required = True)
    parser.add_argument('-o',
                        '--output_dir',
                        help= 'User specify which folder to export to',
                        type = str,
                        required = True)
    parser.add_argument('-objs',
                        '--objects',
                        help= 'Selection of objects',
                        type = parse_list,
                        required = False)
    
    args = parser.parse_args()
    
    return args.input_dir, args.output_dir, args.objects


a = some_parser()
print(a[2])
