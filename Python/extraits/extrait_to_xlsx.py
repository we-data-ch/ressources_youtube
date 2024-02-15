import pdfplumber
import pandas as pd
import sys

# keys: ['text', 'x0', 'x1', 'top', 'doctop', 'bottom', 'upright', 'direction']

# get x0, x1, text
def get_coords(word):
    return [word["x0"], word["top"], word["text"]]


def get_x_from_Name(df, name):
    return df.query(f"content == '{name}'")[["x"]].iloc[0, 0]


def get_y_from_Name(df, name):
    return df.query(f"content == '{name}'")[["y"]].iloc[0, 0]


def get_table_header(df):
    return get_y_from_Name(df, "Date")


def get_x_columns(df):
    # On ne prend pas la solde
    return {"Date": get_x_from_Name(df, "Date"),
            "Description": get_x_from_Name(df, "Description"),
            "Valeur": get_x_from_Name(df, "Valeur"),
            "Débit": get_x_from_Name(df, "Débit"),
            "Crédit": get_x_from_Name(df, "Crédit")}


def get_table_content(page_content, columns_pos, table_header):
    positions = [columns_pos["Date"], columns_pos["Valeur"]]
    # position[3] = Débit, position[4] = Crédit
    credit_interval = [columns_pos["Débit"]+1, columns_pos["Crédit"]]
    debit_interval = [columns_pos["Valeur"]+1, columns_pos["Débit"]]
    description_interval = [columns_pos["Description"], columns_pos["Valeur"]-1]
    date_valeur = page_content.query(f"x in {positions} and y > {table_header}")
    credit = page_content.query(f"x >= {credit_interval[0]} and x <= {credit_interval[1]}")
    debit = page_content.query(f"x >= {debit_interval[0]} and x <= {debit_interval[1]}")
    description = page_content.query(f"x >= {description_interval[0]} and x <= {description_interval[1]}")
    return pd.concat([date_valeur, credit, debit, description])


def get_lines(table_content):
    return table_content.y.unique()


def get_elements_from_line(table_content, line):
    return table_content.query(f"y == {line}").sort_values(by=["x"])


def create_descriptions(df):
    description = ""
    for index, row in df.sort_index().iterrows():
        description += " "+row["content"]
    return description[1:]


def create_row(rows, columns_pos):
    row = []
    for column in ["Date"]:
        pos = columns_pos[column]
        line = rows.query(f"x == {pos}")
        if not line.empty:
            row.append(line.values[0][2])
        else:
            row.append(0)
    credit_interval = [columns_pos["Débit"]+1, columns_pos["Crédit"]]
    debit_interval = [columns_pos["Valeur"]+1, columns_pos["Débit"]]
    description_interval = [columns_pos["Description"], columns_pos["Valeur"]-1]
    description = rows.query(f"x >= {description_interval[0]} and x <= {description_interval[1]}")
    if not description.empty:
        row.append(create_descriptions(description))
    else:
        row.append(0)
    for column in ["Valeur"]:
        pos = columns_pos[column]
        line = rows.query(f"x == {pos}")
        if not line.empty:
            row.append(line.values[0][2])
        else:
            row.append(0)
    credit = rows.query(f"x >= {credit_interval[0]} and x <= {credit_interval[1]}")
    if not credit.empty:
        row.append(credit.values[0][2])
    else:
        row.append(0)
    debit = rows.query(f"x >= {debit_interval[0]} and x <= {debit_interval[1]}")
    if not debit.empty:
        row.append(debit.values[0][2])
    else:
        row.append(0)
    return row


def create_dataframe(table_content, columns_pos):
    csv = []
    lines = get_lines(table_content)
    for line in lines:
        elements = get_elements_from_line(table_content, line)
        row = create_row(elements, columns_pos)
        csv.append(row)
    return pd.DataFrame(csv, columns=["Date", "Description", "Valeur", "Débit", "Crédit"])


def to_dataframe(page):
    try:
        array2D = list(map(get_coords, page.extract_words()))
        page_content = pd.DataFrame(array2D, columns=["x", "y", "content"])
        table_header = get_table_header(page_content)
        columns_pos = get_x_columns(page_content)
        table_content = get_table_content(page_content, columns_pos, table_header)
        return create_dataframe(table_content, columns_pos)
    except:
        return None


with pdfplumber.open(sys.argv[1]) as temp:
    pages = []
    for page in temp.pages:
        if page is not None:
            pages.append(to_dataframe(page))
    total = pd.concat(pages).query("Date != 0")
    total.to_excel("extrait.xlsx", sheet_name="extrait")
