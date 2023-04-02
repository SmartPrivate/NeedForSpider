def get_header(header_file='header.txt'):
    with open(header_file, 'r', encoding='utf-8') as reader:
        lines = list(map(lambda o: o.strip('\n').split(': '), reader.readlines()))
        return {line[0]: line[1] for line in lines}
