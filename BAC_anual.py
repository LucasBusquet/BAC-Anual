# Importo las librerias que voy a usar
import pandas as pd
import numpy as np

# Importo el dataset y me quedo con un subset que considero importante
bac_anual = pd.read_csv(
    "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-economia-y-finanzas/buenos-aires-compras/bac_anual.csv",
    usecols=[
        "id",
        "date",
        "tender/status",
        "tender/items/0/quantity",
        "awards/0/items/0/quantity",
        "tender/value/currency",
        "tender/value/amount",
        "tender/mainProcurementCategory",
        "tender/procurementMethod",
        "tender/procurementMethodDetails",
        "tender/items/0/unit/value/amount",
        "tender/items/0/unit/value/currency",
        "tender/procurementMethod",
        "awards/0/value/amount",
        "awards/0/value/currency",
        "awards/0/items/0/unit/value/amount",
        "awards/0/items/0/unit/value/currency",
        "contracts/0/items/0/unit/value/amount",
        "contracts/0/items/0/quantity",
        "contracts/0/value/amount",
        "contracts/0/value/currency",
    ],
)

# Ahora voy a eliminar valores que aparecen duplicados, difieren de los ultimos dos digitos del 'id'
bac_anual["id"] = bac_anual["id"].str[:-2]
bac_anual = bac_anual.drop_duplicates(subset="id")

# Me voy a quedar con las licitación que estan terminadas
bac_anual = bac_anual[bac_anual["tender/status"] == "complete"]

# Cambiando USD y EUR a ARS (Puede que el valor este desactualizado)
for i in range(len(bac_anual["id"])):
    if (
        bac_anual["awards/0/value/currency"].iloc[i] == "USD"
        or bac_anual["tender/value/currency"].iloc[i] == "USD"
    ):
        bac_anual["tender/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["tender/items/0/unit/value/amount"].iloc[i] * 176
        )
        bac_anual["awards/0/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["awards/0/items/0/unit/value/amount"].iloc[i] * 176
        )
        bac_anual["contracts/0/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["contracts/0/items/0/unit/value/amount"].iloc[i] * 176
        )

    elif (
        bac_anual["awards/0/value/currency"].iloc[i] == "EUR"
        or bac_anual["tender/value/currency"].iloc[i] == "EUR"
    ):
        bac_anual["tender/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["tender/items/0/unit/value/amount"].iloc[i] * 189
        )
        bac_anual["awards/0/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["awards/0/items/0/unit/value/amount"].iloc[i] * 189
        )
        bac_anual["contracts/0/items/0/unit/value/amount"].iloc[i] = (
            bac_anual["contracts/0/items/0/unit/value/amount"].iloc[i] * 189
        )

# Multiplico lo que vale la unidad por la cantidad de unidades para chequear el total
bac_anual["Total_tender_amount"] = bac_anual[
    "tender/items/0/unit/value/amount"
].multiply(bac_anual["tender/items/0/quantity"])
bac_anual["Total_award_amount"] = bac_anual[
    "awards/0/items/0/unit/value/amount"
].multiply(bac_anual["awards/0/items/0/quantity"])
bac_anual["Total_contracts_amount"] = bac_anual[
    "contracts/0/items/0/unit/value/amount"
].multiply(bac_anual["contracts/0/items/0/quantity"])

# Cambio el dia a '%Y/%m/%d'
bac_anual["date"] = bac_anual["date"].str[:10]

# Dropeo algunas columnas que ahora sobran
bac_anual = bac_anual.drop(
    [
        "tender/value/currency",
        "awards/0/items/0/unit/value/currency",
        "awards/0/value/currency",
        "contracts/0/value/currency",
        "tender/items/0/unit/value/currency",
        "tender/status",
        "tender/items/0/unit/value/amount",
        "awards/0/items/0/unit/value/amount",
        "tender/items/0/quantity",
        "awards/0/items/0/quantity",
        "tender/value/amount",
        "awards/0/value/amount",
        "contracts/0/items/0/quantity",
        "contracts/0/items/0/unit/value/amount",
        "contracts/0/value/amount",
    ],
    axis=1,
)

print(bac_anual)
# Exporto el Dataframe como .xls
bac_anual.to_excel("bac_anual.xlsx", sheet_name="sheet1", index=False)
