def make_transaction_description(ballots, transaction):
    
    separators = ['Za', 'AZ', 'pP', 'Vz', 'vh', 'pH']
    
    dictionary = {
        '1': 'f', '2': 'w', '3': 'g', '4': 'F', '5': 'G', 
        '6': 'T', '7': 'R', '8': 'Q', '9': 'y', '0': 'W'
    }
    
    ballot_ids = [ballot.id for ballot in ballots]
    
    ballot_numbers = [ballot.number for ballot in ballots]
    
    reference = '  '.join([str(transaction.id), ' '.join([str(i) for i in ballot_ids])]) 
    
    from random import randint
    
    items = reference.split('  ')
    
    encoded_items = []
    
    for item in items:
        encoded_item = ""
        
        for char in item:
            
            if char == ' ':
                encoded_item += separators[randint(0, len(separators)-1)]
            else:
                encoded_item += dictionary[char]
                
        encoded_items.append(encoded_item)
        
    encoded_ref = ''.join(
        [separators[randint(0, len(separators)-1)], 
         separators[randint(0, len(separators)-1)]]            
    ).join(encoded_items)
    
    description = "Compra de balotas. Numeros " + ", ".join([str(i) for i in ballot_numbers]) + " ref " + encoded_ref
    
    return description
    
def get_values_from_transaction_description(string):
    
    separators = ['Za', 'AZ', 'pP', 'Vz', 'vh', 'pH']
    reverse_dict = {
        'f': '1', 'w': '2', 'g': '3', 'F': '4', 'G': '5', 
        'T': '6', 'R': '7', 'Q': '8', 'y': '9', 'W': '0'
    }
    
    ballot_numbers = [int(i) for i in string.split(' ref ')[0].split(' Numeros ')[1].split(', ')]
    
    encoded_ref = string.split(' ref ')[1]
    
    from itertools import product
    
    perm = product([i for i in range(len(separators))], repeat=2)
    
    sep_patterns = '|'.join([''.join([separators[i[0]], separators[i[1]]]) for i in list(perm)])
    

    import re
    
    encoded_items = re.split(sep_patterns, encoded_ref)
    
    items = []
    
    for encoded_item in encoded_items:
        item = []
        encoded_chars = re.split('|'.join(separators), encoded_item)
        items.append(encoded_chars)
    
    decoded_items = []
    
    for item in items:
        decoded_item_chars = []
        
        for value in item:
            digits = []
            
            for encoded_digit in value:
                digits.append(reverse_dict[encoded_digit])
                
            decoded_item_chars.append(int("".join(digits)))
            
        decoded_items.append(decoded_item_chars)
    
    data = {
        'transaction_id': decoded_items[0][0], 
        'ballot_ids': decoded_items[1], 
        'ballot_numbers': ballot_numbers
    }
    
    return data