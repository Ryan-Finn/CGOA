import sys

OP_CODES = {
    'ADC': {'#': '69', 'zpg': '65', 'zpg,X': '75', 'abs': '6D', 'abs,X': '7D', 'abs,Y': '79', 'ind,X': '61',
            'ind,Y': '71'},
    'AND': {'#': '29', 'zpg': '25', 'zpg,X': '35', 'abs': '2D', 'abs,X': '3D', 'abs,Y': '39', 'ind,X': '21',
            'ind,Y': '31'},
    'ASL': {'': '0A', 'zpg': '06', 'zpg,X': '16', 'abs': '0E', 'abs,X': '1E'},
    'BCC': {'rel': '90'},
    'BCS': {'rel': 'B0'},
    'BEQ': {'rel': 'F0'},
    'BIT': {'zpg': '24', 'abs': '2C'},
    'BMI': {'rel': '30'},
    'BNE': {'rel': 'D0'},
    'BPL': {'rel': '10'},
    'BRK': {'': '00'},
    'BVC': {'rel': '50'},
    'BVS': {'rel': '70'},
    'CLC': {'': '18'},
    'CLD': {'': 'D8'},
    'CLI': {'': '58'},
    'CLV': {'': 'B8'},
    'CMP': {'#': 'C9', 'zpg': 'C5', 'zpg,X': 'D5', 'abs': 'CD', 'abs,X': 'DD', 'abs,Y': 'D9', 'ind,X': 'C1',
            'ind,Y': 'D1'},
    'CPX': {'#': 'E0', 'zpg': 'E4', 'abs': 'EC'},
    'CPY': {'#': 'C0', 'zpg': 'C4', 'abs': 'CC'},
    'DEC': {'zpg': 'C6', 'zpg,X': 'D6', 'abs': 'CE', 'abs,X': 'DE'},
    'DEX': {'': 'CA'},
    'DEY': {'': '88'},
    'EOR': {'#': '49', 'zpg': '45', 'zpg,X': '55', 'abs': '4D', 'abs,X': '5D', 'abs,Y': '59', 'ind,X': '41',
            'ind,Y': '51'},
    'INC': {'zpg': 'E6', 'zpg,X': 'F6', 'abs': 'EE', 'abs,X': 'FE'},
    'INX': {'': 'E8'},
    'INY': {'': 'C8'},
    'JMP': {'abs': '4C', 'ind': '6C'},
    'JSR': {'abs': '20'},
    'LDA': {'#': 'A9', 'zpg': 'A5', 'zpg,X': 'B5', 'abs': 'AD', 'abs,X': 'BD', 'abs,Y': 'B9', 'ind,X': 'A1',
            'ind,Y': 'B1'},
    'LDX': {'#': 'A2', 'zpg': 'A6', 'zpg,Y': 'B6', 'abs': 'AE', 'abs,Y': 'BE'},
    'LDY': {'#': 'A0', 'zpg': 'A4', 'zpg,X': 'B4', 'abs': 'AC', 'abs,X': 'BC'},
    'LSR': {'': '4A', 'zpg': '46', 'zpg,X': '56', 'abs': '4E', 'abs,X': '5E'},
    'NOP': {'': 'EA'},
    'ORA': {'#': '09', 'zpg': '05', 'zpg,X': '15', 'abs': '0D', 'abs,X': '1D', 'abs,Y': '19', 'ind,X': '01',
            'ind,Y': '11'},
    'PHA': {'': '48'},
    'PHP': {'': '08'},
    'PLA': {'': '68'},
    'PLP': {'': '28'},
    'ROL': {'': '2A', 'zpg': '26', 'zpg,X': '36', 'abs': '2E', 'abs,X': '3E'},
    'ROR': {'': '6A', 'zpg': '66', 'zpg,X': '76', 'abs': '6E', 'abs,X': '7E'},
    'RTI': {'': '40'},
    'RTS': {'': '60'},
    'SBC': {'#': 'E9', 'zpg': 'E5', 'zpg,X': 'F5', 'abs': 'ED', 'abs,X': 'FD', 'abs,Y': 'F9', 'ind,X': 'E1',
            'ind,Y': 'F1'},
    'SEC': {'': '38'},
    'SED': {'': 'F8'},
    'SEI': {'': '78'},
    'STA': {'zpg': '85', 'zpg,X': '95', 'abs': '8D', 'abs,X': '9D', 'abs,Y': '99', 'ind,X': '81', 'ind,Y': '91'},
    'STX': {'zpg': '86', 'zpg,Y': '96', 'abs': '8E'},
    'STY': {'zpg': '84', 'zpg,X': '94', 'abs': '8C'},
    'TAX': {'': 'AA'},
    'TAY': {'': 'A8'},
    'TSX': {'': 'BA'},
    'TXA': {'': '8A'},
    'TXS': {'': '9A'},
    'TYA': {'': '98'},
}
BRANCHES = {'BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS'}
JUMPS = {'JMP', 'JSR'}

