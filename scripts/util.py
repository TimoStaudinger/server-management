def print_table(list, columns):
    widths = []
    for k, column in enumerate(columns):
        width = max(map(lambda item: len(str(item[column])), list))
        widths.append(max([width, len(columns[k])]))

    extended_widths = [3]
    extended_widths.extend(widths)

    width = sum(extended_widths) + len(extended_widths) - 1

    string_widths = map(lambda width: str(width), extended_widths)
    format_string = '{:<' + '} {:<'.join(string_widths) + '}'

    print format_string.format('key', *columns)
    print ('-' * width)
    for k, item in enumerate(list):
        values = map(lambda column: item[column], columns)
        print format_string.format(k, *values)
