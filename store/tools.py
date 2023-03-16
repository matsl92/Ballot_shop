# x_description = "96 Compra de balotas. Numeros 8, 13, 14"
x_description = "94 Compra de balotas. Numeros 8"


def get_ballot_ids_from_x_description(x_description):
    items = x_description.split(' ')
    items.pop(0)
    ballot_ids =[]
    for item in items:
        try:
            ballot_id = int(item.strip(','))
            ballot_ids.append(ballot_id)
        except:
            pass

    return(ballot_ids)