symbol_table = {}
errors, o_lines = [], set()
start, end = 0, 0


def addressMode(val):
    if val == '':
        return '', '', ''

    if '#' in val:
        return '#', toBase16(val[1:]), ''

    if 'X' in val:
        if '(' in val:
            return 'ind,X', toBase16(val[1:val.find(',')]), ''
        if int(val[1:val.find(',')], 16) > 255:
            temp = toBase16(val[:val.find(',')])
            return 'abs,X', temp[2:], temp[:2]
        return 'zpg,X', toBase16(val[:val.find(',')]), ''

    if 'Y' in val:
        if '(' in val:
            return 'ind,Y', toBase16(val[1:val.find(')')]), ''
        if int(val[1:val.find(',')], 16) > 255:
            temp = toBase16(val[:val.find(',')])
            return 'abs,Y', temp[2:], temp[:2]
        return 'zpg,Y', toBase16(val[:val.find(',')]), ''

    if '(' in val:
        return 'ind', toBase16(val[1:val.find(')')]), ''

    if int(val[1:], 16) > 255:
        temp = toBase16(val)
        return 'abs', temp[2:], temp[:2]

    return 'zpg', toBase16(val), ''


def toBase10(val):
    temp = str(val)
    if temp in symbol_table:
        temp = symbol_table[temp]

    if temp[0] == '$':
        return int(temp[1:], 16)
    if temp[0] == 'O':
        return int(temp[1:], 8)
    if temp[0] == '%':
        return int(temp[1:], 2)
    return int(temp)


def toBase16(val):
    temp = str(val)
    if temp in symbol_table:
        temp = symbol_table[temp]

    if temp[0] == '$':
        return pad(temp[1:]).upper()
    if temp[0] == 'O':
        return pad(hex(int(temp[1:], 8)).lstrip('0x')).upper()
    if temp[0] == '%':
        return pad(hex(int(temp[1:], 2)).lstrip('0x')).upper()
    return pad(hex(int(temp)).lstrip('0x')).upper()


def pad(val):
    if len(val) == 0:
        return '00'
    if len(val) % 2 == 0:
        return val
    return '0' + val


def sanitize(string):
    temp = string[:string.find(',')] if ',' in string else string
    return temp.lstrip('#').lstrip('(').rstrip(')')


def parseExpr(expr):
    for op in ['+', '-', '*', '/', '!', '.', '&']:
        terms = expr.split(op)
        if len(terms) > 1:
            val1 = parseExpr(terms[0])
            for term in terms[1:]:
                val2 = parseExpr(term)
                if op == '+':
                    val1 += val2
                elif op == '-':
                    val1 -= val2
                elif op == '*':
                    val1 *= val2
                elif op == '/':
                    val1 /= val2
                elif op == '!':
                    val1 ^= val2
                elif op == '.':
                    val1 |= val2
                else:
                    val1 &= val2
            return val1

    return toBase10(expr)


