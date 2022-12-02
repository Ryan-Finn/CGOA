def main():
    lines = []
    symbol_table = {}
    equs = {}
    op_codes = {
        'BRK': {'impl': '00'},
        'ORA': {'X,ind': '01', 'ind,Y': '11', 'zpg': '05', 'zpg,X': '15', '#': '09', 'abs,Y': '19', 'abs': '0D',
                'abs,X': '1D'},
        'ASL': {'zpg': '06', 'zpg,X': '16', 'A': '0A', 'abs': '0E', 'abs,X': '1E'},
        'PHP': {'impl': '08'},
        'BPL': {'rel': '10'},
        'CLC': {'impl': '18'},
        'JSR': {'abs': '20'},
        'AND': {'X,ind': '21', 'ind,Y': '31', 'zpg': '25', 'zpg,X': '35', '#': '29', 'abs,Y': '39', 'abs': '2D',
                'abs,X': '3D'},
        'BIT': {'zpg': '24', 'abs': '2C'},
        'ROL': {'zpg': '26', 'zpg,X': '36', 'A': '2A', 'abs': '2E', 'abs,X': '3E'},
        'PLP': {'impl': '28'},
        'BMI': {'rel': '30'},
        'SEC': {'impl': '38'},
        'RTI': {'impl': '40'},
        'EOR': {'X,ind': '41', 'ind,Y': '51', 'zpg': '45', 'zpg,X': '55', '#': '49', 'abs,Y': '59', 'abs': '4D',
                'abs,X': '5D'},
        'LSR': {'zpg': '46', 'zpg,X': '56', 'A': '4A', 'abs': '4E', 'abs,X': '5E'},
        'PHA': {'impl': '48'},
        'JMP': {'abs': '4C', 'ind': '6C'},
        'BVC': {'rel': '50'},
        'CLI': {'impl': '58'},
        'RTS': {'impl': '60'},
        'ADC': {'X,ind': '61', 'ind,Y': '71', 'zpg': '65', 'zpg,X': '75', '#': '69', 'abs,Y': '79', 'abs': '6D',
                'abs,X': '7D'},
        'ROR': {'zpg': '66', 'zpg,X': '76', 'A': '6A', 'abs': '6E', 'abs,X': '7E'},
        'PLA': {'impl': '68'},
        'BVS': {'rel': '70'},
        'SEI': {'impl': '78'},
        'STA': {'X,ind': '81', 'ind,Y': '91', 'zpg': '85', 'zpg,X': '95', 'abs,Y': '99', 'abs': '8D', 'abs,X': '9D'},
        'STY': {'zpg': '81', 'zpg,Y': '91', 'abs': '8C'},
        'STX': {'zpg': '86', 'zpg,Y': '96', 'abs': '8E'},
        'DEY': {'impl': '88'},
        'TXA': {'impl': '8A'},
        'BCC': {'rel': '90'},
        'TYA': {'impl': '98'},
        'TXS': {'impl': '9A'},
        'LDY': {'#': 'A0', 'zpg': 'A4', 'zpg,X': 'B4', 'abs': 'AC', 'abs,X': 'BC'},
        'LDA': {'X,ind': 'A1', 'ind,Y': 'B1', 'zpg': 'A5', 'zpg,X': 'B5', '#': 'A9', 'abs,Y': 'B9', 'abs': 'AD',
                'abs,X': 'BD'},
        'LDX': {'#': 'A2', 'zpg': 'A6', 'zpg,Y': 'B6', 'abs': 'AE', 'abs,Y': 'BE'},
        'TAY': {'impl': 'A8'},
        'TAX': {'impl': 'AA'},
        'BCS': {'rel': 'B0'},
        'CLV': {'impl': 'B8'},
        'TSX': {'impl': 'BA'},
        'CPY': {'#': 'C0', 'zpg': 'C4', 'abs': 'CC'},
        'CMP': {'X,ind': 'C1', 'ind,Y': 'D1', 'zpg': 'C5', 'zpg,X': 'D5', '#': 'C9', 'abs,Y': 'D9', 'abs': 'CD',
                'abs,X': 'DD'},
        'DEC': {'zpg': 'C6', 'zpg,X': 'D6', 'abs': 'CE', 'abs,X': 'DE'},
        'INY': {'impl': 'C8'},
        'DEX': {'impl': 'CA'},
        'BNE': {'rel': 'D0'},
        'CLD': {'impl': 'D8'},
        'CPX': {'#': 'E0', 'zpg': 'E4', 'abs': 'EC'},
        'SBC': {'X,ind': 'E1', 'ind,Y': 'F1', 'zpg': 'E5', 'zpg,X': 'F5', '#': 'E9', 'abs,Y': 'F9', 'abs': 'ED',
                'abs,X': 'FD'},
        'INC': {'zpg': 'E6', 'zpg,X': 'F6', 'abs': 'EE', 'abs,X': 'FE'},
        'INX': {'impl': 'E8'},
        'NOP': {'impl': 'EA'},
        'BEQ': {'rel': 'F0'},
        'SED': {'impl': 'F8'},
    }
    address = 32768  # = $8000

    with open('sample_files/sample_2.s', 'r') as file:
        for line in file:
            if line[0] != '*':
                label = line[0:9].strip()
                op = line[9:12]
                val = line[14:line.find(';')].strip()

                if op == 'ORG':
                    if val[0] == '$':
                        address = int(val[1:], 16)
                    elif val[0] == '%':
                        address = int(val[1:], 2)
                    else:
                        address = int(val)
                elif op == 'EQU':
                    if val[0] == '$':
                        equs[line[0:9].strip()] = int(val[1:], 16)
                        symbol_table[line[0:9].strip()] = int(val[1:], 16)
                    elif val[0] == '%':
                        equs[line[0:9].strip()] = int(val[1:], 2)
                        symbol_table[line[0:9].strip()] = int(val[1:], 2)
                    else:
                        equs[line[0:9].strip()] = int(val)
                        symbol_table[line[0:9].strip()] = int(val)
                else:
                    if val in equs:
                        lines.append([label, op, equs[val]])
                    else:
                        lines.append([label, op, val])

                    if label != '':
                        symbol_table[label] = address

                    address += 1
                    if val != '':
                        address += 1 + int(val in equs and equs[val] > 255)
        print(lines)
        print(symbol_table)

    # with open('out_files/sample_1.o', 'w') as file:
    #     line = lines[0]
    #     row = ''
    #     if line[1] == 'ORG':
    #         row += line[2].replace('$', '') + ': '
    #     else:
    #         row += '8000: '
    #
    #     for line in lines[1:]:
    #         file.write((line[0] + ' ' * (9 - len(line[0])) + line[1] + '  ' + line[2]).rstrip() + '\n')


if __name__ == '__main__':
    main()
