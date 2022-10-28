def parse(path):
    print("Parsing Path: ", path)
    file = open(path, 'r')

    lines = file.readlines()

    output = []
    current = ["", "", False]
    mode = False

    ranges = []

    for line in lines:
        l = line.rstrip()
        if len(l) > 0 and l[0] == ">" and not mode:
            current[0] = l[1:]
            current[1] = ""
            current[2] = False
            mode = True
            continue

        if len(l) > 0 and l[0:2] == "@>" and not mode:
            current[0] = l[2:]
            current[1] = ""
            current[2] = True
            mode = True
            continue

        if l[0:7] == "RANGES:":
            rest = l[7:]
            rs = rest.split(",")
            ranges = [tuple([int(x.strip()) for x in r.split("-")]) for r in rs]
            ranges = [(i-1, j) for (i, j) in ranges]
        
        if mode:
            if len(l) == 0:
                if current[1]:
                    output.append(tuple(current))
                mode = False
                continue
            current[1] += l

    if current[1]:
        output.append(tuple(current))

    acceptor = [(n, s) for (n, s, a) in output if a]
    if not acceptor:
        raise "No acceptor found. Use @> to nominate"
    acceptor = acceptor[0]

    donors = [(n, s) for (n, s, a) in output if not a]
    


    return ranges, acceptor, donors


def replace(ranges, acceptor, donors):
    output = []
    an, a = acceptor
    for n, d in donors:
        last = 0
        new = ""
        for i, j in ranges:
            new += a[last:i]
            new += d[i:j]
            last = j

        new += a[last:]

        output.append((n + f" - [[{an}]]", new))

    return output

def remove_dashes_str(str):
    return "".join([l for l in str if l != "-"])

def remove_dashes(list):
    return [(n, remove_dashes_str(ls)) for n, ls in list]

def write_antibodies_to_file(path, bodies):
    outtext = ""
    for n, s in bodies:
        outtext += f"> {n}\n{s}\n\n"
    f = open(path, "w")
    f.write(outtext)
    f.close()

def run_on_file(path, outpath, write = True):
    ranges, acceptor, donors = parse(path)
    output = replace(ranges, acceptor, donors)
    output = remove_dashes(output)
    if write:
        write_antibodies_to_file(outpath, output)
    return output, acceptor, donors, ranges

def run_on_directory(path, outpath, write = True):
    import os
    files = [f for f in os.listdir(path) if f[0] != "."]
    inpaths = [os.path.join(path, p) for p in files]
    outpaths = [os.path.join(outpath, p) + ".output" for p in files]
    
    outputs = []
    for ip, op, f in zip(inpaths, outpaths, files):
        o = run_on_file(ip, op, write)
        outputs.append((f, o))

    return outputs
    

def write_xlsx_file(filename, data, db, db_rev):
    import xlsxwriter
    workbook = xlsxwriter.Workbook(filename)

    for (file, (output, acceptor, donors, ranges)) in data:
        sheet = workbook.add_worksheet(file)

        # Write header
        header = ["CD", "ID", "Antibody Sequence", "CDR1", "CDR2", "CDR3", "Moon NB Graft"]
        for i, h in enumerate(header):
            sheet.write(0, i, h)



        donors_dash_rm = remove_dashes(donors)
        for i, ((dname, dseq), (oname, oseq), (dnamerm, dseqrm)) in enumerate(zip(donors, output, donors_dash_rm)):

            #Write sequences
            sheet.write(i + 1, 2, dseqrm)
            sheet.write(i + 1, 6, oseq)
            
            # write cdrs
            for j in range(3):
                r1, r2 = ranges[j]
                cdr = dseq[r1:r2]
                sheet.write(i+1, 3 + j, remove_dashes_str(cdr))

            # write ids
            id = dname.strip().split(" ")[0]
            if id[:2] == "CD":
                sheet.write(i+1, 0, id)
                if id in db_rev:
                    sheet.write(i+1, 1, db_rev[id])
            else:
                sheet.write(i+1, 1, id)
                if id in db:
                    sheet.write(i+1, 0, db[id])


    workbook.close()