def read(filename):
    global errors, o_lines, symbol_table, start, end
    lines = []
    start = 32768  # = $8000
    end = 32768

    with open(f'sample_files/{filename}.s', 'r') as file:
        line_num = 0
        for line in file:
            size = 1
            line_num += 1
            label = line[0:9].strip()
            op = line[9:12]
            val = line[12:line.find(';')].strip()
            errors.append(None)

            # Gate checks
            if line[0] == '*':
                continue
            if op == 'END':
                break
            if op == 'CHK':
                end += 1
                o_lines.add(line_num)
                lines.append([1, op, '', line_num])
                continue
            if op == 'ORG':
                start = toBase10(val)
                end = toBase10(val)
                continue
            if op == 'EQU':
                symbol_table[label] = '$' + toBase16(val)
                continue

            # Error checks
            if end > 65535 or len(symbol_table) > 255:
                sys.exit('Memory Full')
            if op not in OP_CODES.keys() or label in OP_CODES.keys():
                sys.exit(f'Bad opcode in line: {line_num}')
            if label in symbol_table.keys():
                errors[line_num - 1] = f'Duplicate symbol in line: {line_num}'
                continue

            if val != '' and op not in BRANCHES:
                for key, value in symbol_table.items():
                    val = val.replace(key, value)
                val = val.replace(sanitize(val), '$' + toBase16(parseExpr(sanitize(val))))

            if op in BRANCHES:
                size += 1
            elif op in JUMPS or len(sanitize(val)) > 3:
                size += 2
            elif val != '':
                size += 1

            o_lines.add(line_num)
            lines.append([size, op, val, line_num])
            if label != '':
                symbol_table[label] = '$' + toBase16(end)

            end += size

    return lines


def write(filename, lines):
    global errors, o_lines, symbol_table
    with open(f'out_files/{filename}.o', 'w') as file:
        checksum = []
        address = start
        for line in lines:
            offset = 0
            op = line[1]
            val = line[2]
            line_num = line[3]

            if op == 'CHK':
                chk = toBase16(parseExpr('!'.join(checksum)))
                checksum.append('$' + chk)
                file.write((toBase16(address) + ': ' + chk).strip(' ') + '\n')
                continue

            if op in BRANCHES:
                mode = 'rel'
                rel = toBase10(val) - address - 2
                if rel > 127 or rel < -128:  # Error check
                    offset += 2
                    o_lines.remove(line_num)
                    errors[line_num - 1] = f'Bad branch in line: {line_num}'
                    continue

                rel = rel if rel >= 0 else (256 + rel)
                val1 = toBase16(rel)
                val2 = ''
            else:
                mode, val1, val2 = addressMode(val)

            if mode not in OP_CODES[op].keys():
                o_lines.remove(line_num)
                offset += line[0]
                errors[line_num - 1] = f'Bad address mode in line: {line_num}'
                continue

            checksum.append('$' + OP_CODES[op][mode])
            if val1 != '':
                checksum.append('$' + val1)
            if val2 != '':
                checksum.append('$' + val2)

            file.write(' '.join([toBase16(address) + ':', OP_CODES[op][mode], val1, val2]).strip(' ') + '\n')

            address += line[0] - offset


def prettyPrint(order):
    if order == 'alpha':
        string = []
        for key in sorted(symbol_table):
            string.append(f'{key: <9}={symbol_table[key]: <9}')
        print(*string)
    else:
        string = []
        for key_val in sorted(symbol_table.items(), key=lambda item: toBase10(item[1])):
            string.append(f'{key_val[0]: <9}={key_val[1]: <9}')
        print(*string)


def console_out(filename):
    global errors, symbol_table, start, end
    with open(f'sample_files/{filename}.s', 'r') as source:
        with open(f'out_files/{filename}.o', 'r') as o:
            print('Assembling')
            count = 0
            line_num = 0
            for line in source:
                if errors[line_num] is not None:
                    count += 1
                    input(errors[line_num])

                code = ''
                line_num += 1
                if line_num in o_lines:
                    code = o.readline().strip()

                print(f'{code: <15}{line_num: >3} {line.rstrip()}')

            print(f'\n--End assembly, {end - start} bytes, Errors: {count}')
            print('\nSymbol table - alphabetical order:')
            prettyPrint('alpha')
            print('\nSymbol table - numerical order:')
            prettyPrint('num')


def main():
    if len(sys.argv) < 2:
        filename = input('Source Code File: ')
    else:
        filename = sys.argv[1]
    filename = filename.strip().rstrip('.s')

    lines = read(filename)
    write(filename, lines)
    console_out(filename)


if __name__ == '__main__':
    main()
