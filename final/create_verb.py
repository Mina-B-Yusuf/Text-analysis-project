import zipfile
import xml.etree.ElementTree as ET
import json


def read_xlsx_no_dependencies(filepath):
    """
    Reads an Excel .xlsx file WITHOUT openpyxl, xlrd, pandas, or external tools.
    Returns a list of rows, each row is a list of cell values.
    """
    with zipfile.ZipFile(filepath, 'r') as z:

        # Read shared strings (the text stored in xlsx)
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss = z.read("xl/sharedStrings.xml")
            root = ET.fromstring(ss)
            for si in root:
                text = ""
                for t in si:
                    if t.text:
                        text += t.text
                shared_strings.append(text)

        # Read sheet1.xml
        sheet = z.read("xl/worksheets/sheet1.xml")
        root = ET.fromstring(sheet)

        rows = []
        for row in root.iter():
            if row.tag.endswith("row"):
                row_values = []
                for c in row:
                    if c.tag.endswith("c"):
                        cell_type = c.attrib.get("t")
                        v = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")

                        if v is None:
                            row_values.append("")
                        else:
                            val = v.text
                            if cell_type == "s":
                                # shared string index
                                row_values.append(shared_strings[int(val)])
                            else:
                                row_values.append(val)
                rows.append(row_values)
        return rows


def create_reverse_verb_dictionary(excel_path="Verbs.xlsx",
                                   output_json="verbs_reverse.json"):

    print("Reading .xlsx without openpyxl...")

    rows = read_xlsx_no_dependencies(excel_path)

    # Remove header (first row)
    rows = rows[1:]

    reverse_dict = {}

    for row in rows:
        if len(row) == 0:
            continue

        base = str(row[0]).strip().lower()
        if base == "":
            continue

        for form in row:
            form = str(form).strip().lower()
            if form != "":
                reverse_dict[form] = base

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(reverse_dict, f, indent=4, ensure_ascii=False)

    print(f"Reverse verb dictionary saved as {output_json}")
    print(f"Entries: {len(reverse_dict)}")


if __name__ == "__main__":
    create_reverse_verb_dictionary()
    